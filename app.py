import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Gerar uma chave secreta aleatória
if os.environ.get('SECRET_KEY') is None:
    secret_key = secrets.token_urlsafe(32)
    # Imprima a chave secreta para que você possa defini-la como uma variável de ambiente
    print(f"Defina a seguinte chave secreta como uma variável de ambiente: {secret_key}")
else:
    secret_key = os.environ.get('SECRET_KEY')

aplicacao = Flask(__name__)
aplicacao.config['SECRET_KEY'] = secret_key
aplicacao.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'  # Ou configure para PostgreSQL

banco_de_dados = SQLAlchemy()
banco_de_dados.init_app(aplicacao)

from models import Usuario, Tarefa

# --- Rotas ---

@aplicacao.route('/')
def index():
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
        tarefas = Tarefa.query.filter_by(usuario_id=usuario.id).all()
        return render_template('index.html', tarefas=tarefas, usuario=usuario)
    else:
        return redirect(url_for('login'))

@aplicacao.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):  # Verifica o hash da senha
            session['usuario_id'] = usuario.id
            return redirect(url_for('index'))
        else:
            flash('Credenciais inválidas.')
    return render_template('login.html')

@aplicacao.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            flash('Email já cadastrado.')
        else:
            senha_hash = generate_password_hash(senha)  # Gera o hash da senha
            novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
            banco_de_dados.session.add(novo_usuario)
            banco_de_dados.session.commit()
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('login'))
    return render_template('cadastro.html')

@aplicacao.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('index'))

# ... (código das rotas /criar, /editar e /excluir) ...

if __name__ == '__main__':
    with aplicacao.app_context():
        banco_de_dados.create_all()
    from app import aplicacao
    aplicacao.run(debug=True)