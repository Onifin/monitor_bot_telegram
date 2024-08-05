from api import get_alunos

def check_registration(id):

    requisicao = get_alunos()
    alunos = requisicao.json()

    #testa se o aluno está cadastrado
    for key in alunos:
        if "telefone" in alunos[key]:
            is_registered = alunos[key]["telefone"] == id
            if(is_registered): break
    
    return is_registered

def get_class(id):

    requisicao = get_alunos()
    alunos = requisicao.json()

    for key in alunos:
        if "telefone" in alunos[key]:
            if(alunos[key]["telefone"] == id):
                return(alunos[key]["turma"])
    
    return(None)

def get_matricula(id):

    requisicao = get_alunos()
    alunos = requisicao.json()

    for key in alunos:
        if "telefone" in alunos[key]:
            if(alunos[key]["telefone"] == id):
                return(alunos[key]["matricula"])
    
    return(None)
    
    