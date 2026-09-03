from cliente import consultar_cliente, cadastrar_cliente
from conta import depositar, sacar, consultarSaldo, criar_conta

cpf_cadastrado=0

nome=input(('Digite o nome de usuario:'))
cpf=int(input('Digite seu cpf:'))

consultar_cliente(cpf,cpf_cadastrado)

cpf_cadastrado=cpf

cadastro=cadastrar_cliente(nome, cpf)

saldo_conta = 0.0

deposito=float(input('Deposite seu saldo:'))
saldo_conta = depositar(saldo_conta, deposito)

saque=float(input('Digite o quanto gostaria de sacar:'))
saldo_conta= sacar(saldo_conta, saque)

consultarSaldo(saldo_conta)

print('Parabens, sua conta na Militech Bank foi criada com sucesso :3 Aqui vão suas informações:')
cpf_conta, num_conta, tipo, saldo_final = criar_conta(cpf, 1, 'Corrente', saldo_conta)

print("CPF:", cpf_conta)
print("Número da sua conta:", num_conta)
print("Tipo de conta:", tipo)
print("Saldo: R$", saldo_final)
