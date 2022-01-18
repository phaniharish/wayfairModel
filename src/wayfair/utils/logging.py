import sys
import logging


# link the log streams to stdout, so they will be logged to the container logs
LOGGING_PREFIX = "%(asctime)s - %(levelname)s - "
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(f"{LOGGING_PREFIX}%(message)s"))
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
