from telethon import events, Button
from tigerMaf import TASK_CHANNEL

async def do_task(event : events.NewMessage.Event):
    task_text = f"""🤑 تو این بخش میتونید با انجام کار های ساده سکه دریافت کنید

تسک ها در کانال 👈 
{TASK_CHANNEL}
 قرار داده شده
هر وقت هر کدوم از تسک ها رو انجام دادی برای دریافت سکه دکمه " ✅ یک تسک انجام دادم✅ " رو بزن

🔥💰
🔥💰🔥💰
🔥💰🔥💰 🔥💰
🔥💰 🔥💰 🔥💰🔥💰"""
    
    await event.respond(task_text, buttons=[
        [
            Button.text("✅یک تسک انجام دادم✅", resize=True)
        ],
        [
            Button.text("❌بازگشت❌", resize=True)
        ]
    ])