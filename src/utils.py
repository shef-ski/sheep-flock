import time
import os
from datetime import datetime
from pathlib import Path
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
        func(*args, **kwargs)
    

    return timer_wrapper if SHOULD_TIME else default
