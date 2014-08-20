import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ccsimUI.settings'
import experiment.models as exp
import experiment_data.models as exp_data
import matplotlib
matplotlib.use('PDF')


for snp_config in exp.AdditiveEnvironmentSweepParameter.objects.values_list('snp_config', flat=True).distinct():
    for var_env in exp.AdditiveEnvironmentSweepParameter.objects.values_list('var_env', flat=True).distinct():
        return_dict = dict()
        params = exp.AdditiveEnvironmentSweepParameter.objects.filter(snp_config=snp_config, var_env=var_env)
        var_qtls = params.values_list('var_qtl', flat=True).distinct()
        for var_qtl in var_qtls:
            for mouse_per in params.values_list('mouse_per_strain',flat=True).distinct():
                param = params.filter(var_qtl=var_qtl, mouse_per_strain=mouse_per)
                if var_qtl not in return_dict:
                    return_dict[var_qtl] = dict()
                for software in exp.Software.objects.filter(name='emmax'):
                    locus_pvalues = exp_data.AdditiveEnvironmentalSweepModel.objects.filter(
                        software=software, parameter=param, locus_span=50000000).values_list('adj_locus_pvalue', flat=True).order_by('run_number')
                    non_locus_pvalues = exp_data.AdditiveEnvironmentalSweepModel.objects.filter(
                        software=software, parameter=param, locus_span=50000000).values_list('adj_non_locus_pvalue', flat=True).order_by('run_number')

                    count_locus = exp_data.AdditiveEnvironmentalSweepModel.objects.filter(
                        software=software, parameter=param, locus_span=50000000,
                        adj_locus_pvalue__lte=.05, adj_non_locus_pvalue__gt=.05).count()

                    count_non_locus = exp_data.AdditiveEnvironmentalSweepModel.objects.filter(
                        software=software, parameter=param, locus_span=50000000,

                        adj_locus_pvalue__gt=.05, adj_non_locus_pvalue__lte=.05).count()

                    count_locus_non_locus = exp_data.AdditiveEnvironmentalSweepModel.objects.filter(
                        software=software, parameter=param, locus_span=50000000,

                        adj_locus_pvalue__lt=.05, adj_non_locus_pvalue__lt=.05).count()

                    count_nothing = exp_data.AdditiveEnvironmentalSweepModel.objects.filter(
                        software=software, parameter=param, locus_span=50000000,

                        adj_locus_pvalue__gt=.05, adj_non_locus_pvalue__gt=.05).count()
                    if 'table_data' not in return_dict[var_qtl]:
                        return_dict[var_qtl]['table_data'] = []
                    return_dict[var_qtl]['table_data'].append([var_qtl, var_env, mouse_per,
                                                               count_locus, count_non_locus,
                                                               count_locus_non_locus, count_nothing])

        cell_text = []
        rows = []
        columns = ['software', 'varQtl', 'var_env', 'mouse_per', 'locus only', 'non-locus only', 'Both', 'No Hits']

        for var_qtl in return_dict:
            qtl = return_dict[var_qtl]
            for row in qtl['table_data']:
                cell_text.append(row)
                rows.append('emmax')

        fp = open('/home/dtgillis/ccsim_workspace/data_pic/' + "env_sweep.%s-%s.csv" % (snp_config, str(var_env)), 'w')

        for column in columns:
            fp.write(str(column) + ',')
        fp.write(os.linesep)

        for i in range(len(rows)):

            fp.write(str(rows[i]) + ',')

            for data in cell_text[i]:
                fp.write(str(data) + ',')

            fp.write(os.linesep)