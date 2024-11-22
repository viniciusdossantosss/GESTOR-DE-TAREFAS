
from flask import Flask
from models import db, criar_banco
from routes import init_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'sua_chave_secreta'

db.init_app(app)
init_routes(app)

if __name__ == '__main__':
    with app.app_context():
        criar_banco()
    app.run(debug=True)
