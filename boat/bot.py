import telebot
import datetime
from methods import normmetod, coolmetod
from telebot import types
from db import Database
import os


bot = telebot.TeleBot('6428199674:AAGrSeMbj9wIXmXAdYgdozVZaw5A2pD2wiE')
bot_nickname = 'yvs_exchange_bot'
user_dict = {}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "Database.db")
db = Database(db_path)

class User:
    def __init__(self):
        self.image = None
        self.payment = None
        self.address = None
        self.cur = None
        self.sum_out = None
        self.sum_in = None
        self.check = False
        self.type_check = None
        self.lastlottery = None
        self.lottery_check = False
        self.discount = 0
        self.hash = None
        self.bank_card = None
        self.refbonus = 0
        self.referalusecheck = False
        self.discountusecheck = False


class Bankcards:
    def __init__(self):
        self.tink = db.get_bankcard('chng_tink')
        self.sber = db.get_bankcard('chng_sber')
        self.qiwi = db.get_bankcard('chng_qiwi')
        self.sbp = db.get_bankcard('chng_sbp')
        self.crypto = db.get_bankcard('chng_crypto')


rekv = Bankcards()


def dateoutput(secs):
    if secs >= 86400:
        days = secs // 86400
        secs -= days*86400
        hours = secs // 3600
        secs -= hours*3600
        mins = secs // 60
        secs -= mins*60
        return f"До следующей лотереи осталось {days} дней, {hours} часов, {mins} минут, {secs} секунд"
    elif secs >=3600:
        hours = secs // 3600
        secs -= hours * 3600
        mins = secs // 60
        secs -= mins * 60
        return f"До следующей лотереи осталось {hours} часов, {mins} минут, {secs} секунд"
    elif secs >= 60:
        mins = secs // 60
        secs -= mins * 60
        return f"До следующей лотереи осталось {mins} минут, {secs} секунд"
    else:
        return f"До следующей лотереи осталось {secs} секунд"


def is_number(sstr):
    try:
        float(sstr)
        return True
    except ValueError:
        return False


def start_menu():
    return types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton(text='❇️ Купить', callback_data='buy'),
            types.InlineKeyboardButton(text='🔻 Продать', callback_data='sell')],
        [types.InlineKeyboardButton(text='🔂 Наличный обмен', callback_data='change')],
        [types.InlineKeyboardButton(text='🎰 Лотерея', callback_data='jackpot')],
        [types.InlineKeyboardButton(text='🫂 Отзывы', callback_data='review')],
        [types.InlineKeyboardButton(text='🆘 Помощь/связь', callback_data='help')],
        [types.InlineKeyboardButton(text='ℹ️ Инфо', callback_data='info')],
        [types.InlineKeyboardButton(text='🔗 Реферальная ссылка', callback_data='ref')]])


def returnbutton():
    keyb = types.InlineKeyboardMarkup()
    key_calc = types.InlineKeyboardButton(text='↪️ Вернуться на главную', callback_data='return')
    keyb.add(key_calc)
    return keyb


def addreturnbutton(keyboard):
    keyboard.add(types.InlineKeyboardButton(text='↪️ Вернуться на главную', callback_data='return'))
    return keyboard


