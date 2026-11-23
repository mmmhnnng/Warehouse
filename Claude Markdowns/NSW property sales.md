# NSW Property Sales Data – Chat Record

**Participants:** Martin (Devex Systems) and Claude
**Dates:** 20–23 November 2026
**Topic:** Coogee house prices → NSW Valuer General bulk sales data → combined Parquet dataset → analysing it in Python / VS Code

---

## 1. Coogee house prices for the last decade

**Martin:** Find all house prices in Coogee for the last decade.

**Claude:** Searched the web with Nimble. Clean yearly medians were only found from 2021:

| Year | Median house price | Change | Sales |
|---|---|---|---|
| 2021 | $3,962,000 | — | 62 |
| 2022 | $3,710,000 | −6.4% | 51 |
| 2023 | $3,757,900 | +1.3% | 57 |
| 2024 | $4,352,500 | +15.8% | 52 |
| 2025 | $4,900,000 | +12.6% | 65 |
| 2026 (to Q3) | $4,885,890 | −0.3% | 58 |

Source: Heatmaps.com.au (NSW Valuer General data). Carto's 12-month median to 12 Nov 2026 was $4,730,000. 2016–2020 could not be found as a clean house-only series. With only 50–65 house sales a year, yearly medians swing a lot.

## 2. Coogee page on realestate.com.au

**Martin:** Crawl realestate.com.au to find Coogee house prices.

**Claude:** Pulled the Coogee suburb page:

- Median house price **$4,725,000** (Nov 2025 – Oct 2026), up 2.5%
- By bedrooms: 2-bed $2.5M, 3-bed $3.29M, 4-bed $4.73M
- 60 houses sold in 12 months, 23 median days on market, 2.4% rental yield (~$1,700/week)
- Units: median $1.65M, up 10%, 330 sales

The page's 5-year trend chart couldn't be extracted as numbers.

## 3. Spreadsheet of every Coogee house sale, last 3 years

**Martin:** Populate a spreadsheet with all house sales in Coogee for the last 3 years.

**Claude:** Ran a Nimble web research job across domain.com.au, realestate.com.au, onthehouse.com.au and soldnsw.com, merged duplicates, and built a Claude Sheet: **Coogee House Sales Nov 2023 – Nov 2026** (156 sales).

| Period | Sales found | Price disclosed | Median |
|---|---|---|---|
| Nov–Dec 2023 | 2 | 2 | $4,660,000 |
| 2024 | 35 | 33 | $3,900,000 |
| 2025 | 51 | 43 | $4,610,000 |
| 2026 to date | 68 | 51 | $4,700,000 |
| All 3 years | 156 | 129 | $4,330,000 |

Coverage was roughly 85–90% of recorded sales. Notes: 27 undisclosed prices; one unit removed; two unusually low prices flagged; 9 & 11 Baden St kept as one $15M sale; 10 Clifford St sold twice.

**Martin:** Why did it take so long?

**Claude:** About 21 minutes was the research job itself: it ran at high effort, the property sites block bots (so ~107 pages were loaded in a full browser), listings span many pages, and four sources had to be merged. Faster options are medium effort, a narrower request, or the Valuer General's bulk data.

## 4. NSW Valuer General bulk data

**Martin:** Can you download bulk data for suburbs from the NSW Valuer General website?

**Claude:** The files aren't per suburb: each covers all of NSW and has to be filtered. Claude's workspace can't reach the site, so the files would download via the browser.

**Martin:** The online enquiry is limited to 100 sales per enquiry. How do I get around this?

**Claude:** Use the bulk files, which have no cap. Alternatively, run smaller enquiries (short date ranges or street by street) and combine the results.

**Martin:** Link me the bulk files.

**Claude:** Download page: <https://valuation.property.nsw.gov.au/embed/propertySalesInformation>

