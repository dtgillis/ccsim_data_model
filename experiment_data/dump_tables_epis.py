import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ccsimUI.settings'
import experiment.models as exp
import experiment_data.models as exp_data
for multiplier in [.5, 2.0]:
    for snp_config in exp.EpistaticParameter.objects.values_list('snp_config', flat=True).distinct():
    #for multiplier in [.5, 2.0]:
        for mouse_per in exp.EpistaticParameter.objects.values_list('mouse_per_strain', flat=True).distinct():
            return_dict = dict()
            params = exp.EpistaticParameter.objects.filter(snp_config=snp_config, mouse_per_strain=mouse_per)
            var_qtls = params.values_list('var_qtl', flat=True).distinct()
            for var_qtl in var_qtls:
                for snp in ['fa0', 'fa1']:
                    #for multiplier in [.5, 2.0]:
                    param = params.filter(var_qtl=var_qtl, multiplier=multiplier)
                    if var_qtl not in return_dict:
                        return_dict[var_qtl] = dict()
                    for software in exp.Software.objects.all():
                        locus_pvalues = exp_data.EpistaticModel.objects.filter(
                            software=software, parameter=param, locus_span=50000000, snp_id=snp).values_list(
                            'adj_locus_pvalue', flat=True).order_by('run_number')
                        non_locus_pvalues = exp_data.EpistaticModel.objects.filter(
                            software=software, parameter=param, locus_span=50000000, snp_id=snp).values_list(
                            'adj_non_locus_pvalue', flat=True).order_by('run_number')

                        count_locus = exp_data.EpistaticModel.objects.filter(
                            software=software, parameter=param, locus_span=50000000,
                            adj_locus_pvalue__lte=.05, adj_non_locus_pvalue__gt=.05, snp_id=snp).count()

                        count_non_locus = exp_data.EpistaticModel.objects.filter(
                            software=software, parameter=param, locus_span=50000000,
                            adj_locus_pvalue__gt=.05, adj_non_locus_pvalue__lte=.05, snp_id=snp).count()

                        count_locus_non_locus = exp_data.EpistaticModel.objects.filter(
                            software=software, parameter=param, locus_span=50000000,
                            adj_locus_pvalue__lt=.05, adj_non_locus_pvalue__lt=.05, snp_id=snp).count()

                        count_nothing = exp_data.EpistaticModel.objects.filter(
                            software=software, parameter=param, locus_span=50000000,
                            adj_locus_pvalue__gt=.05, adj_non_locus_pvalue__gt=.05, snp_id=snp).count()
                        if software.name not in return_dict[var_qtl]:
                            return_dict[var_qtl][software.name] = dict()

                        if 'table_data' not in return_dict[var_qtl][software.name]:
                            return_dict[var_qtl][software.name]['table_data'] = []
                            return_dict[var_qtl][software.name]['table_data'].append(
                                [var_qtl, multiplier, snp, count_locus,
                                count_non_locus, count_locus_non_locus, count_nothing])
                        else:
                            return_dict[var_qtl][software.name]['table_data'].append(
                                [var_qtl, multiplier, snp, count_locus,
                                count_non_locus, count_locus_non_locus, count_nothing])

            cell_text = []
            rows = []
            columns = ['software', 'varQtl', 'multiplier', 'snp', 'locus only', 'non-locus only', 'Both', 'No Hits']

            for var_qtl in return_dict:
                qtl = return_dict[var_qtl]
                for software in qtl:
                    for row in return_dict[var_qtl][software]['table_data']:
                        cell_text.append(row)
                        rows.append(software)

            fp = open('/home/dtgillis/ccsim_workspace/data_pic/' + "%s-%s-%s.epis.csv" % (snp_config, mouse_per,str(multiplier)), 'w')

            for column in columns:
                fp.write(str(column) + ',')
            fp.write(os.linesep)

            for i in range(len(rows)):

                fp.write(str(rows[i]) + ',')

                for data in cell_text[i]:
                    fp.write(str(data) + ',')

                fp.write(os.linesep)