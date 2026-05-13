
import re
import json

with open("backup_tova.sql", "r", encoding="utf-8", errors="ignore") as f:
    sql_text = f.read()

tables = {}

create_table_pattern = re.compile(
    r"CREATE TABLE public\.(\w+)\s*\((.*?)\);",
    re.DOTALL
)

for match in create_table_pattern.finditer(sql_text):
    table_name = match.group(1)
    body = match.group(2)

    columns = []
    primary_keys = []
    foreign_keys = []

    lines = [line.strip() for line in body.splitlines() if line.strip()]

    for line in lines:
        line = line.rstrip(",")

        if line.startswith("CONSTRAINT") and "PRIMARY KEY" in line:
            pk_match = re.search(r"PRIMARY KEY \((.*?)\)", line)
            if pk_match:
                primary_keys = [x.strip() for x in pk_match.group(1).split(",")]

        elif line.startswith("CONSTRAINT") and "FOREIGN KEY" in line:
            fk_match = re.search(
                r"FOREIGN KEY \((.*?)\)\s+REFERENCES public\.(\w+)\((.*?)\)",
                line
            )

            if fk_match:
                foreign_keys.append({
                    "column": fk_match.group(1).strip(),
                    "references_table": fk_match.group(2).strip(),
                    "references_column": fk_match.group(3).strip()
                })

        elif not line.startswith("CONSTRAINT"):
            parts = line.split()
            if len(parts) >= 2:
                columns.append({
                    "name": parts[0],
                    "type": parts[1]
                })

    tables[table_name] = {
        "columns": columns,
        "primary_keys": primary_keys,
        "foreign_keys": foreign_keys
    }

with open("erd_structure.json", "w", encoding="utf-8") as f:
    json.dump(tables, f, indent=4, ensure_ascii=False)

print("ERD JSON created successfully!")
