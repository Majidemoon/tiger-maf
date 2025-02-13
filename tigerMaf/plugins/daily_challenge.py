from tigerMaf import app, STEP, BOT_USERNAME, CHANNEL
from telethon import events, Button
from tigerMaf.decorators import forced_join, check_user, check_block, signin_required
from tigerMaf.filters import step, is_dice, is_private
from tigerMaf.sql_helpers import (
	check_daily_broadcast_message, 
	update_balance, 
	add_daily_challenge, 
	check_daily_challenge, 
	get_user,
	get_invite_count,
	get_settings
)

win_text = """سکه‌ها ریختن از آسمان! ✨💰
پروفایلت پر از سکه شده! 🎉
برو ببین چقدر ثروتمند شدی! 👀
/profile 👇"""

@app.on(events.NewMessage(incoming=True, pattern="🔥جایزه روزانه🔥", func=lambda e: is_private(e)))
@check_user
@forced_join
@check_block
async def daily_challenge(event):
	
	await challenge_menu(event)

async def challenge_menu(event, after_game = None):

	daily_challenge_buttons  = [
		[
			Button.text("🎲🎲", resize=True),
			Button.text("🎯🎯", resize=True),
			Button.text("🎳🎳", resize=True)
		],
		[
			Button.text("🏀🏀", resize=True),
			Button.text("⚽️⚽️", resize=True),
			Button.text("🎰🎰", resize=True)
		],
		[Button.text("❌بازگشت❌")]]

	if after_game:
		await event.respond("🏠جایزه روزانه", buttons=daily_challenge_buttons)
		return
	
	daily_challenge_text = """🎲 هر روز بیا اینجا و شانستت رو امتحان کن! 🤪
اگر برنده شی، سکه‌ها مثل بارون بهت می‌ریزن! ☔️💸
شروع کن و ببین شانستت چی میگه! 😂"""
	await event.respond(daily_challenge_text, buttons=daily_challenge_buttons)

@app.on(events.NewMessage(incoming=True, pattern=r"^🎲🎲$", func=lambda e: step(e, "home") and is_private(e)))
@check_user
@forced_join
@signin_required
@check_block
async def daily_challenge_dice(event):

	user_id = event.sender_id
	user_message_check = check_daily_broadcast_message(user_id)

	if not user_message_check:

		error_text = """❌ ای دلقک! 🤡 برای تاس انداختن، اول باید یه پیام همگانی بفرستی و به همه بگویی که میخوای شانستت رو امتحان کنی! 📢🎲
دکمه پیام همگانی رو بزن و یه پیام بفرست، بعد بیا تاس بنداز و ببین شانستت چی میگه! 😆🔥"""
		
		await event.respond(error_text)
		return
	
	if check_daily_challenge(user_id, "🎲"):
		error_message = """❌ اوه، چخبرته؟! 
همین الان شانست رو امتحان کردی و حالا باید به حال خودت بزنی و تا فردا بنشینی! 😂 
تا فردا که دوباره بیای و تاس بندازی و شانستت رو امتحان کنی! 🎲🚀"""
		await event.respond(error_message)
		return
	
	STEP[str(user_id)] = ("daily_challenge_dice", )
	
	daily_challenge_buttons = Button.text("🎲", resize=True)
	
	daily_challenge_message = """🤪 هر روز یه بار بیا اینجا و تاس بنداز! 🎊 
	شاید شانست خوب باشه و برنده شی، یا شاید هم نه! 
	😂 دکمه تاس رو بزن و ببین چی میشه! 👀"""
	await event.respond(daily_challenge_message, buttons=daily_challenge_buttons)
	return
	

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "daily_challenge_dice") and is_dice(e, "🎲") and is_private(e)))
@check_user
@forced_join
@signin_required
@check_block
async def daily_challenge_dice2(event : events.NewMessage.Event):
	
	user_id = event.sender_id
	dice = event.message.media.emoticon
	value = event.message.media.value
	
	if event.message.fwd_from:
		await event.respond("برو خونتون")
		return
	
	STEP[str(user_id)] = ("home", )

	user = get_user(user_id)

	win_text_channel = f"""🎲🎲🎲

{user.league}{user.name}

تو روحت رفیق جایزه روزانه بردی🌹

🤖 @{BOT_USERNAME}"""

	add_daily_challenge(user_id, dice, value)
	
	if value == 6 or value == 1:
		await event.respond(win_text)
		setting = get_settings()
		update_balance(user_id, int(setting.daily_challenge_coin_dice))
		await event.client.send_message(CHANNEL, win_text_channel)

	else:
		await event.respond("💔باختید")
	
	await challenge_menu(event, after_game=True)

	return

