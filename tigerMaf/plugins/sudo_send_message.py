from telethon import events, Button
from tigerMaf import app, STEP
from tigerMaf.filters import step, is_text
from tigerMaf.sql_helpers import get_user
from tigerMaf.buttons import start_buttons
from tigerMaf.decorators import check_user

@app.on(events.NewMessage(incoming=True, func=lambda e : is_text(e) and step(e, "message_to_user_get_text")))
async def message_to_user3(event):

    text = event.raw_text
    user_id = STEP[str(event.sender_id)][1]

    message_text = f"""📩 پیام جدید از طرف مدیریت ربات
    
📃 متن پیام :👇

{text}"""
    await app.send_message(user_id, message_text, buttons=[[Button.inline("پاسخ", data=f"message_to_admin")]])

    STEP[str(event.sender_id)] = ("home", )

    
    await event.respond("📩پیام ارسال شد", buttons=start_buttons)
    return

@app.on(events.NewMessage(incoming=True, func=lambda e : is_text(e) and step(e, "message_to_user_get_user")))
async def message_to_user2(event):

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
    
    await event.respond("متن پیام را وارد کن", buttons=[[Button.text("❌بازگشت❌", resize=True)]])

    STEP[str(event.sender_id)] = ("message_to_user_get_text", user.user_id)

    return

@app.on(events.CallbackQuery(pattern="^message_to_user", func=lambda e : step(e, "home")))
@check_user
async def message_to_user(event):

    decoded_data = event.data.decode("utf-8")
    splited_data = decoded_data.split("-")

    if len(splited_data) == 2:
        user_id = int(splited_data[1])
        await event.respond("متن پیام را وارد کن", buttons=[[Button.text("❌بازگشت❌", resize=True)]])

        STEP[str(event.sender_id)] = ("message_to_user_get_text", user_id)
        return
    
    await event.respond("آیدی عددی یا شماره کاربر در لیست و یا نام کاربر را وارد کنید", buttons=[[Button.text("❌بازگشت❌", resize=True)]])

    STEP[str(event.sender_id)] = ("message_to_user_get_user", )

    return


    