from datetime import timedelta
from lib2to3.fixes.fix_input import context

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from platformdirs import user_log_path
from django.contrib import messages
from django.urls import reverse
from auction.models import Aukce, Kategorie, Bid
from aukce.forms import BidForm, AukceForm, AuctionSearchForm, SignUpForm, HodnoceniForm, KategorieForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/sign_up.html"
    success_url = reverse_lazy("hlavni_stranka")

    def form_valid(self, form):
        response = super().form_valid(form)
        profile = self.object.profile

        login(self.request, self.object) # Automatické přihlášení po registraci

        # Pokud uživatel zvolil premium, přesměrujeme ho na stránku s potvrzením
        if profile.waiting_for_premium_confirmation:
            return redirect('premium_confirmation')

        return response

@login_required
def upgrade_to_premium(request):
    profile = request.user.profile
    if not profile.is_premium:
        profile.is_premium = True
        profile.save()
        messages.success(request, "Váš účet byl úspěšně upgradován na PREMIUM.")
    else:
        messages.error(request, "Jste již premium uživatel.")

    return redirect("muj_profil")

@login_required
def premium_confirmation(request):
    profile = request.user.profile
    # Pokud uživatel nečeká na potvrzení premium, přesměrujeme ho na hlavní stránku
    if not profile.waiting_for_premium_confirmation:
        return redirect('hlavni_stranka')

    # Pokud uživatel souhlasí s přechodem na premium
    if request.method == 'POST':
        if 'confirm_premium' in request.POST:
            profile.is_premium = True
            profile.waiting_for_premium_confirmation = False
            profile.save()
            return redirect('muj_profil')

        # Pokud uživatel odmítne premium, bude vytvořen normální účet
        elif 'cancel_premium' in request.POST:
            profile.is_premium = False
            profile.waiting_for_premium_confirmation = False
            profile.save()
            return redirect('muj_profil')

    return render(request, 'premium_confirmation.html', {'user': request.user})

class SubmittableLoginView(LoginView):
    template_name = 'form.html'

class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html'

class SubmittablePasswordResetView(PasswordResetView):
    template_name = "accounts/reset_password.html"

@login_required
def muj_profil(request):
    user = request.user
    sledovane_aukce = user.sledovane_aukce.all()
    aukce = Aukce.objects.filter(user=user, status='ACTIVE')
    vyhrane_aukce = Aukce.objects.filter(Q(vitez=user) | Q(user=user,status='ENDED'))
    dnesni_den = timezone.now().date()
    pocet_aukci_dnes = Aukce.objects.filter(user=user, datum_zacatku__date=dnesni_den).count()

    if not user.profile.is_premium:
        zbyvajici_aukce = max(3 - pocet_aukci_dnes, 0)
    else:
        zbyvajici_aukce = None


    context = {
        'profile': request.user.profile,
        'aukce': aukce,
        'vyhrane_aukce': vyhrane_aukce,
        'sledovane_aukce': sledovane_aukce,
        'zbyvajici_aukce': zbyvajici_aukce,
    }

    return render(
        request, template_name="muj_profil.html", context=context
    )

def hlavni_stranka(request):
    return render(request, 'hlavni_stranka.html')

