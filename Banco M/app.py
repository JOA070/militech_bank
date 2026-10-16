import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
ARQUIVO_JSON = 'dados.json'

def carregar_dados():
    try:
        with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_dados(clientes):
    with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(clientes, f, ensure_ascii=False, indent=4) 
@app.route('/')       
def index():
    clientes = carregar_dados()
    
    total_clientes = len(clientes)
    saldo_total = sum(c.get('saldo', 0) for c in clientes)
    saldo_medio = saldo_total / total_clientes if total_clientes > 0 else 0
    
    if clientes:
        maior_saldo = max(c.get('saldo', 0) for c in clientes)
        menor_saldo = min(c.get('saldo', 0) for c in clientes)
    else:
        maior_saldo = menor_saldo = 0

    contas_positivas = [c for c in clientes if c.get('saldo', 0) > 0]

    metricas = {
        "total_clientes": total_clientes,
        "saldo_total": saldo_total,
        "saldo_medio": saldo_medio,
        "maior_saldo": maior_saldo,
        "menor_saldo": menor_saldo
    }

    return render_template('index.html', 
                           clientes=clientes, 
                           m=metricas, 
                           contas_positivas=contas_positivas)

@app.route('/deletar/<cpf>', methods=['POST'])
def deletar(cpf):
    
    return redirect(url_for('index'))

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    saldo = request.form.get('saldo')

    if nome and cpf and saldo:
        clientes = carregar_dados()
        
        novo_cliente = {
            "nome": nome,
            "cpf": cpf,
            "saldo": float(saldo)
        }
        
        clientes.append(novo_cliente)
        salvar_dados(clientes)

    return redirect(url_for('index'))
def deletar(cpf):
    clientes = carregar_dados()
    clientes_atualizados = [c for c in clientes if c['cpf'] != cpf]
    salvar_dados(clientes_atualizados)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)













