import telebot
from telebot import types
import bd
from config import *
from random import randint
import Course as CB

# Инициализация бота
TOKEN = "6339184612:AAFZ8dUTqpvXLiJSWF02ZHkZoioJPQsVr2M"
bot = telebot.TeleBot(TOKEN)



def ChekUser(message):

    markup = types.InlineKeyboardMarkup()

    capcha_one = types.InlineKeyboardButton(text=callback_capcha[0], callback_data=callback_capcha[0])
    capcha_two = types.InlineKeyboardButton(text=callback_capcha[1], callback_data=callback_capcha[1])
    capcha_tree = types.InlineKeyboardButton(text=callback_capcha[2], callback_data=callback_capcha[2])
    capcha_four = types.InlineKeyboardButton(text=callback_capcha[3], callback_data=callback_capcha[3])
    capcha_five = types.InlineKeyboardButton(text=callback_capcha[4], callback_data=callback_capcha[4])

    markup.add(capcha_one, capcha_two, capcha_tree, capcha_four, capcha_five)
    
    markup.row_width = 2

    capcha_id = randint(0, 4)

    capcha = callback_capcha[capcha_id]

    bd.SetCapcha(message.chat.id, capcha_id)

    print("[Set Capcha]", capcha_id, capcha)

    bot.send_message(message.chat.id, text="Для обеспечения безопастности, необходимо пройти проверку\n"
                                            "Для этого, найдите и выберите одинаковый изобраения\n"
                                            f"{capcha}",
                    reply_markup=markup
    )

def BuyOrder(message):
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton("💴 Узнать цену", callback_data="chek_coast")
    btn2 = types.InlineKeyboardButton("📨 Оформить заказ", callback_data="order")
    back = types.InlineKeyboardButton("⚙️ Вернутся в главное меню", callback_data="back_menu")

    markup.add(btn1, btn2, back)

    bot.send_message(message.chat.id, "Давай подберем тебе одежду", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "login")
def handle_login(call):
    bot.send_message(call.message.chat.id, "Отправьте ваши данные в формате: Имя, Размер одежды, Размер обуви")

# Обработчик текстовых сообщений (для регистрации)
@bot.message_handler(func=lambda message: True)
def handle_registration(message):
    # Разбиваем текст на части (предполагается формат "Имя, Размер одежды, Размер обуви")
    if message.text == "/start":
        ChekUser(message)
    elif message.text[:6] == "Заказ:":
        print("[Order]", message.text[7:])
        parset_data = ParserOrder(message.text[7:])

        coast_in_rub = CB.GetCoast(parset_data["price_in_yuan"])

        order_id = bd.NewOrder(message.chat.id, parset_data, coast_in_rub)

        bot.send_message(message.chat.id, f"Заказ успешной создан!\nНомер вашего заказа: {order_id}", reply_markup=MainMenu(message))
    elif message.text[:5] == "Цена:":
        coast_in_rub = CB.GetCoast(float(message.text[6:]))
        bot.send_message(message.chat.id, f"Цена вашего заказа: {coast_in_rub}₽", reply_markup=MainMenu(message))

    else:
        user_input = message.text.split(", ")
        
        if len(user_input) == 3:
            name, clothing_size, shoe_size = user_input
            # Делаем проверку на корректность данных (например, размер обуви — число)
            try:
                shoe_size = int(shoe_size)
                # Здесь вы можете добавить код для сохранения данных в базу или дальнейшей обработки
                if bd.NewUserNFT(message.chat.id, f"@{message.chat.username}", name, clothing_size, shoe_size):

                    bot.send_message(message.chat.id,
                                    f"Спасибо за регистрацию! Ваши данные: Имя: {name}, Размер одежды: {clothing_size}, Размер обуви: {shoe_size}", reply_markup=MainMenu(message))
                else:
                    bot.send_message(message.chat.id,
                                    f"Данные успешно изменены! Ваши данные: Имя: {name}, Размер одежды: {clothing_size}, Размер обуви: {shoe_size}", reply_markup=MainMenu(message))
                

            except ValueError:
                bot.send_message(message.chat.id, "Ошибка: Размер обуви должен быть числом. Попробуйте снова.")
        else:
            bot.send_message(message.chat.id, "Неверный формат данных", reply_markup=MarkupBackMenu())


