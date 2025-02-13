from telethon import events, Button
from tigerMaf import app, STEP
from tigerMaf.decorators import check_user
from tigerMaf.filters import step, is_sudo, is_text
from tigerMaf.sql_helpers import get_user, update_user_status
from tigerMaf.buttons import start_buttons

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "user_statitics")))
@check_user
async def user_statitics(event : events.NewMessage.Event):

    user_id = event.sender_id
    STEP[str(user_id)] = ("home", )

    target_user = event.raw_text
    if target_user.isdigit():
        if len(target_user) >= 8:

            user = get_user(int(target_user))
        
        else:

            user = get_user(None, id=int(target_user))
    else:

        user = get_user(None, name=target_user)

    if not user:

        await event.respond("کاربر یافت نشد", buttons=[[Button.text("❌بازگشت❌", resize=True)]])
        return
    
    user_access_buttons = [
        [Button.inline("تغییر وضعیت", data=f"change_user_status-{user.user_id}")],
        [Button.inline("راهنمای وضعیت", data=f"help_user_status")],
        [Button.inline("بازگشت", data="panel")]
    ]

    await event.respond("اطلاعات کاربر :‌", buttons=start_buttons)
    sudo_text = f"""نام بازی: {user.league} {user.name}
آیدی عددی: {user.user_id}
موجودی: {user.balance}
وضعیت: {user.status}"""
    await event.respond(sudo_text, buttons=user_access_buttons)
    return

@app.on(events.CallbackQuery(pattern="user_statitics", func=lambda e: is_sudo(e)))
@check_user
async def user_statitics(event : events.CallbackQuery.Event):
    user_id = event.sender_id
    
    await event.respond("کد یا نام یا آیدی عددی کاربر رو بفرست", buttons=Button.text("❌بازگشت❌", resize=True))

    STEP[str(user_id)] = ("user_statitics", )
    return

@app.on(events.CallbackQuery(pattern="help_user_status", func=lambda e: is_sudo(e)))
@check_user
async def help_user_status(event : events.CallbackQuery.Event):

    sudo_text = f"""0 = ban
1 = normaluser
2 = registerd
3 = registerd + dart
4 = registerd + dart + bowling
5 = registerd + dart + bowling + basketball
6 = registerd + dart + bowling + basketball + football
7 = registerd + dart + bowling + basketball + football + cazino"""
    
    await event.respond(sudo_text)
    return

@app.on(events.CallbackQuery(pattern=r"^change_user_status", func=lambda e: is_sudo(e)))
@check_user
async def change_user_status(event : events.CallbackQuery.Event):

    decoded_data = event.data.decode("utf-8")
    target_user = decoded_data.split("-")[1]
    user_id = event.sender_id

    await event.respond("وضعیت جدید کاربر رو وارد کنید حتما قبل از تغییر بخش راهنمای وضعیت را مشاهده کنید", buttons=[[Button.text("❌بازگشت❌", resize=True)]])

    STEP[str(user_id)] = ("change_user_status_get_status", target_user)

    return


@app.on(events.NewMessage(incoming=True, func=lambda e : step(e, "change_user_status_get_status")))
@check_user
async def change_user_status_get_status(event : events.NewMessage.Event):

    user_id = event.sender_id
    target_user = STEP[str(user_id)][1]

    status = event.raw_text

    if status not in ["0", "1", "2", "3", "4", "5", "6", "7"]:

        await event.respond("وضعیت وارد شده نامعتبر است", buttons=[[Button.text("❌بازگشت❌", resize=True)]])
        return
    
    update_user_status(target_user, int(status))

    await event.respond("وضعیت با موفقیت تغییر کرد", buttons=start_buttons)

    STEP[str(user_id)] = ("home", )

    return