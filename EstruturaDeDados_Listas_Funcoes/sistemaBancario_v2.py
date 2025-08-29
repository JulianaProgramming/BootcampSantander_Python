# Estruturas de dados globais
usuarios = []  # Lista para armazenar os usuários cadastrados
contas = []    # Lista para armazenar as contas criadas
AGENCIA = "0001"  # Número fixo da agência
numero_conta = 1   # Contador para gerar novos números de conta

def main():
    """Função principal que exibe o menu e direciona para as operações do sistema bancário."""
    while True:
        print("\n" + "=" * 40)
        print("SISTEMA BANCÁRIO v2")
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
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            print("Erro: CPF já cadastrado!")
            return
    
    data_nascimento = input("Data nascimento (DD/MM/AAAA): ")
    endereco = input("Endereço (rua, num - bairro - cidade/UF): ")
    
    usuario = {
        'nome': nome,
        'cpf': cpf,
        'data_nascimento': data_nascimento,
        'endereco': endereco
    }
    
    usuarios.append(usuario)
    print("Usuário criado com sucesso!")

def criar_conta():
    """Cria uma nova conta para um usuário já cadastrado, buscando pelo CPF."""
    print("\n--- Criar Conta ---")
    
    if len(usuarios) == 0:
        print("Erro: Não há usuários cadastrados!")
        return
    
    cpf = input("Digite o CPF do usuário: ")
    
    # Buscar usuário pelo CPF
    usuario_encontrado = None
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            usuario_encontrado = usuario
            break
    
    if usuario_encontrado is None:
        print("Erro: Usuário não encontrado!")
        return
    
    global numero_conta
    conta = {
        'agencia': AGENCIA,
        'numero': numero_conta,
        'usuario': usuario_encontrado,
        'saldo': 0.0,
        'extrato': [],
        'saques_hoje': 0
    }
    
    contas.append(conta)
    numero_conta += 1
    print(f"Conta {conta['numero']} criada para {usuario_encontrado['nome']}!")

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
        if conta['numero'] == numero:
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
    
    conta['saldo'] += valor
    conta['extrato'].append(f"Depósito: R$ {valor:.2f}")
    print(f"Depósito de R$ {valor:.2f} realizado!")

def operacao_sacar():
    """Realiza saque em uma conta, respeitando limites diários e de valor."""
    print("\n--- Sacar ---")
    conta = encontrar_conta()
    if conta is None:
        return
    
    LIMITE_SAQUES = 3
    LIMITE_VALOR = 500.0
    
    if conta['saques_hoje'] >= LIMITE_SAQUES:
        print("Limite diário de saques atingido!")
        return
    
    valor = input("Valor para sacar: R$ ")
    if not valor.replace('.', '').isdigit():
        print("Valor inválido!")
        return
    
    valor = float(valor)
    if valor <= 0:
        print("Valor deve ser positivo!")
        return
    elif valor > LIMITE_VALOR:
        print(f"Limite máximo por saque: R$ {LIMITE_VALOR:.2f}")
        return
    elif valor > conta['saldo']:
        print("Saldo insuficiente!")
        return
    
    conta['saldo'] -= valor
    conta['extrato'].append(f"Saque: R$ {valor:.2f}")
    conta['saques_hoje'] += 1
    print(f"Saque de R$ {valor:.2f} realizado!")
    print(f"Saques hoje: {conta['saques_hoje']}/{LIMITE_SAQUES}")

def operacao_extrato():
    """Exibe o extrato de movimentações e saldo da conta escolhida."""
    print("\n--- Extrato ---")
    conta = encontrar_conta()
    if conta is None:
        return
    
    print(f"Conta: {conta['numero']} - {conta['usuario']['nome']}")
    print("Movimentações:")
    
    if len(conta['extrato']) == 0:
        print("Nenhuma movimentação")
    else:
        for movimento in conta['extrato']:
            print(f"  {movimento}")
    
    print(f"Saldo: R$ {conta['saldo']:.2f}")

def listar_usuarios():
    """Lista todos os usuários cadastrados no sistema."""
    print("\n--- Usuários Cadastrados ---")
    if len(usuarios) == 0:
        print("Nenhum usuário cadastrado")
    else:
        for i, usuario in enumerate(usuarios, 1):
            print(f"{i}. {usuario['nome']} - CPF: {usuario['cpf']}")
    input("\nPressione Enter para voltar ao menu...")

def listar_contas():
    """Lista todas as contas cadastradas no sistema."""
    print("\n--- Contas Cadastradas ---")
    if len(contas) == 0:
        print("Nenhuma conta cadastrada")
    else:
        for conta in contas:
            print(f"Conta {conta['numero']} - {conta['usuario']['nome']} - Saldo: R$ {conta['saldo']:.2f}")
    input("\nPressione Enter para voltar ao menu...")

# Iniciar o sistema
if __name__ == "__main__":
    main()  # Chama a função principal para iniciar o sistema