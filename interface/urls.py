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
    #url(r'^offer/(?P<idOffer>\d+)/$', views.professor_detail, name = 'offer_detail'),
    #url(r'^offer/(?P<idOffer>\d+)/edit/$', views.professor_edit, name = 'offer_edit'), 
    #url(r'^offer/(?P<idOffer>\d+)/delete/$', views.professor_delete, name = 'offer_delete'),
    #url(r'^offer/create/$', views.professor_create, name = 'offer_create'),                  
    )