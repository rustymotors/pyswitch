import logging
import os

DEFAULT_LOGGING_LEVEL = logging.DEBUG
LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 443

# Legacy branch: real SSLv2/weak-cipher clients (old game clients) --
# routed to the existing nginx container, which already terminates this
# correctly. Must be a *different* port than LISTEN_PORT, since pyswitch
# itself now owns LISTEN_PORT publicly.
LEGACY_BACKEND_HOST = os.getenv("PYSWITCH_LEGACY_BACKEND_HOST", "127.0.0.1")
LEGACY_BACKEND_PORT = int(os.getenv("PYSWITCH_LEGACY_BACKEND_PORT", "9443"))

# Modern branch: real TLS 1.0+ clients -- routed to Caddy (or whatever
# terminates real, current TLS for the actual domains).
MODERN_BACKEND_HOST = os.getenv("PYSWITCH_MODERN_BACKEND_HOST", "127.0.0.1")
MODERN_BACKEND_PORT = int(os.getenv("PYSWITCH_MODERN_BACKEND_PORT", "8443"))
