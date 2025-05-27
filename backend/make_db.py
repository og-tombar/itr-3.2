#!/usr/bin/env python3
"""
Read questions.json ➜ create trivia.db ➜ populate it
Schema matches the JSON structure exactly, with an added auto-increment ID.
Std-lib only: json, sqlite3, pathlib.
"""

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

JSON_PATH = Path("./questions.json")
DB_PATH = Path("questions.db")

# ---------- 1. read the JSON ----------
records: List[Dict[str, Any]] = json.loads(
    JSON_PATH.read_text(encoding="utf-8"))
if not records:
    raise ValueError("JSON is empty!")

# ---------- 2. infer schema from first record ----------
# Get all keys from the first record - this will be our column list
cols = list(records[0].keys())

# Verify all records have the same structure
for i, record in enumerate(records):
    if set(record.keys()) != set(cols):
        raise ValueError(
            f"Record {i} has different keys than the first record")

# ---------- 3. build CREATE TABLE SQL ----------


def col_sql(name: str) -> str:
    if name == "correct_index":
        return f"{name} INTEGER NOT NULL"
    elif name == "difficulty":
        return f"{name} INTEGER NOT NULL"
    else:
        return f"{name} TEXT NOT NULL"


create_sql = (
    "CREATE TABLE IF NOT EXISTS questions (\n"
    "  id INTEGER PRIMARY KEY AUTOINCREMENT,\n  "
    + ",\n  ".join(col_sql(c) for c in cols)
    + "\n);"
)

# ---------- 4. open DB, create table ----------
with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    cur.execute(create_sql)

    # ---------- 5. insert ----------
    placeholders = ", ".join("?" for _ in cols)
    insert_sql = f"INSERT INTO questions ({', '.join(cols)}) VALUES ({placeholders})"

    values = []
    for record in records:
        # Extract values in the same order as cols
        row = [record[col] for col in cols]
        values.append(row)

    cur.executemany(insert_sql, values)
    conn.commit()

print(f"✓ Loaded {len(records)} questions into {DB_PATH}")
