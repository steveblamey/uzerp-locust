import csv

from bs4 import BeautifulSoup

from locust import events
from locust import HttpLocust
from locust import TaskSet
from locust import task

import config


# Hook into some events to collect statistics
def collect_stats(request_type, name, response_time, response_length):
    stats.append([request_type, name, response_time])


def write_stats(filename=config.STATS_FILE):
    """Write collected response times to a CSV file."""
    csv_file = open(filename, 'w')
    csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
    stats.insert(0, ['Request Type', 'URL', 'Response Time'])
    for stat in stats:
        csv_writer.writerow(stat)
    csv_file.close()


if config.COLLECT_STATS:
    stats = []
    events.request_success += collect_stats
    events.quitting += write_stats


class WebsiteTasks(TaskSet):
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
        module_js.replace(self.parent.host, '')
        resource_urls.add(module_js)

        # Request the page resources
        for url in resource_urls:
            self.client.get(url)

    def on_start(self):
        """Log-in to the application."""
        response = self.client.get('/')
        soup = BeautifulSoup(response.content, 'html.parser')
        csrf_hidden = soup.find('input', id='csrf_token_id')

        self.client.post('/?action=login', {
            'username': config.APP_USERNAME,
            'password': config.APP_PASSWORD,
            'csrf_token': csrf_hidden['value'],
            'rememberUser': 'true',
        })

    @task
    def list_sales_orders(self):
        """Request the sales order listing."""
        response = self.client.get(
            '/?pid=413&controller=sorders&module=sales_order')
        self.request_resources(response)


class WebsiteUser(HttpLocust):
    host = config.APP_HOST
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000
