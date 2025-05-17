# sheep-flock

### About

An agent-based model implementation for simulating a sheep flock and herd dogs. 

In the .env file, you can set parameters for a simulation. We recommend focussing on these parameters:
- N_SHEEP
- N_DOG
- SPAWN_CONTROLLABLE_DOG (Set to True for a controllable dog that can be controlled using the arrow keys)
- SHEEP_SPAWN_DISTRIBUTION

### Setup

Use Python 3.12 or a similar version. Create a virtual environment using ``python -m venv venv``, activate it (Windows: ``venv\Scripts\activate ``, Linux/macOS: ``source venv/bin/activate``) and use ``pip install -r requirements.txt`` to install the necessary packages into the venv.

To start a simulation, run the main.py.

from the root directory of the project run:
```
python -m src.main
```



