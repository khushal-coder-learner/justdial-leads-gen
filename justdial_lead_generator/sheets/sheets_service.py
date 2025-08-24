import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetWriter:
    def __init__(self, creds_path:str, sheet_name:str):
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive.file",
                 "https://www.googleapis.com/auth/drive"]
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(sheet_name).sheet1

    def append_row(self,data: list):
        self.sheet.append_row(data)

    def append_rows(self, rows: list):
        self.sheet.append_rows(rows, value_input_option = 'RAW')