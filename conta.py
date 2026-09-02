def depositar(saldo, deposito):    
                if deposito <= 0:
                    print("Inválido")
                else:
                    saldo = saldo + deposito
                return(saldo)

def sacar(saldo, saque):
                if 0 < saque <= saldo:
                    saldo = saldo - saque
                else:
                    print("Saldo insuficiente")
                return(saldo)

def consultarSaldo(saldo):
                print("Saldo:",saldo)
