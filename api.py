import requests
from dotenv import load_dotenv
from decouple import config

# Carregar as variáveis do arquivo .env

api_url = config('API1_BOT')
email = config('USER_EMAIL')
senha = config('USER_PASSWORD')


def get_token():
    # URL da API
    url = f"{api_url}api/v1/users/login"

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
    
        # Retorna o token
        return data['token']['access_token'] 
    else:
        print(f"Erro ao obter o token: {response.status_code}")
        return None

api_token = get_token()

def get_alunos():
    
    headers = {
    "Authorization": f"Bearer {api_token}"
    }

    response = requests.get(api_url+"api/v1/alunos/lista_alunos/", headers=headers)
   
    return(response)

def create_telegram_id(matricula, id):

    headers = {
    "Authorization": f"Bearer {api_token}"
    }

    data = {    
        "matricula": matricula,
        "telefone": id
    }

    response = requests.post(api_url+"api/v1/whatsapp/adicionar_numero", headers=headers, json=data)

    return(response)

def get_telegram_id(matricula):
    headers = {
    "Authorization": f"Bearer {api_token}"
    }

    data = {    
        "matricula": matricula
    }

    response = requests.post(api_url+"api/v1/whatsapp/obter_numero/", headers=headers, json=data)

    return(response)

def delete_telegram_id(matricula):
    headers = {
    "Authorization": f"Bearer {api_token}"
    }

    data = {    
        "matricula": matricula
    }

    response = requests.delete(api_url+"/api/v1/whatsapp/excluir_numero/", headers=headers, json=data)

    return(response)
    
def cadastrar_frequencia(matricula, turma):
    #A função retorna 400 caso tente registrar a presença de um aluno que não tem aulas nesse horário

    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    data = {
        "matricula": matricula,
        "sigla": turma
    }

    # Faz a solicitação POST
    response = requests.post(api_url+"api/v1/presenca/", headers=headers, json=data)

    return(response)