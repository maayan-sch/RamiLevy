import re
import json

with open("backup_tova.sql", "r", encoding="utf-8", errors="ignore") as f:
    sql_text = f.read()

tables = {}

entities = []
relationships = []

# =====================================
# RELATIONSHIP NAMES
# =====================================

relationship_names = {
    ("product", "category"): "Belongs to",
    ("employee", "store"): "Works in",
    ("store", "location"): "Positioned in",
    ("inventory", "product"): "Has",
    ("inventory", "store"): "Located in"
}

# =====================================
# CREATE TABLE
# =====================================

create_table_pattern = re.compile(
    r"CREATE TABLE public\.(\w+)\s*\((.*?)\);",
    re.DOTALL
)

for match in create_table_pattern.finditer(sql_text):

    table_name = match.group(1)
    body = match.group(2)

    attributes = []

    lines = [line.strip() for line in body.splitlines() if line.strip()]

    for line in lines:

        line = line.rstrip(",")

        # Skip constraints
        if line.startswith("CONSTRAINT"):
            continue

        parts = line.split()

        if len(parts) >= 2:

            attribute_name = parts[0]

            # =====================================
            # Extract full data type
            # =====================================

            type_parts = []

            for part in parts[1:]:

                if part.upper() in [
                    "NOT",
                    "NULL",
                    "DEFAULT",
                    "CHECK",
                    "PRIMARY",
                    "REFERENCES",
                    "UNIQUE",
                    "CONSTRAINT"
                ]:
                    break

                type_parts.append(part)

            attribute_type = " ".join(type_parts)

            attributes.append({
                "name": attribute_name,
                "type": attribute_type
            })

    tables[table_name] = {
        "attributes": attributes,
        "primary_keys": [],
        "foreign_keys": []
    }

# =====================================
# PRIMARY KEYS
# =====================================

pk_pattern = re.compile(
    r"ALTER TABLE ONLY public\.(\w+).*?PRIMARY KEY \((.*?)\);",
    re.DOTALL
)

for match in pk_pattern.finditer(sql_text):

    table_name = match.group(1)

    pk_columns = [
        col.strip()
        for col in match.group(2).split(",")
    ]

    if table_name in tables:

        tables[table_name]["primary_keys"] = pk_columns

# =====================================
# FOREIGN KEYS
# =====================================

fk_pattern = re.compile(
    r"ALTER TABLE ONLY public\.(\w+).*?"
    r"FOREIGN KEY \((.*?)\)\s+REFERENCES public\.(\w+)\((.*?)\);",
    re.DOTALL
)

for match in fk_pattern.finditer(sql_text):

    source_table = match.group(1)

    fk_column = match.group(2).strip()

    target_table = match.group(3).strip()

    target_column = match.group(4).strip()

    tables[source_table]["foreign_keys"].append({
        "column": fk_column,
        "references_table": target_table,
        "references_column": target_column
    })

# =====================================
# BUILD ERD
# =====================================

for table_name, data in tables.items():

    pk_set = set(data["primary_keys"])

    fk_set = set(
        fk["column"]
        for fk in data["foreign_keys"]
    )

    # =====================================
    # Check non FK attributes
    # =====================================

    non_fk_attributes = []

    for attr in data["attributes"]:

        if attr["name"] not in fk_set:

            non_fk_attributes.append(attr)

    # =====================================
    # MANY TO MANY RELATIONSHIP
    # =====================================

    if (
        len(data["foreign_keys"]) >= 2
        and pk_set == fk_set
        and len(non_fk_attributes) == 0
    ):

        connected_entities = []

        for fk in data["foreign_keys"]:

            connected_entities.append(
                fk["references_table"]
            )

        relationships.append({
            "relationship_name": table_name,
            "type": "many_to_many",
            "between": connected_entities
        })

    # =====================================
    # NORMAL ENTITY
    # =====================================

    else:

        # Remove FK attributes from entity
        real_attributes = []

        for attr in data["attributes"]:

            if attr["name"] not in fk_set:

                real_attributes.append(attr)

        entities.append({
            "entity_name": table_name,
            "attributes": real_attributes,
            "primary_keys": [
                pk for pk in data["primary_keys"]
                if pk not in fk_set
            ]
        })

        # =====================================
        # Create relationships
        # =====================================

        for fk in data["foreign_keys"]:

            relationship_name = relationship_names.get(
                (table_name, fk["references_table"]),
                f"{table_name}_{fk['references_table']}"
            )

            relationships.append({
                "relationship_name": relationship_name,
                "type": "one_to_many",
                "from_entity": table_name,
                "to_entity": fk["references_table"]
            })

# =====================================
# FINAL ERD STRUCTURE
# =====================================

erd = {
    "entities": entities,
    "relationships": relationships
}

# =====================================
# SAVE JSON
# =====================================

with open("erd_structure.json", "w", encoding="utf-8") as f:

    json.dump(
        erd,
        f,
        indent=4,
        ensure_ascii=False
    )

print("ERD JSON created successfully!")

