from telethon import events, Button
from tigerMaf import app, STEP
from tigerMaf.filters import is_sudo, step
from tigerMaf.sql_helpers import get_settings, updtate_settings
from tigerMaf.decorators import check_user
from tigerMaf.buttons import start_buttons


@app.on(events.CallbackQuery(data="bot_settings"))
@check_user
async def bot_settings(event):
    
    settongs = get_settings()

    settings_buttons = [
        [Button.inline(str(settongs.invite_coin), data="invite_coin"), Button.inline("سکه دعوت دوستان", data="invite_coin")],
        [Button.inline(str(settongs.like_challenge_number_one), data="like_challenge_number_one"), Button.inline("سکه نفر اول لایکی", data="like_challenge_number_one")],
        [Button.inline(str(settongs.like_challenge_number_two), data="like_challenge_number_two"), Button.inline("سکه نفر دوم لایکی", data="like_challenge_number_two")],
        [Button.inline(str(settongs.like_challenge_number_three), data="like_challenge_number_three"), Button.inline("سکه نفر سوم لایکی", data="like_challenge_number_three")],
        [Button.inline(str(settongs.like_challenge_number_four), data="like_challenge_number_four"), Button.inline("سکه نفر چهارم لایکی", data="like_challenge_number_four")],
        [Button.inline(str(settongs.daily_challenge_coin_dice), data="daily_challenge_coin_dice"), Button.inline("سکه تاس روزانه", data="daily_challenge_coin_dice")],
        [Button.inline(str(settongs.daily_challenge_coin_dart), data="daily_challenge_coin_dart"), Button.inline("سکه دارت روزانه", data="daily_challenge_coin_dart")],
        [Button.inline(str(settongs.daily_challenge_coin_bowling), data="daily_challenge_coin_bowling"), Button.inline("سکه بولینگ روزانه", data="daily_challenge_coin_bowling")],
        [Button.inline(str(settongs.daily_challenge_coin_football), data="daily_challenge_coin_football"), Button.inline("سکه فوتبال روزانه", data="daily_challenge_coin_football")],
        [Button.inline(str(settongs.daily_challenge_coin_basketball), data="daily_challenge_coin_basketball"), Button.inline("سکه بسکتبال روزانه", data="daily_challenge_coin_basketball")],
        [Button.inline(str(settongs.daily_challenge_coin_cazino), data="daily_challenge_coin_cazino"), Button.inline("سکه کازینو روزانه", data="daily_challenge_coin_cazino")],
        [Button.inline(str(settongs.maximum_duel), data="maximum_duel"), Button.inline("حداکثر ورودی دوئل", data="maximum_duel")],
        [Button.inline(str(settongs.minimum_duel), data="minimum_duel"), Button.inline("حداقل ورودی دوئل", data="minimum_duel")],
        [Button.inline(str(settongs.minimum_withdraw), data="minimum_withdraw"), Button.inline("حداقل برداشت", data="minimum_withdraw")],
        [Button.inline("بازگشت", data="sudo_panel")]
    ]

    await event.edit("تنظیمات ربات", buttons=settings_buttons)

pattern = r"""invite_coin|like_challenge_number_one|like_challenge_number_two|like_challenge_number_three|like_challenge_number_four|daily_challenge_coin_dice|daily_challenge_coin_dart|daily_challenge_coin_bowling|daily_challenge_coin_football|daily_challenge_coin_basketball|daily_challenge_coin_cazino|maximum_duel|minimum_duel|minimum_withdraw"""

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "set")))
@check_user
async def set_setting(event):

    user_id = event.sender_id
    new_value = event.raw_text
    column_name = STEP.get(str(user_id))[1]

    updtate_settings(column_name, new_value)

    await event.respond("تنظیمات با موفقیت به روز رسانی شد /panel", buttons=start_buttons)

    STEP[str(user_id)] = ("home", )



@app.on(events.CallbackQuery(pattern=pattern, func=lambda e: is_sudo(e)))
@check_user
async def bot_settings_callback(event):

    user_id = event.sender_id
    data = event.data.decode("utf-8")

    await event.respond("مقدار جدید رو بفرست", buttons=[[Button.text("بازگشت", resize=True)]])
    STEP[str(user_id)] = ("set", data)