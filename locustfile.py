import csv
from datetime import datetime
from subprocess import call

from bs4 import BeautifulSoup
import numpy as np

from locust import events
from locust import HttpLocust
from locust import TaskSet
from locust.log import console_logger

import config
from uztasks import tasks


# Hook into some events to collect statistics
def collect_stats(request_type, name, response_time, response_length):
    stats.append(
        [datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
        request_type,
        name,
        response_time])


def write_stats(filename=config.STATS_FILE):
    """
    Log some info and write collected response times to a CSV file.
    """
    response_times = [r[3] for r in stats]
    std_dev = 3 * np.std(response_times)
    mean = np.mean(response_times)
    outliers = [r for r in stats if abs(r[3] - mean) > std_dev]

    console_logger.info("\n uzERP Performance Summary:")
    console_logger.info('3 x Std. Dev: {}, with {} Outliers ({:.2f}%)'.format(
        std_dev,
        len(outliers),
        (float(len(outliers)) / len(response_times) * 100)))
    console_logger.info('Min request time: {}'.format(np.amin(response_times)))
    console_logger.info('Max request time: {}'.format(np.amax(response_times)))

    csv_file = open(filename, 'w')
    csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
    stats.insert(0, ['Time', 'Request Type', 'URL', 'Response Time'])
    for stat in stats:
        csv_writer.writerow(stat)
    csv_file.close()


def chart_stats():
    call('gnuplot -c utils/gnuplot/chart.plt -p', shell=True)


if config.COLLECT_STATS:
    stats = []
    events.request_success += collect_stats
    events.quitting += write_stats

if config.CHART_STATS:
    events.quitting += chart_stats


class UserBehaviour(TaskSet):
    """Primary TaskSet, all other tasks are nested within."""
    tasks = {tasks.SalesTasks: 1,
             tasks.PurchasingTasks: 1}

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


class WebsiteUser(HttpLocust):
    host = config.APP_HOST
    min_wait = config.MIN_WAIT
    max_wait = config.MAX_WAIT
    task_set = UserBehaviour
