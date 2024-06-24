# (c) @LazyDeveloperr
import os
from os import getenv, environ


# Online Stream and Download
PORT = int(environ.get('PORT', 8080))
NO_PORT = bool(environ.get('NO_PORT', False))
APP_NAME = None
if 'DYNO' in environ:
	ON_HEROKU = True
	APP_NAME = environ.get('APP_NAME')
else:
    ON_HEROKU = False
BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
FQDN = str(getenv('FQDN', BIND_ADRESS)) if not ON_HEROKU or getenv('FQDN','lazy-gangster-baby-lazydeveloperr.koyeb.app') else APP_NAME+'.herokuapp.com'
URL = "https://{}/".format(FQDN) if ON_HEROKU or NO_PORT else \
    "http://{}:{}/".format(FQDN, PORT)
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
WORKERS = int(environ.get('WORKERS', '4'))
SESSION_NAME = str(environ.get('SESSION_NAME', 'LazyBot'))
MULTI_CLIENT = False
name = str(environ.get('name', 'LazyPrincess'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
DISABLE_CHANNEL_BUTTON = bool(environ.get('DISABLE_CHANNEL_BUTTON', False))
HAS_SSL=bool(getenv('HAS_SSL',False))
if HAS_SSL:
    URL = "https://{}/".format(FQDN)
else:
    URL = "http://{}/".format(FQDN)
UPDATES_CHANNEL = str(getenv('UPDATES_CHANNEL', None))
BANNED_CHANNELS = list(set(int(x) for x in str(getenv("BANNED_CHANNELS", "-1001987654567")).split())) 
STREAM_LOGS = environ.get('STREAM_LOGS','-1001895607162')
SESSION = environ.get('SESSION','MissRozy')
CUSTOM_CAPTION = environ.get('CUSTOM_CAPTION')


class Config(object):
	API_ID = int(os.environ.get("API_ID", 13323016))
	API_HASH = os.environ.get("API_HASH", "13323016")
	BOT_TOKEN = os.environ.get("BOT_TOKEN","6144687436:AAGShuVn551CQHCWjRkdoBIteGgV0SUWxBo")
	BOT_USERNAME = os.environ.get("BOT_USERNAME" , "MissRozy_BOT")
	DB_CHANNEL = int(os.environ.get("DB_CHANNEL", -1001772120203))
	BOT_OWNER = int(os.environ.get("BOT_OWNER", "5965340120"))
	DATABASE_URL = os.environ.get("DATABASE_URL","mongodb+srv://lazydeveloperr:lazydeveloperr@Cluster0.lpvunl5.mongodb.net/?retryWrites=true&w=majority")
	UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "-1001765107260")
	LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "-1001895607162")
	BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "1234567890").split())
	FORWARD_AS_COPY = bool(os.environ.get("FORWARD_AS_COPY", True))
	BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))
	LAZY_CHANNEL = int(os.environ.get('LAZY_CHANNEL','-100'))
	LAZY_MODE = bool(os.environ.get("LAZY_MODE", False))
	LAZY_PIC = os.environ.get("LAZY_PIC","https://telegra.ph/file/d382d2fad1fdd2a4ccca4.png")
	LP_BTN_MAIN_CH_USRNM = os.environ.get("LP_BTN_MAIN_CH_USRNM")
	LP_CHANNEL_USRNM = os.environ.get("LP_CHANNEL_USRNM")
	LPCH_ADMIN_USRMN = os.environ.get("LPCH_ADMIN_USRMN")
	LP_CUSTOM_TEMPLATE= os.environ.get("LP_CUSTOM_TEMPLATE")
  # LP_CUSTOM_TEMPLATE= os.environ.get("LP_CUSTOM_TEMPLATE","{file_name} - example \n\n Please Upadate this template acording to you @LazyDeveloperr ")
	BANNED_CHAT_IDS = list(set(int(x) for x in os.environ.get("BANNED_CHAT_IDS", "-1001362659779 -1001255795497").split()))
	OTHER_USERS_CAN_SAVE_FILE = bool(os.environ.get("OTHER_USERS_CAN_SAVE_FILE", True))
	AUTO_DELETE_TIME = int(os.environ.get('AUTO_DELETE_TIME', 20))

	ABOUT_BOT_TEXT = f"""Books Store bot. Just click on the link provided by our channel and get your book free of cost."""
	ABOUT_DEV_TEXT = f"""<b>Make sure to share our channel</b>"""
	LAZY_HOME_TEXT = """Please don't store any file in the uneless you're an admin of Book.org. Otherwise I have to Ban you from using the bot."""
	HOME_TEXT = """Please don't store any file in the uneless you're an admin of Book.org. Otherwise I have to Ban you from using the bot."""



