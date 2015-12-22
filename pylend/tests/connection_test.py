from unittest import TestCase
from unittest.mock import patch
from pylend import LendingClub_Connection
from requests import Response
from pylend import (AuthorizationException,
                    ResourceNotFoundException,
                    ExecutionFailureException)


class MockResponse:

    def __init__(self, url, status_code, json_text):
        self.url = url
        self.status_code = status_code
        self.json_text = json_text

    def json(self):
        return self.json_text


class ConnectionTest(TestCase):
    @patch('requests.get')
    def bad_authentication_raises_AuthorizationException_test(
            self,
            requests_get_patch):
        response = Response()
        response.status_code = 401
        requests_get_patch.return_value = response
        c = LendingClub_Connection(api_key="testkey")

        with self.assertRaises(AuthorizationException):
            c.get("foo")

        response = Response()
        response.status_code = 403
        requests_get_patch.return_value = response
        c = LendingClub_Connection(api_key="testkey")

        with self.assertRaises(AuthorizationException):
            c.get("foo")

    @patch('requests.get')
    def server_error_raises_ExecutionFailureException_test(
            self,
            requests_get_patch):

        response = Response()
        response.status_code = 500
        requests_get_patch.return_value = response
        c = LendingClub_Connection(api_key="testkey")

        with self.assertRaises(ExecutionFailureException):
            c.get("foo")

    @patch('requests.get')
    def not_found_raises_ExecutionFailureException_test(
            self,
            requests_get_patch):

        response = Response()
        response.status_code = 404
        requests_get_patch.return_value = response
        c = LendingClub_Connection(api_key="testkey")

        with self.assertRaises(ResourceNotFoundException):
            c.get("foo")

    @patch('requests.get')
    def ok_raises_no_exception_test(
            self,
            requests_get_patch):

        response = MockResponse('foo', 200, '')
        requests_get_patch.return_value = response
        c = LendingClub_Connection(api_key="testkey")

        c.get("foo")

    @patch('requests.get')
    def bad_request_raises_no_exception_test(
            self,
            requests_get_patch):

        response = MockResponse('foo', 400, '')
        requests_get_patch.return_value = response
        c = LendingClub_Connection(api_key="testkey")

        c.get("foo")
