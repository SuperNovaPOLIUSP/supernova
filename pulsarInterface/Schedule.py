from tools.MySQLConnection import MySQLConnection
from tools.timeCheck import checkTimeString, formatHour


class ScheduleError(Exception):
    """
     Exception reporting an error in the execution of a Offer method.

    :version:
    :author:
    """
    pass
    
class Schedule(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associate database key.

    idSchedule  (public)

     The day of the week as it is written in the database's minitableDayOfTheWeek.

    dayOfTheWeek  (public)

     The starting time of the class (e.g. "18:00:00").

    start  (public)

     The ending time of the class (e.g. "03:14:15").

    end  (public)

     Specifies how often the lecture is held at this time (e.g. "weekly", "monthly",
     etc).

    frequency  (public)

    """

    def __init__(self, dayOfTheWeek, end, frequency, start):
        """
         Constructor method.

        @param string dayOfTheWeek : The day of the week as it is written in the database's minitableDayOfTheWeek.
        @param string end : The ending time of the class (e.g. "03:14:15").
        @param string frequency : Specifies how often the lecture is held at this time (e.g. "weekly", "monthly", etc).
        @param string start : The starting time of the class (e.g. "18:00:00").
        @return  :
        @author
        """
        if not isinstance(dayOfTheWeek,(str, unicode)):
            raise ScheduleError('dayOfTheWeek must be unicode')
        #check if dayOfTheWeek is in the database
        cursor = MySQLConnection()              
        if not cursor.execute('SELECT idDayOfTheWeek FROM minitableDayOfTheWeek WHERE dayOfTheWeek = "' + dayOfTheWeek + '" '):   
            raise ScheduleError('dayOfTheWeek must be in the database')
        if not isinstance(end, (str,unicode)):
            raise ScheduleError('end must be a string or unicode')
        if not isinstance(frequency, (str,unicode)):
            raise ScheduleError('frequency must be unicode')
        if not isinstance(start, (str, unicode)):
            raise ScheduleError('start must be a string or unicode')
        #check if the parameter 'end' and start are in the format HH:MM:SS
        if not checkTimeString(end):
            raise ScheduleError("Wrong time format for parameter end. Format must be HH:MM:SS")
        if not checkTimeString(start):
            raise ScheduleError("Wrong time format for parameter start. Format must be HH:MM:SS")        
        self.dayOfTheWeek = dayOfTheWeek
        self.end = formatHour(str(end))
        self.frequency = frequency
        self.start = formatHour(str(start))
        self.idSchedule = None

    def __str__(self):
        """
         Returns the schedule written in a pattern.

        @return string :
        @author
        """
        # E.g "segunda 13:00 - 16:40"
        return self.dayOfTheWeek.encode('utf8') + ' '+ self.start[:5] + ' - ' + self.end[:5] 
    
    def __eq__(self, other):
        if not isinstance(other, Schedule):
            return False
        return self.__dict__ == other.__dict__
        
    def __ne__(self,other):
        return not self.__eq__(other)
 
    @staticmethod 
    def pickById(idSchedule):
        """
         Returns a Schedule object once given its idSchedule.

        @param int idSchedule : Associated database key.
        @return Schedule :
        @author
        """
        cursor = MySQLConnection()
        query = '''SELECT mini.dayOfTheWeek, sch.end, sch.frequency, sch.start  FROM schedule AS sch
        JOIN minitableDayOfTheWeek AS mini ON mini.idDayofTheWeek = sch.idDayOfTheWeek
        WHERE sch.idSchedule = ''' + str(idSchedule)
        
        try:
            values = cursor.execute(query)[0]
        except:
            return None
        end = str(values[1])
        start = str(values[3])
        end = formatHour(end)
        start = formatHour(start)
        schedule = Schedule(values[0], end, values[2], start)
        schedule.idSchedule = idSchedule
        return schedule

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
         > idSchedule
         > dayOfTheWeek_equal or dayOfTheWeek_like
         > start_equal or start_like
         > end_equal or end_like
         > frequency_equal or frequency_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Schedule.find(dayOfTheWeek_equal = "monday", start_like = "09:")

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        query = """SELECT mini.dayOfTheWeek, sch.end, sch.frequency, sch.start, sch.idSchedule FROM schedule AS sch
        JOIN minitableDayOfTheWeek AS mini ON mini.idDayOfTheWeek = sch.idDayOfTheWeek
        """
        schedulesData = cursor.find(query, kwargs)
        schedules = []
        for scheduleData in schedulesData:
            schedule = Schedule(scheduleData[0], str(scheduleData[1]), scheduleData[2], str(scheduleData[3]))
            schedule.idSchedule = scheduleData[4]
            schedules.append(schedule)
        return schedules
        

    def store(self):
        """
         Creates or changes the schedule's data in the database.
         
         Return: True if successful or False otherwise.

        @return  :
        @author
        """
        cursor = MySQLConnection()
        if self.idSchedule == None:
            #Search for idSchedule
            possibleIds = self.find(dayOfTheWeek_equal = self.dayOfTheWeek, end_equal = self.end, frequency_equal = self.frequency, start_equal = self.start)
            if not possibleIds :
                #If there is no idSchedule, then create row
                idDayOfTheWeek = cursor.execute("SELECT idDayOfTheWeek FROM minitableDayOfTheWeek WHERE dayOfTheWeek = '" + self.dayOfTheWeek + "'")[0][0]
                query = 'INSERT INTO schedule (idDayOfTheWeek, end, frequency, start) VALUES(' + str(idDayOfTheWeek) + ', "' + self.end + '", "' + self.frequency + '", "' + self.start + '")'
                cursor.execute(query)
                self.idSchedule = self.find(dayOfTheWeek_equal = self.dayOfTheWeek, end_equal = self.end, frequency_equal = self.frequency, start_equal = self.start)[0].idSchedule                
                return 
            else:
                self.idSchedule = possibleIds[0].idSchedule   #Since all results are the same schedule pick the first one.
                return
        else:
            #If there is an idFaculty try to update row
            query = 'UPDATE schedule SET idDayOfTheWeek = ' + str(idDayOfTheWeek) + ', end = "' + self.end + '", frequency = "'
            query += self.frequency + '" , start = "' + self.start + '" WHERE idSchedule = ' + str(self.idSchedule)
            cursor.execute(query)
            return 

    def delete(self):
        """
         Deletes the schedule's data in the database.
         
         Return: True if successful or False otherwise.

        @return  :
        @author
        """
        if self.idSchedule != None:
            cursor = MySQLConnection()
            idSchedule = self.idSchedule
            if self == Schedule.pickById(idSchedule):
                cursor.execute('DELETE FROM rel_offer_schedule WHERE idSchedule = ' + str(idSchedule))
                cursor.execute('DELETE FROM schedule WHERE idSchedule = ' + str(idSchedule))
            else:
                raise ScheduleError("Can't delete non saved object.")
        else:
            raise ScheduleError('No idSchedule defined.')

