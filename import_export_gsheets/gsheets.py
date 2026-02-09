# Copyright (c) 2026 Brian Nettleton
# SPDX-License-Identifier: MIT

from django.conf import settings
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from allauth.socialaccount.models import SocialToken
from .utils import SheetRef

def get_google_creds(request):
    token = SocialToken.objects.get(
        account__user=request.user,
        account__provider="google"
    )
    provider = settings.SOCIALACCOUNT_PROVIDERS["google"]
    app = provider.get("APP", {})
    return Credentials(
        token=token.token,
        refresh_token=token.token_secret,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=app.get("client_id"),
        client_secret=app.get("secret"),
        scopes=provider.get("SCOPE", []),
    )

def create_spreadsheet(service, title):
    sheet = service.spreadsheets().create(
        body={"properties": {"title": title or "Django Export"}}
    ).execute()
    return sheet["spreadsheetId"]

def ensure_sheet_tab(service, spreadsheet_id, sheet_title):
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    for s in meta["sheets"]:
        if s["properties"]["title"] == sheet_title:
            return sheet_title

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": [{
            "addSheet": {"properties": {"title": sheet_title}}
        }]}
    ).execute()
    return sheet_title

def read_sheet(creds, spreadsheet_id, sheet_title):
    service = build("sheets", "v4", credentials=creds, cache_discovery=False)
    resp = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_title}'",
        valueRenderOption="UNFORMATTED_VALUE",
    ).execute()
    return resp.get("values", [])

def write_sheet(creds, spreadsheet_id, sheet_title, values):
    service = build("sheets", "v4", credentials=creds, cache_discovery=False)
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_title}'!A1",
        valueInputOption="RAW",
        body={"values": values},
    ).execute()
