import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

API_TOKEN = '6600451523:AAGWIR0dGBe6ke6QIMltMlVzwAMjPsZdnvQ'
bot = telebot.TeleBot(API_TOKEN)

# إنشاء قاعدة البيانات إذا لم تكن موجودة
conn = sqlite3.connect('bot_database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    clicks INTEGER DEFAULT 0,
    invites INTEGER DEFAULT 0,
    currency INTEGER DEFAULT 0
)''')
conn.commit()

def get_or_create_user(user_id):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        conn.commit()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
    return user

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = get_or_create_user(message.from_user.id)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("جمع العملة", callback_data="collect_currency"))
    markup.add(InlineKeyboardButton("المهام ودعوات الأصدقاء", callback_data="invite_friends"))
    markup.add(InlineKeyboardButton("التداول", callback_data="trade"))
    bot.send_message(message.chat.id, "مرحبا بك! اختر قسمًا:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user = get_or_create_user(call.from_user.id)
    if call.data == "collect_currency":
        bot.send_message(call.message.chat.id, f"لديك {user[1]} نقرات و {user[3]} عملات.")
    elif call.data == "invite_friends":
        bot.send_message(call.message.chat.id, f"لقد دعوت {user[2]} صديقًا وحصلت على {user[3]} عملات.")
    elif call.data == "trade":
        bot.send_message(call.message.chat.id, "قسم التداول سيكون متاحًا قريبًا.")

bot.polling()
