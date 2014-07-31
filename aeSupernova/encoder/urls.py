from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'aeSupernova.encoder.encoder.openSite'),
    url(r'^createEncoding/$', 'aeSupernova.encoder.encoder.newEncoding'),
    url(r'^deleteEncoding/$', 'aeSupernova.encoder.encoder.deleteEncoding'),
    url(r'^loadEncoding/$', 'aeSupernova.encoder.encoder.fillOffers'),
    url(r'^showPossibleOffers/$', 'aeSupernova.encoder.encoder.showPossibleOffers'),
    url(r'^store/$', 'aeSupernova.encoder.encoder.setOffers'),
    url(r'^deleteEncoding/$', 'aeSupernova.encoder.encoder.deleteEncoding'),
    url(r'^showPossibleEncodings/$', 'aeSupernova.encoder.encoder.possibleCodifications'),
)
