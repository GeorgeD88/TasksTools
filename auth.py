import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError


# token.json file needs to be deletd everytime scopes are modified
SCOPES = [
    'https://www.googleapis.com/auth/tasks',
    'https://www.googleapis.com/auth/tasks.readonly'
    ]


def auth():
    """ Authentication for the Google Tasks API pulled from Google's quickstart.py """

    """ NOTE: token.json stores the user's access and refresh tokens
    and is created automatically when the authorization flow completes
    for the first time. The tokens are saved for all other uses. """

    creds = None

    # loads token file if it already exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available (token file doesn't exist),
    # lets the user log in to renew the credentials.
    if not creds or not creds.valid:
        # if token is just expired, refresh it
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # if no tokens at all, open consent screen
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds
