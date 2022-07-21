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

st.set_page_config(layout="wide", page_title="Trabajo Aplicaciones",page_icon="🎈")



def _max_width_():
    max_width_str = f"max-width: 1400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )
_max_width_()
c30, c31, c32 = st.columns([2.5, 1, 3])
with c30:
    
    st.title("Proyecto Visualizacion")
    st.header("")
with st.expander("Acerca de los datos", expanded=True):
    st.write(
        """     
Para este proyecto trabajaremos con los datos de venta de la empresa de logistica TonyStar, esta empresa participa en el mercado de Corrier a nivel nacional con cobertura de Arica a Punta Areas con una red de 300 sucursales generando más de 1.000.000 de envíos al mes.

La data con la que trabajaremos se encuentra alterada por motivos de seguridad de la compañia y ninguna de los valores es real ademas esta se encuentra agrupada a nivel de regiones. 

Contamos son las ventas desde 2018 a 2022 en ordenes de flete (tickets de venta por cliente) y la venta neta siguiente nivel de detalle: 
	    """
    )
    st.image("datos.png")
    st.markdown("")
st.markdown("")

df_ventas=pd.read_csv('datos_uc.csv',delimiter=';')
venta_mensual_ori=pd.pivot_table(df_ventas,values=['Venta_Neta','Ofs'],index=['Fecha','Origen_Zona'],aggfunc=np.sum).reset_index()
selection = alt.selection_multi(fields=['Origen_Zona'], bind='legend')

st.altair_chart(
    alt.Chart(venta_mensual_ori).mark_area().encode(
        alt.X('yearmonth(Fecha):T', title='Fecha'),
        alt.Y('sum(Ofs):Q'),
        alt.Color('Origen_Zona:N', title='Zona de Origen'),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).add_selection(
        selection
    ).properties(
        width=1400,
        height=500,
        title='Ofs por Zona de Origen'
    )
)
