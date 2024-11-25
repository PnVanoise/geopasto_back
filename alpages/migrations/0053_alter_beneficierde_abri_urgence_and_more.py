# Generated by Django 5.0.6 on 2024-11-06 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0052_situationdexploitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficierde',
            name='abri_urgence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='beneficiaires', to='alpages.abridurgence'),
        ),
        migrations.AlterField(
            model_name='beneficierde',
            name='exploitant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='beneficiaires', to='alpages.exploitant'),
        ),
        migrations.AlterField(
            model_name='etrecompose',
            name='eleveur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='alpages.eleveur'),
        ),
        migrations.AlterField(
            model_name='etrecompose',
            name='exploitant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='alpages.exploitant'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='mesure_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evenements', to='alpages.mesuredeplan'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='type_evenement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evenements', to='alpages.typeevenement'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='unite_pastorale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evenements', to='alpages.unitepastorale'),
        ),
    ]
