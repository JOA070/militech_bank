import random
clientes = []
contas = []

def cadastrar_cliente(nome,cpf):
  cliente = [nome,cpf]
  clientes.append(cliente)
  return cliente


def criar_conta(cpf,numero_conta,tipo_conta,saldo_inicial):
  numero_conta = random.randint(100000,999999)
  conta = [cpf,numero_conta,tipo_conta,saldo_inicial] 
  consta.append(conta)
  return conta
