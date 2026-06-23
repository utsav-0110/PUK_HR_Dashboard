"""
PUK HR Dashboard — Excel Converter
====================================
Usage:
    python convert_to_dashboard.py <input.xlsx>  [output.xlsx]

    If output path is omitted, the output is saved as:
        sample_hr_data.xlsx   (in the same folder as this script)
    so the dashboard picks it up automatically on the next launch.

What this script does
---------------------
1. Reads the HR Master Excel (any sheet named 'Employee_Master_Data' or the first sheet).
2. Fixes dates stored as Excel serial numbers → proper Python date strings.
3. Normalises Employment Status values (Active / Exited / Notice Period / Hold).
4. Normalises DONE/Done/done → "DONE", blank stays blank.
5. Ensures all required columns exist (adds empty ones if missing).
6. Writes a clean .xlsx that the dashboard reads without any manual edits.

Just edit your original template and run this script — you never have to
come to the codebase again.
"""

import sys
import os
import pandas as pd
from datetime import datetime, timedelta


# ── Column definitions (must match app.py constants) ─────────────────────────
REQUIRED_COLUMNS = [
    "Emp Code",
    "Employee Name",
    "DOJ",
    "Exit Date",
    "Employment Status",
    "Department",
    "Gender",
    "New Joining",
    "Resign",
    "F&F",
    "PF",
    "ESIC",
    "PT",
    "LWF",
    "S&E",
    "Trade",
    "Form A under POG Act",
    "Appointment Letter",
    "KYC (PAN+Aadhar+Bank)",
    "PF Form",
    "ESIC Form",
    "Location",
    "Profile Position",
    "Recruiter Name",
    "Profile Source",
    "Remarks",
    # Optional: Resignation Date (used in Payroll page)
]

# Accepted values for Employment Status
STATUS_MAP = {
    "active":        "Active",
    "exited":        "Exited",
    "exit":          "Exited",
    "resigned":      "Exited",
    "notice period": "Notice Period",
    "notice":        "Notice Period",
    "on notice":     "Notice Period",
    "hold":          "Hold",
    "on hold":       "Hold",
}

DONE_COLS = [
    "New Joining", "Resign", "F&F",
    "PF", "ESIC", "PT", "LWF",
    "S&E", "Trade", "Form A under POG Act",
    "Appointment Letter", "KYC (PAN+Aadhar+Bank)", "PF Form", "ESIC Form", "BGV",
]

DATE_COLS = ["DOJ", "Exit Date", "Resignation Date"]

# Excel epoch (Windows): Jan 1, 1900 (with 1900 leap-year bug adjustment)
EXCEL_EPOCH = datetime(1899, 12, 30)


def excel_serial_to_date(val):
    """Convert an Excel date serial number to a pandas Timestamp."""
    try:
        n = float(val)
        if n > 59:  # skip the fake 1900-02-29 Excel bug
            n -= 1
        return EXCEL_EPOCH + timedelta(days=n)
    except (ValueError, TypeError):
        return pd.NaT


def fix_dates(series: pd.Series) -> pd.Series:
    """Parse dates — handles already-parsed Timestamps, serial numbers, and strings."""
    # If already datetime, just return as-is
    if pd.api.types.is_datetime64_any_dtype(series):
        return series
    # Try standard parsing first (handles most string formats)
    result = pd.to_datetime(series, errors="coerce", dayfirst=False)
    # For remaining NaT, try dayfirst=True (DD/MM/YYYY)
    mask = result.isna() & series.notna() & (series.astype(str).str.strip() != "") & (series.astype(str) != "nan")
    if mask.any():
        result[mask] = pd.to_datetime(series[mask], errors="coerce", dayfirst=True)
    # For still-remaining NaT, try Excel serial number
    mask2 = result.isna() & series.notna() & (series.astype(str).str.strip() != "") & (series.astype(str) != "nan")
    if mask2.any():
        result[mask2] = series[mask2].apply(excel_serial_to_date)
    return result


def normalise_done(series: pd.Series) -> pd.Series:
    """Normalise Done/DONE/done → DONE; blank → blank; N/A → N/A."""
    s = series.astype(str).str.strip()
    s = s.replace("nan", "")
    done_mask = s.str.upper() == "DONE"
    na_mask   = s.str.upper() == "N/A"
    out = s.copy()
    out[done_mask] = "DONE"
    out[na_mask]   = "N/A"
    out[~done_mask & ~na_mask] = ""
    return out


def normalise_status(series: pd.Series) -> pd.Series:
    """Normalise Employment Status to one of 4 canonical values."""
    def _map(val):
        if pd.isna(val) or str(val).strip() == "":
            return "Active"          # default if blank
        key = str(val).strip().lower()
        return STATUS_MAP.get(key, str(val).strip().title())
    return series.apply(_map)


def convert(input_path: str, output_path: str):
    print(f"\n📂  Reading:  {input_path}")

    # ── Load ──────────────────────────────────────────────────────────────────
    xl = pd.ExcelFile(input_path)
    sheet = "Employee_Master_Data" if "Employee_Master_Data" in xl.sheet_names else xl.sheet_names[0]
    print(f"    Sheet used: '{sheet}'")
    df = xl.parse(sheet)  # let pandas parse dates natively

    original_cols = list(df.columns)
    print(f"    Rows loaded: {len(df)}")
    print(f"    Columns found: {len(original_cols)}")

    # ── Normalise column names (strip whitespace) ─────────────────────────────
    df.columns = [c.strip() for c in df.columns]

    # ── Fill missing required columns ──────────────────────────────────────────
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = ""
            print(f"    ⚠️  Added missing column: '{col}'")

    # ── Fix dates ─────────────────────────────────────────────────────────────
    for col in DATE_COLS:
        if col in df.columns:
            df[col] = fix_dates(df[col])
            valid = df[col].notna().sum()
            print(f"    📅  {col}: {valid} valid dates")

    # ── Normalise DONE columns ────────────────────────────────────────────────
    for col in DONE_COLS:
        if col in df.columns:
            df[col] = normalise_done(df[col])

    # ── Normalise Employment Status ───────────────────────────────────────────
    if "Employment Status" in df.columns:
        df["Employment Status"] = normalise_status(df["Employment Status"])
        print(f"    📊  Status distribution:\n{df['Employment Status'].value_counts().to_string()}")

    # ── Normalise Gender ──────────────────────────────────────────────────────
    if "Gender" in df.columns:
        df["Gender"] = df["Gender"].astype(str).str.strip().str.title().replace("Nan", "")
        print(f"    ⚧  Gender distribution:\n{df['Gender'].value_counts().to_string()}")

    # ── Clean string columns ───────────────────────────────────────────────────
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].fillna("").astype(str).str.strip()
            df[col] = df[col].replace("nan", "").replace("NaT", "")

    # ── Write output ──────────────────────────────────────────────────────────
    print(f"\n💾  Writing: {output_path}")
    with pd.ExcelWriter(output_path, engine="openpyxl", datetime_format="YYYY-MM-DD") as writer:
        df.to_excel(writer, index=False, sheet_name="Employee_Master_Data")

    print(f"✅  Done!  {len(df)} rows written to '{output_path}'")
    print("\n📌  Next steps:")
    print("    1. If the output is named 'sample_hr_data.xlsx' in the app folder,")
    print("       the dashboard loads it automatically on startup.")
    print("    2. Or upload it via the 'Upload Excel / CSV' panel in the sidebar.\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"❌  File not found: {input_file}")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = sys.argv[2] if len(sys.argv) >= 3 else os.path.join(script_dir, "sample_hr_data.xlsx")

    convert(input_file, output_file)
