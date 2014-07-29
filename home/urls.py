from django.conf.urls import url

from home import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.additive ),
    url(r'^locus_ajax/$', views.locus_ajax_stat),
    url(r'^overall_power_ajax/$', views.overall_power_ajax),
    url(r'^overall_failure_ajax/$', views.overall_failure_ajax)
]