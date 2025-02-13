from tigerMaf import app, STEP, CHANNEL, BOT_USERNAME, STEP_TIME
from telethon import events, Button
from tigerMaf.decorators import forced_join, check_user, check_block
from tigerMaf.filters import step, is_dice, is_private
from tigerMaf.sql_helpers import get_user, update_balance, add_duel, get_last_duel, get_settings
from datetime import datetime, timedelta


@app.on(events.NewMessage(incoming=True, pattern="🎲دوئل🎲", func=lambda e: step(e, "home") and is_private(e)))
@check_user
@forced_join
@check_block
async def duel(event):
	await duel_menu(event)

async def duel_menu(event, indirect = False):

	if indirect:
		duel_txt = "🏠 دوئل"
	else:
		duel_txt = """🏠شما وارد بخش دوئل شدید
تو این قسمت میتونید شرط بندی کنید
آموزش استفاده از بخش دوئل 👇
/DUEL


💎🪙
💎🪙💎🪙
💎🪙💎🪙💎🪙
💎🪙💎🪙💎🪙💎🪙"""

	await event.respond(duel_txt, buttons=[
		[Button.text("🎲🎲🎲"), Button.text("🏀🏀🏀"), Button.text("🎯🎯🎯")],
		[Button.text("❌بازگشت❌", resize=True)]
	])

	STEP[str(event.sender_id)] = ("duel_menu", )
	STEP_TIME[str(event.sender_id)] = datetime.now()
	return

@app.on(events.NewMessage(incoming=True, pattern="❌بازگشت❌", func=lambda e: (step(e, "duel_send_dice") or step(e, "duel_dice_amount")) and is_private(e)))
async def duel_back(event):
	await duel_menu(event, indirect=True)

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "duel_dice_amount") and is_private(e)))
async def duel_dice_amount(event):

	user_id = event.sender_id
	amount = event.raw_text

	if not amount.isdigit():
		not_digit_error_message = """❌ اوه، اشتباه کردی! 🤦‍♂️
عدد رو به انگلیسی بنویس، مثل این: 2
نه اینکه به فارسی بنویسی، حواست باشه! 😂"""

		await event.respond(not_digit_error_message)
		return

	user = get_user(user_id)
	if int(amount) > user.balance:

		not_enough_money_error_message = """❌ اوه، خزانه خالی! 💸
سکه‌هایت تمام شده، حالا چی کار کنی؟ 🤔
سکه بگیر با دستور 👇
/getcoin"""

		await event.respond(not_enough_money_error_message)
		return

	setting = get_settings()
	minimum_duel = setting.minimum_duel
	maximum_duel = setting.maximum_duel
	if int(amount) < minimum_duel:
		minimum_duel_coin_text = f"""❌ اوه، سکه کم داری! 💸
حداقل {minimum_duel} سکه میخواد برای شرط‌بندی، اما تو نداریش! 😂
سکه‌هایت رو افزایش بده، بعد بیا شرط‌بندی کن! 💪"""
		await event.respond(minimum_duel_coin_text)
		return
	
	if int(amount) > maximum_duel:
		maximum_duel_coin_text = f"""❌ اوه، بیش از حد شرط‌بندی کردی! 😱
حداکثر {maximum_duel} سکه میتونی شرط‌بندی کنی، اما تو بیشتر از این گذاشتی! 😂
ورودی رو کمتر کن، تا بتونی شرط‌بندی کنی! 💪"""
		await event.respond(maximum_duel_coin_text)
		return
	
	STEP[str(user_id)] = ("duel_send_dice", int(amount))
	STEP_TIME[str(event.sender_id)] = datetime.now()
	duel_text = f"""🤑 در صورت برنده شدن، {int(amount) * 1.8:2} سکه به پروفایلت اضافه میشه! 💸
و نکته‌ای که مهمه: اگر تاست عدد یک بیاد، تو برنده میشی! 🤩"""

	await event.respond(duel_text, buttons=[[Button.text("🎲")], [Button.text("❌بازگشت❌", resize=True)]])
	return

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "duel_send_dice") and is_dice(e, "🎲") and is_private(e)))
async def duel_send_dice(event):

	user_id = event.sender_id
	dice = event.message.media.emoticon
	value = event.message.media.value
	amount = STEP[str(user_id)][1]
	STEP[str(user_id)] = ("home", )
	
	if event.message.fwd_from:
		await event.respond("برو خونتون")
		return
		
	if value == 6 or value == 1:
		user = get_user(user_id)
		win_text = """💸💸💸
سکه‌هایت اضافه شد! 🤑✅
پروفایلت رو ببین و ببین چقدر ثروتمند شدی! 👀
/profile 👇"""
		channel_win_text = f"""‼️DUEL‼️

{user.league}{user.name}

⭕️بردن همه چیز نیست،🙃
⭕️ولی تمایل به بردن همه چیز است😉

🎲🎲🎲

💰ورودی:{amount}
💰خروجی:{amount*1.8:2}

🤖@{BOT_USERNAME}"""
		await event.respond(win_text)
		await event.client.send_message(CHANNEL, channel_win_text)
		update_balance(user_id, (amount * 1.8) - amount)
		add_duel(user_id, amount, dice, 1)

	else:
		lose_text = "😭 باختید! 💔"
		await event.respond(lose_text)
		update_balance(user_id, -amount)
		add_duel(user_id, amount, dice, 0)

	await duel_menu(event, indirect=True)
	return

