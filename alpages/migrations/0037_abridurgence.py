# Generated by Django 5.0.6 on 2024-10-15 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0036_subventionpnv'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbriDUrgence',
            fields=[
                ('id_abri_urgence', models.BigIntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
                ('etat', models.CharField(max_length=50)),
            ],
        ),
    ]
