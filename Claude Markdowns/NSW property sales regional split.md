# NSW Property Analysis: region split and analysis tools (chat record, 23 Nov 2026)

Project: **NSW Property Analysis** · Source: `NSW_property_sales_1990_2026.parquet` (NSW Valuer General sales, 7,379,003 rows, 30 columns)

---

## 1. Split the data into four regional parquet files

**Output files** (each has all source columns plus `region` and `sub_region`, which is the council area; no suburb appears in more than one file):

| File | Rows | Suburbs |
|---|---|---|
| `sydney_eastern_suburbs_sales_1990_2026.parquet` | 238,623 | 34 |
| `sydney_city_sales_1990_2026.parquet` | 256,448 | 29 |
| `sydney_inner_west_sales_1990_2026.parquet` | 349,867 | 52 |
| `sydney_north_shore_sales_1990_2026.parquet` | 340,406 | 60 |

**Method:** suburb names were upper-cased, with "(...)" qualifiers and a trailing "NSW" removed, then matched to a suburb list, keeping only postcodes 2000–2234. Every suburb on the lists matched sales in the data. Written with DuckDB.

**Region definitions:**
- **Eastern Suburbs:** Waverley, Woollahra (including Paddington and Centennial Park) and Randwick council areas. The Botany Bay area (Botany, Eastlakes, Pagewood, Mascot) is excluded.
- **City:** the City of Sydney council area, except Glebe, Forest Lodge and Erskineville, which are in Inner West.
- **Inner West:** Inner West Council area + Glebe/Forest Lodge/Erskineville + Canada Bay, Burwood and Strathfield council areas (broad definition). For the narrow definition, filter `sub_region` to "Inner West Council" and "City of Sydney (inner west)".
- **North Shore:** Lower North Shore (North Sydney, Mosman, Willoughby, Lane Cove, Hunters Hill) + Upper North Shore (Ku-ring-gai, including Wahroonga). Hornsby is excluded.

**Data note:** some contract dates are invalid (e.g. years 0015 and 2031); left untouched. Definitions saved to the project as `region_definitions.md`.

---

## 2. Best way to analyse the data yourself

