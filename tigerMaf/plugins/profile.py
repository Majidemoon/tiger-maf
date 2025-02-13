from telethon import events, Button
from tigerMaf import app, STEP, ADMIN, MAFIA_GAME_BOT_USERNAME
from tigerMaf.sql_helpers import get_user, get_last_deposit_and_withdraw, update_balance, deposit_and_withdraw, get_like_count, get_settings, duel_count
from tigerMaf.decorators import check_user, check_block
from tigerMaf.filters import step, is_text, is_private
from tigerMaf.buttons import start_buttons
from datetime import datetime

@app.on(events.NewMessage(incoming=True, pattern=r"👤پروفایل👤|/profile", func=lambda e: is_private(e)))
@check_user
@check_block
async def profile(event):
    user_id = event.sender_id

    user = get_user(user_id)
    likes = get_like_count(user_id)
    last_week_likes = get_like_count(user_id, last_week=True)
    all_duel = duel_count(user_id)
    week_duel = duel_count(user_id, week=True)
    win_duel = duel_count(user_id, type="win")
    lose_duel = duel_count(user_id, type="lose")

    profile_text = f"""👤نام: {user.league}{user.name}

🆔آیدی عددی: {user_id}

💰سکه: {user.balance:2}

❤️لایک ها: {0 if likes is None else likes}
❤️لایک های هفته گذشته: {0 if last_week_likes is None else last_week_likes}

📝کد کاربر: {user.id} 

دوئل کل: {all_duel}
دوئل هفتگی: {week_duel}
برد: {win_duel}
باخت: {lose_duel}

🔥💥
🔥💥🔥💥
🔥💥🔥💥🔥💥"""
    
    await event.respond(profile_text, buttons=[
        [
            Button.inline("برداشت سکه", data="withdraw"),
            Button.inline("واریز سکه", data="deposit")
        ]
    ])

@app.on(events.CallbackQuery(data="withdraw", func=lambda e : step(e, "home")))
@check_block
async def withdraw(event):
    user_id = event.sender_id

    last_withdraw = get_last_deposit_and_withdraw(user_id, "withdraw")
    if last_withdraw:
        last_withdraw_date = last_withdraw.date
        if last_withdraw_date.date() == datetime.today().date():
            await event.respond("""💸 فقط یه بار در روز میتونی برداشت کنی! 📆
بعد از اون دیگه نمی‌تونی برداشت کنی، باید صبر کنی تا فردا! """)
            return
    
    withdraw_text = """💸 چقدر میخوای از حسابت برداشت کنی؟ 🤑
توجه کن که فقط یه بار در روز میتونی این کار رو بکنی! ⏰
پس فکر کن و تصمیم بگیر! 🔥"""

    await event.respond(withdraw_text, buttons=[[Button.text("❌بازگشت❌", resize=True)]])

    STEP[str(user_id)] = ("withdraw", )
    return

@app.on(events.NewMessage(incoming=True, func=lambda e : is_text(e) and step(e, "withdraw") and is_private(e)))
@check_block
async def withdraw2(event):
    amount = event.raw_text
    user_id = event.sender_id

    if not amount.isdigit():
        await event.respond("تعداد سکه باید عدد باشه", buttons=[[Button.text("❌بازگشت❌", resize=True)]])
        return
    
    settings = get_settings()
    minimum_withdraw = settings.minimum_withdraw
    if int(amount) < minimum_withdraw:
        await event.respond(f"❌حداقل برداشت {minimum_withdraw} سکه است", buttons=[[Button.text("❌بازگشت❌", resize=True)]])
        return
    
    user = get_user(user_id)
    if int(amount) > user.balance:
        await event.respond("❌عدم موجودی کافی", buttons=[[Button.text("❌بازگشت❌", resize=True)]])
        return
    
    update_balance(user_id, -int(amount))
    deposit_and_withdraw(user_id, int(amount), "withdraw")
    
    await event.respond("""✅ درخواستت ثبت شد! 📝
کوپن سکه‌ات هم بزودی میاد! 📨
منتظر باش و کوپنت رو دریافت کن! 😊""", buttons=start_buttons)
    await app.send_message(ADMIN, f"""درخواست برداشت سکه
[ {user.league}{user.name} ]
تعداد سکه: {amount}
آیدی عددی: {user_id}""",   
        buttons=Button.inline("ارسال کوپن", data=f"message_to_user-{user_id}"))

    STEP[str(user_id)] = ("home", )
    return

