from cliente import cadastrar_cliente, criar_conta, clientes, contas, carregar_clientes, carregar_contas, salvar_clientes, salvar_contas
from conta import depositar, sacar, transferir, consultarSaldo, receber_salario, aplicar_rendimento
from menu import menu
from agencias import listar_agencias
import re

def validar_cpf(cpf):
    # Remove pontos, traços e qualquer caractere que não seja número
    cpf_limpo = re.sub(r'\D', '', cpf)

    # Verifica se o CPF possui exatamente 11 números
    # e impede CPFs com todos os números iguais
    if len(cpf_limpo) != 11 or cpf_limpo == cpf_limpo[0] * 11:
        return False
    numeros = []
    # Transforma cada dígito do CPF em número inteiro
    for digito in cpf_limpo:
        numeros.append(int(digito))

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
# Carrega os dados salvos antes de iniciar o programa
carregar_clientes()
carregar_contas()

# Verifica automaticamente se alguma conta salário
# já completou um mês e precisa receber o salário
for conta in contas:

    if conta["tipo"] == "salario":

        # Se contas antigas não tiverem essa informação,
        # cria a data usando a data atual
        if "ultima_movimentacao" not in conta:
            conta["ultima_movimentacao"] = __import__("datetime").date.today().strftime("%Y-%m-%d")

        saldo_anterior = conta["saldo"]

        receber_salario(conta)

        # Salva somente se o salário realmente caiu
        if conta["saldo"] != saldo_anterior:
            salvar_contas()
# Verifica o rendimento das contas poupança
for conta in contas:

    if conta["tipo"] == "poupanca":

        saldo_anterior = conta["saldo"]

        aplicar_rendimento(conta)

        # Salva somente se houve rendimento
        if conta["saldo"] != saldo_anterior:
            salvar_contas()

