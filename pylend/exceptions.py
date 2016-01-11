
class AuthorizationException(Exception):
    pass


class ResourceNotFoundException(Exception):
    pass


class ExecutionFailureException(Exception):

    def __init__(self, errors=None):
        self.errors = errors


class UnexpectedStatusCodeException(Exception):
    pass