@app.on(events.NewMessage(incoming=True, pattern="🎲🎲🎲", func=lambda e: is_private(e)))
@forced_join
@check_block
async def duel_dice(event):
	
	await event.respond("""💸 چقدر سکه میخوای روی خط بذاری؟ 🤑
چند تا سکه میخوای شرط ببندی؟ 🤔""", buttons=Button.text("❌بازگشت❌", resize=True))

	STEP[str(event.sender_id)] = ("duel_dice_amount", )
	STEP_TIME[str(event.sender_id)] = datetime.now()

	return

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "duel_basketball_amount") and is_private(e)))
async def duel_basketball_amount(event):

	user_id = event.sender_id
	amount = event.raw_text

	if not amount.isdigit():
		not_digit_error_message = """❌ اشتباه کردی! 🙅‍♂️
عدد رو به انگلیسی بنویس، مثل این: 2
نه اینکه به فارسی بنویسی، حواست باشه! 😂"""

		await event.respond(not_digit_error_message)
		return

	user = get_user(user_id)
	if int(amount) > user.balance:

		not_enough_money_error_message = """❌ خزانه خالی! 💸
سکه‌هایت تمام شده، حالا چی کار کنی؟ 🤔
سکه بگیر با دستور 👇
/getcoin"""

		await event.respond(not_enough_money_error_message)
		return

	setting = get_settings()
	minimum_duel = setting.minimum_duel
	maximum_duel = setting.maximum_duel
	if int(amount) < minimum_duel:
		await event.respond(f"""❌ کم آوردی! 💸
حداقل {minimum_duel} سکه میخواد برای شرط‌بندی، اما تو کمتر از این وارد کردی! 😂
سکه‌هایت رو افزایش بده، بعد بیا شرط‌بندی کن! 💪""")
		return
	
	if int(amount) > maximum_duel:
		await event.respond(f"""❌ زیاد آوردی! 💸
حداکثر {maximum_duel} سکه میتونی شرط‌بندی کنی، اما تو بیشتر از این گذاشتی! 😂
سکه‌هایت رو کمتر کن، تا بتونی شرط‌بندی کنی! 💪""")
		return
	
	STEP[str(user_id)] = ("duel_send_basketball", int(amount))
	STEP_TIME[str(event.sender_id)] = datetime.now()
	duel_text = f"""🤑 در صورت برنده شدن، {int(amount) * 1.8:2} سکه به پروفایلت اضافه میشه! 💸
یعنی میتونی ثروتت رو چند برابر کنی! 🤑"""

	await event.respond(duel_text, buttons=[[Button.text("🏀")], [Button.text("❌بازگشت❌", resize=True)]])
	return

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "duel_send_basketball") and is_dice(e, "🏀") and is_private(e)))
async def duel_send_dice(event):

	user_id = event.sender_id
	dice = event.message.media.emoticon
	value = event.message.media.value
	amount = STEP[str(user_id)][1]
	
	if event.message.fwd_from:
		await event.respond("برو خونتون")
		return
	
	STEP[str(user_id)] = ("home", )

	if value == 4 or value == 5:
		user = get_user(user_id)
		win_text = """🔥🔥🔥
سکه‌هایت اضافه شد! 💸✅
پروفایلت رو ببین و ببین چقدر ثروتمند شدی! 👀
/profile 👇"""
		channel_win_text = f"""‼️DUEL‼️

{user.league}{user.name}

⭕️بردن همه چیز نیست،🙃
⭕️ولی تمایل به بردن همه چیز است😉

🏀🏀🏀

💰ورودی:{amount}
💰خروجی:{amount*1.8:2}

🤖@{BOT_USERNAME}"""
		await event.respond(win_text)
		await event.client.send_message(CHANNEL, channel_win_text)
		update_balance(user_id, (amount * 1.8) - amount)
		add_duel(user_id, amount, dice, 1)

	else:
		lose_text = "😢 شکست خوردید! 💔"
		await event.respond(lose_text)
		update_balance(user_id, -amount)
		add_duel(user_id, amount, dice, 0)

	await duel_menu(event, indirect=True)
	return

