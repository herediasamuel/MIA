import streamlit as st
import pandas as pd
import numpy as np
import google

#from google.oauth2 import service_account
#from google.cloud import storage

# Create API client.
#credentials = service_account.Credentials.from_service_account_info(
#    st.secrets["gcp_service_account"]
#)
#client = storage.Client(credentials=credentials)

st.title('Proyecto Visualizacion')

df_ventas=pd.read_excel('MIA/Dummy UC.xlsx',sheet_name='BDD')
st.table(df_ventas)
