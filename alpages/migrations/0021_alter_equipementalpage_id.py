# Generated by Django 5.0.6 on 2024-08-06 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0020_alter_equipementalpage_geom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipementalpage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]