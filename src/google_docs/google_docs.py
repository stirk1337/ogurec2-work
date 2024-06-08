import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'src/google_docs/credentials.json'
SPREADSHEET_ID = '1-W3eVT3ZSxsD5ZJ35vtmX8QI-C46ItON8LtqekbDRRQ'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


def get_table() -> dict:
    values = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='A1:E10',
        majorDimension='ROWS'
    ).execute()
    return values
