import json, os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from .database import COLUMNS

def sync(rows):
    raw, sheet_id = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"), os.getenv("GOOGLE_SHEET_ID")
    if not raw or not sheet_id: return False
    info = json.loads(raw)
    creds = Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    svc = build("sheets", "v4", credentials=creds, cache_discovery=False)
    values = [COLUMNS] + [[r[c] for c in COLUMNS] for r in rows]
    svc.spreadsheets().values().clear(spreadsheetId=sheet_id, range="Internships!A:K").execute()
    svc.spreadsheets().values().update(spreadsheetId=sheet_id, range="Internships!A1", valueInputOption="RAW", body={"values":values}).execute()
    try:
        meta=svc.spreadsheets().get(spreadsheetId=sheet_id).execute(); sh=next((s for s in meta['sheets'] if s['properties']['title']=='Internships'),None)
        if sh:
            sid=sh['properties']['sheetId']; svc.spreadsheets().batchUpdate(spreadsheetId=sheet_id,body={"requests":[{"setBasicFilter":{"filter":{"range":{"sheetId":sid,"startRowIndex":0,"endRowIndex":max(1,len(values)),"startColumnIndex":0,"endColumnIndex":11}}}},{"updateSheetProperties":{"properties":{"sheetId":sid,"gridProperties":{"frozenRowCount":1}},"fields":"gridProperties.frozenRowCount"}}]}).execute()
    except Exception: pass
    return True
