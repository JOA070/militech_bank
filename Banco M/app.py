from analise import gerar_dashboard, calcular_saldo_total, calcular_saldo_medio
from flask import Flask, render_template, request, redirect, url_for
from cliente import Cliente, clientes, carregar_clientes, salvar_clientes
from conta import ContaCorrente, contas, carregar_contas, salvar_contas
import random

app = Flask(__name__)

def carregar_dados_sistema():
    # Carrega os clientes e contas usando os módulos POO
    carregar_clientes()
    carregar_contas()

@app.route('/')       
def index():
    # Carrega os dados atualizados do sistema
    carregar_dados_sistema()
    
    # Chama a função de relatório/dashboard que está no analise.py
    # Passando as listas globais de clientes e contas
    metricas_geral = gerar_dashboard(clientes, contas)
    
    from analise import listar_contas_positivas
    contas_positivas = listar_contas_positivas(contas)

    metricas = {
        "total_clientes": metricas_geral["total_clientes"],
        "saldo_total": metricas_geral["saldo_total"],
        "saldo_medio": metricas_geral["saldo_medio"],
        "maior_saldo": metricas_geral["maior_saldo"][0].saldo if metricas_geral["maior_saldo"] else 0,
        "menor_saldo": metricas_geral["menor_saldo"][0].saldo if metricas_geral["menor_saldo"] else 0
    }

    return render_template('index.html', 
                           clientes=clientes, 
                           contas=contas,
                           m=metricas, 
                           contas_positivas=contas_positivas)

@app.route('/deletar/<cpf>', methods=['POST'])
def deletar(cpf):
    global clientes, contas
    #Filtra objetos cujos CPFs não coincidem
    clientes = [c for c in clientes if c.cpf != cpf]
    contas = [conta for conta in contas if conta.cliente and conta.cliente.cpf != cpf]
    
    salvar_clientes()
    salvar_contas()
    return redirect(url_for('index'))

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    saldo = request.form.get('saldo')

    if nome and cpf and saldo:
        #Verifica se o cliente já existe como objeto
        cliente = next((c for c in clientes if c.cpf == cpf), None)
        if not cliente:
            novo_cliente = Cliente(nome, cpf)
            clientes.append(novo_cliente)
            salvar_clientes()
        else:
            novo_cliente = cliente

        #Cria uma nova conta corrente vinculada ao cliente via POO
        num_conta = random.randint(100000, 999999)
        nova_conta = ContaCorrente(num_conta, "corrente", float(saldo), 1, novo_cliente)
        contas.append(nova_conta)
        salvar_contas()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
