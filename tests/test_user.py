import unittest
import datetime
from vk.users import User


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.unixtime = {'time': 1506187303}
        self.unixtime_is_none = None

    def test_fail_if_not_convert_unixtime_to_datetime_UTC(self):
        last_seen_in_datetime = User._last_seen(self.unixtime)
        self.assertEqual(last_seen_in_datetime, datetime.datetime(2017, 9, 23, 17, 21, 43))

    def test_return_None_when_unixtime_is_None(self):
        last_seen_in_datetime = User._last_seen(self.unixtime_is_none)
        self.assertIsNone(last_seen_in_datetime)

    def test_transform_sex(self):
        sex_items = {
            1: 'female',
            2: 'male'
        }

        sex = User._sex(1)
        self.assertEqual(sex, sex_items[1])

        sex = User._sex(2)
        self.assertEqual(sex, sex_items[2])

        sex = User._sex(3)
        self.assertIsNone(sex)

        sex = User._sex(None)
        self.assertIsNone(sex)
