import os

path = os.path.join(os.path.dirname(__file__), "app.py")
content = open(path, encoding='utf-8').read()

page_keys = [
    'dash_year', 'dash_month', 'dash_rec', 'dash_loc', 'dash_dept',
    'rec_year', 'rec_month', 'rec_loc', 'rec_recruiter',
    'doc_year', 'doc_month', 'doc_dept',
    'pay_year', 'pay_month', 'pay_emp', 'pay_ff',
    'comp_year', 'comp_month', 'comp_dept',
    'lab_state', 'lab_city',
    'hris_year', 'hris_month', 'hris_dept', 'hris_loc',
    'pc_year', 'pc_month', 'pc_dept', 'pc_loc',
]

lines = content.split('\n')
count = 0
for i in range(len(lines)):
    for pk in page_keys:
        if ('key="' + pk + '"') in lines[i] and 'st.selectbox(' in lines[i]:
            lines[i] = lines[i].replace('st.selectbox(', 'persistent_selectbox(', 1)
            count += 1
            break

with open(path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"Done. Replaced {count} selectboxes.")
