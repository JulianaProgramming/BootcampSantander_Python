
# Importa classes para criar abstrações e métodos obrigatórios
from abc import ABC, abstractmethod

class Transacao(ABC):
    """Classe abstrata para operações de transação (depósito/saque)."""
    @abstractmethod
    def registrar(self, conta):
        pass

class Historico:
    """Armazena o histórico de transações de uma conta."""
    def __init__(self):
        self._transacoes = []
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            'tipo': 'Depósito' if isinstance(transacao, Deposito) else 'Saque',
            'valor': transacao.valor
        })
    
    def gerar_relatorio(self):
        return self._transacoes

class Cliente:
    """Representa um cliente do banco, podendo ter várias contas."""
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    """Cliente pessoa física, herda de Cliente e adiciona CPF, nome e data de nascimento."""
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    """Classe base para contas bancárias."""
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def sacar(self, valor):
        if valor <= 0:
            print("Valor deve ser positivo!")
            return False
        elif valor > self._saldo:
            print("Saldo insuficiente!")
            return False
        else:
            self._saldo -= valor
            return True
    
    def depositar(self, valor):
        if valor <= 0:
            print("Valor deve ser positivo!")
            return False
        else:
            self._saldo += valor
            return True

class ContaCorrente(Conta):
    """Conta corrente com limite de valor e quantidade de saques por dia."""
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_realizados = 0
    
    def sacar(self, valor):
        if self._saques_realizados >= self._limite_saques:
            print("Limite diário de saques atingido!")
            return False
        elif valor > self._limite:
            print(f"Valor excede o limite de R$ {self._limite:.2f} por saque!")
            return False
        else:
            if super().sacar(valor):
                self._saques_realizados += 1
                return True
            return False

class Deposito(Transacao):
    """Classe para operação de depósito."""
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    """Classe para operação de saque."""
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


# Variáveis globais para armazenar clientes, contas e o próximo número de conta
clientes = []
contas = []
numero_conta = 1

def main():
    """Função principal que exibe o menu e direciona para as operações do sistema bancário."""
    while True:
        print("\n" + "=" * 40)
        print("SISTEMA BANCÁRIO POO")
        print("=" * 40)
        print("[1] Criar usuário")
        print("[2] Criar conta")
        print("[3] Depositar")
        print("[4] Sacar")
        print("[5] Extrato")
        print("[6] Listar usuários")
        print("[7] Listar contas")
        print("[8] Sair")
        print("=" * 40)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            criar_usuario()
        elif opcao == "2":
            criar_conta()
        elif opcao == "3":
            operacao_depositar()
        elif opcao == "4":
            operacao_sacar()
        elif opcao == "5":
            operacao_extrato()
        elif opcao == "6":
            listar_usuarios()
        elif opcao == "7":
            listar_contas()
        elif opcao == "8":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

def criar_usuario():
    """Cadastra um novo usuário, verificando se o CPF já existe."""
    print("\n--- Criar Usuário ---")
    nome = input("Nome: ")
    cpf = input("CPF (apenas números): ")
    
    # Verificar se CPF já existe
    for cliente in clientes:
        if cliente.cpf == cpf:
            print("Erro: CPF já cadastrado!")
            return
    
    data_nascimento = input("Data nascimento (DD/MM/AAAA): ")
    endereco = input("Endereço (rua, num - bairro - cidade/UF): ")
    
    cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
    clientes.append(cliente)
    print("Usuário criado com sucesso!")

def criar_conta():
    """Cria uma nova conta para um usuário já cadastrado, buscando pelo CPF."""
    print("\n--- Criar Conta ---")
    
    if len(clientes) == 0:
        print("Erro: Não há usuários cadastrados!")
        return
    
    cpf = input("Digite o CPF do usuário: ")
    
    # Buscar cliente pelo CPF
    cliente_encontrado = None
    for cliente in clientes:
        if cliente.cpf == cpf:
            cliente_encontrado = cliente
            break
    
    if cliente_encontrado is None:
        print("Erro: Usuário não encontrado!")
        return
    
    global numero_conta
    conta = ContaCorrente.nova_conta(cliente_encontrado, numero_conta)
    cliente_encontrado.adicionar_conta(conta)
    contas.append(conta)
    numero_conta += 1
    print(f"Conta {conta.numero} criada para {cliente_encontrado.nome}!")

def encontrar_conta():
    """Busca uma conta pelo número informado pelo usuário."""
    if len(contas) == 0:
        print("Não há contas cadastradas!")
        return None
    
    numero = input("Número da conta: ")
    if not numero.isdigit():
        print("Número inválido!")
        return None
    
    numero = int(numero)
    for conta in contas:
        if conta.numero == numero:
            return conta
    
    print("Conta não encontrada!")
    return None

def operacao_depositar():
    """Realiza depósito em uma conta existente, validando o valor informado."""
    print("\n--- Depositar ---")
    conta = encontrar_conta()
    if conta is None:
        return
    
    valor = input("Valor para depositar: R$ ")
    if not valor.replace('.', '').isdigit():
        print("Valor inválido!")
        return
    
    valor = float(valor)
    if valor <= 0:
        print("Valor deve ser positivo!")
        return
    
    deposito = Deposito(valor)
    conta.cliente.realizar_transacao(conta, deposito)
    print(f"Depósito de R$ {valor:.2f} realizado!")

def operacao_sacar():
    """Realiza saque em uma conta, respeitando limites e validando o valor informado."""
    print("\n--- Sacar ---")
    conta = encontrar_conta()
    if conta is None:
        return
    
    valor = input("Valor para sacar: R$ ")
    if not valor.replace('.', '').isdigit():
        print("Valor inválido!")
        return
    
    valor = float(valor)
    if valor <= 0:
        print("Valor deve ser positivo!")
        return
    
    saque = Saque(valor)
    conta.cliente.realizar_transacao(conta, saque)

def operacao_extrato():
    """Exibe o extrato de movimentações e saldo da conta escolhida."""
    print("\n--- Extrato ---")
    conta = encontrar_conta()
    if conta is None:
        return
    
    print(f"Conta: {conta.numero} - {conta.cliente.nome}")
    print("Movimentações:")
    
    transacoes = conta.historico.gerar_relatorio()
    if len(transacoes) == 0:
        print("Nenhuma movimentação")
    else:
        for transacao in transacoes:
            print(f"  {transacao['tipo']}: R$ {transacao['valor']:.2f}")
    
    print(f"Saldo: R$ {conta.saldo:.2f}")

def listar_usuarios():
    """Lista todos os usuários cadastrados no sistema."""
    print("\n--- Usuários Cadastrados ---")
    if len(clientes) == 0:
        print("Nenhum usuário cadastrado")
    else:
        for i, cliente in enumerate(clientes, 1):
            print(f"{i}. {cliente.nome} - CPF: {cliente.cpf}")

def listar_contas():
    """Lista todas as contas cadastradas no sistema."""
    print("\n--- Contas Cadastradas ---")
    if len(contas) == 0:
        print("Nenhuma conta cadastrada")
    else:
        for conta in contas:
            print(f"Conta {conta.numero} - {conta.cliente.nome} - Saldo: R$ {conta.saldo:.2f}")


# Inicia o sistema bancário orientado a objetos
if __name__ == "__main__":
    main()