from telethon import Button

start_buttons = [
    [Button.text("📨پیام خصوصی📨", resize=True), Button.text("💬پیام به کانال💬")],
    [Button.text("🎲دوئل🎲"), Button.text("❤️‍🔥لایکی❤️‍🔥"), Button.text("👤پروفایل👤")],
    [Button.text("✅لینک دعوت✅"), Button.text("🔥جایزه روزانه🔥")],
    [Button.text("👨‍💻پیام به ادمین👨‍💻"), Button.text("🔍راهنما🔎")]
]

sudo_buttons = [
    [Button.inline("آمار ربات 📊", data="statitics"), Button.inline("آمار کاربر 👥", data="user_statitics")],
    [Button.inline("بلاک/آنبلاک کاربر 🚫", data="block_unblock_user")],
    [Button.inline("پیام به کاربر 📨", data="message_to_user"), Button.inline("افزایش موجودی 💸", data="add_balance")],
    [Button.inline("پیام همگانی 📢", data="send_to_all"), Button.inline("فروارد همگانی 📨", data="forward_to_all")],
    [Button.inline("تنظیمات ربات ⚙️", data="bot_settings"), Button.inline("قفل ها 🔒", data="brodcast_locks")]
]