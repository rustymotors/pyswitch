import io
from loguru import logger
from pyswitch.src.ssl.ssl_v2 import SSLv2Record
from pyswitch.src.tls import TLSProtocolVersion
from pyswitch.src.tls_constants import TLSContentType
from pyswitch.src.utils import assert_enough_data, bin2hex, is_msb_set
import socket
from socketserver import StreamRequestHandler


class ConnectionHandler(StreamRequestHandler):
    request: socket.socket
    rfile: io.BufferedReader

    def handle(self):
        logger.debug(
            "Connection from: {}, id: {}".format(
                self.client_address, self.request.fileno()
            )
        )

        first_bytes = peek_data(self.request, len=32814)

        logger.debug("First bytes: {}".format(bin2hex(first_bytes)))

        try:
            content_type = TLSContentType(first_bytes[0])
            print("Content Type: ", content_type.name)
        except ValueError:
            # Unable to parse as TLS, try SSL
            try:
                if is_msb_set(first_bytes[0]):
                    logger.debug("Length MSB is set, record is 2 bytes")
                    record_length = ((first_bytes[0] & 0x7F) << 8) | first_bytes[1]
                else:
                    logger.debug("Length MSB is not set, record is 3 bytes")
                    record_length = ((first_bytes[0] & 0x3F) << 8) | first_bytes[1]

                logger.debug("Record length: {}".format(record_length))
                try:
                    assert_enough_data(
                        len(self.rfile.peek(record_length)), record_length
                    )
                except ValueError as e:
                    logger.error("Error: {}".format(e))

                ssl_record = SSLv2Record(self.rfile.read(record_length))

                logger.debug("SSL Record: {}".format(ssl_record))
                self.request.close()
                return

            except Exception as e:
                print("Error: ", e)
                self.request.close()
                return

        protocol_version = TLSProtocolVersion(first_bytes[1:3])
        print("Protocol version: ", protocol_version)

        return


def peek_data(sock: socket.socket, len: int):
    """
    Receive data from the socket without removing it from the receive buffer.

    Args:
        sock (socket.socket): The socket object to receive data from.
        len (int): The maximum number of bytes to receive.

    Returns:
        bytes: The received data as bytes.

    Raises:
        OSError: If an error occurs while receiving data.

    """
    return sock.recv(len, socket.MSG_PEEK)
