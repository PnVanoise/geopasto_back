# Generated by Django 5.0.6 on 2024-06-17 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0003_quartierup_categorie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quartierup',
            name='categorie',
        ),
        migrations.DeleteModel(
            name='Categorie',
        ),
    ]