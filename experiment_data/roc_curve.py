import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'ccsimUI.settings'; import django
from experiment_data import models as data_models
from experiment import models as exp_models
import numpy as np
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt

return_dict = dict()
snp_config = '3_0'
mouse_per = '10'

params = exp_models.Parameters.objects.filter(snp_config=snp_config, mouse_per_strain=mouse_per)

var_qtls = params.values_list('var_qtl', flat=True).distinct()

for var_qtl in var_qtls:

    param = params.filter(var_qtl=var_qtl)

    return_dict[var_qtl] = dict()

    for software in exp_models.Software.objects.all():


        software_line = []

        new_plots = []

        software_line.append([0, 0])
        for i in range(1, 21):

            pvalue = i * .05

            tp = data_models.AdditiveModel.objects.filter(
                software=software, parameter=param, adj_locus_pvalue__lte=pvalue,
                locus_span=50000000).count()
            fp = data_models.AdditiveModel.objects.filter(
                software=software, parameter=param, adj_non_locus_pvalue__lte=pvalue,
                locus_span=50000000).count()

            #tpr = tp/float(tp+fn)

            software_line.append([fp, tp])


        locus_pvalues = data_models.AdditiveModel.objects.filter(
            software=software, parameter=param, locus_span=50000000).values_list('adj_locus_pvalue', flat=True).order_by('run_number')
        non_locus_pvalues = data_models.AdditiveModel.objects.filter(
            software=software, parameter=param, locus_span=50000000).values_list('adj_non_locus_pvalue', flat=True).order_by('run_number')

        count_locus = data_models.AdditiveModel.objects.filter(
            software=software, parameter=param, locus_span=50000000,
            adj_locus_pvalue__lte=.05, adj_non_locus_pvalue__gt=.05).count()

        count_non_locus = data_models.AdditiveModel.objects.filter(
            software=software, parameter=param, locus_span=50000000,

            adj_locus_pvalue__gt=.05, adj_non_locus_pvalue__lte=.05).count()

        count_locus_non_locus = data_models.AdditiveModel.objects.filter(
            software=software, parameter=param, locus_span=50000000,

            adj_locus_pvalue__lt=.05, adj_non_locus_pvalue__lt=.05).count()

        count_nothing = data_models.AdditiveModel.objects.filter(
            software=software, parameter=param, locus_span=50000000,

            adj_locus_pvalue__gt=.05, adj_non_locus_pvalue__gt=.05).count()

        return_dict[var_qtl][software.name] = software_line

        return_dict[var_qtl][software.name] = dict()

        return_dict[var_qtl][software.name]['roc'] = software_line

        return_dict[var_qtl][software.name]['plot2'] = (
            non_locus_pvalues, locus_pvalues, count_locus,
            count_non_locus, count_locus_non_locus, count_nothing)
        return_dict[var_qtl][software.name]['table_data'] = (
            var_qtl, count_locus, count_non_locus, count_locus_non_locus, count_nothing)

locus_lines = dict()
non_locus_lines = dict()
cell_text = []
rows = []
columns = ['software', 'varQtl', 'locus only', 'non-locus only', 'Both', 'No Hits']

for var_qtl in return_dict:

    qtl = return_dict[var_qtl]

    # subplot = 1

    for software in qtl:

        # if software not in locus_lines:
        #     locus_lines[software] = []
        #     non_locus_lines[software] = []

        # plt.subplot(2, 2, subplot)
        # points = qtl[software]['plot2']
        # plt.plot(-np.log(np.array(points[0])), -np.log(np.array(points[1])), '.', label=var_qtl)

        # locus_lines[software].append(points[2])
        # non_locus_lines[software].append(points[3])
        cell_text.append(return_dict[var_qtl][software]['table_data'])
        rows.append(software)
        # subplot += 1
        # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)
        # for pvalue in [.05]:
        #
        #     plt.axhline(y=-np.log(pvalue), ls='--', color='k', linewidth=2)
        #     plt.axvline(x=-np.log(pvalue), ls='--', color='k', linewidth=2)
        #
        # plt.title(software)



fp = open('/home/dtgillis/ccsim_workspace/data_pic/' + "%s-%s.csv" % (snp_config, mouse_per), 'w')

for column in columns:
    fp.write(str(column) + ',')
fp.write(os.linesep)

for i in range(len(rows)):

    fp.write(str(rows[i]) + ',')

    for data in cell_text[i]:
        fp.write(str(data) + ',')

    fp.write(os.linesep)


# #plt.tight_layout(pad=.04, w_pad=.1, h_pad=.4)
# plt.suptitle("SNP Config: %s , Mouse Per Strain: %s" % (snp_config, mouse_per), fontsize=14, fontweight='bold')
# plt.savefig('/home/dtgillis/ccsim_workspace/data_pic/' + "%s-%s-%s-%s.pdf" % (snp_config, mouse_per, snp, multiplier))
#
# table_fig = plt.figure()
# #plt.subplot(3, 1, 3)
#
# ax = plt.gca()
#
# ax.axis('off')
#
# the_table = ax.table(
#     cellText=cell_text, rowLabels=rows, colLabels=columns, loc='center')
#
#
#
#
# #plt.tight_layout()
#
# plt.suptitle("SNP Config: %s , Mouse Per Strain: %s" % (snp_config, mouse_per), fontsize=14, fontweight='bold')
# plt.savefig('/home/dtgillis/ccsim_workspace/data_pic/' + "%s-%s-%s-%s.table.pdf" % (snp_config, mouse_per, snp, multiplier))
# plt.show()











