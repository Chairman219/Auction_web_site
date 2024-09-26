from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from auction.models import Bid, Aukce

class SignUpForm(UserCreationForm):

  class Meta(UserCreationForm.Meta):
    fields = ["username", "first_name"]

    def save(self, commit=True):
      self.instance.is_active = False # výběr toho zda jsou nově vytvořené účty uživatelů ihned aktivní nebo ne, False = ne True = ano
      return super().save(commit)

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["castka"]

class AukceForm(ModelForm):
    class Meta:
        model = Aukce
        fields = ['nazev', 'popis', 'kategorie', 'minimalni_prihoz', 'castka_kup_ted', 'propagace', 'lokalita', 'datum_zacatku', 'datum_ukonceni']