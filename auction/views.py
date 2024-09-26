from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DeleteView

from auction.models import Aukce, Kategorie, Bid
from aukce.forms import BidForm, SignUpForm, AukceForm


class SignUpView(CreateView):
    template_name = "accounts/sign_up.html"
    form_class = SignUpForm
    success_url = reverse_lazy("hlavni_stranka")


class SubmittableLoginView(LoginView):
    template_name = 'form.html'

class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html'

class SubmittablePasswordResetView(PasswordResetView):
    template_name = "accounts/reset_password.html"



def hlavni_stranka(request):
    return render(request, 'hlavni_stranka.html')

class SeznamAukciView(ListView):
    model = Aukce
    template_name = 'seznam_aukci.html'
    context_object_name = "aktivni_aukce"

    def get_queryset(self):
        return Aukce.objects.filter(datum_zacatku__lte=timezone.now(), datum_ukonceni__gte=timezone.now())

def aukcni_stranka(request, aukce_id):
    aukce = get_object_or_404(Aukce, id=aukce_id)
    bids = aukce.bids.all()

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.aukce = aukce
            bid.uzivatel = request.user
            bid.save()
            return redirect("aukcni_stranka", aukce_id=aukce_id)
    else:
        form = BidForm()

    return render(request, "aukcni_stranka.html", {'aukce': aukce, 'bids': bids, 'form': form})

# zobrazení všech kategorií
def seznam_kategorii(request):
    kategorie = Kategorie.objects.all()
    return render(request, 'seznam_kategorii.html', {'kategorie': kategorie})

# zobrazení aukcí v konkrétních kategorií
def aukce_v_kategorii(request, kategorie_id):
    kategorie = get_object_or_404(Kategorie, id=kategorie_id)
    aukce_v_kategorii = Aukce.objects.filter(kategorie=kategorie)
    return render(request, 'aukce_v_kategorii.html', {'aukce': aukce_v_kategorii, 'kategorie': kategorie})

class VytvoritKategoriiView(PermissionRequiredMixin, CreateView):
    model = Kategorie
    template_name = 'vytvorit_kategorii.html'
    fields = ['nazev']
    success_url = reverse_lazy('seznam_kategorii')
    permission_required = 'auction.muze_vytvorit_kategorii'

class VytvorAukciView(LoginRequiredMixin, CreateView):
    model = Aukce
    form_class = AukceForm
    template_name = 'vytvor_aukci.html'
    success_url = reverse_lazy('seznam_aukci')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SmazatAukciView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Aukce
    template_name = 'smazat_aukci.html'
    success_url = reverse_lazy('seznam_aukci')

    def test_func(self):
        aukce = self.get_object()
        # Aukci může smazat pouze uživatel který ji vytvořil nebo admin,
        return self.request.user == aukce.user or self.request.user.is_superuser