@app.on(events.NewMessage(incoming=True, pattern="🏀🏀🏀", func=lambda e: is_private(e)))
@forced_join
@check_block
async def duel_basketball(event):

	user_id = event.sender_id
	last_duel = get_last_duel(user_id, "🏀")
	if last_duel:
		if datetime.now() - last_duel.date < timedelta(minutes=3):
			await event.respond("""😬 3 دقیقه صبر کن! ⏰
بعد دوباره میتونی بازی کنی و سکه‌های بیشتری ببری! 💸""")
			return
	
	await event.respond("""💸 چقدر میخوای روی خط بذاری؟ 🤑
چند تا سکه میخوای شرط ببندی؟ 💸""", buttons=Button.text("❌بازگشت❌", resize=True))

	STEP[str(event.sender_id)] = ("duel_basketball_amount", )
	STEP_TIME[str(event.sender_id)] = datetime.now()

	return

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "duel_dart_amount") and is_private(e)))
async def duel_dart_amount(event):

	user_id = event.sender_id
	amount = event.raw_text

	if not amount.isdigit():
		not_digit_error_message = """❌ اشتباه کردی! 🙅‍♂️
عدد رو به انگلیسی بنویس، مثل این: 2
نه اینکه به فارسی بنویسی، حواست باشه! 😂"""

		await event.respond(not_digit_error_message)
		return

	user = get_user(user_id)
	if int(amount) > user.balance:

		not_enough_money_error_message = """❌ خزانه خالی! 💸
سکه‌هایت تمام شده، حالا چی کار کنی؟ 🤔
سکه بگیر با دستور 👇
/getcoin و دوباره بیا شرط‌بندی کن! 💪"""

		await event.respond(not_enough_money_error_message)
		return

	setting = get_settings()
	minimum_duel = setting.minimum_duel
	maximum_duel = setting.maximum_duel
	if int(amount) < minimum_duel:
		await event.respond(f"""❌ کم آوردی! 💸
حداقل {minimum_duel} سکه میخواد برای شرط‌بندی، اما تو کمتر از این داری! 😂
سکه‌هایت رو افزایش بده، بعد بیا شرط‌بندی کن! 💪 و ببین چی میشه! 🔥""")
		return
	
	if int(amount) > maximum_duel:
		await event.respond(f"""❌ زیاد آوردی! 💸
حداکثر {maximum_duel} سکه میتونی شرط‌بندی کنی، اما تو بیشتر از این گذاشتی! 😂
سکه‌هایت رو کمتر کن! 💪""")
		return
	
	STEP[str(user_id)] = ("duel_send_dart", int(amount))
	STEP_TIME[str(event.sender_id)] = datetime.now()
	duel_text = f"""🤑 در صورت برنده شدن، {int(amount) * 1.8:2} سکه به پروفایلت اضافه میشه! 💸
یعنی میتونی ثروتت رو چند برابر کنی! 🤑
و نکته‌ای که مهمه: اگر دارتت بیرون بره، تو برنده میشی! 😎"""

	await event.respond(duel_text, buttons=[[Button.text("🎯")], [Button.text("❌بازگشت❌", resize=True)]])
	return

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "duel_send_dart") and is_dice(e, "🎯") and is_private(e)))
async def duel_send_dart(event):

	user_id = event.sender_id
	dice = event.message.media.emoticon
	value = event.message.media.value
	amount = STEP[str(user_id)][1]
	
	if event.message.fwd_from:
		await event.respond("برو خونتون")
		return
	
	STEP[str(user_id)] = ("home", )

	if value == 6 or value == 1:
		user = get_user(user_id)
		win_text = """یییییییییپ! 🎉🎉🎉
سکه‌هات اضافه شد! 💸✅
پروفایلت رو ببین و لذت ببر! 👀
/profile 👇"""
		channel_win_text = f"""‼️DUEL‼️

{user.league}{user.name}

⭕️بردن همه چیز نیست،🙃
⭕️ولی تمایل به بردن همه چیز است😉

🎯🎯🎯

💰ورودی:{amount}
💰خروجی:{amount*1.8:2}

🤖@{BOT_USERNAME}"""
		await event.respond(win_text)
		await event.client.send_message(CHANNEL, channel_win_text)
		update_balance(user_id, (amount * 1.8) - amount)
		add_duel(user_id, amount, dice, 1)

	else:
		lose_text = "😭 اوه، باختید! 💔"
		await event.respond(lose_text)
		update_balance(user_id, -amount)
		add_duel(user_id, amount, dice, 0)

	await duel_menu(event, indirect=True)
	return

@app.on(events.NewMessage(incoming=True, pattern="🎯🎯🎯", func=lambda e: is_private(e)))
@forced_join
@check_block
async def duel_dice(event):

	user_id = event.sender_id
	last_duel = get_last_duel(user_id, "🎯")
	if last_duel:
		if datetime.now() - last_duel.date < timedelta(minutes=3):
			await event.respond("""😬 3 دقیقه صبر کن! ⏰
بعد دوباره میتونی بازی کنی و سکه‌های بیشتری ببری! 💸""")
			return
	
	await event.respond("""💸 سکه‌هات رو روی میز بزار! 🤑
چند تا میخوای شرط ببندی؟ 🔥""", buttons=Button.text("❌بازگشت❌", resize=True))

	STEP[str(event.sender_id)] = ("duel_dart_amount", )
	STEP_TIME[str(event.sender_id)] = datetime.now()

	return
