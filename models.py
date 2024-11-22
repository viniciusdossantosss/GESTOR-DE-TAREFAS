from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

banco_de_dados = SQLAlchemy()

class Usuario(banco_de_dados.Model):
    identificador = banco_de_dados.Column(banco_de_dados.Integer, primary_key=True)
    nome = banco_de_dados.Column(banco_de_dados.String(80), nullable=False)
    email = banco_de_dados.Column(banco_de_dados.String(120), unique=True, nullable=False)
    senha = banco_de_dados.Column(banco_de_dados.String(120), nullable=False)
    tarefas = banco_de_dados.relationship('Tarefa', backref='usuario', lazy=True)

class Tarefa(banco_de_dados.Model):
    identificador = banco_de_dados.Column(banco_de_dados.Integer, primary_key=True)
    titulo = banco_de_dados.Column(banco_de_dados.String(100), nullable=False)
    descricao = banco_de_dados.Column(banco_de_dados.String(200))
    prazo = banco_de_dados.Column(banco_de_dados.Date)
    status = banco_de_dados.Column(banco_de_dados.String(20), default='pendente')
    data_criacao = banco_de_dados.Column(banco_de_dados.DateTime, default=datetime.utcnow)
    usuario_identificador = banco_de_dados.Column(banco_de_dados.Integer, banco_de_dados.ForeignKey('usuario.identificador'), nullable=False)