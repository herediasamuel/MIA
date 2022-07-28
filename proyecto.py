import streamlit as st
import pandas as pd
import numpy as np
import google
import altair as alt
import base64

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
    file_ = open("intro.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    file2_ = open("equipo.gif", "rb")
    contents2 = file2_.read()
    data2_url = base64.b64encode(contents2).decode("utf-8")
    file2_.close()
    st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
    )
    f'<img src="data:image/gif;base64,{data2_url}" alt="cat gif">',
    unsafe_allow_html=True,
    )
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

### Primer idioms

df_ventas=pd.read_csv('datos_uc.csv',delimiter=';')
df_od=pd.pivot_table(df_ventas,values=['Venta_Neta','Ofs'],index=['Fecha','Origen_Zona','Destino_Zona'],aggfunc=np.sum).reset_index()
df_od['Fecha']=pd.to_datetime(df_od['Fecha'],dayfirst=True)

### Grafico de Origen - Destino

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

# Grafico de Venta Anual

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


### Segundo idioms

df_cat=pd.pivot_table(df_ventas,values=['Venta_Neta','Ofs'],index=['Fecha','Nombre_Categoria','Tipo_de_Entrega','Tipo_de_Emision_Origen','Origen_Zona','Destino_Zona'],aggfunc=np.sum).reset_index()
df_cat['Fecha']=pd.to_datetime(df_cat['Fecha'],dayfirst=True)

## Grafico de Barras de Origen

color = alt.Color('Tipo_de_Emision_Origen:N',title='Tipo de Emision de Origen',scale=alt.Scale(scheme='tableau20'))
ori_2= alt.selection_multi(encodings=['color'])
g_os = alt.Chart(df_cat).mark_bar().encode(
    y=alt.Y('sum(Ofs):Q', stack='normalize',axis=alt.Axis(format=".0%"),title='% de Ofs'),
    x=alt.X('Origen_Zona:N', title='Zona de Origen'),
    color=alt.condition(ori_2,color,alt.value('lightgray'),title='Tipo de Emision de Origen')
).properties(
    width=500,
    height=200,
    title='Distribución de Ofs en % según Origen y tipo de Entrega'
).add_selection(
    ori_2
)

## Grafico de Barras de Destino

color = alt.Color('Tipo_de_Entrega:N',title='Tipo de Entrega',scale=alt.Scale(scheme='dark2'))
dest_2= alt.selection_multi(encodings=['color'])
g_ds = alt.Chart(df_cat).mark_bar().encode(
    y=alt.Y('sum(Ofs):Q', stack='normalize',axis=alt.Axis(format=".0%"),title='% de Ofs'),
    x=alt.X('Destino_Zona:N', title='Zona de Destino'),
    color=alt.condition(dest_2,color,alt.value('lightgray'),title='Tipo de Entrega')
).properties(
    width=500,
    height=200,
    title='Distribución de Ofs en % según Origen y tipo de Entrega'
).add_selection(
    dest_2
)

## Grafico de Venta por Categoria

color=alt.Color('Nombre_Categoria:N',title='Categoria Cliente')
cat= alt.selection_multi(encodings=['color'])
g_cat=alt.Chart(df_cat).mark_bar().encode(
    alt.X('Fecha:T', title='Fecha'),
    alt.Y('sum(Ofs):Q'),
    color=alt.condition(cat,color,alt.value('lightgray'),title='Tipo de Entrega'),
).add_selection(
    cat
).properties(
    width=1000,
    height=200,
    title='Ofs por Periodo Enero 2018 a Junio 2022'
)
g_os=g_os.transform_filter(
    cat
)
g_ds=g_ds.transform_filter(
    cat
)

### Union de Graficos

o_d=g_os|g_ds

grafico_2=alt.vconcat(
    g_cat,
    o_d,
    title="Ordenes de Flete 2018 a 2022 según Origen, Tipo de Origen, Destino y Tipo de Entrega"
)

st.altair_chart(grafico_2)
