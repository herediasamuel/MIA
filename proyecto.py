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

df_ventas=pd.read_csv('datos_uc.csv',delimiter=';')


venta_mensual_ori=pd.pivot_table(df_ventas,values=['Venta_Neta','Ofs'],index=['Fecha','Origen_Zona'],aggfunc=np.sum).reset_index()


st.table(venta_mensual_ori)

selection = alt.selection_multi(fields=['Origen_Zona'], bind='legend')

st.altair_chart(
    alt.Chart(venta_mensual_ori).mark_area().encode(
        alt.X('yearmonth(Fecha Nominal):N', title='Fecha'),
        alt.Y('sum(Ofs):Q'),
        alt.Color('Origen_Zona:N', title='Zona de Origen'),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).add_selection(
        selection
    ).properties(
        width=700,
        height=300,
        title='Ofs por Zona de Origen'
    )
)
