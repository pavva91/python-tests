import unittest
from unittest.mock import Mock, patch

from requests.exceptions import Timeout

from holidays import get_holidays, is_weekday


class TestHolidays(unittest.TestCase):

    @patch("holidays.requests")
    def test_get_holidays_timeout(self, mock_requests):
        mock_requests.get.side_effect = Timeout
        with self.assertRaises(Timeout):
            get_holidays()
            mock_requests.get.assert_called_once()

    @patch("holidays.requests")
    def test_get_holidays_not_200(self, mock_requests):
        r = Mock()
        r.status_code = 400
        mock_requests.get.return_value = r
        actual = get_holidays()
        expected = None
        self.assertEqual(actual, expected)
        # self.assertNotEqual(actual, expected)
        mock_requests.get.assert_called_once()

    # @patch("holidays.requests")
    # @patch("holidays.datetime")
    # def test_get_holidays_200(self, mock_requests, mock_datetime):
    # def test_get_holidays_200(self, mock_requests):
    def test_get_holidays_200_is_weekday_should_return_true(self):
        with patch("holidays.requests") as stub_requests:
            with patch("holidays.datetime") as stub_datetime:
                response_mock = Mock()
                response_mock.status_code = 200

                today_mock = Mock()
                today_mock.weekday.return_value = 2

                stub_requests.get.return_value = response_mock

                stub_datetime.today.return_value = today_mock

                actual = get_holidays()
                # expected = None
                expected = True
                # expected = False
                self.assertEqual(actual, expected)
                # self.assertNotEqual(actual, expected)
                self.assertTrue(actual)

                stub_requests.get.assert_called_once()

    def test_get_holidays_200_is_not_weekday_should_return_false(self):
        with patch("holidays.requests") as stub_requests:
            with patch("holidays.datetime") as stub_datetime:
                response_mock = Mock()
                response_mock.status_code = 200

                today_mock = Mock()
                today_mock.weekday.return_value = 5

                stub_requests.get.return_value = response_mock

                stub_datetime.today.return_value = today_mock

                actual = get_holidays()
                expected = False

                self.assertEqual(actual, expected)
                self.assertFalse(actual)
                stub_requests.get.assert_called_once()
                stub_datetime.today.assert_called_once()

    def test_is_weekday_when_saturday_should_return_false(self):
        with patch("holidays.datetime") as stub_datetime:
            today_mock = Mock()
            today_mock.weekday.return_value = 5

            stub_datetime.today.return_value = today_mock

            actual = is_weekday()
            expected = False

            self.assertEqual(actual, expected)
            self.assertFalse(actual)
            stub_datetime.today.assert_called_once()


    @patch("holidays.datetime")
    def test_is_weekday_when_monday_should_return_false(self, stub_datetime):
        today_mock = Mock()
        today_mock.weekday.return_value = 0

        stub_datetime.today.return_value = today_mock

        actual = is_weekday()
        expected = True

        self.assertEqual(actual, expected)
        self.assertTrue(actual)
        stub_datetime.today.assert_called_once()


if __name__ == "__main__":
    unittest.main()
