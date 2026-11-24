"""
Rewrite nsw_property_sales.parquet as a smaller, faster Parquet file using DuckDB:
  - rows sorted by district, suburb, street, house/unit number, contract date
  - ZSTD compression at level 19
  - Parquet v2 encodings (delta encoding for numbers and dates) + min/max statistics
Column order and all values are unchanged.

Setup (once):   pip install duckdb
Run:            python compress_parquet.py
"""
import os
import time
import duckdb

SRC = "nsw_property_sales.parquet"            # the file Claude made
DST = "nsw_property_sales_zstd19.parquet"     # the new compact file

con = duckdb.connect()

start = time.time()
con.execute(f"""
    COPY (
        SELECT *
        FROM read_parquet('{SRC}')
        ORDER BY district_code, locality, street_name, house_number, unit_number, contract_date
    )
    TO '{DST}'
    (FORMAT parquet,
     COMPRESSION zstd,
     COMPRESSION_LEVEL 19,
     ROW_GROUP_SIZE 500000,
     PARQUET_VERSION v2)
""")
print(f"Written in {time.time() - start:.0f} s")

# ---- check the new file holds exactly the same data ----
def summary(path):
    return con.execute(f"""
        SELECT COUNT(*)                          AS rows,
               COUNT(DISTINCT property_id)       AS properties,
               SUM(purchase_price)               AS total_price,
               MIN(contract_date), MAX(contract_date),
               SUM(LENGTH(legal_description))    AS legal_desc_chars
        FROM read_parquet('{path}')
    """).fetchone()

old, new = summary(SRC), summary(DST)
print("Original:", old)
print("New:     ", new)
print("Identical contents" if old == new else "WARNING: contents differ, keep the original")

# full row-by-row comparison (order-independent); 0 means every row matches
diff = con.execute(f"""
    SELECT COUNT(*) FROM (
        (SELECT * FROM read_parquet('{SRC}') EXCEPT ALL SELECT * FROM read_parquet('{DST}'))
        UNION ALL
        (SELECT * FROM read_parquet('{DST}') EXCEPT ALL SELECT * FROM read_parquet('{SRC}'))
    )
""").fetchone()[0]
print("Rows that differ:", diff)

mb = lambda p: os.path.getsize(p) / 1e6
print(f"Size: {mb(SRC):.0f} MB -> {mb(DST):.0f} MB ({100 * (1 - mb(DST) / mb(SRC)):.0f}% smaller)")
