# Generated by Django 5.0.6 on 2024-08-07 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0021_alter_equipementalpage_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeequipementalpage',
            name='typegeom',
            field=models.CharField(blank=True, choices=[('Point', 'Point'), ('Polygon', 'Polygon'), ('LineString', 'LineString'), ('Pas de géométrie', 'Pas de géométrie')], default='Pas de géométrie', max_length=20, null=True),
        ),
    ]