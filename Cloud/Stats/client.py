import pika
import json
from stats import PerformanceStats


class ConnectionClient(object):

    """docstring for ConnectionClient"""

    def __init__(self):
        super(ConnectionClient, self).__init__()

    def send_data(self):
        data = {}
        credentials = pika.PlainCredentials('ovi', 'password')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='79.112.126.38', credentials=credentials))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs',
                                 type='fanout')

        perf = PerformanceStats()
        data = perf.getStats()

        message = json.dumps(data)
        channel.basic_publish(exchange='logs',
                              routing_key='',
                              body=message)
        print " Mesajul a fost trimis"
        connection.close()

client = ConnectionClient()
client.send_data()
