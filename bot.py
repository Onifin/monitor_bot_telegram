import telebot
import google.generativeai as genai
import requests
from dotenv import load_dotenv
import os
from api import get_alunos, get_token

# Carregar as variáveis do arquivo .env
load_dotenv()

#TELEGRAM
API_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

#GEMINI
gemini_token = os.getenv('GEMINI_TOKEN')
genai.configure(api_key=gemini_token)
model = genai.GenerativeModel('gemini-pro')

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Olá, sou o AVE (Assistente virtual educacional).\
""")

# Handle '/start' and '/help'
@bot.message_handler(commands=['teste'])
def send_welcome(message):
    bot.reply_to(message, """teste feito""")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    numero = message
    print(get_token())
    #print(message.chat.id)
    response = model.generate_content(message.text)
    bot.reply_to(message, response.text)

bot.infinity_polling()