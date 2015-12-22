import json
import arrow
from .mock_connection import MockConnection
from unittest import TestCase
from pylend import Loans, ExecutionFailureException

VALID_RESPONSE = json.loads("""{
    "asOfDate":"2014-09-03T14:41:53.959-07:00",
    "loans": [
    {
        "id":111111,
        "memberId":222222,
        "loanAmount":1750.0,
        "fundedAmount":25.0,
        "term":36,
        "intRate":10.99,
        "expDefaultRate":3.5,
        "serviceFeeRate":0.85,
        "installment":57.29,
        "grade":"B",
        "subGrade":"B3",
        "empLength":0,
        "homeOwnership":"OWN",
        "annualInc":123432.0,
        "isIncV":"Requested",
        "acceptD":"2014-08-25T10:56:29.000-07:00",
        "expD":"2014-09-08T10:57:13.000-07:00",
        "listD":"2014-08-25T10:50:20.000-07:00",
        "creditPullD":"2014-08-25T10:56:18.000-07:00",
        "reviewStatusD":"2014-09-03T14:41:53.957-07:00",
        "reviewStatus":"NOT_APPROVED",
        "desc":"Loan description",
        "purpose":"debt_consolidation",
        "addrZip":"904xx",
        "addrState":"CA",
        "investorCount":"",
        "ilsExpD":"2014-08-25T11:00:00.000-07:00",
        "initialListStatus":"F",
        "empTitle":"",
        "accNowDelinq":"",
        "accOpenPast24Mths":23,
        "bcOpenToBuy":30000,
        "percentBcGt75":23.0,
        "bcUtil":23.0,
        "dti":0.0,
        "delinq2Yrs":1,
        "delinqAmnt":0.0,
        "earliestCrLine":"1984-09-15T00:00:00.000-07:00",
        "ficoRangeLow":750,
        "ficoRangeHigh":754,
        "inqLast6Mths":0,
        "mthsSinceLastDelinq":90,
        "mthsSinceLastRecord":0,
        "mthsSinceRecentInq":14,
        "mthsSinceRecentRevolDelinq":23,
        "mthsSinceRecentBc":23,
        "mortAcc":23,
        "openAcc":3,
        "pubRec":0,
        "totalBalExMort":13944,
        "revolBal":1.0,
        "revolUtil":0.0,
        "totalBcLimit":23,
        "totalAcc":4,
        "totalIlHighCreditLimit":12,
        "numRevAccts":28,
        "mthsSinceRecentBcDlq":52,
        "pubRecBankruptcies":0,
        "numAcctsEver120Ppd":12,
        "chargeoffWithin12Mths":0,
        "collections12MthsExMed":0,
        "taxLiens":0,
        "mthsSinceLastMajorDerog":12,
        "numSats":8,
        "numTlOpPast12m":0,
        "moSinRcntTl":12,
        "totHiCredLim":12,
        "totCurBal":12,
        "avgCurBal":12,
        "numBcTl":12,
        "numActvBcTl":12,
        "numBcSats":7,
        "pctTlNvrDlq":12,
        "numTl90gDpd24m":12,
        "numTl30dpd":12,
        "numTl120dpd2m":12,
        "numIlTl":12,
        "moSinOldIlAcct":12,
        "numActvRevTl":12,
        "moSinOldRevTlOp":12,
        "moSinRcntRevTlOp":11,
        "totalRevHiLim":12,
        "numRevTlBalGt0":12,
        "numOpRevTl":12,
        "totCollAmt":12,
        "applicationType":"JOINT",
        "annualIncJoint":223000.0,
        "dtiJoint":20.8,
        "isIncVJoint":"VERIFIED",
        "openAcc6m":null,
        "openIl6m":null,
        "openIl12m":null,
        "openIl24m":null,
        "mthsSinceRcntIl":null,
        "totalBalIl":null,
        "iLUtil":null,
        "openRv12m":null,
        "openRv24m":null,
        "maxBalBc":null,
        "allUtil":null,
        "totalCreditRv":23.0,
        "inqFi":null,
        "totalFiTl":null,
        "inqLast12m":185
    }]
}""")


class LoanTest(TestCase):
    def correctly_passes_showAll_param_test(self):
        showAllValue = False

        def callback(resource, api_version, query_params):
            self.assertIsNotNone(query_params)
            self.assertTrue('showAll' in query_params)
            self.assertEqual(showAllValue, query_params['showAll'])
            return VALID_RESPONSE
        connection = MockConnection(callback)
        l = Loans(connection)

        l.get_listed_loans()
        l.get_listed_loans(get_all_loans=False)
        showAllValue = True
        l.get_listed_loans(get_all_loans=True)

    def json_with_error_block_raises_exception_test(self):

        def callback(resource, api_version, query_params):
            return json.loads('{"errors": "foo"}')
        connection = MockConnection(callback)
        l = Loans(connection)

        with self.assertRaises(ExecutionFailureException):
            l.get_listed_loans()

    def verify_asOfDate_datetime_converted_test(self):

        def callback(resource, api_version, query_params):
            return VALID_RESPONSE

        connection = MockConnection(callback)
        l = Loans(connection)

        result = l.get_listed_loans()

        self.assertEqual(arrow.get("2014-09-03T14:41:53.959-07:00"),
                         result['asOfDate'])

    def verify_loan_datetimes_converted_test(self):

        def callback(resource, api_version, query_params):
            return VALID_RESPONSE

        dates = {}
        dates["acceptD"] = arrow.get("2014-08-25T10:56:29.000-07:00")
        dates["expD"] = arrow.get("2014-09-08T10:57:13.000-07:00")
        dates["listD"] = arrow.get("2014-08-25T10:50:20.000-07:00")
        dates["creditPullD"] = arrow.get("2014-08-25T10:56:18.000-07:00")
        dates["reviewStatusD"] = arrow.get("2014-09-03T14:41:53.957-07:00")
        dates["ilsExpD"] = arrow.get("2014-08-25T11:00:00.000-07:00")
        dates["earliestCrLine"] = arrow.get("1984-09-15T00:00:00.000-07:00")

        connection = MockConnection(callback)
        l = Loans(connection)

        loan = l.get_listed_loans()['loans'][0]

        for date in dates:
            self.assertEqual(dates[date], loan[date])
