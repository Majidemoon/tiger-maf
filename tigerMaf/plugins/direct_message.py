from telethon import events, Button
from tigerMaf.decorators import forced_join, signin_required, check_user, check_block
from tigerMaf import app, STEP, STEP_TIME
from tigerMaf.filters import step, is_text, is_private
from tigerMaf.sql_helpers import get_user, get_ubu, ubu, add_message
from tigerMaf.buttons import start_buttons
from datetime import datetime
from telethon.errors import UserIsBlockedError, InputUserDeactivatedError, MessageTooLongError

direct_message_text = """📩کد یا نام گیرنده پیام رو بفرست، اما حواست باشه! 🤔

لیست کد هر کاربر 👇
/list

آموزش ویدئویی پیام فرستادن 👇
/guideline2

آموزش ارسال بازی دوستانه مافیا 👇
/guideline4

⭕️مثال: با توجه به لیست بالا مثلا کد ALI_TIGER، 1 است
پس برای ارسال پیام به ALI_TIGER میتونی کد 1 یا نامش رو بنویسی، هر دوتا درسته! 😊

برای خروج از دکمه بازگشت استفاده کن 👇، تا دوباره به صفحه قبل برگردی! 👈"""
    

@app.on(events.NewMessage(incoming=True, func=lambda e : is_text(e) and step(e, "send_direct_message") and is_private(e)))
@check_user
async def send_direct_message(event):
    message = event.raw_text
    target_user = int(STEP[str(event.sender_id)][1])
    message_type = int(STEP[str(event.sender_id)][2])
    sender_user = get_user(event.sender_id)

    if message_type == 1:
        message_text = f"""👽 اوه، یک پیام ناشناس رسید! 🤐
متن پیام 👀

{message}

یه نفر ناشناس پیام فرستاده، اما من نمیگم کی بوده! 🤫"""
    
    else:
        message_text = f"""📬 خبر خوب! 📨 یه پیام خصوصی رسید! 🤫
از طرف [ {sender_user.league}{sender_user.name} ] 🤔
متن پیام 👀

{message}

یه دوست یا شاید یه دشمن! 😜 پیام فرستاده، حالا ببین چی میگه! 😁"""
        
    if STEP[str(event.sender_id)][2] == 1:
        is_annonymous = 1
    else:
        is_annonymous = 0

    try:
        await app.send_message(target_user, message_text, buttons=[[Button.inline("✍️پاسخ", f"answer_to_direct_message-{sender_user.user_id}-{is_annonymous}"), Button.inline("⛔️بلاک/آنبلاک❎", f"block_unblock_ubu-{sender_user.user_id}")]])
        STEP[str(event.sender_id)] = ("home", )

    except UserIsBlockedError:
        STEP[str(event.sender_id)] = ("home", )
        user = get_user(target_user)
        user_isblocked_text = f"متاسفانه {user.league}{user.name} ربات رو حذف کرده و نمیتونیم بهش پیام بدیم🫠"
        await event.respond(user_isblocked_text, buttons=start_buttons)
        return
    
    except InputUserDeactivatedError:
        STEP[str(event.sender_id)] = ("home", )
        user = get_user(target_user)
        user_deactiveded_text = f"متاسفانه {user.league}{user.name} دیلیت اکانت زده و نمیتونیم بهش پیام بدیم🫠"
        await event.respond(user_deactiveded_text, buttons=start_buttons)
        return
    
    except MessageTooLongError:
        msg_too_long_text = "متاسفانه تعداد کاراکتر های پیام بیشتر از حد مجاز است!"
        await event.respond(msg_too_long_text, buttons=start_buttons)
    
    add_message(event.sender_id, "annonymous" if is_annonymous else "direct", event.raw_text, target_user)
    await event.respond("پیام شما با موفقیت ارسال شد ✅ و الان در حال پرواز به سمت مقصد است! 📨✈️", buttons=start_buttons)

@app.on(events.NewMessage(incoming=True, pattern="^(?!.*/list)(?!.*/guideline2)(?!.*/guideline4)", func=lambda e : is_text(e) and step(e, "get_user_id_or_name") and is_private(e)))
@check_block
async def get_user_id_or_name(event):
    
    message_to = event.raw_text

    if message_to.isdigit():
        target_user = get_user(None, id=int(message_to))
    else :
        target_user = get_user(None, name=message_to)

    if not target_user:

        user_not_found_text = """❌ اوه، نام رو اشتباه وارد کردی! 🤦‍♂️
لطفا آموزش ویدیویی پیام خصوصی فرستادن رو ببین 👀
/guideline2

⭕️نکته: یادت باشه که لیگ رو کنار اسم نزنی، فقط نام رو بنویس! 😊"""

        await event.respond(user_not_found_text)
        return
    
    is_bloced_by_target_user = get_ubu(target_user.user_id, event.sender_id)

    if is_bloced_by_target_user:
        if not is_bloced_by_target_user.status:
            block_message = """❌ اوه، بلاک شدی! 🚫
این کاربر تو رو بلاک کرده، حالا دیگه نمیتونی بهش پیام بفرستی! 😂"""
            await event.respond(block_message, buttons=start_buttons)
            STEP[str(event.sender_id)] = ("home", )
            return

    direct_message_text2 = f"""📮پیام مورد نظر برای ارسال به [ {target_user.league}{target_user.name} ] را بفرست
اما حواست باشه که پیامت ناشناس نیست، اسم و رسمت معلومه! 😜
پیامت رو بفرست و منتظر جوابش باش! 📨"""
        
    await event.respond(direct_message_text2, buttons=[[Button.inline("حالت پیام رو عوض کن! 🔀", data="change_message_type")]])

    STEP[str(event.sender_id)] = ("send_direct_message", target_user.user_id, 0) # 1 = annonymous
    STEP_TIME[str(event.sender_id)] = datetime.now()

