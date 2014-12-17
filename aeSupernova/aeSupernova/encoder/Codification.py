from pulsarInterface.Answer import Answer
from pulsarInterface.Cycle import Cycle
from pulsarInterface.Offer import Offer, OfferError
from pulsarInterface.OpticalSheet import OpticalSheet, OpticalSheetError
from pulsarInterface.TimePeriod import TimePeriod


class Codification(object):
    
    def __init__(self, name, idTimePeriod):
        self.name = name
        self.possibleOffers = []
        self.offers = None
        self.idTimePeriod = idTimePeriod
        self.os = None
        
    @staticmethod
    def new(name, idTimePeriod):
        codification = Codification(name, idTimePeriod)
        codification.os = OpticalSheet('Codificada')
        codification.os.setEncodingName(name)
        codification.os.store()
        return codification
    
    @staticmethod
    def update(idOpticalSheet, idTimePeriod):
        os = OpticalSheet.pickById(idOpticalSheet)
        hasAnswers = False
        answersDict = Answer.countAnswers(opticalSheet = os)
        for alternative in answersDict:
            if answersDict[alternative] > 0:
                hasAnswers = True
        if hasAnswers:
            return "Can not edit Codification that has answers"
        codification = Codification(os.encodingName, idTimePeriod)
        codification.os = os
        return codification
        
    def fillPossibleOffers(self, idCycle, term):
        cycle = Cycle.pickById(idCycle)
        cycle.completeMandatoryIdealTerms()
        cycle.completeElectiveIdealTerms()
        possibleCourses = []
        for term in cycle.mandatoryIdealTerms:
            for course in cycle.mandatoryIdealTerms[term]:
                possibleCourses.append(course)
        for term in cycle.electiveIdealTerms:
            for course in cycle.electiveIdealTerms[term]:
                possibleCourses.append(course)
        for idealTermCourse in possibleCourses:
            for offer in Offer.find(course = idealTermCourse.course, timePeriod = TimePeriod.pickById(self.idTimePeriod)):
                self.possibleOffers.append(offer)
        
    def setOffers(self, offers):
        for offer in offers:
            if not isinstance(offer, Offer):
                raise OfferError('Input must be a list of Offer objects')
        self.offers = offers
        
    def fillOffers(self):
        self.os.fillOpticalSheetFields()
        self.offers = []
        for field in self.os.fields:
            self.offers.append(field.offer)
        
    def setOpticalSheet(self, opticalSheet):
        if not isinstance(opticalSheet,OpticalSheet):
            raise OpticalSheetError('opticalSheet must be an OpticalSheet type object')
        self.os = opticalSheet
        
    def store(self):
        self.os.encodingName = self.name
        self.os.fields = []
        for offer in self.offers:
            self.os.addOpticalSheetField([offer],self.offers.index(offer))
        self.os.store()
