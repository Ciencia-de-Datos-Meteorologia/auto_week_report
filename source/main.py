import streamlit as st
import google_tools
import datetime as dt
import pandas as pd
import locale
import subprocess

# Set the locale to Spanish (Spain)
locale.setlocale(locale.LC_TIME, 'es_MX')
# result = subprocess.run(['locale', '-a'], stdout=subprocess.PIPE,
# stderr=subprocess.PIPE, universal_newlines=True)
# st.write(result.stdout)

metadata_id = '1LcFZ3YqS8TcgA6zl5QaMwIBHiguc3kqjf5OjGNKNaRI'

pre_columns = ['Actividad', 'Objeto', 'Lugar donde se realizó',
               'Actores participantes', 'Resultados Esperados']
post_columns = ['Actividad', 'Objeto', 'Lugar donde se realizó',
                'Actores participantes', 'Resultados', 'Medio de verificación']

pre_column_format = '|c|CCCCC|'
post_column_format = '|c|DDDDDD|'

# List with users that might have errors or mistakes
pending_users = []
warning_users = []

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
    # week_name = friday_report.strftime('%Y-%m-%d')
    selected_monday = friday_report
    report_columns = pre_columns
    report_type_n = 0
    column_format = pre_column_format
    report_title = 'Informe de planificación semanal'
elif report_type == 'Post':
    # week_name = monday_report.strftime('%Y-%m-%d')
    selected_monday = monday_report
    report_columns = post_columns
    report_type_n = 1
    column_format = post_column_format
    report_title = 'Informe de resultados semanales'

selected_date = st.date_input('Semana',
                              selected_monday, format='DD/MM/YYYY')

report_date = selected_date.strftime('Semana del %d de %B')

st.markdown(f'## {report_title} '+report_date.replace('Semana del', '-'))

google_tools.download_file(metadata_id, 'metadata.csv', drive_service, 'csv')
metadata = pd.read_csv('metadata.csv')

section_folders = metadata['Sección'].unique()


report_files = []

for folder in section_folders:
    section_files_query = google_tools.list_files_from_path(
        f'{folder}/{selected_date.strftime("%Y-%m-%d")}', drive_service, week_report_folder_id)
    if section_files_query is not None:
        section_files = [f for f in section_files_query if f['mimeType']
                         == 'application/vnd.google-apps.spreadsheet']
        report_files += section_files

st.write(report_files)

with open('source/Plantilla_documento/main.template.tex', 'r') as tex_main:
    tex_main_str = tex_main.read()

tex_main_str = tex_main_str.replace('...title...', report_title)
tex_main_str = tex_main_str.replace('...date...', report_date)

with open('source/Plantilla_documento/content.template.tex', 'r') as tex_content:
    tex_content_str = tex_content.read()

for report in report_files:
    id_name = report['name']
    try:
        full_name = metadata[metadata['Usuario'] == id_name]['Nombre'].values[0]
    except Exception as e:
        full_name = id_name
        # st.write(e)
        st.toast(f'Usuario no encontrado: `{id_name}`')
    # st.markdown(f'### {report["name"]}')
    st.markdown(f'- **{full_name}**')
    google_tools.download_file(report['id'], 'temp_report.xlsx', drive_service, 'xlsx')
    try:
        data = pd.read_excel('temp_report.xlsx', sheet_name=report_type, dtype=str)
    except ValueError:
        # st.write(type(e), e)
        data = pd.read_excel('temp_report.xlsx', sheet_name=report_type_n, dtype=str)
        # warning_users.append(id_name)
        st.toast(f'Hojas con nombre incorrecto: `{id_name}`')

    try:
        data = data[report_columns]
    except Exception:
        # warning_users.append(id_name)
        data = data.iloc[:, :len(report_columns)]
        st.toast(f'Columnas con nombre incorrecto: `{id_name}`')

    data.dropna(thresh=2, inplace=True)

    if data.empty:
        continue

    data.index = data.index + 1
    data.columns.name = 'No.'
    data.columns = report_columns

    # st.dataframe(data)

    for column in data.columns:
        data[column] = data[column].str.replace('&', '\\&')
        data[column] = data[column].str.replace('\\\\&', '\\&')
        data[column] = data[column].str.replace('_', '\\_')
        data[column] = data[column].str.replace('\\\\_', '\\_')

    latex_report = data.to_latex(column_format=column_format)

    original_header = 'No.'
    for column_name in report_columns:
        original_header += f' & {column_name}'

    new_header = '\\rowcolor{darkBlue}\n\\headerrow No.'
    for column_name in report_columns:
        new_header += f' & \\headerrow {column_name}'

    # original_header = 'No. & Actividad & Objeto ' +\
    #     '& Lugar donde se realizó & Actores participantes ' +\
    #     '& Resultados Esperados'
    # new_header = '\\rowcolor{darkBlue}\n\\headerrow No. & ' +\
    #     '\\headerrow Actividad & \\headerrow Objeto & ' +\
    #     '\\headerrow Lugar donde se realizó & ' +\
    #     '\\headerrow Actores participantes & ' +\
    #     '\\headerrow Resultados esperados'

    latex_report = latex_report.replace('\\begin{tabular}', '\\begin{longtable}')
    latex_report = latex_report.replace('\\end{tabular}', '\\end{longtable}')
    latex_report = latex_report.replace('\\\\', '\\tabularnewline\\hline')
    latex_report = latex_report.replace('\\toprule', '\\hline')
    latex_report = latex_report.replace('\\bottomrule', '')
    latex_report = latex_report.replace('\\midrule', '')
    latex_report = latex_report.replace(original_header, new_header)

    # st.markdown(f'```latex\n{latex_report}\n```')

    tex_content_str += f'\n\\section*{{{full_name}}}\n\n{latex_report}\n\n'


st.write(warning_users)

# tex_main = open('source/Plantilla_documento/main.tex','r')
# tex_content = open('source/Plantilla_documento/content.tex','r')
#
# tex_main_str = tex
#
# tex_main.close()
# tex_content.close()

with open('source/Plantilla_documento/main.tex', 'w') as tex_main:
    tex_main.write(tex_main_str)

with open('source/Plantilla_documento/content.tex', 'w') as tex_content:
    tex_content.write(tex_content_str)


st.markdown(f'```latex\n{tex_main_str}\n```')
st.markdown(f'```latex\n{tex_content_str}\n```')

# st.text('Pre compile')
latex_compile = 'pdflatex -output-directory=tex_out main.tex'
latex_exe = subprocess.run(latex_compile.split(' '), cwd='source/Plantilla_documento/')
# stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# st.write(latex_exe.stdout)
# st.text('Post compile')

with open('source/Plantilla_documento/tex_out/main.pdf', 'rb') as pdf_out:
    pdf_out_bins = pdf_out.read()

# st.text('Post read')

st.download_button('compilado.pdf', pdf_out_bins, 'compilado.pdf')

# st.download_button('main.tex', tex_main_str, 'main.tex', 'text/tex')
# st.download_button('content.tex', tex_content_str, 'content.tex', 'text/tex')
