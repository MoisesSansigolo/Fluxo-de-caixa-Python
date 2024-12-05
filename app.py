from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from controllers.home_controller import home_bp
from model.models import db
from controllers.api_controller import api_bp 

app = Flask(__name__, static_folder='static')
app.secret_key = 'Jon160616Ba$'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@NAVANTB0641/Caixas?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

CORS(app, resources={r"/api/*": {"origins": "*"}})

def capitalize_words(s):
    return ' '.join(word.capitalize() for word in s.split())

app.jinja_env.globals['capitalize_words'] = capitalize_words
app.register_blueprint(home_bp)
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
