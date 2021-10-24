from requests.adapters import HTTPAdapter

DEFAULT_TIMEOUT = 5  # seconds


class TimeoutHTTPAdapter(HTTPAdapter):
    """Timeout HTTP Adapter

    Attributes:
        timeout: Timeout in seconds
    """

    def __init__(self, *args, **kwargs):
        """Initialize timeout

        Args:
            args (*): Arguments
            kwargs (**): Keyword arguments
        """
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        """Send request
        """
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)
