# Machine Learning na Confiabilidade Industrial

Esse repositório contém os código e dados utilizados para minha dissertação de mestrado. 

O objetivo do estudo foi a criação de um modelo integrado para otimização do intervalo entre manutenções preventivas, por meio de previsão ajustada por Machine Learning de dados de tempo até falha e otimização de indicadores da manutenção industrial. O trabalho se divide em 3 partes:

- Ajuste de dados TFF a curvas de distribuição Weibull por meio de ML e Lognormal por aritmética
- Otimização dos indicadores industriais por meio do método PSO
- Criação de uma aplicação para Windows (standalone) e terminal para realizar as etapas acima

# Conteúdo do repositório

- Pasta principal: Arquivos importantes para criação, treinamento e execução das redes neurais e geração de dados sintéticos
- Resultados Lognormal: Planilha do Excel com resultados para a distribuição Lognormal
- Resultados Weibull: Planilhas do Excel com resultados para a distribuição Weibull
- Treinamentos: Redes Neurais treinadas para ajuste a distribuição Weibull
- Data: Planilhas do Excel com os bancos de dados gerados e utilizados nesse trabalho
- App: Pasta contendo aplicação para terminal

OBS: Para aplicação standalone ver seção *Releases*.

# Aplicativo

O aplicativo foi desenvolvido para facilitar a utilização dos algoritmos desenvolvidos nesse trabalho.

O aplicativo é divido em três abas que refletem a divisão do trabalho: Dados, Indicadores e Otimização. A aba Sobre contém créditos, links de interesse e acesso a conteúdo de ajuda e Tutorial.

## Dados 
![Screenshot 1](https://user-images.githubusercontent.com/64225460/135008233-5db257d5-1a12-4d30-bce4-ca5d1ff793aa.jpg)

-Introdução dos dados TTF, escolha de uma distribuição por meio do coeficiente de determinação e outras operações.

## Indicadores
![Screenshot 2](https://user-images.githubusercontent.com/64225460/135008451-2f77f4cb-c129-4b64-92f5-17c99401aa97.jpg)

-Cálculo dos indicadores confiabilidade e taxa de falha.

## Otimização
![Screenshot 3](https://user-images.githubusercontent.com/64225460/135008571-9a7b1bf6-4389-47cf-98f9-6d5f8bd53568.jpg)

-Otimização do intervalo para Manutenção preventiva e cálculo do custo de operação esperado para o equipamento/sistema. O processo de otimização usa processos do aplicativo [Opp!](https://github.com/LukeKort/Opp/releases).

![Screenshot 4](https://user-images.githubusercontent.com/64225460/135008672-bd4c4f27-5d6d-4b0a-b923-97e98884b1a2.jpg)

-Os gráficos disponíveis permitem uma melhor visualização do comportamento dos indicadores industriais e otimização.

## Instruções

-Execute o arquivo main.py. Outras instruções e arquivo de ajuda na aba *Sobre*

## Requisitos

-Você precisará das seguintes bibliotecas instaladas:

- **Numpy** 1.19.5 ou mais novo
- **Pandas** 1.2.4 ou mais novo
- **PyQt5** 5.9.2 ou mais novo
- **tkinter** 8.6.10 ou mais novo
- **Matplotlib** 3.3.4 ou mais novo
- **Tensorflow** 2.5.0 ou mais novo

OBS: Testado em Python 3.8.10.
