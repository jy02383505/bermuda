import asyncore
import logging
import socket, sys, time
from cStringIO import StringIO
from util import log_utils


# LOG_FILENAME = '/Application/bermuda/logs/asyncpostal.log'
# # logging.basicConfig(filename=LOG_FILENAME,
# #                     format='%(asctime)s - %(name)s - %(levelname)s - %(process)d - Line:%(lineno)d - %(message)s',
# #                     level=logging.INFO)
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(process)d - Line:%(lineno)d - %(message)s")
# fh = logging.FileHandler(LOG_FILENAME)
# fh.setFormatter(formatter)
#
# logger = logging.getLogger('asyncpostal')
# logger.addHandler(fh)
# logger.setLevel(logging.WARNING)

logger = log_utils.get_postal_Logger()


class HttpClient(asyncore.dispatcher):
    def __init__(self, host, port, body, read_count=1000, my_map=None, connect_timeout=1.5, response_timeout=1.5):
        self.host = host
        self.start_time = time.time()
        self.connect_time = time.time()
        # LOG_FILENAME = '/Application/bermuda/logs/asyncpostal.log'
        # # logging.basicConfig(filename=LOG_FILENAME,
        # #                     format='%(asctime)s - %(name)s - %(levelname)s - %(process)d - Line:%(lineno)d - %(message)s',
        # #                     level=logging.INFO)
        # formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(process)d - Line:%(lineno)d - %(message)s")
        # fh = logging.FileHandler(LOG_FILENAME)
        # fh.setFormatter(formatter)
        #
        # self.logger = logging.getLogger('asyncpostal')
        # self.logger.addHandler(fh)
        # self.logger.setLevel(logging.WARNING)
        # # self.logger = log_utils.get_postal_Logger()
        self.logger = logger
        asyncore.dispatcher.__init__(self, map=my_map)
        self.write_buffer = 'POST / HTTP/1.0\r\nContent-Length:%d\r\n\r\n%s' % (len(body), body)
        self.read_buffer = StringIO()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (self.host, port)
        self.logger.debug('connecting to %s', address)
        self.connect(address)
        self.strerror = 'no_error'
        self.read_count = read_count
        self.response_code = 200
        self.total_cost = 0
        self.connect_cost = 0
        self.response_cost = 0
        self.connect_timeout = connect_timeout
        self.response_timeout = response_timeout

    # 501 the refreshd response too slow
    # 502 The network is OK,But the refreshd does not work
    # 503 can not reach the server

    def handle_connect(self):
        self.connect_time = time.time()
        self.logger.debug('handle_connect(),{0}'.format(self.connect_time))

    def handle_close(self):
        self.close()
        end_time = time.time()
        self.connect_cost = self.connect_time - self.start_time
        self.total_cost = end_time - self.start_time
        self.response_cost = end_time - self.connect_time
        self.logger.debug(
            'host={0} code={1} cost={2:.2f} connect_cost={3:.2f} response_cost={4:.2f}'.format(
            self.host, self.response_code, self.total_cost, self.connect_cost,
             self.response_cost))

    def handle_error(self):
        try:
            t, v, tb = sys.exc_info()
            self.strerror = v.strerror
            self.response_code = 502
        except Exception, e:
            self.response_code = 502
            self.strerror = 'Connection refused %s' % e

    def writable(self):
        is_writable = (not self._is_connect_timeout()) and (len(self.write_buffer) > 0)
        return is_writable

    def _is_connect_timeout(self):
        is_timeout = True if not self.connected and (time.time() - self.start_time) >= self.connect_timeout else False
        return is_timeout

    def _is_response_timeout(self):
        is_timeout = True if self.connected and (time.time() - self.connect_time) >= self.response_timeout else False
        return is_timeout

    def readable(self):
        if self._is_connect_timeout():
            self.connect_time = time.time()
            self.strerror = 'Connection time out'
            self.response_code = 503
            self.handle_close()
            return False
        if self._is_response_timeout():
            self.strerror = 'readable too much'
            self.response_code = 501
            self.handle_close()
            return False
        return True

    def handle_write(self):
        sent = self.send(self.write_buffer)
        self.logger.debug('handle_write() -> "%s"', self.write_buffer[:sent])
        self.write_buffer = self.write_buffer[sent:]

    def handle_read(self):
        self.logger.debug('handle_read() -> starting')
        data = self.recv(8192)
        self.logger.debug('handle_read() -> %d bytes', len(data))
        self.read_buffer.write(data)

