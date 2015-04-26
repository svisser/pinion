import unittest

import pinion
from pinion import parse_hosts, create_packet


class BaseTestCase(unittest.TestCase):

    def test_parse_hosts(self):
        expected = [("127.0.0.1", 4730)]
        self.assertEqual(parse_hosts([("127.0.0.1", "4730")]), expected)
        self.assertEqual(parse_hosts(["127.0.0.1"]), expected)
        self.assertEqual(parse_hosts(["127.0.0.1:4730"]), expected)
        self.assertEqual(parse_hosts([{'host': "127.0.0.1"}]), expected)
        self.assertEqual(parse_hosts([{'host': "127.0.0.1", 'port': "4730"}]), expected)

class GearmanClientTestCase(unittest.TestCase):

    def test_submit_job_job_data_does_not_contain_null(self):
        client = pinion.GearmanClient(["127.0.0.1"])
        with self.assertRaises(pinion.GearmanException):
            client.submit_job('task', b'\x00containsNULL')


class GearmanWorkerTestCase(unittest.TestCase):
    pass
