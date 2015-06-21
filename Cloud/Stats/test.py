import unittest
import stats
import client
import pika


class MyTest(unittest.TestCase):

    def size_list(self):
        p = stats.PerformanceStats()
        self.assertNotEqual(len(p.getStats()), 0)

    def connection_failed(self):
        c = client.ConnectionClient()
        c.send_data()
        with self.assertRaises(pika.exceptions.AMQPConnectionError):
            print 'Eroare de conexiune catre server!'


if __name__ == '__main__':
    unittest.main()
