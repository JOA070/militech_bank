def depositar(saldo, deposito):
    if deposito <= 0:
        print("Valor inválido para depósito!")
        return saldo
    
    saldo = saldo + deposito
    return saldo

def sacar(saldo, saque):
    if saque > saldo or saque <= 0:
        print("Valor inválido para retirada!")
        return saldo
    
    saldo = saldo - saque
    return saldo

def consultarSaldo(saldo):
    print("Saldo da conta: R$", saldo)

def transferir(saldo_origem, saldo_destino, valor):
    if valor > saldo_origem or valor <= 0:
        print("Valor inválido para transferência!")
        return saldo_origem, saldo_destino

    saldo_origem = saldo_origem - valor
    saldo_destino = saldo_destino + valor
    print("Transferência realizada com sucesso!")

    return saldo_origem, saldo_destino