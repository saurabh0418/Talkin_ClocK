from unittest import TestCase
from talking_clock import TalkingClock

class Mytestingcl(TestCase):
    def setUp(self):
        self.Talker = TalkingClock()

    def tearDown(self):
        del self.Talker

    def test_all_zeros(self):
        self.assertEqual(self.Talker.time_string_to_words("00:00"), "It's twelve am")

    def test_single_digit_minutes(self):
        test_cases = [
                ("1", "one"), ("2", "two"), ("3", "three"), ("4", "four"), ("5", "five"),
                    ("6", "six"), ("7", "seven"), ("8", "eight"), ("9", "nine"),
            ]
        for i in test_cases:
            result = self.Talker.time_string_to_words("00:0{}".format(i[0]))
            expected_result = "It's twelve oh {} am".format(i[1])
            self.assertEqual(result, expected_result)

    def test_tens_plus_single_digits(self):
        test_cases = [
                ("1", "one"), ("2", "two"), ("3", "three"), ("4", "four"), ("5", "five"),
                ("6", "six"), ("7", "seven"), ("8", "eight"), ("9", "nine"),
            ]
        for i in test_cases:
            result = self.Talker.time_string_to_words("00:2{}".format(i[0]))
            expected_result = "It's twelve twenty {} am".format(i[1])
            self.assertEqual(result, expected_result)

    def test_all_minute_tens(self):
        test_cases = [("20", "twenty"), ("30", "thirty"), ("40", "fourty"), ("50", "fifty")]
        for i in test_cases:
            result = self.Talker.time_string_to_words("00:{}".format(i[0]))
            expected_result = "It's twelve {} am".format(i[1])
            self.assertEqual(result, expected_result)

    def test_over_sixty_minutes(self):
        self.assertEqual(self.Talker.time_string_to_words("00:65"), "It's twelve oh five am")

    def test_over_twenty_four_hours(self):
        self.assertEqual(self.Talker.time_string_to_words("26:00"), "It's two am")

    def test_negative_hours(self):
        self.assertEqual(self.Talker.time_string_to_words("-2:00"), "It's ten pm")

    def test_negative_minutes(self):
        self.assertEqual(self.Talker.time_string_to_words("00:-10"), "It's twelve fifty am")

    def test_not_a_time(self):
        self.assertRaisesRegexp(ValueError, "Time not in format ",
                                self.Talker.time_string_to_words, "blaaa, cheese 23984742")

    def test_numbers_with_no_colon(self):
        self.assertRaisesRegexp(ValueError, "Time not in format",
                                self.Talker.time_string_to_words, "0259")

    def test_time_with_seconds(self):
        self.assertRaisesRegexp(ValueError, "Time not in format",
                                self.Talker.time_string_to_words, "02:59:02")

    def test_reddit_sample_data(self):
        test_cases = [
                ("00:00", "It's twelve am"),
                    ("01:30", "It's one thirty am"),
                    ("12:05", "It's twelve oh five pm"),
                    ("14:01", "It's two oh one pm"),
                    ("20:29", "It's eight twenty nine pm"),
                    ("21:00", "It's nine pm"),
            ]
        for i in test_cases:
            self.assertEqual(self.Talker.time_string_to_words(i[0]), i[1])

