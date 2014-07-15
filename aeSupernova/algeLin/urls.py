from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','aeSupernova.algeLin.algeLin.initAlgeLin'),
    url(r'^imprimir/$', 'aeSupernova.algeLin.algeLin.algeLin'),
    url(r'^abreFolha/$', 'aeSupernova.algeLin.algeLin.abrirFolha'),
    url(r'^imagem/$', 'aeSupernova.algeLin.algeLin.imagemAlgeLin'),
)

