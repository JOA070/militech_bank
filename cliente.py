def cadastrar_cliente(nome,cpf):
  return nome,cpf

def consultar_cliente(cpf):
  if cpf == cpf_cadastrado:
    print ('O cliente tem conta') 
  else:
    print ('Cliente não encontrado') 

def criar_conta(cpf,numero_conta,tipo_conta,saldo_inicial):
  return cpf,numero_conta,tipo_conta,saldo_inicial
