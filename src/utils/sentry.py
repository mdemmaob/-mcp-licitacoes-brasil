import sentry_sdk
import os

SENTRY_DSN = os.getenv("SENTRY_DSN", "")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=1.0,
        environment=os.getenv("ENVIRONMENT", "production")
    )

def capture_exception(e):
    sentry_sdk.capture_exception(e) 