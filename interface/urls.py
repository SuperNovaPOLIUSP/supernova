from django.conf.urls import patterns, url
from interface import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'interface'),
    url(r'^professor/$', views.professor, name = 'professor'),
    url(r'^professor/(?P<idProfessor>\d+)/$', views.professor_detail, name = 'professor_detail'),
    url(r'^professor/(?P<idProfessor>\d+)/edit/$', views.professor_edit, name = 'professor_edit'), 
    url(r'^professor/(?P<idProfessor>\d+)/delete/$', views.professor_delete, name = 'professor_delete'),
    url(r'^professor/create/$', views.professor_create, name = 'professor_create'),       
    url(r'^offer/$', views.offer, name = 'offer'),
    url(r'^offer/(?P<idOffer>\d+)/$', views.offer_detail, name = 'offer_detail'),
    url(r'^offer/(?P<idOffer>\d+)/edit/$', views.offer_edit, name = 'offer_edit'),
    url(r'^offer/(?P<idOffer>\d+)/delete/$', views.offer_delete, name = 'offer_delete'),
    url(r'^offer/(?P<idTimePeriod>\d+)/(?P<idCourse>\d+)/create/$', views.offer_create, name = 'offer_create'),
    url(r'^offerList/$', views.offer_list, name = 'offer_list'),
    url(r'^offerListGenerate/$', views.offer_list_generate, name = 'offer_list_generate'),                    
    )