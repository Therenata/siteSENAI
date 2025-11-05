"""Análise simples do PIB com geração de gráficos.

Gera dois gráficos:
- `pib_por_ano.png` (linha do PIB por ano)
- `crescimento_pib.png` (barras com taxa de crescimento anual em %)

As imagens são salvas na pasta `Html/img/` do repositório para fácil inclusão em páginas.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import requests


def carregar_dados(url: str = None) -> pd.DataFrame:
    """Tenta obter dados do IBGE via API Sidra; se falhar, usa fallback para uma fonte pública.

    A função retorna um DataFrame com colunas pelo menos: ['ano', 'pib']
    """
    # Primeiro, tentar IBGE Sidra (assumindo tabela anual de PIB). Se falhar, usa fallback
    try:
        # Exemplo de consulta Sidra (pode ser ajustada conforme necessidade)
        sidra_url = 'https://apisidra.ibge.gov.br/values/t/5938/n1/1/v/all/p/all/c11255/90707/d/v585%202'
        resp = requests.get(sidra_url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        # Sidra retorna uma lista onde o primeiro elemento são cabeçalhos
        headers = data[0]
        rows = data[1:]
        # Tentar identificar colunas de ano e valor
        # Procurar o nome das colunas que contenham 'Year' ou 'Ano' e 'Valor' ou 'Value'
        df = pd.DataFrame(rows, columns=headers)
        # Normalizar nomes
        df.columns = [c.lower() for c in df.columns]
        # Tentar extrair ano e valor
        possible_year_cols = [c for c in df.columns if 'ano' in c or 'year' in c]
        possible_value_cols = [c for c in df.columns if 'valor' in c or 'value' in c or 'v' == c]
        if possible_year_cols and possible_value_cols:
            year_col = possible_year_cols[0]
            value_col = possible_value_cols[0]
            df2 = df[[year_col, value_col]].copy()
            df2.columns = ['ano', 'pib']
            # converter tipo
            df2['ano'] = pd.to_numeric(df2['ano'], errors='coerce')
            df2['pib'] = pd.to_numeric(df2['pib'].str.replace(',','.'), errors='coerce') if df2['pib'].dtype == object else pd.to_numeric(df2['pib'], errors='coerce')
            df2 = df2.dropna(subset=['ano', 'pib'])
            return df2
        else:
            print('Resposta IBGE recebida, mas não foi possível mapear colunas ano/pib. Usando fallback.')
    except Exception as e:
        print(f'Não foi possível obter dados diretamente do IBGE: {e}')

    # Fallback: usar CSV público conhecido
    fallback = 'https://raw.githubusercontent.com/datasets-brasil/pib/master/pib_ano.csv'
    try:
        df = pd.read_csv(fallback)
        # padronizar colunas
        if 'ano' in df.columns and 'pib' in df.columns:
            return df[['ano','pib']].copy()
        # tentar qualquer mapeamento simples
        for col in df.columns:
            if col.lower() in ('ano', 'year'):
                year = col
            if col.lower() in ('pib', 'valor'):
                pibcol = col
        if 'year' in locals() and 'pibcol' in locals():
            df2 = df[[year, pibcol]].copy()
            df2.columns = ['ano','pib']
            return df2
        return df
    except Exception as e:
        print(f'Erro ao carregar dados de fallback: {e}')
        return pd.DataFrame()


def gerar_plots(df: pd.DataFrame, salvar_em: str = None, mostrar: bool = False):
    if df.empty:
        print('DataFrame vazio — nenhum gráfico será gerado.')
        return

    # Agregar PIB por ano
    pib_por_ano = df.groupby('ano', as_index=True)['pib'].sum().sort_index()

    # Calcular crescimento percentual ano a ano
    crescimento = pib_por_ano.pct_change() * 100

    # Diretório de saída (por padrão, Html/img)
    if salvar_em is None:
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        # Salvar por padrão em Project - ok_test/img conforme solicitado
        salvar_em = os.path.join(repo_root, 'Project - ok_test', 'img')

    os.makedirs(salvar_em, exist_ok=True)

    # Plot 1: PIB por ano (linha)
    plt.figure(figsize=(10, 5))
    plt.plot(pib_por_ano.index, pib_por_ano.values, marker='o', color='#2b8cbe')
    plt.title('PIB por Ano')
    plt.xlabel('Ano')
    plt.ylabel('PIB (unidades)')
    plt.grid(alpha=0.25)
    caminho_pib = os.path.join(salvar_em, 'pib_por_ano.png')
    plt.tight_layout()
    plt.savefig(caminho_pib, dpi=150)
    if mostrar:
        plt.show()
    plt.close()

    # Plot 2: Crescimento percentual (barras)
    plt.figure(figsize=(10, 5))
    plt.bar(crescimento.index, crescimento.values, color='#66c2a5')
    plt.title('Crescimento Anual do PIB (%)')
    plt.xlabel('Ano')
    plt.ylabel('Crescimento (%)')
    plt.grid(axis='y', alpha=0.25)
    caminho_cres = os.path.join(salvar_em, 'crescimento_pib.png')
    plt.tight_layout()
    plt.savefig(caminho_cres, dpi=150)
    if mostrar:
        plt.show()
    plt.close()

    print(f'Gráficos salvos em: {salvar_em}\n- {os.path.basename(caminho_pib)}\n- {os.path.basename(caminho_cres)}')


def analise_pib(mostrar: bool = False):
    dados = carregar_dados()

    if dados.empty:
        print('Os dados estão vazios ou não puderam ser carregados.')
        return

    ano_atual = int(dados['ano'].max())
    pib_atual = dados[dados['ano'] == ano_atual]['pib'].sum()
    pib_anterior = dados[dados['ano'] == (ano_atual - 1)]['pib'].sum()

    crescimento = None
    if pib_anterior != 0:
        crescimento = (pib_atual - pib_anterior) / pib_anterior * 100

    print(f'PIB do ano atual ({ano_atual}): {pib_atual:.2f}')
    print(f'PIB do ano anterior ({ano_atual - 1}): {pib_anterior:.2f}')
    if crescimento is not None:
        print(f'Crescimento do PIB: {crescimento:.2f}%')
    else:
        print('Não foi possível calcular crescimento (divisão por zero).')

    # Gerar e salvar gráficos
    gerar_plots(dados, mostrar=mostrar)


if __name__ == '__main__':
    # Ao executar diretamente, gera os gráficos e não abre a janela (útil para servidores/CI)
    analise_pib(mostrar=False)
