from cliente import (cadastrar_cliente,criar_conta,clientes,contas,carregar_clientes,carregar_contas,salvar_clientes,salvar_contas,)
from conta import (depositar,sacar,transferir,consultarSaldo,receber_salario,aplicar_rendimento,)
from menu import menu
from agencias import listar_agencias
from datetime import date
from functools import reduce
import re


def validar_cpf(cpf):
    cpf_limpo = re.sub(r"\D", "", cpf)         # Remove pontos, traços e caracteres que não sejam números

    if len(cpf_limpo) != 11 or cpf_limpo == cpf_limpo[0] * 11:      # O CPF deve ter 11 dígitos e não pode conter todos os dígitos iguais
        return False
    numeros = [int(digito) for digito in cpf_limpo]     # Converte cada dígito do CPF para um número inteiro

    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += numeros[i] * (10 - i)

    verificador1 = (soma * 10 % 11) % 10

    if numeros[9] != verificador1:
        return False

    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += numeros[i] * (11 - i)

    verificador2 = (soma * 10 % 11) % 10

    if numeros[10] != verificador2:
        return False
    return True


def buscar_conta():
    # Permite localizar uma conta pelo CPF ou pelo número da conta
    escolha = input(
        "Deseja procurar a conta por:\n"
        "1 - CPF\n"
        "2 - Número da conta\n"
        "Escolha: "
    )

    if escolha == "1":
        cpf = re.sub(r"\D", "", input("Digite o CPF: "))

        for conta in contas:
            if conta["cpf"] == cpf:
                return conta

        print("Conta não encontrada.")
        return None

    if escolha == "2":
        try:
            numero_conta = int(input("Digite o número da conta: "))
        except ValueError:
            print("Digite apenas números.")
            return None

        for conta in contas:
            if conta["numero_conta"] == numero_conta:
                return conta

        print("Conta não encontrada.")
        return None

    print("Opção inválida!")
    return None


def atualizar_contas_automaticamente():
    # Carrega os dados salvos antes de iniciar o programa
    carregar_clientes()
    carregar_contas()

    # Verifica se alguma conta salário já completou um mês
    for conta in contas:
        if conta["tipo"] == "salario":

            # Garante que a data exista e seja um objeto date
            if "ultima_movimentacao" not in conta:
                conta["ultima_movimentacao"] = date.today()
            elif isinstance(conta["ultima_movimentacao"], str):
                conta["ultima_movimentacao"] = date.fromisoformat(
                    conta["ultima_movimentacao"]
                )

            saldo_anterior = conta["saldo"]
            receber_salario(conta)

            # Salva apenas se o salário realmente foi depositado
            if conta["saldo"] != saldo_anterior:
                salvar_contas()

    # Verifica os rendimentos das contas poupança
    for conta in contas:
        if conta["tipo"] == "poupanca":

            # Garante que a data exista e seja um objeto date
            if "ultima_movimentacao" not in conta:
                conta["ultima_movimentacao"] = date.today()
            elif isinstance(conta["ultima_movimentacao"], str):
                conta["ultima_movimentacao"] = date.fromisoformat(
                    conta["ultima_movimentacao"]
                )

            saldo_anterior = conta["saldo"]
            aplicar_rendimento(conta)

            # Salva apenas se houve rendimento
            if conta["saldo"] != saldo_anterior:
                salvar_contas()


def cadastrar_cliente_e_conta():
    nome = input("Digite o nome do cliente: ")

    # Continua solicitando o CPF até receber um válido
    while True:
        cpf = input("Informe o CPF: ")

        if validar_cpf(cpf):
            break

        print("CPF inválido! Digite um CPF correto com 11 dígitos.")

    # Armazena o CPF somente com números
    cpf = re.sub(r"\D", "", cpf)

    # Solicita uma agência válida
    while True:
        try:
            opcao_agencia = int(input(
                "Qual agência deseja?\n"
                "1 - Militech Central\n"
                "2 - Militech Corpo Plaza\n"
            ))

            if opcao_agencia in [1, 2]:
                break

            print("Opção inválida! Digite 1 ou 2.")

        except ValueError:
            print("Digite apenas 1 ou 2.")

    # Solicita um tipo de conta válido
    while True:
        try:
            opcao_tipo = int(input(
                "Qual tipo de conta deseja?\n"
                "1 - Poupança\n"
                "2 - Corrente\n"
                "3 - Salário\n"
            ))

            if opcao_tipo in [1, 2, 3]:
                break

            print("Opção inválida! Digite 1, 2 ou 3.")

        except ValueError:
            print("Digite apenas 1, 2 ou 3.")

    # Converte a opção numérica para o nome usado no sistema
    tipos = {
        1: "poupanca",
        2: "corrente",
        3: "salario",
    }

    tipo_conta = tipos[opcao_tipo]

    # O número da agência corresponde à opção selecionada
    agencia = opcao_agencia
    saldo_inicial = 0

    # Cadastra o cliente e cria sua conta
    cadastrar_cliente(nome, cpf)
    criar_conta(cpf, tipo_conta, saldo_inicial, agencia)

    # Localiza a conta recém-criada para registrar os dados iniciais
    for conta in contas:
        if conta["cpf"] == cpf and conta["tipo"] == tipo_conta:

            # Conta salário possui salário fixo de R$ 2.500
            if tipo_conta == "salario":
                conta["salario"] = 2500

            # A data inicial serve como referência para o primeiro mês
            if "ultima_movimentacao" not in conta:
                conta["ultima_movimentacao"] = date.today()

            break

    # Salva as alterações nos arquivos JSON
    salvar_contas()
    salvar_clientes()


