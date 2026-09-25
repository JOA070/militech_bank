from cliente import cadastrar_cliente, criar_conta, clientes, contas, carregar_clientes,carregar_contas,salvar_clientes,salvar_contas
from conta import depositar, sacar, transferir, consultarSaldo
from menu import menu
from agencias import agencias

lista_agencias = agencias()
carregar_clientes()
carregar_contas()

opcao=''

while (opcao != '0'):
    opcao = menu()
    
    if opcao == '1':
        nome = input("Digite o nome do cliente: ")
        cpf = int(input("Informe o CPF: "))

        cliente = cadastrar_cliente(nome, cpf)


        tipo_conta = "Corrente"
        saldo_inicial = 0
        opcao_agencia = int(input("Qual agencia deseja?\n""1- Militech Central\n""2- Militech Corpo Plaza\n"))

        while opcao_agencia != 1 and opcao_agencia != 2:
            print("Opção inválida! Digite 1 ou 2.")

            opcao_agencia = int(input("Qual agencia deseja?\n""1- Militech Central\n""2- Militech Corpo Plaza\n"))

        if opcao_agencia == 1:
            conta = criar_conta(cpf,tipo_conta, saldo_inicial, lista_agencias[0][0])
            salvar_clientes()
            salvar_contas()

        elif opcao_agencia == 2:
            conta = criar_conta(cpf,tipo_conta,saldo_inicial,lista_agencias[1][0])
            salvar_clientes()
            salvar_contas()
             

            saldo = conta[3]

    elif opcao == '2':
           lista_agencias = agencias()
           print("\n--- AGÊNCIAS ---")

           for agencia in lista_agencias:
                 print("Número:", agencia[0])
                 print("Nome:", agencia[1])
                 print("-" * 20)
           input("\nPressione Enter para voltar ao menu...")

    elif opcao == '3':
        print("\n--- CLIENTES CADASTRADOS ---")
        for cliente in clientes:
            print("Cliente:", cliente)
        input("\nPressione Enter para continuar...")
    elif opcao == '4':
        print("\n--- CONTAS CADASTRADAS ---")
        for conta in contas:
            print("CPF da Conta:", conta[0])
            print("Tipo da Conta:", conta[1])
            print("Saldo: R$", conta[3])
            print("-" * 20)
        input("\nPressione Enter para continuar...")


    elif opcao =='5':
        try:
            cpf = int(input("Digite o CPF: "))
        except ValueError:
            print("CPF inválido! Digite apenas números.")
            continue

        indice = 0
        indice_conta = -1

        for conta in contas:
            if conta[0] == cpf:
                indice_conta = indice
                conta = contas[indice]
                saldo = conta[3]
                print("Conta encontrada no índice", indice)
                break

            indice = indice + 1

        if indice_conta == -1:
            print("Conta não encontrada.")

        else:
            try:
                deposito = float(input(
                    "Digite o valor do depósito: R$ "
                ))
            except ValueError:
                print("Valor inválido! Digite um número.")
                continue

            saldo = depositar(saldo, deposito)

            nova_conta = (conta[0],conta[1],conta[2],saldo,conta[4])
            conta = nova_conta
            contas[indice_conta] = conta
            salvar_contas()


    elif opcao == '6':
        try:
            cpf = int(input("Digite o CPF: "))
        except ValueError:
            print("CPF inválido! Digite apenas números.")
            continue

        indice = 0
        indice_conta = -1

        for conta in contas:
            if conta[0] == cpf:
                indice_conta = indice
                conta = contas[indice]
                saldo = conta[3]
                print("Conta encontrada no índice", indice)
                break

            indice = indice + 1

        if indice_conta == -1:
            print("Conta não encontrada.")

        else:
            try:
                saque = float(input(
                    "Digite o valor do saque: R$ "))
            except ValueError:
                print("Valor inválido! Digite um número.")
                continue

            saldo = sacar(saldo, saque)
            nova_conta = (conta[0],conta[1],conta[2],saldo,conta[4])
            conta = nova_conta
            contas[indice_conta] = conta
            salvar_contas()

    elif opcao == '7':
        try:
            cpf_origem = int(input("Digite o CPF da conta de origem: "))
            cpf_destino = int(input("Digite o CPF da conta de destino: "))

        except ValueError:
            print("CPF inválido! Digite apenas números.")
            continue

        if cpf_origem == cpf_destino:
            print("A conta de origem e destino devem ser diferentes.")

        else:
            try:
                valor = float(input("Digite o valor da transferência: "))
            except ValueError:
                print("Valor inválido! Digite um número.")
                continue

            indice = 0
            indice_origem = -1
            indice_destino = -1

            for conta in contas:
                if conta[0] == cpf_origem:
                    indice_origem = indice
                    conta_origem = contas[indice]
                    saldo_origem = conta_origem[3]
                indice = indice + 1

            indice = 0

            for conta in contas:
                if conta[0] == cpf_destino:
                    indice_destino = indice
                    conta_destino = contas[indice]
                    saldo_destino = conta_destino[3]
                indice = indice + 1

            if indice_origem == -1 or indice_destino == -1:
                print("Uma ou ambas as contas não foram encontradas.")

            else:
                saldo_origem, saldo_destino = transferir(saldo_origem,saldo_destino,valor)

                conta_origem = (conta_origem[0],conta_origem[1],conta_origem[2],saldo_origem,conta_origem[4])
                conta_destino = (conta_destino[0],conta_destino[1],conta_destino[2],saldo_destino,conta_destino[4])

                contas[indice_origem] = conta_origem
                contas[indice_destino] = conta_destino
                salvar_contas()

      
    elif opcao == '8':
        try:
            cpf = int(input("Digite o CPF: "))
        except ValueError:
            print("CPF inválido! Digite apenas números.")
            continue

        encontrou = False

        for conta in contas:
            if conta[0] == cpf:
                encontrou = True
                saldo = conta[3]
                consultarSaldo(saldo)
                break
        if encontrou == False:
            print("Conta não encontrada.")


    elif opcao == '9':
            
        print("\n--- RELATÓRIO DO BANCO E AGÊNCIAS ---")

        saldo_total = 0.0

        nome_ag1 = lista_agencias[0][0]
        total_ag1 = 0.0
        quantidade_ag1 = 0

        nome_ag2 = lista_agencias[1][0]
        total_ag2 = 0.0
        quantidade_ag2 = 0

        for conta in contas:
                saldo = conta[3]
                agencia_conta = conta[4]

                saldo_total += saldo

                if agencia_conta == nome_ag1:
                    total_ag1 += saldo
                    quantidade_ag1 += 1
                elif agencia_conta == nome_ag2:
                    total_ag2 += saldo
                    quantidade_ag2 += 1

        print("Militech Central:", nome_ag1)
        print("  - Total de Clientes:", quantidade_ag1)
        print("  - Montante Acumulado: R$", total_ag1)
        print("-" * 30)

        print("Militech Corpo Plaza:", nome_ag2)
        print("  - Total de Clientes:", quantidade_ag2)
        print("  - Montante Acumulado: R$", total_ag2)
        print("-" * 30)

        if quantidade_ag1 > quantidade_ag2:
                print("Agência com mais clientes:", nome_ag1)
        elif quantidade_ag2 > quantidade_ag1:
                print("Agência com mais clientes:", nome_ag2)
        else:
                print("Ambas as agências possuem a mesma quantidade de clientes.")

        print("\nTOTAL GERAL DEPOSITADO NO BANCO: R$", saldo_total)
        input("\nPressione Enter para continuar...")
        
    elif opcao == '0':
        print('Saindo...')
    else: 
        print('Opção invalida. Tente novamente')