def discbonusaccept(userid, messageid, check = True):
    keyboard = types.InlineKeyboardMarkup()
    if user_dict[userid].type_check == 'buy':
        keyboard.add(types.InlineKeyboardButton(text='Подтвердить', callback_data='to_photo'))
        if user_dict[userid].discount > 0:
            keyboard.add(types.InlineKeyboardButton(text='Использовать скидку', callback_data='discount'))
        if db.get_refbalance(userid) >= 500:
            keyboard.add(
                types.InlineKeyboardButton(text='Использовать реферальный баланс', callback_data='ref_discount'))
        keyboard = addreturnbutton(keyboard)
        if check:
            bot.edit_message_text(chat_id=userid, message_id=messageid,
                                  text="Подтвердите правильность введенных вами данных\n" +
                                       f"Адрес кошелька - {user_dict[userid].address}\n"
                                       f"Cумма к оплате - {user_dict[userid].sum_in} RUB\n"
                                       f"Получаемая сумма - {user_dict[userid].sum_out} {user_dict[userid].cur}\n"
                                       f"Cпособ оплаты - {user_dict[userid].payment}\n", reply_markup=keyboard)
        else:
            bot.send_message(userid, text="Подтвердите правильность введенных вами данных\n" +
                                          f"Адрес кошелька - "
                                          f"{user_dict[userid].address}\nCумма к оплате - {user_dict[userid].sum_in} RUB\n"
                                          f"Получаемая сумма - {user_dict[userid].sum_out} {user_dict[userid].cur}\n"
                                          f"Cпособ оплаты - {user_dict[userid].payment}\n",
                             reply_markup=keyboard)
    elif user_dict[userid].type_check == 'sell':
        keyboard.add(types.InlineKeyboardButton(text='Подтвердить', callback_data='to_ref'))
        if user_dict[userid].discount > 0:
            keyboard.add(types.InlineKeyboardButton(text='Использовать скидку', callback_data='discount'))
        elif db.get_refbalance(userid) >= 500:
            keyboard.add(
                types.InlineKeyboardButton(text='Использовать реферальный баланс', callback_data='ref_discount'))
        keyboard = addreturnbutton(keyboard)
        if check:
            bot.edit_message_text(chat_id=userid, message_id=messageid,
                                  text="Подтвердите правильность введенных вами данных\n" +
                                       f"Адрес кошелька - "
                                       f"{user_dict[userid].address}\n Реквизиты для выплаты - {user_dict[userid].bank_card}\n"
                                       f"Cумма к оплате - {user_dict[userid].sum_in} {user_dict[userid].cur}\n"
                                       f"Получаемая сумма - {user_dict[userid].sum_out} RUB\n"
                                       f"Cпособ оплаты - {user_dict[userid].payment}\n",
                                  reply_markup=keyboard)
        else:
            bot.send_message(userid,
                             text="Подтвердите правильность введенных вами данных\n" +
                                  f"Адрес кошелька - "
                                  f"{user_dict[userid].address}\n"
                                  f"Реквизиты для выплаты -  {user_dict[userid].bank_card}\n"
                                  f"Cумма к оплате - {user_dict[userid].sum_in} {user_dict[userid].cur}\n"
                                  f"Получаемая сумма - {user_dict[userid].sum_out} RUB\n"
                                  f"Cпособ оплаты - {user_dict[userid].payment}\n",
                             reply_markup=keyboard)


def calculator_normmetod(message):
    if is_number(message.text):
        if user_dict[message.chat.id].type_check == 'buy':
            if float(message.text) >= 500:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='Продолжить', callback_data='to_payment'))
                keyboard = addreturnbutton(keyboard)
                user_dict[message.chat.id].sum_in = float(message.text)
                user_dict[message.chat.id].refbonus = round((user_dict[message.chat.id].sum_in / 98.0) * 0.35, 2)
                user_dict[message.chat.id].sum_out = normmetod(user_dict[message.chat.id].cur,
                                                             user_dict[message.chat.id].sum_in, 'buy')
                if user_dict[message.chat.id].cur == "USDT":
                    user_dict[message.chat.id].sum_out = round(user_dict[message.chat.id].sum_out, 4)
                else:
                    user_dict[message.chat.id].sum_out = round(user_dict[message.chat.id].sum_out, 6)
                bot.send_message(message.from_user.id,
                                 text=f'По текущему курсу это будет {str(user_dict[message.chat.id].sum_out)} '
                                      f'{user_dict[message.chat.id].cur}', reply_markup=keyboard)
            else:
                mesg = bot.send_message(message.from_user.id, text="Введенная сумма слишком маленькая, повторите ввод")
                bot.register_next_step_handler(mesg, calculator_normmetod)
        elif user_dict[message.chat.id].type_check == 'sell':
            currency = normmetod(user_dict[message.chat.id].cur, 1, 'sell')
            if float(message.text) * currency >= 500:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='Продолжить', callback_data='to_payment'))
                keyboard = addreturnbutton(keyboard)
                user_dict[message.chat.id].sum_in = float(message.text)
                user_dict[message.chat.id].sum_out = round(float(message.text) * currency, 2)
                user_dict[message.chat.id].refbonus = round((user_dict[message.chat.id].sum_out / 98.0) * 0.35, 2)
                bot.send_message(message.from_user.id,
                                 text=f'По текущему курсу это будет {str(user_dict[message.chat.id].sum_out)} RUB',
                                 reply_markup=keyboard)
            else:
                mesg = bot.send_message(message.from_user.id, text="Введенная сумма слишком маленькая, повторите ввод")
                bot.register_next_step_handler(mesg, calculator_normmetod)
    else:
        mesg = bot.send_message(message.from_user.id, text="Введите корректное число")
        bot.register_next_step_handler(mesg, calculator_normmetod)


