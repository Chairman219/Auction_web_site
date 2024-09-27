from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic
from django.forms import ModelForm, Form, ModelChoiceField, DateField, DecimalField
from django.forms import CharField

from auction.models import Bid, Aukce, Profile, Kategorie

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'email']

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)
        profile = Profile(user=result)
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
        fields = ['nazev', 'popis', 'kategorie', 'minimalni_prihoz', 'castka_kup_ted', 'propagace', 'lokalita', 'datum_zacatku', 'datum_ukonceni']

class AuctionSearchForm(Form):
    nazev = CharField(required=False)
    kategorie = ModelChoiceField(queryset=Kategorie.objects.all(), required=False)
    minimalni_prihoz = DecimalField(required=False, min_value=0)
    datum_zacatku = DateField(required=False)