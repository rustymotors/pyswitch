from os import getenv
from pyswitch.PySwitch import PySwitch
from dotenv import load_dotenv, find_dotenv

import sentry_sdk


def main():
    load_dotenv(find_dotenv())

    sentry_dsn = getenv("SENTRY_DSN")

    sentry_sdk.init(
        dsn=sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
        enable_tracing=True,
    )

    switch = PySwitch()
    switch.run()


if __name__ == "__main__":
    main()