def calculator_coolmetod(message):
    if is_number(message.text):
        if user_dict[message.chat.id].type_check == 'buy':
            if float(message.text) >= 500:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='Продолжить', callback_data='to_payment'))
                keyboard = addreturnbutton(keyboard)
                user_dict[message.chat.id].sum_in = float(message.text)
                user_dict[message.chat.id].refbonus = round((user_dict[message.chat.id].sum_in/98.0)*0.35, 2)
                user_dict[message.chat.id].sum_out = round(coolmetod(user_dict[message.chat.id].cur,
                                                             user_dict[message.chat.id].sum_in, 'buy'), 4)
                bot.send_message(message.from_user.id, text=f'По текущему курсу это будет {str(user_dict[message.chat.id].sum_out)} {user_dict[message.chat.id].cur}', reply_markup=keyboard)
            else:
                mesg = bot.send_message(message.from_user.id, text="Введенная сумма слишком маленькая, повторите ввод")
                bot.register_next_step_handler(mesg, calculator_coolmetod)
        elif user_dict[message.chat.id].type_check == 'sell':
            currency = coolmetod(user_dict[message.chat.id].cur, 1, 'sell')
            if float(message.text) * currency >= 500:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='Продолжить', callback_data='to_payment'))
                keyboard = addreturnbutton(keyboard)
                user_dict[message.chat.id].sum_in = float(message.text)
                user_dict[message.chat.id].sum_out = round(float(message.text) * currency, 2)
                user_dict[message.chat.id].refbonus = round((user_dict[message.chat.id].sum_out/98.0) * 0.35
                                                            , 2)
                bot.send_message(message.from_user.id,
                                 text=f'По текущему курсу это будет {str(user_dict[message.chat.id].sum_out)} RUB',
                                 reply_markup=keyboard)
            else:
                mesg = bot.send_message(message.from_user.id, text="Введенная сумма слишком маленькая, повторите ввод")
                bot.register_next_step_handler(mesg, calculator_coolmetod)
    else:
        mesg = bot.send_message(message.from_user.id, text="Введите корректное число")
        bot.register_next_step_handler(mesg, calculator_coolmetod)


def to_bank_card(message):
    user_dict[message.chat.id].bank_card = message.text
    mesg = bot.send_message(message.chat.id,
                                 text='💳 Введите адрес кошелька, с которого вы собираетесь отправлять средства')
    bot.register_next_step_handler(mesg, to_address)


def to_address(message):
    user_dict[message.chat.id].address = message.text
    discbonusaccept(message.chat.id, message.id, False)


def checkphoto(message):
    keyboard = returnbutton()
    if message.photo is None:
        mesg = bot.send_message(message.chat.id, 'Это не фотография!')
        bot.register_next_step_handler(mesg, checkphoto)
    else:
        raw = message.photo[-1].file_id
        name = raw + ".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(name, 'wb') as new_file: new_file.write(downloaded_file)
        img = open(name, 'rb')
        user_dict[message.chat.id].image = img
        if user_dict[message.chat.id].type_check == 'buy':
            bot.send_message(message.chat.id,
                         text=' ✨Спасибо за покупку! Ждем вас снова', reply_markup=keyboard)
            bot.send_message(-1001832491440, text=f"Адрес кошелька - {user_dict[message.chat.id].address}\n"
                                         f"Cумма к оплате - {user_dict[message.chat.id].sum_in} RUB\n"
                                         f"Получаемая сумма - {user_dict[message.chat.id].sum_out} {user_dict[message.chat.id].cur}\n"
                                         f"Cпособ оплаты - {user_dict[message.chat.id].payment}\nИмя пользователя - @{message.chat.username}\n"
                f"ID пользователя - {message.chat.id}")
        else:
            bot.send_message(message.chat.id,
                                 text="Спасибо!", reply_markup=keyboard)
            bot.send_message(-1001832491440, text=f"Адрес кошелька - {user_dict[message.chat.id].address}\n"
                                            f"Cумма к оплате - {user_dict[message.chat.id].sum_in} {user_dict[message.chat.id].cur}\n"
                                            f"Получаемая сумма - {user_dict[message.chat.id].sum_out} RUB\n"
                                            f"Cпособ оплаты - {user_dict[message.chat.id].payment}\nИмя пользователя - @{message.chat.username}\n"
                f"ID пользователя - {message.chat.id}")
        bot.send_photo(-1001832491440, user_dict[message.chat.id].image)
        img.close()
        os.remove(name)
        keyb = types.InlineKeyboardMarkup()
        keyb.add(types.InlineKeyboardButton(text='Подвердить', callback_data='add_ref_bonuses'))
        bot.send_message(-1001832491440, f'Подтвердите выполнение заказа \n ID - '
                                    f'{message.chat.id} \nБонус - {user_dict[message.chat.id].refbonus}', reply_markup=keyb)

