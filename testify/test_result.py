"""This module contains the TestResult class, each instance of which holds status information for a single test method."""
__testify = 1
import datetime

class TestResult(object):
    def __init__(self, test_method):
        super(TestResult, self).__init__(self)
        self.test_method = test_method
        self.test_method_name = test_method.__name__
        self.success = self.failure = self.error = self.skipped = self.incomplete = self.unexpected_success = self.expected_failure = None
        self.complete = False

    def start(self):
        self.start_time = datetime.datetime.now()

    def _complete(self):
        self.complete = True
        self.end_time = datetime.datetime.now()
        self.run_time = self.end_time - self.start_time

    def end_in_skipped(self):
        if not self.complete:
            self._complete()
            self.skipped = True

    def end_in_failure(self, exception_info):
        if not self.complete:
            self._complete()
            self.failure = True
            self.exception_info = exception_info
            if self.test_method.im_class.in_suite(self.test_method, 'expected-failure'):
                self.expected_failure = True

    def end_in_error(self, exception_info):
        if not self.complete:
            self._complete()
            self.error = True
            self.exception_info = exception_info
            if self.test_method.im_class.in_suite(self.test_method, 'expected-failure'):
                self.expected_failure = True

    def end_in_success(self):
        if not self.complete:
            self._complete()
            self.success = True
            if self.test_method.im_class.in_suite(self.test_method, 'expected-failure'):
                self.unexpected_success = True

    def end_in_incomplete(self, exception_info):
        if not self.complete:
            self._complete()
            self.incomplete = True
            self.exception_info = exception_info

    def normalized_run_time(self):
        return "%.2fs" % (self.run_time.seconds + (self.run_time.microseconds / 1000000.0))