@bot.callback_query_handler(func = lambda call : True)
def Chek(call):
    # message = call.message

    global callback_capcha
    capcha_id = bd.GetCapcha(call.message.chat.id)
    print("[Get Capcha]", capcha_id, callback_capcha[capcha_id], "\n")

    if call.data == callback_capcha[capcha_id]:
        acsess = bd.GetAcsess(call.message.chat.id)

        if not acsess:      # Проверка наличия в базе данных сведений о пользователе

            markup = types.InlineKeyboardMarkup()
            login = types.InlineKeyboardButton("💻 Зарегистрироваться", callback_data="login")
            markup.add(login)

            # print(call.message.chat.id)

            bot.send_photo(call.message.chat.id,
                           photo=open("images/menu.jpg", "rb"),
                           caption="Пожалуйста зарегистрируйтесь. Для этого укажите: Имя, Размер одежды, Размер обуви. "
                                    "Затем нажмите кнопку 'Зарегистрироваться'. Это поможет в подборе одежды. \nПример: Иван, XXL, 45",
                           reply_markup=markup)

        else:
            bot.send_photo(call.message.chat.id,
                           photo=open("images/menu.jpg", "rb"), #"/images/menu.jpg",
                           caption="Вы уже зарегистрированы, добро пожаловать!",
                           reply_markup=MainMenu(call.message))
            

    elif call.data == "get_order":          # Работа с заказми  
        BuyOrder(call.message)
            
    elif call.data == "change_data":        # Получение введеных данных об пользователе

        name, clothing_size, shoe_size = bd.GetDataUser(call.message.chat.id)       
        print("[Change Data]", name, " ", clothing_size, " ", shoe_size)

        text = f"Твои данные: Имя: {name}, Размер одежды: {clothing_size}, Размер обуви: {shoe_size}\n Хочешь изменить?"

        bot.send_photo(call.message.chat.id,
                           photo=open("images/mydata.jpg", "rb"), #"/images/menu.jpg",
                           caption=text,
                           reply_markup=ChangeData(call.message))


    elif call.data == "edit_data":          # Изменение введеных данных об пользователе
        handle_login(call)

    elif call.data == "back_menu":          # Возврат в главное меню
        
        bot.send_photo(call.message.chat.id,
                           photo=open("images/main.jpg", "rb"), #"/images/menu.jpg",
                           #caption="Вы уже зарегистрированы, добро пожаловать!",
                           reply_markup=MainMenu(call.message))

    elif call.data == "order":         # Оформление заказа
        text=(
                            "Введите через запятую следующие данные:\n\n"
                            "*Заказ:* `'тип одежды', 'размер одежды', 'Цена товара в ¥', 'ссылка на товар'`\n\n"
                            "*Пример:*\n"
                            "`Заказ: кроссовки, XL, 596.1, https://dw4.co/t/A/1r6VSvROn`"
                        )
        bot.send_photo(call.message.chat.id,
                           photo=open("images/order.jpg", "rb"), #"/images/menu.jpg",
                           caption=text,
                           parse_mode="Markdown")

    elif call.data == "chek_coast":
        text=(
                "Введите цену в Юанях:\n\n"
                "*Пример:*\n"
                "`Цена: 596.1`"
            )
        bot.send_photo(call.message.chat.id,
                           photo=open("images/price.jpg", "rb"), #"/images/menu.jpg",
                           caption=text,
                           parse_mode="Markdown")


    # elif call.data ==         
    else:
        bot.send_message(call.message.chat.id, 
                            text="Такое не работает")

@bot.message_handler(commands=['start'])
def start_handler(message):
    ChekUser(message)



# Запуск бота
bot.infinity_polling(timeout=30, long_polling_timeout = 10)