def listar_clientes():
    print("\n--- CLIENTES CADASTRADOS ---")

    for cliente in clientes:
        print("Cliente:", cliente["nome"])
        print("CPF:", cliente["cpf"])


def listar_contas():
    print("\n--- CONTAS CADASTRADAS ---")

    for conta in contas:
        print("Número da Conta:", conta["numero_conta"])
        print("CPF da Conta:", conta["cpf"])
        print("Tipo da Conta:", conta["tipo"])
        print("-" * 20)


def realizar_deposito():
    conta = buscar_conta()

    if conta is None:
        return

    try:
        deposito = float(input("Digite o valor do depósito: R$ "))
    except ValueError:
        print("Valor inválido! Digite um número.")
        return

    saldo_anterior = conta["saldo"]

    # A função recebe a conta inteira e atualiza seu saldo
    depositar(conta, deposito)

    # Só salva e confirma se o saldo realmente mudou
    if conta["saldo"] != saldo_anterior:
        salvar_contas()
        print("Depósito realizado com sucesso!")


def realizar_saque():
    conta = buscar_conta()

    if conta is None:
        return

    try:
        saque = float(input("Digite o valor do saque: R$ "))
    except ValueError:
        print("Valor inválido! Digite um número.")
        return

    saldo_anterior = conta["saldo"]

    # A função valida o saque e atualiza o saldo
    sacar(conta, saque)

    # Só salva e confirma se o saldo realmente mudou
    if conta["saldo"] != saldo_anterior:
        salvar_contas()
        print("Saque realizado com sucesso!")


def realizar_transferencia():
    print("\n--- CONTA DE ORIGEM ---")
    conta_origem = buscar_conta()

    if conta_origem is None:
        return

    print("\n--- CONTA DE DESTINO ---")
    conta_destino = buscar_conta()

    if conta_destino is None:
        return

    # Impede transferências para a própria conta
    if conta_origem is conta_destino:
        print("A conta de origem e destino devem ser diferentes.")
        return

    try:
        valor = float(input("Digite o valor da transferência: R$ "))
    except ValueError:
        print("Valor inválido! Digite um número.")
        return

    saldo_origem = conta_origem["saldo"]
    saldo_destino = conta_destino["saldo"]

    # Envia as duas contas e o valor para a função de transferência
    transferir(conta_origem, conta_destino, valor)

    # Salva apenas se algum dos saldos foi alterado
    if (
        conta_origem["saldo"] != saldo_origem
        or conta_destino["saldo"] != saldo_destino
    ):
        salvar_contas()


def consultar_saldo_conta():
    conta = buscar_conta()

    if conta is None:
        return

    consultarSaldo(conta)


def gerar_relatorio():
    print("\n--- RELATÓRIO DO BANCO E AGÊNCIAS ---")

    # Soma os saldos de todas as contas usando reduce
    saldo_total = reduce(
        lambda total, conta: total + conta["saldo"],
        contas,
        0
    )

    # Filtra as contas pertencentes a cada agência
    contas_agencia1 = list(
        filter(lambda conta: conta["agencia"] == 1, contas)
    )

    contas_agencia2 = list(
        filter(lambda conta: conta["agencia"] == 2, contas)
    )

    # Soma os saldos de cada agência usando reduce
    total_agencia1 = reduce(
        lambda total, conta: total + conta["saldo"],
        contas_agencia1,
        0
    )

    total_agencia2 = reduce(
        lambda total, conta: total + conta["saldo"],
        contas_agencia2,
        0
    )

    # Conta quantas contas existem em cada agência
    quantidade_agencia1 = len(contas_agencia1)
    quantidade_agencia2 = len(contas_agencia2)

    print("Militech Central:")
    print(" - Total de Contas:", quantidade_agencia1)
    print(" - Montante Acumulado: R$", total_agencia1)
    print("-" * 30)

    print("Militech Corpo Plaza:")
    print(" - Total de Contas:", quantidade_agencia2)
    print(" - Montante Acumulado: R$", total_agencia2)
    print("-" * 30)

    # Compara a quantidade de contas de cada agência
    if quantidade_agencia1 > quantidade_agencia2:
        print("Agência com mais contas: Militech Central")

    elif quantidade_agencia2 > quantidade_agencia1:
        print("Agência com mais contas: Militech Corpo Plaza")

    else:
        print("Ambas as agências possuem a mesma quantidade de contas.")

    print("\nTOTAL GERAL DEPOSITADO NO BANCO: R$", saldo_total)


# Atualiza os dados e aplica os pagamentos/rendimentos antes do menu
atualizar_contas_automaticamente()

opcao = ""

while opcao != "0":
    opcao = menu()

    # 1 - Cadastrar cliente e conta
    if opcao == "1":
        cadastrar_cliente_e_conta()

    # 2 - Listar agências
    elif opcao == "2":
        listar_agencias()

    # 3 - Listar clientes
    elif opcao == "3":
        listar_clientes()

    # 4 - Listar contas
    elif opcao == "4":
        listar_contas()

    # 5 - Depositar
    elif opcao == "5":
        realizar_deposito()

    # 6 - Sacar
    elif opcao == "6":
        realizar_saque()

    # 7 - Transferir
    elif opcao == "7":
        realizar_transferencia()

    # 8 - Consultar saldo
    elif opcao == "8":
        consultar_saldo_conta()

    # 9 - Exibir relatório geral e por agência
    elif opcao == "9":
        gerar_relatorio()

    # 0 - Encerrar o programa
    elif opcao == "0":
        print("Programa encerrado.")

    else:
        print("Opção inválida!")
