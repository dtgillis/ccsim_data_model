from django.conf.urls import url

from sensitive import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^sensitivity/$', views.sensitive ),
    url(r'^sensitivityajax/$', views.sensitivity_ajax),
    url(r'^sensitivitypowerajax/$', views.sensitivity_ajax_power)
]