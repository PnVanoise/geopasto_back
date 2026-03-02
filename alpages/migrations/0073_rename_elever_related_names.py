from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alpages', '0072_unitepastorale_secteur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elever',
            name='eleveur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='elevers', to='alpages.eleveur'),
        ),
        migrations.AlterField(
            model_name='elever',
            name='situation_exploitation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='elevers', to='alpages.situationdexploitation'),
        ),
        migrations.AlterField(
            model_name='elever',
            name='type_cheptel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='elevers', to='alpages.typecheptel'),
        ),
    ]
