from flask import Flask
from models import db, criar_banco
from routes import init_routes

def create_app():
    # Inicializa a aplicação Flask
    app = Flask(__name__)
    
    # Configurações da aplicação
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'sua_chave_secreta'

    # Inicializa o banco de dados
    db.init_app(app)
    
    # Cria o banco de dados e as tabelas
    with app.app_context():
        db.create_all()
    
    # Configura as rotas
    init_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)