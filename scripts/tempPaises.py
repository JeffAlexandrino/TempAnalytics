import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os

# ---------------------------------------------------------------
# Função para carregar e preparar o DataFrame
# ---------------------------------------------------------------
def carregar_dados(filepath):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Arquivo '{filepath}' não encontrado.")
    df = pd.read_csv(filepath)
    df['dt'] = pd.to_datetime(df['dt'])
    df['ano'] = df['dt'].dt.year
    df['mes'] = df['dt'].dt.month
    # Remove linhas sem valor de temperatura
    df = df.dropna(subset=['AverageTemperature'])
    return df


# ---------------------------------------------------------------
# Funções de plotagem separadas
# ---------------------------------------------------------------
def plot_evolucao_por_pais(df):
    """
    Gráfico 1: Evolução da temperatura média ao longo do tempo por país.
    """
    paises = [
        "Brazil", "Argentina", "Chile", "Peru", "Colombia",
        "United States", "Canada", "Mexico",
        "China", "India", "Japan", "Russia",
        "Germany", "France", "United Kingdom", "Italy", "Spain"
    ]
    plt.figure(figsize=(16, 8))
    for pais in paises:
        serie = df[df['Country'] == pais].groupby('ano')['AverageTemperature'].mean()
        plt.plot(serie.index, serie.values, label=pais)
    plt.title('1. Evolução da Temperatura Média por País (Celsius)', fontsize=16)
    plt.xlabel('Ano')
    plt.ylabel('Temperatura Média (°C)')
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_media_por_decada_paises(df):
    """
    Gráfico 2: Temperatura média por década (linha para cada país).
    """
    df['decada'] = (df['ano'] // 10) * 10
    df_decadas = df.groupby(['Country', 'decada'])['AverageTemperature'].mean().reset_index()
    plt.figure(figsize=(16, 8))
    sns.lineplot(data=df_decadas, x='decada', y='AverageTemperature', hue='Country')
    plt.title('2. Temperatura Média por Década (Celsius)', fontsize=16)
    plt.xlabel('Década')
    plt.ylabel('Temperatura Média (°C)')
    plt.legend(title='País')
    plt.tight_layout()
    plt.show()


def plot_amplitude_termica(df):
    """
    Gráfico 3: Amplitude térmica anual por país (máx - mín).
    """
    amplitudes = df.groupby(['Country', 'ano'])['AverageTemperature'].agg(['max', 'min'])
    amplitudes['amplitude'] = amplitudes['max'] - amplitudes['min']
    amplitudes = amplitudes.reset_index()
    plt.figure(figsize=(16, 8))
    sns.lineplot(data=amplitudes, x='ano', y='amplitude', hue='Country')
    plt.title('3. Amplitude Térmica Anual por País', fontsize=16)
    plt.xlabel('Ano')
    plt.ylabel('Amplitude (°C)')
    plt.tight_layout()
    plt.show()


def plot_distribuicao_temperaturas(df):
    """
    Gráfico 4: Densidade da distribuição de temperaturas médias por país.
    """
    paises = [
        "Brazil", "Argentina", "Chile", "Peru", "Colombia",
        "United States", "Canada", "Mexico",
        "China", "India", "Japan", "Russia",
        "Germany", "France", "United Kingdom", "Italy", "Spain"
    ]
    plt.figure(figsize=(16, 8))
    for pais in paises:
        sns.kdeplot(df[df['Country'] == pais]['AverageTemperature'], label=pais, fill=True)
    plt.title('4. Distribuição de Temperaturas Médias por País', fontsize=16)
    plt.xlabel('Temperatura Média (°C)')
    plt.ylabel('Densidade')
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_mapa_calor_brasil(df):
    """
    Gráfico 5: Mapa de calor de temperatura média mensal por ano somente para o Brasil.
    """
    if 'Brazil' not in df['Country'].unique():
        print("Aviso: não há dados do Brasil neste CSV. Pulando mapa de calor.")
        return

    brasil = df[df['Country'] == 'Brazil']
    temp_mensal = brasil.groupby(['ano', 'mes'])['AverageTemperature'].mean().unstack()
    plt.figure(figsize=(14, 10))
    sns.heatmap(temp_mensal, cmap='YlOrRd', linewidths=0.5, linecolor='gray')
    plt.title('5. Mapa de Calor: Temperatura Média no Brasil (Ano × Mês)', fontsize=16)
    plt.xlabel('Mês')
    plt.ylabel('Ano')
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Visualização de variação de temperatura por país.")
    parser.add_argument(
        '--grafico',
        choices=["Todos", "evolucao", "decada", "amplitude", "distribuicao", "mapa"],
        default="Todos",
        help="Escolha o gráfico a ser exibido"
    )
    parser.add_argument(
    '--arquivo',
    default="scripts/data/GlobalLandTemperaturesByCountry.csv",
    help="Caminho para o CSV de temperaturas por país"
)

    args = parser.parse_args()

    # Carrega dados ou dispara FileNotFoundError
    df = carregar_dados(args.arquivo)

    # Determina qual função de plot executar
    if args.grafico == "evolucao":
        plot_evolucao_por_pais(df)
    elif args.grafico == "decada":
        plot_media_por_decada_paises(df)
    elif args.grafico == "amplitude":
        plot_amplitude_termica(df)
    elif args.grafico == "distribuicao":
        plot_distribuicao_temperaturas(df)
    elif args.grafico == "mapa":
        plot_mapa_calor_brasil(df)
    else:  # "Todos"
        plot_evolucao_por_pais(df)
        plot_media_por_decada_paises(df)
        plot_amplitude_termica(df)
        plot_distribuicao_temperaturas(df)
        plot_mapa_calor_brasil(df)


if __name__ == "__main__":
    main()
