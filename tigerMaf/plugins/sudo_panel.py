from telethon import events, Button
from tigerMaf import app, STEP, ADMIN
from tigerMaf.buttons import sudo_buttons
from tigerMaf.filters import is_sudo
from tigerMaf.decorators import check_user

async def sudo_panel(event):

    if isinstance(event, events.CallbackQuery.Event):
        await event.edit("👮پنل مدیریت ربات", buttons=sudo_buttons)

    else:
        await event.respond("👮پنل مدیریت ربات", buttons=sudo_buttons)

@app.on(events.NewMessage(incoming=True, pattern="/panel", from_users=ADMIN))
@check_user
async def sudo_panel_callback(event):

    await sudo_panel(event)

@app.on(events.CallbackQuery(data="sudo_panel", func=lambda e: is_sudo(e)))
async def sudo_panel_callback(event):

    await sudo_panel(event)