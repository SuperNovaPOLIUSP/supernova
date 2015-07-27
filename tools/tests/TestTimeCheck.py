import unittest
import sys
sys.path.append('..')
sys.path.append('../..')
from timeCheck import checkTimeString, checkDateString, formatHour


class TimeCheckTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_time_check_correct_string(self):
        string = '12:00:00'
        self.assertTrue(checkTimeString(string))

    def test_time_check_correct_with_one_character_hour(self):
        string = '2:00:00'
        self.assertTrue(checkTimeString(string))

    def test_time_check_wrong_argument(self):
        string = 12
        self.assertFalse(checkTimeString(string))

    def test_time_check_incorrect_hour(self):
        string = '24:00:00'
        self.assertFalse(checkTimeString(string))

    def test_time_check_incorrect_minute(self):
        string = '12:60:00'
        self.assertFalse(checkTimeString(string))

    def test_time_check_incorrect_second(self):
        string = '12:00:60'
        self.assertFalse(checkTimeString(string))

    def test_time_check_incorrect_time(self):
        string = '143:00:121'
        self.assertFalse(checkTimeString(string))

    def test_date_check_correct_string(self):
        string = '2000-10-07'
        self.assertTrue(checkDateString(string))

    def test_date_check_wrong_argument(self):
        string = None
        self.assertFalse(checkDateString(string))

    def test_date_check_correct_size_wrong_characters(self):
        string = '2AAA-01-01'
        self.assertFalse(checkDateString(string))

    def test_date_check_incorrect_month(self):
        string = '2000-13-01'
        self.assertFalse(checkDateString(string))

    def test_date_check_incorrect_day(self):
        string = '2000-12-32'
        self.assertFalse(checkDateString(string))

    def test_date_check_incorrect_size(self):
        string = '20002-12-32'
        self.assertFalse(checkDateString(string))

    def test_format_hour(self):
        string = '1:23:01'
        self.assertEqual('01:23:01', formatHour(string))


if __name__ == '__main__':
    unittest.main()