def checkhash(message):
    user_dict[message.chat.id].hash = message.text
    bot.send_message(message.chat.id,
                        text="Спасибо!", reply_markup=returnbutton())
    bot.send_message(-1001832491440, text=f"Адрес кошелька - {user_dict[message.chat.id].address}\n"
                f"Cумма к оплате - {user_dict[message.chat.id].sum_in} {user_dict[message.chat.id].cur}\n"
                f"Получаемая сумма - {user_dict[message.chat.id].sum_out} RUB\n"
                f"Cпособ выплаты - {user_dict[message.chat.id].payment}\n"
                f"Хэш транзакции - {user_dict[message.chat.id].hash}\nИмя пользователя - @{message.chat.username}\n"
                f"ID пользователя - {message.chat.id}")
    keyb = types.InlineKeyboardMarkup()
    keyb.add(types.InlineKeyboardButton(text='Подвердить', callback_data='add_ref_bonuses'))
    bot.send_message(-1001832491440, f'Подтвердите выполнение заказа \n ID - '
                                f'{message.chat.id} \nБонус - {user_dict[message.chat.id].refbonus}',
                     reply_markup=keyb)


def xchangecity_input(message):
    bot.send_message(-1001832491440, text=f"Заявка на наличный обмен\n"
                                     f"Город - {message.text}\nID пользователя - @{message.chat.username}")
    bot.send_message(chat_id=message.chat.id, text="💌 Ожидайте, с вами свяжется в ближайшее время менеджер",
                          reply_markup=returnbutton())


def set_tink(message):
    db.set_bankcard('chng_tink', message.text)
    bot.send_message(chat_id=message.chat.id, text="Реквизиты успешно изменены", reply_markup=start_menu())


def set_sber(message):
    db.set_bankcard('chng_sber', message.text)
    bot.send_message(chat_id=message.chat.id, text="Реквизиты успешно изменены", reply_markup=start_menu())


def set_qiwi(message):
        db.set_bankcard('chng_qiwi', message.text)
        bot.send_message(chat_id=message.chat.id, text="Реквизиты успешно изменены", reply_markup=start_menu())


def set_sbp(message):
    db.set_bankcard('chng_sbp', message.text)
    bot.send_message(chat_id=message.chat.id, text="Реквизиты успешно изменены", reply_markup=start_menu())


def set_btc(message):
    db.set_bankcard('chng_btc', message.text)
    bot.send_message(chat_id=message.chat.id, text="Реквизиты успешно изменены", reply_markup=start_menu())


def set_usdt(message):
    db.set_bankcard('chng_usdt', message.text)
    bot.send_message(chat_id=message.chat.id, text="Реквизиты успешно изменены", reply_markup=start_menu())


def set_eth(message):
    db.set_bankcard('chng_eth', message.text)
    bot.send_message(chat_id=message.chat.id, text="Реквизиты успешно изменены", reply_markup=start_menu())


def set_trx(message):
    db.set_bankcard('chng_trx', message.text)
    bot.send_message(chat_id=message.chat.id, text="Реквизиты успешно изменены", reply_markup=start_menu())


