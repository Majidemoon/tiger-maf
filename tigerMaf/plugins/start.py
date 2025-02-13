
import asyncio
from telethon import events, Button
from tigerMaf import app, CHANNEL, MAFIA_GAME_BOT_USERNAME, STEP
from tigerMaf.sql_helpers import create_user, get_user
from tigerMaf.decorators import check_user
from tigerMaf.buttons import start_buttons
from tigerMaf.filters import is_private

start_text1 = f"""🔥🎲 ثبت نام 🔥🎲

این ربات مخصوص پلیر های مافیا طراحی شده و وقتی شما پیام به کانال یا پیام خصوصی میدید بقیه اسمی که شما باهاش مافیا بازی میکنید رو میبینن نه اسم اکانت تلگرامتون
پس قبل از استفاده از قابلیت های ربات، ربات باید بدونه اسم مافیاتون چیه
برای این کار کافیه وارد ربات مافیا بشید 
{MAFIA_GAME_BOT_USERNAME}
دکمه پروفایل رو بزنید و پروفایل مافیاتون رو برای ربات فوروارد کنید ربات اسم و لیگ شما رو از اون پیامی که فوروارد کردید برمیداره و ذخیره میکنه به همین سادگی
آموزش تصویری ثبت نام کردن👇
/guideline

🔥🎲
🔥🎲🔥🎲
🔥🎲🔥🎲🔥🎲
🔥🎲🔥🎲🔥🎲🔥🎲"""

start_text2 = """سلام به شما 🌹 NAME 🌹عضو جدید ربات 
ورودتان را خوش آمد می گوییم و امیدواریم
لحظات خوبی را در این ربات سپری کنید❤️‍🔥

راهنمای ربات👇

/help"""



@app.on(events.NewMessage(incoming=True, pattern="^/start", func= lambda e: is_private(e)))
@check_user
async def start(event : events.NewMessage.Event):

    name = event.sender.first_name
    user_id = event.sender_id

    user = get_user(user_id)
    if not user:
        splited_text = event.raw_text.split(" ")

        invited_by = None
        if len(splited_text) > 1 and splited_text[1].isdigit():

            ref_link = int(splited_text[1])
            ref_user = get_user(ref_link)
            if ref_user:
                invited_by = ref_user.user_id

        create_user(user_id, invited_by)

        if invited_by:
            await app.send_message(int(invited_by), """یییییییییپ! 🎉
دعوتت جواب داد! 👍
کاربری با لینک دعوت شما عضو ربات شد! 🤝
حالا منتظر باش تا ثبت نام کنه، بعد سکه‌ات رو دریافت میکنی! 💸""")
    
    STEP[str(user_id)] = ("home", )

    start_text2_with_name = start_text2.replace("NAME", name)

    user = get_user(user_id)

    if not user.name:
        await event.respond(start_text1)
    await event.respond(start_text2_with_name, buttons=start_buttons)
