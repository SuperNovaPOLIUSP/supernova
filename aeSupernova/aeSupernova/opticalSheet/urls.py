from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'aeSupernova.opticalSheet.opticalSheet.openSite'),
    url(r'^findCourses/$', 'aeSupernova.opticalSheet.opticalSheet.findCourses'),
    url(r'^getCourses/$', 'aeSupernova.opticalSheet.opticalSheet.getCourses'),
    url(r'^expandCourse/$', 'aeSupernova.opticalSheet.opticalSheet.expandCourse'),
    url(r'^findOffers/$', 'aeSupernova.opticalSheet.opticalSheet.findOffers'),
    url(r'^getAnswerTypes/$', 'aeSupernova.opticalSheet.opticalSheet.getAnswerTypes'),
    url(r'^getQuestions/$', 'aeSupernova.opticalSheet.opticalSheet.getQuestions'),
    url(r'^storeQuestions/$', 'aeSupernova.opticalSheet.opticalSheet.storeQuestions'),
    url(r'^findOpticalSheetByTimePeriod_Cycle_Term/$', 'aeSupernova.opticalSheet.opticalSheet.findOpticalSheetByTimePeriod_Cycle_Term'),
    url(r'^findOpticalSheetById/$', 'aeSupernova.opticalSheet.opticalSheet.findOpticalSheetById'),
    url(r'^store/$', 'aeSupernova.opticalSheet.opticalSheet.store'),
    url(r'^printOpticalSheet/$', 'aeSupernova.opticalSheet.opticalSheet.printOpticalSheet'),
    url(r'^getPrintedOpticalSheet/$', 'aeSupernova.opticalSheet.opticalSheet.getPrintedOpticalSheet'),
    url(r'^printAMC/$', 'aeSupernova.opticalSheet.opticalSheet.printAMC'),
    url(r'^getPrintedAMC/$', 'aeSupernova.opticalSheet.opticalSheet.getPrintedAMC'),
    url(r'^printQualitativeQuestionnaire/$', 'aeSupernova.opticalSheet.opticalSheet.printQualitativeQuestionnaire'),
    url(r'^getPrintedQualitativeQuestionnaire/$', 'aeSupernova.opticalSheet.opticalSheet.getPrintedQualitativeQuestionnaire'),
    url(r'^getEncodings/$', 'aeSupernova.opticalSheet.opticalSheet.getEncodings'),
    url(r'^removeCycleFromOpticalSheet/$', 'aeSupernova.opticalSheet.opticalSheet.removeCycleFromOpticalSheet'),
    url(r'^listOldOpticalSheets/$', 'aeSupernova.opticalSheet.opticalSheet.listOldOpticalSheets'),
)
