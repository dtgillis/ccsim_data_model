"""
Created on May 30, 2014

@author: dtgillis
"""
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ccsimUI.settings'
from experiment_data.data import ExperimentDataImporter
import experiment.models as exp


def parse_additive_data():

    for software in exp.Software.objects.all():
        params = exp.AdditiveParameter.objects.all()
        for param in params:
            if software.name in ['htree', 'bagpipe'] \
                    and (param.mouse_per_strain == '5' or param.mouse_per_strain == '10'):
                continue
            elif param.var_qtl in [.20, .15] and param.mouse_per_strain != 'inf':
                continue
            else:
                exp_data = ExperimentDataImporter(
                    params=param, software=software,
                    base_dir='/home/dtgillis/ccsim_workspace/data_django', sweep_size=50000000)

                exp_data.parse_additive_data()

if __name__ == '__main__':
    parse_additive_data()
    #parse_data(additive=False)
    #parse_epis_data()