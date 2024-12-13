import os
from pathlib import Path
from datetime import datetime

n_sheep = os.getenv("N_SHEEP",0)
n_dog = os.getenv("N_DOG",0)

timestamp_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_OUTPUTFILE = Path(__file__).parent.parent / "logs" / f"durations_{n_sheep}_{n_dog}_{timestamp_now}"
