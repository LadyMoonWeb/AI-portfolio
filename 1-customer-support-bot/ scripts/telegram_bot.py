#  Этот файл нужен, если требуется сложная логика взаимодействия с Telegram API,
#  которую нельзя реализовать напрямую в n8n.  Например, если нужно обрабатывать
#  сложные типы сообщений, загружать файлы и т.д.  В большинстве случаев может быть не нужен.

import telebot
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот поддержки. Задайте свой вопрос.")

# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#         bot.reply_to(message, message.text)

# Запуск бота (только если требуется отдельный процесс)
# bot.infinity_polling()
