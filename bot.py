import logging
from threading import Thread
import requests
from aiogram import Bot, Dispatcher, executor, types
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import os
import config
import markups as nav
from db import Database
from selenium.webdriver.chrome.service import Service


# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
db = Database('db.db')

# parser
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--mute-audio")
options.binary_location = os.environ.get('GOOGLE_CHROME_SHIM', None)
driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=options)


def generate_message(messages, user_id):
    user = db.get_user_by_id(user_id)
    new_message = []
    for i in range(len(messages)):
        if user[i + 3] == 1:
            new_message.append(messages[i] + '🟢')
        else:
            new_message.append(messages[i] + '🔴')
    if db.get_status_by_id(user_id) == 1:
        new_message.append('Показать коэффициент🟢')
    else:
        new_message.append('Показать коэффициент🔴')
    return new_message


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id, 'Crash\nDouble\nTriple\nQuadro\nAce')
            await bot.send_message(message.from_user.id, 'Добро пожаловать!', reply_markup=nav.mainUserMenu)
        else:
            if message.from_user.id == config.ADMIN_ID:
                await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=nav.mainAdminMenu)
            else:
                await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=nav.mainUserMenu)
        db.update_open_menu('main_menu', message.from_user.id)


def sendall(count, cf):
    users = db.get_users()
    for row in users:
        try:
            if row[3 + count - 1] == 1:
                if db.get_status_by_id(row[1]) == 1:
                    requests.get(
                        f"https://api.telegram.org/bot{config.API_TOKEN}/sendMessage?chat_id={row[1]}&text={db.get_all_words_by_id(row[1]).split()[count - 1]} - {cf}x")
                else:
                    requests.get(
                        f"https://api.telegram.org/bot{config.API_TOKEN}/sendMessage?chat_id={row[1]}&text={db.get_all_words_by_id(row[1]).split()[count - 1]}")
                if int(row[1]) != 1:
                    db.set_active(row[1], 1)
        except:
            db.set_active(row[1], 0)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == '⚙Настройки':
        await bot.send_message(message.from_user.id, 'Ваши настройки:',
                               reply_markup=nav.create_options_menu(
                                   generate_message(db.get_all_words_by_id(message.from_user.id).split(),
                                                    message.from_user.id)))
        db.update_open_menu('settings_menu', message.from_user.id)
    elif message.text == '◀Главное меню':
        if message.from_user.id == config.ADMIN_ID:
            await bot.send_message(message.from_user.id, 'Перемещаемся в главное меню...',
                                   reply_markup=nav.mainAdminMenu)
        else:
            await bot.send_message(message.from_user.id, 'Перемещаемся в главное меню...',
                                   reply_markup=nav.mainUserMenu)
        db.update_open_menu('main_menu', message.from_user.id)
    elif message.text == '✏Радактировать названия':
        await bot.send_message(message.from_user.id, 'Сообщения для изменения:',
                               reply_markup=nav.create_redact_menu(
                                   generate_message(db.get_all_words_by_id(message.from_user.id).split(),
                                                    message.from_user.id)))
        db.update_open_menu('redact_menu', message.from_user.id)
    elif message.text == '❌Отмена':
        await bot.send_message(message.from_user.id, 'Изменение текста оменено!',
                               reply_markup=nav.mainUserMenu)
        db.update_open_menu('main_menu', message.from_user.id)
        db.update_change_text(None, message.from_user.id)
    elif db.get_open_menu_by_id(message.from_user.id) == 'change_text' and db.get_change_text_by_id(
            message.from_user.id) is not None:
        await bot.send_message(message.from_user.id, 'Вы успешно изменили название сообщения!',
                               reply_markup=nav.mainAdminMenu)
        db.update_open_menu('main_menu', message.from_user.id)
        db.update_words_by_id(message.from_user.id, db.get_all_words_by_id(message.from_user.id).split(),
                              db.get_change_text_by_id(message.from_user.id), message.text)


@dp.callback_query_handler(text='first_message')
async def first_call(callback: types.CallbackQuery):
    if db.get_status_setting('first_setting', callback.from_user.id) == 1:
        db.update_status_setting('first_setting', callback.from_user.id, 0)
    else:
        db.update_status_setting('first_setting', callback.from_user.id, 1)
    await callback.message.edit_reply_markup(reply_markup=nav.create_options_menu(
        generate_message(db.get_all_words_by_id(callback.from_user.id).split(), callback.from_user.id)))


@dp.callback_query_handler(text='second_message')
async def first_call(callback: types.CallbackQuery):
    if db.get_status_setting('second_setting', callback.from_user.id) == 1:
        db.update_status_setting('second_setting', callback.from_user.id, 0)
    else:
        db.update_status_setting('second_setting', callback.from_user.id, 1)
    await callback.message.edit_reply_markup(reply_markup=nav.create_options_menu(
        generate_message(db.get_all_words_by_id(callback.from_user.id).split(), callback.from_user.id)))


