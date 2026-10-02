from datetime import date


def depositar(conta, deposito):

    # Conta salário não permite depósitos comuns
    if conta["tipo"] == "salario":
        print("Operação não permitida para esse tipo de conta!")
        return conta

    # Verifica se o valor do depósito é válido
    elif deposito <= 0:
        print("Valor inválido para depósito!")
        return conta

    # Adiciona o valor ao saldo
    conta["saldo"] = conta["saldo"] + deposito

    # Registra a data da movimentação
    conta["ultima_movimentacao"] = date.today().strftime("%Y-%m-%d")

    return conta


def sacar(conta, saque):

    # Verifica se o saque é maior que o saldo ou se é menor ou igual a zero
    if saque > conta["saldo"] or saque <= 0:
        print("Valor inválido para retirada!")
        return conta

    # Retira o valor do saldo
    conta["saldo"] = conta["saldo"] - saque

    # Registra a data da movimentação
    conta["ultima_movimentacao"] = date.today().strftime("%Y-%m-%d")

    return conta


def consultarSaldo(conta):

    # Mostra o saldo atual da conta
    print("Saldo da conta: R$", conta["saldo"])


def transferir(conta_origem, conta_destino, valor):

    # Verifica se o valor é inválido ou maior que o saldo da origem
    if valor > conta_origem["saldo"] or valor <= 0:
        print("Valor inválido para transferência!")
        return conta_origem, conta_destino

    # Retira o dinheiro da conta de origem
    conta_origem["saldo"] = conta_origem["saldo"] - valor

    # Adiciona o dinheiro na conta de destino
    conta_destino["saldo"] = conta_destino["saldo"] + valor

    # Registra a data da movimentação nas duas contas
    data_atual = date.today().strftime("%Y-%m-%d")

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

    # Calcula quantos meses completos se passaram
    meses = (hoje.year - ultima_data.year) * 12
    meses = meses + hoje.month - ultima_data.month

    # Se ainda não chegou ao mesmo dia do mês,
    # significa que o mês ainda não está completo
    if hoje.day < ultima_data.day:
        meses = meses - 1

    # Se passou pelo menos um mês, recebe o salário
    if meses >= 1:
        conta["saldo"] = conta["saldo"] + salario

        # Atualiza a data do último recebimento
        conta["ultima_movimentacao"] = hoje

        print("Salário de R$ 2500,00 recebido!")

    return conta


def aplicar_rendimento(conta):

    # O rendimento só é aplicado para contas poupança
    if conta["tipo"] != "poupanca":
        return conta

    hoje = date.today()

    # Recupera a data da última movimentação
    ultima_data = date.fromisoformat(conta["ultima_movimentacao"])

    # Calcula a quantidade de meses completos sem movimentação
    meses = (hoje.year - ultima_data.year) * 12
    meses = meses + hoje.month - ultima_data.month

    # Se o dia atual ainda não chegou ao dia da última movimentação,
    # o último mês ainda não está completo
    if hoje.day < ultima_data.day:
        meses = meses - 1

    # Aplica 1% de rendimento para cada mês completo
    for i in range(meses):
        conta["saldo"] = conta["saldo"] * 1.01

    # Atualiza a data depois de aplicar o rendimento
    if meses > 0:
        conta["ultima_movimentacao"] = hoje.strftime("%Y-%m-%d")

    return conta
