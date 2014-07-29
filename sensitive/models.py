from django.db import models

# Create your models here.


class ParametersManager(models.Manager):
    """
    custom manager to make parameter objects
    """
    def create_param(self, snp_config, var_qtl, var_env, var_gen, strains, mouse_per_strain):
        
        param = self.create(
            snp_config=snp_config, varQtl=var_qtl, varEnv=var_env,
            varGen=var_gen, strains=strains, mousePerStrain=mouse_per_strain)
        
        return param
    
        
class Parameters(models.Model):
    
    snp_config = models.CharField(max_length=3)
    varQtl = models.FloatField()
    varEnv = models.FloatField()
    varGen = models.FloatField()
    strains = models.PositiveIntegerField()
    mousePerStrain = models.CharField(max_length=3)
    objects = ParametersManager()
    
    class Meta:
        unique_together = ('snp_config', 'varQtl', 'varEnv', 'varGen', 'strains', 'mousePerStrain')
    
    def __unicode__(self):
        if self.mousePerStrain != 'inf':

            name = 'CC_' + self.snp_config + \
                   '_' + str(int(self.varQtl * 100)) + \
                   '_' + str(self.strains) + '.' + self.mousePerStrain

            return name

        else:
            name = 'CC_' + self.snp_config + \
                   '_' + str(int(self.varQtl*100)) +\
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
            software=software, mousePerStrain=mouse_per_strain,
            location=location, scale=scale, shape=shape)
        
        return gev_model

        
class GevModelParams(models.Model):
    
    software = models.ForeignKey(Software)
    mousePerStrain = models.CharField(max_length=3)
    location = models.FloatField()
    scale = models.FloatField()
    shape = models.FloatField()
    objects = GevModelParamsManager()
    
    class Meta:
        unique_together = ('mousePerStrain', 'software')
        
    def __unicode__(self):
        return 'gev model ' + self.software.name + ' mice per ' + str(self.mousePerStrain)


class ExtremeManager(models.Manager):
    """
    custom manager to make extreme value objects
    """
    
    def create_extreme_value(self, mouse_per_strain, software, alpha, threshold):
        
        extreme_v = self.create(mousePerStrain=mouse_per_strain, software=software, alpha=alpha, threshold=threshold)
        
        return extreme_v
        

class ExtremeValues(models.Model):
    
    mousePerStrain = models.CharField(max_length=3)
    software = models.ForeignKey(Software)
    alpha = models.FloatField()
    threshold = models.FloatField()
    objects = ExtremeManager()
    
    
    class Meta:
        unique_together = ('mousePerStrain', 'software', 'alpha', 'threshold')
    
    def __unicode__(self):
        return self.mousePerStrain + ' ' + self.software.name
    
    def get_extreme_value(self, mouse_per, software, alpha=.05):
        """
         mouse_per : mouse per Strain,
         software : String of the software
         alpha : alpha level defaults to .05
        """
        
        tmp_software = software.objects.all().filter(name=software)
        
        self.objects.filter(mousePerStrain=mouse_per,
                            software=tmp_software, alpha=alpha)
        
        return self.threshold


class SensitivityManager(models.Manager):    
    """
    custom manager to make sensitivity objects
    """
    
    def create_sensitivity(self, parameter, software, run_number, pvalue, adj_pvalue):
        
        sensitivity = self.create(
            parameter=parameter, software=software, runNumber=run_number, pValue=pvalue, adjPvalue=adj_pvalue)
        
        return sensitivity


class Sensitivity(models.Model):
    
    parameter = models.ForeignKey(Parameters)
    software = models.ForeignKey(Software)
    runNumber = models.IntegerField()
    pValue = models.FloatField()
    adjPvalue = models.FloatField()
    objects = SensitivityManager()

    class Meta:
        unique_together = ('parameter', 'software', 'runNumber')
    
    def __unicode__(self):
        return self.software.name + ' ' + str(self.runNumber)
