"""
Created on May 30, 2014

@author: Daniel Gillis
"""
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ccsimUI.settings'
import experiment.models as exp
from scipy.stats import genextreme
import numpy as np


def create_software():
    """
    Creates the software records
    """

    for software in ['bagpipe', 'plink', 'emmax', 'htree']:
        exp.Software.objects.create_software(name=software).save()


def create_gev_models():
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
    gev_model_list = []
    for mouse_per in ['inf', '1', '5', '10']:

        for software in exp.Software.objects.all():

            if software.name == 'htree' and (mouse_per == '5' or mouse_per == '10'):
                continue
            else:

                data_file = base_dir + dir_dict[mouse_per] + software.name + '.evd'
                np_extreme_values = np.genfromtxt(data_file)
                if software.name in ['plink', 'emmax']:
                    np_extreme_values = -np.log(np_extreme_values)
                shape, location, scale = genextreme.fit(np_extreme_values, -1, loc=np_extreme_values.mean())
                gev_model_list.append(exp.GevModelParam(
                    software=software, mouse_per_strain=mouse_per,
                    location=location, scale=scale, shape=shape, strains=150, var_env=.25))

    ## additive large strain numbers models
    base_dir = '/home/dtgillis/ccsim_workspace/evd/strain_sweep'

    for mouse_per in ['inf']:

        for software in exp.Software.objects.filter(name='emmax'):

            for strain_num in [300, 450, 900]:
                data_file = base_dir + os.sep + 'CC_0_0_0_' + str(strain_num) + '.' + software.name + '.top'
                np_extreme_values = np.genfromtxt(data_file)
                np_extreme_values = -np.log(np_extreme_values)
                shape, location, scale = genextreme.fit(np_extreme_values, -1, loc=np_extreme_values.mean())
                gev_model_list.append(exp.GevModelParam(
                    software=software, mouse_per_strain=mouse_per,
                    location=location, scale=scale, shape=shape, strains=strain_num, var_env=.25))

    exp.GevModelParam.objects.bulk_create(gev_model_list)

    ## additive large strain numbers models
    base_dir = '/home/dtgillis/ccsim_workspace/evd/env_sweep'
    gev_model_list = []
    for mouse_per in ['inf', '1', '5', '10']:
        for var_env in [.05, .50]:
            for software in exp.Software.objects.filter(name='emmax'):
                if mouse_per == 'inf':
                    data_file = base_dir + os.sep + 'CC_0_0_0_' + str(int(var_env * 100)) + '_150.emmax.top'
                else:
                    data_file = base_dir + os.sep + 'CC_0_0_0_' + str(int(var_env * 100)) + '_150.' + mouse_per + '.emmax.top'

                np_extreme_values = np.genfromtxt(data_file)
                np_extreme_values = -np.log(np_extreme_values)
                shape, location, scale = genextreme.fit(np_extreme_values, -1, loc=np_extreme_values.mean())
                gev_model_list.append(exp.GevModelParam(
                    software=software, mouse_per_strain=mouse_per,
                    location=location, scale=scale, shape=shape, strains=150, var_env=var_env))

    exp.GevModelParam.objects.bulk_create(gev_model_list)

    return 0


def create_epistatic_parameters():
    """
    creates initial epistatic parameter records in the database
    """
    var_env = .25
    parameters_list = []
    for var_qtl in [.05, .1, .15, .20, .25]:
        for snp_config in ['1_1']:
            for mouse_per in ['inf', '1', '5', '10']:
                for multiplier in [.5, 2.0]:
                    var_gen = 1.0 - var_qtl - var_env
                    parameters_list.append(exp.EpistaticParameter(
                        snp_config=snp_config, var_qtl=var_qtl, mouse_per_strain=mouse_per,
                        var_env=var_env, var_gen=var_gen, strains=150, multiplier=multiplier))
    exp.EpistaticParameter.objects.bulk_create(parameters_list)


def create_additive_parameters():
    """
    creates initial additive parameter records in the database

    """
    var_env = .25
    parameters_list = []
    for var_qtl in [.05, .1, .15, .20, .25]:
        for snp_config in ['1_0', '2_0', '3_0']:
            for mouse_per in ['inf', '1', '5', '10']:
                var_gen = 1.0 - var_qtl - var_env
                parameters_list.append(exp.AdditiveParameter(
                    snp_config=snp_config, var_qtl=var_qtl, mouse_per_strain=mouse_per,
                    var_env=var_env, var_gen=var_gen, strains=150))
    exp.AdditiveParameter.objects.bulk_create(parameters_list)


def create_additive_large_strain_parameters():
    """
    creates initial additive model parameters with sweep on number of strains
    only infinite models
    :return:
    """
    var_env = .25
    parameters_list = []
    for var_qtl in [.05, .1, .15]:
        for snp_config in ['1_0']:
            for mouse_per in ['inf']:
                for strain_num in [150, 300, 450, 900]:
                    var_gen = 1.0 - var_qtl - var_env
                    parameters_list.append(exp.AdditiveStrainSweepParameter(
                        snp_config=snp_config, var_qtl=var_qtl, mouse_per_strain=mouse_per,
                        var_env=var_env, var_gen=var_gen, strains=strain_num))

    exp.AdditiveStrainSweepParameter.objects.bulk_create(parameters_list)

def create_additive_environment_sweep_parameters():
    """
    creates initial additive model parameters with sweep on environmental effects

    :return:
    """
    strain_num = 150
    parameters_list = []
    for var_qtl in [.05, .1, .15]:
        for snp_config in ['1_0']:
            for mouse_per in ['inf', '1', '5', '10']:
                for var_env in [.05, .25, .50]:
                    var_gen = 1.0 - var_qtl - var_env
                    parameters_list.append(exp.AdditiveEnvironmentSweepParameter(
                        snp_config=snp_config, var_qtl=var_qtl, mouse_per_strain=mouse_per,
                        var_env=var_env, var_gen=var_gen, strains=strain_num))

    exp.AdditiveEnvironmentSweepParameter.objects.bulk_create(parameters_list)

if __name__ == '__main__':
    create_software()
    create_additive_parameters()
    create_epistatic_parameters()
    create_additive_large_strain_parameters()
    create_additive_environment_sweep_parameters()
    create_gev_models()
