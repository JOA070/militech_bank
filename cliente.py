class Cliente:
    """Representa um cliente, que pode possuir várias contas."""

    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        # Um cliente começa sem contas; elas são associadas depois.
        self.contas = []

    def adicionar_conta(self, conta):
        if conta not in self.contas:
            self.contas.append(conta)

    def __str__(self):
        return f"{self.nome} - CPF: {self.cpf}"
