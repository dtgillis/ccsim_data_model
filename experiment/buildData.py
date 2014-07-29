"""
Created on May 30, 2014

@author: Daniel Gillis
"""
import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'ccsimUI.settings'; import django
from experiment.models import Parameters
from experiment.models import Software
from experiment.models import GevModelParams
from scipy.stats import genextreme
import numpy as np


def create_gev_models_scipy():
    """
    parses the top values and creates
    extreme value dist and saves the
    parameters to the database
    """

    base_dir = '/home/dtgillis/ccsim_workspace/evd/'
    dir_dict = {'inf': 'CC_0_0_0_150/',
                '1': 'CC_0_0_0_150.1/',
                '5': 'CC_0_0_0_150.5/',
                '10': 'CC_0_0_0_150.10/'}

    for mouse_per in ['inf', '1', '5', '10']:

        for software in Software.objects.all():

            if software.name == 'htree' and (mouse_per == '5' or mouse_per == '10'):
                continue
            else:

                data_file = base_dir + dir_dict[mouse_per] + software.name + '.evd'

                np_extreme_values = np.genfromtxt(data_file)

                if software.name in ['plink', 'emmax']:
                    np_extreme_values = -np.log(np_extreme_values)

                shape, location, scale = genextreme.fit(np_extreme_values, -1, loc=np_extreme_values.mean())

                tmp_gev_model = GevModelParams.objects.create_gev_model(
                    software=software, mouse_per_strain=mouse_per,
                    location=location, scale=scale, shape=shape)
                tmp_gev_model.save()

    return 0


def create_parameters():
    """
    creates initial parameter records in the database

    """
    var_env = .25
    for var_qtl in [.05, .1, .25]:
        for snp_config in ['1_0', '1_1', '2_0', '3_0']:
            for mouse_per in ['inf', '1', '5', '10']:
                var_gen = 1.0 - var_qtl - var_env
                tmp_param = Parameters.objects.create_param(
                    snp_config=snp_config, varQtl=var_qtl, mousePerStrain=mouse_per,
                    varEnv=var_env, varGen=var_gen, strains=150)
                tmp_param.save()

                    

if __name__ == '__main__':
    create_parameters()
    create_gev_models_scipy()