**Tools:** DuckDB (query and filter) → Python with GeoPandas (join to boundaries, choropleths) → PySAL `esda` (Getis-Ord Gi* / Local Moran's I hotspots) → folium, lonboard or kepler.gl (interactive maps) → QGIS (GUI exploration and layer stacking).

**Map data to download:**
- ABS Suburbs and Localities (SAL) or Postal Areas (POA) boundaries, ASGS 2021.
- G-NAF (free national address file with coordinates), to turn each sale into a point for hex or heat maps.
- NSW Spatial Services cadastre, for lot-level shapes (match on `legal_description`).

**Cleaning:**
- Remove duplicates on `dealing_number` + `property_id`.
- Drop bad dates.
- Keep residential sales only; exclude non-market and part-share (`pct_interest`) sales.
- $/sqm only works for houses (land area); check `area_unit`, as some rows are hectares.
- Use medians and adjust for inflation with ABS CPI.
- Compare like with like (houses with houses) or build a repeat-sales index, so a change in the mix of homes sold doesn't look like a price change.

**Workflow:** filtered DuckDB view → suburb × year medians, $/sqm, growth → join to SAL boundaries → choropleth (quantile colour scale) → Gi* hotspots → one layer per filter in QGIS or kepler.gl.

---

## 3. QGIS vs Mapbox

| | QGIS | Mapbox |
|---|---|---|
| What it is | Free desktop GIS app | Paid web mapping platform |
| Strength | Analysis, layer stacking, print maps | Fast, polished interactive web maps |
| Analysis tools | Many built in, plus plugins and Python | Very few; analyse elsewhere first |
| Cost | Free | Free tier, then pay per map load |

Use QGIS for analysis and exploration. For sharing on the web: kepler.gl (free, no code), MapLibre (free fork of Mapbox GL JS) or Felt. Use Mapbox only for a client-facing product.

---

## 4. What DuckDB is

A free, open-source SQL database that runs inside your program, with no server ("SQLite for analytics"). It queries parquet and CSV files directly, handles 7M+ rows in seconds and works with data larger than memory. Results go to pandas in one line, and it has a spatial extension. It's not built for many users writing at once (use Postgres for that).

---

## 5. What people used before DuckDB (2019)

- **pandas / R:** everything in memory, so slow or crashing on large data.
- **SQLite:** built for transactions, slow for analytics.
- **Postgres + PostGIS:** powerful, but needs a server and importing data.
- **Spark / Hadoop:** cluster tools, overkill for laptop-sized data.
- **Cloud warehouses** (BigQuery, Snowflake): pay per query, data in the cloud.
- **Excel / Access:** Excel stops at about 1M rows.
- **Desktop GIS:** slow on large datasets.

Polars arrived around the same time as a fast alternative to pandas.

---

## 6. DuckDB vs pandas vs Polars

| | DuckDB | pandas | Polars |
|---|---|---|---|
| How you write it | SQL | Python methods | Python expressions |
| Speed / memory | Very fast / low | Slowest / high | Very fast / low |
| Reads parquet without loading it | Yes | No | Yes (`scan_parquet`) |
| Spatial | Spatial extension | GeoPandas (the standard) | Limited |

**For this project:** DuckDB for the heavy lifting; pandas/GeoPandas for the small result (maps, PySAL). Polars only if you prefer Python syntax to SQL. They share data with almost no conversion cost (`.df()`, `.pl()`).

---

## 7. SQL vs Python

Use both: **SQL** to filter, join and aggregate; **Python** for maps, statistics and automation. If you're learning one first, **start with SQL**: it's quicker to pick up and works in almost every data tool. The usual setup is a Jupyter notebook running Python with SQL strings sent to DuckDB.

---

## 8. The two setups

```
A: parquet → DuckDB (SQL) ───────→ pandas → GeoPandas → maps / hotspots
B: parquet → Polars (Python) ─→ .to_pandas() → GeoPandas → maps / hotspots
```

**Setup:**
```bash
python -m venv .venv && source .venv/bin/activate
pip install jupyterlab pyarrow pandas geopandas mapclassify folium libpysal esda matplotlib
pip install duckdb      # A
pip install polars      # B
```

**A: clean and summarise in SQL**
```python
import duckdb
con = duckdb.connect()
con.sql("""
CREATE OR REPLACE VIEW sales AS
SELECT DISTINCT ON (dealing_number, property_id) *
FROM 'data/sydney_*_sales_1990_2026.parquet'
WHERE contract_date BETWEEN '1990-01-01' AND current_date
  AND property_type = 'Residence' AND purchase_price > 50000
  AND (pct_interest IS NULL OR pct_interest IN (0, 100))
""")
summary = con.sql("""
SELECT upper(suburb) AS suburb, region, year(contract_date) AS yr,
       median(purchase_price) AS median_price,
       median(purchase_price / area) FILTER (WHERE area_unit='m2' AND area BETWEEN 100 AND 5000) AS median_psqm,
       count(*) AS n
FROM sales GROUP BY ALL
""").df()
```

**B: clean and summarise in Polars**
```python
import polars as pl
sales = (pl.scan_parquet("data/sydney_*_sales_1990_2026.parquet")
    .filter(pl.col("contract_date").is_between(pl.date(1990,1,1), pl.lit(pl.date(2026,11,23))),
            pl.col("property_type") == "Residence", pl.col("purchase_price") > 50_000,
            pl.col("pct_interest").is_null() | pl.col("pct_interest").is_in([0, 100]))
    .unique(subset=["dealing_number", "property_id"]))
psqm_ok = (pl.col("area_unit") == "m2") & pl.col("area").is_between(100, 5000)
summary = (sales.with_columns(pl.col("suburb").str.to_uppercase(), yr=pl.col("contract_date").dt.year())
    .group_by("suburb", "region", "yr")
    .agg(median_price=pl.col("purchase_price").median(),
         median_psqm=(pl.col("purchase_price") / pl.col("area")).filter(psqm_ok).median(),
         n=pl.len())
    .collect().to_pandas())
```

**Shared: map and hotspots**
```python
import geopandas as gpd, libpysal, esda
sal = gpd.read_file("data/SAL_2021_AUST_GDA2020.shp")
sal = sal[sal.STE_NAME21 == "New South Wales"]
sal["suburb"] = sal.SAL_NAME21.str.replace(r"\s*\(.*\)", "", regex=True).str.upper()
gdf = sal.merge(summary[(summary.yr == 2025) & (summary.n >= 10)], on="suburb")
gdf.explore(column="median_psqm", scheme="quantiles")
w = libpysal.weights.Queen.from_dataframe(gdf, use_index=True)
g = esda.G_Local(gdf.median_psqm.fillna(gdf.median_psqm.median()), w, star=True)
gdf["hotspot"] = ["hot" if z > 0 and p < 0.05 else "cold" if z < 0 and p < 0.05 else "ns"
                  for z, p in zip(g.Zs, g.p_sim)]
gdf.to_file("out/psqm_2025.gpkg")
```

These snippets haven't been run. Check the actual `property_type` and `pct_interest` values first.

**Recommendation:** DuckDB + GeoPandas, because the SQL is shorter, it can save tables between sessions, it has spatial joins built in, and SQL skills carry over to other tools.

**What each stage does:** the parquet files (240k–350k rows per region) are cleaned and summarised by DuckDB or Polars down to a few thousand suburb × year rows. That small table is handed to pandas, joined by GeoPandas to a few hundred suburb shapes, and then mapped. The hand-off to pandas exists because GeoPandas and PySAL are built on pandas.

---

## 9. How long it would take

- **Computer time:** seconds for every step.
- **Your time:** about 1 day if you already know Python/SQL; about 3–5 days with some coding but new to GIS; about 2–3 weeks part-time as a beginner.
- **What takes longest:** data quality (50% or more of the effort), matching suburb names to boundaries, and G-NAF geocoding (another 1–3 days).
- **Comparison:** DuckDB is faster to start if you know any SQL; Polars syntax takes a few days to feel natural.

---

## 10. Is DuckDB a Python package?

Yes (`pip install duckdb`, then `import duckdb`), with no server. It's also available as a command-line tool, for R, Node, Java, Rust and Go, in the browser (DuckDB-WASM), in DBeaver, and with its own browser interface (`duckdb -ui`).

---

## 11. PyCharm vs VS Code

**VS Code** is recommended for notebooks + DuckDB + GeoPandas: free, light, very good Jupyter support, with interactive maps shown inside the notebook. **PyCharm** suits large Python applications and heavy refactoring; its advanced database tools are in the paid tier. Alternatives: JupyterLab, or **Positron** (Posit's data-science IDE built on VS Code).

---

## 12. Is Positron faster to set up than DuckDB + pandas?

They aren't alternatives: Positron is an editor, and DuckDB and pandas are libraries you install inside it. Positron vs VS Code setup is about 5–10 min vs 10–15 min. Positron's advantages: a built-in data viewer, variables pane, plots pane, and a console + script workflow. Downsides: it's newer, with fewer extensions and less help online.

---

## 13. Viewing data in VS Code

1. **Data Wrangler extension (recommended):** right-click a parquet or CSV file → Open in Data Wrangler. Gives a sortable, filterable grid, column stats and histograms, and point-and-click cleaning that writes pandas code.
2. **Jupyter Variables panel** → click a DataFrame to open it.
3. **In code:** `df.head()`, `df.sample()`, `df.describe()`, `df.info()`, and `duckdb.sql("SUMMARIZE 'file.parquet'")`.
4. **DuckDB SQL extensions** (e.g. SQLTools with a DuckDB driver).

For the full 7.4M-row NSW file, sample first (`USING SAMPLE 50000`).

---

## 14. Choropleth maps in VS Code

1. **Static:** `gdf.plot(column=..., scheme="quantiles", k=7)`.
2. **Interactive:** `gdf.explore(...)` (folium), which supports stacked layers and `.save("map.html")`.
3. **Plotly** `px.choropleth_map(...)`; adding `animation_frame="yr"` gives a time-slider map.
4. **Lonboard** `viz(gdf)` for large point datasets.
5. **Outside the notebook:** export a `.gpkg` for QGIS, or open the data in kepler.gl.

**Tips:** simplify the boundaries, use quantile or natural-break colour scales, hide suburbs with fewer than about 10 sales, and map Gi* results as a separate three-colour layer.

---

## 15. Do I have to plot in VS Code before QGIS? Does Positron map automatically?

No to both. Neither IDE draws maps without code; Positron's viewer shows tables only. You can go straight from cleaned data to QGIS: Python cleans, summarises, joins and runs `to_file(".gpkg")`, then QGIS does the point-and-click styling. A quick `gdf.explore()` check is optional.

---

## 16. Does VS Code have a plots pane?

Not a dedicated one. Plots appear inline in notebooks; the **Interactive Window** (`# %%` cells in a `.py` file) keeps a running history of outputs; the **Plot Viewer** zooms and saves static plots; and outputs can be moved to their own editor group.

**What "for maps it makes little difference" meant:** a plots pane mainly helps with static charts. Interactive maps are fully usable inside notebooks, and QGIS is better than either IDE for exploring maps.

---

## 17. Where QGIS fits

- **Option 1 (recommended):** parquet → DuckDB → GeoPandas (join + Gi* hotspots) → `.gpkg` → QGIS for styling, layers and exploration.
- **Option 2:** DuckDB summary → CSV/parquet → QGIS does the join (Layer Properties → Joins) and the mapping.
- **In practice it's a loop:** spot an oddity in QGIS → fix it in Python → re-export to the same `.gpkg` → refresh the layer in QGIS (styling stays).
- Save each filter as its own layer in one GeoPackage (e.g. `houses_2025_psqm`, `units_2025_price`, `hotspots_gi`) so you can switch them on and off in QGIS.
