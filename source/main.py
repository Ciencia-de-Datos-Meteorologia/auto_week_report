import streamlit as st
import google_tools

# Initialize streamlit page
st.set_page_config(initial_sidebar_state='collapsed')
st.title('Compilación de informe semanal')

client_secrets = st.secrets.client_secret
# print(client_secrets)

drive_sevice = google_tools.get_drive_service(client_secrets)

st.sidebar.markdown('## Parámetros adicionales')

week_report_folder_id = st.sidebar.text_input(
    'ID de la carpeta "Informe Mensual"', '1gOzvoBpXS1hzAwIE3ihJEvoBXT9lj45b')
