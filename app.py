from flask import Flask, request, jsonify
from banco_dados import *
from modelos import Pessoa
from pydantic import ValidationError

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Garante que o banco de dados e a tabela existam ao iniciar o servidor
criar_tabela()

# Rota GET para listar todas as pessoas
@app.route('/pessoas', methods=['GET'])
def listar_pessoas():
    limite = request.args.get('limite', type=int)
    nome = request.args.get('nome') # Obtém o nome do parâmetro de query (opcional)
    pessoas = listar_pessoas_banco(limite, nome)
    return jsonify(pessoas), 200

# Rota POST para criar uma nova pessoa
@app.route('/pessoas', methods=['POST'])
def criar_pessoa():
    try:
        # Tenta validar os dados usando o modelo Pessoa
        dados = request.get_json()
        pessoa = Pessoa(**dados)

        id_pessoa = criar_pessoa_banco(
            nome=pessoa.nome,
            idade=pessoa.idade,
            sexo=pessoa.sexo,
            email=pessoa.email
        )

        return jsonify({'id': id_pessoa, **dados}), 201

    except ValidationError as e:
        # Retorna os erros de validação de forma amigável
        return jsonify({
            'erro': 'Dados inválidos',
            'detalhes': e.errors()
        }), 400

# Rota GET para buscar uma pessoa pelo ID
@app.route('/pessoas/<int:id>', methods=['GET'])
def obter_pessoa(id):
    pessoa = buscar_pessoa_por_id(id)

    if pessoa:
        return jsonify(pessoa), 200

    return jsonify({'erro', f'Pessoa com ID {id} não encontrada.'}), 404

# Rota DELETE para deletar uma pessoa pelo ID
@app.route('/pessoas/<int:id>', methods=['DELETE'])
def deletar_pessoa(id):
    try:
        deletar_pessoa_banco(id)
        return jsonify({'mensagem': f'Pessoa com ID {id} foi deletada com sucesso.'}), 200
    except ValueError as e:
        return jsonify({'erro': str(e)}), 404

# Rota PUT para editar uma pessoa
@app.route('/pessoas/<int:id>', methods=['PUT'])
def editar_pessoa(id):
    try:
        # Tenta validar os dados usando o modelo Pessoa
        dados = request.get_json()
        pessoa = Pessoa(**dados)

        editar_pessoa_banco(
            id,
            pessoa.nome,
            pessoa.idade,
            pessoa.sexo,
            pessoa.email
        )
        return jsonify({'mensagem': 'Pessoa atualizada com sucesso!'}), 200

    except ValidationError as e:
        # Retorna os erros de validação de forma amigável
        return jsonify({
            'erro': 'Dados inválidos',
            'detalhes': e.errors()
        }), 400
    except Exception as e:
        return jsonify({'erro': f'Erro ao atualizar pessoa: {str(e)}'})

# Executa o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
