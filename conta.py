from abc import ABC, abstractmethod
from datetime import date
import random


class Conta(ABC):
    """Classe abstrata com os dados e operações comuns a qualquer conta."""
    def __init__(self, cliente, agencia, saldo_inicial=0):
        self.cliente = cliente
        self.agencia = agencia
        self.numero_conta = self._gerar_numero()
        self.saldo = float(saldo_inicial)
        self.ultima_movimentacao = date.today()

    @staticmethod
    def _gerar_numero():
        # Gera um número aleatório de seis dígitos.
        return random.randint(100000, 999999)

    @property
    @abstractmethod
    def tipo(self):
        # Cada classe filha deve informar seu próprio tipo.
        pass

    def depositar(self, valor):
        if valor <= 0:
            return False

        self.saldo += valor
        self.ultima_movimentacao = date.today()
        return True

    def sacar(self, valor):
        if valor <= 0 or valor > self.saldo:
            return False

        self.saldo -= valor
        self.ultima_movimentacao = date.today()
        return True

    def transferir(self, conta_destino, valor):
        # Verifica se a conta de destino existe e é diferente da origem.
        if conta_destino is None or conta_destino is self:
            return False

        # Verifica se o valor é válido e se existe saldo suficiente.
        if valor <= 0 or valor > self.saldo:
            return False

        # Retira o dinheiro da conta de origem.
        self.saldo -= valor

        # Adiciona o dinheiro na conta de destino.
        conta_destino.saldo += valor

        # Atualiza a data de movimentação das duas contas.
        hoje = date.today()
        self.ultima_movimentacao = hoje
        conta_destino.ultima_movimentacao = hoje

        return True

    def consultar_saldo(self):
        return self.saldo

    def __str__(self):
        return f"{self.tipo.title()} nº {self.numero_conta} - R$ {self.saldo:.2f}"


# CLASSE FILHA: CONTA CORRENTE
class ContaCorrente(Conta):

    @property
    def tipo(self):
        return "corrente"


# CLASSE FILHA: CONTA POUPANÇA
class ContaPoupanca(Conta):

    TAXA_MENSAL = 0.01  # Taxa de rendimento de 1% ao mês.

    @property
    def tipo(self):
        return "poupanca"

    def aplicar_rendimento(self):
        hoje = date.today()
        ultima = self.ultima_movimentacao

        # Calcula a quantidade de meses completos desde a última movimentação.
        meses = (hoje.year - ultima.year) * 12 + hoje.month - ultima.month

        if hoje.day < ultima.day:
            meses -= 1

        # Aplica o rendimento somente se houver meses completos.
        if meses > 0:
            self.saldo *= (1 + self.TAXA_MENSAL) ** meses
            self.ultima_movimentacao = hoje
            return True

        return False


    # Atualiza a data depois de aplicar o rendimento
    if meses > 0:
        conta["ultima_movimentacao"] = hoje
    return conta
