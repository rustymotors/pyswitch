from pyswitch.ConnectionHandler import ConnectionHandler


from socketserver import ThreadingTCPServer

from pyswitch.config import DEFAULT_LOGGING_LEVEL, LISTEN_HOST, LISTEN_PORT
from pyswitch.src.setup_logging import setup_logging


class PySwitch:
    server: ThreadingTCPServer

    def __init__(self):

        setup_logging(DEFAULT_LOGGING_LEVEL)

        try:
            self.server = ThreadingTCPServer(
                (LISTEN_HOST, LISTEN_PORT), ConnectionHandler
            )
        except OSError as e:
            if e.errno == 98:
                print("Port is already in use")
                exit(1)

    def run(self):
        self.server.serve_forever()
