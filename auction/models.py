from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models import EmailField, SET_NULL
from django.template.defaultfilters import default
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model, TextField, ForeignKey, CASCADE, DateTimeField, DecimalField, IntegerField, \
    BooleanField, CharField, ImageField, ManyToManyField, OneToOneField

from django.contrib.auth import get_user_model
User = get_user_model()

class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    vyhrane_aukce = ManyToManyField('Aukce', related_name='vyhrane_aukce', blank=True)
    city = CharField(max_length=100)
    address = CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}"


class Kategorie(Model):
    nazev = CharField(max_length=100)
    logo = ImageField(upload_to='kategorie_loga/', blank=True, null=True)

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
    sledujici = ManyToManyField(User, related_name='sledovane_aukce', blank=True)
    image = ImageField(upload_to='auction_images/', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])


    def __str__(self):
        return self.nazev


    def ukoncit_aukci(self):
        if timezone.now() > self.datum_ukonceni:
            self.is_active = False
            self.status = 'ENDED'

            nejvyssi_prihoz = self.bids.order_by('-castka').first()
            if nejvyssi_prihoz:
                self.vitez = nejvyssi_prihoz.uzivatel
                self.save()

                profile = nejvyssi_prihoz.uzivatel.profile
                profile.vyhrane_aukce.add(self)
                profile.save()


    def save(self, *args, **kwargs):
        if self.status == 'ACTIVE':
            self.ukoncit_aukci()

        super().save(*args, **kwargs)


    def kup_hned(self, user):
        self.vitez = user
        self.status = 'BOUGHT'
        self.is_active = False
        self.datum_ukonceni = timezone.now()
        self.save()

    def clean(self):
        super().clean()
        if self.datum_ukonceni < self.datum_zacatku:
            raise ValidationError("Datum ukončení nemůže být dříve než datum začátku aukce.")



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

class Hodnoceni(Model):
    aukce = ForeignKey(Aukce, on_delete=CASCADE, related_name='hodnoceni')
    uzivatel = ForeignKey(User, on_delete=CASCADE)

    rating_aukce = IntegerField(choices=[(i, i) for i in range(1, 6)])
    rating_prodejce = IntegerField(choices=[(i, i) for i in range(1, 6)])
    komentar_prodejce = TextField(blank=True, null=True)
    rating_kupujiciho = IntegerField(choices=[(i, i) for i in range(1, 6)])
    komentar_kupujiciho = TextField(blank=True, null=True)

    def __str__(self):
        return f"Hodnocení pro aukci: {self.aukce.nazev} od uživatel {self.uzivatel.username}"