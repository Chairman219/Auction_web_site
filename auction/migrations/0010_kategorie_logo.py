# Generated by Django 4.1 on 2024-10-07 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0009_profile_vyhrane_aukce'),
    ]

    operations = [
        migrations.AddField(
            model_name='kategorie',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='kategorie_loga/'),
        ),
    ]
