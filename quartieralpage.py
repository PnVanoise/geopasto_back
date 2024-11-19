# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class AlpagesQuartieralpage(models.Model):
    id = models.BigIntegerField(primary_key=True)
    geom = models.MultiPolygonField(srid=2154, blank=True, null=True)
    quartier_code_court = models.CharField(max_length=10, blank=True, null=True)
    date_presence_troupeau = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alpages_quartieralpage'