@app.on(events.CallbackQuery(data="deposit", func=lambda e : step(e, "home")))
@check_block
async def deposit(event):
    user_id = event.sender_id
    
    deposit_text = f"""کوپن سکه رو بفرست! 📨
با دستور createcoupen در منوی ربات مافیا ({MAFIA_GAME_BOT_USERNAME}) میتونی کوپن سکه درست کنی! 🔧
اما حواست باشه که کوپن رو درست بفرستی، نه اینکه چیزی دیگه بفرستی! 😂
کوپن باید حداقل 10 سکه باشه! 🔥"""

    await event.respond(deposit_text, buttons=[[Button.text("❌بازگشت❌", resize=True)]])

    STEP[str(user_id)] = ("deposit", )

@app.on(events.NewMessage(incoming=True, func=lambda e : is_text(e) and step(e, "deposit") and is_private(e)))
@check_block
async def deposit2(event):
    withdraw_text2 = """صبر کن! 🕰️
ادمین زودتر آنلاین میشه و کوپنت رو چک میکنه! 👀
اگر کوپنت معتبر باشه، سکه‌ات اضافه میشه! 💸
منتظر بمون! 😊"""

    await event.respond(withdraw_text2, buttons=start_buttons)

    user_id = event.sender_id
    user = get_user(user_id)

    admin_text = f"""درخواست واریز سکه

نام بازی: {user.league} {user.name}
نام: {event.sender.first_name} {event.sender.last_name if event.sender.last_name else ""}
آیدی عددی: {user_id}
نام کاربری: {"@" + event.sender.username if event.sender.username else "ندارد"}
کوپن: {event.raw_text}"""
    
    await app.send_message(ADMIN, admin_text, buttons=[[Button.inline("تایید واریز", data=f"add_balance-{user_id}"), Button.inline("لغو", data=f"cancel_deposit-{user_id}")]])

    STEP[str(user_id)] = ("home", )

@app.on(events.CallbackQuery(pattern="^cancel_deposit"))
async def cancel_deposit(event):
    
    decoded_data = event.data.decode("utf-8")
    split_data = decoded_data.split("-")
    user_id = int(split_data[1])

    await event.respond("درخواست لغو شد", buttons=[[Button.inline("ارسال دلیل لغو به کاربر", data=f"send_reason-{user_id}")]])

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "send_cancel_reason") and is_text(e) and is_private(e)))
async def send_reason2(event : events.NewMessage.Event):

    target_user = STEP[str(event.sender_id)][1]

    STEP[str(event.sender_id)] = ("home", )

    admin_message_text = f"""🚨پیام جدید از طرف مدیریت🚨
    
🚫درخواست واریز سکه شما به دلیل زیر لغو شد🚫

{event.raw_text}"""

    await app.send_message(target_user, admin_message_text, buttons=[[Button.inline("👨‍💻پیام به ادمین👨‍💻", data="message_to_admin")]])
    await event.respond("پیام ارسال شد", buttons=start_buttons)

@app.on(events.CallbackQuery(pattern="^send_reason"))
async def send_reason(event):

    decoded_data = event.data.decode("utf-8")
    split_data = decoded_data.split("-")
    user_id = int(split_data[1])

    send_reason_text = "دلیل لغو رو بنویس تا به کاربر ارسال بشه"

    await event.respond(send_reason_text, buttons=[[Button.text("❌بازگشت❌", resize=True)]])

    STEP[str(event.sender_id)] = ("send_cancel_reason", user_id)

