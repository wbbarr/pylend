import arrow
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


class OwnedNotesTest(TestCase):
    __VALID_RESULT = """
{
    "myNotes" : [
    {
        "loanId":11111,
        "noteId":22222,
        "orderId":33333,
        "interestRate":13.57,
        "loanLength":36,
        "loanStatus":"Late (31-120 days)",
        "grade":"C",
        "loanAmount":10800,
        "noteAmount":25,
        "paymentsReceived":5.88,
        "issueDate":"2009-11-12T06:34:02.000-08:00",
        "orderDate":"2009-11-05T09:33:50.000-08:00",
        "loanStatusDate":"2013-05-20T13:13:53.000-07:00"
    },
    {
        "loanId":44444,
        "noteId":55555,
        "orderId":66666,
        "interestRate":14.26,
        "loanLength":36,
        "loanStatus":"Late (31-120 days)",
        "grade":"C",
        "loanAmount":3000,
        "noteAmount":25,
        "paymentsReceived":7.65,
        "issueDate":"2009-09-18T01:04:34.000-07:00",
        "orderDate":"2009-09-15T11:28:12.000-07:00",
        "loanStatusDate":"2013-05-23T17:27:51.000-07:00"
    }
    ]
}
    """

    def valid_result_raises_no_exceptions_test(self):
        def callback(resource, api_version, query_params):
            return json.loads(self.__VALID_RESULT)
        connection = MockConnection(callback)
        a = Account(connection, 1)

        a.owned_notes()

    def dates_are_converted_test(self):
        def callback(resource, api_version, query_params):
            return json.loads(self.__VALID_RESULT)
        connection = MockConnection(callback)
        a = Account(connection, 1)

        result = a.owned_notes()
        self.assertEquals(
            arrow.get("2009-11-12T06:34:02.000-08:00"),
            result['myNotes'][0]['issueDate'])

    def detailed_info_requests_data_from_detailednotes_test(self):
        def callback(resource, api_version, query_params):
            self.assertEquals('accounts/1/detailednotes', resource)
            return json.loads(self.__VALID_RESULT)
        connection = MockConnection(callback)
        a = Account(connection, 1)

        a.owned_notes(detailed_info=True)


class PortfoliosTest(TestCase):
    __VALID_RESULT = """
{
    "myPortfolios":[
    {
        "portfolioId":11111,
        "portfolioName":"Portfolio1",
        "portfolioDescription":"Sample Portfolio Description"},
    {
        "portfolioId":22222,
        "portfolioName":"Portfolio2",
        "portfolioDescription":null
    }]
}
    """

    def valid_result_raises_no_exceptions_test(self):
        def callback(resource, api_version, query_params):
            return json.loads(self.__VALID_RESULT)
        connection = MockConnection(callback)
        a = Account(connection, 1)

        a.portfolios()
