'''
Created on May 30, 2014

@author: dtgillis
'''
import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'ccsimUI.settings'; import django
from sensitive.data import SensitivityImporter
from sensitive.models import Parameters
from sensitive.models import Software
from sensitive.models import GevModelParams
from sensitive.models import ExtremeValues
from scipy.stats import genextreme
import numpy as np

def parse_gev_models_r():
    
    base_dir = '/home/dtgillis/ccsim_workspace/evd/'
    dir_dict = {'inf': 'CC_0_0_0_150/',
                '1': 'CC_0_0_0_150.1/',
                '5': 'CC_0_0_0_150.5/',
                '10': 'CC_0_0_0_150.10/'}
    
    for mousePer in ['inf', '1', '5', '10']:
        
        for software in Software.objects.all():
            
            if software.name == 'htree' and ( mousePer == '5' or mousePer == '10' ):
                continue
            else:
                
                data_file = base_dir + dir_dict[mousePer] + software.name + '.gev'
                
                fp = open(data_file,'r')
                
                lines = fp.readlines()
                
                data_fields = lines[1].split()
                
                tmp_gev = GevModelParams.objects.create_gev_model(
                    software=software, mousePerStrain=mousePer,
                    location=data_fields[0], scale=data_fields[2], shape=data_fields[4])
                tmp_gev.save()
                
                fp.close()
                
                # now load up the actual thresholds of the models 
                
                data_file = base_dir + dir_dict[mousePer] + software.name + '.thresh'
                
                for line in open(data_file, 'r'):
                    
                    tmp_extreme = ExtremeValues.objects.create_extreme_value(
                        mousePerStrain=mousePer, software=software,
                        alpha=line.split()[0], threshold=line.split()[1])
                    
                    tmp_extreme.save()


def create_gev_models_scipy():

    base_dir = '/home/dtgillis/ccsim_workspace/evd/'
    dir_dict = {'inf': 'CC_0_0_0_150/',
            '1': 'CC_0_0_0_150.1/',
            '5': 'CC_0_0_0_150.5/',
            '10': 'CC_0_0_0_150.10/'}

    for mouse_per in ['inf', '1', '5', '10']:

        for software in Software.objects.all():

            if software.name == 'htree' and ( mouse_per == '5' or mouse_per == '10' ):
                continue
            else:

                data_file = base_dir + dir_dict[mouse_per] + software.name + '.evd'

                np_extreme_values = np.genfromtxt(data_file)

                if software.name in ['plink', 'emmax']:
                    np_extreme_values = -np.log(np_extreme_values)

                shape, location, scale = genextreme.fit(np_extreme_values, -1, loc=np_extreme_values.mean())

                tmp_gev_model = GevModelParams.objects.create_gev_model(
                    software=software, mousePerStrain=mouse_per,
                    location=location, scale=scale, shape=shape)
                tmp_gev_model.save()

                frozen_gev = genextreme(shape, loc=location, scale=scale)

                for quantile in [.95, .99]:

                    extreme_value = frozen_gev.ppf(quantile)

                    tmp_extreme_model = ExtremeValues.objects.create_extreme_value(
                        mousePerStrain=mouse_per, software=software,
                        alpha=quantile, threshold=extreme_value)

                    tmp_extreme_model.save()

    return 0
def create_parameters():
    
    var_env = .25
    for var_qtl in [.05, .1, .25]:
        for snp_config in ['1_0', '1_1', '2_0', '3_0']:
            for mouse_per in ['inf', '1', '5', '10']:
                var_gen = 1.0 - var_qtl - var_env
                tmp_param = Parameters.objects.create_param(
                    snp_config=snp_config, varQtl=var_qtl, mousePerStrain=mouse_per,
                    varEnv=var_env, varGen=var_gen, strains=150)
                tmp_param.save()

                    
def parse_data():

    for software in Software.objects.all():

        for params in Parameters.objects.all():
            
            if software.name=='htree' and (params.mousePerStrain == '5' or params.mousePerStrain=='10'):
                continue
            else:
                sens = SensitivityImporter(
                    params=params, software=software,
                    base_dir='/home/dtgillis/ccsim_workspace/data_django')
                sens.parse_data()




if __name__ == '__main__':
    #create_gev_models_scipy()
    #createParameters()
    #parseGevModels()
    parse_data()