from flask import render_template, request
import requests
import json
from app import app

link = "https://flasktintgrazy-default-rtdb.firebaseio.com/"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', titulo="Página Inicial")

@app.route('/contato')
def contato():
    return render_template('contato.html', titulo="Contatos")

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', titulo="Cadastrar")

@app.route('/excluir', methods=['POST', 'GET'])
def excluir():
    if request.method == 'POST':
        cpf = request.form.get("cpf")
        return remover_usuario(cpf)
    return render_template('excluir.html', titulo="Excluir")

@app.route('/atualizar', methods=['GET'])
def atualizar():
    return render_template('atualizar.html', titulo="Atualizar")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrar_usuario():
    try:
        cpf = request.form.get("cpf")
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")
        pagamento = request.form.get("pagamento")
        dados = {'cpf': cpf, 'nome': nome, 'telefone': telefone, 'endereco': endereco, 'pagamento': pagamento}
        requests.post(f'{link}/cadastro/.json', data=json.dumps(dados))
        return 'Cadastrado com sucesso!'
    except Exception as e:
        return f'Ocorreu um erro: {e}'

@app.route('/listar')
def listar_tudo():
    try:
        requisicao = requests.get(f'{link}/cadastro/.json')
        dicionario = requisicao.json()
        return dicionario
    except Exception as e:
        return f'Ocorreu um erro: {e}'

@app.route('/listarIndividual', methods=['POST', 'GET'])
def listar_individual():
    if request.method == 'POST':
        try:
            cpf = request.form.get("cpf")

            requisicao = requests.get(f'{link}/cadastro/.json')
            dicionario = requisicao.json()

            for codigo, dados in dicionario.items():
                if dados['cpf'] == cpf:
                    return json.dumps(dados), 200  # Retorna o usuário em formato JSON

            return json.dumps({"erro": "CPF não encontrado!"}), 404

        except Exception as e:
            return json.dumps({"erro": f"Ocorreu um erro: {e}"}), 500

    return render_template('listar_individual.html')

@app.route('/atualize', methods=['POST'])
def atualizar_usuario():
    try:
        cpf = request.form.get("cpf")
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")
        pagamento = request.form.get("pagamento")

        requisicao = requests.get(f'{link}/cadastro/.json')
        dicionario = requisicao.json()

        dados = {'cpf': cpf, 'nome': nome, 'telefone': telefone, 'endereco': endereco, 'pagamento': pagamento}
        for codigo in dicionario:
            if dicionario[codigo]['cpf'] == cpf:
                requests.patch(f'{link}/cadastro/{codigo}/.json', data=json.dumps(dados))
                return 'Atualizado com sucesso!'
        return 'CPF não encontrado!'
    except Exception as e:
        return f'Algo deu errado: {e}'

@app.route('/remover', methods=['POST'])
def remover_usuario(cpf=None):
    try:
        if not cpf:
            cpf = request.form.get("cpf")
        requisicao = requests.get(f'{link}/cadastro/.json')
        dicionario = requisicao.json()
        for codigo in dicionario:
            if dicionario[codigo]['cpf'] == cpf:
                requests.delete(f'{link}/cadastro/{codigo}/.json')
                return 'Excluído com sucesso!'
        return 'CPF não encontrado!'
    except Exception as e:
        return f'Algo deu errado: {e}'
