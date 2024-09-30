from django.core.exceptions import ValidationError
from django.db.models import EmailField, SET_NULL
from django.template.defaultfilters import default
from django.utils import timezone

from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models import Model, TextField, ForeignKey, CASCADE, DateTimeField, DecimalField, IntegerField, \
    BooleanField, CharField, ImageField, ManyToManyField, OneToOneField



class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    city = CharField(max_length=100)
    adress = CharField(max_length=100)

    def __str__(self):
        return self.user


class Kategorie(Model):
    nazev = CharField(max_length=100)

    class Meta:
        permissions = [
            ("muze_vytvorit_kategorii", "Může vytvářet kategorie")
        ]

    def __str__(self):
        return self.nazev

class Aukce(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Aktivní'),
        ('ENDED', 'Ukončená'),
        ('BOUGHT', 'Zakoupená'),
    ]

    nazev = CharField(max_length=100, default="")
    popis = TextField(default="")
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
    vitez = ForeignKey(User, null=True, blank=True, on_delete=SET_NULL, related_name='vyhrane_aukce')
    status = CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')


    def __str__(self):
        return self.nazev



    def ukoncit_aukci(self):

        if timezone.now() > self.datum_ukonceni:
            self.is_active = False

    def save(self, *args, **kwargs):

        original_is_active = self.is_active
        self.ukoncit_aukci()


        if original_is_active != self.is_active:
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def kup_hned(self, user):
        self.vitez = user
        self.status = 'BOUGHT'
        self.save()



class Bid(Model):
    aukce = ForeignKey(Aukce, on_delete=CASCADE, related_name='bids')
    uzivatel = ForeignKey(User, on_delete=CASCADE)
    castka = DecimalField(max_digits=10, decimal_places=2, default=0.0)
    datum_prihozu = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uzivatel.username} - {self.castka} Kč"

    def clean(self):
        if self.castka <= 0:
            raise ValidationError('Příhoz musí být kladné číslo.')
