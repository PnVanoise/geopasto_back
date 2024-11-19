# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class QuartiersAlpages(models.Model):
    fid = models.BigIntegerField(primary_key=True)
    geom = models.MultiPolygonField(srid=2154, blank=True, null=True)
    id = models.BigIntegerField(blank=True, null=True)
    code_quart = models.CharField(max_length=15, blank=True, null=True)
    surface = models.FloatField(blank=True, null=True)
    bd_quartiers_2015_field_1 = models.CharField(db_column='BD_quartiers_2015_field_1', blank=True, null=True)  # Field name made lowercase.
    bd_quartiers_2015_nom_up = models.CharField(db_column='BD_quartiers_2015_NOM_UP', blank=True, null=True)  # Field name made lowercase.
    bd_quartiers_2015_nom_2 = models.CharField(db_column='BD_quartiers_2015_NOM_2', blank=True, null=True)  # Field name made lowercase.
    bd_quartiers_2015_quartier = models.CharField(db_column='BD_quartiers_2015_Quartier', blank=True, null=True)  # Field name made lowercase.
    bd_quartiers_2015_nom_quart = models.CharField(db_column='BD_quartiers_2015_Nom_quart', blank=True, null=True)  # Field name made lowercase.
    bd_quartiers_2015_field_7 = models.CharField(db_column='BD_quartiers_2015_field_7', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Quartiers alpages'


class Secteurs(models.Model):
    fid = models.BigIntegerField(primary_key=True)
    geom = models.MultiPolygonField(srid=2154, blank=True, null=True)
    nom = models.CharField(max_length=45, blank=True, null=True)
    surface = models.BigIntegerField(blank=True, null=True)
    id_secteur = models.BigIntegerField(blank=True, null=True)
    sigle = models.CharField(max_length=10, blank=True, null=True)
    legende = models.CharField(max_length=100, blank=True, null=True)
    aoa_ha = models.FloatField(blank=True, null=True)
    aoa_pour = models.FloatField(blank=True, null=True)
    coeur = models.FloatField(blank=True, null=True)
    coeur_pour = models.FloatField(blank=True, null=True)
    aa_ha = models.FloatField(blank=True, null=True)
    aa_pourc = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Secteurs'


class AlpagesCategorie(models.Model):
    id = models.BigAutoField(primary_key=True)
    description_categorie = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'alpages_categorie'


class AlpagesQuartierup(models.Model):
    id = models.BigAutoField(primary_key=True)
    quartier_code = models.CharField(max_length=15, blank=True, null=True)
    surface = models.FloatField(blank=True, null=True)
    up_code = models.CharField(max_length=254, blank=True, null=True)
    up_nom_1 = models.CharField(max_length=254, blank=True, null=True)
    up_nom_2 = models.CharField(max_length=254, blank=True, null=True)
    quartier_code_court = models.CharField(max_length=254, blank=True, null=True)
    quartier_nom = models.CharField(max_length=254, blank=True, null=True)
    geom = models.MultiPolygonField(srid=2154)
    categorie = models.ForeignKey(AlpagesCategorie, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'alpages_quartierup'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