@app.on(events.NewMessage(incoming=True, pattern=r"^🎯🎯$", func=lambda e: step(e, "home") and is_private(e)))
@check_user
@forced_join
@signin_required
@check_block
async def daily_challenge_dart(event):

	user_id = event.sender_id
	user_message_check = check_daily_broadcast_message(user_id)
	user_invite_count = get_invite_count(user_id, registerd=True)
	user = get_user(user_id)


	if user_invite_count < 1 and user.status < 3:

		error_text = "هی دلقک! 🤡 برای انداختن دارت، حداقل یک زیرمجموعه باید داشته باشی، نه اینکه مثل من تنها باشی و فقط به دیوار بچسبی 😂"
		
		await event.respond(error_text)
		return

	if not user_message_check:

		error_text = "هی دلقک! 🤡 برای انداختن دارت، حداقل امروز یک پیام همگانی باید بفرستی، نه اینکه مثل من فقط به خودت پیام بفرستی و جواب هم ندهی 😂! دکمه پیام همگانی رو بزن و یک پیام بفرست، شاید کسی جوابت رو بده 😆"
		
		await event.respond(error_text)
		return
	
	if check_daily_challenge(user_id, "🎯"):
		error_message = "هی دلقک! 🤡 شانس امروزت به آب ریخت! 🌊 اما نگران نباش، فردا دوباره میتونی دارت بندازی و ببینی آیا شانست عوض میشه یا نه 😂! تا فردا منتظر بمون و دوباره شانس خودت رو امتحان کن! 🤞"
		await event.respond(error_message)
		return
	
	STEP[str(user_id)] = ("daily_challenge_dart", )
	
	daily_challenge_buttons = Button.text("🎯", resize=True)
	
	daily_challenge_message = "هی دلقک! 🤡 هر روز یک بار میتونی شانست خودت رو امتحان کنی! 🎉 مثل اینه که هر روز یک بار میتونی ببینی آیا شانستت خوبه یا نه 😂! پس منتظر نباش، دکمه دارت رو بزن 👇 و ببین شانستت چی میگه! 🤔"
	await event.respond(daily_challenge_message, buttons=daily_challenge_buttons)
	return
	

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "daily_challenge_dart") and is_dice(e, "🎯") and is_private(e)))
@check_user
@forced_join
@signin_required
@check_block
async def daily_challenge_dirt2(event : events.NewMessage.Event):
	
	user_id = event.sender_id
	dice = event.message.media.emoticon
	value = event.message.media.value
	
	if event.message.fwd_from:
		await event.respond("برو خونتون")
		return

	STEP[str(user_id)] = ("home", )

	user = get_user(user_id)

	win_text_channel = f"""🎯🎯🎯

{user.league}{user.name}

تو روحت رفیق جایزه روزانه بردی🌹

🤖 @{BOT_USERNAME}"""

	add_daily_challenge(user_id, dice, value)
	
	if value == 6 or value == 1:
		await event.respond(win_text)
		setting = get_settings()
		update_balance(user_id, int(setting.daily_challenge_coin_dart))
		await event.client.send_message(CHANNEL, win_text_channel)

	else:
		await event.respond("💔باختید")
	
	await challenge_menu(event, after_game=True)

	return

