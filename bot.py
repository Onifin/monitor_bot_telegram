import telebot
import google.generativeai as genai
import requests
from dotenv import load_dotenv
import os

from api import get_alunos, get_token, create_telegram_id, cadastrar_frequencia
from utils import check_registration, get_class, get_matricula, get_nome
from history import history, history_handler

# Carregar as variáveis do arquivo .env
load_dotenv()

#TELEGRAM
API_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

#GEMINI
gemini_token = os.getenv('GEMINI_TOKEN')
genai.configure(api_key=gemini_token)
model = genai.GenerativeModel('gemini-pro')

#Histórico
bot_history = history_handler()

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Olá, sou o AVE (Assistente virtual educacional).\
""")

@bot.message_handler(commands=['presença', 'presenca', 'frequencia'])
def presenca(message):

    id = str(message.chat.id)
    is_registered = check_registration(id)

    if(not is_registered):
        bot.reply_to(message, "É necessário fazer o cadastro para usar o bot")
        return
    
    turma = get_class(id)
    matricula = get_matricula(id)
    
    response = cadastrar_frequencia(int(matricula), turma)

    response_dict = response.json()

    if "detail" in response_dict:
        bot.reply_to(message, response_dict["detail"])
    elif "mensagem" in response_dict:
        bot.reply_to(message, response_dict["mensagem"]+": "+get_nome(id))
    else:
        bot.reply_to(message, "Ocorreu um erro inesperado. Tente novamente mais tarde.")

@bot.message_handler(commands=['cadastro'])
def create_id(message):
    # Checa se o usuário enviou o cadastro no formato correto
    # /cadastro matricula
    message_split = message.text.split(" ")
    if len(message_split) != 2:
        bot.reply_to(message, 
            """
            O comando de cadastro deve seguir o seguinte formato:

            /cadastro matricula
                    
            Ex.:

            /cadastro 20230013400
            """)
        return
    
    matricula = message_split[1]
    id = message.chat.id
    
    response = create_telegram_id(matricula, str(id))
    response_dict = response.json()
    
    if "detail" in response_dict:
        bot.reply_to(message, response_dict["detail"])
    elif "mensagem" in response_dict:
        bot.reply_to(message, response_dict["mensagem"])
    else:
        bot.reply_to(message, "Ocorreu um erro inesperado. Tente novamente mais tarde.")

@bot.message_handler(func=lambda message: True)
def message_text(message):
    
    id = str(message.chat.id)
    is_registered = check_registration(id)

    if(not is_registered):
        bot.reply_to(message, "É necessário fazer o cadastro para usar o bot")
        return
    
    h = bot_history.get_history(id) 
    h.append_message(message.text, "user")

    #Envia o histórico de mensagens para o modelo
    response = model.generate_content(h.get_chat())
    bot.reply_to(message, response.text)
    
    #adiciona a mensagem e a resposta ao histórico
    
    h.append_message(response.text, "model")

bot.infinity_polling()