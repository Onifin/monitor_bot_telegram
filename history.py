import os

import google.generativeai as genai

gemini_token = os.environ['GEMINI_TOKEN']
genai.configure(api_key=gemini_token)
model = genai.GenerativeModel('gemini-pro')

init_memory = """
Você é o AVE, um bot feito para ajudar alunos em lógica de programação (LOP), quando alguém falar com você diga isso e a trate bem.

Lista de informações importantes: 

* Você ajuda os alunos da matéria Lógica de programação da ECT (escola de ciências e tecnologia).

* Os horários dos laboratórios de LOP são 24t34.

* AVE significa assistente virtual educacional.

* O professor da turma A se chama Orivaldo.

* link do canal do professor Orivaldo é https://www.youtube.com/@orivaldo

* link do servidor do discord da disciplina LOP https://discord.gg/xqmRkFnB4Y

Quando a informação estiverem nessa lista responda de forma sucinta sem adicionar muita informação a mais.
"""

class history:
  """A class used to represent a history of a conversation
  
  Attributes
  ----------

  number: str
    The number atribute is the id of the object, It looks like a primary key.

  chat: list
    This atribute storage the conversation. 
    Each part of the conversation is a dictionary.

    The dictionary contains the role (who send the message) and the parts that contains the message.
    
    {
      "role": "user",
      "parts": [message],
    }
  """
  
  def __init__(self, number, memory=""):
    """
    This method recive the number and the previus memory of the model
    """
    self.number = number
    self.chat = []
    self.queue = []

    if(len(memory) != 0):
      self.chat.append({
      "role": "user",
      "parts": [memory]
      })

      response = model.generate_content(self.chat)

      self.chat.append({
        "role": "model",
        "parts": [response.text]
      })

  def get_number(self):
    return self.number
  
  def append_message(self, message, message_sender):
    if(self.get_last_message_role() == "user" and message_sender == "user"):
      self.queue.append(message)
      print("FILA: ")
      print(self.queue)
      #time.sleep(5)
      return False
    
    if(message_sender == 'user'):
      self.chat.append({
          "role": "user",
          "parts": [message],
      })
    else:
      self.chat.append({
        "role": "model",
        "parts": [message],
      })
    return True
    
  def pop_message(self):
    self.chat.pop()
  
  def get_chat(self):
    return self.chat
  
  def get_last_message_role(self):
    if(self.chat_is_empty()):
      return None
    return self.chat[-1]["role"]

  def chat_is_empty(self):
    return(len(self.chat) == 0)
  
  def check_pendding_messages(self):
    return(len(self.queue) != 0)
  
  def get_pendding_message(self):
    print("FILA ANTES")
    print(self.queue)
    msg = self.queue.pop(0)
    print("FILA DEPOIS")
    print(self.queue)
    return msg
  
class history_handler:
  def __init__(self):
    self.history_list = []

  def add_history(self, new_history):
    self.history_list.append(new_history)

  def change_history(self, history_changed, number):
    for i in range(len(self.history_list)):
      if(self.history_list[i].number == number):
        self.history_list[i] = history_changed

  def get_history(self, number):
    for i in range(len(self.history_list)):
      if(self.history_list[i].number == number):
        return self.history_list[i]
    
    h = history(number, init_memory)
    self.add_history(h)

    return h
