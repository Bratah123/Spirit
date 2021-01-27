# Spirit
Maplestory V176

A MapleStory Server Emulator in Python.

Current Conventions:
- methods: snake_case
- variables: snake_case
- classes: PascalCase
- "Constants": MACRO_CASE
- Note: Only use `@staticmethod` for out_packet functions, else use top level functions

Installation:
- Install [Python](https://www.python.org/)
  - Preferably v3.8.5+
- Install dependencies by using `pip install -r requirements.txt`
  - Note: It is recommended to create a virtual environment (VENV)
  - If you wish to manually install dependencies (on venv) here is the list:
    - pip install swordiedb==1.0.2
    - pip install mysql-connector-python-rf==2.2.2
    - pip install pycryptodomex==3.9.9

Current Progress:
- Character Creation Works!
  - TODO: Implement Saving/Database

Tech Stack:
- Python 3.8.5
- MySQL & WAMP

Inspirations:
  - Rooba
  - Swordie


A Project mostly for learning and educational purposes
