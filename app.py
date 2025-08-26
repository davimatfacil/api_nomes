import pandas as pd
import requests
import streamlit as st


def fazer_requisicao(url, params = None):
    resposta = requests.get(url = url, params = params)
    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f'Erro na requisição: {e}')
        resultado = None
    else:
        resultado = resposta.json()
    return resultado

def pegar_nome_por_decada(nome):
    url = f'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}'
    nome_por_decada = fazer_requisicao(url)
    if not nome_por_decada:
        return {}
    dicionario_decadas = {}
    for dados in nome_por_decada[0]['res']:
        decada = dados['periodo']
        quantidade = dados['frequencia']
        dicionario_decadas[decada] = quantidade
    return dicionario_decadas


def main():
    st.title('Nomes do Brasil')
    st.write('Dados do IBGE (fonte: https://servicodados.ibge.gov.br/api/docs/nomes?versao=2)')
    nome = st.text_input('Digite um nome')
    if not nome:
        st.stop()

    dicionario_decadas = pegar_nome_por_decada(nome)
    df = pd.DataFrame.from_dict(dicionario_decadas, orient='index')
    st.bar_chart(df)

if __name__ == '__main__':
    main()
