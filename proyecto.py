import streamlit as st
import pandas as pd
import numpy as np
import google
import altair as alt

alt.data_transformers.enable('default', max_rows=None)
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
    
    st.title("Proyecto Visualización")
    st.header("Integrandes: Edgar Heredia, Alejandro García y Misael Zavala.")
with st.expander("Acerca de los datos", expanded=False):
    st.write(
        """     
Para este proyecto trabajaremos con los datos de venta de la empresa de logistica TonyStar, esta empresa participa en el mercado de Corrier a nivel nacional con cobertura de Arica a Punta Areas con una red de 300 sucursales generando más de 700.000 de envíos al mes.

La data con la que trabajaremos se encuentra alterada por motivos de seguridad de la compañia y ninguna de los valores es real ademas esta se encuentra agrupada a nivel de regiones. 

Contamos son las ventas desde 2018 a 2022 en ordenes de flete (tickets de venta por cliente) y la venta neta siguiente nivel de detalle: 
	    """
    )
    st.image("tabla_datos.png")
    st.markdown("")
st.markdown("")

df_ventas=pd.read_csv('datos_uc.csv',delimiter=';')
df_od=pd.pivot_table(df_ventas,values=['Venta_Neta','Ofs'],index=['Fecha','Origen_Zona','Destino_Zona'],aggfunc=np.sum).reset_index()
df_od['Fecha']=pd.to_datetime(df_od['Fecha'],dayfirst=True)

color = alt.Color('Destino_Zona:N',title='Zona de Destino')
dest= alt.selection_multi(encodings=['color'])
brush = alt.selection_interval(encodings=['x'])

g_od = alt.Chart(df_od).mark_bar().encode(
    x=alt.X('sum(Ofs):Q', stack='normalize',axis=alt.Axis(format=".0%"),title='% de Ofs'),
    y=alt.Y('Origen_Zona:N', title='Zona de Origen'),
    color=alt.condition(dest,color,alt.value('lightgray'),title='Zona de Destino')
).properties(
    width=1000,
    height=500,
    title='Distribución de Ordenes de Flete en % según Origen y Destino'
).transform_filter(
    brush
).add_selection(
    dest
)

ofs=alt.Chart(df_od).mark_line().encode(
    alt.X('Fecha:T', title='Fecha de Envios'),
    alt.Y('sum(Ofs):Q',title='Ordenes de Flete Mensuales'),
).add_selection(
    brush
).properties(
    width=1000,
    height=200,
    title='Ordenes de Flete Distribuidas por Periodo Enero 2018 a Junio 2022'
).transform_filter(
    dest
)

grafico1=alt.vconcat(
    ofs,
    g_od,
    title="Ordenes de Flete 2018 a 2022 y su Distribucion según Origen y Destino"
)

st.altair_chart(grafico1)


