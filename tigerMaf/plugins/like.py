from telethon import events, Button
from tigerMaf import app, STEP
from tigerMaf.filters import step, is_private
from tigerMaf.decorators import check_user, signin_required, check_block, forced_join
from tigerMaf.sql_helpers import get_this_week_top_likes, get_user, get_like_count, like_user, get_user_daily_liked_count, check_like_user
from tigerMaf.buttons import start_buttons

@app.on(events.NewMessage(incoming=True, func=lambda e : step(e, "like_player") and is_private(e)))
@check_user
@signin_required
@check_block
@forced_join
async def like_player(event):
    
    liker_user = event.sender_id
    liked_user = event.raw_text

    if liked_user.isdigit():
        user = get_user(None, id=int(liked_user))
    else:
        user = get_user(None, name=liked_user)
    
    if not user:
        not_exist_error_message = """❌کاربر مورد نظر یافت نشد"""

        await event.respond(not_exist_error_message)
        return
    
    if not user.name:
        not_exist_error_message = """❌کاربر مورد نظر یافت نشد"""

        await event.respond(not_exist_error_message)
        return
    
    if user.user_id == liker_user:
        like_error_message = """❌شما نمیتوانید خودتان را لایک کنید"""

        await event.respond(like_error_message)
        return
    
    daily_like_count = get_user_daily_liked_count(liker_user)

    if daily_like_count >= 10:

        like_error_message = """❌لایک های شما به پایان رسیده است
        در هر روز میتوانید تا 10 نفر لایک کنید"""

        await event.respond(like_error_message)
        return
    
    if check_like_user(liker_user, user.user_id):
        like_error_message = """❌شما قبلا این کاربر را لایک کرده اید"""

        await event.respond(like_error_message)
        return

    like_user(liker_user, user.user_id)

    like_text = f"✅لایک شد\n\n{user.league} {user.name}"
    await event.respond(like_text, buttons=start_buttons)
    STEP[str(event.sender_id)] = ("home", )

    return

@app.on(events.NewMessage(incoming=True, pattern="❤️‍🔥لایکی❤️‍🔥", func=lambda e : step(e, "home") and is_private(e)))
@check_user
@signin_required
@check_block
@forced_join
async def like(event):
    
    likes_text = await this_week_likes(event)
    await event.respond(likes_text, buttons=Button.inline("نتایج هفته قبل", data="last_week_likes"))

    like_player_text = """میخوای کیو لایک کنی؟ 🤔
کد یا نامش رو بفرست و من لایکشو میزنم! 🤩
لیست کد هر کاربر 👇
/list

مثال: کد ALI_TIGER، 1 است
پس برای لایک ALI_TIGER باید کد 1 را ارسال کنی! 🔥

دکمه بازگشت 👇 رو بزن و برو سراغ کار دیگه! 👋"""
    await event.respond(like_player_text, buttons=Button.text("❌بازگشت❌", resize=True))
    STEP[str(event.sender_id)] = ("like_player", )

async def this_week_likes(event):
    this_week_likes = get_this_week_top_likes()
    user_id = event.sender_id
    user_like_count = get_like_count(user_id)

    if not this_week_likes:
        likes_text = "این هفته هیچکس لایک نشده"
    else:
        likes_text = "لایک های این هفته"

        for top_user_id, count in this_week_likes:
            user = get_user(top_user_id)
            likes_text+=f"\n{user.league}{user.name} : {count}"
        
        likes_text+=f"\n\nتعداد لایک های شما : {0 if user_like_count is None else user_like_count}"
    
    return likes_text

@app.on(events.CallbackQuery(data="last_week_likes"))
async def last_week_likes(event):
    user_id = event.sender_id
    last_week_top_likes = get_this_week_top_likes(last_week=True)
    user_like_count = get_like_count(user_id, last_week=True)

    if not last_week_top_likes:
        likes_text = "هفته پیش هیچکس لایک نشده"
    else:
        likes_text = "لایک های هفته قبل"

        for user_id, like in last_week_top_likes:
            user = get_user(user_id)
            likes_text+=f"\n{user.league}{user.name} : {like}"

        likes_text+=f"\n\nتعداد لایک های شما : {user_like_count if user_like_count is not None else 0}"

    await event.edit(likes_text, buttons=Button.inline("نتایج این هفته", data="this_week_likes"))

@app.on(events.CallbackQuery(data="this_week_likes"))
async def this_week_likes_callback(event):

    await event.edit(await this_week_likes(event), buttons=Button.inline("نتایج هفته قبل", data="last_week_likes"))
    return
