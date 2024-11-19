# Generated by Django 5.0.6 on 2024-10-15 09:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0035_etrecompose'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubventionPNV',
            fields=[
                ('id_subvention', models.BigIntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=15)),
                ('engage', models.BooleanField(default=False)),
                ('paye', models.BooleanField(default=False)),
                ('exploitant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subventions', to='alpages.exploitant')),
            ],
        ),
    ]