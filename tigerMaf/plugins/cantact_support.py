from telethon import events, Button
from tigerMaf import app, STEP, ADMIN
from tigerMaf.filters import step, is_text, is_private
from tigerMaf.decorators import check_user, check_block
from tigerMaf.buttons import start_buttons
from tigerMaf.sql_helpers import get_user


@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "message_to_admin") and is_text(e) and is_private(e)))
async def message_to_admin3(event):

    await event.respond("پیام ارسال شد", buttons=start_buttons)

    user = get_user(event.sender_id)

    message_text = f"""پیام جدید از طرف [ {user.league} {user.name} ]
آیدی عددی: {event.sender_id}
پیام:
    
{event.raw_text}"""
    await app.send_message(ADMIN, message_text, buttons=[[Button.inline("پاسخ", data=f"message_to_user-{event.sender_id}"), Button.inline("بلاک/آنبلاک", data=f"block_unblock_user-{event.sender_id}")]])

    STEP[str(event.sender_id)] = ("home", )

@app.on(events.NewMessage(incoming=True, pattern="👨‍💻پیام به ادمین👨‍💻", func=lambda e: step(e, "home") and is_private(e)))
@check_user
@check_block
async def cantact_support(event):
    await message_to_admin2(event)

@app.on(events.CallbackQuery(data="message_to_admin",func=lambda e : step(e, "home")))
@check_block
async def message_to_admin(event):
    await message_to_admin2(event)

async def message_to_admin2(event):
    sender = event.sender_id

    support_message = """پیامت رو اینجا بنویس تا به ادمین برسه!

برای خروج، از دکمه بازگشت استفاده کن 👇😉"""

    await event.respond(support_message, buttons=[[Button.text("❌بازگشت❌", resize=True)]])

    STEP[str(sender)] = ("message_to_admin", )

