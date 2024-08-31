from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

import re
import os

load_dotenv()

app = FastAPI()
credentials = service_account.Credentials.from_service_account_file('key.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=credentials)
spreadsheet_id = os.getenv('SPREADSHEET_ID')
sheet_name = 'Sheet1'

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/subscribe")
async def submit(request: Request):
    form_data = await request.form()
    print(form_data)
    email = form_data['email']
    userType = form_data['userType']
    if email == "":
        return "Please enter an email address"
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return "Please enter a valid email address"
    if userType == "":
        return "Please select a user type"
    
    values = [[email, userType]]

    try:
        # Append the data to the Google Sheet
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A1",
            valueInputOption="USER_ENTERED",
            body={"values": values}
        ).execute()

        return "thank you for subscribing!"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "something went wrong while adding data into the spreadsheet. can you help us by contacting our x account?"