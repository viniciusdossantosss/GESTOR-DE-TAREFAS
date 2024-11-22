
from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Tarefa

def init_routes(app):
    @app.route('/')
    def home():
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = Usuario.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
            flash('Credenciais inválidas.')
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('login'))

    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        tarefas = Tarefa.query.all()
        return render_template('dashboard.html', tarefas=tarefas)

    @app.route('/criar_tarefa', methods=['GET', 'POST'])
    def criar_tarefa():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            titulo = request.form['titulo']
            descricao = request.form['descricao']
            tarefa = Tarefa(titulo=titulo, descricao=descricao)
            db.session.add(tarefa)
            db.session.commit()
            return redirect(url_for('dashboard'))
        return render_template('criar_tarefa.html')

    @app.route('/editar_tarefa/<int:id>', methods=['GET', 'POST'])
    def editar_tarefa(id):
        tarefa = Tarefa.query.get_or_404(id)
        if request.method == 'POST':
            tarefa.titulo = request.form['titulo']
            tarefa.descricao = request.form['descricao']
            tarefa.status = request.form['status']
            db.session.commit()
            return redirect(url_for('dashboard'))
        return render_template('editar_tarefa.html', tarefa=tarefa)

    @app.route('/excluir_tarefa/<int:id>')
    def excluir_tarefa(id):
        tarefa = Tarefa.query.get_or_404(id)
        db.session.delete(tarefa)
        db.session.commit()
        return redirect(url_for('dashboard'))
