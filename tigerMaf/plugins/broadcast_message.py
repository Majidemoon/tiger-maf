from tigerMaf import app, STEP, CHANNEL_LINK, CHANNEL, STEP_TIME, LOG_CHANNEL
from telethon import events, Button
from tigerMaf.decorators import forced_join, signin_required, check_user, check_block
from tigerMaf.filters import step, is_text, is_photo, is_media, is_video, is_gif, is_sticker, is_audio, is_voice, is_private
from tigerMaf.sql_helpers import get_user, add_message, get_settings, update_balance, get_last_channel_message
from tigerMaf.buttons import start_buttons
from datetime import datetime


@app.on(events.NewMessage(incoming=True, func=lambda e : step(e, "broadcast_message") and is_private(e)))
@check_user
@check_block
@forced_join
async def broadcast_message2(event : events.NewMessage.Event):

    user_id = event.sender_id

    user = get_user(user_id)
    settings = get_settings()

    channel_text = f"""{event.raw_text}

{user.league} {user.name}"""
    user_text = f"""✅ پیامت با موفقیت ارسال شد!

برای مشاهده پیام اینجا کلیک کن 👇
{CHANNEL_LINK}"""

    if is_text(event) and not is_media(event):
        if (len(event.raw_text) == 1) and not event.raw_text.isdigit():
            await event.respond("فرمت پیام ارسالی اشتباه است")
            return
        last_message = get_last_channel_message(user_id)
        print(last_message)
        if last_message and last_message.message and (last_message.message == event.raw_text):
            await event.respond("پیام تکراری است")
            return
        m = await event.client.send_message(CHANNEL, channel_text)
        await event.respond(user_text, buttons=start_buttons)

    elif is_photo(event):
        if settings.channel_photo_lock == 0:
            await event.respond("ارسال تصویر فعلا امکان پذیر نمیباشد")
            return

        m = await event.client.send_file(CHANNEL, event.message.photo, caption=f"{event.raw_text if event.raw_text else ''}\n\n{user.league} {user.name}")
        await event.respond(user_text, buttons=start_buttons)

    elif is_video(event):
        if settings.channel_video_lock == 0:
            await event.respond("ارسال ویدیو فعلا امکان پذیر نمیباشد")
            return

        m = await event.client.send_file(CHANNEL, event.message.video, caption=f"{event.raw_text if event.raw_text else ''}\n\n{user.league} {user.name}")
        await event.respond(user_text, buttons=start_buttons)

    elif is_gif(event):
        if settings.channel_gif_lock == 0:
            await event.respond("ارسال گیف فعلا امکان پذیر نمیباشد")
            return

        await event.client.send_file(CHANNEL, event.message.gif, caption=f"{event.raw_text if event.raw_text else ''}\n\n{user.league} {user.name}:")
        await event.respond(user_text, buttons=start_buttons)

    elif is_sticker(event):
        if settings.channel_sticker_lock == 0:
            await event.respond("ارسال استیکر فعلا امکان پذیر نمیباشد")
            return

        m = await event.client.send_file(CHANNEL, event.message.sticker)
        await event.client.send_message(CHANNEL, f"{user.league} {user.name}:")
        await event.respond(user_text, buttons=start_buttons)

    elif is_audio(event):
        if settings.channel_audio_lock == 0:
            await event.respond("ارسال موزیک فعلا امکان پذیر نمیباشد")
            return

        m = await event.client.send_file(CHANNEL, event.message.audio, caption=f"{event.raw_text if event.raw_text else ''}\n\n{user.league} {user.name}")
        await event.respond(user_text, buttons=start_buttons)

    elif is_voice(event):
        if settings.channel_voice_lock == 0:
            await event.respond("ارسال صدا فعلا امکان پذیر نمیباشد")
            return

        m = await event.client.send_file(CHANNEL, event.message.voice, caption=f"{event.raw_text if event.raw_text else ''}\n\n{user.league} {user.name}")
        await event.respond(user_text, buttons=start_buttons)
    
    else:
        await event.respond("""❌فرمت فایل ارسالی اشتباه است""")
        return

    add_message(user_id, "channel", event.raw_text if event.raw_text else "None")
    channel_link = f"https://t.me/{CHANNEL_LINK[1:]}" if CHANNEL_LINK.startswith("@") else CHANNEL_LINK
    log_text = f"""new channel message
{channel_link}/{m.id}
{user.league} {user.name}
balance : {user.balance}
id : {user.id}
name : {event.sender.first_name} {event.sender.last_name if event.sender.last_name else ''}
username : {f'@{event.sender.username}' if event.sender.username else ''}
user_id : {event.sender_id}
"""
    await app.send_message(LOG_CHANNEL, log_text, link_preview=False)
    update_balance(user_id, 0.2)

    STEP[str(user_id)] = ("home", )

    return

@app.on(events.NewMessage(incoming=True, pattern="💬پیام به کانال💬", func=lambda e : step(e, "home") and is_private(e)))
@check_user
@check_block
@forced_join
@signin_required
async def broadcast_message(event):

    user_id = event.sender_id

    user = get_user(user_id)

    if user.league == "🎗" and user.status < 2:

        broadcast_error_text = """❌ لیگ ربان نمی‌تونه پیام‌های عمومی بفرسته.

اگر فیک نیستید، به ادمین پیام بدید!"""

        await event.respond(broadcast_error_text)

        return
    
    broadcast_message_text = f"""✍🏻 پیامت رو بنویس

پیام شما به صورت خودکار در کانال 

{CHANNEL_LINK}
 ارسال میشود

تبلیغات آزاد است ولی قبلش باید 50سکه کوپن بدین 

آموزش ارسال بازی دوستانه مافیا👇

/guideline4


🎉💥
🎉💥🎉💥
🎉💥🎉💥🎉💥
🎉💥🎉💥🎉💥🎉💥"""
    
    await event.respond(broadcast_message_text, buttons=[Button.text("❌بازگشت❌", resize=True)])

    STEP[str(user_id)] = ("broadcast_message", )
    STEP_TIME[str(event.sender_id)] = datetime.now()

    return
