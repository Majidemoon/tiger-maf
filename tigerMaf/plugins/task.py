from telethon import events, Button
from tigerMaf import app, STEP, ADMIN, TASK_CHANNEL
from tigerMaf.decorators import check_user, check_block
from tigerMaf.filters import step, is_text, is_photo
from tigerMaf.sql_helpers import get_user
from tigerMaf.buttons import start_buttons
from tigerMaf.plugins.task2 import do_task

@app.on(events.NewMessage(incoming=True, pattern=r"🗂تسک🗂|/task", func=lambda e: step(e, "home")))
@check_user
@check_block
async def task(event):
    await do_task(event)
    print(event)

@app.on(events.NewMessage(incoming=True, func=lambda e : (is_text(e) or is_photo(e)) and step(e, "do_task")))
@check_block
async def do_task3(event : events.NewMessage.Event):

    user_id = event.sender_id
    user = get_user(user_id)


    await event.client.forward_messages(ADMIN, event.message)

    admin_photo_text = f"""تسک جدید از طرف [{user.league}{user.name}] 👆
آیدی عددی : {user_id}"""
    
    await event.client.send_message(ADMIN, admin_photo_text, buttons=[[Button.inline("تایید", f"add_balance-{user.user_id}"), Button.inline("لغو", f"message_to_user-{user.user_id}")]])

    await event.respond("تسک شما ارسال شد در صورت تایید ادمین سکه به پروفایل شما اضافه میشه", buttons=start_buttons)

    STEP[str(event.sender_id)] = ("home", )
    return


@app.on(events.NewMessage(incoming=True, pattern="✅یک تسک انجام دادم✅", func=lambda e: step(e, "home")))
@check_user
@check_block
async def do_task2(event):
    
    do_task_text = """🗂مدرک تسکی که انجام دادی رو به صورت عکس بفرست

 میتونی پیام هم ارسال کنی"""

    await event.respond(do_task_text, buttons=[[Button.text("❌بازگشت❌", resize=True)]])

    STEP[str(event.sender_id)] = ("do_task", )
    return
