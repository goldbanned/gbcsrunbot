from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# User menu
btnSettings = KeyboardButton('⚙Настройки')
btnRedact = KeyboardButton('✏Радактировать названия')
mainUserMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnSettings, btnRedact)

# Admin menu
btnAdminPanel = KeyboardButton('🔥Админ панель')
mainAdminMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnSettings, btnRedact).row(btnAdminPanel)


# Options menu
def create_options_menu(messages):
    optionsMenu = InlineKeyboardMarkup(row_width=1)
    optionsMenu.insert(InlineKeyboardButton(messages[0], callback_data='first_message'))
    optionsMenu.insert(InlineKeyboardButton(messages[1], callback_data='second_message'))
    optionsMenu.insert(InlineKeyboardButton(messages[2], callback_data='third_message'))
    optionsMenu.insert(InlineKeyboardButton(messages[3], callback_data='fourth_message'))
    optionsMenu.insert(InlineKeyboardButton(messages[4], callback_data='fifth_message'))
    optionsMenu.insert(InlineKeyboardButton(messages[5], callback_data='show_the_coefficient'))
    return optionsMenu


def create_redact_menu(messages):
    redactMenu = InlineKeyboardMarkup(row_width=1)
    redactMenu.insert(InlineKeyboardButton(messages[0], callback_data='first_message_change'))
    redactMenu.insert(InlineKeyboardButton(messages[1], callback_data='second_message_change'))
    redactMenu.insert(InlineKeyboardButton(messages[2], callback_data='third_message_change'))
    redactMenu.insert(InlineKeyboardButton(messages[3], callback_data='fourth_message_change'))
    redactMenu.insert(InlineKeyboardButton(messages[4], callback_data='fifth_message_change'))
    return redactMenu


btnCancel = KeyboardButton('❌Отмена')
menuChangeText = ReplyKeyboardMarkup(resize_keyboard=True).row(btnCancel)
