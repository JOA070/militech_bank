from analise import(
    listar_contas_positivas,
    calcular_saldo_total,
    calcular_saldo_medio,
    encontrar_menor_saldo,
    encontrar_maior_saldo,
    gerar_dashboard
)

contas = [
    {"numero_conta": 101, "saldo": 1000},
    {"numero_conta": 102, "saldo": 0},
    {"numero_conta": 103, "saldo": -200},
    {"numero_conta": 104, "saldo": 3000}
]

clientes = [
    {"nome": "Ana", "cpf": "111"},
    {"nome": "Bruno", "cpf": "222"}
]
print("Saldo total calculado:", calcular_saldo_total(contas))
assert calcular_saldo_total(contas) == 3800
assert len(listar_contas_positivas(contas)) == 2
assert calcular_saldo_total(contas) == 3800
assert encontrar_maior_saldo(contas)["numero_conta"] == 104
assert encontrar_menor_saldo(contas)["numero_conta"] == 103
assert calcular_saldo_medio(contas) == 950

dashboard = gerar_dashboard(clientes, contas)

assert dashboard["total_clientes"] == 2
assert dashboard["total_contas"] == 4
assert dashboard["saldo_total"] == 3800

assert calcular_saldo_total([]) == 0
assert calcular_saldo_medio([]) == 0
assert encontrar_maior_saldo([]) is None
assert encontrar_menor_saldo([]) is None

print("Todos os testes passaram!")
