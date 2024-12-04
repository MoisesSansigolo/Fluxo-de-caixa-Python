
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_


app = Flask(__name__)
app.secret_key = 'Jon160616Ba$'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@NAVANTB0641/Caixas?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Caixas(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   tipo = db.Column(db.String(100), nullable=False)
   valor = db.Column(db.Float, nullable=False)
   status = db.Column(db.String(20), nullable=False)

   def __repr__(self):
      return f'<Caixas {self.tipo} - {self.valor}>'

@app.route('/')
def index():
   tipo = request.args.get('tipo', '')

   if tipo:
      caixas = Caixas.query.filter(or_(Caixas.tipo.ilike(f'%{tipo}%'))).all()
   else:
      caixas = Caixas.query.all()

   receitas = sum(caixa.valor for caixa in caixas if caixa.status == 1)
   despesas = sum(caixa.valor for caixa in caixas if caixa.status == 0)
   valor_total = receitas - despesas

   return render_template('index.html', receitas = receitas, despesas = despesas, 
                          valor_total = valor_total, extrato = caixas, termo_busca = tipo)

   

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
   if request.method == 'POST':
      tipo = request.form['tipo']
      valor = float(request.form['valor'])
      status = int(request.form['status'])

      nova_conta = Caixas(tipo=tipo, valor=valor, status=status)

      db.session.add(nova_conta)
      db.session.commit()
      return redirect(url_for('index'))

   return render_template('adicionar.html')

@app.route('/excluir/<int:id>', methods=['GET'])
def excluir(id):
   conta = Caixas.query.get(id)
   if conta:
      db.session.delete(conta)
      db.session.commit()

   return redirect(url_for('index'))

def capitalize_words(s):
    return ' '.join(word.capitalize() for word in s.split())
app.jinja_env.globals['capitalize_words'] = capitalize_words


if __name__ == '__main__':
   app.run(debug=True)