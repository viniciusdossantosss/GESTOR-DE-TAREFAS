from config import banco_de_dados

class Usuario(banco_de_dados.Model):
    id = banco_de_dados.Column(banco_de_dados.Integer, primary_key=True)
    nome = banco_de_dados.Column(banco_de_dados.String(80), nullable=False)
    email = banco_de_dados.Column(banco_de_dados.String(120), unique=True, nullable=False)
    senha = banco_de_dados.Column(banco_de_dados.String(128), nullable=False)

class Tarefa(banco_de_dados.Model):
    id = banco_de_dados.Column(banco_de_dados.Integer, primary_key=True)
    titulo = banco_de_dados.Column(banco_de_dados.String(200), nullable=False)
    descricao = banco_de_dados.Column(banco_de_dados.String(500), nullable=True)
    prazo = banco_de_dados.Column(banco_de_dados.Date, nullable=True)
    usuario_id = banco_de_dados.Column(banco_de_dados.Integer, banco_de_dados.ForeignKey('usuario.id'))
