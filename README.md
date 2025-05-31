# Análise de Temperaturas Globais

Este projeto tem como finalidade a análise exploratória de dados climáticos históricos, com ênfase na variação da temperatura da superfície terrestre ao longo do tempo. A proposta visa compreender padrões, tendências e variações sazonais, tanto em nível global quanto nacional, a partir de dados provenientes de fontes confiáveis e amplamente reconhecidas.

Por meio da linguagem Python e de bibliotecas especializadas em ciência de dados, os dados são processados, transformados e visualizados de maneira clara e intuitiva, permitindo insights significativos sobre o comportamento térmico do planeta.

## Estrutura do Projeto

A organização dos diretórios e arquivos tem por objetivo garantir a modularidade e clareza da aplicação:

```
TEMPANALYTICS/
│
├── .venv/                         
│
├── scripts/                      
│   ├── data/                      # Conjunto de arquivos CSV com os dados brutos
│   │   ├── GlobalTemperatures.csv
│   │   └── GlobalLandTemperaturesByCountry.csv
│   ├── tempGlobal.py              # Geração de gráficos e análises com base em dados globais
│   └── tempPaises.py              # Geração de gráficos e análises por país
│
├── menu.py                        # Interface interativa para seleção e execução das análises   
│
└── README.md                      
```

## Funcionalidades

O projeto está dividido em três módulos principais:

### 1. Análises Globais (`tempGlobal.py`)
Responsável pela análise dos dados contidos em `GlobalTemperatures.csv`, este módulo permite:

- Visualizar a média global das temperaturas ao longo do tempo.
- Comparar dados globais com e sem inclusão de áreas oceânicas.
- Aplicar médias móveis para melhor interpretação de tendências.
- Realizar comparações por década, por mês ou por estação do ano.

### 2. Análises por País (`tempPaises.py`)
Utilizando os dados presentes em `GlobalLandTemperaturesByCountry.csv`, este script fornece:

- Evolução histórica da temperatura média em países específicos.
- Comparações entre múltiplos países selecionados.
- Filtros personalizados por período e localização geográfica.
- Gráficos que ilustram a intensificação das variações térmicas locais.

### 3. Interface Gráfica (`menu.py`)
A interface gráfica, desenvolvida com a biblioteca `tkinter`, proporciona uma experiência acessível e objetiva:

- Navegação por meio de menus para escolher o tipo de análise.
- Integração com os scripts analíticos.
- Execução facilitada de gráficos com base na escolha do usuário.

## Como Executar

### 1. Pré-requisitos

- Python 3.7 ou superior instalado na máquina.
- Recomendável o uso de ambiente virtual para gerenciamento das dependências.

### 2. Instalação das dependências

Execute o seguinte comando no terminal:

```bash
pip install pandas matplotlib seaborn
```

### 3. Execução

Para utilizar a interface gráfica do projeto:

```bash
python menu.py
```

Na interface, selecione o tipo de análise desejada, a opção de gráfico e clique em **Executar**.

Caso prefira executar diretamente via terminal:

```bash
python scripts/tempGlobal.py
python scripts/tempPaises.py
```

## Fonte dos Dados

Os dados utilizados nesta aplicação foram obtidos do repositório [Kaggle - Berkeley Earth](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data), amplamente reconhecido por sua qualidade e confiabilidade. Os conjuntos de dados incluem:

- `GlobalTemperatures.csv`: média global das temperaturas da superfície, incluindo dados com e sem oceano.
- `GlobalLandTemperaturesByCountry.csv`: série histórica de temperaturas médias por país.

## Licença

Este projeto é de uso acadêmico e educativo. Não possui fins comerciais e está disponível para fins de estudo, modificação e aprimoramento conforme necessário.
