import streamlit as st
import pandas as pd
import json
import requests
import numpy as np


def load_file(upload_file):
    if upload_file is not None:
        if upload_file.name.endswith('.csv'):
            df = pd.read_csv(upload_file)
        elif upload_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(upload_file)
        else:
            st.error('Arquivo nao suportado!')
            return None
        return df
    else:
        return None
    
def call_api(data_test):
    url = 'https://fiscal-milka-thales-7d33bed5.koyeb.app/empresa/predict'
    header = {'Content-type': 'application/json'}
    data = json.dumps(data_test.to_dict(orient='records'))

    r = requests.post(url, data=str(data), headers=header)
    return r.json()



st.title('Previsões de Entrega de Pedidos')


uploaded_file = st.file_uploader(label='Escolha um arquivo CSV ou Excel para prever o tempo de entrega', type=['csv','xls', 'xlsx'])

df = load_file(uploaded_file)

if df is not None:
    st.write('Base de Dados para Prever:')
    st.dataframe(df)

    response = call_api(df)
    st.write('Previsões feitas pelo nosso modelo')
    df_response = pd.DataFrame(response)
    df_response['prediction'] = np.expm1(df_response['prediction'])
    st.dataframe(df_response)



