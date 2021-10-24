import requests
from requests.packages.urllib3.util import Retry

from timeout_adapter import TimeoutHTTPAdapter


class HTTPSession():
    def __init__(self, baseurl, retry=3) -> None:
        # Create session
        self.session = requests.Session()
        assert_status_hook = lambda response, * \
            args, **kwargs: response.raise_for_status()
        self.session.hooks["response"] = [assert_status_hook]
        # Set default timeout and retries
        retries = Retry(total=retry, backoff_factor=1,
                        status_forcelist=[429, 500, 502, 503, 504])
        adapter = TimeoutHTTPAdapter(timeout=2.5, max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        # Set BaseURL
        self.baseurl = baseurl

    def get_json(self, url):
        r = self.session.get(self.baseurl + str(url))
        return r.json()
