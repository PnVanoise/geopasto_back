# Generated by Django 5.0.6 on 2024-07-04 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0012_logement_activite_laitiere_logement_etat_batiment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logement',
            name='acces_final',
            field=models.CharField(choices=[('carrossable', 'carrossable'), ('4_4', '4*4'), ('quad', 'quad'), ('pedestre', 'pédestre')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='logement',
            name='statut',
            field=models.CharField(choices=[('existant', 'existant'), ('besoin', 'besoin')], max_length=50, null=True),
        ),
    ]