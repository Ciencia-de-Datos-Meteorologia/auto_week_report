# import os
import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
import google_tools
# from google.oauth2.credentials import Credentials

# Load the client secret from the Streamlit Cloud secret
# client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
client_secret = st.secrets.client_secret

# st.text(client_secret)
#
#
# def google_oauth_login(client_secret):
#     # Set up the OAuth flow
#     flow = InstalledAppFlow.from_client_config(
#         client_secret,
#         scopes=['https://www.googleapis.com/auth/drive.readonly'],
#         redirect_uri='http://localhost:8501/'
#     )
#
#     # Start the OAuth login flow
#     authorization_url, state = flow.authorization_url(
#         access_type='offline',
#         include_granted_scopes='true')
#
#     # Redirect the user to the authorization URL
#     # st.markdown(f"[Click here to login with Google]({authorization_url})")
#
#     try:
#         flow.fetch_token(code=st.query_params['code'])
#         creds = flow.credentials
#     except Exception:
#         creds = None
#         # st.button('Google login', authorization_url)
#     # st.write(creds)
#     return authorization_url, creds
#
#
# # login_button = st.button()
# #
# # if login_button
#
# url, creds = google_oauth_login()
# st.link_button('DriveLink', url)
#
# # # Handle the OAuth callback
# # if 'code' in st.query_params:
# #     st.text(st.query_params)
# #     code = st.query_params['code']
# #     flow = InstalledAppFlow.from_client_config(
# #         client_secret,
# #         scopes=['https://www.googleapis.com/auth/drive.readonly'],
# #         redirect_uri='http://localhost:8501/'
# #     )
# #     flow.fetch_token(code=code)
# #     creds = flow.credentials
# #     # st.write(creds)
# #     st.write("Login successful!")
# #     # You can now use the creds to interact with the Google Drive API
# #
#
# st.text(st.query_params)

try:
    auth_url, creds = google_tools.google_oauth_login(client_secret, st.query_params['code'])
except KeyError:
    auth_url, creds = google_tools.google_oauth_login(client_secret)

if creds is None:
    st.link_button('DriveLink', auth_url)
else:
    st.button('DriveLink', disabled=True)