- Yearly files: `https://www.valuergeneral.nsw.gov.au/__psi/yearly/<YEAR>.zip` (1990–2025)
- 2026 weekly files: `https://www.valuergeneral.nsw.gov.au/__psi/weekly/<YYYYMMDD>.zip` (05 Jan – 16 Nov 2026)
- Format guides:
  - [Current format (2001 onwards)](https://www.valuergeneral.nsw.gov.au/__data/assets/pdf_file/0015/216402/Current_Property_Sales_Data_File_Format_2001_to_Current.pdf)
  - [Archived format (1990–2001)](https://www.valuergeneral.nsw.gov.au/__data/assets/pdf_file/0014/216401/Archived_Property_Sales_Data_File_Format_1990_to_2001_V2.pdf)

## 5. Understanding the files

**Martin:** Can you read zip files? What are .DAT files?

**Claude:** Yes. A `.DAT` file is plain text, one record per line, fields separated by `;`. Example:

```
B;207;1994263;1;20250331 01:07;;2;11;HAVELOCK AVE;COOGEE;2034;53;M;20250326;20250326;970000;;R;RESIDENCE;14;;;0;AU923640;
```

That's council 207 (Randwick), 2/11 Havelock Ave Coogee, 53 m², contract and settlement 26 Mar 2025, $970,000, residence, strata lot 14. In the 2025 file Coogee had 444 sales, 69 of them houses; 2025-contract houses had a median of $4,850,000.

**Martin:** Why does each weekly folder have a variable number of .DAT files numbered up to ~708?

**Claude:** The number prefix is a **council area code**, not a sequence. A council only gets a file in a week if it had sales recorded. 2025 had 129 distinct codes (001–902), with 59–129 files per week. Coogee is in `207_` (Randwick). The same sale can appear in more than one week, so duplicates must be removed.

**Martin:** What council areas are 1–10?

| Code | Council area (inferred from suburbs) | 2025 sales |
|---|---|---|
| 001 | Cessnock | 2,841 |
| 002 | Dungog | 310 |
| 003 | — (no 2025 files) | — |
| 004 | Lake Macquarie | 6,009 |
| 005 | Maitland | 3,623 |
| 006 | — (no 2025 files) | — |
| 007 | Muswellbrook | 662 |
| 008 | Newcastle | 5,153 |
| 009 | — (no 2025 files) | — |
| 010 | Port Stephens | 2,289 |

**Martin:** What do record types A, B, C, D and Z mean?

| Letter | Meaning |
|---|---|
| A | Header: file type, council code, creation time |
| B | Sale details: address, dates, price, area, zoning, type, strata lot, dealing number |
| C | Legal description (lot/plan), linked to its B line |
| D | Buyer (`P`) / seller (`V`); names always withheld |
| Z | Footer with line counts for checking |

**Martin:** How would people normally combine bulk .DAT files?

**Claude:** Common approaches: `grep "^B;"` on the command line, Excel Power Query (From Folder), Python/pandas or R, a database (DuckDB, SQLite, Postgres), or ready-made scripts/paid providers.

## 6. Building the yearly spreadsheets

**Martin:** Combine the 2025 data into a spreadsheet.

**Claude:** Built `NSW_property_sales_2025.xlsx`: 237,408 NSW sales, one row per sale, duplicates removed, A/Z/D lines dropped, legal descriptions joined from C lines. Too big for a Claude Sheet, so it's an Excel file.

**Martin:** Do the same for 2008–2025, then for 1990–2007.

**Claude:** Built one Excel workbook per year (1990–2025), about 20–30 MB each. Notes:

- The re-uploaded 2025 zip contained a full copy of `2024.zip`, which was excluded so 2024 wasn't counted twice.
- 1990 to March 2001 use an **older format** with different columns; 2001 mixes both and has a `Record format` column.
- 1991 and 1992 had stray control characters in lot dimensions, which were removed.
- Annual files group sales by when they were recorded, not contract date.

**Martin:** What do you mean 1990–2000 use an older format?

| | Older format (1990 – Mar 2001) | Newer format (Mar 2001 onwards) |
|---|---|---|
| Lines per sale | One | Several (B, C, D) |
| Date style | `13/12/1990` | `20250326` |
| Dates recorded | Contract only | Contract and settlement |
| Property type | Not recorded | Recorded |
| Strata lot number | Not recorded | Recorded |
| Lot dimensions | Recorded | Not recorded |
| File grouping | One file per year | One file per council per week |

## 7. Combining everything into Parquet

**Martin:** What's the most efficient way to store all this? A CSV file?

| Format | Approx. size | Notes |
|---|---|---|
| Excel | — | Won't fit (~1M row limit) |
| CSV | ~1–1.2 GB | Universal, but slow and untyped |
| **Parquet** | ~120–230 MB | Compressed, typed, fast; works with pandas, R, DuckDB, Power BI |
| DuckDB | ~150–250 MB | SQL queries in a single file |
| SQLite | ~1 GB | Widely supported, slower for summaries |

**Martin:** Combine all file data into a single Parquet file.

**Claude:** Built `NSW_property_sales_1990_2025.parquet` (7,215,915 sales, 224 MB), later updated with 2026 to **`NSW_property_sales_1990_2026.parquet` (7,379,003 sales, 229 MB)**.

- Columns use lowercase and underscores (`contract_date`, `purchase_price`, `suburb`, ...).
- `record_format` is `archived` or `current`, and `file_year` records the source annual file.
- 9,306 sales appearing in two years' files were counted once (latest version); 12 more overlapped between 2025 and 2026.
- Source data quirks left as-is: ~2,463 contract dates before 1980, a few in the future, 496 with no contract date, ~52,842 with no or $0 price (9,445 in 1990).

**Median Coogee house price (approx. before 2001):**

| Year | Median | Year | Median |
|---|---|---|---|
| 1991 | $315,000 | 2010 | $1,740,000 |
| 1995 | $420,000 | 2015 | $2,585,000 |
| 2000 | $775,500 | 2020 | $3,125,000 |
| 2005 | $1,380,000 | 2025 | $4,850,000 |

**Martin:** 2026 weekly files – do I need to download and combine all of them?

**Claude:** Yes, until the 2026 annual file is published. Built `NSW_property_sales_2026.xlsx` (163,100 sales recorded 5 Jan – 16 Nov 2026; 119,922 with 2026 contracts). Coogee 2026 so far: 35 house sales, median $5,000,000.

**Martin:** Does the Parquet file have all suburbs?

**Claude:** Yes: 7,220 distinct suburb names over 1990–2026 (4,265 in the last 5 years, because of renamed suburbs and spelling variants), 751 postcodes, 223 council codes, 65,456 sales with no suburb. Names are in capitals, and `SOUTH COOGEE` is separate from `COOGEE`.

**Martin:** Split the Parquet file into 1990–1999, 2000–2009, 2010–2019, 2020–2026.

| File | Sales | Size |
|---|---|---|
| `NSW_property_sales_1990_1999.parquet` | 1,792,992 | 53 MB |
| `NSW_property_sales_2000_2009.parquet` | 2,169,187 | 67 MB |
| `NSW_property_sales_2010_2019.parquet` | 2,045,575 | 66 MB |
| `NSW_property_sales_2020_2026.parquet` | 1,371,249 | 44 MB |
| **Total** | **7,379,003** | |

Split by contract year. The 3,517 sales with missing or impossible contract dates go by the year of their source file. Don't keep the combined file and the split files in the same folder if you read the whole folder, or every sale loads twice.

## 8. Opening the data in Python and VS Code

### Installing packages

Run this in a terminal (Windows: cmd or PowerShell; Mac: Terminal), not inside Python:

```bash
pip install pandas pyarrow
# alternatives
python -m pip install pandas pyarrow
pip3 install pandas pyarrow        # Mac
%pip install pandas pyarrow        # inside a Jupyter cell
```

*pip* stands for "pip installs packages". It installs packages from PyPI.

### VS Code setup

1. **File → Open Folder** on `Q:\User Data\Martin\Misc\NSW Property Data`.
2. Install the **Python** and **Jupyter** extensions by Microsoft. Python Debugger comes with them; the "ms" figures in the Extensions list are just startup times.
3. If you see a Restricted Mode banner, trust the folder.
4. **Ctrl+Shift+P → Create: New Jupyter Notebook** and save it in the data folder.
5. **Select Kernel → Python Environments → Python 3.14** (`D:\Users\mhg\AppData\Local\Programs\Python\Python314\python.exe`), and install `ipykernel` if prompted. If no list appears, use **Python: Select Interpreter → Enter interpreter path…**.

**Notes:**

- Opening a `.parquet` file directly in the editor shows garbled text. That's normal, because it's binary; read it with pandas instead.
- A **kernel** is the Python process that runs the notebook's cells.
- **Jupyter** is a notebook format (cells with results shown under each one); VS Code is the editor that runs it.

### Loading the data

```python
import pandas as pd

# Everything (~7.4M rows, ~3 GB RAM, ~10 s)
df = pd.read_parquet("NSW_property_sales_1990_2026.parquet")

# Just Coogee
df = pd.read_parquet("NSW_property_sales_1990_2026.parquet",
                     filters=[("suburb", "==", "COOGEE")])

# Several suburbs, or a postcode
df = pd.read_parquet("NSW_property_sales_1990_2026.parquet",
                     filters=[("suburb", "in", ["COOGEE", "SOUTH COOGEE", "CLOVELLY", "RANDWICK"])])
df = pd.read_parquet("NSW_property_sales_1990_2026.parquet",
                     filters=[("postcode", "==", "2034")])

# A whole folder of Parquet files (no overlapping files!)
df = pd.read_parquet("parquet_files/", filters=[("suburb", "==", "COOGEE")])

# Full Windows path if the notebook is elsewhere
df = pd.read_parquet(r"Q:\User Data\Martin\Misc\NSW Property Data\NSW_property_sales_1990_2026.parquet")
```

`df` is just a variable name: it holds whatever the last `read_parquet` call loaded. A filter applied when loading is why `df` showed only Coogee.

### Viewing and analysing

```python
df.head(20)            # preview only – all rows are still loaded
df.tail(20); df.sample(20); df.iloc[100:140]
pd.set_option("display.max_columns", None)

# Median price per year, excluding $0 / missing prices
sales = df[df["purchase_price"] > 0].copy()
sales["year"] = pd.to_datetime(sales["contract_date"], errors="coerce").dt.year
sales.groupby("year")["purchase_price"].agg(["count", "median"])

# Houses since 2001
houses = df[(df["property_type"] == "Residence") & df["unit_no"].isna()]

# Days from contract to settlement (2001+ only)
recent = df[df["record_format"] == "current"].copy()
recent["days_to_settle"] = (pd.to_datetime(recent["settlement_date"])
                            - pd.to_datetime(recent["contract_date"])).dt.days
recent["days_to_settle"].median()

# Export
houses.to_excel("coogee_houses.xlsx", index=False)
```

**Data Wrangler:** run a cell ending in `df`, then click **Open 'df' in Data Wrangler** to scroll, sort and filter. It's best used on a filtered subset, not all 7.4M rows.

**Things to remember:**

- **Settlement dates are blank before 2001.** The old format never recorded them (Coogee: 5,229 older rows have none; all 9,940 rows from 2001 have them).
- **Price outliers:** the largest Coogee sales are not houses, for example $395.2M for 146 Coogee Bay Rd in 2020 ("Other"), $139.5M for 80 Mount St in 2017 (one strata lot), and $77.1M for 88 Moverly Rd in 2003. Use medians, or filter to residences.
- **Prices of $0** are mostly 1990 records with no usable price.

---

## Files produced

| File | Contents |
|---|---|
| Claude Sheet: *Coogee House Sales Nov 2023 – Nov 2026* | 156 web-scraped Coogee house sales plus a summary tab |
| `NSW_property_sales_<YEAR>.xlsx` (1990–2026) | One workbook per year of NSW sales |
| `NSW_property_sales_1990_2026.parquet` | All 7,379,003 sales combined |
| `NSW_property_sales_1990_1999.parquet` … `2020_2026.parquet` | The same data split into four periods |

*Data: NSW Valuer General bulk Property Sales Information, licensed under CC BY-NC-ND 4.0.*
