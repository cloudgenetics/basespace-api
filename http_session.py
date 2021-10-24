import requests
from requests.packages.urllib3.util import Retry

from timeout_adapter import TimeoutHTTPAdapter


class HTTPSession():
    """HTTP session with retries and base URL

    Methods
    -------
    get_json(url)
        Returns a JSON object from a GET call on url

    download_file(url, file)
        Write response of GET to a file
    """

    def __init__(self, baseurl='', timeout=2.5, retry=3) -> None:
        """
        Parameters
        ----------
        baseurl : str
            BaseURL - can be left empty
        retry : int
            Number of retries for failed REST attempts
        timeout : float
            Time in seconds before timeout
        """
        # Create session
        self.session = requests.Session()
        assert_status_hook = lambda response, \
            *args, **kwargs: response.raise_for_status()
        self.session.hooks["response"] = [assert_status_hook]
        # Set default timeout and retries
        retries = Retry(total=retry, backoff_factor=1,
                        status_forcelist=[429, 500, 502, 503, 504])
        adapter = TimeoutHTTPAdapter(timeout=timeout, max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        # Set BaseURL
        self.baseurl = baseurl

    def get_json(self, url):
        """Return a JSON object from GET
        Parameters
        ----------
        url : str
            url for GET request
        """
        r = self.session.get(self.baseurl + str(url))
        return r.json()

    def download_file(self, url, file):
        """Download file from GET
        Parameters
        ----------
        url : str
            url for GET request
        file : str
            Output file path
        """
        r = self.session.get(self.baseurl + str(url))
        with open(file, 'wb') as f:
            f.write(r.content)
