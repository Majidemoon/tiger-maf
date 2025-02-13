from telethon import events
from tigerMaf import CHANNEL, app, CHANNEL_LINK, MAFIA_GAME_BOT_USERNAME
from telethon.errors import UserNotParticipantError
from functools import wraps
from tigerMaf.sql_helpers import get_user, create_user
from tigerMaf import STEP

def forced_join(func):
    @wraps(func)
    async def wrapper(event : events.NewMessage.Event):
        user_id = event.sender_id

        try:
            await app.get_permissions(CHANNEL, user_id)
            await app.get_permissions(-1002280671664, user_id)
            await app.get_permissions(-1002078361352, user_id)
            await func(event)
        except UserNotParticipantError:

            await event.reply(
                f"""برای استفاده از قابلیت های ربات شما باید در کانال های زیر عضو باشید👇

{CHANNEL_LINK} - کانال مافیا تایگر 
https://t.me/akharin_gheghenos
https://t.me/+B8IjS_mibSE5MmM0""",
link_preview=False
            )
            return
    return wrapper


def signin_required(func):
    @wraps(func)
    async def wrapper(event : events.NewMessage.Event):
        user = get_user(event.sender_id)
        if user.name:
            await func(event)
        else:
            signin_required_text = F"""❌برای استفاده از این قابلیت شما باید نام شما ثبت شده باشه ولی شما هنوز ثبت نام نکردید!

برای ثبت نام کافیه وارد ربات مافیا {MAFIA_GAME_BOT_USERNAME} بشید دکمه پروفایل رو بزنید پروفایل رو برای این ربات فوروارد کنید(توجه کنید فوروارد!)تا ربات اسم و لیگت رو متوجه بشه و ذخیره کنه به همین سادگی
آموزش ویدیویی👇
/guideline"""

            await event.respond(signin_required_text)
            return
    return wrapper

def check_user(func):
    @wraps(func)
    async def wrapper(event : events.NewMessage.Event):
        user_id = event.sender_id
        if str(user_id) in STEP.keys():
            await func(event)
        else:
            STEP[str(user_id)] = ("home", )
            await func(event)
    return wrapper

def check_block(func):
    @wraps(func)
    async def wrapper(event : events.NewMessage.Event):
        user_id = event.sender_id
        user = get_user(user_id)
        if not user:
            create_user(user_id)
        
        if user.status > 0:
            await func(event)
        else:
            await event.respond("❌ در حال حاضر حساب شما مسدود میباشد")
    return wrapper