@app.on(events.NewMessage(incoming=True, pattern="📨پیام خصوصی📨", func=lambda e : step(e, "home") and is_private(e)))
@check_user
@forced_join
@signin_required
@check_block
async def direct_message(event):

    user_id = event.sender_id

    await event.respond(direct_message_text, buttons=[[Button.text("❌بازگشت❌", resize=True)]])

    STEP[str(user_id)] = ("get_user_id_or_name", )
    STEP_TIME[str(event.sender_id)] = datetime.now()

@app.on(events.CallbackQuery(pattern="^change_message_type", func=lambda e : step(e, "send_direct_message")))
@check_block
async def change_message_type(event : events.CallbackQuery.Event):

    message_type = STEP[str(event.sender_id)][2]
    target_user = STEP[str(event.sender_id)][1]

    not_anonymous_text = "پیامت به صورت عادی ارسال میشه! 😊"
    annoymous_text = """حالت ناشناس فعال شد! 🤫
پیامت به صورت ناشناس ارسال میشه و کسی نمی دونه کی فرستاد! 😎"""

    orginal_message = await event.get_message()

    if message_type == 1:
        STEP[str(event.sender_id)] = ("send_direct_message", target_user, 0) # 0 = not annonymous
        message_text = orginal_message.raw_text.replace(annoymous_text, not_anonymous_text)

    else:
        STEP[str(event.sender_id)] = ("send_direct_message", target_user, 1)
        message_text = orginal_message.raw_text.replace(not_anonymous_text, annoymous_text)

    await event.edit(message_text, buttons=[[Button.inline("حالت پیام رو عوض کن! 🔀", data="change_message_type")]])

@app.on(events.CallbackQuery(pattern="^answer_to_direct_message"))
@check_block
async def answer_to_direct_message(event : events.CallbackQuery.Event):

    decoded_data = event.data.decode('utf-8')
    splited_data = decoded_data.split("-")
    target_user = splited_data[1]
    is_annonymous = int(splited_data[2])

    is_bloced_by_target_user = get_ubu(target_user, event.sender_id)

    if is_bloced_by_target_user:
        if not is_bloced_by_target_user.status:
            block_message = """"❌ اوه، بلاک شدی! 🚫
این کاربر تو رو بلاک کرده، حالا دیگه نمیتونی بهش پیام بفرستی! 😂"""
            await event.respond(block_message, buttons=start_buttons)
            STEP[str(event.sender_id)] = ("home", )
            return

    if is_annonymous == 1:
        direct_message_answer_text = "پیامت به صورت ناشناس ارسال میشه، هیچکس نمی دونه کی فرستاد! 😉"
    else:
        direct_message_answer_text = "پیامت با اسم و مشخصاتت ارسال میشه! 😊"
    
    direct_message_answer_text2 = f"""✍️ جواب رو بنویس! 📝
پاسخ به پیام رو اینجا بنویس و بفرست 👇

{direct_message_answer_text}"""
        
    await event.respond(direct_message_answer_text2, buttons=[[Button.inline("حالت پیام رو عوض کن! 🔀", data="change_message_type")], [Button.inline("❌بازگشت❌", data="home")]])

    STEP[str(event.sender_id)] = ("send_direct_message", target_user, is_annonymous) # 1 = annonymous

@app.on(events.CallbackQuery(pattern="^block_unblock_ubu"))
@check_block
async def block_unblock_ubu(event : events.CallbackQuery.Event):

    decoded_data = event.data.decode('utf-8')
    
    target_user = decoded_data.split("-")[1]

    is_blocked = ubu(event.sender_id, target_user)

    if is_blocked == "blocked":
        block_message = """"⛔️ اوه، بلاک شد! 😂
این کاربر دیگه نمیتونه بهت پیام بفرسته، حالا میتونی در آرامش باشی! 😊"""
        unblock_message = """"✅ اوه، آزادی! 🎉
این کاربر از بلاک دراومد، حالا میتونه دوباره بهت پیام بفرسته، حواست باشه! 😜"""
        await event.respond(block_message)
    else:
        await event.respond(unblock_message)
