# Generated by Django 5.0.6 on 2024-10-29 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0048_logementtest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logementtest',
            old_name='geom',
            new_name='geometry',
        ),
    ]