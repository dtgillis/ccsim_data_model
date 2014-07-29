'''
Created on May 30, 2014

@author: dtgillis
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ccsimUI.settings'
import experiment_data.models as exp_data
import experiment.models as exp
import numpy as np
from scipy.stats import genextreme


class ExperimentDataImporter(object):
    """
    Class used to import data from text files into the
    database.

    requires a param and software object.

    requires a base direcrtory pointing to files
    """
   

    def __init__(self, params, software, base_dir, sweep_size):
        """
        Constructor
        Should take in a params object and also a software object 
        
        """
        self.params = params
        self.software = software
        self.base_dir = base_dir
        self.sweep_size = sweep_size
        self.data_prefix = self.params.__unicode__() + '.' + self.software.name
        self.gev_model_params = exp.GevModelParam.objects.filter(
            software=software, mouse_per_strain=params.mouse_per_strain).get()

    def get_adjusted_pvalue_scipy(self, p_value, gev):

        adj_p_value = gev.sf(p_value)

        return adj_p_value

    def parse_additive_data(self):

        if self.software.name != 'bagpipe':
            data_file = self.base_dir + os.sep + self.data_prefix + '.' + str(self.sweep_size/1000000) + '.dat'
        else:
            data_file = self.base_dir + os.sep + self.data_prefix + '_add.' + str(self.sweep_size/1000000) + '.dat'
        run_number = 1

        np_extreme_values = np.genfromtxt(data_file, skip_header=1, usecols=(1, 2, 3))

        frozen_gev = genextreme(
            self.gev_model_params.shape, loc=self.gev_model_params.location,
            scale=self.gev_model_params.scale)
        additive_models_list = []
        for data in np_extreme_values:

            adj_pvalues = self.get_adjusted_pvalue_scipy(data, frozen_gev)

            additive_models_list.append(exp_data.AdditiveModel(
                parameter=self.params, software=self.software,
                run_number=run_number, locus_span=self.sweep_size, locus_pvalue=data[0],
                adj_locus_pvalue=adj_pvalues[0], non_locus_pvalue=data[1],
                adj_non_locus_pvalue=adj_pvalues[1], non_chrm_pvalue=data[2],
                adj_non_chrm_pvalue=adj_pvalues[2]))
            run_number += 1

        exp_data.AdditiveModel.objects.bulk_create(additive_models_list)
        
        return 0

    def parse_epis_results(self):

        data_file = \
            self.base_dir + os.sep \
            + 'CC_1_1_.5' + self.data_prefix.split('CC_1_1')[1] \
            + '.' + str(self.sweep_size/1000000) + '.dat'

        run_number = 1

        np_extreme_values = np.genfromtxt(data_file, skip_header=1, usecols=(1, 2, 3))

        frozen_gev = genextreme(
            self.gev_model_params.shape, loc=self.gev_model_params.location,
            scale=self.gev_model_params.scale)

        for data in np_extreme_values:

            adj_pvalues = self.get_adjusted_pvalue_scipy(data, frozen_gev)

            if run_number <= 1000:
                snp_id = 'fa0'
            else:
                snp_id = 'fa1'

            tmp_model = exp_data.EpistaticModel.objects.create_epistatic_model(
                parameter=self.params, software=self.software,
                run_number=run_number % 1000, locus_span=self.sweep_size,
                snp_id=snp_id, locus_pvalue=data[0],
                adj_locus_pvalue=adj_pvalues[0], non_locus_pvalue=data[1],
                adj_non_locus_pvalue=adj_pvalues[1], non_chrm_pvalue=data[2],
                adj_non_chrm_pvalue=adj_pvalues[2], multiplier=.5)

            tmp_model.save()

            run_number += 1

        return 0