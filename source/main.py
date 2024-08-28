import streamlit as st
import google_tools
import datetime as dt
import pandas as pd

metadata_id = '1LcFZ3YqS8TcgA6zl5QaMwIBHiguc3kqjf5OjGNKNaRI'

# Page oficial url:
page_url = 'https://reporte-semana.streamlit.app/'
scopes = [
    'https://www.googleapis.com/auth/drive.readonly',
]


# Initialize streamlit page
st.set_page_config(initial_sidebar_state='collapsed')
st.title('Compilación de informe semanal')


# Get drive authentication
client_secret = st.secrets.client_secret

if 'creds' not in st.session_state:

    col1, col2, col3 = st.columns(3)

    try:
        creds = google_tools.google_oauth_get_creds(
            client_secret, st.query_params['code'], page_url, scopes)
        st.session_state['creds'] = creds
    except KeyError:
        # if login_button:
        auth_url = google_tools.google_oauth_link(client_secret, page_url, scopes)
        # col3.link_button('Ir a Google', auth_url)
        login_button = col2.link_button('Conectar a Google Drive', auth_url)

if 'creds' not in st.session_state:
    st.markdown('### Por favor inicie sesión')
    st.stop()

drive_service = google_tools.get_drive_service(st.session_state['creds'])


# SideBar:
st.sidebar.markdown('## Parámetros adicionales')

week_report_folder_id = st.sidebar.text_input(
    'ID de la carpeta "Informe Mensual"', '1gOzvoBpXS1hzAwIE3ihJEvoBXT9lj45b')


# Main page
run_date = dt.date.today()

friday_report = run_date + dt.timedelta(-run_date.weekday())
monday_report = run_date + dt.timedelta(-7 - run_date.weekday())

report_type = st.radio('Tipo de reporte:', ['Pre', 'Post'])

if report_type == 'Pre':
    week_name = friday_report.strftime('%Y-%m-%d')
    selected_monday = friday_report
elif report_type == 'Post':
    week_name = monday_report.strftime('%Y-%m-%d')
    selected_monday = monday_report

selected_date = st.date_input('Semana',
                              selected_monday, format='DD/MM/YYYY')

google_tools.download_file(metadata_id, 'metadata.csv', drive_service)
metadata = pd.read_csv('metadata.csv')

section_folders = metadata['Sección'].unique()


report_files = []

for folder in section_folders:
    section_files_query = google_tools.list_files_from_path(
        f'{folder}/{week_name}', drive_service, week_report_folder_id)
    if section_files_query is not None:
        section_files = [f for f in section_files_query if f['mimeType']
                         == 'application/vnd.google-apps.spreadsheet']
        report_files += section_files

st.write(section_files)

for report in report_files:
    google_tools.download_file(report['id'], 'temp_report.csv', drive_service)
    data = pd.read_csv('temp_report.csv')
    data.drop('No.', inplace=True)
    st.dataframe(data)
