"""aukce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from auction.views import VytvorAukciView, hlavni_stranka, SeznamAukciView, aukcni_stranka, seznam_kategorii, \
    aukce_v_kategorii, SubmittableLoginView, SubmittablePasswordChangeView, SubmittablePasswordResetView, \
    SmazatAukciView, VytvoritKategoriiView, vyhledavani_aukci, muj_profil, SignUpView, ohodnotit_aukci, sleduj_aukci, \
    odhlasit_aukci, SmazatKategoriiView, UpravitKategoriiView, upgrade_to_premium

from auction.models import Aukce, Bid, Kategorie, Profile, Hodnoceni

admin.site.register(Aukce)
admin.site.register(Kategorie)
admin.site.register(Profile)
admin.site.register(Hodnoceni)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('password_change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', SubmittablePasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('muj_profil/', muj_profil, name='muj_profil'),
    path("", hlavni_stranka, name="hlavni_stranka"),
    path('aukce/', SeznamAukciView.as_view(), name='seznam_aukci'),
    path('aukce/<int:aukce_id>/', aukcni_stranka, name='aukcni_stranka'),
    path('aukce/vytvor/', VytvorAukciView.as_view(), name='vytvor_aukci'),
    path('aukce/<int:pk>/smazat/', SmazatAukciView.as_view(), name='smazat_aukci'),
    path('kategorie/', seznam_kategorii, name='seznam_kategorii'),
    path('kategorie/<int:kategorie_id>/', aukce_v_kategorii, name='aukce_v_kategorii'),
    path('kategorie/vytvorit/', VytvoritKategoriiView.as_view(), name='vytvorit_kategorii'),
    path('kategorie/smazat/<int:pk>', SmazatKategoriiView.as_view(), name='smazat_kategorii'),
    path('kategorie/upravit/<int:pk>', UpravitKategoriiView.as_view(), name='upravit_kategorii'),
    path('vyhledavani/', vyhledavani_aukci, name='vyhledavani_aukci'),
    path('aukce/<int:aukce_id>/hodnotit/', ohodnotit_aukci, name='hodnotit_aukci'),
    path('aukce/<int:aukce_id>/sleduj/', sleduj_aukci, name='sleduj_aukci'),
    path('aukce/<int:aukce_id>/odhlasit/', odhlasit_aukci, name='odhlasit_aukci'),
    path('muj_profil/upgrade/', upgrade_to_premium, name='upgrade_to_premium')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
