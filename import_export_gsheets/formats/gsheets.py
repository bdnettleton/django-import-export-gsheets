# Copyright (c) 2026 Brian Nettleton
# SPDX-License-Identifier: MIT

import tablib
from import_export.formats.base_formats import Format
from import_export_gsheets.utils import parse_sheet_url
from import_export_gsheets.gsheets import (
    get_google_creds,
    read_sheet,
    write_sheet,
    create_spreadsheet,
    ensure_sheet_tab,
)

class GoogleSheetsFormat(Format):
    def get_title(self):
        return "Google Sheets"

    def get_extension(self):
        return "gsheets"

    def can_import(self):
        return True

    def can_export(self):
        return True

    def is_binary(self):
        return False

    def create_dataset(self, in_stream=None, **kwargs):
        request = kwargs["request"]
        sheet_url = kwargs["gsheets_url"]
        tab = kwargs.get("gsheets_tab")

        creds = get_google_creds(request)
        ref = parse_sheet_url(sheet_url)

        if not tab:
            tab = "Sheet1"

        values = read_sheet(creds, ref.spreadsheet_id, tab)
        dataset = tablib.Dataset()
        if not values:
            return dataset
        dataset.headers = values[0]
        for row in values[1:]:
            dataset.append(row)
        return dataset

    def export_data(self, dataset, **kwargs):
        request = kwargs["request"]
        tab = kwargs.get("gsheets_tab") or "export"

        creds = get_google_creds(request)

        if kwargs.get("create_new_spreadsheet"):
            service = build("sheets", "v4", credentials=creds, cache_discovery=False)
            spreadsheet_id = create_spreadsheet(
                service,
                kwargs.get("new_spreadsheet_title"),
            )
        else:
            ref = parse_sheet_url(kwargs["gsheets_url"])
            spreadsheet_id = ref.spreadsheet_id
            service = build("sheets", "v4", credentials=creds, cache_discovery=False)

        ensure_sheet_tab(service, spreadsheet_id, tab)

        values = [dataset.headers] + list(dataset)
        write_sheet(creds, spreadsheet_id, tab, values)
        return ""
