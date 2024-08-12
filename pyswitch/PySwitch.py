import logging
from pyswitch.ConnectionHandler import ConnectionHandler


from socketserver import ThreadingTCPServer

from pyswitch.setup_logging import setup_logging

DEFAULT_LOGGING_LEVEL = logging.DEBUG


class PySwitch:
    server: ThreadingTCPServer

    def __init__(self):

        setup_logging(DEFAULT_LOGGING_LEVEL)

        self.server = ThreadingTCPServer(("0.0.0.0", 443), ConnectionHandler)

    def run(self):
        try:
            self.server.serve_forever()
        except OSError as e:
            print("Error: ", e)
            print("Exiting")
            exit(1)

        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt")
            print("Exiting")
            exit(0)