@app.on(events.NewMessage(incoming=True, pattern=r"^🎳🎳$", func=lambda e: step(e, "home") and is_private(e)))
@check_user
@forced_join
@signin_required
@check_block
async def daily_challenge_bowling(event):

	user_id = event.sender_id
	user_message_check = check_daily_broadcast_message(user_id)
	user_invite_count = get_invite_count(user_id, registerd=True)
	user = get_user(user_id)

	if user_invite_count < 2 and user.status < 4:

		error_text = """هی دلقک! 🤡 
برای بولینگ انداختن، حداقل دو تا دوست دلقک باید داشته باشی که باهاش بازی کنی 🤣! 
نه اینکه مثل من تنها باشی و توپ رو به خودت پرتاب کنی 😂! 
پس دو تا زیرمجموعه ثبت نام کن و بعد بیا بولینگ بازی کن! 🏹"""
		
		await event.respond(error_text)
		return

	if not user_message_check:

		error_text = """هی دلقک! 🤡 
برای بولینگ انداختن، باید امروز حداقل یک پیام همگانی بفرستی و به همه بگویی که میخوای توپ رو پرتاب کنی 📣! 
نه اینکه مثل من فقط توپ رو پرتاب کنی و هیچکس نفهمه 😂! 
دکمه پیام همگانی رو بزن و یک پیام بفرست، شاید کسی از توپت دربیاد 😆"""
		
		await event.respond(error_text)
		return
	
	if check_daily_challenge(user_id, "🎳"):
		error_message = """هی دلقک! 🤡 
		امروز توپت به درخت خورده! 🌳 
		اما نگران نباش، فردا دوباره میتونی بولینگ بندازی و ببینی آیا شانستت عوض میشه یا نه 😂! 
		تا فردا منتظر بمون و دوباره توپ رو پرتاب کن، شاید این بار به درخت نخوره 😆"""
		await event.respond(error_message)
		return
	
	STEP[str(user_id)] = ("daily_challenge_bowling", )
	
	daily_challenge_buttons = Button.text("🎳", resize=True)
	
	daily_challenge_message = """هی دلقک! 🤡 
	هر روز یک بار میتونی توپ رو پرتاب کنی و شانستت رو امتحان کنی! 
	🎳 دکمه بولینگ رو بزن 👇 
	و ببین میتونی پین‌ها رو به زمین بکشی یا نه! 😂"""
	await event.respond(daily_challenge_message, buttons=daily_challenge_buttons)
	return
	

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "daily_challenge_bowling") and is_dice(e, "🎳") and is_private(e)))
@check_user
@forced_join
@signin_required
@check_block
async def daily_challenge_bowlnig2(event : events.NewMessage.Event):
	
	user_id = event.sender_id
	dice = event.message.media.emoticon
	value = event.message.media.value
	
	if event.message.fwd_from:
		await event.respond("برو خونتون")
		return
	
	STEP[str(user_id)] = ("home", )

	user = get_user(user_id)

	win_text_channel = f"""🎳🎳🎳

{user.league}{user.name}

تو روحت رفیق جایزه روزانه بردی🌹

🤖 @{BOT_USERNAME}"""

	add_daily_challenge(user_id, dice, value)
	
	if value == 6 or value == 2:
		await event.respond(win_text)
		setting = get_settings()
		update_balance(user_id, int(setting.daily_challenge_coin_bowling))
		await event.client.send_message(CHANNEL, win_text_channel)

	else:
		await event.respond("💔باختید")
	
	await challenge_menu(event, after_game=True)

	return

