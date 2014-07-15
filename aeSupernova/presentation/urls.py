from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'aeSupernova.presentation.presentation.openSite'),
    url(r'^findReports/$', 'aeSupernova.presentation.presentation.findReports'),
    url(r'^getReport/$', 'aeSupernova.presentation.presentation.getReport'),

)
