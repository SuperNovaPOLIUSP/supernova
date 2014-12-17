from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'aeSupernova.generator.generator.openSite'),
    url(r'^lerJupiter/$', 'aeSupernova.lerJupiter.lerJupiter.lerJupiter'),
    url(r'^$', 'aeSupernova.generator.generator.openSite'),
    url(r'^loadCourses/$', 'aeSupernova.generator.generator.loadCourses'),
    url(r'^generateCourses/$', 'aeSupernova.generator.generator.generateCourses'),
)
