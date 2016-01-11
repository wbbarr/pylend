class MockConnection:
    def __init__(self, get_callback=None, post_callback=None):
        self.get_callback = get_callback

    def get(self, resource, api_version='v1', query_params=None):
        method = self.get_callback
        return method(resource, api_version, query_params)

    def post(self, resource, body, api_version='v1', query_params=None):
        method = self.post_callback
        return method(resource, body, api_version, query_params)
