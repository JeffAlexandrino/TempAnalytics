import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os

# Configurações gerais de estilo
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def carregar_dados(filepath):
    """
    Lê o CSV de temperaturas globais e retorna um DataFrame contendo as colunas:
    - date (datetime)
    - year (ano)
    - month (mês)
    - qualquer coluna de temperatura presente no CSV.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Arquivo '{filepath}' não encontrado.")
    df = pd.read_csv(filepath, parse_dates=['dt'])
    wanted = [
        'dt',
        'LandAverageTemperature', 'LandMinTemperature', 'LandMaxTemperature',
        'LandAverageTemperatureUncertainty',
        'LandAndOceanAverageTemperature', 'LandAndOceanAverageTemperatureUncertainty'
    ]
    # Mantém apenas as colunas que realmente existem no CSV
    cols = [c for c in wanted if c in df.columns]
    if 'dt' not in cols:
        raise ValueError("Coluna 'dt' não foi encontrada no CSV!")
    df = df[cols].rename(columns={'dt': 'date'})
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    return df


def get_season(month):
    """Retorna a estação do ano (em português) a partir do mês (1 a 12)."""
    if 3 <= month <= 5:
        return 'Primavera'
    elif 6 <= month <= 8:
        return 'Verão'
    elif 9 <= month <= 11:
        return 'Outono'
    else:
        return 'Inverno'


def plot_sazonal_com_incerteza(df):
    """
    Gráfico 1: Sazonal com incerteza.
    Considera apenas as colunas LandAverageTemperature e LandAverageTemperatureUncertainty,
    agrupando por ano e estação, e plota linhas com intervalo de incerteza.
    """
    # Garante que existem as colunas mínimas
    if 'LandAverageTemperature' not in df.columns:
        print("Aviso: coluna 'LandAverageTemperature' não encontrada. Pulando gráfico sazonal.")
        return
    if 'LandAverageTemperatureUncertainty' not in df.columns:
        print("Aviso: coluna 'LandAverageTemperatureUncertainty' não encontrada. Pulando gráfico sazonal.")
        return

    df['season'] = df['month'].apply(get_season)

    # Agrupa por (year, season) calculando média e média de incerteza
    seasonal = (
        df.dropna(subset=['LandAverageTemperature'])
          .groupby(['year', 'season'])
          .agg(
              LandAverageTemperature_mean=('LandAverageTemperature', 'mean'),
              LandAverageTemperatureUncertainty_mean=('LandAverageTemperatureUncertainty', 'mean')
          )
          .reset_index()
    )
    pivotado = seasonal.pivot(index='year', columns='season')

    seasons = ['Primavera', 'Verão', 'Outono', 'Inverno']
    colors = ['#2ca02c', '#ff7f0e', '#d62728', '#1f77b4']
    fig, ax = plt.subplots()
    for season, color in zip(seasons, colors):
        # Se faltar dados para alguma estação, preenche com séries vazias para evitar erro
        if season not in pivotado['LandAverageTemperature_mean']:
            continue
        y = pivotado['LandAverageTemperature_mean'][season]
        err = pivotado['LandAverageTemperatureUncertainty_mean'][season]
        years = pivotado.index.values
        ax.plot(years, y, label=f'Média de {season}', color=color)
        ax.fill_between(years, y - err, y + err, alpha=0.2, color=color)

    ax.set_title('Temperaturas Sazonais da Terra com Incerteza')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Temperatura (°C)')
    ax.legend(loc='best')
    plt.tight_layout()
    plt.show()


def plot_media_movel_10anos(df):
    """
    Gráfico 2: Média móvel de 10 anos da temperatura média global.
    Usa janela de 120 meses (min_periods=60) para suavizar.
    """
    if 'LandAverageTemperature' not in df.columns:
        print("Aviso: coluna 'LandAverageTemperature' não encontrada. Pulando média móvel.")
        return

    tmp_series = (
        df.set_index('date')['LandAverageTemperature']
          .dropna()
          .rolling(window=120, min_periods=60)
          .mean()
    )
    plt.figure()
    plt.plot(tmp_series.index.year, tmp_series.values)
    plt.title('Média Móvel de 10 Anos da Temperatura Média Global da Terra')
    plt.xlabel('Ano')
    plt.ylabel('Temperatura (°C)')
    plt.tight_layout()
    plt.show()


def plot_terra_vs_terraoceano(df):
    """
    Gráfico 3: Comparação Terra vs Terra+Oceano (média móvel de 12 meses).
    """
    if 'LandAverageTemperature' not in df.columns or 'LandAndOceanAverageTemperature' not in df.columns:
        print("Aviso: colunas 'LandAverageTemperature' ou 'LandAndOceanAverageTemperature' não encontradas. Pulando comparação.")
        return

    monthly = (
        df.set_index('date')
          [['LandAverageTemperature', 'LandAndOceanAverageTemperature']]
          .dropna()
          .rolling(window=12, min_periods=6)
          .mean()
    )
    plt.figure()
    plt.plot(
        monthly.index.year + (monthly.index.month - 1) / 12,
        monthly['LandAverageTemperature'], label='Terra'
    )
    plt.plot(
        monthly.index.year + (monthly.index.month - 1) / 12,
        monthly['LandAndOceanAverageTemperature'], label='Terra+Oceano'
    )
    plt.title('Média Móvel de 12 Meses: Terra vs Terra+Oceano')
    plt.xlabel('Ano')
    plt.ylabel('Temperatura (°C)')
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_por_decada(df):
    """
    Gráfico 4: Temperatura média por década (barra).
    """
    if 'LandAverageTemperature' not in df.columns:
        print("Aviso: coluna 'LandAverageTemperature' não encontrada. Pulando gráfico por década.")
        return

    df['decade'] = (df['year'] // 10) * 10
    decade_avg = (
        df.dropna(subset=['LandAverageTemperature'])
          .groupby('decade')['LandAverageTemperature']
          .mean()
          .reset_index()
    )
    plt.figure()
    sns.barplot(data=decade_avg, x='decade', y='LandAverageTemperature', color='salmon')
    plt.title('Temperatura Média Global por Década')
    plt.xlabel('Década')
    plt.ylabel('Temperatura (°C)')
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Visualização de temperatura global por estação.")
    parser.add_argument(
        '--grafico',
        choices=["Todos", "sazonal", "media_movel", "comparacao", "decadas"],
        default="Todos",
        help="Escolha o gráfico a ser exibido"
    )
    parser.add_argument(
    '--arquivo',
    default="scripts/data/GlobalTemperatures.csv",
    help="Caminho para o CSV de temperaturas globais"
)

    args = parser.parse_args()

    # Carrega os dados
    df = carregar_dados(args.arquivo)

    # Chama apenas a função correspondente ao gráfico solicitado
    if args.grafico == "sazonal":
        plot_sazonal_com_incerteza(df)
    elif args.grafico == "media_movel":
        plot_media_movel_10anos(df)
    elif args.grafico == "comparacao":
        plot_terra_vs_terraoceano(df)
    elif args.grafico == "decadas":
        plot_por_decada(df)
    else:  # "Todos"
        plot_sazonal_com_incerteza(df)
        plot_media_movel_10anos(df)
        plot_terra_vs_terraoceano(df)
        plot_por_decada(df)


if __name__ == "__main__":
    main()
