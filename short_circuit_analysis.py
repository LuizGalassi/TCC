#!/usr/bin/env python3
"""
Análise de Curto-Circuito Trifásico em Sistema de Potência
Short-Circuit Analysis for Power System with Parallel Lines

Este script calcula:
- Corrente de curto-circuito (Icc) em um ponto específico
- Tensões de sequência na barra Z
- Tensões de fase na barra Z

Dados do problema:
- Impedância da linha: Z+ = 0.05 + j0.45 Ω/km
- Potência base: Sb = 100 MVA
- Tensão de alta: 230 kV
- Configuração: Duas linhas em paralelo (L1 e L2)
- Falta: Curto-circuito trifásico na metade da linha L2
"""

import numpy as np
import cmath

class ShortCircuitAnalysis:
    def __init__(self):
        # Parâmetros do sistema
        self.Sb = 100e6  # Potência base em VA (100 MVA)
        self.Vb = 230e3  # Tensão base em V (230 kV)
        self.Z_linha_km = complex(0.05, 0.45)  # Impedância por km (Ω/km)

        # Impedância base
        self.Zb = (self.Vb ** 2) / self.Sb  # Ω

        # Corrente base
        self.Ib = self.Sb / (np.sqrt(3) * self.Vb)  # A

        print("="*80)
        print("ANÁLISE DE CURTO-CIRCUITO TRIFÁSICO")
        print("="*80)
        print(f"\nParâmetros do Sistema:")
        print(f"  Potência Base (Sb): {self.Sb/1e6:.0f} MVA")
        print(f"  Tensão Base (Vb): {self.Vb/1e3:.0f} kV")
        print(f"  Impedância da Linha (Z+): {self.Z_linha_km.real:.2f} + j{self.Z_linha_km.imag:.2f} Ω/km")
        print(f"  Impedância Base (Zb): {self.Zb:.4f} Ω")
        print(f"  Corrente Base (Ib): {self.Ib:.2f} A")

    def set_line_length(self, length_km):
        """Define o comprimento da linha em km"""
        self.length_km = length_km
        # Impedância total de uma linha
        self.Z_linha_total = self.Z_linha_km * length_km  # Ω
        # Impedância em pu
        self.Z_linha_pu = self.Z_linha_total / self.Zb

        print(f"\nComprimento da Linha: {length_km} km")
        print(f"  Impedância Total de uma Linha: {self.Z_linha_total.real:.4f} + j{self.Z_linha_total.imag:.4f} Ω")
        print(f"  Impedância Total de uma Linha (pu): {self.Z_linha_pu.real:.6f} + j{self.Z_linha_pu.imag:.6f} pu")

    def set_source_impedance(self, Z_source):
        """Define a impedância da fonte em Ω"""
        self.Z_source = Z_source
        self.Z_source_pu = Z_source / self.Zb
        print(f"\nImpedância da Fonte: {Z_source.real:.4f} + j{Z_source.imag:.4f} Ω")
        print(f"  Impedância da Fonte (pu): {self.Z_source_pu.real:.6f} + j{self.Z_source_pu.imag:.6f} pu")

    def calculate_parallel_lines_fault(self):
        """
        Calcula o curto-circuito trifásico na metade da linha L2
        quando há duas linhas idênticas em paralelo (L1 e L2)
        """
        print("\n" + "="*80)
        print("CONFIGURAÇÃO DO SISTEMA")
        print("="*80)
        print("\nDuas linhas em paralelo (L1 e L2) entre as barras")
        print("Falta: Curto-circuito trifásico na metade da linha L2")

        # Impedância de meia linha L2 (da barra até o ponto de falta)
        Z_half_L2 = self.Z_linha_total / 2  # Ω
        Z_half_L2_pu = self.Z_linha_pu / 2

        print(f"\nImpedância de meia linha L2 (até a falta):")
        print(f"  {Z_half_L2.real:.4f} + j{Z_half_L2.imag:.4f} Ω")
        print(f"  {Z_half_L2_pu.real:.6f} + j{Z_half_L2_pu.imag:.6f} pu")

        # Linha L1 inteira em paralelo com meia linha L2
        # Impedância equivalente das linhas em paralelo até o ponto de falta
        Z_parallel = (self.Z_linha_total * Z_half_L2) / (self.Z_linha_total + Z_half_L2)
        Z_parallel_pu = (self.Z_linha_pu * Z_half_L2_pu) / (self.Z_linha_pu + Z_half_L2_pu)

        print(f"\nImpedância Equivalente (L1 // meia L2):")
        print(f"  {Z_parallel.real:.4f} + j{Z_parallel.imag:.4f} Ω")
        print(f"  {Z_parallel_pu.real:.6f} + j{Z_parallel_pu.imag:.6f} pu")

        # Impedância total de Thévenin vista do ponto de falta
        if hasattr(self, 'Z_source'):
            Z_th = self.Z_source + Z_parallel
            Z_th_pu = self.Z_source_pu + Z_parallel_pu
        else:
            # Se não houver impedância da fonte, considera apenas as linhas
            Z_th = Z_parallel
            Z_th_pu = Z_parallel_pu

        print(f"\nImpedância de Thévenin (vista do ponto de falta):")
        print(f"  {Z_th.real:.4f} + j{Z_th.imag:.4f} Ω")
        print(f"  {Z_th_pu.real:.6f} + j{Z_th_pu.imag:.6f} pu")
        print(f"  Módulo: {abs(Z_th):.4f} Ω")
        print(f"  Ângulo: {np.angle(Z_th, deg=True):.2f}°")

        # Tensão pré-falta (assumindo tensão nominal)
        V_prefault = self.Vb / np.sqrt(3)  # Tensão de fase em V
        V_prefault_pu = 1.0  # pu

        print(f"\nTensão Pré-Falta (fase-neutro):")
        print(f"  {V_prefault/1e3:.4f} kV")
        print(f"  {V_prefault_pu:.4f} pu")

        # Corrente de curto-circuito no ponto de falta
        I_cc = V_prefault / Z_th  # A
        I_cc_pu = V_prefault_pu / Z_th_pu  # pu

        print("\n" + "="*80)
        print("CORRENTE DE CURTO-CIRCUITO NO PONTO DE FALTA")
        print("="*80)
        print(f"\nCorrente de Curto-Circuito (Icc):")
        print(f"  {abs(I_cc):.2f} A")
        print(f"  {abs(I_cc)/1e3:.4f} kA")
        print(f"  {abs(I_cc_pu):.4f} pu")
        print(f"  Ângulo: {np.angle(I_cc, deg=True):.2f}°")

        # Corrente de curto-circuito trifásica (3 fases)
        I_cc_3phase = np.sqrt(3) * abs(I_cc)
        print(f"\nCorrente de Curto-Circuito Trifásica Total:")
        print(f"  {I_cc_3phase/1e3:.4f} kA")

        # Cálculo das tensões na barra Z (assumindo que é a barra de origem)
        # Durante a falta, a tensão no ponto de falta é zero
        # A tensão na barra Z depende da queda de tensão nas linhas

        # Corrente pela linha L1 inteira
        I_L1 = V_prefault / self.Z_linha_total - I_cc * Z_half_L2 / (self.Z_linha_total + Z_half_L2)

        # Corrente pela meia linha L2
        I_L2_half = I_cc - I_L1

        # Tensão na barra Z durante a falta (considerando queda na impedância da fonte)
        if hasattr(self, 'Z_source'):
            # A corrente total que sai da barra Z
            I_total_source = I_cc
            V_bus_Z = V_prefault - self.Z_source * I_total_source
            V_bus_Z_pu = V_prefault_pu - self.Z_source_pu * I_cc_pu
        else:
            # Se não há impedância da fonte, a tensão na barra Z é a tensão pré-falta
            V_bus_Z = V_prefault
            V_bus_Z_pu = V_prefault_pu

        print("\n" + "="*80)
        print("TENSÕES NA BARRA Z")
        print("="*80)

        # Para curto-circuito trifásico simétrico, as tensões de sequência são:
        # V1 = tensão de sequência positiva
        # V2 = 0 (sequência negativa)
        # V0 = 0 (sequência zero)

        V1 = V_bus_Z
        V2 = complex(0, 0)
        V0 = complex(0, 0)

        print(f"\nTensões de Sequência na Barra Z:")
        print(f"  Sequência Positiva (V1): {abs(V1)/1e3:.4f} kV ∠{np.angle(V1, deg=True):.2f}°")
        print(f"  Sequência Negativa (V2): {abs(V2)/1e3:.4f} kV")
        print(f"  Sequência Zero (V0): {abs(V0)/1e3:.4f} kV")

        print(f"\nTensões de Sequência em pu:")
        print(f"  Sequência Positiva (V1): {abs(V_bus_Z_pu):.4f} pu ∠{np.angle(V_bus_Z_pu, deg=True):.2f}°")
        print(f"  Sequência Negativa (V2): {abs(V2):.4f} pu")
        print(f"  Sequência Zero (V0): {abs(V0):.4f} pu")

        # Matriz de transformação de Fortescue
        a = complex(-0.5, np.sqrt(3)/2)  # operador 120°
        A = np.array([[1, 1, 1],
                      [1, a**2, a],
                      [1, a, a**2]])

        # Vetor de tensões de sequência
        V_seq = np.array([V0, V1, V2])

        # Tensões de fase
        V_phase = np.dot(A, V_seq)

        Va = V_phase[0]
        Vb = V_phase[1]
        Vc = V_phase[2]

        print(f"\nTensões de Fase na Barra Z (fase-neutro):")
        print(f"  Va: {abs(Va)/1e3:.4f} kV ∠{np.angle(Va, deg=True):.2f}°")
        print(f"  Vb: {abs(Vb)/1e3:.4f} kV ∠{np.angle(Vb, deg=True):.2f}°")
        print(f"  Vc: {abs(Vc)/1e3:.4f} kV ∠{np.angle(Vc, deg=True):.2f}°")

        # Tensões de linha (fase-fase)
        Vab = Va - Vb
        Vbc = Vb - Vc
        Vca = Vc - Va

        print(f"\nTensões de Linha na Barra Z (fase-fase):")
        print(f"  Vab: {abs(Vab)/1e3:.4f} kV ∠{np.angle(Vab, deg=True):.2f}°")
        print(f"  Vbc: {abs(Vbc)/1e3:.4f} kV ∠{np.angle(Vbc, deg=True):.2f}°")
        print(f"  Vca: {abs(Vca)/1e3:.4f} kV ∠{np.angle(Vca, deg=True):.2f}°")

        print("\n" + "="*80)
        print("RESUMO DOS RESULTADOS")
        print("="*80)
        print(f"\n1. Corrente de Curto-Circuito (Icc):")
        print(f"   - Icc = {abs(I_cc)/1e3:.4f} kA ({abs(I_cc_pu):.4f} pu)")

        print(f"\n2. Tensões de Sequência na Barra Z:")
        print(f"   - V1 (sequência +): {abs(V1)/1e3:.4f} kV ({abs(V_bus_Z_pu):.4f} pu)")
        print(f"   - V2 (sequência -): {abs(V2)/1e3:.4f} kV")
        print(f"   - V0 (sequência 0): {abs(V0)/1e3:.4f} kV")

        print(f"\n3. Tensões de Fase na Barra Z:")
        print(f"   - Va: {abs(Va)/1e3:.4f} kV")
        print(f"   - Vb: {abs(Vb)/1e3:.4f} kV")
        print(f"   - Vc: {abs(Vc)/1e3:.4f} kV")

        print("\n" + "="*80)

        # Retornar resultados para uso posterior
        return {
            'I_cc_A': abs(I_cc),
            'I_cc_kA': abs(I_cc)/1e3,
            'I_cc_pu': abs(I_cc_pu),
            'I_cc_angle': np.angle(I_cc, deg=True),
            'V1_kV': abs(V1)/1e3,
            'V2_kV': abs(V2)/1e3,
            'V0_kV': abs(V0)/1e3,
            'Va_kV': abs(Va)/1e3,
            'Vb_kV': abs(Vb)/1e3,
            'Vc_kV': abs(Vc)/1e3,
            'Vab_kV': abs(Vab)/1e3,
            'Vbc_kV': abs(Vbc)/1e3,
            'Vca_kV': abs(Vca)/1e3,
            'Z_th_ohm': abs(Z_th),
            'Z_th_angle': np.angle(Z_th, deg=True)
        }


def main():
    """Função principal para executar a análise"""

    # Criar objeto de análise
    analysis = ShortCircuitAnalysis()

    # Definir o comprimento da linha (exemplo: 100 km)
    # NOTA: Ajuste este valor conforme necessário para o seu problema específico
    line_length = 100  # km
    analysis.set_line_length(line_length)

    # Definir impedância da fonte (opcional)
    # Se você tiver informações sobre a impedância da fonte, descomente e ajuste:
    # Z_source = complex(0.5, 5.0)  # Exemplo: 0.5 + j5.0 Ω
    # analysis.set_source_impedance(Z_source)

    # Calcular curto-circuito com linhas em paralelo
    results = analysis.calculate_parallel_lines_fault()

    print("\nAnálise concluída com sucesso!")
    print("Para modificar o comprimento da linha ou impedância da fonte,")
    print("edite os valores na função main() deste script.")


if __name__ == "__main__":
    main()