@app.on(events.NewMessage(incoming=True, pattern=r"^🏀🏀$", func=lambda e: step(e, "home") and is_private(e)))
@check_user
@forced_join
@signin_required
@check_block
async def daily_challenge_basket(event):

	user_id = event.sender_id
	user_message_check = check_daily_broadcast_message(user_id)
	user_invite_count = get_invite_count(user_id, registerd=True)
	user = get_user(user_id)

	if user_invite_count < 3 and user.status < 5:

		error_text = """❌ اوه، توپ تو دستت نیست! 🤹‍♂️ 
		برای بسکت انداختن، باید حداقل سه تا دوست دلقک داشته باشی که باهاش بازی کنی! 🤣 
		نه اینکه مثل من تنها باشی و توپ رو به خودت پرتاب کنی 😂"""
		
		await event.respond(error_text)
		return

	if not user_message_check:

		error_text = """❌ توپ تو هواست، اما تو هنوز آماده نیستی! 🤹‍♂️ 
		برای بسکت انداختن، باید امروز حداقل یک بار به همه بگویی که میخوای توپ رو بندازی! 
		📢 دکمه پیام همگانی رو بزن و یک پیام بفرست، 
		بعد بیا توپ بنداز و ببین چی میشه! 😆"""
		
		await event.respond(error_text)
		return
	
	if check_daily_challenge(user_id, "🏀"):
		error_message = """❌ اوه، توپ تو دستت بود، اما حالا باید تا فردا صبر کنی! 
		🤹‍♂️ امروز شانستت رو امتحان کردی، 
		اما فردا دوباره میتونی توپ بندازی و ببینی آیا شانستت عوض میشه یا نه! 😂 
		تا فردا، توپ رو درآورده و منتظر بمون! 👀"""
		await event.respond(error_message)
		return
	
	STEP[str(user_id)] = ("daily_challenge_basket", )
	
	daily_challenge_buttons = Button.text("🏀", resize=True)
	
	daily_challenge_message = """🏀 ایهال! 🤹‍♂️ 
	هر روز میتونی توپ رو بندازی و ببینی آیا شانستت خوبه یا نه! 🤔 
	دکمه بسکت رو بزن 👇 و ببین چی میشه! 
	شاید توپ تو بسکت بره، شاید هم به سرت بخوره! 😂"""
	await event.respond(daily_challenge_message, buttons=daily_challenge_buttons)
	return
	

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "daily_challenge_basket") and is_dice(e, "🏀") and is_private(e)))
@check_user
@forced_join
@signin_required
@check_block
async def daily_challenge_basket2(event : events.NewMessage.Event):
	
	user_id = event.sender_id
	dice = event.message.media.emoticon
	value = event.message.media.value
	
	if event.message.fwd_from:
		await event.respond("برو خونتون")
		return
	
	STEP[str(user_id)] = ("home", )

	user = get_user(user_id)

	win_text_channel = f"""🏀🏀🏀

{user.league}{user.name}

تو روحت رفیق جایزه روزانه بردی🌹

🤖 @{BOT_USERNAME}"""

	add_daily_challenge(user_id, dice, value)
	
	if value == 4 or value == 5:
		await event.respond(win_text)
		setting = get_settings()
		update_balance(user_id, int(setting.daily_challenge_coin_basketball))
		await event.client.send_message(CHANNEL, win_text_channel)

	else:
		await event.respond("💔باختید")
	
	await challenge_menu(event, after_game=True)

	return

# Dont change football emoji never in two function below ⚽
@app.on(events.NewMessage(incoming=True, pattern=r"^⚽️⚽️$", func=lambda e: step(e, "home") and is_private(e)))
@check_user
@forced_join
@signin_required
@check_block
async def daily_challenge_football(event):

	user_id = event.sender_id
	user_message_check = check_daily_broadcast_message(user_id)
	user_invite_count = get_invite_count(user_id, registerd=True)
	user = get_user(user_id)

	if user_invite_count < 4 and user.status < 6:

		error_text = """❌ اوه، توپ تو زمین نیست! 
		⚽️ برای فوتبال انداختن، باید حداقل چهار تا دوست دلقک داشته باشی که باهاش بازی کنی! 🤣 
		نه اینکه مثل من تنها باشی و توپ رو به خودت پرتاب کنی و خودت رو بزنی! 😂"""
		
		await event.respond(error_text)
		return

	if not user_message_check:

		error_text = """❌ توپ تو زمین نیست! ⚽️ 
		برای فوتبال انداختن، باید امروز حداقل یک بار به همه بگویی که میخوای توپ رو بندازی! 
		📢 دکمه پیام همگانی رو بزن و یک پیام بفرست، 
		بعد بیا توپ بنداز و ببین چی میشه! 😆"""
		
		await event.respond(error_text)
		return
	
	if check_daily_challenge(user_id, "⚽"):
		error_message = """❌ اوه، توپ تو دستت بود، 
		اما حالا باید تا فردا صبر کنی! ⚽️ 
		امروز شانستت رو امتحان کردی، 
		اما فردا دوباره میتونی توپ بندازی و ببینی آیا شانستت عوض میشه یا نه! 😂 
		تا فردا، توپ رو دربیار و منتظر بمون! 👀"""
		await event.respond(error_message)
		return
	
	STEP[str(user_id)] = ("daily_challenge_football", )
	
	daily_challenge_buttons = Button.text("⚽️", resize=True)
	
	daily_challenge_message = """⚽️ ایهال! 🤹‍♂️ 
	هر روز میتونی توپ رو بندازی و ببینی آیا شانستت خوبه یا نه! 🤔 
	دکمه فوتبال رو بزن 👇 
	و ببین چی میشه! 
	شاید توپ تو دروازه بره، شاید هم به سرت بخوره! 😂"""
	await event.respond(daily_challenge_message, buttons=daily_challenge_buttons)
	return
	

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "daily_challenge_football") and is_dice(e, "⚽") and is_private(e)))
@check_user
@forced_join
@signin_required
@check_block
async def daily_challenge_football2(event : events.NewMessage.Event):
	
	
	user_id = event.sender_id

	dice = event.message.media.emoticon
	value = event.message.media.value
	
	if event.message.fwd_from:
		await event.respond("برو خونتون")
		return
	
	STEP[str(user_id)] = ("home", )

	user = get_user(user_id)

	win_text_channel = f"""⚽️⚽️⚽️

{user.league}{user.name}

تو روحت رفیق جایزه روزانه بردی🌹

🤖 @{BOT_USERNAME}"""

	add_daily_challenge(user_id, dice, value)
	
	if value == 3 or value == 4 or value == 5:
		await event.respond(win_text)
		setting = get_settings()
		update_balance(user_id, int(setting.daily_challenge_coin_football))
		await event.client.send_message(CHANNEL, win_text_channel)

	else:
		await event.respond("💔باختید")
	
	await challenge_menu(event, after_game=True)

	return

