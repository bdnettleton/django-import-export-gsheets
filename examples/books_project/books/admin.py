from django.contrib import admin
from import_export_gsheets.admin import GoogleSheetsImportExportModelAdmin
from .models import Book

@admin.register(Book)
class BookAdmin(GoogleSheetsImportExportModelAdmin):
    pass
