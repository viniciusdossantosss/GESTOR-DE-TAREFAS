from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

aplicacao = Flask(__name__)
aplicacao.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Substitua por uma chave secreta forte
aplicacao.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'

banco_de_dados = SQLAlchemy(aplicacao)

from models import Usuario, Tarefa

# --- Rotas ---

@aplicacao.route('/')
def index():
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
        tarefas = Tarefa.query.filter_by(usuario_id=usuario.id).all()
        return render_template('index.html', tarefas=tarefas, usuario=usuario)
    return render_template('index.html')  # Renderiza index.html mesmo se não estiver logado

@aplicacao.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            return redirect(url_for('index'))
        else:
            flash('Credenciais inválidas.')
    return redirect(url_for('index'))  # Redireciona para index.html após o login

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
            senha_hash = generate_password_hash(senha)
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

@aplicacao.route('/criar', methods=['GET', 'POST'])
def criar_tarefa():
    if 'usuario_id' in session:
        if request.method == 'POST':
            titulo = request.form['titulo']
            descricao = request.form['descricao']
            prazo = request.form['prazo']
            if prazo:
                prazo = datetime.strptime(prazo, '%Y-%m-%d').date()
            nova_tarefa = Tarefa(titulo=titulo, descricao=descricao, prazo=prazo, usuario_id=session['usuario_id'])
            banco_de_dados.session.add(nova_tarefa)
            banco_de_dados.session.commit()
            return redirect(url_for('index'))
        return render_template('criar_tarefa.html')
    return redirect(url_for('login'))

@aplicacao.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_tarefa(identificador):
    if 'usuario_id' in session:
        tarefa = Tarefa.query.get_or_404(identificador)
        if tarefa.usuario_id != session['usuario_id']:
            flash('Você não tem permissão para editar esta tarefa.')
            return redirect(url_for('index'))
        if request.method == 'POST':
            tarefa.titulo = request.form['titulo']
            tarefa.descricao = request.form['descricao']
            prazo = request.form['prazo']
            if prazo:
                tarefa.prazo = datetime.strptime(prazo, '%Y-%m-%d').date()
            else:
                tarefa.prazo = None
            tarefa.status = request.form['status']
            banco_de_dados.session.commit()
            return redirect(url_for('index'))
        return render_template('editar_tarefa.html', tarefa=tarefa)
    return redirect(url_for('login'))

@aplicacao.route('/excluir/<int:id>')
def excluir_tarefa(identificador):
    if 'usuario_id' in session:
        tarefa = Tarefa.query.get_or_404(identificador)
        if tarefa.usuario_id != session['usuario_id']:
            flash('Você não tem permissão para excluir esta tarefa.')
            return redirect(url_for('index'))
        banco_de_dados.session.delete(tarefa)
        banco_de_dados.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    with aplicacao.app_context():
        banco_de_dados.create_all()
    aplicacao.run(debug=True)