@app.on(events.NewMessage(incoming=True, pattern=r"^🎰🎰$", func=lambda e: step(e, "home") and is_private(e)))
@check_user
@forced_join
@signin_required
@check_block
async def daily_challenge_cazino(event):

	user_id = event.sender_id
	user_message_check = check_daily_broadcast_message(user_id)
	user_invite_count = get_invite_count(user_id, registerd=True)
	user = get_user(user_id)

	if user_invite_count < 5 and user.status < 7:
		error_text = """❌برای کازینو انداختن باید حداقل پنج زیرمجموعه ثبت نام شده داشته باشید"""
		
		await event.respond(error_text)
		return

	if not user_message_check:

		error_text = """❌برای کازینو انداختن باید امروز حداقل یک پیام همگانی داده باشید
دکمه پیام همگانی رو بزنید و یک پیام بفرستید"""
		
		await event.respond(error_text)
		return
	
	if check_daily_challenge(user_id, "🎰"):
		error_message = """❌شما امروز شانستون رو امتحان کردید، فردا میتونید دوباره کازینو بندازید"""
		await event.respond(error_message)
		return
	
	STEP[str(user_id)] = ("daily_challenge_cazino", )
	
	daily_challenge_buttons = Button.text("🎰", resize=True)
	
	daily_challenge_message = """🎰هر روز میتونید یک بار شانستون رو تو این قسمت امتحان کنید
دکمه کازینو بزنید👇"""
	await event.respond(daily_challenge_message, buttons=daily_challenge_buttons)
	return
	

@app.on(events.NewMessage(incoming=True, func=lambda e: step(e, "daily_challenge_cazino") and is_dice(e, "🎰") and is_private(e)))
@check_user
@forced_join
@signin_required
@check_block
async def daily_challenge_cazino2(event : events.NewMessage.Event):
	
	
	user_id = event.sender_id

	dice = event.message.media.emoticon
	value = event.message.media.value
	
	if event.message.fwd_from:
		await event.respond("برو خونتون")
		return
	
	STEP[str(user_id)] = ("home", )

	user = get_user(user_id)

	win_text_channel = f"""🎰🎰🎰

{user.league}{user.name}

تو روحت رفیق جایزه روزانه بردی🌹

🤖 @{BOT_USERNAME}"""

	add_daily_challenge(user_id, dice, value)
	
	if value == 1 or value == 22 or value == 43 or value == 64:
		await event.respond(win_text)
		setting = get_settings()
		update_balance(user_id, int(setting.daily_challenge_coin_cazino))
		await event.client.send_message(CHANNEL, win_text_channel)

	else:
		await event.respond("💔باختید")
	
	await challenge_menu(event, after_game=True)

	return
