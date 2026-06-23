import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

today = datetime.today()

departments = ["Sales", "HR", "Finance", "Operations", "IT", "Marketing", "Legal", "Admin"]
statuses = ["Active", "Active", "Active", "Active", "Exited", "Notice Period", "Hold"]
positions = ["Sales Executive", "HR Executive", "Accountant", "Operations Manager",
             "Software Developer", "Marketing Manager", "Legal Advisor", "Admin Officer"]
locations = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Pune"]
recruiters = ["Priya Sharma", "Amit Verma", "Sunita Rao", "Rahul Gupta", "Neha Singh"]
sources = ["Naukri", "LinkedIn", "Referral", "Campus", "Walk-in", "Indeed"]

done_blank = lambda p: random.choices(["DONE", ""], weights=[p, 1-p])[0]
done_blank_na = lambda p: random.choices(["DONE", "", "N/A"], weights=[p*0.8, (1-p)*0.7, 0.15])[0]

n = 150
rows = []
for i in range(n):
    doj = today - timedelta(days=random.randint(10, 1800))
    status = random.choice(statuses)
    resign_date = doj + timedelta(days=random.randint(300, 1500)) if status in ["Exited", "Notice Period"] else ""
    exit_date = resign_date + timedelta(days=60) if status == "Exited" and resign_date else ""

    rows.append({
        "Emp Code": f"PUK{1000+i}",
        "Employee Name": f"Employee {i+1}",
        "DOJ": doj.strftime("%Y-%m-%d"),
        "Department": random.choice(departments),
        "Employment Status": status,
        "Resignation Date": resign_date.strftime("%Y-%m-%d") if resign_date else "",
        "Exit Date": exit_date.strftime("%Y-%m-%d") if exit_date else "",
        # Payroll
        "New Joining": done_blank(0.88),
        "Resign": "DONE" if status in ["Exited", "Notice Period"] else "",
        "F&F": done_blank(0.60) if status == "Exited" else "",
        # Compliance
        "PF": done_blank_na(0.85),
        "ESIC": done_blank_na(0.80),
        "PT": done_blank_na(0.78),
        "LWF": done_blank_na(0.75),
        # Labour Compliance
        "S&E": done_blank_na(0.82),
        "Trade": done_blank_na(0.77),
        "Form A under POG Act": done_blank_na(0.70),
        # Documentation
        "Appointment Letter": done_blank(0.90),
        "KYC (PAN+Aadhar+Bank)": done_blank(0.84),
        "PF Form": done_blank(0.80),
        "ESIC Form": done_blank(0.78),
        "BGV": done_blank_na(0.72),
        # Recruitment
        "Location": random.choice(locations),
        "Profile Position": random.choice(positions),
        "Recruiter Name": random.choice(recruiters),
        "Profile Source": random.choice(sources),
        "Remarks": random.choice(["", "", "", "Follow up needed", "Documents pending", "Verified"]),
    })

df = pd.DataFrame(rows)
df.to_excel("sample_hr_data.xlsx", index=False)
df.to_csv("sample_hr_data.csv", index=False)
print(f"Generated {n} rows.")
print(df.head(3).to_string())
