def validar_binario(valor, tamanho_esperado, nome_campo):
    valor = valor.strip()

    if not all(c in '01' for c in valor):
        print(f"Erro: O campo '{nome_campo}' deve conter apenas 0 e 1.")
        return False

    if len(valor) != tamanho_esperado:
        print(f"Erro: O campo '{nome_campo}' deve ter exatamente {tamanho_esperado} bits.")
        print(f"Voce digitou {len(valor)} bits.")
        return False
    
    return True

def obter_campo_binario(nome_campo, tamanho):
    while True:
        valor = input(f"  {nome_campo} ({tamanho} bits): ").strip()
        if validar_binario(valor, tamanho, nome_campo):
            return valor

def binario_para_hex(binario):
    decimal = int(binario, 2)
    hex_valor = format(decimal, '08X')
    return hex_valor

def obter_instrucao():
    print("\nDigite os campos da instrucao (binario):")
    
    opercode = obter_campo_binario("OPERCODE (ULA)", 5)
    sel_clock = obter_campo_binario("SEL CLOCK", 5)
    sel_a = obter_campo_binario("SEL A", 5)
    sel_b = obter_campo_binario("SEL B", 5)
    externo = obter_campo_binario("EXTERNO", 11)
    i = obter_campo_binario("i (entrada externa)", 1)
    
    instrucao_binaria = opercode + sel_clock + sel_a + sel_b + externo + i
    
    instrucao_hex = binario_para_hex(instrucao_binaria)
    
    print(f"\nInstrucao montada:")
    print(f"   Binario:      {instrucao_binaria}")
    print(f"   Hexadecimal:  {instrucao_hex}")
    
    return instrucao_hex

def main():
    print("=" * 60)
    print("  GERADOR DE ARQUIVO .MEMDUMP PARA LOGISIM")
    print("=" * 60)
    
    # Configuração inicial
    while True:
        try:
            tamanho_memoria = int(input("\nQuantas palavras de memoria (32 bits)? "))
            if tamanho_memoria <= 0:
                print("Erro: O tamanho deve ser maior que zero.")
                continue
            break
        except ValueError:
            print("Erro: Por favor, digite um numero valido.")
    
    nome_arquivo = input("Nome do arquivo de saida (ex: programa): ").strip()
    if not nome_arquivo.endswith('.memdump'):
        nome_arquivo += '.memdump'
    
    memoria = ['00000000'] * tamanho_memoria
    indice_atual = 0
    
    print(f"\nMemoria inicializada com {tamanho_memoria} palavras.")
    print(f"Arquivo de saida: {nome_arquivo}")
    
    while indice_atual < tamanho_memoria:
        print(f"\n{'─' * 60}")
        print(f"Posicao atual: {indice_atual}/{tamanho_memoria}")
        print(f"Espacos restantes: {tamanho_memoria - indice_atual}")
        
        if indice_atual > 0:
            continuar = input("\nDeseja inserir outra instrucao? (s/n): ").strip().lower()
            if continuar != 's':
                print("\nEncerrando entrada de instrucoes...")
                break
        
        try:
            instrucao_hex = obter_instrucao()
            memoria[indice_atual] = instrucao_hex
            indice_atual += 1
            print(f"Instrucao armazenada na posicao {indice_atual - 1}")
        except KeyboardInterrupt:
            print("\n\nOperacao cancelada pelo usuario.")
            break
        except Exception as e:
            print(f"\nErro inesperado: {e}")
            continuar = input("Deseja tentar novamente? (s/n): ").strip().lower()
            if continuar != 's':
                break
    
    print(f"\n{'=' * 60}")
    print("Gerando arquivo .memdump...")
    
    try:
        with open(nome_arquivo, 'w') as f:
            f.write("v2.0 raw\n")
            for palavra in memoria:
                f.write(f"{palavra}\n")
        
        print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")
        print(f"\nResumo:")
        print(f"   Total de palavras: {tamanho_memoria}")
        print(f"   Instrucoes inseridas: {indice_atual}")
        print(f"   Palavras vazias: {tamanho_memoria - indice_atual}")
        print(f"\nO arquivo pode ser carregado diretamente no Logisim.")
        
    except IOError as e:
        print(f"Erro ao gravar arquivo: {e}")
    except Exception as e:
        print(f"Erro inesperado ao gravar arquivo: {e}")
    
    print("=" * 60)


try:
    main()
except KeyboardInterrupt:
    print("\n\nPrograma encerrado pelo usuario.")
except Exception as e:
    print(f"\nErro fatal: {e}")