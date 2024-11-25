# Generated by Django 5.0.6 on 2024-10-03 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0024_unitepastorale'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProprietaireFoncier',
            fields=[
                ('id_proprietaire', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nom_propr', models.CharField(max_length=50)),
                ('prenom_propr', models.CharField(blank=True, max_length=50, null=True)),
                ('tel_propr', models.CharField(blank=True, max_length=30, null=True)),
                ('mail_propr', models.CharField(blank=True, max_length=50, null=True)),
                ('adresse_propr', models.CharField(blank=True, max_length=100, null=True)),
                ('commentaire', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
