import streamlit as st
import google_tools
import datetime as dt
import pandas as pd

# Initialize streamlit page
st.set_page_config(initial_sidebar_state='collapsed')
st.title('Compilación de informe semanal')

client_secret = st.secrets.client_secret
# print(client_secrets)

# drive_sevice = google_tools.get_drive_service(client_secret)
drive_service = google_tools.get_authenticated_credentials(client_secret)
st.markdown(f'[Click here]({drive_service[0]})')
# people_service = google_tools.get_people_service(client_secret)

st.sidebar.markdown('## Parámetros adicionales')

week_report_folder_id = st.sidebar.text_input(
    'ID de la carpeta "Informe Mensual"', '1gOzvoBpXS1hzAwIE3ihJEvoBXT9lj45b')

run_date = st.sidebar.date_input('Fecha de inicialización',
                                 dt.datetime.today(), format='DD/MM/YYYY')

monday = run_date + dt.timedelta(-run_date.weekday())
friday = run_date + dt.timedelta(4 - run_date.weekday())

report_type = st.radio('Tipo de reporte:', ['Pre', 'Post'])

if report_type == 'Pre':
    week_name = friday.strftime('%Y-%m-%d')
elif report_type == 'Post':
    week_name = monday.strftime('%Y-%m-%d')

st.text(week_name)

# email = st.text_input('Correo')
# name = google_tools.search_name(people_service, email)

# st.markdown(f'**Name:** {name}')

section_folders = [
    'aplicaciones_climaticas',
    'cambio_climatico',
    'ciencia_de_datos',
]


report_files = []

for folder in section_folders:
    section_files_query = google_tools.list_files_from_path(
        f'{folder}/{week_name}', drive_sevice, week_report_folder_id)
    if section_files_query is not None:
        section_files = [f for f in section_files_query if f['mimeType']
                         == 'application/vnd.google-apps.spreadsheet']
        report_files += section_files


for report in report_files:
    google_tools.download_file(report['id'], 'temp_report.csv', drive_sevice)
    data = pd.read_csv('temp_report.csv')
    st.dataframe(data)
