from telethon import events, Button
from tigerMaf import app, STEP, ADMIN
from tigerMaf.filters import step, is_text
from tigerMaf.sql_helpers import get_user, update_balance, deposit_and_withdraw
from tigerMaf.buttons import start_buttons

@app.on(events.CallbackQuery(pattern="^add_balance", func=lambda e : step(e, "home")))
async def add_balance1(event):

    decoded_data = event.data.decode("utf-8")
    split_data = decoded_data.split("-")

    if len(split_data) == 3:
        user_id = int(split_data[1])
        amount = int(split_data[2])

        update_balance(user_id, amount)

        user_text = f"✅مقدار {abs(int(amount))} سکه از طرف ادمین به پروفایل شما اضافه شد"
        admin_text = "سکه با موفقیت به پروفایل کاربر اضافه شد"
        deposit_and_withdraw(user_id, abs(int(amount)), "deposit")
        await event.respond(admin_text)
        await event.client.send_message(user_id, user_text)
        return
    
    if len(split_data) == 2:
        user_id = int(split_data[1])

        await event.respond("مقدار سکه ای که میخوای به کاربر اضافه بشه رو وارد کن", buttons=[[Button.text("❌بازگشت❌", resize=True)]])

        STEP[str(ADMIN)] = ("add_balance_get_amount", user_id)

    else:
        await event.respond("آیدی عددی یا شماره کاربر در لیست و یا نام کاربر را وارد کنید", buttons=[[Button.text("❌بازگشت❌", resize=True)]])

        STEP[str(event.sender_id)] = ("add_balance_get_user", )

    return

@app.on(events.NewMessage(incoming=True, func=lambda e : is_text(e) and step(e, "add_balance_get_amount")))
async def add_balance3(event):

    amount = event.raw_text
    target_user = STEP[str(event.sender_id)][1]

    # remove all spaces like "-  12345"
    while " " in amount:
        amount = amount.replace(" ", "")


    # Accept only numbers like +12345 or -12345 or 12345
    if not amount.isdigit() and not ((amount.startswith("-") or amount.startswith("+")) and amount[1:].isdigit()):
        await event.respond("مقدار سکه فقط میتونه عدد باشه", buttons=[[Button.text("❌بازگشت❌", resize=True)]])
        return
        
    
    update_balance(target_user, int(amount))

    if int (amount) < 0:
        user_text = f"✅مقدار {abs(int(amount))} سکه از طرف ادمین از پروفایل شما کسر شد"
        admin_text = "سکه با موفقیت از پروفایل کاربر کسر شد"
        deposit_and_withdraw(target_user, abs(int(amount)), "withdraw")
    else:
        user_text = f"✅مقدار {abs(int(amount))} سکه از طرف ادمین به پروفایل شما اضافه شد"
        admin_text = "سکه با موفقیت به پروفایل کاربر اضافه شد"
        deposit_and_withdraw(target_user, abs(int(amount)), "deposit")

    await event.respond(admin_text, buttons=start_buttons)
    await app.send_message(target_user, user_text)

    STEP[str(event.sender_id)] = ("home", )

@app.on(events.NewMessage(incoming=True, func=lambda e : is_text(e) and step(e, "add_balance_get_user")))
async def add_balance2(event):

    target_user = event.raw_text

    if target_user.isdigit():
        if len(target_user) >= 8:

            user = get_user(int(target_user))
        
        else:

            user = get_user(None, id=int(target_user))

    else:

        user = get_user(None, username=target_user)

    if not user:

        await event.respond("کاربر یافت نشد", buttons=[[Button.text("❌بازگشت❌", resize=True)]])
        return
    
    await event.respond("مقدار سکه ای که میخوای به کاربر اضافه بشه رو وارد کن", buttons=[[Button.text("❌بازگشت❌", resize=True)]])

    STEP[str(event.sender_id)] = ("add_balance_get_amount", user.user_id)

    return