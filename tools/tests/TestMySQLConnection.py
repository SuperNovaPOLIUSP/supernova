import unittest
import sys
import os
sys.path.append('..')
sys.path.append('../..')
from MySQLConnection import MySQLConnection
from django.db import ProgrammingError


class MySQLConnectionTest(unittest.TestCase):

    def setUp(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'aeSupernova.settings'
        self.database = 'supernova'

    def test_create_connection(self):
        connection = MySQLConnection(database=self.database)
        self.assertIsNotNone(connection, 'Connection could not be created')

    def test_execute_query(self):
        connection = MySQLConnection(database=self.database)
        query = 'SHOW DATABASES'
        result = connection.execute(query)
        self.assertIn((u'supernova',), result,
                      'Supernova not in databases')

    def test_execute_query_exception(self):
        connection = MySQLConnection(database=self.database)
        query = 'SELECT'
        self.assertRaises(ProgrammingError, connection.execute, (query))

    def test_find_no_parameters(self):
        connection = MySQLConnection(database=self.database)
        query = 'SHOW DATABASES'
        result = connection.find(query, {})
        self.assertIn((u'supernova',), result)

if __name__ == '__main__':
    unittest.main()
