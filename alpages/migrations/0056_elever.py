# Generated by Django 5.0.6 on 2024-11-06 14:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0055_gardesituation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elever',
            fields=[
                ('id_elever', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre_animaux', models.IntegerField()),
                ('date_debut', models.DateField(blank=True, null=True)),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('eleveur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eleveurs', to='alpages.eleveur')),
                ('situation_exploitation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eleveurs', to='alpages.situationdexploitation')),
                ('type_cheptel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eleveurs', to='alpages.typecheptel')),
            ],
        ),
    ]
