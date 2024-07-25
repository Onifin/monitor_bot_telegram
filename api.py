import requests
from dotenv import load_dotenv
import os

# Carregar as variáveis do arquivo .env
load_dotenv()

api_url = os.getenv('API_BOT')
email = os.getenv('USER_EMAIL')
senha = os.getenv('USER_PASSWORD')

def get_token():
    # URL da API
    url = f"{api_url}api/v1/users/login"
    print(url)
    print(email)
    print(senha)

    # Dados de autenticação
    auth_data = {
        "email": email,
        "password": senha
    }

    # Faz a solicitação POST
    response = requests.post(url, json=auth_data)

    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Converte a resposta para JSON
        data = response.json()
        
        print(data['message']) 
        # Retorna o token
        return data['token']['access_token'] 
    else:
        print(f"Erro ao obter o token: {response.status_code}")
        return None

def get_alunos():

    response = requests.get(api_url+"api/v1/alunos/lista_alunos/")

    return(response)

def cria_usuario(email, senha):

    data = {
        "email": email,
        "username": "IAN",
        "id_discord": "12345",
        "password": senha
    }

    print(api_url)

    response = requests.post(api_url+"api/v1/users/adiciona", json=data)

    return(response)