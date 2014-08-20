import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ccsimUI.settings'
import experiment.models as exp
import experiment_data.models as exp_data
import matplotlib.pyplot as plt
import numpy as np


return_dict = dict()
bins = 11
allele_range = []
for param_id in exp_data.AdditiveModelAlleleFrequency.objects.values_list('parameter', flat=True).distinct():
    param = exp.AdditiveParameter.objects.filter(pk=param_id).get()
    if param.var_qtl not in return_dict:
        return_dict[param.var_qtl] = dict()
    for software in exp.Software.objects.all():
        if software.name not in return_dict[param.var_qtl]:
            return_dict[param.var_qtl][software.name] = []
        lower_range = 0.0
        for upper_range in np.linspace(0, .5, num=bins):
            if upper_range == lower_range:
                continue
            run_numbers = exp_data.AdditiveModelAlleleFrequency.objects.filter(
                parameter=param, allele_frequency__gte=lower_range,
                allele_frequency__lt=upper_range).values_list('run_number', flat=True).order_by('run_number')

            locus_pvalues = np.array(exp_data.AdditiveModel.objects.filter(
                parameter=param, software=software, locus_span=50000000,
                run_number__in=run_numbers,
                ).values_list(
                'adj_locus_pvalue', flat=True).order_by('run_number'))

            count_sig = (locus_pvalues < .05).sum()
            if locus_pvalues.shape[0] != 0:
                return_dict[param.var_qtl][software.name].append(
                    [count_sig/float(locus_pvalues.shape[0]), locus_pvalues.shape[0]])
            else:
                return_dict[param.var_qtl][software.name].append(["NA", 0])


            lower_range = upper_range

lower_range = 0.0
columns = []
allele_freq_file = open('/home/dtgillis/ccsim_workspace/data_pic/allele_freq.csv', 'w')
for upper_range in np.linspace(0, .5, num=bins):
    if upper_range == lower_range:
        continue
    columns.append("{0:.1f}%-{1:.1f}%".format(lower_range*100, upper_range*100))
    lower_range = upper_range

allele_freq_file.write('software,var_qtl')
for element in columns:
    allele_freq_file.write(",{0:s}".format(element))

allele_freq_file.write(os.linesep)

for var_qtl in return_dict:
    for software in return_dict[var_qtl]:
        allele_freq_file.write(software + ',' + str(var_qtl))
        for datum in return_dict[var_qtl][software]:
            if datum[0] == "NA":
                allele_freq_file.write(',NA (0)')
            else:
                allele_freq_file.write(',{0:.2f} ({1:d})'.format(datum[0], datum[1]))
        allele_freq_file.write(os.linesep)



