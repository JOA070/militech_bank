from functools import reduce


def listar_contas_positivas(contas):
    # Agora cada conta é um objeto; seu saldo é acessado por .saldo.
    return list(filter(lambda conta: conta.saldo > 0, contas))


def calcular_saldo_total(contas):
    saldos = map(lambda conta: conta.saldo, contas)
    return reduce(lambda total, saldo: total + saldo, saldos, 0)


def encontrar_maior_saldo(contas):
    if not contas:
        return None
    return max(contas, key=lambda conta: conta.saldo)


def encontrar_menor_saldo(contas):
    if not contas:
        return None
    return min(contas, key=lambda conta: conta.saldo)


def calcular_saldo_medio(contas):
    if not contas:
        return 0
    return calcular_saldo_total(contas) / len(contas)


def gerar_dashboard(clientes, contas):
    return {
        "total_clientes": len(clientes),
        "total_contas": len(contas),
        "saldo_total": calcular_saldo_total(contas),
        "saldo_medio": calcular_saldo_medio(contas),
        "maior_saldo": encontrar_maior_saldo(contas),
        "menor_saldo": encontrar_menor_saldo(contas),
    }

