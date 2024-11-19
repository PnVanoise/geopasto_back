# Generated by Django 5.0.6 on 2024-10-16 10:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0040_typeevenement_evenement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evenement',
            name='mesure_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evenements', to='alpages.mesuredeplan'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='type_evenement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evenements', to='alpages.typeevenement'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='unite_pastorale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evenements', to='alpages.unitepastorale'),
        ),
    ]
