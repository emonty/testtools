# Copyright (c) 2009 Jonathan M. Lange. See LICENSE for details.

"""Test ConcurrentTestSuite and related things."""

__metaclass__ = type

import unittest

from testtools import (
    ConcurrentTestSuite,
    iterate_tests,
    TestCase,
    )
from testtools.matchers import (
    Equals,
    MatchesAny,
    )
from testtools.tests.helpers import LoggingResult


class TestConcurrentTestSuiteRun(TestCase):

    def test_trivial(self):
        log = []
        result = LoggingResult(log)
        class Sample(TestCase):

            def __hash__(self):
                return id(self)

            def test_method(self):
                pass
        test1 = Sample('test_method')
        test2 = Sample('test_method')
        original_suite = unittest.TestSuite([test1, test2])
        suite = ConcurrentTestSuite(original_suite, self.split_suite)
        suite.run(result)
        log1first = [('startTest', test1), ('addSuccess', test1),
            ('stopTest', test1), ('startTest', test2), ('addSuccess', test2),
            ('stopTest', test2)]
        log2first = [('startTest', test2), ('addSuccess', test2),
            ('stopTest', test2), ('startTest', test1), ('addSuccess', test1),
            ('stopTest', test1)]
        self.assertThat(log, MatchesAny(Equals(log1first), Equals(log2first)))

    def split_suite(self, suite):
        tests = list(iterate_tests(suite))
        return tests[0], tests[1]


def test_suite():
    from unittest import TestLoader
    return TestLoader().loadTestsFromName(__name__)