from django.shortcuts import render 
from django.http import HttpResponseRedirect,HttpResponse
from experiment_data import models as data_models
from experiment import models as exp_models
from django.db.models import Q
import json
import numpy as np
# Create your views here.

def additive(request,param=-1,softwareID=-1):
    # get the softwares
    software_choice = []
    softwares = exp_models.Software.objects.values_list('name', flat=True).distinct()
    for software in softwares:
        software_choice.append(str(software))

    # get the parameters
    vqtls = exp_models.Parameters.objects.values_list('var_qtl', flat=True).distinct()
    vqtl_choice = []
    for vqtl in vqtls:
        vqtl_choice.append(str(vqtl))

    # get the snpconfigs
    snp_config_choice = []
    snps = exp_models.Parameters.objects.values_list('snp_config', flat=True).distinct()
    for snp in snps:
        snp_config_choice.append(str(snp))

    return render(request, 'locus_specific.html',
                  {'varQtl': vqtl_choice, 'snpConChoice': snp_config_choice,
                   'softwares': software_choice})


def bad_ajax_request():
    error = {'error': 'bad call'}
    error_return = HttpResponse(json.dumps(error),
                                status=400, content_type='application/json')

    return error_return

#
# def locus_ajax(request):
#     """
#
#     :param request:
#     :return: data in json form
#     """
#     error = {'error': 'bad call'}
#     error_return = HttpResponse(json.dumps(error),
#                                 status=400, content_type='application/json')
#     #print request.POST['varQtl']
#     if 'varQtl' in request.GET:
#         var_qtl = str(request.GET['varQtl'])
#     else:
#         return error_return
#     if 'software' in request.GET:
#         software = str(request.GET['software'])
#     else:
#         return error_return
#     if 'snp_config' in request.GET:
#         snp_config = str(request.GET['snp_config'])
#     else:
#         return error_return
#
#     # create the different dicts to get back the data we need to d3
#     return_dict = dict()
#
#     mice_per_strain = exp_models.Parameters.objects.values_list('mouse_per_strain', flat=True).distinct()
#
#     for mice_per in mice_per_strain:
#
#         params = exp_models.Parameters.objects.filter(
#             snp_config=snp_config, var_qtl=var_qtl, mouse_per_strain=mice_per)
#
#         software_obj = exp_models.Software.objects.get(name=software)
#
#         sens_values = data_models.AdditiveModel.objects.filter(Q(adj_non_locus_pvalue__lte=.05) |
#                                                                Q(adj_locus_pvalue__lte=.05) |
#                                                                Q(adj_non_chrm_pvalue__lte=.05),
#                                                                software=software_obj, parameter=params).values('runNumber', 'adjPvalue', 'pValue')
#
#         if len(sens_values) != 0:
#
#             return_dict[mice_per] = []
#             for sens in sens_values:
#                 if sens['adjPvalue'] == 0.0:
#                     sens['adjPvalue'] = 1e-15
#                 adjp = -np.log(sens['adjPvalue']);
#
#                 return_dict[mice_per].append(
#                     dict(adjpValue=-np.log(sens['adjPvalue']),
#                          pValue=sens['pValue'], runNumber=sens['runNumber']))
#
#     return HttpResponse(json.dumps(return_dict), status=200, content_type='application/json')
#

def locus_ajax_stat(request):
    """
    :param request:
    :return: json for power curves
    """

    if 'snp_config' in request.GET:
        snp_config = str(request.GET['snp_config'])
    else:
        return bad_ajax_request()

    mice_per_strain = exp_models.Parameters.objects.values_list('mouse_per_strain', flat=True).distinct()

    return_dict = dict()

    #return_dict
    for software_obj in exp_models.Software.objects.all():

        return_dict[software_obj.name] = dict()

        for mouse_per in mice_per_strain:

            params = exp_models.Parameters.objects.filter(
                snp_config=snp_config, mouse_per_strain=mouse_per)

            power_curve = []

            for param in params:

                power_count = data_models.AdditiveModel.objects.filter(
                    parameter=param, software=software_obj, adj_locus_pvalue__lte=.05, ).count()

                power_curve.append({'mouse_per': mouse_per, 'var_qtl': param.var_qtl, 'power': power_count/1000.0})

            return_dict[software_obj.name][mouse_per] = power_curve

    return HttpResponse(json.dumps(return_dict), status=200, content_type='application/json')


