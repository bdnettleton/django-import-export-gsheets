# Copyright (c) 2026 Brian Nettleton
# SPDX-License-Identifier: MIT

from django import forms
from import_export.forms import ImportForm, ExportForm

class GoogleSheetsMixin(forms.Form):
    gsheets_url = forms.URLField(
        required=False,
        label="Google Sheet URL",
        help_text="Leave blank to create a new spreadsheet",
    )
    create_new_spreadsheet = forms.BooleanField(
        required=False,
        label="Create new spreadsheet",
        initial=False,
    )
    new_spreadsheet_title = forms.CharField(
        required=False,
        label="New spreadsheet title",
    )
    gsheets_tab = forms.CharField(
        required=False,
        label="Sheet tab name",
        help_text="Optional. Will be created if missing.",
    )

class GoogleSheetsImportForm(GoogleSheetsMixin, ImportForm):
    pass

class GoogleSheetsExportForm(GoogleSheetsMixin, ExportForm):
    pass
