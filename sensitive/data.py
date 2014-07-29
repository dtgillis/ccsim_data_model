'''
Created on May 30, 2014

@author: dtgillis
'''

import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'ccsimUI.settings';
from sensitive.models import Sensitivity
from sensitive.models import GevModelParams
import numpy as np
from rpy2 import robjects as r
from scipy.stats import genextreme

class SensitivityImporter(object):
    '''
    Class used to import data from text files into the
    database.

    requires a param and software object.

    requires a base direcrtory pointing to files
    '''
   

    def __init__(self, params, software, base_dir):
        '''
        Constructor
        Should take in a params object and also a software object 
        
        '''
        self.params = params
        self.software = software
        self.base_dir = base_dir
        self.data_prefix = self.params.__unicode__() + '.' + self.software.name + '.top'

        self.gevModelParams = GevModelParams.objects.filter(
            software=software, mousePerStrain=params.mousePerStrain).get()

        r.r(''' require('evd')''')
    
    def get_adjusted_pvalue_r(self, p_value):
        
        
        r.globalenv['loc'] = self.gevModelParams.location
        
        r.globalenv['shape'] = self.gevModelParams.shape
        
        r.globalenv['scale'] = self.gevModelParams.scale
        
        r.globalenv['pvalue'] = p_value
        
        tmp_ans = r.r('''
        pgev( pvalue , loc=loc,scale=scale,shape=shape,lower.tail=FALSE)
        ''')
        
        return tmp_ans[0]

    def get_adjusted_pvalue_scipy(self, p_value, gev):

        adj_p_value = gev.sf(p_value)

        return adj_p_value

    def parse_data(self):
        
        data_file = self.base_dir + '/' + self.data_prefix
        
        # what run number ?
        
        run_number = 1

        np_extreme_values = np.genfromtxt(data_file)

        if self.software.name in ['plink', 'emmax']:
            np_extreme_values = -np.log(np_extreme_values)

        frozen_gev = genextreme(
            self.gevModelParams.shape, loc=self.gevModelParams.location,
            scale=self.gevModelParams.scale)

        for p_value in np_extreme_values:
            
            tmp_sens = Sensitivity.objects.create_sensitivity(
                parameter=self.params, software=self.software,
                runNumber=run_number, pValue=p_value,
                adjPvalue=self.get_adjusted_pvalue_scipy(p_value, frozen_gev))
            tmp_sens.save()
            run_number += 1
        
        return 0 
            
            
            
        
            
        
    