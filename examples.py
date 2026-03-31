#!/usr/bin/env python3
"""
Exemplos de Uso do Script de Análise de Curto-Circuito

Este script demonstra diferentes cenários e como modificar
os parâmetros para diferentes análises.
"""

from short_circuit_analysis import ShortCircuitAnalysis

def example_1_basic():
    """Exemplo 1: Análise básica com 100 km sem impedância da fonte"""
    print("\n" + "="*80)
    print("EXEMPLO 1: Análise Básica (100 km, sem impedância da fonte)")
    print("="*80)

    analysis = ShortCircuitAnalysis()
    analysis.set_line_length(100)  # 100 km
    results = analysis.calculate_parallel_lines_fault()

    return results


def example_2_short_line():
    """Exemplo 2: Linha curta de 50 km"""
    print("\n" + "="*80)
    print("EXEMPLO 2: Linha Curta (50 km)")
    print("="*80)

    analysis = ShortCircuitAnalysis()
    analysis.set_line_length(50)  # 50 km
    results = analysis.calculate_parallel_lines_fault()

    return results


def example_3_long_line():
    """Exemplo 3: Linha longa de 200 km"""
    print("\n" + "="*80)
    print("EXEMPLO 3: Linha Longa (200 km)")
    print("="*80)

    analysis = ShortCircuitAnalysis()
    analysis.set_line_length(200)  # 200 km
    results = analysis.calculate_parallel_lines_fault()

    return results


def example_4_with_source_impedance():
    """Exemplo 4: Com impedância da fonte"""
    print("\n" + "="*80)
    print("EXEMPLO 4: Com Impedância da Fonte")
    print("="*80)

    analysis = ShortCircuitAnalysis()
    analysis.set_line_length(100)  # 100 km

    # Definir impedância da fonte
    # Exemplo: impedância equivalente do sistema de geração
    Z_source = complex(1.0, 10.0)  # 1.0 + j10.0 Ω
    analysis.set_source_impedance(Z_source)

    results = analysis.calculate_parallel_lines_fault()

    return results


def example_5_comparison():
    """Exemplo 5: Comparação de diferentes comprimentos"""
    print("\n" + "="*80)
    print("EXEMPLO 5: Comparação de Diferentes Comprimentos de Linha")
    print("="*80)

    lengths = [50, 100, 150, 200]
    results_list = []

    print("\n{:>10} | {:>12} | {:>12} | {:>12}".format(
        "Comp (km)", "Icc (kA)", "Z_th (Ω)", "V1 (kV)"))
    print("-" * 60)

    for length in lengths:
        analysis = ShortCircuitAnalysis()
        # Suprimir saída detalhada para comparação
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        analysis.set_line_length(length)
        results = analysis.calculate_parallel_lines_fault()

        sys.stdout = old_stdout

        print("{:10} | {:12.4f} | {:12.4f} | {:12.4f}".format(
            length,
            results['I_cc_kA'],
            results['Z_th_ohm'],
            results['V1_kV']
        ))

        results_list.append(results)

    print("\nObservações:")
    print("- Quanto maior o comprimento da linha, maior a impedância")
    print("- Maior impedância resulta em menor corrente de curto-circuito")
    print("- Para este exemplo, as tensões na barra Z permanecem constantes")
    print("  (assumindo sem impedância da fonte)")

    return results_list


def example_6_custom_parameters():
    """Exemplo 6: Parâmetros customizados para seu problema específico"""
    print("\n" + "="*80)
    print("EXEMPLO 6: Configure Aqui Seus Parâmetros Específicos")
    print("="*80)

    # MODIFIQUE AQUI PARA SEU PROBLEMA ESPECÍFICO
    # ============================================

    # Comprimento da linha em km
    LINE_LENGTH = 100  # km - MODIFIQUE ESTE VALOR

    # Impedância da fonte em Ω (opcional)
    # Descomente se você conhece a impedância da fonte
    # Z_SOURCE = complex(1.0, 10.0)  # R + jX em Ω

    # ============================================

    analysis = ShortCircuitAnalysis()
    analysis.set_line_length(LINE_LENGTH)

    # Se você definiu impedância da fonte, descomente:
    # analysis.set_source_impedance(Z_SOURCE)

    results = analysis.calculate_parallel_lines_fault()

    return results


def main():
    """Menu principal para escolher exemplos"""
    print("\n" + "="*80)
    print("EXEMPLOS DE ANÁLISE DE CURTO-CIRCUITO")
    print("="*80)
    print("\nEscolha um exemplo para executar:")
    print("1 - Análise básica (100 km, sem impedância da fonte)")
    print("2 - Linha curta (50 km)")
    print("3 - Linha longa (200 km)")
    print("4 - Com impedância da fonte")
    print("5 - Comparação de diferentes comprimentos")
    print("6 - Parâmetros customizados (edite o script)")
    print("0 - Executar todos os exemplos")

    try:
        choice = input("\nDigite o número do exemplo (ou Enter para exemplo 1): ").strip()

        if choice == "" or choice == "1":
            example_1_basic()
        elif choice == "2":
            example_2_short_line()
        elif choice == "3":
            example_3_long_line()
        elif choice == "4":
            example_4_with_source_impedance()
        elif choice == "5":
            example_5_comparison()
        elif choice == "6":
            example_6_custom_parameters()
        elif choice == "0":
            example_1_basic()
            example_2_short_line()
            example_3_long_line()
            example_4_with_source_impedance()
            example_5_comparison()
        else:
            print(f"\nOpção inválida: {choice}")
            print("Executando exemplo 1 (padrão)...")
            example_1_basic()

    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
    except Exception as e:
        print(f"\nErro: {e}")
        print("Executando exemplo 1 (padrão)...")
        example_1_basic()


if __name__ == "__main__":
    main()
