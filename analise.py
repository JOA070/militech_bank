from functools import reduce

def listar_contas_positivas(contas):
    return list(filter(lambda conta: conta["saldo"] > 0, contas))

def calcular_saldo_total(contas):
    saldos = map(lambda conta: conta["saldo"], contas)
    return reduce(lambda total, saldo: total + saldo, saldos, 0)

def encontrar_maior_saldo(contas):
    if not contas:
        return None
    maior = max([conta["saldo"] for conta in contas])
    return [conta for conta in contas if conta["saldo"] == maior[0]]

def encontrar_menor_saldo(contas):
    if not contas:
        return None
    menor = min([conta["saldo"] for conta in contas])
    return [conta for conta in contas if conta["saldo"] == menor[0]]

def calcular_saldo_medio(contas):
    if not contas:
        return 0
    return calcular_saldo_total(contas)/len(contas)

def gerar_dashboard(clientes, contas):
    maior = encontrar_maior_saldo(contas)
    menor = encontrar_menor_saldo(contas)
    return{
        "total_clientes": len(clientes),
        "total_contas": len(contas),
        "saldo_total": calcular_saldo_total(contas),
        "saldo_medio": calcular_saldo_medio(contas),
        "maior_saldo": maior,
        "menor_saldo": menor
    }
