from tigerMaf import app, BOT_USERNAME
from tigerMaf.decorators import signin_required, check_user, check_block
from telethon import events
from tigerMaf.filters import step, is_private
from tigerMaf.sql_helpers import get_invite_count


@app.on(events.NewMessage(incoming=True, pattern=r"✅لینک دعوت✅|/link", func=lambda e : step(e, "home") and is_private(e)))
@check_user
@signin_required
@check_block
async def invite_friends(event : events.NewMessage.Event):

    user_id = event.sender_id

    all_invites = get_invite_count(user_id)
    registered_invites = get_invite_count(user_id, registerd=True)

    invite_caption = f"""🔱ربات TIGER🔱

ما یک ربات مخصوص مافیا پلیر های دُهات و مافیا طراحی کردیم

قابلیت های ربات👇

⭕️پیام خصوصی: تا حالا شده بخواید به کسی که قبلا تو بازی دیدید پیام بدید ولی آیدی تلگرامش رو نداشته باشید؟ از طریق این ربات میتونید بهش پیام ارسال کنید

⭕️پیام ناشناس: میتونید پیام ناشناس به پلیر های مافیا ارسال کنید ارسال کنید👽

⭕️پیام  به کانال : پیام شما به صورت خودکار همراه با اسمتون داخل کانال فرستاده میشه و بقیه مافیا پلیر ها میتونن پیام شما رو ببینن

⭕️جایزه روزانه:هر روز میتونید یک بار شانستون رو در تاس، بولینگ، بسکتبال، فوتبال و دارت امتحان کنید و در صورت برنده شدن سکه مافیا جایزه میگیرید

⭕️دوئل : میتونید در بازی های تاس و بسکتبال, دارت شرط‌بندی کنید

در ضمن با دعوت کردن دوستاتون میتونید سکه دریافت کنید

آیدی ربات تایگر👇
https://t.me/{BOT_USERNAME}?start={user_id}

🔥❤️‍🔥
🔥❤️‍🔥🔥❤️‍🔥
🔥❤️‍🔥🔥❤️‍🔥🔥❤️‍🔥
🔥❤️‍🔥🔥❤️‍🔥🔥❤️‍🔥🔥❤️‍🔥"""
    
    invite_text = """این بنر اختصاصی شماست👆

هر کسی که با لینک اختصاصی شما وارد ربات بشه برای شما یک رفرال اضافه میشه و هر رفرال برابر است با 2 سکه

⭕️نکته: وقتی کاربری با لینک دعوت شما وارد ربات میشه برای شما پیام ارسال میشه، و زمانی که اون کاربر ثبت نام کنه برای شما کوپن سکه ارسال میشه

⭕️نکته: کسایی که دعوت میکنید باید حداقل 1000 امتیاز داشته باشند یعنی حداقل این لیگ💫

🪙💎
🪙💎🪙💎
🪙💎🪙💎🪙💎
🪙💎🪙💎🪙💎🪙💎"""

    invite_text2 = f"""👤تعداد افرادی که تا الان با لینک شما وارد ربات شدن:
{all_invites} نفر

👤تعداد افرادی که تا الان با لینک شما وارد ربات شدن و ثبت نام کردند:
{registered_invites} نفر"""
    
    await app.send_file(user_id, "tigerMaf/files/invite/invite.jpg", caption=invite_caption)
    await event.respond(invite_text)
    await event.respond(invite_text2)
    return
