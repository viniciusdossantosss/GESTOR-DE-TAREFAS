from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'  # Usando SQLite

db = SQLAlchemy(app)

from models import Usuario, Tarefa  # Importe as classes do models.py

# --- Rotas ---

@app.route('/')
def index():
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
        tarefas = Tarefa.query.filter_by(usuario_id=usuario.id).all()
        return render_template('index.html', tarefas=tarefas, usuario=usuario)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
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
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
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
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('login'))

@app.route('/criar', methods=['GET', 'POST'])
def criar_tarefa():
    if 'usuario_id' in session:
        if request.method == 'POST':
            titulo = request.form['titulo']
            descricao = request.form['descricao']
            prazo = request.form['prazo']
            if prazo:
                prazo = datetime.strptime(prazo, '%Y-%m-%d').date()
            nova_tarefa = Tarefa(titulo=titulo, descricao=descricao, prazo=prazo, usuario_id=session['usuario_id'])
            db.session.add(nova_tarefa)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('criar_tarefa.html')  # Crie este template!
    return redirect(url_for('login'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_tarefa(id):
    if 'usuario_id' in session:
        tarefa = Tarefa.query.get_or_404(id)
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
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('editar_tarefa.html', tarefa=tarefa)  # Crie este template!
    return redirect(url_for('login'))

@app.route('/excluir/<int:id>')
def excluir_tarefa(id):
    if 'usuario_id' in session:
        tarefa = Tarefa.query.get_or_404(id)
        if tarefa.usuario_id != session['usuario_id']:
            flash('Você não tem permissão para excluir esta tarefa.')
            return redirect(url_for('index'))
        db.session.delete(tarefa)
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)