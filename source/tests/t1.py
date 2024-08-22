# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
#
# # Prompt the user to log in and grant access
# creds = Credentials.from_authorized_user_info(info=user_info)
#
# # Create a Google Drive API client
# drive_service = build('drive', 'v3', credentials=creds)
#
# # Use the drive_service to interact with the Google Drive API
# # For example, to list the user's files:
# files = drive_service.files().list().execute()
# for file in files.get('files', []):
#     print(f"Found file: {file['name']}")

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import os
import io
import json

# Set the scopes for the API you want to access
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def get_authenticated_credentials():
    """
    Prompts the user to log in and grant access to the application.
    Returns the user's OAuth 2.0 credentials.
    """
    creds = None

    # # Try to load existing credentials from a file
    # try:
    #     creds = Credentials.from_authorized_user_info(info=None, file_name='token.json')
    # except FileNotFoundError:
    #     pass

    # Try to load existing credentials from a file
    token_file = 'token.json'
    if os.path.exists(token_file):
        with open(token_file, 'r') as token:
            creds = Credentials.from_authorized_user_info(info=json.load(token))

    # If no credentials are available, start the OAuth 2.0 flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e1:
                try:
                    os.remove('token.json')
                    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e2:
                    raise Exception(
                        f'The following error ocour:\n    {e1}\n' +
                        f'So removing the token was intended but it gives the error:\n    {e2}')

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def find_file_by_path(path):
    """
    Find a file in Google Drive by its POSIX-like path.
    """
    parts = path.split('/')
    current_folder_id = 'root'
    for part in parts[:-1]:
        files = list_files(current_folder_id, part)
        if not files:
            return None
        current_folder_id = files[0]['id']

    filename = parts[-1]
    files = list_files(current_folder_id, filename)
    if files:
        return files[0]
    else:
        return None


def list_files(parent_id, name=None):
    """
    List files in the specified Google Drive folder.
    If name is provided, it will filter the results by filename.
    """
    query = "trashed = false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    if name:
        query += f" and name = '{name}'"

    results = drive_service.files().list(
        pageSize=100,
        fields="nextPageToken, files(id, name, mimeType, parents)",
        q=query
    ).execute()

    return results.get('files', [])


def download_file(file_id, local_path):
    """
    Download a file from Google Drive to the specified local path.
    """
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    with open(local_path, 'wb') as f:
        f.write(fh.getvalue())


# Example usage
creds = get_authenticated_credentials()
print(f'\n{creds.to_json()}')

# Try to make a sample API request
drive_service = build('drive', 'v3', credentials=creds)
files = drive_service.files().list().execute()
print(f"\nFound {len(files.get('files', []))} files in your Google Drive.")
print(files.get('files', []))
