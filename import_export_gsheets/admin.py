# Copyright (c) 2026 Brian Nettleton
# SPDX-License-Identifier: MIT

from import_export.admin import ImportExportModelAdmin
from .forms import GoogleSheetsImportForm, GoogleSheetsExportForm
from .formats.gsheets import GoogleSheetsFormat

class GoogleSheetsImportExportModelAdmin(ImportExportModelAdmin):
    import_form_class = GoogleSheetsImportForm
    export_form_class = GoogleSheetsExportForm

    def get_import_formats(self):
        return [GoogleSheetsFormat()] + super().get_import_formats()

    def get_export_formats(self):
        return [GoogleSheetsFormat()] + super().get_export_formats()

    def get_import_data_kwargs(self, request, form=None, **kwargs):
        data = super().get_import_data_kwargs(request, form, **kwargs)
        if form:
            data.update({
                "request": request,
                "gsheets_url": form.cleaned_data.get("gsheets_url"),
                "gsheets_tab": form.cleaned_data.get("gsheets_tab"),
            })
        return data

    def get_export_data_kwargs(self, request, form=None, **kwargs):
        data = super().get_export_data_kwargs(request, form, **kwargs)
        if form:
            data.update({
                "request": request,
                "gsheets_url": form.cleaned_data.get("gsheets_url"),
                "create_new_spreadsheet": form.cleaned_data.get("create_new_spreadsheet"),
                "new_spreadsheet_title": form.cleaned_data.get("new_spreadsheet_title"),
                "gsheets_tab": form.cleaned_data.get("gsheets_tab"),
            })
        return data
