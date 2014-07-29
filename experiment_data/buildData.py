"""
Created on May 30, 2014

@author: dtgillis
"""
import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'ccsimUI.settings'; import django
from experiment_data.data import ExperimentDataImporter
from experiment.models import Parameters
from experiment.models import Software
from django.db.models import Q


def parse_data(additive=True):

    for software in Software.objects.all():

        if additive is True:
            params = Parameters.objects.exclude(snp_config='1_1')
        else:
            params = Parameters.objects.filter(Q(mouse_per_strain='inf') | Q(mouse_per_strain='1'),
                                               snp_config='1_1')

        for param in params:

            if software.name == 'htree' and (param.mouse_per_strain == '5' or param.mouse_per_strain == '10'):
                continue
            else:
                exp_data = ExperimentDataImporter(
                    params=param, software=software,
                    base_dir='/home/dtgillis/ccsim_workspace/data_django', sweep_size=50000000)

                if additive:
                    exp_data.parse_additive_data()
                else:
                    exp_data.parse_epis_results()


if __name__ == '__main__':
    # parse_data(additive=True)
    parse_data(additive=False)
    #parse_epis_data()