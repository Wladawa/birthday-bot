import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import sqlite3
from datetime import datetime

# Настройки
TOKEN = "7555717491:AAG3GFkZrZ06WTb6iiNnCZRkaFogEwKt4TY"  # Замените на токен от @BotFather

# Подключение к SQLite
conn = sqlite3.connect('birthdays.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS birthdays
                  (user_id INTEGER, name TEXT, date TEXT)''')
conn.commit()

# Команда /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот для напоминаний о днях рождения. Используй /add чтобы добавить запись.")

# Команда /add
def add_birthday(update: Update, context: CallbackContext):
    update.message.reply_text("Введите имя и дату в формате: Иван 31.12.2024")

def save_birthday(update: Update, context: CallbackContext):
    try:
        text = update.message.text.split()
        name, date = text[0], text[1]
        datetime.strptime(date, "%d.%m.%Y")  # Проверка формата даты
        cursor.execute("INSERT INTO birthdays VALUES (?, ?, ?)", 
                      (update.effective_user.id, name, date))
        conn.commit()
        update.message.reply_text(f"✅ Добавлено: {name} - {date}")
    except:
        update.message.reply_text("❌ Ошибка. Формат: Имя ДД.ММ.ГГГГ")

# Основная функция
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add_birthday))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, save_birthday))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
