from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializa o objeto SQLAlchemy
banco_de_dados = SQLAlchemy()

def create_app():
    """Cria e configura o aplicativo Flask."""
    app = Flask(__name__)

    # Configurações do aplicativo
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Substitua por uma chave segura
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'  # Ou outro banco (PostgreSQL, MySQL)

    # Inicializa o SQLAlchemy com o aplicativo
    banco_de_dados.init_app(app)

    # Importa rotas e modelos no contexto da aplicação
    with app.app_context():
        from models import Usuario, Tarefa
        banco_de_dados.create_all()  # Cria as tabelas no banco

    return app