opcao = ''
while opcao != '0':

    opcao = menu()

    # 1 - CADASTRAR CLIENTE E CONTA
    if opcao == '1':

        nome = input("Digite o nome do cliente: ")

        # Continua pedindo o CPF até o usuário informar um válido
        while True:

            cpf = input("Informe o CPF: ")
            if validar_cpf(cpf):
                break
            print("CPF inválido! Digite um CPF correto com 11 dígitos.")

        # Mantém somente os números do CPF
        cpf = re.sub(r'\D', '', cpf)

        # Escolha da agência
        while True:
            try:
                opcao_agencia = int(input(
                    "Qual agencia deseja?\n"
                    "1- Militech Central\n"
                    "2- Militech Corpo Plaza\n"
                ))
                if opcao_agencia == 1 or opcao_agencia == 2:
                    break
                print("Opção inválida! Digite 1 ou 2.")
            except ValueError:
                print("Digite apenas 1 ou 2.")

        # Escolha do tipo de conta
        while True:
            try:
                tipo_conta = int(input(
                    "Qual tipo de conta deseja?\n"
                    "1- Poupança\n"
                    "2- Corrente\n"
                    "3- Salário\n"
                ))
                if tipo_conta == 1 or tipo_conta == 2 or tipo_conta == 3:
                    break
                print("Opção inválida! Digite 1, 2 ou 3.")
            except ValueError:
                print("Digite apenas 1, 2 ou 3.")

        # Cadastra o cliente
        cadastrar_cliente(nome, cpf)
        saldo_inicial = 0

        if tipo_conta == 1:
            tipo_conta = "poupanca"
        elif tipo_conta == 2:
            tipo_conta = "corrente"
        elif tipo_conta == 3:
            tipo_conta = "salario"

        # Guarda o número da agência escolhida
        if opcao_agencia == 1:
            agencia = 1
        elif opcao_agencia == 2:
            agencia = 2

        # Cria a conta
        criar_conta(cpf, tipo_conta, saldo_inicial, agencia)

        # Procura a conta recém-criada para adicionar
        # as informações específicas da conta salário
        for conta in contas:
            if conta["cpf"] == cpf:
                # Conta salário possui salário fixo de R$ 2.500
                if tipo_conta == "salario":
                    conta["salario"] = 2500

                # Registra a data de criação da conta
                # como a data inicial para contar o primeiro mês
                if "ultima_movimentacao" not in conta:
                    conta["ultima_movimentacao"] = __import__("datetime").date.today().strftime("%Y-%m-%d")
                break

        # Salva as alterações nos arquivos JSON
        salvar_contas()
        salvar_clientes()

    # 2 - LISTAR AGÊNCIAS

    elif opcao == '2':

        listar_agencias()

    # 3 - LISTAR CLIENTES

    elif opcao == '3':
        print("\n--- CLIENTES CADASTRADOS ---")
        for cliente in clientes:
            print("Cliente:", cliente["nome"])
            print("CPF:", cliente["cpf"])

    # 4 - LISTAR CONTAS
    elif opcao == '4':
        print("\n--- CONTAS CADASTRADAS ---")
        for conta in contas:
            print("Número da Conta:", conta["numero_conta"])
            print("CPF da Conta:", conta["cpf"])
            print("Tipo da Conta:", conta["tipo"])
            print("-" * 20)

    # 5 - DEPOSITAR
    elif opcao == '5':
        escolha = input(
            "Deseja procurar a conta por:\n"
            "1 - CPF\n"
            "2 - Número da conta\n"
            "Escolha: "
        )
        conta_encontrada = False

        if escolha == '1':
            cpf = re.sub(r'\D', '', input("Digite o CPF: "))
            for conta in contas:
                if conta["cpf"] == cpf:
                    conta_encontrada = True
                    break

        elif escolha == '2':
            try:
                numero_conta = int(input("Digite o número da conta: "))
                for conta in contas:
                    if conta["numero_conta"] == numero_conta:
                        conta_encontrada = True
                        break
            except ValueError:
                print("Digite apenas números.")
                continue

        else:
            print("Opção inválida!")
            continue

        if conta_encontrada == False:
            print("Conta não encontrada.")
            continue

        try:
            deposito = float(input("Digite o valor do depósito: R$ "))
        except ValueError:
            print("Valor inválido! Digite um número.")
            continue

        saldo_anterior = conta["saldo"]

        # Passa a conta inteira para a função
        conta = depositar(conta, deposito)

        # Só mostra sucesso se o saldo realmente mudou
        if conta["saldo"] != saldo_anterior:
            salvar_contas()
            print("Depósito realizado com sucesso!")

    # 6 - SACAR

    elif opcao == '6':
        escolha = input(
            "Deseja procurar a conta por:\n"
            "1 - CPF\n"
            "2 - Número da conta\n"
            "Escolha: "
        )
        conta_encontrada = False

        if escolha == '1':
            cpf = re.sub(r'\D', '', input("Digite o CPF: "))
            for conta in contas:
                if conta["cpf"] == cpf:
                    conta_encontrada = True
                    break

        elif escolha == '2':
            try:
                numero_conta = int(input("Digite o número da conta: "))
                for conta in contas:
                    if conta["numero_conta"] == numero_conta:
                        conta_encontrada = True
                        break

            except ValueError:
                print("Digite apenas números.")
                continue

        else:
            print("Opção inválida!")
            continue

        if conta_encontrada == False:
            print("Conta não encontrada.")
            continue

        try:
            saque = float(input("Digite o valor do saque: R$ "))
        except ValueError:
            print("Valor inválido! Digite um número.")
            continue

        saldo_anterior = conta["saldo"]

        # Passa a conta inteira para a função
        conta = sacar(conta, saque)

        # Só salva e mostra sucesso se o saldo realmente mudou
        if conta["saldo"] != saldo_anterior:
            salvar_contas()
            print("Saque realizado com sucesso!")

    # 7 - TRANSFERIR
    elif opcao == '7':
        print("\n--- CONTA DE ORIGEM ---")
        escolha = input(
            "Deseja procurar a conta por:\n"
            "1 - CPF\n"
            "2 - Número da conta\n"
            "Escolha: "
        )
        conta_origem = None

        if escolha == '1':
            cpf_origem = re.sub(r'\D', '', input("Digite o CPF: "))
            for conta in contas:
                if conta["cpf"] == cpf_origem:
                    conta_origem = conta
                    break

        elif escolha == '2':
            try:
                numero_origem = int(input("Digite o número da conta: "))

                for conta in contas:
                    if conta["numero_conta"] == numero_origem:
                        conta_origem = conta
                        break

            except ValueError:
                print("Digite apenas números.")
                continue

        else:
            print("Opção inválida!")
            continue

        if conta_origem == None:
            print("Conta de origem não encontrada.")
            continue

        print("\n--- CONTA DE DESTINO ---")
        escolha = input(
            "Deseja procurar a conta por:\n"
            "1 - CPF\n"
            "2 - Número da conta\n"
            "Escolha: "
        )
        conta_destino = None

        if escolha == '1':
            cpf_destino = re.sub(r'\D', '', input("Digite o CPF: "))
            for conta in contas:
                if conta["cpf"] == cpf_destino:
                    conta_destino = conta
                    break

        elif escolha == '2':
            try:
                numero_destino = int(input("Digite o número da conta: "))
                for conta in contas:
                    if conta["numero_conta"] == numero_destino:
                        conta_destino = conta
                        break
            except ValueError:
                print("Digite apenas números.")
                continue

        else:
            print("Opção inválida!")
            continue

        if conta_destino == None:
            print("Conta de destino não encontrada.")
            continue

        # Impede transferência para a própria conta
        if conta_origem == conta_destino:
            print("A conta de origem e destino devem ser diferentes.")
            continue
        try:
            valor = float(input("Digite o valor da transferência: "))
        except ValueError:
            print("Valor inválido! Digite um número.")
            continue

        saldo_origem = conta_origem["saldo"]
        saldo_destino = conta_destino["saldo"]

        # Passa as duas contas inteiras para a função
        conta_origem, conta_destino = transferir(
            conta_origem,
            conta_destino,
            valor
        )

        # Salva somente se houve alteração
        if conta_origem["saldo"] != saldo_origem or conta_destino["saldo"] != saldo_destino:
            salvar_contas()

    # 8 - CONSULTAR SALDO

    elif opcao == '8':
        escolha = input(
            "Deseja procurar a conta por:\n"
            "1 - CPF\n"
            "2 - Número da conta\n"
            "Escolha: "
        )
        conta_encontrada = False

        if escolha == '1':
            cpf = re.sub(r'\D', '', input("Digite o CPF: "))
            for conta in contas:
                if conta["cpf"] == cpf:
                    conta_encontrada = True
                    break

        elif escolha == '2':
            try:
                numero_conta = int(input("Digite o número da conta: "))
                for conta in contas:
                    if conta["numero_conta"] == numero_conta:
                        conta_encontrada = True
                        break

            except ValueError:
                print("Digite apenas números.")
                continue

        else:
            print("Opção inválida!")
            continue

        if conta_encontrada == False:
            print("Conta não encontrada.")
            continue

        consultarSaldo(conta)

    # 9 - RELATÓRIO
    elif opcao == '9':
        print("\n--- RELATÓRIO DO BANCO E AGÊNCIAS ---")
        saldo_total = 0.0

        total_agencia1 = 0
        quantidade_agencia1 = 0

        total_agencia2 = 0
        quantidade_agencia2 = 0

        # Percorre todas as contas
        # para calcular os valores de cada agência
        for conta in contas:
            saldo = conta["saldo"]
            agencia = conta["agencia"]
            saldo_total += saldo

            if agencia == 1:
                total_agencia1 += saldo
                quantidade_agencia1 += 1

            elif agencia == 2:
                total_agencia2 += saldo
                quantidade_agencia2 += 1

        print("Militech Central:")
        print(" - Total de Clientes:", quantidade_agencia1)
        print(" - Montante Acumulado: R$", total_agencia1)
        print("-" * 30)

        print("Militech Corpo Plaza:")
        print(" - Total de Clientes:", quantidade_agencia2)
        print(" - Montante Acumulado: R$", total_agencia2)
        print("-" * 30)

        # Compara a quantidade de clientes de cada agência
        if quantidade_agencia1 > quantidade_agencia2:
            print("Agência com mais clientes: Militech Central")

        elif quantidade_agencia2 > quantidade_agencia1:
            print("Agência com mais clientes: Militech Corpo Plaza")

        else:
            print("Ambas as agências possuem a mesma quantidade de clientes.")

        print("\nTOTAL GERAL DEPOSITADO NO BANCO: R$", saldo_total)

    # 0 - SAIR
    elif opcao == '0':
        print("Programa encerrado.")
    else:
        print("Opção inválida!")
