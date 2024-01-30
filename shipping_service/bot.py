from django.conf import settings
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from orders.tasks import delivery_employee_refusal, delivery_confirmation, delivery_confirmed, customer_backed_out
from organization.tasks import add_employee
from organization.models import Cities, DeliveryService
from orders.models import Orders

bot = TeleBot(settings.TOKEN_BOT, parse_mode='HTML')
user_data = {}
smile1 = u'\U0001F60A'  # веселый смайлик
smile2 = u'\U0001F614'  # грустный смайлик


def open_orders(message):
    order = Orders.objects.filter(delivery_service__telegram=message.chat.id, paid=True,
                                  delivered=False)
    for item in order:
        bot.send_message(message.chat.id, f"Заказ №{item.id}\n"
                                          f"Забрать: {item.user.address}\n"
                                          f"Доставить: {item.address}\n"
                                          f"Контактный телефон: {item.phone}")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        chat_id = DeliveryService.objects.get(telegram=message.from_user.id)
        if chat_id:
            bot.send_message(message.chat.id, f"Привет {chat_id.fio}")
            if chat_id.work_authorization:
                if chat_id.status and not chat_id.day_off:
                    bot.send_message(message.chat.id, "У вас есть незавершенные задания.\n\n")
                    open_orders(message)
                elif not chat_id.status and chat_id.day_off:
                    bot.send_message(message.chat.id, f"У вас выходной, хотите поработать!? {smile1} Сообщите об этом "
                                                      f"вашему менеджеру:")
                    open_orders(message)
                elif chat_id.status and chat_id.day_off:
                    bot.send_message(message.chat.id, "У вас выходной и есть незавершенные задания. Обязательно "
                                                      "сообщите об этом вашему менеджеру!")
                    open_orders(message)
                elif not chat_id.status and not chat_id.day_off:
                    bot.send_message(message.chat.id, f"В данный момент для вас нет задания. Подождите немного и оно "
                                                      f"обязательно появится! {smile1}")
            else:
                bot.send_message(message.chat.id, f"У вас нет допуска к работе {smile2} Уточните у вашего "
                                                  f"менеджера, почему так происходит.")
        else:
            pass
    except DeliveryService.DoesNotExist:
        keyboard = InlineKeyboardMarkup()
        yes_job = InlineKeyboardButton("Да", callback_data='yes_job:')
        no_job = InlineKeyboardButton("Отмена", callback_data='no_job:')
        keyboard.add(yes_job, no_job)
        bot.send_message(message.chat.id, "Заинтересованы в вакансии сотрудника службы доставки еды?",
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: True)
def order_acceptance(callback):
    chat_id = callback.from_user.id
    id_data = callback.data.split(':')[1]
    if callback.data.startswith('no:'):
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)
        delivery_employee_refusal.delay(chat_id, id_data)
        bot.send_message(callback.message.chat.id, f"Вы отказались от Заказа №{id_data}")

    elif callback.data.startswith('yes:'):
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)
        bot.send_message(callback.message.chat.id, f"Вы приняли Заказ №{id_data}")
        delivery_confirmation.apply_async(args=[chat_id, id_data], countdown=60)

    elif callback.data.startswith('yes_delivery:'):
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)
        bot.send_message(callback.message.chat.id, f"Заказ №{id_data} выполнен, {smile1} спасибо за работу!")
        delivery_confirmed.delay(id_data, chat_id)

    elif callback.data.startswith('client_refused:'):
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)
        bot.send_message(callback.message.chat.id, f"Возвращайтесь с Заказом №{id_data} обратно {smile2}")
        customer_backed_out.delay(id_data)

    elif callback.data.startswith('yes_job:'):
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)
        bot.send_message(callback.message.chat.id, "Введите ваши Фамилия Имя Отчество:")
        bot.register_next_step_handler(callback.message, get_fio)

    elif callback.data.startswith('no_job:'):
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)

    elif callback.data.startswith(f'city:'):
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)
        user_data['city'] = id_data

        keyboard = InlineKeyboardMarkup()
        bot.send_message(callback.message.chat.id, f"Спасибо! Ваши данные:\n\nФИО: {user_data['fio']}\n"
                                                   f"Возраст: {user_data['age']}\nТелефон: {user_data['phone']}\n"
                                                   f"Город: {user_data['city']}\n\n")
        employee_yes = InlineKeyboardButton("Да", callback_data='employee_yes:')
        employee_no = InlineKeyboardButton("Нет", callback_data='yes_job:')
        keyboard.add(employee_yes, employee_no)
        bot.send_message(callback.message.chat.id, "Данные заполнены корректно?",
                         reply_markup=keyboard)

    elif callback.data.startswith('employee_yes:'):
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)
        add_employee.delay(user_data)
        bot.send_message(callback.message.chat.id, "Данные приняты. Ожидайте, скоро с вами свяжутся.")


def get_fio(message):
    fio = message.text
    if len(fio) > 10:
        user_data['chat_id'] = message.from_user.id
        user_data['fio'] = message.text
        bot.send_message(message.chat.id, "Введите ваш возраст:")
        bot.register_next_step_handler(message, get_age)
    else:
        bot.send_message(message.chat.id, "Недостаточно данных. Введите ваши Фамилия Имя Отчество снова:")
        bot.register_next_step_handler(message, get_fio)


def get_age(message):
    age = message.text
    if age.isdigit() and len(age) == 2:
        user_data['age'] = age
        bot.send_message(message.chat.id, "Введите ваш номер телефона (используйте только цифры без 8 и +7):")
        bot.register_next_step_handler(message, get_phone)
    else:
        bot.send_message(message.chat.id, "Некорректный возраст. Введите ваш возраст снова:")
        bot.register_next_step_handler(message, get_age)


def get_phone(message):
    phone = message.text
    if phone.isdigit() and len(phone) == 10:
        user_data['phone'] = message.text
        cities = Cities.objects.all()
        markup = types.InlineKeyboardMarkup(row_width=2)
        for city in cities:
            button = types.InlineKeyboardButton(city.city, callback_data=f'city:{city}')
            markup.add(button)
        bot.send_message(message.chat.id, 'Выберите ваш город:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Некорректный номер телефона. Введите ваш номер телефона снова:")
        bot.register_next_step_handler(message, get_phone)
