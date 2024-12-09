import os
from pathlib import Path
from datetime import datetime

n_sheep = os.getenv("N_SHEEP",0)
n_dog = os.getenv("N_DOG",0)
LOG_OUTPUTFILE = Path(__file__).parent.parent / "logs" / f"durations_{n_sheep}_{n_dog}_{datetime.now()}"
