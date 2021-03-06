class Error(Exception):
    """ Generic Error exception. This can be used
        when an error is not passed from the API.
    """

class ApiError(Error):
    """ ApiError should be used when handling errors
        from the API.
    """
    def __init__(self, api_response):
        """
        """
        msg = "{msg}: {type}".format(**api_response.json()['meta'])
        super().__init__(msg)
