# Generated by Django 5.0.6 on 2024-10-28 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0046_alter_beneficierde_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beneficierde',
            name='id',
        ),
        migrations.AddField(
            model_name='beneficierde',
            name='id_beneficier_de',
            field=models.BigIntegerField(primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
