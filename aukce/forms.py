from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Model
from django.forms import EmailField, Textarea, ChoiceField
from django.db.transaction import atomic
from django.forms import ModelForm, Form, ModelChoiceField, DateField, DecimalField
from django.forms import CharField

from auction.models import Bid, Aukce, Kategorie, Profile, Hodnoceni


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email']

    city = CharField(widget=Textarea, min_length=1)
    adress = CharField(widget=Textarea, min_length=1)

    #Volba pro typ účtu
    PREMIUM_CHOICES = [
        (False, "Normální účet"),
        (True, "Premium účet")
    ]
    is_premium = ChoiceField(choices=PREMIUM_CHOICES, label="Typ účtu")

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email']

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)

        city = self.cleaned_data['city']
        adress = self.cleaned_data['adress']
        is_premium = self.cleaned_data['is_premium'] == 'True'
        profile = Profile(city=city, adress=adress, user=result, waiting_for_premium_confirmation=is_premium)
        if commit:
            profile.save()
        return result


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["castka"]

class AukceForm(ModelForm):
    class Meta:
        model = Aukce
        fields = ['nazev', 'popis', 'kategorie', 'minimalni_prihoz', 'castka_kup_ted', 'datum_zacatku', 'datum_ukonceni', 'image']

class AuctionSearchForm(Form):
    nazev = CharField(required=False)
    kategorie = ModelChoiceField(queryset=Kategorie.objects.all(), required=False)
    minimalni_prihoz = DecimalField(required=False, min_value=0)
    castka_kup_ted = DecimalField(required=False, min_value=0)
    datum_zacatku = DateField(required=False)

class HodnoceniForm(ModelForm):
    class Meta:
        model = Hodnoceni
        fields = ['rating_aukce', 'rating_prodejce', 'komentar_k_aukci']

class KategorieForm(ModelForm):
    class Meta:
        model = Kategorie
        fields = ['nazev','logo']