from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Caixas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Caixas {self.tipo} - {self.valor}>'
