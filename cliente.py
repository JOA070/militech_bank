import random
import json

clientes = []
contas = []

def cadastrar_cliente(nome,cpf):
  cliente = (nome,cpf)
  clientes.append(cliente)
  return cliente


def criar_conta(cpf,tipo_conta,saldo):
  numero_conta = random.randint(100000,999999)
  conta = (cpf,numero_conta,tipo_conta,saldo)
  consta.append(conta)
  return conta

def salvar_clientes(clientes):
  with open("clientes.json" , "w") as arquivo:
    json.dump(clientes, arquivo)


def carregar_clientes():
  try:
    with open("clientes.json" , "r") as arquivo:
      dados = json.load(arquivo)

      clientes.clear()
      for cliente in dados:
        clientes.append(cliente)
  except FileNotFoundError:
    pass

def salvar_contas(contas):
  with open("contas.json" , "w") as arquivo:
    json.dump(contas, arquivo)

def carregar_contas():
  try:
    with open("contas.json" , "r") as arquivo:
      dados = json.load(arquivo)

      contas.clear()

      for conta in dados:
        contas.append(conta)
  except FileNotFoundError:
    pass
