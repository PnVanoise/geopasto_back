# Generated by Django 5.0.6 on 2024-06-14 07:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0002_categorie'),
    ]

    operations = [
        migrations.AddField(
            model_name='quartierup',
            name='categorie',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='alpages', to='alpages.categorie'),
            preserve_default=False,
        ),
    ]
