# Generated by Django 5.0.6 on 2024-10-03 09:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0025_proprietairefoncier'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitepastorale',
            name='proprietaire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unites_pastorales', to='alpages.proprietairefoncier'),
        ),
    ]