"""
Created on May 30, 2014

@author: Daniel Gillis

"""
from django.db import models

#Experiment Models


class ParametersManager(models.Manager):
    """
    custom manager to make parameter objects
    """
    def create_param(self, snp_config, var_qtl, var_env, var_gen, strains, mouse_per_strain):

        param = self.create(
            snp_config=snp_config, var_qtl=var_qtl, var_env=var_env,
            var_gen=var_gen, strains=strains, mouse_per_strain=mouse_per_strain)

        return param


class Parameters(models.Model):

    snp_config = models.CharField(max_length=3)
    var_qtl = models.FloatField()
    var_env = models.FloatField()
    var_gen = models.FloatField()
    strains = models.PositiveIntegerField()
    mouse_per_strain = models.CharField(max_length=3)
    objects = ParametersManager()

    class Meta:
        unique_together = ('snp_config', 'var_qtl', 'var_env', 'var_gen', 'strains', 'mouse_per_strain')

    def __unicode__(self):
        if self.mouse_per_strain != 'inf':

            name = 'CC_' + self.snp_config + \
                   '_' + str(int(self.var_qtl * 100)) + \
                   '_' + str(self.strains) + '.' + self.mouse_per_strain

            return name

        else:
            name = 'CC_' + self.snp_config + \
                   '_' + str(int(self.var_qtl*100)) +\
                   '_' + str(self.strains)

            return name


class SoftwareManager(models.Manager):
    """
    custom manager to make software objects
    """

    def create_software(self, name):

        software = self.create(name=name)

        return software


class Software(models.Model):

    name = models.CharField(max_length=10)
    objects = SoftwareManager()

    def __unicode__(self):
        return self.name


class GevModelParamsManager(models.Manager):
    """
    custom manager to make gevmodelparams
    """

    def create_gev_model(self, software, mouse_per_strain, location, scale, shape):

        gev_model = self.create(
            software=software, mouse_per_strain=mouse_per_strain,
            location=location, scale=scale, shape=shape)

        return gev_model


class GevModelParams(models.Model):

    software = models.ForeignKey(Software)
    mouse_per_strain = models.CharField(max_length=3)
    location = models.FloatField()
    scale = models.FloatField()
    shape = models.FloatField()
    objects = GevModelParamsManager()

    class Meta:
        unique_together = ('mouse_per_strain', 'software')

    def __unicode__(self):
        return 'gev model ' + self.software.name + ' mice per ' + str(self.mouse_per_strain)

