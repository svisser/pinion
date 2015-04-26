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

    def test_create_packet(self):
        self.assertEqual(create_packet(1, []), b'\x00REQ\x00\x00\x00\x01\x00\x00\x00\x00')
        self.assertEqual(create_packet(1, [b'a']), b'\x00REQ\x00\x00\x00\x01\x00\x00\x00\x01a')
        self.assertEqual(create_packet(1, [b'a', b'b']), b'\x00REQ\x00\x00\x00\x01\x00\x00\x00\x03a\x00b')

    def test_create_packet_accepts_only_binary_packet_data(self):
        with self.assertRaises(pinion.GearmanException):
            self.assertEqual(create_packet(1, [u"\u2603"]))


class GearmanClientTestCase(unittest.TestCase):

    def test_submit_job_job_data_does_not_contain_null(self):
        client = pinion.GearmanClient(["127.0.0.1"])
        with self.assertRaises(pinion.GearmanException):
            client.submit_job('task', b'\x00containsNULL')


class GearmanWorkerTestCase(unittest.TestCase):
    pass
