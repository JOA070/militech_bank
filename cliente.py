import random
import json
from datetime import date

clientes = []
def cadastrar_cliente(nome, cpf):

    cliente = {
        "nome": nome,
        "cpf": cpf
    }

    clientes.append(cliente)
    clientes.sort(key=lambda cliente: cliente["nome"]) # Ordena os clientes alfabeticamente pelo nome.
    return clientes

contas = []
def criar_conta(cpf, tipo_conta, saldo_inicial, agencia):

    conta = {
        "cpf": cpf,
        "numero_conta": random.randint(100000, 999999),
        "tipo": tipo_conta,
        "saldo": saldo_inicial,
        "agencia": agencia,
        "ultima_movimentacao": date.today()
    }
    contas.append(conta)
    contas.sort(key=lambda conta: conta["cpf"])  # Ordena as contas pelo CPF do titular.
    return contas

def salvar_clientes():
    with open("clientes.json", "w") as arquivo: # Abre o arquivo para escrita e salva os clientes em formato JSON.
        json.dump(clientes, arquivo, indent=4)


def carregar_clientes():

    try:
        with open("clientes.json", "r") as arquivo: # Abre o arquivo para leitura e recupera os clientes salvos.
            dados = json.load(arquivo)

            clientes.clear()     # Remove os dados atuais antes de carregar os dados do arquivo.
            clientes.extend(dados)    # Adiciona todos os clientes carregados à lista.
            clientes.sort(key=lambda cliente: cliente["nome"])    # Mantém os clientes em ordem alfabética.

    except FileNotFoundError:
        pass    # Se o arquivo ainda não existir, não faz nada.


def salvar_contas():
            # Cria uma nova lista para preparar as contas para o JSON.
    dados = [      
        {**conta, "ultima_movimentacao": conta["ultima_movimentacao"].isoformat()} 
        for conta in contas
    ]
    with open("contas.json", "w") as arquivo: # Salva os dados preparados no arquivo JSON
        json.dump(dados, arquivo, indent=4)

def carregar_contas():

    try:   # Abre o arquivo e recupera as contas salvas.
        with open("contas.json", "r") as arquivo: 
            dados = json.load(arquivo)

            contas.clear()    # Remove as contas atuais antes de carregar as salvas.

            for conta in dados: # Converte a data de texto para um objeto date.
                conta["ultima_movimentacao"] = date.fromisoformat(conta["ultima_movimentacao"])
            contas.extend(dados)    # Adiciona todos os dicionários de contas à lista.
            contas.sort(key=lambda conta: conta["cpf"])    # Ordena as contas pelo CPF do titular.

    except FileNotFoundError:
        pass    # Se o arquivo ainda não existir, não faz nada.
