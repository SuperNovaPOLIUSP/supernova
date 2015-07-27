from TimePeriod import TimePeriod
from Professor import Professor
from Course import Course
from Schedule import Schedule
from tools.MySQLConnection import MySQLConnection 

class OfferError(Exception):
    """
     Exception reporting an error in the execution of a Offer method.

    :version:
    :author:
    """
    pass

class Offer(object):

    """
     Representation of an offer in the data base.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key of this offer.

    idOffer  (public)

     The database ID of the course related to this offer.

    course  (public)

     The professor responsible for this offer.

    professor  (public)

     The time period related to this offer.

    timePeriod  (public)

     The college class's number of this offer.

    classNumber  (public)

     It is True if this offer is a practical class, and False if it is a theoretical
     class.

    practical  (public)

     The number of max students allowed in this offer.

    numberOfRegistrationis  (public)

     List of schedules when the lectures related to this offer are held.

    schedules  (public)

    """

    def __init__(self, timePeriod, course, classNumber, practical, professor):
        """
         Creates an Offer object if all the parameters needed are specified, except by
         the numberOfRegistration, which is not necessarily needed.

        @param TimePeriod timePeriod : The offer's time period.
        @param int idCourse : The offer's course associated database key.
        @param int classNumber : The college class's number of the offer.
        @param bool pratica : It's true if the offer is a practical class, and false if it is a theoretical class.
        @param Professor professor : The professor responsible for this offer.
        @param int numberOfRegistrations : The maximum number of students allowed in this offer.
        @return  :
        @author
        """
        #Parameters verification.
        if not isinstance(timePeriod, TimePeriod) or not TimePeriod.pickById(timePeriod.idTimePeriod) == timePeriod:
            raise OfferError('Parameter timePerid must be a TimePeriod object that exists in the database.')
        if not isinstance(course, Course) or not Course.pickById(course.idCourse) == course:
            raise OfferError('Parameter course must be a Course object.')            
        if not isinstance(classNumber, (int, long)):
            raise OfferError('Parameter classNumber must be an int or a long.')
        if not isinstance(practical, (int, long)):
            raise OfferError('Parameter practical must be a bool.')

        #Setting parameters that have set function
        self.setProfessor(professor)
        #Setting other parameters
        self.timePeriod = timePeriod
        self.course = course
        self.classNumber = classNumber
        self.practical = practical
        #Setting None parameters
        self.numberOfRegistrations = None
        self.schedules = []
        self.idOffer = None

    def __eq__(self, other):
        if not isinstance(other, Offer):
            return False
        return self.__dict__ == other.__dict__
  
    def __ne__(self,other):
        return not self.__eq__(other)

    def setProfessor(self, professor):
        """
        Associate a new professor with the offer, if the given professor is a Professor object and there are non not saved changes in it.

        @param Professor professor : The new professor responsible for this offer
        @return  :
        @author
        """
        if not isinstance(professor, Professor) or not Professor.pickById(professor.idProfessor) == professor:
            raise OfferError('Parameter professor must be a Professor object that exists in the database.')
        self.professor = professor

    def setNumberOfRegistrations(self, numberOfRegistrations):
        """
        Checks if the numberOfRegistration is an int or a long and it is bigger or equal 0 and then set the number of registration of this offer.

        @param int numberOfRegistrations : The number of registrations of this offer
        @return  :
        @author
        """
        if not isinstance(numberOfRegistrations, (int, long, type(None))) :
            raise OfferError('Parameter numberOfRegistrations must be an int or a long or None')

        self.numberOfRegistrations = numberOfRegistrations

    def setSchedules(self, schedules):
        """
        Checks if schedules is a list of valid Schedule objects that have no non saved changes, and then sets this offer schedules to the schedules given. 

        @param Schedule schedules : The list of Schedule objects of this offer
        @return  :
        @author
        """
        for schedule in schedules:
            if not isinstance(schedule, Schedule) or not schedule == Schedule.pickById(schedule.idSchedule):
                raise OfferError('Parameter schedules must be a list of Schedule objects')
        self.schedules = schedules

    def fillSchedules(self):
        """
         Finds the schedules associated to this offer through a query in the database.

        @param  :
        @return  :
        @author
        """
        if self.idOffer != None:
            cursor = MySQLConnection()
            schedulesData = cursor.execute('SELECT idSchedule FROM rel_offer_schedule WHERE idOffer = ' + str(self.idOffer))
            self.schedules = [Schedule.pickById(scheduleData[0]) for scheduleData in schedulesData]
        else:
            raise OfferError('idOffer is not defined')



    @staticmethod
    def offersName(setsOfOffers):
        """
         Receives a list of list of offers and returns the name associated with each set of offers, in the same order as the given list.All offers must belong to the same course and timePeriod. This method run multiples offerLists at once in order to improve efficiency in possibleNames method.
         E.g. (P)[professor's name].

        @param Offer[][] setOfOffers : List of list of offers
        @return string[] :
        @author
        """
        complements = []
        otherOffers = None
        #course and timePeriod must be equal in all the offers.
        course = setsOfOffers[0][0].course
        timePeriod = setsOfOffers[0][0].timePeriod
        
        for offers in setsOfOffers:
            #Check if offers is a list of offer
            for offer in offers:
                if not isinstance(offer, Offer):
                    OfferError("offers must be a list of Offer objects")
                    return None
            #Check if the professor and the practical is the same in this specific set of offers.
            professor = offers[0].professor
            practical = offers[0].practical
            for offer in offers[1:]:
                if not offer.timePeriod == timePeriod:
                    return None #timePeriod must be equal in all the offers.
                if not offer.course == course:
                    return None #course must be equal in all the offers.
                if not professor == offer.professor:
                    professor = None
                if practical != offer.practical:
                    practical = None
            complement = ''
            #Now checks if there are other offers in this course that have diferent professors and practical from this set this check is the same for all setsOfOffer
            if otherOffers == None:
                otherOffers = Offer.find(course = course, timePeriod = timePeriod)
            if offers == otherOffers: #if they are all the offers there are no complement
                complements.append('')
            else:
                otherProfessor = False
                otherPractical = False
                otherProfessorInPractical = False
                for otherOffer in otherOffers:
                    if professor != None:
                        if not otherOffer.professor == professor:
                            otherProfessor = True                    
                    if practical != None:
                        if otherOffer.practical != practical:
                            otherPractical = True
                    if professor != None and practical != None:
                        if otherOffer.practical == practical and otherOffer.professor != professor:
                            otherProfessorInPractical = True
                if not otherProfessorInPractical:
                    if otherPractical:
                        if practical == 1:
                            complement = complement + '(P)'
                        else:
                            complement = complement + '(T)'
                else:
                    #Now creats the name
                    if otherProfessor:
                        complement = complement + '[' + professor.name + ']'
                    if otherPractical:
                        if practical == 1:
                            complement = complement + '(P)'
                        else:
                            complement = complement + '(T)'
                complements.append(complement) 
        return complements

    @staticmethod
    def possibleNames(offers):
        """
         Returns a list of dicts in the form {complement:offersComplement,offers:Offer[]},
         where the offers is a subset of this courses offers, and the complement is the name of
         this subset. The list contain all possible names for that set of offers.
    
        @return [] :
        @author
        """
        if len(offers)==0:
            print 'offers list is empty'
            return None
        setsOfOffers = []
        #First fill a set with all offers
        setsOfOffers.append({'professor':None,'offers':[],'practical':None})
        for offer in offers:
            setsOfOffers[0]['offers'].append(offer)
        #Check if there are more than one offer per classNumber
        moreThanOneOffer = False
        classNumbers = []
        for offer in offers:
            if offer.classNumber in classNumbers:
                moreThanOneOffer = True
                break
            else:
                classNumbers.append(offer.classNumber)
        if moreThanOneOffer:
            #Now check if professors are different in one classNumber
            moreThanOneProfessor = False
            for classNumber in classNumbers:
                professors = []
                for offer in offers:
                    if offer.classNumber == classNumber:
                        if not offer.professor in professors:
                            if len(professors)>0:
                                moreThanOneProfessor = True
                                break
                            else:
                                professors.append(offer.professor)
            if moreThanOneProfessor:
                #If there are more than one professor per classNumber (even if it is in only one classNumber) there is a possibility to seperate per professor
                for offer in offers:
                    added = False
                    for setOfOffers in setsOfOffers:
                        if setOfOffers['professor'] == offer.professor.idProfessor:
                            added = True
                            setOfOffers['offers'].append(offer)
                    if not added:
                        setsOfOffers.append({'professor':offer.professor.idProfessor,'offers':list([offer]),'practical':None})
        
        for setOfOffers in setsOfOffers:
            practical = setOfOffers['offers'][0].practical
            offersPractical1 = []
            offersPractical2 = []
            moreThanOnePractical = False
            for offer in setOfOffers['offers']:
                if offer.practical != practical:
                    offersPractical2.append(offer)
                    moreThanOnePractical = True
                else:
                    offersPractical1.append(offer)
            if moreThanOnePractical:
                setsOfOffers.append({'professor':setOfOffers['professor'], 'offers':offersPractical1, 'practical':offersPractical1[0].practical})
                setsOfOffers.append({'professor':setOfOffers['professor'], 'offers':offersPractical2, 'practical':offersPractical2[0].practical})
        #Creates the list of names
        cleanSetOfOffers = [] #is a list with only the offers
        for setOfOffers in  setsOfOffers:
            cleanSetOfOffers.append(setOfOffers['offers'])
        names = Offer.offersName(cleanSetOfOffers)
        returns = []
        i = 0
        #Join the list of names with the offers
        for name in names:
            returns.append({'name':name, 'offers': setsOfOffers[i]['offers']}) #The order is the same
            i = i + 1
        return returns
 
    @staticmethod
    def pickById(idOffer):
        """
         Searches for an offer with the same id as the value of the parameter idOffer.
         
         Return: one object of the class Offer, if successful, or none, if unsuccessful.

        @param int idOffer : Associated database key of the offer you are searching for.

        @return Offer :
        @author
        """
        cursor = MySQLConnection()
        try:
            offerData = cursor.execute('SELECT idOffer, idTimePeriod, idCourse, classNumber, practical, idProfessor, numberOfRegistrations FROM aggr_offer WHERE idOffer = ' + str(idOffer))[0]
        except:
            return None
        offer = Offer(TimePeriod.pickById(offerData[1]), Course.pickById(offerData[2]), offerData[3], offerData[4], Professor.pickById(offerData[5]))
        offer.setNumberOfRegistrations(offerData[6])
        offer.idOffer = offerData[0]
        offer.fillSchedules()
        return offer

    @staticmethod
    def find(**kwargs):
        """
         Searches the database to find one or more objects that fit the description
         specified by the method's parameters. It is possible to perform two kinds of
         search when passing a string as a parameter: a search for the exact string
         (EQUAL operator) and a search for at least part of the string (LIKE operator).
         
         Returns:
         All the objects that are related to existing offers in the database, if there
         are not any parameters passed.
         
         A list of objects that match the specifications made by one (or more) of the
         following parameters:
         > idOffer
         > idCourse
         > course
         > professor
         > timePeriod
         > classNumber
         > practical
         > numberOfRegistration
         > schedule
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Offer.find(classNumber = 3, practical = True)

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  Offer[]:
        @author
        """
        cursor = MySQLConnection()
        #first prepare the kwargs for the MySQLConnection.find function
        complement = ''
        parameters = {}
        for key in kwargs:
            if key == 'course':
                parameters['aggr.idCourse'] = kwargs['course'].idCourse
            if key == 'professor':
                parameters['aggr.idProfessor'] = kwargs['professor'].idProfessor
            elif key == 'timePeriod':
                parameters['aggr.idTimePeriod'] = kwargs['timePeriod'].idTimePeriod
            elif key == 'schedule':
                complement = ' JOIN rel_offer_schedule ros ON ros.idOffer = aggr.idOffer'
                parameters['ros.idSchedule'] = kwargs[key].idSchedule
            else:
                parameters['aggr.' + key] = kwargs[key]
        offersData = cursor.find('SELECT aggr.idOffer, aggr.idTimePeriod, aggr.idCourse, aggr.classNumber, aggr.practical, aggr.idProfessor, aggr.numberOfRegistrations FROM aggr_offer aggr' + complement, parameters)
        offers = []
        for offerData in offersData:
            if 'timePeriod' in kwargs:
                timePeriod = kwargs['timePeriod']    
            else:
                timePeriod = TimePeriod.pickById(offerData[1])

            if 'course' in kwargs:
                course = kwargs['course']
            else:
                course = Course.pickById(offerData[2])

            if 'professor' in kwargs:
                professor = kwargs['professor']
            else:
                professor = Professor.pickById(offerData[5])

            offer = Offer(timePeriod, course, offerData[3], offerData[4], professor)
            offer.setNumberOfRegistrations(offerData[6])
            offer.idOffer = offerData[0]
            offer.fillSchedules()
            offers.append(offer)
        return offers

    def store(self):
        """
         Creates or alters the professor's data in the database.
         
         Return: true if successful or false if unsuccessful.

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        if self.numberOfRegistrations == None:
            mySQLNumberOfRegistrations = 'NULL'  #in MySQL is NULL
        else:
            mySQLNumberOfRegistrations = self.numberOfRegistrations
        if self.idOffer == None:
            offers = self.find(course = self.course, professor = self.professor, timePeriod = self.timePeriod, classNumber = self.classNumber, practical = self.practical, numberOfRegistrations = self.numberOfRegistrations) #Schedule does not define the offer 
            if len(offers) > 0:
                self.idOffer = offers[0].idOffer #Any offer that fit those paramaters is the same as this offer
                return
            else: 
                #Create this offer
                query = 'INSERT INTO aggr_offer (idTimePeriod, idCourse, classNumber, practical, idProfessor, numberOfRegistrations) VALUES(' + str(self.timePeriod.idTimePeriod) + ', ' + str(self.course.idCourse) + ', ' + str(self.classNumber) + ', ' + str(self.practical) + ', ' + str(self.professor.idProfessor) + ', ' + str(mySQLNumberOfRegistrations) + ')'
                cursor.execute(query)
                self.idOffer = self.find(course = self.course, professor = self.professor, timePeriod = self.timePeriod, classNumber = self.classNumber, practical = self.practical, numberOfRegistrations = self.numberOfRegistrations)[0].idOffer
        else:
            #Update offer
            query = 'UPDATE aggr_offer SET idTimePeriod = ' + str(self.timePeriod.idTimePeriod) + ', idCourse = ' + str(self.course.idCourse) + ', classNumber = ' + str(self.classNumber) + ', practical = ' + str(self.practical) + ', idProfessor = ' + str(self.professor.idProfessor) + ', numberOfRegistrations = ' + str(mySQLNumberOfRegistrations) + ' WHERE idOffer = ' + str(self.idOffer)
            cursor.execute(query)
        #Create the rel_offer_schedule
        idsScheduleOld = cursor.execute('SELECT idSchedule FROM rel_offer_schedule WHERE idOffer = ' + str(self.idOffer))
        #First delete all the old relations
        for idScheduleOld in idsScheduleOld:
            cursor.execute('DELETE FROM rel_offer_schedule WHERE idOffer = ' + str(self.idOffer) + ' AND idSchedule = ' + str(idScheduleOld[0]))
        #Now creates all the new relations
        for schedule in self.schedules:
            cursor.execute('INSERT INTO rel_offer_schedule (idOffer, idSchedule) VALUES (' + str(self.idOffer) + ', ' + str(schedule.idSchedule) + ')')
        
        return

    def delete(self):
        """
         Deletes the professor's data in the database.
         
         Return:  true if successful or false if unsuccessful.

        @return bool :
        @author
        """
        if self.idOffer != None:
            cursor = MySQLConnection()
            if self == Offer.pickById(self.idOffer):
                cursor.execute('DELETE FROM rel_offer_schedule WHERE idOffer = ' + str(self.idOffer))
                cursor.execute('DELETE FROM aggr_offer WHERE idOffer = ' + str(self.idOffer))
            else:
                raise OfferError("Can't delete non saved object.")
        else:
            raise OfferError('No idOffer defined.')


