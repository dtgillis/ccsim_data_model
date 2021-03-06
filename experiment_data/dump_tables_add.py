import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ccsimUI.settings'
import experiment.models as exp
import experiment_data.models as exp_data
import numpy as np
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt


for snp_config in exp.AdditiveParameter.objects.values_list('snp_config', flat=True).distinct():
    for mouse_per in exp.AdditiveParameter.objects.values_list('mouse_per_strain', flat=True).distinct():
        return_dict = dict()
        params = exp.AdditiveParameter.objects.filter(snp_config=snp_config, mouse_per_strain=mouse_per)
        var_qtls = params.values_list('var_qtl', flat=True).distinct()
        for var_qtl in var_qtls:
            param = params.filter(var_qtl=var_qtl)
            return_dict[var_qtl] = dict()
            for software in exp.Software.objects.all():
                # software_line = []
                # new_plots = []
                # software_line.append([0, 0])
                # for i in range(1, 21):
                #     pvalue = i * .05
                #
                #     tp = exp_data.AdditiveModel.objects.filter(
                #         software=software, parameter=param, adj_locus_pvalue__lte=pvalue,
                #         locus_span=50000000).count()
                #     fp = exp_data.AdditiveModel.objects.filter(
                #         software=software, parameter=param, adj_non_locus_pvalue__lte=pvalue,
                #         locus_span=50000000).count()
                #
                #     #tpr = tp/float(tp+fn)
                #
                #     software_line.append([fp, tp])


                locus_pvalues = exp_data.AdditiveModel.objects.filter(
                    software=software, parameter=param, locus_span=50000000).values_list('adj_locus_pvalue', flat=True).order_by('run_number')
                non_locus_pvalues = exp_data.AdditiveModel.objects.filter(
                    software=software, parameter=param, locus_span=50000000).values_list('adj_non_locus_pvalue', flat=True).order_by('run_number')

                count_locus = exp_data.AdditiveModel.objects.filter(
                    software=software, parameter=param, locus_span=50000000,
                    adj_locus_pvalue__lte=.05, adj_non_locus_pvalue__gt=.05).count()

                count_non_locus = exp_data.AdditiveModel.objects.filter(
                    software=software, parameter=param, locus_span=50000000,

                    adj_locus_pvalue__gt=.05, adj_non_locus_pvalue__lte=.05).count()

                count_locus_non_locus = exp_data.AdditiveModel.objects.filter(
                    software=software, parameter=param, locus_span=50000000,

                    adj_locus_pvalue__lt=.05, adj_non_locus_pvalue__lt=.05).count()

                count_nothing = exp_data.AdditiveModel.objects.filter(
                    software=software, parameter=param, locus_span=50000000,

                    adj_locus_pvalue__gt=.05, adj_non_locus_pvalue__gt=.05).count()
                return_dict[var_qtl][software.name] = dict()
                return_dict[var_qtl][software.name]['table_data'] = (
                    var_qtl, count_locus, count_non_locus, count_locus_non_locus, count_nothing)

        cell_text = []
        rows = []
        columns = ['software', 'varQtl', 'locus only', 'non-locus only', 'Both', 'No Hits']

        for var_qtl in return_dict:
            qtl = return_dict[var_qtl]
            for software in qtl:
                cell_text.append(return_dict[var_qtl][software]['table_data'])
                rows.append(software)

        fp = open('/home/dtgillis/ccsim_workspace/data_pic/' + "%s-%s.csv" % (snp_config, mouse_per), 'w')

        for column in columns:
            fp.write(str(column) + ',')
        fp.write(os.linesep)

        for i in range(len(rows)):

            fp.write(str(rows[i]) + ',')

            for data in cell_text[i]:
                fp.write(str(data) + ',')

            fp.write(os.linesep)