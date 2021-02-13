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
    - pip install swordiedb
    - pip install mysql-connector-python-rf
    - pip install pycryptodomex
    - pip install SQLAlchemy
  - Make a schema in MySQL named `spirit` and run `initTables_characters.sql` first, and then the rest of them in any order.
  - Run server.py in PyCharm and you should be good to go.

## Current Progress:
  - General:
    - [x] AES Encryption 
    - [x] Packet with write/read properties
    - [x] InPacket Handler
    - [x] Packet Reader
    - [x] Database ORM
  - Login Handler:
    - [x] Login Server
    - [x] Login
    - [x] Auto Register
    - [x] Select World
    - [x] Channel Select
    - [x] Character List
    - [x] Character Creation (Sorta)
    - [ ] Pic Creation
    - [ ] Character Deletion
    - [ ] Pic Verification
  - Goals:
    - [ ] Channel Server
    - [ ] Get in game
    

Tech Stack:
- Python 3.8.5
- MySQL & WAMP

Inspirations:
  - Rooba
  - Swordie


A Project mostly for learning and educational purposes
