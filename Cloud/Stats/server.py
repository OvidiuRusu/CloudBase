import pika
import json
import sys
from os import environ
from django.conf import settings
sys.path.append('C:\\Users\\R\\Desktop\\Cloud\\Stats')
environ['DJANGO_SETTINGS_MODULE'] = 'performance.settings'

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'Performances',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
)

from django.db import models
from performance.models import *


class Server(object):

    """docstring for Server"""

    def __init__(self):
        super(Server, self).__init__()
        self.connection = None

    def start_server(self):

        credentials = pika.PlainCredentials('ovi', 'password')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))

        channel = self.connection.channel()

        channel.exchange_declare(exchange='logs',
                                 type='fanout')

        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='logs',
                           queue=queue_name)

        print ' [*] Waiting for logs. To exit press CTRL+C'

        channel.basic_consume(self.callback,
                              queue=queue_name,
                              no_ack=True)

        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print "Serverul a primit datele"
        results = json.loads(body)
        for key in results.keys():
            aux = results.get(key)
            data = aux.values()
            if key != 'total' and not PcInfo.objects.filter(pc_name=data[3], ip=data[2]).exists():
                pc = PcInfo(pc_name=data[3], ip=data[2])
                pc.save()
            if key != 'total':
                index = PcInfo.objects.get(pc_name=data[3], ip=data[2])
            if key == 'total':
                cpu = data[0]
                memory = data[1]
                disk = data[2]
                p = Performance(pc=index, cpu_percent=cpu, memory_percent=memory, disk_percent=disk)
                p.save()
            else:
                s = Statistic(pc=index, process_name=data[1], cpu=data[7], memory=data[6], reads=data[0], writes=data[4], threads=data[5])
                s.save()
                print 'PC:', data[3]
                print 'IP:', data[2]
                print 'Process name:', data[1]
                print 'Cpu: %0.1f%% ' % data[7]
                print 'Memory: %0.1f%%' % data[6]
                print 'Reads B/s:', data[0]
                print 'Writes B/s:', data[4]
                print 'Threads:', data[5]
        print "CPU percent: %d%%" % cpu
        print "Memory percent: %d%%" % memory
        print "Disk percent: %d%%" % disk


server = Server()
server.start_server()
