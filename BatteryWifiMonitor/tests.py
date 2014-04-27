import os, subprocess
from types import ListType, DictType

from django.test import TestCase

import utils, api

class TestUtils(TestCase):
    def test_sudo_access(self):
        """
        If the current process is run with root privileges, any linux command
        should be able to run under sudo without a password.
        If it's with no root privileges, but the password for sudo is cached,
        remove the cache to test if has_sudo_access() would detect that a
        password is needed.
        """
        if os.geteuid() == 0:
            self.assertTrue(utils.has_sudo_access())
        else:
            # The -K (kill) sudo option removes the user's cached credentials
            subprocess.call(['sudo', '-K'], stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            self.assertFalse(utils.has_sudo_access())

    def test_command_output(self):
        """
        Run a linux command without sudo:
        seq - prints numeric sequences
        """
        input_command = ['seq', '5']
        seq_result = utils.command_output(input_command)
        seq_expected = "1\n2\n3\n4\n5\n"
        self.assertEqual(seq_result, seq_expected)

    def test_sudo_command_output(self):
        """
        Run a linux command with sudo (if it's available):
        seq - prints numeric sequences
        """
        input_command = ['echo', 'test']
        echo_result = utils.sudo_command_output(input_command)
        echo_expected = "test\n"
        self.assertEqual(echo_result, echo_expected)

    def test_networks_search(self):
        """
        Search for networks, the result should be a non-empty list
        """
        result = utils.networks_search()
        self.assertIsInstance(result, ListType)
        self.assertGreater(len(result), 0)

    def test_battery_status(self):
        """
        Get battery status. The result should be a dict with at least one item
        with 'status' key. This test should pass even if acpi tool couldn't
        find a battery.
        """
        result = utils.battery_status()
        self.assertIsInstance(result, DictType)
        self.assertTrue(result.has_key("status"))

    def test_battery_status_full_info(self):
        """
        Get battery status. The result dict should have the following keys:
        percent, time, time_info. The values are expected to match the correct
        regular expressions.
        This test should pass only if acpi tool could find a battery and parsed
        the information correctly.
        test_battery_status() is a more general test.
        """
        result = utils.battery_status()
        self.assertTrue(result.has_key("percent"))
        self.assertTrue(result.has_key("time"))
        self.assertTrue(result.has_key("time_info"))
        self.assertRegexpMatches(result['time'], "(\\d+)(:)(\\d+)(:)(\\d+)")
        self.assertRegexpMatches(result['percent'], "(\\d+)(%)")


class TestAPI(TestCase):
    def test_convert_networks_list_to_json(self):
        input_list = ['foo', 'bar', 'testnet']
        result = api.convert_networks_list_to_json(input_list)
        expected = '{"networks": ["foo", "bar", "testnet"]}'
        self.assertEqual(result, expected)

    def test_convert_battery_dict_to_json(self):
        input_dict = {'status': 'Discharging', 'percent': '49%',
            'time': '01:24:39', 'time_info': 'remaining'}
        result = api.convert_battery_dict_to_json(input_dict)
        expected = '{"status": "Discharging", "time_info": "remaining", '
        expected += '"percent": "49%", "time": "01:24:39"}'
        self.assertEqual(result, expected)