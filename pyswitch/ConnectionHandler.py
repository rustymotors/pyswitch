import socket
from socketserver import StreamRequestHandler

from loguru import logger

from pyswitch.config import (
    LEGACY_BACKEND_HOST,
    LEGACY_BACKEND_PORT,
    MODERN_BACKEND_HOST,
    MODERN_BACKEND_PORT,
)
from pyswitch.src.relay import relay_streams
from pyswitch.src.utils import bin2hex, is_msb_set

# Real TLS record ContentType values (RFC 8446 5.1) -- checked directly as
# ints rather than via TLSContentType, since that enum aliases 23 and 255 to
# the same member (APPLICATION_DATA_1 | APPLICATION_DATA_2 is a bitwise OR
# of ints, not a set of accepted values) and would misclassify a legacy
# SSLv2 record whose first byte happens to be 0xFF as modern TLS.
REAL_TLS_CONTENT_TYPES = {20, 21, 22, 23}

# Most ClientHellos land in a single TCP segment well under this; only the
# classification header (a few bytes) actually needs to be present here --
# whatever else arrives in the same read is still forwarded to the backend
# unparsed, along with everything that follows.
INITIAL_READ_SIZE = 65536


class ConnectionHandler(StreamRequestHandler):
    request: socket.socket

    def handle(self):
        logger.debug(
            "Connection from: {}, id: {}".format(
                self.client_address, self.request.fileno()
            )
        )

        try:
            initial_data = self.request.recv(INITIAL_READ_SIZE)
        except OSError as e:
            logger.debug("Error reading initial data: {}", e)
            return

        if not initial_data:
            logger.debug("Client disconnected before sending data")
            return

        logger.debug("First bytes: {}", bin2hex(initial_data[:32]))

        try:
            is_legacy = self._is_legacy_ssl(initial_data)
        except ValueError as e:
            logger.error("Could not classify connection, closing: {}", e)
            return

        if is_legacy:
            backend_host, backend_port = LEGACY_BACKEND_HOST, LEGACY_BACKEND_PORT
            logger.info(
                "{}: classified legacy SSL, routing to {}:{}",
                self.client_address,
                backend_host,
                backend_port,
            )
        else:
            backend_host, backend_port = MODERN_BACKEND_HOST, MODERN_BACKEND_PORT
            logger.info(
                "{}: classified modern TLS, routing to {}:{}",
                self.client_address,
                backend_host,
                backend_port,
            )

        try:
            backend_sock = socket.create_connection((backend_host, backend_port))
        except OSError as e:
            logger.error(
                "Could not connect to backend {}:{}: {}", backend_host, backend_port, e
            )
            return

        try:
            backend_sock.sendall(initial_data)
        except OSError as e:
            logger.error("Could not forward initial data to backend: {}", e)
            backend_sock.close()
            return

        relay_streams(self.request, backend_sock)

    @staticmethod
    def _is_legacy_ssl(data: bytes) -> bool:
        """True if data looks like a legacy SSLv2 record (no real
        ContentType byte); False if it looks like real TLS/SSLv3+. Raises
        ValueError if it matches neither shape."""
        if len(data) < 2:
            raise ValueError("Not enough data to classify connection")

        if data[0] in REAL_TLS_CONTENT_TYPES:
            return False

        # Not a real ContentType -- check for the legacy SSLv2 2/3-byte
        # record header shape instead (the high bit of the first byte is
        # the 2-vs-3-byte-header flag, not a content type at all).
        if is_msb_set(data[0]):
            record_length = ((data[0] & 0x7F) << 8) | data[1]
        else:
            record_length = ((data[0] & 0x3F) << 8) | data[1]

        if record_length <= 0:
            raise ValueError(
                f"First byte 0x{data[0]:02x} is neither a real TLS ContentType "
                "nor a plausible SSLv2 record header"
            )

        return True
