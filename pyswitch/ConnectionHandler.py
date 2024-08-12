import io
import logging
from ssl import create_default_context
import ssl

from loguru import logger
from pyswitch.setup_logging import setup_logging
from pyswitch.ssl import SSLProtocolVersion
from pyswitch.ssl_constants import SSLContentType
from pyswitch.tls import TLSProtocolVersion
from pyswitch.tls_constants import TLSContentType
from pyswitch.utils import bin2hex
import socket
from socketserver import StreamRequestHandler

DEFAULT_LOGGING_LEVEL = logging.DEBUG


setup_logging(DEFAULT_LOGGING_LEVEL)


class ConnectionHandler(StreamRequestHandler):
    request: socket.socket
    rfile: io.BufferedReader

    def handle(self):
        logger.debug(
            "Connection from: ", self.client_address, "id: ", self.request.fileno()
        )
        print("Connection from: ", self.client_address)

        first_bytes = self.request.recv(32814, socket.MSG_PEEK)

        print("first_bytes_len: ", len(first_bytes))

        print("First 4 bytes: ", bin2hex(first_bytes))

        ssl_class = first_bytes[0] & 0x80

        print("SSL Class: ", ssl_class)

        try:
            content_type = TLSContentType(first_bytes[0])
            protocol_version = TLSProtocolVersion(first_bytes[1:3])
        except ValueError:
            try:
                ssl_record_length = ((first_bytes[0] & 0x7F) << 8) | first_bytes[1]
                ssl_is_escape = first_bytes[2] & 0x80

                print("SSL Record Length: ", ssl_record_length)

                if ssl_is_escape:
                    print("SSL Record is escape")
                    return
                else:
                    ssl_record_type = first_bytes[2]
                    print("SSL Record Type: ", ssl_record_type)
                    content_type = SSLContentType("handshake")
                    protocol_version = SSLProtocolVersion(first_bytes[3:5])
            except Exception as e:
                print("Error: ", e)
                return

        print("Content Type: ", content_type.name)

        print("Protocol version: ", protocol_version)

        ssl_context = create_default_context(ssl.Purpose.CLIENT_AUTH)

        with ssl_context.wrap_socket(self.request, server_side=True) as ssl_socket:
            print("SSL version: ", ssl_socket.version())
