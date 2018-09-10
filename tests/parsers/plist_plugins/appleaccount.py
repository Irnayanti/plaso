#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the Apple account plist plugin."""

from __future__ import unicode_literals

import unittest

from plaso.formatters import plist  # pylint: disable=unused-import
from plaso.parsers.plist_plugins import appleaccount

from tests import test_lib as shared_test_lib
from tests.parsers.plist_plugins import test_lib


class AppleAccountPluginTest(test_lib.PlistPluginTestCase):
  """Tests for the Apple account plist plugin."""

  @shared_test_lib.skipUnlessHasTestFile([
      'com.apple.coreservices.appleidauthenticationinfo.'
      'ABC0ABC1-ABC0-ABC0-ABC0-ABC0ABC1ABC2.plist'])
  def testProcess(self):
    """Tests the Process function."""
    plist_file = (
        'com.apple.coreservices.appleidauthenticationinfo.'
        'ABC0ABC1-ABC0-ABC0-ABC0-ABC0ABC1ABC2.plist')
    plist_name = plist_file

    plugin = appleaccount.AppleAccountPlugin()
    storage_writer = self._ParsePlistFileWithPlugin(
        plugin, [plist_name], plist_name)

    self.assertEqual(storage_writer.number_of_errors, 0)
    self.assertEqual(storage_writer.number_of_events, 3)

    # The order in which PlistParser generates events is nondeterministic
    # hence we sort the events.
    events = list(storage_writer.GetSortedEvents())

    expected_timestamps = [1372106802000000, 1387980032000000, 1387980032000000]
    timestamps = sorted([event.timestamp for event in events])

    self.assertEqual(timestamps, expected_timestamps)

    event = events[0]
    self.assertEqual(event.root, '/Accounts')
    self.assertEqual(event.key, 'email@domain.com')

    expected_description = (
        'Configured Apple account email@domain.com (Joaquin Moreno Garijo)')
    self.assertEqual(event.desc, expected_description)

    expected_message = '/Accounts/email@domain.com {0:s}'.format(
        expected_description)
    expected_short_message = '{0:s}...'.format(expected_message[:77])
    self._TestGetMessageStrings(event, expected_message, expected_short_message)

    event = events[1]
    expected_description = (
        'Connected Apple account '
        'email@domain.com (Joaquin Moreno Garijo)')
    self.assertEqual(event.desc, expected_description)

    event = events[2]
    expected_description = (
        'Last validation Apple account '
        'email@domain.com (Joaquin Moreno Garijo)')
    self.assertEqual(event.desc, expected_description)


if __name__ == '__main__':
  unittest.main()
