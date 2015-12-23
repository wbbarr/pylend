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


def _normalize_loan_format(json_payload):
        json_payload['asOfDate'] = arrow.get(json_payload['asOfDate'])
        json_payload['loans'] = [pylend._convert_datetimes(
            loan,
            LOAN_DATETIME_FIELDS) for loan in json_payload['loans']]
        return json_payload


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
