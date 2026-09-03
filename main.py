from cliente import cadastrar_cliente, criar_conta
from conta import depositar, sacar

nome = input("Digite o nome do cliente: ")
cpf = input("Digite o CPF do cliente: ")

cliente, cpf_cadastrado = cadastrar_cliente(nome, cpf)

numero_conta = 1
tipo_conta = "Corrente"
saldo_inicial = 0

cpf_conta, conta, tipoConta, saldo = criar_conta(cpf_cadastrado,numero_conta,tipo_conta,saldo_inicial)
deposito = float(input("Digite o valor do depósito: R$ "))

saldo = depositar(saldo, deposito)
saque = float(input("Digite o valor do saque: R$ "))
saldo = sacar(saldo, saque)

print("\n--- CLIENTE ---")
print("Nome:", cliente)
print("CPF:", cpf_cadastrado)

print("\n--- CONTA ---")
print("Número:", conta)
print("Tipo:", tipoConta)
print("Saldo:", saldo)
