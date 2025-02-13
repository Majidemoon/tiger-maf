from telethon import TelegramClient
from decouple import config
import logging
from tigerMaf.models import session, Settings

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Basics
API_ID = config('API_ID', default=None, cast=int)
API_HASH = config('API_HASH', default=None)
BOT_TOKEN = config('BOT_TOKEN', default=None)
CHANNEL = config('CHANNEL', default=None, cast=int)
CHANNEL_LINK = config('CHANNEL_LINK', default=None)
MAFIA_GAME_BOT_ID = config('MAFIA_GAME_BOT_ID', default=None, cast=int)
MAFIA_GAME_BOT_USERNAME = config('MAFIA_GAME_BOT_USERNAME', default=None)
STEP = {}
STEP_TIME = {}
ADMIN = config('ADMIN', default=None, cast=int)
BOT_USERNAME = config('BOT_USERNAME', default=None)
TASK_CHANNEL = config('TASK_CHANNEL', default=None)
LOG_CHANNEL = config('LOG_CHANNEL', default=None, cast=int)

COMMANDS_LIST = [
    "/start",
    "/help",
    "/guideline",
    "/profile",
    "/like",
    "/panel",
    "/guideline2",
    "/guideline3",
    "/guideline4",
    "/list",
    "/DUEL",
    "/getcoin",
    "/task"
]

app = TelegramClient('TigerMaf', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

SessionLocal = session

init_session = SessionLocal()
settings = init_session.query(Settings).first()

if not settings:
    settings = Settings(
        id=1, 
        bot_on_off=1, 
        channel_photo_lock=1, 
        channel_video_lock=1, 
        channel_gif_lock=1, 
        channel_sticker_lock=1, 
        channel_audio_lock=1, 
        channel_voice_lock=1, 
    )
    init_session.add(settings)
    init_session.commit()

init_session.close()