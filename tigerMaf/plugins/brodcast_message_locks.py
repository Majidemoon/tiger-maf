from telethon import events, Button
from tigerMaf.filters import is_sudo
from tigerMaf import app
from tigerMaf.sql_helpers import get_settings, toggle_brodcast_locks

@app.on(events.CallbackQuery(data="brodcast_locks", func=lambda e : is_sudo(e)))
async def brodcast_locks_callback(event):
    await brodcast_locks(event)

async def brodcast_locks(event):

    locks = get_settings()
    photo = locks.channel_photo_lock
    video = locks.channel_video_lock
    gif = locks.channel_gif_lock
    sticker = locks.channel_sticker_lock
    voice = locks.channel_voice_lock
    music = locks.channel_audio_lock

    locks_buttons = [
        [Button.inline("🔓✅" if photo else "🔒❌", data="channel_photo_lock"), Button.inline("📸عکس📸", data="channel_photo_lock")],
        [Button.inline("🔓✅" if video else "🔒❌", data="channel_video_lock"), Button.inline("📹ویدیو📹", data="channel_video_lock")],
        [Button.inline("🔓✅" if gif else "🔒❌", data="channel_gif_lock"), Button.inline("🖼گیف🖼", data="channel_gif_lock")],
        [Button.inline("🔓✅" if sticker else "🔒❌", data="channel_sticker_lock"), Button.inline("🗺استیکر🗺", data="channel_sticker_lock")],
        [Button.inline("🔓✅" if voice else "🔒❌", data="channel_voice_lock"), Button.inline("🎤صدا🎤", data="channel_voice_lock")],
        [Button.inline("🔓✅" if music else "🔒❌", data="channel_audio_lock"), Button.inline("🎵موزیک🎵", data="channel_audio_lock")],
        [Button.inline("بازگشت 🔙", data="sudo_panel")]
    ]
    await event.edit("🔒 | قفل های ارسال پیام به کانال", buttons=locks_buttons)


@app.on(events.CallbackQuery(pattern=r"channel_photo_lock|channel_video_lock|channel_gif_lock|channel_sticker_lock|channel_voice_lock|channel_audio_lock", func=lambda e : is_sudo(e)))
async def channel_photo_lock(event):

    locks_message = {
        "channel_photo_lock": "عکس",
        "channel_video_lock": "ویدیو",
        "channel_gif_lock": "گیف",
        "channel_sticker_lock": "استیکر",
        "channel_voice_lock": "صدا",
        "channel_audio_lock": "موزیک"
    }

    locks = get_settings()
    data = event.data.decode("UTF-8")
    if getattr(locks, data):
        answer = f"قفل {locks_message[data]} فعال شد ✅"
    else:
        answer = f"قفل {locks_message[data]} غیر فعال شد ❌"

    toggle_brodcast_locks(data)
    await event.answer(answer)
    await brodcast_locks(event)