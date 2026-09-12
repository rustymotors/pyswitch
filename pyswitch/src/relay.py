"""Bidirectional raw-byte TCP relay.

Used once a connection has been classified (legacy SSLv2 vs. modern TLS) --
neither side of the relay is ever parsed or terminated here. Each backend
speaks real TLS (or real SSLv2) to the client directly; this just pumps
bytes between two already-connected sockets until either side closes.
"""

import select
import socket

from loguru import logger

RECV_BUFFER_SIZE = 65536
IDLE_TIMEOUT_SECONDS = 300


def relay_streams(client_sock: socket.socket, backend_sock: socket.socket) -> None:
    """Pumps bytes between client_sock and backend_sock until either side
    closes, errors, or goes idle for IDLE_TIMEOUT_SECONDS. Closes neither
    socket on entry; closes both on exit."""
    sockets = [client_sock, backend_sock]
    try:
        while True:
            readable, _, exceptional = select.select(
                sockets, [], sockets, IDLE_TIMEOUT_SECONDS
            )

            if exceptional:
                logger.debug("Relay: socket exception, closing")
                return

            if not readable:
                logger.debug("Relay: idle timeout, closing")
                return

            for source in readable:
                destination = backend_sock if source is client_sock else client_sock
                try:
                    data = source.recv(RECV_BUFFER_SIZE)
                except OSError as e:
                    logger.debug("Relay: recv error, closing: {}", e)
                    return

                if not data:
                    logger.debug("Relay: peer closed connection")
                    return

                try:
                    destination.sendall(data)
                except OSError as e:
                    logger.debug("Relay: send error, closing: {}", e)
                    return
    finally:
        for sock in (client_sock, backend_sock):
            try:
                sock.close()
            except OSError:
                pass
