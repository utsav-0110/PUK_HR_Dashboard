# 🏢 Purple United Sales Limited — HR Analytics Dashboard

**Premium Enterprise-Grade HR Analytics Platform**

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the dashboard
```bash
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`

---

## ✅ Features

| Feature | Description |
|---------|-------------|
| 🎨 Premium Purple Theme | Royal Purple `#7B2FF7` with glassmorphism cards |
| 🔽 4 Dynamic Filters | Year · Month · Recruiter Name · Location |
| 📊 Live KPI Cards | Animated, glow-on-hover, auto-recalculate |
| 📈 Interactive Charts | Bar, Line, Donut, Area, Heatmap, Bubble |
| ⏱️ Live Clock | Real-time HH:MM:SS display |
| 📂 Auto Excel Integration | Drop in new Excel file → dashboard updates |
| 📥 Export Reports | Download filtered data as Excel or CSV |
| 🗺️ Heatmaps | Hiring trends by Department × Year |

## 🔽 Filters

**Only 4 filters** — all work independently and in combination:

1. **Year** — Filter by joining year (from DOJ)
2. **Month** — Filter by joining month (from DOJ)
3. **Recruiter Name** — Show only records recruited by selected person
4. **Location** — Show only records from selected city

When filters are combined, all KPIs and charts update to show **only the intersection** of selected values.

## 📂 Updating Your Data

**Just replace the Excel file** — no code changes needed:

1. Name your file `sample_hr_data.xlsx` (or any .xlsx / .csv)
2. Upload via the sidebar uploader OR replace the file in the folder
3. Dashboard auto-detects new rows, recruiters, years, months, locations

### Required Columns
| Column | Notes |
|--------|-------|
| Emp Code | Unique employee identifier |
| Employee Name | Full name |
| DOJ | Date of Joining (YYYY-MM-DD) |
| Department | Sales, HR, IT, etc. |
| Employment Status | Active / Exited / Notice Period / Hold |
| Resignation Date | If applicable |
| Exit Date | If applicable |
| New Joining | DONE / blank |
| Resign | DONE / blank |
| F&F | DONE / blank |
| PF, ESIC, PT, LWF | DONE / N/A / blank |
| S&E, Trade, Form A under POG Act | DONE / N/A / blank |
| Appointment Letter, KYC, PF Form, ESIC Form, BGV | DONE / N/A / blank |
| Location | City name |
| Profile Position | Job title |
| Recruiter Name | Recruiter who sourced the candidate |
| Profile Source | Campus / Walk-in / Indeed / etc. |

## 🎨 Theme

- **Primary:** `#7B2FF7` Royal Purple
- **Secondary:** `#A855F7` Violet  
- **Accent:** `#C084FC` Neon Purple Glow
- **Background:** `#1C1F2B`
- **Cards:** `#252938`

Built with **Python · Streamlit · Plotly**
