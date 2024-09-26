from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from auction.models import Bid, Aukce, CustomUser

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "mesto", "adresa", "typ_uctu"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user
class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["castka"]

class AukceForm(ModelForm):
    class Meta:
        model = Aukce
        fields = ['nazev', 'popis', 'kategorie', 'minimalni_prihoz', 'castka_kup_ted', 'propagace', 'lokalita', 'datum_zacatku', 'datum_ukonceni']