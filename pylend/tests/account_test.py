import json
from .mock_connection import MockConnection
from unittest import TestCase
from pylend import Account, ExecutionFailureException


class AccountSetupTest(TestCase):
    connection = MockConnection(None)

    def init_raises_exception_with_bad_params_test(self):
        with self.assertRaises(ValueError):
            Account(None, None)
        with self.assertRaises(ValueError):
            Account(self.connection, None)
        with self.assertRaises(ValueError):
            Account(None, 1)

    def init_succeeds_with_good_params_test(self):
        Account(self.connection, 1)


class AccountSummaryTest(TestCase):
    __VALID_RESULT = """{
        "investorId": 1788402,
        "availableCash": 50.77,
        "accountTotal": 100.15,
        "accruedInterest": 0.26,
        "infundingBalance": 0,
        "receivedInterest": 0.16,
        "receivedPrincipal": 0.62,
        "receivedLateFees": 0,
        "outstandingPrincipal": 49.38,
        "totalNotes": 2,
        "totalPortfolios": 3
        } """

    def json_with_error_block_raises_exception_test(self):

        def callback(resource, api_version, query_params):
            return json.loads("""{"errors": "foo"}""")
        connection = MockConnection(callback)
        a = Account(connection, 1)

        with self.assertRaises(ExecutionFailureException):
            a.account_summary()

    def valid_result_raises_no_exceptions_test(self):
        def callback(resource, api_version, query_params):
            return json.loads(self.__VALID_RESULT)
        connection = MockConnection(callback)
        a = Account(connection, 1)

        a.account_summary()


class PendingTransfersTest(TestCase):
    __VALID_RESULT = """
        {"transfers": [{"transferDate": "2015-12-23T00:00:00.000-08:00", "status": "Scheduled", "sourceAccount": "samplebank", "cancellable": "true", "frequency": "One Time", "amount": 25.0, "operation": "ADD_FUNDS", "transferId": 1164216018, "endDate": null},
        {"transferDate": "2015-12-29T00:00:00.000-08:00", "status": "Scheduled", "sourceAccount": "somebank", "cancellable": "true", "frequency": "One Time", "amount": 25.0, "operation": "ADD_FUNDS", "transferId": 1164216019, "endDate": null},
        {
        "transferId": 34074842,
        "transferDate": "2015-01-23T00:00:00.000-0800",
        "amount": 100,
        "sourceAccount": "samplebank",
        "status": "Scheduled",
        "frequency": "Weekly",
        "endDate": null,
        "operation": "ADD_FUNDS",
        "cancellable": "true"},
        {
        "transferId": 34074843,
        "transferDate": "2015-01-23T00:00:00.000-0800",
        "amount": 100,
        "sourceAccount": "samplebank",
        "status": "Scheduled",
        "frequency": "1st and 16th of each Month",
        "endDate": "2015-01-29T00:00:00.000-0800",
        "operation": "ADD_FUNDS",
        "cancellable": "true"}]}
    """

    def valid_result_raises_no_exceptions_test(self):
        def callback(resource, api_version, query_params):
            return json.loads(self.__VALID_RESULT)
        connection = MockConnection(callback)
        a = Account(connection, 1)

        a.pending_transfers()

    def null_enddate_is_not_converted_test(self):
        def callback(resource, api_version, query_params):
            return json.loads(self.__VALID_RESULT)
        connection = MockConnection(callback)
        a = Account(connection, 1)

        result = a.pending_transfers()

        self.assertIsNone(result['transfers'][0]['endDate'])

    def frequencies_are_converted_test(self):
        def callback(resource, api_version, query_params):
            return json.loads(self.__VALID_RESULT)
        connection = MockConnection(callback)
        a = Account(connection, 1)

        result = a.pending_transfers()

        self.assertEquals("LOAD_ONCE", result['transfers'][0]['frequency'])
        self.assertEquals("LOAD_ON_DAY_1_AND_16",
                          result['transfers'][3]['frequency'])
