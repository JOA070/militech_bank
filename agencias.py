def agencias():
    #Lista com os dados das agencias do banco
    lista_agencias = [
        {
            "numero": 1, "nome": "Militech Central",
            },
        {
            "numero": 2, "nome": "Militech Corpo Plaza"
        }
    ]
    return lista_agencias

def listar_agencias():
    #Obtem a lista de agencias para exibir os dados 
    lista_agencias = agencias()
    print("\n--- AGÊNCIAS ---")

    #Percorre cada agencia e exibe seus dados
    for agencia in lista_agencias:
        print("Número: ", agencia["numero"])
        print("Nome: ", agencia["nome"])
        print("-" * 20)

    
'''from agencias import agencias, listar_agencias''' #importar no main