def set_xmr(message):
    db.set_bankcard('chng_xmr', message.text)
    bot.send_message(chat_id=message.chat.id, text="Реквизиты успешно изменены", reply_markup=start_menu())


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            referer_id = str(message.text[7:])
            if referer_id:
                if referer_id != str(message.from_user.id):
                    db.add_user(message.from_user.id, referer_id)
                    try:
                        bot.send_message(referer_id, 'По Вашей ссылке зарегистрировался новый пользователь')
                        bot.send_message(message.from_user.id, "Вы успешно зарегистрировались по реферальной ссылке")
                    except:
                        pass
                else:
                    bot.send_message(message.from_user.id, "Нельзя регистрироваться по собственной реферальной ссылке")
            else:
                db.add_user(message.from_user.id)
        bot.send_message(message.from_user.id, text="Выберите действие", reply_markup=start_menu())


@bot.message_handler(commands=['configrekv'])
def get_text_commands(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Тинькофф', callback_data='chng_tink'))
    keyboard.add(types.InlineKeyboardButton(text='Сбербанк', callback_data='chng_sber'))
    keyboard.add(types.InlineKeyboardButton(text='Киви', callback_data='chng_qiwi'))
    keyboard.add(types.InlineKeyboardButton(text='СБП', callback_data='chng_sbp'))
    keyboard.add(types.InlineKeyboardButton(text='BTC', callback_data='chng_btc'))
    keyboard.add(types.InlineKeyboardButton(text='USDT', callback_data='chng_usdt'))
    keyboard.add(types.InlineKeyboardButton(text='ETH', callback_data='chng_eth'))
    keyboard.add(types.InlineKeyboardButton(text='TRX', callback_data='chng_trx'))
    keyboard.add(types.InlineKeyboardButton(text='XMR', callback_data='chng_xmr'))
    keyboard = addreturnbutton(keyboard)
    bot.send_message(message.from_user.id, "Выберите реквизиты, которые нужно поменять", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['buy', 'sell', 'change', 'review', 'help', 'info', 'jackpot', 'ref'])
def callback_start(call):
    if call.message.chat.id not in user_dict.keys():
        user_dict[call.message.chat.id] = User()
    if call.data == "buy" or call.data == "sell":
        user_dict[call.message.chat.id].type_check = call.data
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='USDT', callback_data='USDT'))
        keyboard.add(types.InlineKeyboardButton(text='BTC', callback_data='BTC'))
        keyboard.add(types.InlineKeyboardButton(text='ETH', callback_data='ETH'))
        keyboard.add(types.InlineKeyboardButton(text='TRX', callback_data='TRX'))
        keyboard.add(types.InlineKeyboardButton(text='XMR', callback_data='XMR'))
        keyboard = addreturnbutton(keyboard)
        if call.data == "buy":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text="☑️ Выберите валюту, которую Вы хотите купить:", reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text="☑️ Выберите валюту, которую вы хотите продать:", reply_markup=keyboard)
    elif call.data == 'change':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Москва', callback_data='msk'))
        keyboard.add(types.InlineKeyboardButton(text='Санкт-Петербург', callback_data='spb'))
        keyboard.add(types.InlineKeyboardButton(text='Казань', callback_data='kzn'))
        keyboard.add(types.InlineKeyboardButton(text='Другой город', callback_data='oth'))
        keyboard = addreturnbutton(keyboard)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="🏪 Выберите город:",
                              reply_markup=keyboard)
    elif call.data == 'review':
        keyboard = returnbutton()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text="📨Будем рады любым комментариям и пожеланиям по работе сервиса\n\n@yvs_review - опыт наших клиентов",
                              reply_markup=keyboard)
    elif call.data == 'info':
        keyboard = returnbutton()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
            text="ℹ️ Информационный раздел\n\n🤖 @yvs_exchange_bot - первый полуавтоматический бот - "
                "обменник с низким курсом и возможностью выбора оплаты/продажи НАЛИЧНЫМИ\n"
                "🔄️ Обмены в 2 стороны - как продаёт, так и скупает.\n🧸 Бесплатный розыгрыш скидочных "
                 "купонов каждые 72ч\n\nДругие наши проекты - @yvs_adapter", reply_markup=keyboard)
    elif call.data == 'help':
        keyboard = returnbutton()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
            text="🆘 Вы зашли в раздел помощь\n\nВ данном разделе, Вы можете связаться напрямую и выбрать"
            " другие монеты для приобретения не указанные в самом боте\n"
        "⚠️ ВАЖНО! По вопросам оплаты в случае, если Вы ошиблись с суммой перевода можете сразу звонить!\n☎️ @yvs99",
                              reply_markup=keyboard)
    elif call.data == 'jackpot':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Испытать удачу', callback_data='ludik'))
        keyboard = addreturnbutton(keyboard)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text="🎰 Лотерея\n\nℹ️ В данном разделе Вы можете испытать удачу и получить купон!\n"
                                   "🍀 Возможность испытать удачу приняв участие в разделе «Лотерея» проводится раз в 72ч",
                              reply_markup=keyboard)
    elif call.data == 'ref':
        keyboard = returnbutton()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f"🔗 Ваша реферальная ссылка \n"
                                   f"https://t.me/{bot_nickname}?start={call.message.chat.id}\n"
                                   f"Ваш баланс - {db.get_refbalance(call.message.chat.id)}",
                              reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'ludik')
