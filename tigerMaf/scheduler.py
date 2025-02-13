from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from tigerMaf import app, CHANNEL, BOT_USERNAME, STEP_TIME, STEP
from tigerMaf.sql_helpers import get_this_week_top_likes, get_user, update_balance, get_settings
import asyncio
from datetime import datetime, timedelta
from tigerMaf.buttons import start_buttons

async def like_win():
    # top_liked = get_this_week_top_likes(last_week=True)
    top_liked = get_this_week_top_likes(last_week=True)

    setting = get_settings()

    users_prize = {0 : setting.like_challenge_number_one, 1 : setting.like_challenge_number_two, 2 : setting.like_challenge_number_three, 3 : setting.like_challenge_number_four}
    
    channel_text = "نفرات برتر این هفته چالش لایکی:\n\n"

    for user_count, (user_id, count) in enumerate(top_liked):
        user = get_user(user_id)
        channel_text += f"""{user_count+1}. {user.league}{user.name}: 
تعداد لایک: {count} 
جایزه: {users_prize[user_count]}\n"""
        
        update_balance(user_id, users_prize[user_count])
        try:
            await app.send_message(user_id, f"تبریک! جایزه شما: {users_prize[user_count]}")
        except:
            pass

    channel_text += f"""جایزه نفرات برتر به پروفایلشون اضافه شد
اگه توام میخوای یکی از برنده های هفته بعد ما باشی همین الان بیا ربات و لایک جمع کن

@{BOT_USERNAME}"""

    await app.send_message(CHANNEL, channel_text)

async def check_step():
    for user in list(STEP_TIME.keys()):
        now = datetime.now()
        time = STEP_TIME[user]
        if now - time > timedelta(minutes=2):
            STEP_TIME.pop(user)
            STEP[str(user)] = ("home", )
            await app.send_message(int(user), "🏠صفحه اصلی", buttons=start_buttons)


def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(like_win, CronTrigger(day_of_week="sat", hour=0, minute=0, timezone="Asia/Tehran"))
    scheduler.add_job(check_step, "interval", minutes=1)
    scheduler.start()
    return scheduler