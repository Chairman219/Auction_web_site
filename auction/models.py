from django.template.defaultfilters import default
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, TextField, ForeignKey, CASCADE, DateTimeField, DecimalField, IntegerField, BooleanField, CharField, ImageField



class Kategorie(Model):
    nazev = CharField(max_length=100)

    class Meta:
        permissions = [
            ("muze_vytvorit_kategorii", "Může vytvářet kategorie")
        ]

    def __str__(self):
        return self.nazev

class Aukce(Model):
    nazev = CharField(max_length=100, default="")
    popis = TextField(default="")
    # fotky = ImageField(upload_to="fotky/", blank=True, null=True)
    kategorie = ForeignKey(Kategorie, on_delete=CASCADE)
    minimalni_prihoz = DecimalField(max_digits=10, decimal_places=2, default=0.0)
    castka_kup_ted = DecimalField(max_digits=10, decimal_places=2, default=0.0)
    propagace = BooleanField(default=False)
    lokalita = CharField(max_length=100, default="")
    datum_zacatku = DateTimeField(default=timezone.now)
    datum_ukonceni = DateTimeField(default=timezone.now)
    pocet_zobrazeni = IntegerField(default=0)
    user = ForeignKey(User, on_delete=CASCADE)
    is_active = BooleanField(default=True)

    def __str__(self):
        return self.nazev

    def je_aktivni(self):
        now = timezone.now()
        return self.datum_zacatku <= now <= self.datum_ukonceni

class Bid(Model):
    aukce = ForeignKey(Aukce, on_delete=CASCADE, related_name='bids')
    uzivatel = ForeignKey(User, on_delete=CASCADE)
    castka = DecimalField(max_digits=10, decimal_places=2, default=0.0)
    datum_prihozu = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uzivatel.username} - {self.castka} Kč"
