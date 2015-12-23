import arrow
from .connection import Connection
from .exceptions import (AuthorizationException,
                         ResourceNotFoundException,
                         ExecutionFailureException,
                         UnexpectedStatusCodeException)
from .loans import Loans
from .account import Account


def _convert_datetimes(convertable_object, convertable_fields):
    for field in convertable_fields:
        if field not in convertable_object:
            continue

        convertable_object[field] = arrow.get(
            convertable_object[field]
            ) if convertable_object[field] is not None else None
    return convertable_object
