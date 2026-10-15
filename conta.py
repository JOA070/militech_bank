from datetime import date

def calcular_meses_completos(hoje, ultima_data):    # Calcula a diferença entre os meses e anos das duas datas
    meses = (hoje.year - ultima_data.year) * 12
    meses += hoje.month - ultima_data.month

    if hoje.day < ultima_data.day:      # Desconsidera o último mês se ele ainda não estiver completo
        meses -= 1

    return meses


def depositar(conta, deposito):
    # Conta salário não permite depósitos comuns
    if conta["tipo"] == "salario":
        print("Operação não permitida para esse tipo de conta!")
        return conta

    # Verifica se o valor do depósito é válido
    if deposito <= 0:
        print("Valor inválido para depósito!")
        return conta

    conta["saldo"] += deposito  # Adiciona o valor ao saldo
    conta["ultima_movimentacao"] = date.today()  # Registra a data da movimentação

    return conta


def sacar(conta, saque):
    # Verifica se o saque é maior que o saldo ou se é menor ou igual a zero
    if saque > conta["saldo"] or saque <= 0:
        print("Valor inválido para retirada!")
        return conta

    conta["saldo"] -= saque     # Retira o valor do saldo
    conta["ultima_movimentacao"] = date.today()   # Registra a data da movimentação
    return conta


def consultarSaldo(conta):
    print("Saldo da conta: R$", conta["saldo"])     # Mostra o saldo atual da conta


def transferir(conta_origem, conta_destino, valor):
    # Verifica se o valor é inválido ou maior que o saldo da origem
    if valor > conta_origem["saldo"] or valor <= 0:
        print("Valor inválido para transferência!")
        return conta_origem, conta_destino

    conta_origem["saldo"] -= valor      # Retira o dinheiro da conta de origem
    conta_destino["saldo"] += valor     # Adiciona o dinheiro na conta de destino

    # Registra a data da movimentação nas duas contas
    data_atual = date.today()
    conta_origem["ultima_movimentacao"] = data_atual
    conta_destino["ultima_movimentacao"] = data_atual

    print("Transferência realizada com sucesso!")
    return conta_origem, conta_destino


def receber_salario(conta):
    # Só contas do tipo salário podem receber o salário
    if conta["tipo"] != "salario":
        return conta

    # O salário mensal da conta salário é fixo em R$ 2.500
    salario = 2500

    hoje = date.today()

    # Recupera a data do último recebimento
    ultima_data = conta["ultima_movimentacao"]

    meses = calcular_meses_completos(hoje, ultima_data)     # Verifica quantos meses completos se passaram

    if meses >= 1:  # Deposita o salário se já passou pelo menos um mês completo
        conta["saldo"] += salario     
        conta["ultima_movimentacao"] = hoje     # Atualiza a data do último recebimento
        print("Salário de R$ 2500,00 recebido!")
    return conta


def aplicar_rendimento(conta):
    # O rendimento só é aplicado para contas poupança
    if conta["tipo"] != "poupanca":
        return conta

    hoje = date.today()
    # Recupera a data da última movimentação
    ultima_data = conta["ultima_movimentacao"]

    meses = calcular_meses_completos(hoje, ultima_data) # Verifica quantos meses completos se passaram

    # Aplica 1% de rendimento para cada mês completo
    for i in range(meses):
        conta["saldo"] *= 1.01

    # Atualiza a data depois de aplicar o rendimento
    if meses > 0:
        conta["ultima_movimentacao"] = hoje
    return conta
