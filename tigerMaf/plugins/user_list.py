from telethon import events, Button
from tigerMaf.decorators import check_user, check_block, forced_join
from tigerMaf import app, STEP
from tigerMaf.sql_helpers import get_users_list, get_this_week_top_likes, duel_list, get_user
from tigerMaf.filters import is_private
chunks = 45

@app.on(events.NewMessage(incoming=True, pattern=r"/like\b", func=lambda e: is_private(e)))
@check_user
@check_block
@forced_join
async def showlist(event  : events.NewMessage.Event):
    
    users = get_this_week_top_likes(limit=100)

    if len(users) == 0:
        await event.respond("لیست لایک های کل خالی است")
        return
    text = "🏆لیست لایک های کل:\n\n"
    rank_emojis = {1: "🥇", 2: "🥈", 3: "🥉"}

    for rank, user_count in enumerate(users, 1):

        user_id = user_count[0]
        like_count = user_count[1]
        user = get_user(user_id)

        emoji = rank_emojis.get(rank, "")

        text += f"{emoji} {user.id} ـ {user.league}{user.name} ـ {like_count} ❤️\n"

    await event.respond(text)
    return

@app.on(events.NewMessage(incoming=True, pattern=r"/duel\b", func=lambda e: is_private(e)))
@check_user
@check_block
@forced_join
async def showlist(event  : events.NewMessage.Event):
    
    users = duel_list(week=True)

    if len(users) == 0:
        await event.respond("لیست دوئل های کل خالی است")
        return
    text = "🏆لیست دوئل های کل:\n\n"
    rank_emojis = {1: "🥇", 2: "🥈", 3: "🥉"}

    for rank, user_count in enumerate(users, 1):

        user_id = user_count[0]
        like_count = user_count[1]
        user = get_user(user_id)

        emoji = rank_emojis.get(rank, "")

        text += f"{emoji} {user.id} ـ {user.league}{user.name} ـ {like_count} ❤️\n"

    await event.respond(text)
    return

@app.on(events.NewMessage(incoming=True, pattern=r"/duell\b", func=lambda e: is_private(e)))
@check_user
@check_block
@forced_join
async def showlist(event  : events.NewMessage.Event):
    
    users = duel_list()

    if len(users) == 0:
        await event.respond("لیست دوئل های کل خالی است")
        return
    text = "🏆لیست دوئل های کل:\n\n"
    rank_emojis = {1: "🥇", 2: "🥈", 3: "🥉"}

    for rank, user_count in enumerate(users, 1):

        user_id = user_count[0]
        like_count = user_count[1]
        user = get_user(user_id)

        emoji = rank_emojis.get(rank, "")

        text += f"{emoji} {user.id} ـ {user.league}{user.name} ـ {like_count} ❤️\n"

    await event.respond(text)
    return

@app.on(events.NewMessage(incoming=True, pattern=r"/list\b", func=lambda e: is_private(e)))
@check_user
@check_block
@forced_join
async def show(event  : events.NewMessage.Event):
    text, user_count = user_list(chunks=chunks)
    if user_count > chunks:
        await event.respond(text, buttons=[[Button.inline("➡️", data=f"next_page-{2}")]])
        return
    
    await event.respond(text)
    return

@app.on(events.CallbackQuery(pattern="^next_page"))
@check_user
@check_block
@forced_join
async def next_page(event : events.CallbackQuery.Event):
    decoded_data = event.data.decode("utf-8")
    split_data = decoded_data.split("-")
    page = int(split_data[1])
    
    text, user_count = user_list(page=page, chunks=chunks)
    if page == 1:
        await event.edit(text, buttons=[[Button.inline("➡️", data=f"next_page-{page+1}")]])
        return
    if user_count > chunks * page:
        await event.edit(text, buttons=[[Button.inline("⬅️", data=f"next_page-{page-1}"), Button.inline("➡️", data=f"next_page-{page+1}")]])
        return
    
    await event.edit(text, buttons=[[Button.inline("⬅️", data=f"next_page-{page-1}")]])
    return

def user_list(page=1, chunks=45):
    
    users, user_count = get_users_list(page=page, chunks=chunks)
    if users:
        text = """لیست اعضا! 👥
افرادی که تا الان در این ربات ثبت نام کرده اند: 👇
(ببین کی‌ها عضو شدند!) 👀\n\n"""
        for user in users:
            text += f"{user.id} ـ {user.league} {user.name}\n"
        return text, user_count
