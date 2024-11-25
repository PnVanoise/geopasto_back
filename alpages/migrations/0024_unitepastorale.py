# Generated by Django 5.0.6 on 2024-09-12 12:46

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0023_alter_equipementalpage_geom'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitePastorale',
            fields=[
                ('id_unite_pastorale', models.BigIntegerField(primary_key=True, serialize=False)),
                ('code_up', models.CharField(max_length=50)),
                ('nom_up', models.CharField(max_length=50)),
                ('annee_version', models.BigIntegerField()),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=2154)),
                ('version_active', models.BooleanField()),
            ],
        ),
    ]
