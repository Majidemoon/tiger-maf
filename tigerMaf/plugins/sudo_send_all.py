from telethon import events, Button
from tigerMaf import app, STEP
from tigerMaf.buttons import start_buttons
from tigerMaf.decorators import check_user
from tigerMaf.filters import step, is_sudo
from tigerMaf.sql_helpers import get_users_list
import threading
from tigerMaf.utils import progress_bar

async def send_to_all_func(event, message, drop_author=True):
    page = 1
    chunks = 100
    succes = 0
    unsucces = 0
    while True:
        users, user_count = get_users_list(page=page, chunks=chunks)

        for user in users:
            try:
                await event.client.forward_messages(user.user_id, event.message, drop_author=drop_author)
                succes += 1
            except Exception as e:
                print(e)
                unsucces += 1
            
            progress = await progress_bar(succes+unsucces, user_count)
            admin_text = f"""تعداد کل کاربران : {user_count}
ارسال موفق : {succes}
ارسال ناموفق : {unsucces}
{progress}"""
            await message.edit(admin_text)

        if page * chunks > user_count:
            break
        page += 1
    
    if drop_author:
        await message.reply("ارسال همگانی با موفقیت انجام شد")
    else:
        await message.reply("فروارد همگانی با موفقیت انجام شد")

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "send_to_all")))
@check_user
async def send_to_all(event : events.NewMessage.Event):

    user_id = event.sender_id
    STEP[str(user_id)] = ("home", )

    await event.respond("در حال آماده سازی...", buttons=start_buttons)
    message = await event.respond("در حال ارسال...")

    threading.Thread(await send_to_all_func(event, message)).start()

@app.on(events.CallbackQuery(pattern="send_to_all", func=lambda e: is_sudo(e)))
@check_user
async def send_to_all2(event : events.CallbackQuery.Event):
    
    user_id = event.sender_id
    
    await event.respond("پیامت رو بفرست تا به همه بفرستم", buttons=[[Button.text("❌بازگشت❌", resize=True)]])
    STEP[str(user_id)] = ("send_to_all", )

    return

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "forward_to_all")))
@check_user
async def forward_to_all(event : events.NewMessage.Event):

    user_id = event.sender_id
    STEP[str(user_id)] = ("home", )

    await event.respond("در حال آماده سازی...", buttons=start_buttons)
    message = await event.respond("در حال ارسال...")

    threading.Thread(await send_to_all_func(event, message, drop_author=False)).start()

@app.on(events.CallbackQuery(pattern="forward_to_all", func=lambda e: is_sudo(e)))
@check_user
async def forward_to_all2(event : events.CallbackQuery.Event):
    
    user_id = event.sender_id
    
    await event.respond("پیامت رو بفرست تا به همه بفرستم", buttons=[[Button.text("❌بازگشت❌", resize=True)]])
    STEP[str(user_id)] = ("forward_to_all", )

    return