class HttpClient_url(asyncore.dispatcher):
    def __init__(self, host, port, Interface, body, read_count=1000, my_map=None, connect_timeout=1.5, response_timeout=1.5):
        self.host = host
        self.start_time = time.time()
        self.connect_time = time.time()
        self.logger = logger
        asyncore.dispatcher.__init__(self, map=my_map)
        #self.write_buffer = 'POST /checkcertisexits HTTP/1.0\r\nContent-Length:%d\r\n\r\n%s' % (len(body), body)
        self.write_buffer = 'POST /%s HTTP/1.0\r\nContent-Length:%d\r\n\r\n%s' % (Interface,len(body), body)
        self.read_buffer = StringIO()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (self.host, port)
        self.logger.debug('connecting to %s', address)
        self.connect(address)
        self.strerror = 'no_error'
        self.read_count = read_count
        self.response_code = 200
        self.total_cost = 0
        self.connect_cost = 0
        self.response_cost = 0
        self.connect_timeout = connect_timeout
        self.response_timeout = response_timeout

    # 501 the refreshd response too slow
    # 502 The network is OK,But the refreshd does not work
    # 503 can not reach the server

    def handle_connect(self):
        self.connect_time = time.time()
        self.logger.debug('handle_connect(),{0}'.format(self.connect_time))

    def handle_close(self):
        self.close()
        self.close()
        end_time = time.time()
        self.connect_cost = self.connect_time - self.start_time
        self.total_cost = end_time - self.start_time
        self.response_cost = end_time - self.connect_time
        self.logger.debug(
            'ip={0} code={1} cost={2:.2f} connect_cost={3:.2f} response_cost={4:.2f}'.format(
            self.host, self.response_code, self.total_cost, self.connect_cost,
             self.response_cost))

    def handle_error(self):
        try:
            t, v, tb = sys.exc_info()
            self.strerror = v.strerror
            self.response_code = 502
        except Exception, e:
            self.response_code = 502
            self.strerror = 'Connection refused %s' % e

    def writable(self):
        is_writable = (not self._is_connect_timeout()) and (len(self.write_buffer) > 0)
        return is_writable

    def _is_connect_timeout(self):
        is_timeout = True if not self.connected and (time.time() - self.start_time) >= self.connect_timeout else False
        return is_timeout

    def _is_response_timeout(self):
        is_timeout = True if self.connected and (time.time() - self.connect_time) >= self.response_timeout else False
        return is_timeout

    def readable(self):
        if self._is_connect_timeout():
            self.connect_time = time.time()
            self.strerror = 'Connection time out'
            self.response_code = 503
            self.handle_close()
            return False
        if self._is_response_timeout():
            self.strerror = 'readable too much'
            self.response_code = 501
            self.handle_close()
            return False
        self.logger.debug('test_rubin readable is true')
        return True

    def handle_write(self):
        sent = self.send(self.write_buffer)
        self.logger.debug('handle_write() -> "%s"', self.write_buffer[:sent])
        self.write_buffer = self.write_buffer[sent:]

    def handle_read(self):
        self.logger.debug('handle_read() -> starting')
        data = self.recv(8192)
        self.logger.debug('handle_read() -> %d bytes', len(data))
        self.read_buffer.write(data)


class HttpClient_test(asyncore.dispatcher):
    def __init__(self, host, port, body, read_count=1000, my_map=None, connect_timeout=1.5, response_timeout=1.5):
        self.host = host
        self.start_time = time.time()
        self.connect_time = time.time()
        # LOG_FILENAME = '/Application/bermuda/logs/asyncpostal.log'
        # # logging.basicConfig(filename=LOG_FILENAME,
        # #                     format='%(asctime)s - %(name)s - %(levelname)s - %(process)d - Line:%(lineno)d - %(message)s',
        # #                     level=logging.INFO)
        # formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(process)d - Line:%(lineno)d - %(message)s")
        # fh = logging.FileHandler(LOG_FILENAME)
        # fh.setFormatter(formatter)
        #
        # self.logger = logging.getLogger('asyncpostal')
        # self.logger.addHandler(fh)
        # self.logger.setLevel(logging.WARNING)
        # # self.logger = log_utils.get_postal_Logger()
        self.logger = logger
        asyncore.dispatcher.__init__(self, map=my_map)
        self.write_buffer = 'GET %s HTTP/1.0\r\n\r\n' % body
        self.read_buffer = StringIO()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (self.host, port)
        self.logger.debug('connecting to %s', address)
        self.connect(address)
        self.strerror = 'no_error'
        self.read_count = read_count
        self.response_code = 200
        self.total_cost = 0
        self.connect_cost = 0
        self.response_cost = 0
        self.connect_timeout = connect_timeout
        self.response_timeout = response_timeout

    # 501 the refreshd response too slow
    # 502 The network is OK,But the refreshd does not work
    # 503 can not reach the server

    def handle_connect(self):
        self.connect_time = time.time()
        self.logger.debug('handle_connect(),{0}'.format(self.connect_time))

    def handle_close(self):
        self.close()
        end_time = time.time()
        self.connect_cost = self.connect_time - self.start_time
        self.total_cost = end_time - self.start_time
        self.response_cost = end_time - self.connect_time
        self.logger.debug(
            'host={0} code={1} cost={2:.2f} connect_cost={3:.2f} response_cost={4:.2f}'.format(
            self.host, self.response_code, self.total_cost, self.connect_cost,
             self.response_cost))

    def handle_error(self):
        try:
            t, v, tb = sys.exc_info()
            self.strerror = v.strerror
            self.response_code = 502
        except Exception, e:
            self.response_code = 502
            self.strerror = 'Connection refused %s' % e

    def writable(self):
        is_writable = (not self._is_connect_timeout()) and (len(self.write_buffer) > 0)
        return is_writable

    def _is_connect_timeout(self):
        is_timeout = True if not self.connected and (time.time() - self.start_time) >= self.connect_timeout else False
        return is_timeout

    def _is_response_timeout(self):
        is_timeout = True if self.connected and (time.time() - self.connect_time) >= self.response_timeout else False
        return is_timeout

    def readable(self):
        if self._is_connect_timeout():
            self.connect_time = time.time()
            self.strerror = 'Connection time out'
            self.response_code = 503
            self.handle_close()
            return False
        if self._is_response_timeout():
            self.strerror = 'readable too much'
            self.response_code = 501
            self.handle_close()
            return False
        return True

    def handle_write(self):
        sent = self.send(self.write_buffer)
        self.logger.debug('handle_write() -> "%s"', self.write_buffer[:sent])
        self.write_buffer = self.write_buffer[sent:]

    def handle_read(self):
        self.logger.debug('handle_read() -> starting')
        data = self.recv(8192)
        self.logger.debug('handle_read() -> %d bytes', len(data))
        self.read_buffer.write(data)
