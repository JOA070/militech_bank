import json
from datetime import date
from pathlib import Path
from agencia import Agencia
from cliente import Cliente
from conta import ContaCorrente, ContaPoupanca


class Banco:
    """Coordena os objetos e faz a leitura/gravação dos arquivos JSON."""

    def __init__(self, arquivo_clientes="clientes.json", arquivo_contas="contas.json"):
        pasta_projeto = Path(__file__).resolve().parent

        self.arquivo_clientes = pasta_projeto / arquivo_clientes
        self.arquivo_contas = pasta_projeto / arquivo_contas
        self.agencia = Agencia()  # Simplificação: existe somente uma agência.
        self.clientes = []
        self.contas = []

    def buscar_cliente(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                return cliente
        return None

    def buscar_conta(self, numero_conta):
        for conta in self.contas:
            if str(conta.numero_conta) == str(numero_conta):
                return conta
        return None

    def _numero_conta_disponivel(self):
        numeros_existentes = [conta.numero_conta for conta in self.contas]
        numero = ContaCorrente._gerar_numero()
        while numero in numeros_existentes:
            numero = ContaCorrente._gerar_numero()
        return numero

    def cadastrar_cliente(self, nome, cpf):
        if self.buscar_cliente(cpf):
            return None
        cliente = Cliente(nome, cpf)
        self.clientes.append(cliente)
        self.clientes.sort(key=lambda item: item.nome.lower())
        return cliente

    def criar_conta(self, cliente, tipo, saldo_inicial=0):
        if cliente is None or saldo_inicial < 0:
            return None
        # O projeto permite no máximo uma conta de cada tipo por cliente.
        if any(conta.tipo == tipo for conta in cliente.contas):
            return None

        if tipo == "corrente":
            conta = ContaCorrente(cliente, self.agencia, saldo_inicial)
        elif tipo == "poupanca":
            conta = ContaPoupanca(cliente, self.agencia, saldo_inicial)
        else:
            return None

        # Evita repetir o número aleatório de uma conta já existente.
        while any(item.numero_conta == conta.numero_conta for item in self.contas):
            conta.numero_conta = conta._gerar_numero()

        self.contas.append(conta)
        cliente.adicionar_conta(conta)
        self.agencia.adicionar_conta(conta)
        return conta


    def remover_conta(self, numero_conta):
        """Remove uma conta do banco, do cliente e da agência."""
        conta = self.buscar_conta(numero_conta)
        if conta is None:
            return False

        self.contas.remove(conta)
        if conta in conta.cliente.contas:
            conta.cliente.contas.remove(conta)
        if conta in self.agencia.contas:
            self.agencia.contas.remove(conta)
        return True

    def remover_cliente(self, cpf):
        """Remove o cliente e todas as contas que pertencem a ele."""
        cliente = self.buscar_cliente(cpf)
        if cliente is None:
            return False

        # Fazemos uma cópia porque a lista original será alterada no laço.
        for conta in cliente.contas[:]:
            self.remover_conta(conta.numero_conta)

        self.clientes.remove(cliente)
        return True

    def carregar(self):
        """Lê os JSON uma vez e reconstrói as relações entre os objetos."""
        if self.arquivo_clientes.exists():
            with self.arquivo_clientes.open("r", encoding="utf-8") as arquivo:
                dados_clientes = json.load(arquivo)
            for dados in dados_clientes:
                self.cadastrar_cliente(dados["nome"], dados["cpf"])

        if self.arquivo_contas.exists():
            with self.arquivo_contas.open("r", encoding="utf-8") as arquivo:
                dados_contas = json.load(arquivo)

            for dados in dados_contas:
                cliente = self.buscar_cliente(dados["cpf"])
                if cliente is None:
                    # Ignora uma conta cujo cliente não exista no arquivo de clientes.
                    continue

                tipo = dados.get("tipo")
                if tipo not in ("corrente", "poupanca"):
                    # Contas salário não fazem parte das regras da Etapa 5.
                    continue

                conta = self.criar_conta(cliente, tipo, dados.get("saldo", 0))
                if conta is not None:
                    conta.numero_conta = int(dados["numero_conta"])
                    conta.ultima_movimentacao = date.fromisoformat(dados["ultima_movimentacao"])
                print(f"Dados carregados: {len(self.clientes)} cliente(s) e {len(self.contas)} conta(s).")

    def salvar(self):
        """Converte os objetos em dicionários simples para gravar no JSON."""
        dados_clientes = [
            {"nome": cliente.nome, "cpf": cliente.cpf}
            for cliente in self.clientes
        ]
        dados_contas = [
            {
                "cpf": conta.cliente.cpf,
                "numero_conta": conta.numero_conta,
                "tipo": conta.tipo,
                "saldo": conta.saldo,
                "agencia": self.agencia.numero,
                "ultima_movimentacao": conta.ultima_movimentacao.isoformat(),
            }
            for conta in self.contas
        ]

        with self.arquivo_clientes.open("w", encoding="utf-8") as arquivo:
            json.dump(dados_clientes, arquivo, indent=4, ensure_ascii=False)
        with self.arquivo_contas.open("w", encoding="utf-8") as arquivo:
            json.dump(dados_contas, arquivo, indent=4, ensure_ascii=False)
