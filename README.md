# TCC - Análise de Curto-Circuito em Sistemas de Potência

Este repositório contém ferramentas para análise de curto-circuito trifásico em sistemas de potência com linhas de transmissão em paralelo.

## Descrição do Problema

O script `short_circuit_analysis.py` resolve o seguinte problema:

**Configuração do Sistema:**
- Impedância da linha: Z+ = 0.05 + j0.45 Ω/km
- Potência base: Sb = 100 MVA
- Tensão do lado de alta: 230 kV
- Configuração: Duas linhas idênticas em paralelo (L1 e L2)

**Análise:**
- Aplica um curto-circuito trifásico na metade da linha L2
- Calcula a corrente de curto-circuito (Icc)
- Calcula as tensões de sequência na barra Z
- Calcula as tensões de fase na barra Z

## Instalação

### Requisitos
- Python 3.6 ou superior
- NumPy

### Instalação das Dependências

```bash
pip install -r requirements.txt
```

Ou instalar manualmente:

```bash
pip install numpy
```

## Uso

Execute o script principal:

```bash
python3 short_circuit_analysis.py
```

### Personalização

Você pode modificar os parâmetros do sistema editando o arquivo `short_circuit_analysis.py`:

**1. Comprimento da Linha:**
```python
line_length = 100  # km (modifique este valor)
analysis.set_line_length(line_length)
```

**2. Impedância da Fonte (opcional):**
```python
Z_source = complex(0.5, 5.0)  # Ω (descomente e ajuste)
analysis.set_source_impedance(Z_source)
```

## Resultados da Análise

O script fornece os seguintes resultados:

### 1. Corrente de Curto-Circuito
- Corrente no ponto de falta em A, kA e pu
- Ângulo da corrente
- Corrente trifásica total

### 2. Tensões de Sequência na Barra Z
- Tensão de sequência positiva (V1)
- Tensão de sequência negativa (V2)
- Tensão de sequência zero (V0)

### 3. Tensões de Fase na Barra Z
- Tensões fase-neutro (Va, Vb, Vc)
- Tensões fase-fase (Vab, Vbc, Vca)

## Exemplo de Saída

```
================================================================================
ANÁLISE DE CURTO-CIRCUITO TRIFÁSICO
================================================================================

Parâmetros do Sistema:
  Potência Base (Sb): 100 MVA
  Tensão Base (Vb): 230 kV
  Impedância da Linha (Z+): 0.05 + j0.45 Ω/km
  Impedância Base (Zb): 529.0000 Ω
  Corrente Base (Ib): 251.02 A

Comprimento da Linha: 100 km
  Impedância Total de uma Linha: 5.0000 + j45.0000 Ω

================================================================================
RESUMO DOS RESULTADOS
================================================================================

1. Corrente de Curto-Circuito (Icc):
   - Icc = 8.7986 kA (35.0510 pu)

2. Tensões de Sequência na Barra Z:
   - V1 (sequência +): 132.7906 kV (1.0000 pu)
   - V2 (sequência -): 0.0000 kV
   - V0 (sequência 0): 0.0000 kV

3. Tensões de Fase na Barra Z:
   - Va: 132.7906 kV
   - Vb: 132.7906 kV
   - Vc: 132.7906 kV
```

## Metodologia

### Configuração do Sistema

O sistema consiste em:
- Duas linhas de transmissão idênticas (L1 e L2) conectadas em paralelo
- Linha L1: conecta as barras inteira
- Linha L2: falta aplicada na metade da linha

### Cálculo da Impedância Equivalente

1. **Impedância de meia linha L2:** Z_L2/2
2. **Impedância equivalente:** Z_eq = (Z_L1 × Z_L2/2) / (Z_L1 + Z_L2/2)
3. **Impedância de Thévenin:** Z_th = Z_source + Z_eq (se houver fonte)

### Cálculo da Corrente de Curto-Circuito

Para um curto-circuito trifásico:
- I_cc = V_prefault / Z_th

Onde:
- V_prefault = tensão pré-falta (tensão nominal)
- Z_th = impedância de Thévenin vista do ponto de falta

### Tensões de Sequência

Para curto-circuito trifásico simétrico:
- V1 = tensão de sequência positiva (calculada)
- V2 = 0 (sequência negativa)
- V0 = 0 (sequência zero)

### Tensões de Fase

Utilizando a transformação de Fortescue:
- V_abc = A × V_012

Onde A é a matriz de transformação e V_012 é o vetor de tensões de sequência.

## Estrutura do Código

```
short_circuit_analysis.py
├── ShortCircuitAnalysis (classe principal)
│   ├── __init__() - Inicializa parâmetros do sistema
│   ├── set_line_length() - Define comprimento da linha
│   ├── set_source_impedance() - Define impedância da fonte
│   └── calculate_parallel_lines_fault() - Calcula curto-circuito
└── main() - Função principal
```

## Conceitos de Sistemas de Potência

### Sistema por Unidade (pu)

O sistema por unidade normaliza grandezas usando valores base:
- Potência base: Sb = 100 MVA
- Tensão base: Vb = 230 kV
- Impedância base: Zb = Vb² / Sb
- Corrente base: Ib = Sb / (√3 × Vb)

### Componentes Simétricas

Método de Fortescue para análise de sistemas desequilibrados:
- Sequência positiva: rotação ABC
- Sequência negativa: rotação ACB
- Sequência zero: componente homopolar

### Curto-Circuito Trifásico

- Tipo mais severo de falta
- Sistema permanece balanceado
- Apenas componente de sequência positiva presente
- Correntes e tensões simétricas

## Referências

- Stevenson, W. D. (1982). Elements of Power System Analysis
- Grainger, J. J., & Stevenson, W. D. (1994). Power System Analysis
- Anderson, P. M. (1995). Analysis of Faulted Power Systems

## Autor

Luiz Gustavo Galassi

## Licença

Este projeto é fornecido como material educacional para análise de sistemas de potência.
