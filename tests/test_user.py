import unittest
import datetime
from vk.users import User


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.unixtime = {'time': 1506187303}

    def test_fail_if_not_convert_unixtime_to_datetime_UTC(self):
        last_seen_in_datetime = User._last_seen(self.unixtime)
        self.assertEqual(last_seen_in_datetime, datetime.datetime(2017, 9, 23, 17, 21, 43))
