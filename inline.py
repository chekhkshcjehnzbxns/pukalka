from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


Choice = CallbackData("choice", "name")
EditCallback = CallbackData("edit", "num")


def choice_game_keyboard():
	markup = InlineKeyboardMarkup(row_width=3)
	button1 = InlineKeyboardButton(
		text="🔫 Standoff 2",
		callback_data=Choice.new(name="standoff")
	)
	button2 = InlineKeyboardButton(
		text="🌟 Brawl Stars",
		callback_data=Choice.new(name="brawl")
	)
	button3 = InlineKeyboardButton(
		text="🔥 Free Fire",
		callback_data=Choice.new(name="freefire")
	)
	button4 = InlineKeyboardButton(
		text="🌴 Pubg Mobile",
		callback_data=Choice.new(name="pubg")
	)
	button5 = InlineKeyboardButton(
		text="🌀 Roblox",
		callback_data=Choice.new(name="roblox")
	)
	button6 = InlineKeyboardButton(
		text="🚓 Blitz Mobile",
		callback_data=Choice.new(name="blitz")
	)
	button7 = InlineKeyboardButton(
		text="👑 Clash Royale",
		callback_data=Choice.new(name="clash")
	)
	button8 = InlineKeyboardButton(
		text="👧 Avakin Live",
		callback_data=Choice.new(name="avakin")
	)
	button9 = InlineKeyboardButton(
		text="💃 Fortnite",
		callback_data=Choice.new(name="fortnite")
	)
	button10 = InlineKeyboardButton(
		text="🏜️ Minecraft",
		callback_data=Choice.new(name="minecraft")
	)
	button11 = InlineKeyboardButton(
		text="🏘️ Black Russia",
		callback_data=Choice.new(name="blackru")
	)
	markup.add(
		button1, button2,
		button3, button4,
		button5, button6,
		button7, button8,
		button9, button10,
		button11
	)
	return markup


def num_keyboard():
	markup = InlineKeyboardMarkup()
	button1 = InlineKeyboardButton(
		text="1️⃣",
		callback_data=EditCallback.new(num="1")
	)
	button2 = InlineKeyboardButton(
		text="2️⃣",
		callback_data=EditCallback.new(num="2")
	)
	button3 = InlineKeyboardButton(
		text="3️⃣",
		callback_data=EditCallback.new(num="3")
	)
	markup.add(button1, button2, button3)
	
	button4 = InlineKeyboardButton(
		text="4️⃣",
		callback_data=EditCallback.new(num="4")
	)
	button5 = InlineKeyboardButton(
		text="5️⃣",
		callback_data=EditCallback.new(num="5")
	)
	button6 = InlineKeyboardButton(
		text="6⃣",
		callback_data=EditCallback.new(num="6")
	)
	markup.add(button4, button5, button6)
	
	button7 = InlineKeyboardButton(
		text="7⃣",
		callback_data=EditCallback.new(num="7")
	)
	button8 = InlineKeyboardButton(
		text="8⃣",
		callback_data=EditCallback.new(num="8")
	)
	button9 = InlineKeyboardButton(
		text="9⃣",
		callback_data=EditCallback.new(num="9")
	)
	markup.add(button7, button8, button9)
	
	back = InlineKeyboardButton(
		text="◀️",
		callback_data="back"
	)
	button0 = InlineKeyboardButton(
		text="0⃣",
		callback_data=EditCallback.new(num="0")
	)
	markup.add(back, button0)
	return markup
	

yesno_keyboard = InlineKeyboardMarkup().add(
	InlineKeyboardButton("✅ Да", callback_data="yes"),
	InlineKeyboardButton("❌ Нет", callback_data="no")
)

