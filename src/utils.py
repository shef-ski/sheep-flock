import time
import os
from src import LOG_OUTPUTFILE

SHOULD_TIME = bool(os.getenv("TIME_EXECUTION", 0))


def timed(func):
    def timer_wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        duration = time.time() - start
        open(LOG_OUTPUTFILE, "a").write(f"{func.__name__},{duration}\n")
        return res

    def default(*args, **kwargs):
        return func(*args, **kwargs)

    return timer_wrapper if SHOULD_TIME else default


def strtobool(val: str) -> int:
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return 1
    elif val in ("n", "no", "f", "false", "off", "0"):
        return 0
    else:
        raise ValueError(f"Invalid truth value: {val}")

