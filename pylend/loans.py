import logging
import arrow
import pylend
from .exceptions import ExecutionFailureException

LOAN_DATETIME_FIELDS = \
    [
        'ilsExpD',
        'earliestCrLine',
        'acceptD',
        'expD',
        'listD',
        'creditPullD',
        'reviewStatusD'
    ]


def create_order(loan, amount, portfolio_id=None):
    if loan is None:
        raise ValueError('loan must not be None')

    loanAmount = loan['loanAmount']
    fundedAmount = loan['fundedAmount']
    amount_to_fund = min((loanAmount-fundedAmount), amount)
    return LoanOrder(loan['id'], amount_to_fund, portfolio_id)


def _normalize_loan_format(json_payload):
        json_payload['asOfDate'] = arrow.get(json_payload['asOfDate'])
        json_payload['loans'] = [pylend._convert_datetimes(
            loan,
            LOAN_DATETIME_FIELDS) for loan in json_payload['loans']]
        return json_payload


class LoanOrder:
    def __init__(self, loan_id, amount, portfolio_id=None):
        self.loan_id = loan_id
        self.amount = amount
        self.portfolio_id = portfolio_id

    def __str__(self):
        fmt = "Loan Id {0}, with a requested funding amount of {1}, portfolio {2}"
        return fmt.format(self.loan_id, self.amount, self.portfolio_id)

    def __repr__(self):
        fmt = "Loan Id {0}, with a requested funding amount of {1}, portfolio {2}"
        return fmt.format(self.loan_id, self.amount, self.portfolio_id)

    def get_dict(self):
        result = {'loanId': self.loan_id, 'requestedAmount': self.amount}
        if self.portfolio_id is not None:
            result['portfolioId'] = self.portfolio_id
        return result


class Loans:
    __connection = None
    __logger = None

    def __init__(self, connection):
        if connection is None:
            raise ValueError('connection must be a non-None Connection object')
        self.__connection = connection
        self.__logger = logging.getLogger('pylend')

    def listed_loans(self, get_all_loans=False):
        url_path = 'loans/listing'
        query_params = {'showAll': get_all_loans}
        self.__logger.debug('Retrieving path {0} with query_params {1}'
                            .format(url_path, query_params))

        json_payload = self.__connection.get(url_path,
                                             query_params=query_params)
        self.__logger.debug("JSON Payload:\n{0}".format(json_payload))
        self._check_for_errors(json_payload)
        json_payload = _normalize_loan_format(json_payload)
        return json_payload

    def _check_for_errors(self, json_payload):
        if 'errors' in json_payload:
            self.__logger.error('Listed loan has errors: {0}'
                                .format(json_payload['errors']))
            raise ExecutionFailureException()
