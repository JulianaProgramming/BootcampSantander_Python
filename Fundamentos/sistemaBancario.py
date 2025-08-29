# Sistema Bancário MUITO Simples

# Inicializa o saldo da conta
saldo = 0.0

# Loop principal do sistema bancário
while True:
    # Exibe o menu de opções
    print("\n--- Sistema Bancário ---")
    print("1. Ver Saldo")
    print("2. Depositar")
    print("3. Sacar")
    print("4. Sair")
    
    # Solicita a opção do usuário
    opcao = input("Escolha: ")
    
    # Opção 1: Ver saldo
    if opcao == "1":
        print(f"Saldo atual: R$ {saldo:.2f}")
    
    # Opção 2: Depositar valor
    elif opcao == "2":
        valor = float(input("Valor para depositar: R$ "))
        if valor > 0:
            saldo += valor
            print(f"Depositado: R$ {valor:.2f}")
        else:
            print("Valor inválido!")
    
    # Opção 3: Sacar valor
    elif opcao == "3":
        valor = float(input("Valor para sacar: R$ "))
        if valor > 0 and valor <= saldo:
            saldo -= valor
            print(f"Sacado: R$ {valor:.2f}")
        else:
            print("Valor inválido ou saldo insuficiente!")
    
    # Opção 4: Sair do sistema
    elif opcao == "4":
        print("Até logo!")
        break
    
    # Opção inválida
    else:
        print("Opção inválida!")