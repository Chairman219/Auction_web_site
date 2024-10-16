from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from auction.models import Profile
from django.test import TestCase
from auction.models import Aukce, Kategorie, Bid
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class SignUpViewTests(TestCase):

    def test_signup_with_premium_redirect(self):
        """Test, zda registrace s volbou Premium účtu přesměruje na premium_confirmation url."""
        response = self.client.post(reverse('sign_up'), {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'city': 'TestCity',
            'adress': 'TestAdress',
            'is_premium': 'True'
        })

        # Ověření, že byl uživatel přesměrován na premium_confirmation
        self.assertRedirects(response, reverse('premium_confirmation'))

        # Ověření, že byl vytvořen uživatelský profil
        user = User.objects.get(username='testuser')
        self.assertTrue(Profile.objects.filter(user=user).exists())

        # Ověření, že profil má čekání na potvrzení Premium účtu
        self.assertTrue(user.profile.waiting_for_premium_confirmation)

    def test_signup_with_normal_account(self):
        """Test, zda registrace s normálním účtem nepřesměruje na premium_confirmation url."""
        response = self.client.post(reverse('sign_up'), {
            'username': 'testuser2',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser2@example.com',
            'city': 'TestCity',
            'adress': 'TestAdress',
            'is_premium': 'False'
        })

        # Ověření, že uživatel není přesměrován na premium_confirmation
        self.assertRedirects(response, reverse('hlavni_stranka'))

        # Ověření, že profil nečeká na potvrzení Premium účtu
        user = User.objects.get(username='testuser2')
        self.assertFalse(user.profile.waiting_for_premium_confirmation)


class PremiumConfirmationViewTests(TestCase):
    def setUp(self):
        """Před každým testem vytvoříme uživatele s profilem čekajícím na potvrzení Premium účtu."""
        self.user = User.objects.create_user(username='premiumuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, city='TestCity', adress='TestAdress', waiting_for_premium_confirmation=True)

    def test_confirm_premium(self):
        """Test pro potvrzení Premium účtu."""
        self.client.login(username='premiumuser', password='testpassword')
        response = self.client.post(reverse('premium_confirmation'), {'confirm_premium': 'true'})

        # Ověření, že byl uživatel přesměrován na profil
        self.assertRedirects(response, reverse('muj_profil'))

        # Ověření, že je uživatel nyní Premium
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.is_premium)
        self.assertFalse(self.profile.waiting_for_premium_confirmation)

    def test_cancel_premium(self):
        """Test pro zrušení Premium účtu."""
        self.client.login(username='premiumuser', password='testpassword')
        response = self.client.post(reverse('premium_confirmation'), {'cancel_premium': 'true'})

        # Ověření, že byl uživatel přesměrován na profil
        self.assertRedirects(response, reverse('muj_profil'))

        # Ověření, že uživatel nemá Premium účet
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.is_premium)
        self.assertFalse(self.profile.waiting_for_premium_confirmation)

class AukceModelTests(TestCase):
    def setUp(self):
        """Před každým testem vytvoříme uživatele, kategorii a aukci."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.kategorie = Kategorie.objects.create(nazev="TestKategorie")
        self.aukce = Aukce.objects.create(
            nazev="Test Aukce",
            popis="Test popis",
            kategorie=self.kategorie,
            minimalni_prihoz=Decimal('100.00'),
            user=self.user,
            datum_zacatku=timezone.now(),
            datum_ukonceni=timezone.now() + timezone.timedelta(days=1)
        )

    def test_update_minimalni_prihoz(self):
        """Test pro aktualizaci minimálního příhozu."""
        new_bid = Decimal('150.00')
        self.aukce.update_minimalni_prihoz(new_bid, self.user)

        # Ověření, že minimální příhoz byl aktualizován
        self.aukce.refresh_from_db()
        self.assertEqual(self.aukce.minimalni_prihoz, new_bid)
        self.assertEqual(self.aukce.nejvyssi_prihoz_uzivatel, self.user)
