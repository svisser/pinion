import struct

__title__ = 'pinion'
__version__ = '0.0.1'
__author__ = 'Simeon Visser'
__email__ = 'simeonvisser@gmail.com'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2015 Simeon Visser'

from pinion import compat

NULL_BYTE = b'\x00'
MAGIC_CODE_REQ = b'\x00REQ'
MAGIC_CODE_RES = b'\x00RES'

PACKET_TYPE_CAN_DO = 1
PACKET_TYPE_CANT_DO = 2
PACKET_TYPE_RESET_ABILITIES = 3
PACKET_TYPE_PRE_SLEEP = 4
PACKET_TYPE_NOOP = 6
PACKET_TYPE_SUBMIT_JOB = 7
PACKET_TYPE_JOB_CREATED = 8
PACKET_TYPE_GRAB_JOB = 9
PACKET_TYPE_NO_JOB = 10
PACKET_TYPE_JOB_ASSIGN = 11
PACKET_TYPE_WORK_STATUS = 12
PACKET_TYPE_WORK_COMPLETE = 13
PACKET_TYPE_WORK_FAIL = 14
PACKET_TYPE_GET_STATUS = 15
PACKET_TYPE_ECHO_REQ = 16
PACKET_TYPE_ECHO_RES = 17
PACKET_TYPE_SUBMIT_JOB_BG = 18
PACKET_TYPE_ERROR = 19
PACKET_TYPE_STATUS_RES = 20
PACKET_TYPE_SUBMIT_JOB_HIGH = 21
PACKET_TYPE_SET_CLIENT_ID = 22
PACKET_TYPE_CAN_DO_TIMEOUT = 23
PACKET_TYPE_ALL_YOURS = 24
PACKET_TYPE_WORK_EXCEPTION = 25
PACKET_TYPE_OPTION_REQ = 26
PACKET_TYPE_OPTION_RES = 27
PACKET_TYPE_WORK_DATA = 28
PACKET_TYPE_WORK_WARNING = 29
PACKET_TYPE_GRAB_JOB_UNIQ = 30
PACKET_TYPE_JOB_ASSIGN_UNIQ = 31
PACKET_TYPE_SUBMIT_JOB_HIGH_BG = 32
PACKET_TYPE_SUBMIT_JOB_LOW = 33
PACKET_TYPE_SUBMIT_JOB_LOW_BG = 34
PACKET_TYPE_SUBMIT_JOB_SCHED = 35
PACKET_TYPE_SUBMIT_JOB_EPOCH = 36

DEFAULT_GEARMAN_PORT = 4730

JOB_PRIORITY_NORMAL = 0
JOB_PRIORITY_LOW = 1
JOB_PRIORITY_HIGH = 2

SUBMIT_JOB_PACKET_TYPES = {
    (True, JOB_PRIORITY_LOW): PACKET_TYPE_SUBMIT_JOB_LOW_BG,
    (True, JOB_PRIORITY_NORMAL): PACKET_TYPE_SUBMIT_JOB_BG,
    (True, JOB_PRIORITY_HIGH): PACKET_TYPE_SUBMIT_JOB_HIGH_BG,
    (False, JOB_PRIORITY_LOW): PACKET_TYPE_SUBMIT_JOB_LOW,
    (False, JOB_PRIORITY_NORMAL): PACKET_TYPE_SUBMIT_JOB,
    (False, JOB_PRIORITY_HIGH): PACKET_TYPE_SUBMIT_JOB_HIGH,
}


def parse_hosts(hosts):
    result = []
    for host in hosts:
        gearman_address, gearman_port = None, None
        try:
            gearman_address = host['host']
            gearman_port = host['port']
        except (AttributeError, KeyError, TypeError):
            pass
        if gearman_address is None:
            try:
                gearman_address, gearman_port = host
            except (TypeError, ValueError):
                pass
        if gearman_address is None:
            try:
                gearman_address, _, gearman_port = host.partition(':')
            except AttributeError:
                pass
        result.append({
            'host': gearman_address,
            'port': int(gearman_port or DEFAULT_GEARMAN_PORT)
        })
    return result


def create_packet(packet_type, packet_data, is_response=False):
    if not all(isinstance(item, compat.bytes_type) for item in packet_data):
        raise GearmanException("Non-bytes element found in packet data")

    magic_code = MAGIC_CODE_RES if is_response else MAGIC_CODE_REQ
    payload = NULL_BYTE.join(packet_data)
    packet_length = len(payload)
    packet_format = '!4sII{}s'.format(packet_length)
    return struct.pack(packet_format, magic_code, packet_type, packet_length, payload)


class GearmanConnection(object):

    def __init__(self, host, port=DEFAULT_GEARMAN_PORT):
        self.host = host
        self.port = port

    def connect(self):
        pass


class GearmanException(Exception):
    pass


class GearmanManager(object):

    connection_class = GearmanConnection

    def __init__(self, hosts):
        self.hosts = parse_hosts(hosts)
        self.connections = [self.connection_class(host) for host in self.hosts]


class GearmanClient(GearmanManager):

    def submit_job(self, task_name, task_data, priority=JOB_PRIORITY_NORMAL, background=False):
        if NULL_BYTE in task_data:
            raise GearmanException("Job data contains NULL byte")

        unique_id = b''
        packet_data = [task_name.encode('ascii'), unique_id, task_data]
        packet = create_packet(SUBMIT_JOB_PACKET_TYPES[priority, background], packet_data)

    def get_status(self):
        pass

    def set_connection_option(self):
        pass


class GearmanWorker(GearmanManager):

    def register_task(self, task, task_handler, timeout=None):
        pass

    def unregister_task(self, task):
        pass

    def reset_abilities(self):
        pass

    def sleep(self):
        pass

    def request_job(self, unique=False):
        pass

    def send_work_data(self, job, data):
        pass

    def send_work_warning(self, job, data):
        pass

    def send_work_status(self, job, numerator, denominator):
        pass

    def send_work_complete(self, job, data):
        pass

    def send_work_fail(self, job):
        pass

    def send_work_exception(self, job, data):
        pass

    def set_client_id(self, client_id):
        pass
