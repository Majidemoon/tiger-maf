from telethon import events, Button
from tigerMaf import app, STEP
from tigerMaf.filters import step, is_text
from tigerMaf.sql_helpers import get_user, block_unblock_user
from tigerMaf.buttons import start_buttons

async def block_unblock_user3(event : events.NewMessage.Event, user_id : int):

    status = block_unblock_user(user_id)

    if status == "blocked":
        admin_text = f"کاربر {user_id} با موفقیت بلاک شد"
        user_text = "حساب شما توسط ادمین مسدود شد🛑"

    else:
        admin_text = f"کاربر {user_id} با موفقیت آزاد شد"
        user_text = "حساب شما توسط ادمین از مسدودیت خارج شد✅"

    await event.respond(admin_text, buttons=start_buttons)

    await app.send_message(user_id, user_text)

    STEP[str(event.sender_id)] = ("home", )
    return

@app.on(events.NewMessage(incoming=True, func=lambda e : is_text(e) and step(e, "block_unblock_user_get_user")))
async def block_unblock_user2(event : events.NewMessage.Event):

    target_user = event.raw_text

    if target_user.isdigit():
        if len(target_user) >= 8:

            user = get_user(int(target_user))
        
        else:

            user = get_user(None, id=int(target_user))

    else:

        user = get_user(None, username=target_user)

    if not user:

        await event.respond("کاربر یافت نشد", buttons=[[Button.text("❌بازگشت❌", resize=True)]])
        return
    
    await block_unblock_user3(event, user.user_id)

@app.on(events.CallbackQuery(pattern=r"^block_unblock_user", func=lambda e : step(e, "home")))
async def block_unblock_user1(event : events.CallbackQuery.Event):

    decoded_data = event.data.decode("utf-8")
    splited_data = decoded_data.split("-")

    if len(splited_data) == 2:
        user_id = int(splited_data[1])
        await block_unblock_user3(event, user_id)
        return
    
    await event.respond("آیدی عددی یا شماره کاربر در لیست و یا نام کاربر را وارد کنید", buttons=[[Button.text("❌بازگشت❌", resize=True)]])

    STEP[str(event.sender_id)] = ("block_unblock_user_get_user", )

    return