class SeznamAukciView(ListView):
    model = Aukce
    template_name = 'seznam_aukci.html'
    context_object_name = "aktivni_aukce"

    def get_queryset(self):
        # Filtruje aukce, které jsou aktuálně aktivní (datum začátku a ukončení)
        return Aukce.objects.filter(status='ACTIVE', datum_zacatku__lte=timezone.now(), datum_ukonceni__gte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['ukoncene_aukce'] = Aukce.objects.filter(status='ENDED')

        now = timezone.now()
        context['skonceni_brzy_aukce'] = Aukce.objects.filter(
            status = 'ACTIVE',
            datum_ukonceni__gt=now,
            datum_ukonceni__lt=now + timedelta(minutes=2)
        )

        return context


def aukcni_stranka(request, aukce_id):
    aukce = get_object_or_404(Aukce, id=aukce_id)
    aukce.pocet_zobrazeni += 1
    aukce.save()

    bids = aukce.bids.all()
    error_message = None
    success_message = None

    form = BidForm()

    if aukce.status == 'ENDED':
        error_message = "Aukce již byla ukončena"

    elif request.method == 'POST':
        if 'koupit_hned' in request.POST:
            if aukce.status == 'ACTIVE':
                aukce.kup_hned(request.user)
                success_message = "Úspěšně jste zakoupili předmět."
                return redirect('muj_profil')
            else:
                error_message = "Aukce již není aktivní."

        else:
            form = BidForm(request.POST)
            if form.is_valid():
                bid_amount = form.cleaned_data['castka']
                if bid_amount < aukce.minimalni_prihoz:
                    error_message = f"Musíte přihodit alespoň {aukce.minimalni_prihoz} Kč."
                else:
                    bid = form.save(commit=False)
                    bid.aukce = aukce
                    bid.uzivatel = request.user
                    bid.save()
                    aukce.sledujici.add(request.user)
                    aukce.update_minimalni_prihoz(bid_amount, request.user)
                    success_message = "Přihoz byl úspěšně zadán"
                    return redirect("aukcni_stranka", aukce_id=aukce_id)
            else:
                error_message = "Nastala chyba při zpracování vašeho příhozu."
    else:
        form = BidForm()

    return render(request, 'aukcni_stranka.html', {
        'aukce': aukce,
        'bids': bids,
        'form': form,
        'error_message': error_message,
        'success_message': success_message,
    })

# zobrazení všech kategorií
def seznam_kategorii(request):
    kategorie = Kategorie.objects.all()
    return render(request, 'seznam_kategorii.html', {'kategorie': kategorie})

# zobrazení aukcí v konkrétních kategorií
def aukce_v_kategorii(request, kategorie_id):
    kategorie = get_object_or_404(Kategorie, id=kategorie_id)
    aukce_v_kategorii = Aukce.objects.filter(kategorie=kategorie)
    return render(request, 'aukce_v_kategorii.html', {'aukce': aukce_v_kategorii, 'kategorie': kategorie})

@login_required
def ohodnotit_aukci(request, aukce_id):
    aukce = get_object_or_404(Aukce, id=aukce_id)

    if request.method == 'POST':
        form = HodnoceniForm(request.POST)
        if form.is_valid():
            hodnoceni = form.save(commit=False)
            hodnoceni.aukce = aukce
            hodnoceni.uzivatel = request.user
            hodnoceni.save()
            return redirect('aukcni_stranka', aukce_id=aukce_id)
    else:
        form = HodnoceniForm()

    return render(request, 'hodnotit_aukci.html', {'form': form, 'aukce': aukce})


class VytvoritKategoriiView(PermissionRequiredMixin, CreateView):
    model = Kategorie
    template_name = 'vytvorit_kategorii.html'
    fields = ['nazev', 'logo']
    success_url = reverse_lazy('seznam_kategorii')
    permission_required = 'auction.muze_vytvorit_kategorii'

class SmazatKategoriiView(PermissionRequiredMixin, DeleteView):
    model = Kategorie
    template_name = 'smazat_kategorii.html'
    success_url = reverse_lazy('seznam_kategorii')
    permission_required = 'auction.delete_kategorie'

class UpravitKategoriiView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Kategorie
    form_class = KategorieForm
    success_url = reverse_lazy('seznam_kategorii')
    permission_required = 'auction.update_kategorie'

class VytvorAukciView(LoginRequiredMixin, CreateView):
    model = Aukce
    form_class = AukceForm
    template_name = 'vytvor_aukci.html'
    success_url = reverse_lazy('seznam_aukci')

    def form_valid(self, form):
        user_profile = self.request.user.profile

        #Kontrola zda uživatel není PREMIUM
        if not user_profile.is_premium:
            #Vyhledávání aukcí, které uživatel dnes vytvořil
            dnesni_den = timezone.now().date()
            pocet_aukci_dnes = Aukce.objects.filter(user=self.request.user, datum_zacatku__date=dnesni_den).count()

            #Pokud uživatel vytvořil více než 3 aukce za den
            if pocet_aukci_dnes >= 3:
                premium_link = reverse('upgrade_to_premium')
                limit_message = (f"Normální uživatel může vytvořit maximálně 3 aukce za jeden den. "
                                 f"Pokud chcete vytvářet více jak tři aukce denně, "
                                 f"změňte si svůj profil na<a href='{premium_link}'> Premium</a>.")
                return self.render_to_response(self.get_context_data(form=form, limit_message=limit_message))

        #Pokud je uživatel PREMIUM, nebo limit není překročen
        form.instance.user = self.request.user
        form.instance.lokalita = self.request.user.profile.city
        return super().form_valid(form)

class SmazatAukciView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Aukce
    template_name = 'smazat_aukci.html'
    success_url = reverse_lazy('seznam_aukci')

    def test_func(self):
        aukce = self.get_object()
        # Aukci může smazat pouze uživatel který ji vytvořil nebo admin,
        return self.request.user == aukce.user or self.request.user.is_superuser

def vyhledavani_aukci(request):
    form = AuctionSearchForm(request.GET or None)
    aukce = Aukce.objects.none()  # Prázdný queryset

    if form.is_valid():
        nazev = form.cleaned_data.get('nazev')
        kategorie = form.cleaned_data.get('kategorie')
        minimalni_prihoz = form.cleaned_data.get('minimalni_prihoz')
        datum_zacatku = form.cleaned_data.get('datum_zacatku')
        castka_kup_ted = form.cleaned_data.get('castka_kup_ted')

        # Vytvoření základního querysetu
        aukce = Aukce.objects.all()  # Získá všechny aukce

        if nazev:
            aukce = aukce.filter(nazev__icontains=nazev)
        if kategorie:
            aukce = aukce.filter(kategorie=kategorie)
        if minimalni_prihoz:
            aukce = aukce.filter(minimalni_prihoz__gte=minimalni_prihoz)
        if datum_zacatku:
            aukce = aukce.filter(datum_zacatku__gte=datum_zacatku)
        if castka_kup_ted:
            aukce = aukce.filter(castka_kup_ted__gte=castka_kup_ted)

    return render(request, 'vyhledavani_aukci.html', {'form': form, 'aukce': aukce})

@login_required
def sleduj_aukci(request, aukce_id):
    aukce = get_object_or_404(Aukce, id=aukce_id)
    aukce.sledujici.add(request.user)
    return redirect('aukcni_stranka', aukce_id=aukce_id)

@login_required
def odhlasit_aukci(request, aukce_id):
    aukce = get_object_or_404(Aukce, id=aukce_id)
    aukce.sledujici.remove(request.user)
    return redirect('aukcni_stranka', aukce_id=aukce_id)