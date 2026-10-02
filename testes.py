from conta import aplicar_rendimento
from datetime import date


# Testa o rendimento de uma conta poupança
def test_rendimento_poupanca():
    conta = {
        "cpf": 111,
        "numero_conta": 147189,
        "tipo": "poupanca",
        "saldo": 1000,
        "agencia": 1,
        "ultima_movimentacao": date(2026, 6, 24)
    }

    # Aplica o rendimento na conta
    aplicar_rendimento(conta)

    # Verifica se o saldo final está correto
    assert round(conta["saldo"], 2) == 1030.30





# Testa se o depósito atualiza corretamente o saldo da conta
def test_deposito():
    conta = {
        "cpf": 111,
        "numero_conta": 147189,
        "tipo": "corrente",
        "saldo": 1000,
        "agencia": 1,
        "ultima_movimentacao": date(2026, 6, 24)
    }

    # Realiza um depósito de R$ 500,00
    conta["saldo"] = depositar(conta["saldo"], 500)

    # Verifica se o saldo foi atualizado corretamente
    assert conta["saldo"] == 1500
