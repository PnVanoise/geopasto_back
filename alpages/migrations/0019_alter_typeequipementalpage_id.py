# Generated by Django 5.0.6 on 2024-07-28 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0018_quartieralpage_alter_logement_propriete_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeequipementalpage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
