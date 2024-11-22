from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    tarefas = db.relationship('Tarefa', backref='usuario', lazy=True)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    prazo = db.Column(db.Date)
    status = db.Column(db.String(20), default='pendente')
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)