@dp.callback_query_handler(text='third_message')
async def first_call(callback: types.CallbackQuery):
    if db.get_status_setting('third_setting', callback.from_user.id) == 1:
        db.update_status_setting('third_setting', callback.from_user.id, 0)
    else:
        db.update_status_setting('third_setting', callback.from_user.id, 1)
    await callback.message.edit_reply_markup(reply_markup=nav.create_options_menu(
        generate_message(db.get_all_words_by_id(callback.from_user.id).split(), callback.from_user.id)))


@dp.callback_query_handler(text='fourth_message')
async def first_call(callback: types.CallbackQuery):
    if db.get_status_setting('fourth_setting', callback.from_user.id) == 1:
        db.update_status_setting('fourth_setting', callback.from_user.id, 0)
    else:
        db.update_status_setting('fourth_setting', callback.from_user.id, 1)
    await callback.message.edit_reply_markup(reply_markup=nav.create_options_menu(
        generate_message(db.get_all_words_by_id(callback.from_user.id).split(), callback.from_user.id)))


@dp.callback_query_handler(text='fifth_message')
async def first_call(callback: types.CallbackQuery):
    if db.get_status_setting('fifth_setting', callback.from_user.id) == 1:
        db.update_status_setting('fifth_setting', callback.from_user.id, 0)
    else:
        db.update_status_setting('fifth_setting', callback.from_user.id, 1)
    await callback.message.edit_reply_markup(reply_markup=nav.create_options_menu(
        generate_message(db.get_all_words_by_id(callback.from_user.id).split(), callback.from_user.id)))


@dp.callback_query_handler(text='first_message_change')
async def first_call(callback: types.CallbackQuery):
    await callback.message.answer('Отправьте в чат текст для нового сообщения:', reply_markup=nav.menuChangeText)
    db.update_change_text(0, callback.from_user.id)
    db.update_open_menu('change_text', callback.from_user.id)


@dp.callback_query_handler(text='second_message_change')
async def first_call(callback: types.CallbackQuery):
    await callback.message.answer('Отправьте в чат текст для нового сообщения:', reply_markup=nav.menuChangeText)
    db.update_change_text(1, callback.from_user.id)
    db.update_open_menu('change_text', callback.from_user.id)


@dp.callback_query_handler(text='third_message_change')
async def first_call(callback: types.CallbackQuery):
    await callback.message.answer('Отправьте в чат текст для нового сообщения:', reply_markup=nav.menuChangeText)
    db.update_change_text(2, callback.from_user.id)
    db.update_open_menu('change_text', callback.from_user.id)


@dp.callback_query_handler(text='fourth_message_change')
async def first_call(callback: types.CallbackQuery):
    await callback.message.answer('Отправьте в чат текст для нового сообщения:', reply_markup=nav.menuChangeText)
    db.update_change_text(3, callback.from_user.id)
    db.update_open_menu('change_text', callback.from_user.id)


@dp.callback_query_handler(text='fifth_message_change')
async def first_call(callback: types.CallbackQuery):
    await callback.message.answer('Отправьте в чат текст для нового сообщения:', reply_markup=nav.menuChangeText)
    db.update_change_text(4, callback.from_user.id)
    db.update_open_menu('change_text', callback.from_user.id)


@dp.callback_query_handler(text='show_the_coefficient')
async def first_call(callback: types.CallbackQuery):
    if db.get_status_by_id(callback.from_user.id) == 1:
        db.update_status_by_id(callback.from_user.id, 0)
    else:
        db.update_status_by_id(callback.from_user.id, 1)
    await callback.message.edit_reply_markup(reply_markup=nav.create_options_menu(
        generate_message(db.get_all_words_by_id(callback.from_user.id).split(), callback.from_user.id)))


def start_parsing():
    driver.get('https://csgorun.gg/')
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'switcher__content')))
    driver.find_element(By.CLASS_NAME, 'switcher__content').click()
    last_element = driver.find_element(By.CLASS_NAME, 'graph-label').get_attribute("href")
    last_element = int(last_element[last_element.rfind('/') + 1::])
    count = 0
    while True:
        if last_element != int(driver.find_element(By.CLASS_NAME, 'graph-label').get_attribute("href")[
                               driver.find_element(By.CLASS_NAME, 'graph-label').get_attribute("href").rfind(
                                   '/') + 1::]):
            last_element += 1
        WebDriverWait(driver, 10000).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="/games/' + str(last_element + 1) + '"]')))
        element = driver.find_element(By.XPATH, '//a[@href="/games/' + str(last_element + 1) + '"]')
        if 0 <= float(element.text[:-1]) <= 1.19:
            count += 1
            sendall(count, float(element.text[:-1]))
        else:
            count = 0
        last_element += 1


if __name__ == '__main__':
    Thread(target=start_parsing, args=[]).start()
    executor.start_polling(dp)
