from telethon import events, Button
from tigerMaf import app, MAFIA_GAME_BOT_ID, ADMIN, MAFIA_GAME_BOT_USERNAME
from tigerMaf.filters import forward_check, is_private
import re
import emoji
from tigerMaf.sql_helpers import update_user_name_and_league, check_name, get_user, get_settings
from tigerMaf.decorators import check_user, check_block

signup_text1 = f"""برای ثبت نام باید پروفایل مافیا خود را فقط فقط از ربات زیر فوروارد کنید👇

{MAFIA_GAME_BOT_USERNAME}"""
signup_error_name_used = """❌نام  قبلا توسط کاربری اشغال شده است
لطفا نام را تغییر داده و دوباره تلاش کنید"""

@app.on(events.NewMessage(incoming=True, pattern="^• نام شما:", func=lambda e: forward_check(e) and is_private(e)))
@check_user
@check_block
async def signup(event : events.NewMessage.Event):
    
    # Filter messages that forwarded from other bots
    if event.fwd_from.from_id.user_id != MAFIA_GAME_BOT_ID:
        await event.respond(signup_text1)
        return

    # re patterns for name and league
    name_pattern = r'• نام شما:\s*(.*?)\n'
    league_pattern1 = r'• لیگ:\s*(.*?)\n'
    league_pattern2 = r'لیگ فعلی:\s*(.*?)\n'
    score_pattern = r'• امتیاز:\s*(.*?)\n'

    user_id = event.sender_id

    name_match = re.search(name_pattern, event.raw_text)
    score_match = re.search(score_pattern, event.raw_text)
    league_match = re.search(league_pattern2, event.raw_text)
    # if not first league mathch, search for second
    if not league_match:
        league_match = re.search(league_pattern1, event.raw_text)

    name = name_match.group(1)
    score = score_match.group(1)
    if not name:    #if name not found return invalid name
        await event.respond("نام نامعتبر است")
        return
    
    if not check_name(name, user_id):
        await event.respond(signup_error_name_used)
        return
    
    raw_league = league_match.group(1)

    # extract emoji from string
    league = [char for char in raw_league if char in emoji.EMOJI_DATA][0]

    user = get_user(user_id)
    if user and (not user.name) and user.invited_by and int(score) >= 1000:
        inviter_user = get_user(user.invited_by)
        text = f"""یییییییییپ! 🎉
کاربری که دعوت کردی، ثبت نام کرد! 👍
حالا منتظر باش تا ادمین تاییدش کنه، بعد سکه‌ات اضافه میشه! 💸
شما دعوت کردی، او ثبت نام کرد، حالا نوبت سکه هاست! 😊"""
        
        admin_text = f"""دعوت جدید به ربات
دعوت کننده : 
آیدی عددی : {inviter_user.user_id}
{inviter_user.game_profile}

دعوت شونده :
آیدی عددی : {user.user_id}
{event.raw_text}"""

        await app.send_message(int(user.invited_by), text)
        friend_coin = get_settings().invite_coin
        await app.send_message(ADMIN, admin_text, buttons=[[Button.inline("تایید", f"add_balance-{user.invited_by}-{friend_coin}"), Button.inline("لغو", f"message_to_user-{user.invited_by}")]])

    if league == "🎗":
        status = 2
    else:
        status = 1
    
    update_user_name_and_league(user_id, name, league, game_profile=event.raw_text, status=status)

    successful_signup_text = f"""یییییییییپ! 🎉
نام شما با موفقیت ثبت شد! ✅
نام شما: {name} 👋

لیست دوستانت که تا الان ثبت نام کردند 👇
/list

و یادت باشه که اگر اسم یا لیگت رو تغییر دادی، دوباره پروفایلت رو فوروارد کن تا اطلاعاتت آپدیت بشه! 🔁"""

    await event.respond(successful_signup_text)

