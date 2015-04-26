import unittest

import pinion


class GearmanClientTestCase(unittest.TestCase):

    def test_client_accepts_hosts(self):
        expected = [("127.0.0.1", 4730)]
        self.assertEqual(pinion.GearmanClient([("127.0.0.1", "4730")]).hosts, expected)
        self.assertEqual(pinion.GearmanClient(["127.0.0.1"]).hosts, expected)
        self.assertEqual(pinion.GearmanClient(["127.0.0.1:4730"]).hosts, expected)
        self.assertEqual(pinion.GearmanClient([{'host': "127.0.0.1"}]).hosts, expected)
        self.assertEqual(pinion.GearmanClient([{'host': "127.0.0.1", 'port': "4730"}]).hosts, expected)

    def test_submit_job_job_data_does_not_contain_null(self):
        client = pinion.GearmanClient(["127.0.0.1"])
        with self.assertRaises(pinion.GearmanException):
            client.submit_job('task', b'\x00containsNULL')


class GearmanWorkerTestCase(unittest.TestCase):
    pass
