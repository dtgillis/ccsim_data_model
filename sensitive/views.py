from django.shortcuts import render 
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from sensitive import models as m 
import json
import numpy as np
# Create your views here.


    
def index(request):
    
    return HttpResponse(output)



def sensitive(request,param=-1,softwareID=-1):
    # get the softwares 
    softwareChoice = [] 
    softwares = m.Software.objects.values_list('name',flat=True).distinct()
    for software in softwares:
        softwareChoice.append(str(software))
    
    # get the parameters 
    vqtls = m.Parameters.objects.values_list('varQtl',flat=True).distinct()
    vqtlChoice = [] 
    for vqtl in vqtls:
        vqtlChoice.append(str(vqtl))
    
    # get the snpconfigs 
    snpConChoice = []     
    snps = m.Parameters.objects.values_list('snp_config',flat=True).distinct()
    for snp in snps:
        snpConChoice.append(str(snp))
    
    
    return render(request, 'sensitivity.html',
                  {'varQtl': vqtlChoice, 'snpConChoice': snpConChoice,
                   'softwares': softwareChoice})


def bad_ajax_request():
    error = {'error': 'bad call'}
    error_return = HttpResponse(json.dumps(error),
                                status=400, content_type='application/json')

    return error_return


def sensitivity_ajax(request):
    """

    :param request:
    :return: data in json form
    """
    error = {'error': 'bad call'}
    error_return = HttpResponse(json.dumps(error),
                                status=400, content_type='application/json')
    #print request.POST['varQtl']
    if request.GET.has_key('varQtl'):
        var_qtl = str(request.GET['varQtl'])
    else:
        return error_return
    if request.GET.has_key('software'):
        software = str(request.GET['software'])
    else:
        return error_return
    if request.GET.has_key('snp_config'):
        snp_config = str(request.GET['snp_config'])
    else: 
        return error_return

    # create the different dicts to get back the data we need to d3
    return_dict = dict()
    
    mice_per_strain = m.Parameters.objects.values_list('mousePerStrain', flat=True).distinct()
    
    for mice_per in mice_per_strain:
        
        #returnDict[str(micePer)] = dict()
        # get parameter object 
        params = m.Parameters.objects.filter(
            snp_config=snp_config, varQtl=var_qtl, mousePerStrain=mice_per)
        
        software_obj = m.Software.objects.get(name=software)
        
        sens_values = m.Sensitivity.objects.filter(
            software=software_obj, parameter=params).values(
            'runNumber', 'adjPvalue', 'pValue')

        if len(sens_values) != 0:

            return_dict[mice_per] = []
            for sens in sens_values:
                if sens['adjPvalue'] == 0.0:
                    sens['adjPvalue'] = 1e-15
                adjp = -np.log(sens['adjPvalue']);

                return_dict[mice_per].append(
                    dict(adjpValue=-np.log(sens['adjPvalue']),
                         pValue=sens['pValue'], runNumber=sens['runNumber']))

    return HttpResponse(json.dumps(return_dict), status=200, content_type='application/json')


def sensitivity_ajax_power(request):
    """
    :param request:
    :return: json for power curves
    """

     #print request.POST['varQtl']
    # if request.GET.has_key('varQtl'):
    #     var_qtl = str(request.GET['varQtl'])
    # else:
    #     return bad_ajax_request()
    # if request.GET.has_key('software'):
    #     software = str(request.GET['software'])
    # else:
    #     return bad_ajax_request()
    if request.GET.has_key('snp_config'):
        snp_config = str(request.GET['snp_config'])
    else:
        return bad_ajax_request()

    mice_per_strain = m.Parameters.objects.values_list('mousePerStrain', flat=True).distinct()



    return_dict = dict()

    #return_dict
    for software_obj in m.Software.objects.all():

        return_dict[software_obj.name] = dict()

        for mouse_per in mice_per_strain:

            params = m.Parameters.objects.filter(
                    snp_config=snp_config, mousePerStrain=mouse_per)

            power_curve = []

            for param in params:

                params = m.Parameters.objects.filter(
                    snp_config=snp_config, mousePerStrain=mouse_per)

                power_count = m.Sensitivity.objects.filter(
                    parameter=param, software=software_obj, adjPvalue__lte=.05, ).count()

                power_curve.append({'mouse_per': mouse_per, 'var_qtl': param.varQtl, 'power': power_count/1000.0})

            return_dict[software_obj.name][mouse_per] = power_curve


    return HttpResponse(json.dumps(return_dict), status=200, content_type='application/json')






        
        
        
        
        
        
        
        
    
        