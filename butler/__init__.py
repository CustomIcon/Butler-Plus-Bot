import os
import sys
import time

from pyrogram import Client, errors
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from butler.config import Config

StartTime = time.time()


ENV = bool(os.environ.get('ENV', False))

BUTLER_VERSION = "2.1"

if ENV:
    # Logger
    logger = os.environ.get('LOGGER', True)
    time_country = os.environ.get("time_country", None)

    # Must be filled
    api_id = os.environ.get('api_id', None)
    api_hash = os.environ.get('api_hash', None)

    # From config
    Command = os.environ.get("Command", "! . - ^").split()
    BUTLER_WORKER = int(os.environ.get('ASSISTANT_WORKER', 2))

    try:
        TEST_DEVELOP = bool(os.environ.get('TEST_DEVELOP', False))
    except AttributeError:
        pass

    # APIs
    lydia_api = os.environ.get('lydia_api', None)
    sw_api = os.environ.get('sw_api', None)
    # LOADER
    BUTLER_LOAD = os.environ.get("BUTLER_LOAD", "").split()
    BUTLER_NOLOAD = os.environ.get("BUTLER_NOLOAD", "").split()

    DB_URI = os.environ.get('DB_URI', "postgres://username:password@localhost:5432/database")
    BUTLER_TOKEN = os.environ.get('BUTLER_TOKEN', None)
    SUDO = [int(x) for x in os.environ.get("SUDO", "").split()]
    OWNER = [int(x) for x in os.environ.get("OWNER", "").split()]
else:
    # logger
    logger = Config.LOGGER
    # Version

    # Must be filled
    api_id = Config.api_id
    api_hash = Config.api_hash

    # From config
    Command = Config.Command
    BUTLER_WORKER = Config.BUTLER_WORKER

    # APIs
    sw_api = Config.sw_api
    lydia_api = Config.lydia_api
    # LOADER
    BUTLER_LOAD = Config.BUTLER_LOAD
    BUTLER_NOLOAD = Config.BUTLER_NOLOAD

    DB_URI = Config.DB_URI
    BUTLER_TOKEN = Config.BUTLER_TOKEN
    SUDO = Config.SUDO
    OWNER = Config.OWNER
OwnerName = ""
app_version = f"BUTLER v{BUTLER_VERSION}"
BotUsername = ""
BotID = 0
# Required for some features
# Set temp var for load later
Owner = 0
BotName = ""
OwnerUsername = ""

DB_AVAILABLE = False
BOTINLINE_AVAIABLE = False


# Postgresql
def mulaisql() -> scoped_session:
    global DB_AVAILABLE
    engine = create_engine(DB_URI, client_encoding="utf8")
    BASE.metadata.bind = engine
    try:
        BASE.metadata.create_all(engine)
    except exc.OperationalError:
        DB_AVAILABLE = False
        return False
    DB_AVAILABLE = True
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


async def get_self():
    global Owner, SUDO
    Owner = OWNER
    if Owner not in SUDO:
        SUDO.append(Owner)


async def get_bot():
    global BotID, BotName, BotUsername
    getbot = await butler.get_me()
    BotID = getbot.id
    BotName = getbot.first_name
    BotUsername = getbot.username


BASE = declarative_base()
SESSION = mulaisql()

butler = Client(
    'butler',
    api_id=api_id,
    api_hash=api_hash,
    bot_token=BUTLER_TOKEN,
    workers=BUTLER_WORKER
    )
