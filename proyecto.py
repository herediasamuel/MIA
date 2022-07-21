import streamlit as st
import pandas as pd
import numpy as np
import google
import altair as alt

#from google.oauth2 import service_account
#from google.cloud import storage

# Create API client.
#credentials = service_account.Credentials.from_service_account_info(
#    st.secrets["gcp_service_account"]
#)
#client = storage.Client(credentials=credentials)

st.title('Proyecto Visualizacion')

df_ventas=pd.read_csv('datos_uc.csv',delimiter='\t')


venta_mensual=pd.pivot_table(df_ventas,values=['Ofs'],index=['Fecha','Nombre_Categoria'],aggfunc=np.sum)
st.table(venta_mensual)

st.altair_chart(
    alt.Chart(venta_mensual).mark_bar().encode(
        alt.X('yearmonth(Fecha):N', title='Fecha'),
        alt.Y('Ofs:Q', title='Venta Neta Mensual'), 
    ).properties(
        width=1000,
        height=500,
        title='Ventas Netas Mensaules 2018 a 2022'
    )
)

