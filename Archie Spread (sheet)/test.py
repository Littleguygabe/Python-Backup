
import gspread
from google.oauth2.service_account import Credentials

scopes = [
    'https://www.googleapis.com/auth/spreadsheets'
]

creds = Credentials.from_service_account_file('credentials.json',scopes=scopes)
client = gspread.authorize(creds)

sheet_id = '1LZyDovz3UvO99BcPWJWUP-06KgynzjacJmqFA1DfYmo'
sheet = client.open_by_key(sheet_id)

mainSheet = sheet.sheet1
data_list = [
    ["John", "A software engineer", 42, 15, "yes", "no", "17-11-2023"],
    ["Alice", "An artist", 76, 8, "no", "yes", "03-10-2023"],
    ["Bob", "A plumber", 65, 12, "yes", "yes", "28-11-2023"],
    ["Emily", "A teacher", 30, 17, "yes", "no", "14-09-2023"],
    ["Michael", "A doctor", 88, 10, "no", "yes", "22-10-2023"]
]


mainSheet.update(data_list,'A3:G8')