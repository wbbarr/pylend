import time
import requests
import logging
from datetime import datetime, timedelta
from .exceptions import (AuthorizationException,
                         ResourceNotFoundException,
                         ExecutionFailureException,
                         UnexpectedStatusCodeException)


class LendingClub_Connection:
    __api_key = None
    __last_request = None
    __logger = None
    __request_delay = None
    __JSON_CONTENT_TYPE = 'application/json'
    __PYLEND_USER_AGENT = 'pylend v0.0.1'
    __LENDINGCLUB_BASE_URI = 'https://api.lendingclub.com/api/investor/{0}/{1}'

    def __init__(self, api_key, request_delay=timedelta(seconds=1.0)):
        if api_key is None:
            raise ValueError('api_key must be provided and not None.')
        self.__api_key = api_key
        self.__last_request = datetime.min
        self.__request_delay = request_delay
        self.__logger = logging.getLogger('pylend')

    def get(self, resource, api_version='v1', query_params=None):
        headers = {
            'Accept': self.__JSON_CONTENT_TYPE,
            'Authorization': self.__api_key,
            'User-Agent': self.__PYLEND_USER_AGENT
        }

        request_uri = self.__LENDINGCLUB_BASE_URI.format(api_version, resource)
        self._delay_if_necessary()
        response = requests.get(request_uri,
                                headers=headers,
                                params=query_params)
        self.__last_request = datetime.now()
        self.__logger.debug('URI for get request: {0}'.format(response.url))
        self._check_for_errors(response)
        return response.json()

    def _delay_if_necessary(self):
        delta = datetime.now() - self.__last_request

        if delta < self.__request_delay:
            self.__logger.debug('Sleeping for {0} before sending request'
                                .format(delta.total_seconds()))
            time.sleep(delta.total_seconds())

    def _check_for_errors(self, response):
        self.__logger.info('Status code: {0}'.format(response.status_code))

        if response.status_code == 200:
            return
        elif response.status_code == 400:
            # We will let the caller handle this, as it is often call-specific
            return
        elif response.status_code == 401 or response.status_code == 403:
            self.__logger.error('Encountered Authorization error code {0}: {1}'
                                .format(response.status_code, response.text))
            raise AuthorizationException()
        elif response.status_code == 404:
            self.__logger.error('Resource {0} not found.'.format(response.url))
            raise ResourceNotFoundException()
        elif response.status_code == 500:
            self.__logger.error('Request failed with 500 error: {0}'
                                .format(response.text))
            raise ExecutionFailureException()
        else:
            self.__logger.error(
                'Unexpected status code returned: {0}. Response text:{1}'
                .format(response.status_code, response.text))
            raise UnexpectedStatusCodeException()
