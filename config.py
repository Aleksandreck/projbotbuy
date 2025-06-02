
import telebot
from telebot import types
from presetBase import admin_list


#bot = telebot.TeleBot(TOKEN)

callback_capcha = ['👥', '👾', '🐰', '🍀', '🍌']
flag_capcha = False


def DotMenu(message):
    markup = types.ReplyKeyboardRemove()
    return markup

def MainMenu(message):
    markup = types.InlineKeyboardMarkup()

    markup.row_width = 2

    #btn0 = types.InlineKeyboardButton("📂 Мои данные", callback_data="my nft")
    btn1 = types.InlineKeyboardButton('✈ Оформить заказ', callback_data="get_order")
    btn2 = types.InlineKeyboardButton('📂 Мои данные', callback_data="change_data")

    # btn2 = types.InlineKeyboardButton("🔗 Реферальная программа", callback_data="refer programm")

    # log_inst = types.InlineKeyboardButton(text="📱 Instagram", url='https://instagram.com/ton_elephants')
    log_tg = types.InlineKeyboardButton(text="✈ Telegram", url='https://t.me/kicksboxlog')
    log_chat = types.InlineKeyboardButton(text='🗣 Отзывы клиентов', url='https://t.me/+DdJEiUvR0Vg2NDdi')

    chat_id = message.chat.id

    markup.add(btn1, btn2, log_tg, log_chat)
   

    return markup

def ChangeData(message):
    markup = types.InlineKeyboardMarkup()

    markup.row_width = 2

    btn1 = types.InlineKeyboardButton("Изменить данные", callback_data="edit_data")
    back_Menu = types.InlineKeyboardButton(text="⚙️ Вернутся в главное меню", callback_data="back_menu")

    markup.add(btn1, back_Menu)

    return markup

def show_url_sub():
    """Вывод инлайн кнопки с подписками"""
    
    markup = types.InlineKeyboardMarkup()

    markup.row_width = 3

    log_tg = types.InlineKeyboardButton(text="✈ Telegram", url='https://t.me/kicksboxlog')
    log_chat = types.InlineKeyboardButton(text='🗣 Отзывы клиентов', url='https://t.me/+DdJEiUvR0Vg2NDdi')

    back_Menu = types.InlineKeyboardButton(text="⚙️ Вернутся в главное меню", callback_data="back_menu")

    


    markup.add(log_tg, log_chat, back_Menu)

    


    return markup

def MarkupBackMenu():
    markup = types.InlineKeyboardMarkup()

    back_Menu = types.InlineKeyboardButton(text="⚙️ Вернутся в главное меню", callback_data="back_menu")

    markup.add(back_Menu)
    
    return markup

def ParserOrder(user_input):
    try:
        # Убираем лишние пробелы и разделяем строку по запятой
        parts = [part.strip() for part in user_input.split(",")]
        
        if len(parts) != 4:
            raise ValueError("Неверный формат данных. Требуется 4 элемента.")

        # Распределяем значения
        clothing_type = parts[0]  # Тип одежды
        size = (parts[1])  # Количество
        price_in_yuan = float(parts[2])  # Цена в юанях
        link = parts[3]  # Ссылка на товар

        return {
            "clothing_type": clothing_type,
            "size": size,
            "price_in_yuan": price_in_yuan,
            "link": link
        }

    except ValueError as e:
        print(f"Ошибка при обработке данных: {e}")
        return None

