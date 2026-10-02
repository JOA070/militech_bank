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

    for cliente_atual in range(len(clientes)):   # Percorre as posicoes dos clientes
        for outro_cliente in range(cliente_atual + 1, len(clientes)):  # compara o cliente atual com os proximos clientes

            if clientes[cliente_atual]["nome"] > clientes[outro_cliente]["nome"]:  # verifica se os clientes estao fora de ordem alfabetica

                clientes[cliente_atual], clientes[outro_cliente] = clientes[outro_cliente], clientes[cliente_atual] # troca os clientes de posicao

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

    # ordena igual o anterior, a mudanca é que agora sao ordenacao de contas por cpf
    for conta_atual in range(len(contas)):

        for outra_conta in range(conta_atual + 1, len(contas)):

            if contas[conta_atual]["cpf"] > contas[outra_conta]["cpf"]:

                contas[conta_atual], contas[outra_conta] = contas[outra_conta], contas[conta_atual]

    return contas


def salvar_clientes():

    with open("clientes.json", "w") as arquivo: # Salva a lista de clientes no arquivo JSON

        json.dump(clientes, arquivo, indent=4)


def carregar_clientes():

    try:

        with open("clientes.json", "r") as arquivo: # Abre o arquivo JSON para recuperar os clientes salvos

            dados = json.load(arquivo)

            clientes.clear()

            for cliente in dados: # Adiciona os clientes carregados na lista

                clientes.append(cliente)

            for i in range(len(clientes)):

                for j in range(i + 1, len(clientes)):

                    if clientes[i]["nome"] > clientes[j]["nome"]:

                        clientes[i], clientes[j] = clientes[j], clientes[i]

    except FileNotFoundError:

        pass


def salvar_contas():

    dados = []

    for conta in contas: # Cria uma copia das contas para preparar os dados para o JSON

        conta_salvar = conta.copy()

        conta_salvar["ultima_movimentacao"] = conta_salvar["ultima_movimentacao"].isoformat() # Converte a data para texto, pois o JSON nao salva objetos date

        dados.append(conta_salvar)

    with open("contas.json", "w") as arquivo: # Salva as contas no arquivo JSON

        json.dump(dados, arquivo, indent=4)


def carregar_contas():

    try:

        with open("contas.json", "r") as arquivo: # Abre o arquivo JSON para recuperar as contas salvas

            dados = json.load(arquivo)

            contas.clear()

            for conta in dados: # Converte a data salva como texto novamente para date

                conta["ultima_movimentacao"] = date.fromisoformat(conta["ultima_movimentacao"])

                contas.append(conta)

            for i in range(len(contas)):

                for j in range(i + 1, len(contas)):

                    if contas[i]["cpf"] > contas[j]["cpf"]:

                        contas[i], contas[j] = contas[j], contas[i]

    except FileNotFoundError:

        pass