def callback_roll(call):
    current_time = datetime.datetime.now()
    if user_dict[call.message.chat.id].lastlottery is None:
        if user_dict[call.message.chat.id].lottery_check:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Вы получили скидку 100 RUB", reply_markup=returnbutton())
            user_dict[call.message.chat.id].discount = 100
            user_dict[call.message.chat.id].lottery_check = False
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text="Вы получили скидку 50 RUB", reply_markup=returnbutton())
            user_dict[call.message.chat.id].discount = 50
            user_dict[call.message.chat.id].lottery_check = True
        user_dict[call.message.chat.id].lastlottery = current_time
    elif (current_time - user_dict[call.message.chat.id].lastlottery).total_seconds() >= 259200:
        if user_dict[call.message.chat.id].lottery_check:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Вы получили скидку 100 RUB", reply_markup=returnbutton())
            user_dict[call.message.chat.id].discount = 100
            user_dict[call.message.chat.id].lottery_check = False
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text="Вы получили скидку 50 RUB", reply_markup=returnbutton())
            user_dict[call.message.chat.id].discount = 50
            user_dict[call.message.chat.id].lottery_check = True
        user_dict[call.message.chat.id].lastlottery = current_time
    else:
        diff = int((current_time - user_dict[call.message.chat.id].lastlottery).total_seconds())
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=dateoutput(259200 - diff), reply_markup=returnbutton())


@bot.callback_query_handler(func=lambda call: call.data == 'return')
def callback_return(call):
    if call.data == "return":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Выберите действие", reply_markup=start_menu())


@bot.callback_query_handler(func=lambda call: call.data in ['msk', 'spb', 'kzn', 'oth'])
def callback_city(call):
    id = call.message.chat.username
    if call.data == "msk":
        bot.send_message(-1001832491440, text= f"Заявка на наличный обмен\n"
                                          f"Город - Москва\nID пользователя - @{id}")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text="💌 Ожидайте, с вами свяжется в ближайшее время менеджер",
                              reply_markup=returnbutton())
    elif call.data == "spb":
        bot.send_message(-1001832491440, text= f"Заявка на наличный обмен\n"
                                          f"Город - Санкт-Петербург\nID пользователя - @{id}")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text="💌 Ожидайте, с вами свяжется в ближайшее время менеджер",
                              reply_markup=returnbutton())
    elif call.data == "kzn":
        bot.send_message(-1001832491440, text=f"Заявка на наличный обмен\n"
                                         f"Город - Казань\nID пользователя - @{id}")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text="💌 Ожидайте, с вами свяжется в ближайшее время менеджер",
                              reply_markup=returnbutton())
    else:
        mesg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Введите город")
        bot.register_next_step_handler(mesg, xchangecity_input)


