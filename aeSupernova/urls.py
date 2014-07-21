from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from login import views
from aeSupernova import views as supernovaviews
import login

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aeSupernova.views.home', name='home'),
    # url(r'^aeSupernova/', include('aeSupernova.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', 'aeSupernova.view.index'),
    url(r'^index/$', supernovaviews.index, name='index.html'),
    url(r'^opticalSheet/', include('aeSupernova.opticalSheet.urls')),
    url(r'^datafile/', include('aeSupernova.datafile.urls')),
    url(r'^header/', include('aeSupernova.header.urls')),
    url(r'^generator/', include('aeSupernova.generator.urls')),
    url(r'^control/', include('aeSupernova.control.urls')),
    url(r'^presentation/', include('aeSupernova.presentation.urls')),
    url(r'^encoder/', include('aeSupernova.encoder.urls')),
    url(r'^lerJupiter/', include('aeSupernova.lerJupiter.urls')),
    url(r'^algeLin/', include('aeSupernova.algeLin.urls')),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.user_logout, name='logout'),
    )