def overall_power_ajax(request):
    """
    :param request:
    :return: json for power curves
    """

    if 'snp_config' in request.GET:
        snp_config = str(request.GET['snp_config'])
    else:
        return bad_ajax_request()

    mice_per_strain = exp_models.Parameters.objects.values_list('mouse_per_strain', flat=True).distinct()

    return_dict = dict()

    #return_dict
    for software_obj in exp_models.Software.objects.all():

        return_dict[software_obj.name] = dict()

        for mouse_per in mice_per_strain:

            params = exp_models.Parameters.objects.filter(
                snp_config=snp_config, mouse_per_strain=mouse_per)

            power_curve = []

            for param in params:

                power_count = data_models.AdditiveModel.objects.filter(Q(adj_non_locus_pvalue__lte=.05) |
                                                                       Q(adj_locus_pvalue__lte=.05) |
                                                                       Q(adj_non_chrm_pvalue__lte=.05),
                                                                       software=software_obj, parameter=params).count()

                power_curve.append({'mouse_per': mouse_per, 'var_qtl': param.var_qtl, 'power': power_count/1000.0})

            return_dict[software_obj.name][mouse_per] = power_curve

    return HttpResponse(json.dumps(return_dict), status=200, content_type='application/json')


def overall_failure_ajax(request):
    """
    :param request:
    :return: json for power curves
    """

    if 'snp_config' in request.GET:
        snp_config = str(request.GET['snp_config'])
    else:
        return bad_ajax_request()

    mice_per_strain = exp_models.Parameters.objects.values_list('mouse_per_strain', flat=True).distinct()

    return_dict = dict()

    #return_dict
    for software_obj in exp_models.Software.objects.all():

        return_dict[software_obj.name] = dict()

        for mouse_per in mice_per_strain:

            params = exp_models.Parameters.objects.filter(
                snp_config=snp_config, mouse_per_strain=mouse_per)

            power_curve = []

            for param in params:

                power_count = data_models.AdditiveModel.objects.filter(Q(adj_non_chrm_pvalue__lte=.05) ,
                                                                       adj_locus_pvalue__gt=.05,
                                                                       parameter=param, software=software_obj).count()

                power_curve.append({'mouse_per': mouse_per, 'var_qtl': param.var_qtl, 'power': power_count/1000.0})

            return_dict[software_obj.name][mouse_per] = power_curve

    return HttpResponse(json.dumps(return_dict), status=200, content_type='application/json')

def roc_curve_ajax(response):

    if 'snp_config' in response.GET:
        snp_config = response.GET['snp_config']
    else:
        return bad_ajax_request()


    return_dict = dict()

    params = exp_models.Parameters.objects.filter(snp_config='1_1')

    var_qtls = params.value_list('var_qtl', flat=True).distinct()

    for var_qtl in var_qtls:

        param = params.filter(var_qtl=var_qtl)

        return_dict[var_qtl] = dict()

        for software in exp_models.Software.objects.all():


            software_line = []

            for i in range(1, 21):

                pvalue = i * .05
                tp = data_models.AdditiveModel.objects.filter(software=software, param=param, adj_locus_pvalue__lte=pvalue)
                fp = data_models.AdditiveModel.objects.filter(software=software, param=param, adj_non_locus_pvalue__lte=pvalue)
                software_line.append([fp, tp])


            return_dict['var_qtl'][software.name] = software_line

    return json.dump(return_dict, status=200, content_type='application/json')











        
        
        
        
        
        
        
        
    
        