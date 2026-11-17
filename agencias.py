class Agencia:
    """Representa a única agência"""

    def __init__(self, numero=1, nome="Militech Central"):
        self.numero = numero
        self.nome = nome
        self.contas = []

    def adicionar_conta(self, conta):
        if conta not in self.contas:
            self.contas.append(conta)

    def __str__(self):
        return f"Agência {self.numero} - {self.nome}"
