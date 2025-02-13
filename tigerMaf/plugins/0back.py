from telethon import events
from tigerMaf import app, STEP
from tigerMaf.buttons import start_buttons
from tigerMaf.decorators import check_user
from tigerMaf.plugins.task2 import do_task
from tigerMaf.filters import is_private

async def home_function(event):
    if STEP.get(str(event.sender_id))[0] in ["duel_dice_amount", "duel_send_dice"]:
        return

    elif STEP.get(str(event.sender_id))[0] in ["send_direct_message", "get_user_id_or_name"]:
        await event.respond("🏠 از بخش پیام به پلیر خارج شدید. برای ادامه از منو استفاده کنید!", buttons=start_buttons)

    elif STEP.get(str(event.sender_id))[0] == "broadcast_message":
        await event.respond("❎ از بخش پیام همگانی خارج شدید.", buttons=start_buttons)

    elif STEP.get(str(event.sender_id))[0] == "do_task":
        await do_task(event)
    else:
        await event.respond("صفحه اصلی!", buttons=start_buttons)
    
    STEP[str(event.sender_id)] = ("home", )
    return

@app.on(events.NewMessage(incoming=True, pattern="❌بازگشت❌", func=lambda e: is_private(e)))
@check_user
async def back(event):
    await home_function(event)
    

@app.on(events.CallbackQuery(pattern="home"))
@check_user
async def back_home(event):
    await home_function(event)
