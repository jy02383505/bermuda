# import asyncore
# import logging
# import socket, sys, time
# from cStringIO import StringIO
# from __init__ import *
# from core import asyncpostal
# from core.asyncpostal import  HttpClient
#
# class HttpClientTest(unittest.TestCase):
#     def setUp(self):
#         asyncpostal.asyncore=mock()
#         asyncpostal.asyncore.dispatcher=mock()
#         when(asyncpostal.asyncore.dispatcher).__init__(mock(),map=None)
#             # .thenReturn("")
#         socket=mock()
#         when(socket).socket(mock(), mock())
#         self.test=HttpClient('localhost',21118,body=test_data.COMMAND_URL_LIST_ONE , read_count=1000)
#
#
#     def test_handle_connect(self):
#
#         self.test.handle_connect()
#
#     def test_handle_close(self):
#         self.test.handle_close()
#         self.close()
#         end_time = time.time()
#         self.connect_cost = int((self.connect_time - self.start_time) * 1000)
#         self.total_cost = int((end_time - self.start_time) * 1000)
#         self.response_cost = int((end_time - self.connect_time) * 1000)
#         self.logger.debug('host=%s code=%s cost=%dms connect_cost=%d response_cost=%d' % (
#             self.host, self.response_code, self.total_cost, self.connect_cost, self.response_cost))
#
#
#     def test_handle_error(self):
#         asyncpostal.sys=mock()
#         t, v, tb='t',json.loads('{"strerror":"ee"}'),'tb'
#         when(asyncpostal.sys).exc_info().thenReturn(t, v, tb)
#         self.test.handle_error()
#         self.assertEqual(self.test.strerror,'ee')
#         self.assertEqual(self.test.response_code,502)
#
#
#     def test_writable(self):
#         rslt = self.test.writable()
#         self.assertTrue(rslt)
#
#     def test_is_connect_timeout(self):
#         rslt = self.test._is_connect_timeout()
#         self.assertTrue(rslt)
#
#     def test_is_response_timeout(self):
#         rslt = self.test._is_response_timeout()
#         self.assertTrue(rslt)
#
#     def test_readable(self):
#         rslt = self.test.readable()
#         self.assertTrue(rslt)
#
#
#     # def test_handle_write(self):
#     #     sent = self.send(self.write_buffer)
#     #     self.logger.debug('handle_write() -> "%s"', self.write_buffer[:sent])
#     #     self.write_buffer = self.write_buffer[sent:]
#     #
#     # def test_handle_read(self):
#     #     self.logger.debug('handle_read() -> starting')
#     #     data = self.recv(8192)
#     #     self.logger.debug('handle_read() -> %d bytes', len(data))
#     #     self.read_buffer.write(data)
