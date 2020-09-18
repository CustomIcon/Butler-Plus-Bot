class Config(object):
    # logger
    LOGGER = True
    # Version

    # Must be filled
    api_id = ''
    api_hash = ''
    # From config
    BUTLER_WORKER = 2
    # LOADER
    BUTLER_LOAD = []
    BUTLER_NOLOAD = []

    DB_URI = ''
    BUTLER_TOKEN = ''
    SUDO = []
    OWNER = 123

class Development(Config):
	TEST_DEVELOP = True
	LOGGER = True