@bot.callback_query_handler(func=lambda call: call.data in ["USDT", "BTC", "ETH", "TRX", "XMR"])
def callback_currency(call):
    user_dict[call.message.chat.id].cur = call.data
    if user_dict[call.message.chat.id].type_check == 'buy':
        mesg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                     text=f"💱 На какую сумму Вы хотите купить {user_dict[call.message.chat.id].cur}?"
                                          f"\n(Минимальная сумма покупки от 500₽)")
    elif user_dict[call.message.chat.id].type_check == 'sell':
        mesg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                     text=f"💱 Сколько {user_dict[call.message.chat.id].cur} Вы хотите продать?"
                                          f"\n(Минимальная сумма продажи от 500₽)")
    if call.data in ["USDT", "BTC", "ETH"]:
        bot.register_next_step_handler(mesg, calculator_normmetod)
    else:
        bot.register_next_step_handler(mesg, calculator_coolmetod)


@bot.callback_query_handler(func=lambda call: call.data == "to_payment")
def callback_payment(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='🟨 Тинькофф', callback_data='to_address_tink'))
    keyboard.add(types.InlineKeyboardButton(text='🟩 Сбербанк', callback_data='to_address_sber'))
    keyboard.add(types.InlineKeyboardButton(text='🟧 Qiwi', callback_data='to_address_qiwi'))
    keyboard.add(types.InlineKeyboardButton(text='🔳 СБП', callback_data='to_address_sbp'))
    keyboard = addreturnbutton(keyboard)
    if user_dict[call.message.chat.id].type_check == 'buy':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Выберите способ оплаты",
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Выберите способ выплаты",
                              reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ["to_address_tink", "to_address_sber", "to_address_qiwi", "to_address_sbp"])
def callback_currency(call):
    if call.data == "to_address_tink":
        user_dict[call.message.chat.id].payment = "Тинькофф"
    elif call.data == "to_address_sber":
        user_dict[call.message.chat.id].payment = "Сбербанк"
    elif call.data == "to_address_qiwi":
        user_dict[call.message.chat.id].payment = "Qiwi"
    else:
        user_dict[call.message.chat.id].payment = "СБП"
    if user_dict[call.message.chat.id].type_check == 'buy':
        mesg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                 text='🪙 Введите адрес для получения средств указав сеть (BEP20/TRC20/ERC20/BITCOIN)')
        bot.register_next_step_handler(mesg, to_address)
    elif user_dict[call.message.chat.id].type_check == 'sell':
        mesg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                     text='💳 Укажите реквизиты для получения денежных средств')
        bot.register_next_step_handler(mesg, to_bank_card)


@bot.callback_query_handler(func=lambda call: call.data in ["to_photo", "to_ref"])
def send_application(call):
    if call.data == 'to_photo':
        user_dict[call.message.chat.id].check = True
        if user_dict[call.message.chat.id].payment == 'Тинькофф':
            destination = rekv.tink
        elif user_dict[call.message.chat.id].payment == 'Сбербанк':
            destination = rekv.sber
        elif user_dict[call.message.chat.id].payment == 'Киви':
            destination = rekv.qiwi
        elif user_dict[call.message.chat.id].payment == 'СБП':
            destination = rekv.sbp
        else:
            destination = rekv.crypto
        mesg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                 text='📑 Переведите средства по указанному адресу в течение 15 минут\n'
                                      'После оплаты, не забудьте отправить фото чека в чат для подтверждения!' + f'\nАдрес для оплаты - {destination}')
        bot.register_next_step_handler(mesg, checkphoto)
    elif call.data == 'to_ref':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Отправить хэш транзакции', callback_data='hash'))
        keyboard.add(types.InlineKeyboardButton(text='Прикрепить скрин', callback_data='screen'))
        keyboard = addreturnbutton(keyboard)
        destination = rekv.crypto
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='📑 Переведите средства по указанному адресу в течение 15 минут\n'
                                      + f'\nАдрес для оплаты - {destination}')
        bot.send_message(call.message.chat.id, text="📑 Отправьте хэш транзакции или прикрепите "
                                                           "скрин для подтверждения оплаты", reply_markup = keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ["screen", "hash"])
def send_confirm_payment(call):
    if call.data == 'hash':
        mesg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                     text='📑 Переведите средства по указанному адресу в течении 15 минут\n'
                                      'После оплаты, не забудьте отправить хэш транзакции в чат для подтверждения!')
        bot.register_next_step_handler(mesg, checkhash)
    else:
        user_dict[call.message.chat.id].check = True
        mesg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                     text='📑Переведите средства по указанному адресу в течении 15 минут\n'
                                      'После оплаты, не забудьте отправить скрин транзакции в чат для подтверждения!')
        bot.register_next_step_handler(mesg, checkphoto)


