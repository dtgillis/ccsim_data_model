'''
Created on Jun 2, 2014

@author: dtgillis
'''

from django import forms
from sensitive import models as m 

class SensitivityForm(forms.Form):
    '''
    classdocs
    '''
    varQtlChoices = [] 
    snpConChoice = [] 
    varQtl = forms.ChoiceField(varQtlChoices) 
    snp_config = forms.ChoiceField(snpConChoice)
    
    def __init__(self, ):
        '''
        Constructor
        '''
        self.vqtlChoice = [] 
        vqtls = m.Parameters.objects.values_list('varQtl',flat=True).distinct()
        for vqtl in vqtls:
            self.vqtlChoice.append([str(vqtl),str(vqtl)])
        
        self.snpConChoice = []     
        snps = m.Parameters.objects.values_list('snp_config',flat=True).distinct()
        
        for snp in snps:
            self.snpConChoice.append([str(snp),str(snp)])
            
    
    
    
  
    
    
    
        
        