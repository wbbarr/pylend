import logging
import pylend
from .exceptions import ExecutionFailureException

TRANSFER_DATETIME_FIELDS = \
    [
        'transferDate',
        'endDate'
    ]

TRANSFER_FREQUENCY_MAPPING = \
    {
        "One Time": "LOAD_ONCE",
        "Weekly": "LOAD_WEEKLY",
        "Every Other Week": "LOAD_BIWEEKLY",
        "1st and 16th of each Month": "LOAD_ON_DAY_1_AND_16",
        "Monthly": "LOAD_MONTHLY"
    }


def _normalize_received_transfers(json_payload):

    def normalize_transfer(transfer):
        transfer = pylend._convert_datetimes(
            transfer,
            TRANSFER_DATETIME_FIELDS)
        transfer['frequency'] = TRANSFER_FREQUENCY_MAPPING[
            transfer['frequency']]
        return transfer

    json_payload['transfers'] = [
        normalize_transfer(transfer) for transfer in json_payload['transfers']]
    return json_payload


class Account:
    __connection = None
    __account_id = None
    __logger = None
    __ACCOUNT_API_ROOT = 'accounts/{0}/{1}'

    def __init__(self, connection, account_id):
        if connection is None:
            raise ValueError('connection must be a non-None Connection object')
        if account_id is None:
            raise ValueError(
                'account_id must be a non-None integer account ID')

        self.__connection = connection
        self.__account_id = account_id
        self.__logger = logging.getLogger('pylend')

    def account_summary(self):
        return self._account_resource_get('summary')

    def available_cash(self):
        return self._account_resource_get('availablecash')

    def pending_transfers(self):
        json_payload = self._account_resource_get('funds/pending')
        return _normalize_received_transfers(json_payload)

    def _check_for_errors(self, json_payload):
        if 'errors' in json_payload:
            self.__logger.error('Listed loan has errors: {0}'
                                .format(json_payload['errors']))
            raise ExecutionFailureException()

    def _account_resource_get(self, resource):
        api_path = self.__ACCOUNT_API_ROOT.format(self.__account_id, resource)

        json_payload = self.__connection.get(api_path)
        self.__logger.debug('Response: {0}'.format(json_payload))

        self._check_for_errors(json_payload)
        return json_payload
