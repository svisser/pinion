import unittest

import pinion


class GearmanClientTestCase(unittest.TestCase):

    def test_client_accepts_hosts(self):
        expected = [("127.0.0.1", 4730)]
        self.assertEqual(pinion.GearmanClient([("127.0.0.1", "4730")]).hosts, expected)
        self.assertEqual(pinion.GearmanClient(["127.0.0.1"]).hosts, expected)
        self.assertEqual(pinion.GearmanClient(["127.0.0.1:4730"]).hosts, expected)


class GearmanWorkerTestCase(unittest.TestCase):
    pass
