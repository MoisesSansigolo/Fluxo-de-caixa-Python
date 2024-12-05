# controllers/home_controller.py
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import or_
from model.models import db, Caixas  # Importa o db e o modelo Caixas

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    tipo = request.args.get('tipo', '')
    if tipo:
        caixas = Caixas.query.filter(or_(Caixas.tipo.ilike(f'%{tipo}%'))).all()
    else:
        caixas = Caixas.query.all()

    receitas = sum(caixa.valor for caixa in caixas if caixa.status == 1)
    despesas = sum(caixa.valor for caixa in caixas if caixa.status == 0)
    valor_total = receitas - despesas

    return render_template('index.html', receitas=receitas, despesas=despesas,
                           valor_total=valor_total, extrato=caixas, termo_busca=tipo)

@home_bp.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        tipo = request.body['tipo']
        valor = float(request.body['valor'])
        status = int(request.body['status'])

        nova_conta = Caixas(tipo=tipo, valor=valor, status=status)

        db.session.add(nova_conta)
        db.session.commit()
        return redirect(url_for('home.index'))

    return render_template('adicionar.html')

@home_bp.route('/excluir/<int:id>', methods=['GET'])
def excluir(id):
    conta = Caixas.query.get(id)
    if conta:
        db.session.delete(conta)
        db.session.commit()

    return redirect(url_for('home.index'))
