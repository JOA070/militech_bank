import random
import json

clientes = []
contas = []

def cadastrar_cliente(nome, cpf):
    cliente = (nome, cpf)
    clientes.append(cliente)

    for i in range(len(clientes)):
        for j in range(i + 1, len(clientes)):
            if clientes[i][0] > clientes[j][0]:
                clientes[i], clientes[j] = clientes[j], clientes[i]

    return cliente

def criar_conta(cpf, tipo_conta, saldo_inicial, agencia):
    numero_conta = random.randint(100000, 999999)
    conta = (cpf, numero_conta, tipo_conta, saldo_inicial, agencia)
    contas.append(conta)

    for i in range(len(contas)):
        for j in range(i + 1, len(contas)):
            if contas[i][0] > contas[j][0]:
                contas[i], contas[j] = contas[j], contas[i]

    return conta

def salvar_clientes():
    with open("clientes.json", "w") as arquivo:
        json.dump(clientes, arquivo)

def carregar_clientes():
    try:
        with open("clientes.json", "r") as arquivo:
            dados = json.load(arquivo)
            clientes.clear()

            for cliente in dados:
                clientes.append(tuple(cliente))

            for i in range(len(clientes)):
                for j in range(i + 1, len(clientes)):
                    if clientes[i][0] > clientes[j][0]:
                        clientes[i], clientes[j] = clientes[j], clientes[i]

    except FileNotFoundError:
        pass

def salvar_contas():
    with open("contas.json", "w") as arquivo:
        json.dump(contas, arquivo)

def carregar_contas():
    try:
        with open("contas.json", "r") as arquivo:
            dados = json.load(arquivo)
            contas.clear()

            for conta in dados:
                contas.append(tuple(conta))

            for i in range(len(contas)):
                for j in range(i + 1, len(contas)):
                    if contas[i][0] > contas[j][0]:
                        contas[i], contas[j] = contas[j], contas[i]

    except FileNotFoundError:
        pass
