# Copyright (c) 2026 Brian Nettleton
# SPDX-License-Identifier: MIT

import re
from dataclasses import dataclass
from typing import Optional

_SHEET_RE = re.compile(r"/spreadsheets/d/([a-zA-Z0-9-_]+)")
_GID_RE = re.compile(r"(?:[#&?]gid=)(\d+)")

@dataclass(frozen=True)
class SheetRef:
    spreadsheet_id: str
    gid: Optional[int] = None

def parse_sheet_url(url: str) -> SheetRef:
    m = _SHEET_RE.search(url or "")
    if not m:
        raise ValueError("Invalid Google Sheet URL")
    spreadsheet_id = m.group(1)
    gid_m = _GID_RE.search(url or "")
    gid = int(gid_m.group(1)) if gid_m else None
    return SheetRef(spreadsheet_id, gid)
