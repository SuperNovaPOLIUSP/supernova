# coding: utf8

from django.db import connections


class MySQLConnection(object):
    """
    :version:
    :author:
    """
    """ ATTRIBUTES
    cursor  (public)
    """

    def __init__(self, database='supernova'):
        """
         When initialized the attribute cursor gets django's MySQL cursor.
        @return  :
        @author
        """
        # reads database connection settings from file
        self.cursor = connections[database].cursor()

    def execute(self, query):
        """
         Returns a list containing the rows fetched from the query.

        @param string query :
        @return  :
        @author
        """
        try:
            self.cursor.execute(query)
        except Exception, e:
            print 'ERROR: ' + str(e) + '\n' + 'Query: ' + query
        return self.cursor.fetchall()

    def find(self, queryStart, parameters, queryEnd=''):
        complements = []
        for key in parameters:
            if parameters[key] is None:
                # Even if there is no _ this will work
                complements.append(key.split('_')[0] + ' is null')
            elif isinstance(parameters[key], (int, long)):
                complements.append(key + ' = ' + str(parameters[key]))
            elif isinstance(parameters[key], (str, unicode)):
                if key.split('_')[1] == 'equal':
                    complements.append(key.split('_')[0] + ' = "' +
                                       parameters[key] + '"')
                elif key.split('_')[1] == 'like':
                    complements.append(key.split('_')[0] + ' LIKE "%%' +
                                       parameters[key] + '%%"')
            elif isinstance(parameters[key], list):
                #When using multiple terms they are OR
                tempComplements = []
                for parameter in parameters[key]:
                    if parameter is None:
                        # Even if there is no _ this will work
                        tempComplements.append(key.split('_')[0] + ' is null')
                    elif isinstance(parameter, (int, long)):
                        tempComplements.append(key + ' = ' + str(parameter))
                    elif isinstance(parameter, (str, unicode)):
                        if key.split('_')[1] == 'equal':
                            tempComplements.append(key.split('_')[0] + ' = "' +
                                                   parameter + '"')
                        elif key.split('_')[1] == 'like':
                            tempComplements.append(key.split('_')[0] +
                                                   ' LIKE "%%' + parameter +
                                                   '%%"')
                complements.append('(' + ' OR '.join(tempComplements) + ')')

        if len(complements) > 0:
            query = queryStart + ' WHERE '
            query = query + ' AND '.join(complements)
        else:
            query = queryStart
        query = query + queryEnd
        return self.execute(query)


class MySQLQueryError(Exception):
    """
     Exception reporting an error in the execution of a MySQL query.

    :version:
    :author:
    """
    pass
