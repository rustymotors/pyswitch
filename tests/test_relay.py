import socket
import threading
import unittest

from pyswitch.src.relay import relay_streams


class RelayStreamsTestCase(unittest.TestCase):
    def test_forwards_bytes_both_directions_and_closes_on_peer_close(self):
        # client <-> client_side  ==(relay_streams)==  backend_side <-> backend
        client, client_side = socket.socketpair()
        backend_side, backend = socket.socketpair()

        relay_thread = threading.Thread(
            target=relay_streams, args=(client_side, backend_side), daemon=True
        )
        relay_thread.start()

        client.sendall(b"hello from client")
        self.assertEqual(backend.recv(4096), b"hello from client")

        backend.sendall(b"hello from backend")
        self.assertEqual(client.recv(4096), b"hello from backend")

        client.close()
        relay_thread.join(timeout=5)
        self.assertFalse(relay_thread.is_alive())

        backend.close()

    def test_idle_timeout_closes_relay(self):
        client, client_side = socket.socketpair()
        backend_side, backend = socket.socketpair()

        relay_thread = threading.Thread(
            target=relay_streams,
            args=(client_side, backend_side),
            kwargs={},
            daemon=True,
        )

        import pyswitch.src.relay as relay_module

        original_timeout = relay_module.IDLE_TIMEOUT_SECONDS
        relay_module.IDLE_TIMEOUT_SECONDS = 0.1
        try:
            relay_thread.start()
            relay_thread.join(timeout=5)
            self.assertFalse(relay_thread.is_alive())
        finally:
            relay_module.IDLE_TIMEOUT_SECONDS = original_timeout
            client.close()
            backend.close()


if __name__ == "__main__":
    unittest.main()