@bot.callback_query_handler(func=lambda call: call.data in ["discount", "ref_discount"])
def send_discount(call):
    if call.data == "discount":
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='✅ Использовать', callback_data='disc_yes'))
        keyboard.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='disc_no'))
        keyboard = addreturnbutton(keyboard)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                     text='Использовать жетон скидки?', reply_markup=keyboard)
    elif call.data == "ref_discount":
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='✅ Использовать', callback_data='ref_yes'))
        keyboard.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='ref_no'))
        keyboard = addreturnbutton(keyboard)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Использовать реферальный баланс?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ["disc_yes", 'disc_no'])
def send_submit(call):
    if call.data == 'disc_yes':
        if user_dict[call.message.chat.id].type_check == 'buy':
            user_dict[call.message.chat.id].sum_in -= user_dict[call.message.chat.id].discount
            user_dict[call.message.chat.id].discount = 0
            if user_dict[call.message.chat.id].sum_in < 0:
                user_dict[call.message.chat.id].sum_in = 0
            user_dict[call.message.chat.id].discountusecheck = True
        elif user_dict[call.message.chat.id].type_check == 'sell':
            user_dict[call.message.chat.id].sum_out += user_dict[call.message.chat.id].discount
            user_dict[call.message.chat.id].discount = 0
            user_dict[call.message.chat.id].discountusecheck = True
    discbonusaccept(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=lambda call: call.data in ["ref_yes", 'ref_no'])
def send_submit(call):
    if call.data == 'ref_yes':
        if user_dict[call.message.chat.id].type_check == 'buy':
            user_dict[call.message.chat.id].sum_in -= db.get_refbalance(call.message.chat.id)
            db.null_refbalance(call.message.chat.id)
            if user_dict[call.message.chat.id].sum_in < 0:
                user_dict[call.message.chat.id].sum_in = 0
            user_dict[call.message.chat.id].referalusecheck = True
        elif user_dict[call.message.chat.id].type_check == 'sell':
            user_dict[call.message.chat.id].sum_out += db.get_refbalance(call.message.chat.id)
            db.null_refbalance(call.message.chat.id)
            user_dict[call.message.chat.id].referalusecheck = True
    discbonusaccept(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=lambda call: call.data in ['add_ref_bonuses'])
def send_refbonuses(call):
    start = call.message.text.find('ID - ') + 5
    new_start = call.message.text.find('Бонус - ') + 8
    end = call.message.text[start:].find(' ')
    userid = int(call.message.text[start:][:end])
    bonus = float(call.message.text[new_start:])
    refererid = db.check_referer(userid)
    if refererid !=0:
        db.add_refbalance(refererid, bonus)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Выполнение заказа "
                                                                                         "подтверждено")


@bot.callback_query_handler(func=lambda call: call.data in ['chng_tink', 'chng_sber', 'chng_qiwi',
                                                            'chng_sbp', 'chng_btc', 'chng_usdt', 'chng_eth',
                                                            'chng_trx', 'chng_xmr'])
def send_changes(call):
    mesg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                 text='Введите новые реквизиты')
    if call.data == 'chng_tink':
        bot.register_next_step_handler(mesg, set_tink)
    elif call.data == 'chng_sber':
        bot.register_next_step_handler(mesg, set_sber)
    elif call.data == 'chng_qiwi':
        bot.register_next_step_handler(mesg, set_qiwi)
    elif call.data == 'chng_sbp':
        bot.register_next_step_handler(mesg, set_sbp)
    elif call.data == 'chng_btc':
        bot.register_next_step_handler(mesg, set_btc)
    elif call.data == 'chng_usdt':
        bot.register_next_step_handler(mesg, set_usdt)
    elif call.data == 'chng_eth':
        bot.register_next_step_handler(mesg, set_eth)
    elif call.data == 'chng_trx':
        bot.register_next_step_handler(mesg, set_trx)
    elif call.data == 'chng_xmr':
        bot.register_next_step_handler(mesg, set_xmr)


bot.polling(none_stop=True)
