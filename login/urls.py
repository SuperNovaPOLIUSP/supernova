from django.conf.urls import patterns, include, url
from login import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.user_login, name = 'login'),
    url(r'^login_control/$', views.login_control, name = 'login_control'),
    url(r'^login_control_generate/$', views.login_control_generate, name = 'login_control_generate'),             
    )