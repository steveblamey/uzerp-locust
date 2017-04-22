from bs4 import BeautifulSoup

from locust import TaskSet

import config


class UzTaskSet(TaskSet):
    def request_resources(self, response=None):
        """
        Parse HTML response content to extract resource urls (javascript
        and css) and request those resources from the host.

        Args:
            response (object): locust request response
        """
        soup = BeautifulSoup(response.content, 'html.parser')
        resource_urls = set()

        # Find resource urls with a src attribute
        for res in soup.find_all(src=True):
            url = res['src']
            if url[0] != '/':
                url = '/' + url
            resource_urls.add(url)

        # Find stylesheet urls
        for rel in soup.find_all(rel='stylesheet'):
            url = rel['href']
            resource_urls.add(url)

        # Find module js url
        js_url_start = response.content.find('loadScript("') + 12
        js_url_end = response.content.find('"', js_url_start)
        module_js = '/' + response.content[js_url_start:js_url_end]
        module_js.replace(self.locust.host, '')
        resource_urls.add(module_js)

        # Request the page resources
        for url in resource_urls:
            self.client.get(url)
