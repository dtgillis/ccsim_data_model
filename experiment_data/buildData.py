"""
Created on May 30, 2014

@author: dtgillis
"""
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ccsimUI.settings'
from experiment_data.data import ExperimentDataImporter
import experiment.models as exp
import experiment_data.models as exp_data


def parse_additive_data():

    for software in exp.Software.objects.all():
        params = exp.AdditiveParameter.objects.all()
        for param in params:
            # htree never done for 5 or 10 mouse model
            if software.name in ['htree'] \
                    and (param.mouse_per_strain == '5' or param.mouse_per_strain == '10'):
                continue
            # bagpipe,htree 1 mouse 15 and 20 not done yet
            # if software.name in ['bagpipe']:
            #     # if param.var_qtl in [.20, .15] and param.mouse_per_strain != 'inf':
            #     #     continue
            #     if param.snp_config in ['2_0'] and param.mouse_per_strain in ['5']:
            #         pass
            #     elif param.snp_config not in ['1_0'] and param.mouse_per_strain in ['5', '10']:
            #         continue

            # no software runs for .2 or .15 with 5 or 10 mice
            if param.var_qtl in [.20, .15] and param.mouse_per_strain not in ['inf', '1']:
                continue
            else:
                exp_data_in = ExperimentDataImporter(
                    params=param, software=software,
                    base_dir='/home/dtgillis/ccsim_workspace/data_django', sweep_size=50000000)

                exp_data_in.parse_additive_data()


def parse_epistatic_data():

    for software in exp.Software.objects.all():
        params = exp.EpistaticParameter.objects.all()
        for param in params:
            if software.name in ['htree'] \
                    and (param.mouse_per_strain == '5' or param.mouse_per_strain == '10'):
                continue
            elif param.var_qtl in [.20, .15] and param.mouse_per_strain not in ['inf', '1']:
                continue
            elif param.multiplier == .5 and param.mouse_per_strain not in ['inf', '1']:
                continue
            else:
                exp_data_in = ExperimentDataImporter(
                    params=param, software=software,
                    base_dir='/home/dtgillis/ccsim_workspace/data_django', sweep_size=50000000)

                exp_data_in.parse_epistatic_data()


def parse_additive_strain_sweep_data():

    for software in exp.Software.objects.filter(name='emmax'):
        params = exp.AdditiveStrainSweepParameter.objects.all()
        for param in params:
            exp_data_in = ExperimentDataImporter(
                params=param, software=software,
                base_dir='/home/dtgillis/ccsim_workspace/data_django', sweep_size=50000000)
            exp_data_in.parse_additive_strain_sweep()


def parse_additive_env_sweep_data():

    for software in exp.Software.objects.filter(name='emmax'):
        params = exp.AdditiveEnvironmentSweepParameter.objects.all()
        for param in params:
            exp_data_in = ExperimentDataImporter(
                params=param, software=software,
                base_dir='/home/dtgillis/ccsim_workspace/data_django', sweep_size=50000000)
            exp_data_in.parse_additive_env_sweep()


def parse_allele_frequency_data():
    base_dir = '/home/dtgillis/ccsim_workspace/data_django/minor_allele/'
    params = exp.AdditiveParameter.objects.filter(snp_config='1_0',
                                                  var_qtl__in=[.05, .10, .15, .20, .25],
                                                  mouse_per_strain='inf')
    allele_freq_list = []
    for param in params:
        for line in open(base_dir + param.__unicode__() + '.maf.dat', 'r'):
            fields = line.split()
            allele_freq_list.append(exp_data.AdditiveModelAlleleFrequency(parameter=param,
                                                                          run_number=int(fields[0]),
                                                                          allele_frequency=float(fields[1])))

    exp_data.AdditiveModelAlleleFrequency.objects.bulk_create(allele_freq_list)





if __name__ == '__main__':
    parse_additive_data()
    parse_epistatic_data()
    parse_additive_strain_sweep_data()
    parse_additive_env_sweep_data()
    parse_allele_frequency_data()