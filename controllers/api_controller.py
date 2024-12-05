from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from model.models import db, Caixas

api_bp = Blueprint('api', __name__)

# Define a rota para listar os caixas
@api_bp.route('/caixas', methods=['GET'])
def api_index():
    tipo = request.args.get('tipo', '')
    
    # Filtra os caixas pela tipo, caso especificado
    if tipo:
        caixas = Caixas.query.filter(or_(Caixas.tipo.ilike(f'%{tipo}%'))).all()
    else:
        caixas = Caixas.query.all()

    receitas = sum(caixa.valor for caixa in caixas if caixa.status == 1)
    despesas = sum(caixa.valor for caixa in caixas if caixa.status == 0)
    valor_total = receitas - despesas

    data = {
        'receitas': receitas,
        'despesas': despesas,
        'valor_total': valor_total,
        'extrato': [
            {'id': caixa.id, 'tipo': caixa.tipo, 'valor': caixa.valor, 'status': caixa.status}
            for caixa in caixas
        ]
    }
    return jsonify(data)

# Define a rota para cadastrar um novo caixa
@api_bp.route('/caixas', methods=['POST'])
def api_cadastrar():
    data = request.json

    tipo = data.get('tipo')
    valor = data.get('valor')
    status = data.get('status')

    if not tipo or valor is None or status is None:
        return jsonify({'error': 'Dados inválidos'}), 400

    try:
        valor = float(valor)
        status = int(status)
    except ValueError:
        return jsonify({'error': 'Valor e status devem ser números'}), 400

    novo_caixa = Caixas(tipo=tipo, valor=valor, status=status)
    db.session.add(novo_caixa)
    db.session.commit()

    return jsonify({
        'id': novo_caixa.id,
        'tipo': novo_caixa.tipo,
        'valor': novo_caixa.valor,
        'status': novo_caixa.status
    })

# Define a rota para excluir um caixa pelo id
@api_bp.route('/caixas/<int:id>', methods=['DELETE'])
def api_excluir(id):
    caixa = Caixas.query.get(id)
    if caixa:
        db.session.delete(caixa)
        db.session.commit()
        return jsonify({}), 204
    else:
        return jsonify({'error': 'Registro não encontrado'}), 404
