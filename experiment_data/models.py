from django.db import models

# Create your models here.
import experiment.models as exp


class AdditiveModelManager(models.Manager):

    def create_additive_model(self, parameter, software, run_number,
                              locus_span, locus_pvalue, adj_locus_pvalue,
                              non_locus_pvalue, adj_non_locus_pvalue,
                              non_chrm_pvalue, adj_non_chrm_pvalue):

        additive_model = self.create(parameter=parameter, software=software, run_number=run_number,
                                     locus_span=locus_span, locus_pvalue=locus_pvalue,
                                     adj_locus_pvalue=adj_locus_pvalue, non_locus_pvalue=non_locus_pvalue,
                                     adj_non_locus_pvalue=adj_non_locus_pvalue, non_chrm_pvalue=non_chrm_pvalue,
                                     adj_non_chrm_pvalue=adj_non_chrm_pvalue)

        return additive_model


class AdditiveModel(models.Model):

    parameter = models.ForeignKey(exp.AdditiveParameter)
    software = models.ForeignKey(exp.Software)
    run_number = models.IntegerField()
    locus_span = models.IntegerField()
    locus_pvalue = models.FloatField()
    adj_locus_pvalue = models.FloatField()
    non_locus_pvalue = models.FloatField()
    adj_non_locus_pvalue = models.FloatField()
    non_chrm_pvalue = models.FloatField()
    adj_non_chrm_pvalue = models.FloatField()
    objects = AdditiveModelManager()

    class Meta:
        unique_together = ('parameter', 'software', 'run_number', 'locus_span')


class EpistaticModelManager(models.Manager):

    def create_epistatic_model(self, parameter, software, run_number, snp_id,
                              locus_span, locus_pvalue, adj_locus_pvalue,
                              non_locus_pvalue, adj_non_locus_pvalue,
                              non_chrm_pvalue, adj_non_chrm_pvalue, multiplier):

        epistatic_model = self.create(
            parameter=parameter, software=software, run_number=run_number,
            snp_id=snp_id, locus_span=locus_span, locus_pvalue=locus_pvalue,
            adj_locus_pvalue=adj_locus_pvalue, non_locus_pvalue=non_locus_pvalue,
            adj_non_locus_pvalue=adj_non_locus_pvalue, non_chrm_pvalue=non_chrm_pvalue,
            adj_non_chrm_pvalue=adj_non_chrm_pvalue, multiplier=multiplier)

        return epistatic_model


class EpistaticModel(models.Model):

    parameter = models.ForeignKey(exp.EpistaticParameter)
    software = models.ForeignKey(exp.Software)
    run_number = models.IntegerField()
    locus_span = models.IntegerField()
    locus_pvalue = models.FloatField()
    adj_locus_pvalue = models.FloatField()
    non_locus_pvalue = models.FloatField()
    adj_non_locus_pvalue = models.FloatField()
    non_chrm_pvalue = models.FloatField()
    adj_non_chrm_pvalue = models.FloatField()
    snp_id = models.CharField(max_length=3)
    objects = EpistaticModelManager()

    class Meta:
        unique_together = ('parameter', 'software', 'run_number', 'locus_span', 'snp_id')


class AdditiveStrainSweepModel(models.Model):

    parameter = models.ForeignKey(exp.AdditiveStrainSweepParameter)
    software = models.ForeignKey(exp.Software)
    run_number = models.IntegerField()
    locus_span = models.IntegerField()
    locus_pvalue = models.FloatField()
    adj_locus_pvalue = models.FloatField()
    non_locus_pvalue = models.FloatField()
    adj_non_locus_pvalue = models.FloatField()
    non_chrm_pvalue = models.FloatField()
    adj_non_chrm_pvalue = models.FloatField()

    class Meta:
        unique_together = ('parameter', 'software', 'run_number', 'locus_span')


class AdditiveEnvironmentalSweepModel(models.Model):

    parameter = models.ForeignKey(exp.AdditiveEnvironmentSweepParameter)
    software = models.ForeignKey(exp.Software)
    run_number = models.IntegerField()
    locus_span = models.IntegerField()
    locus_pvalue = models.FloatField()
    adj_locus_pvalue = models.FloatField()
    non_locus_pvalue = models.FloatField()
    adj_non_locus_pvalue = models.FloatField()
    non_chrm_pvalue = models.FloatField()
    adj_non_chrm_pvalue = models.FloatField()

    class Meta:
        unique_together = ('parameter', 'software', 'run_number', 'locus_span')


class AdditiveModelAlleleFrequency(models.Model):

    parameter = models.ForeignKey(exp.AdditiveParameter)
    run_number = models.IntegerField()
    allele_frequency = models.FloatField()

    class Meta:
        unique_together = ('parameter', 'run_number')