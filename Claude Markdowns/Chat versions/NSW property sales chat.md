# NSW Property Sales Data – Full Chat

**Participants:** Martin (Devex Systems) and Claude
**Dates:** 20–23 November 2026

Martin's questions are quoted exactly as typed. Claude's answers are condensed, keeping the substance, tables and code.

---

### 1

> **Martin:** /nimble:search find all house prices in Coogee for the last decade

**Claude:** Searched with the Nimble connector (the Nimble CLI wasn't installed). Clean yearly Coogee house medians were only available from 2021 (Heatmaps.com.au, NSW Valuer General sales data):

| Year | Median house price | Change | Sales |
|---|---|---|---|
| 2021 | $3,962,000 | — | 62 |
| 2022 | $3,710,000 | −6.4% | 51 |
| 2023 | $3,757,900 | +1.3% | 57 |
| 2024 | $4,352,500 | +15.8% | 52 |
| 2025 | $4,900,000 | +12.6% | 65 |
| 2026 (to Q3) | $4,885,890 | −0.3% | 58 |

- Carto's 12-month median to 12 Nov 2026 was $4,730,000.
- 2016–2020 wasn't available as a house-only series. AreaSearch's 10-year figure ($1.185M → $1.79M) mixes houses and units.
- With only 50–65 house sales a year, yearly medians swing a lot.

---

### 2

> **Martin:** crawl through [Search for Real Estate, Property & Homes - realestate.com.au](https://www.realestate.com.au/) to find coogee house prices

**Claude:** Nimble had no ready-made scraper for the site, so Claude pulled the Coogee suburb page directly.

- **Median house price $4,725,000** (Nov 2025 – Oct 2026), up 2.5% on the year.
- By bedrooms: 2-bed $2,500,000 · 3-bed $3,292,500 · 4-bed $4,725,000.
- 60 houses sold in 12 months, 23 median days on market, 11 listed last month, 1,646 interested buyers, ~$1,700/week rent (2.4% yield).
- Units: median $1,650,000 (up 10%), 330 sales.
- The page's 5-year trend chart couldn't be extracted as numbers.

---

### 3

> **Martin:** Can you populate in a spreadsheet all buy/sell house prices for every property in Coogee for the last 3 years

**Claude:** Ran a Nimble web research job across domain.com.au, realestate.com.au, onthehouse.com.au and soldnsw.com, merged cross-site duplicates, and built a Claude Sheet, **"Coogee House Sales Nov 2023 – Nov 2026"**, with 156 sales (Sales tab plus a Summary tab).

| Period | Sales found | Price disclosed | Median |
|---|---|---|---|
| Nov–Dec 2023 | 2 | 2 | $4,660,000 |
| 2024 | 35 | 33 | $3,900,000 |
| 2025 | 51 | 43 | $4,610,000 |
| 2026 to date | 68 | 51 | $4,700,000 |
| All 3 years | 156 | 129 | $4,330,000 |

- Coverage was about 85–90% of recorded sales, with 2024 the thinnest.
- 27 sales had undisclosed prices.
- One unit was removed (8/226 Oberon St), two very low prices were flagged (50 Mount St, 2 Quail St), 9 & 11 Baden St was kept as one $15M sale, and 10 Clifford St sold twice ($2.7M in 2024, $4.6M in 2025).

---

### 4

> **Martin:** why did it take so long?

**Claude:** About 21 minutes was the research job itself:

- It ran at **high** effort (8–17 minutes quoted, against 3–6 at medium).
- The property sites block bots, so ~107 pages had to be loaded in a full browser.
- Listings span ~10 pages per site, plus individual listings.
- Four sources had to be compared and merged.

Faster options: medium effort, a narrower request, or the NSW Valuer General bulk sales file.

---

### 5

> **Martin:** can you download bulk data for suburbs in NSW Valuer General website?

**Claude:** Yes, with a catch. The files aren't per suburb: each covers all of NSW, so they have to be filtered to Coogee. Claude's workspace can't reach the site directly, so the files would download through the browser. Needed: 2023, 2024 and 2025 yearly files plus the 46 weekly 2026 files. Claude asked permission before downloading.

---

### 6

> **Martin:** NSW Value General property sales enquiries are limited to 100 sales generated per enquiry, how can I get around this?

**Claude:** The **bulk files** have no cap; the 100-result limit only applies to the online enquiry tool. If you use the enquiry tool anyway, run smaller searches (1–2 month date ranges, or street by street) and combine the results. The bulk files are faster and less likely to miss sales.

---

### 7

> **Martin:** link me the bulk files

**Claude:**

- Download page: <https://valuation.property.nsw.gov.au/embed/propertySalesInformation>
- Yearly files: `https://www.valuergeneral.nsw.gov.au/__psi/yearly/<YEAR>.zip` (2023, 2024, 2025, …)
- 2026 weekly files: `https://www.valuergeneral.nsw.gov.au/__psi/weekly/<YYYYMMDD>.zip`, from `20260105` to `20261116` (46 files)
- [Current file format guide (2001 onwards)](https://www.valuergeneral.nsw.gov.au/__data/assets/pdf_file/0015/216402/Current_Property_Sales_Data_File_Format_2001_to_Current.pdf)

Each zip contains more zips, one per council area. Coogee is in Randwick council.

---

### 8

> **Martin:** *(uploaded 2025.zip)* can you read zip files? and what are .DAT files?

**Claude:** Yes, the 2025 file opened fine: **444 Coogee sales, 69 of them houses**.

A `.DAT` file is plain text, one record per line, with fields separated by `;`:

```
B;207;1994263;1;20250331 01:07;;2;11;HAVELOCK AVE;COOGEE;2034;53;M;20250326;20250326;970000;;R;RESIDENCE;14;;;0;AU923640;
```

That's a sale (`B`) in council area 207 (Randwick): 2/11 Havelock Ave Coogee, 53 m², contract and settlement 26 Mar 2025, $970,000, residence, strata lot 14.

`2025.zip` holds 52 weekly zips, each with one `.DAT` per council (~6,400 files). The 58 houses with 2025 contracts had a median of **$4,850,000**, against Heatmaps' $4.9M.

---

### 9

> **Martin:** inside are 52 files, which are labelled the date which each weekly sales report was captured. however each weekly folder seems to have variable amount of .DAT files numbered usually up to 708, explain

**Claude:** The number prefix is a **council area code**, not a sequence number.

- `207_SALES_DATA_NNME_31032025.DAT` = Randwick council's sales recorded in the week of 31 Mar 2025.
- 2025 has **129 distinct codes** (001–902). The gaps are from merged or renamed councils, such as the 2016 amalgamations.
- A council only gets a file if it had sales that week: **59–129 files per week**. 54 councils appear every week; rural ones much less often.
- The file date is when the sale was recorded, not the contract date, and the same sale can appear in more than one week (Coogee: 453 entries, 444 unique sales).

---

### 10

> **Martin:** so what council area is 1-10?

**Claude:** All Hunter region. Names are inferred from the suburbs in each code's 2025 sales:

| Code | Council area | 2025 sales | Main suburbs |
|---|---|---|---|
| 001 | Cessnock | 2,841 | Cessnock, Kurri Kurri, North Rothbury |
| 002 | Dungog | 310 | Dungog, Clarence Town, Vacy |
| 003 | — | none | no 2025 files |
| 004 | Lake Macquarie | 6,009 | Charlestown, Warners Bay, Cardiff |
| 005 | Maitland | 3,623 | Rutherford, East Maitland, Thornton |
| 006 | — | none | no 2025 files |
| 007 | Muswellbrook | 662 | Muswellbrook, Denman |
| 008 | Newcastle | 5,153 | Newcastle, Merewether, Wallsend |
| 009 | — | none | no 2025 files |
| 010 | Port Stephens | 2,289 | Raymond Terrace, Nelson Bay |

---

### 11

> **Martin:** can you concatenate the whole 2025 sales file data into a spreadsheet

**Claude:** Built **`NSW_property_sales_2025.xlsx`** (27 MB): **237,408 NSW sales**, one row per sale. It's too large for a Claude Sheet, so it's an Excel file.

- Duplicates across weeks were removed (latest version kept).
- A/Z marker lines and the D lines (buyers and sellers, names always blank) were dropped. Legal descriptions were joined from the C lines.
- 208,447 residences, 16,797 vacant land, 12,164 other.
- About 85% have 2025 contract dates; the rest are older contracts recorded in 2025, so filter on Contract date.

---

### 12

> **Martin:** how would people normally combine bulk .DAT files?

**Claude:**

1. **Command line:** `grep -h "^B;" */*.DAT > sales_2025.csv`
2. **Excel Power Query:** Get Data → From Folder → Combine, `;` delimiter, filter to `B`. Refreshable, but limited to ~1M rows.
3. **Python/pandas** (or R):
   ```python
   import glob, pandas as pd
   rows = [l.rstrip("\n").split(";") for f in glob.glob("*/*.DAT")
           for l in open(f, encoding="latin-1") if l.startswith("B;")]
   pd.DataFrame(rows).to_csv("sales.csv", index=False)
   ```
4. **A database** (DuckDB, SQLite, Postgres) for many years of data.
5. **Ready-made scripts** on GitHub, or paid providers (PropTrack, CoreLogic).

---

### 13

> **Martin:** what does sale type A, B, C, D and Z mean?

**Claude:** They're **record types**, not sale types:

| Letter | Meaning | Example |
|---|---|---|
| A | Header, one per file | `A;RTSALEDATA;207;20250331 01:07;VALNET;` |
| B | Sale details (the useful data) | address, dates, price, area, zoning, type, strata lot, dealing no. |
| C | Legal description (lot/plan) | `C;…;14/SP10533;` |
| D | Buyer (`P`) or seller (`V`); names withheld | `D;…;P;;;;;;` |
| Z | Footer with line counts | `Z;160;33;33;92;` |

The B, C and D lines for one sale share the council code, property ID and sale counter.

---

### 14

> **Martin:** *(uploaded 2008–2025 zips)* combine the data within each zip file into their own spreadsheets like you already did for 2025

**Claude:** Built 18 workbooks (2008–2025), about 3.7M sales in total.

| Year | Sales | Year | Sales |
|---|---|---|---|
| 2008 | 190,157 | 2017 | 249,867 |
| 2009 | 197,227 | 2018 | 210,503 |
| 2010 | 185,237 | 2019 | 189,587 |
| 2011 | 174,811 | 2020 | 197,009 |
| 2012 | 174,595 | 2021 | 240,190 |
| 2013 | 195,281 | 2022 | 195,935 |
| 2014 | 217,689 | 2023 | 183,552 |
| 2015 | 231,932 | 2024 | 214,069 |
| 2016 | 224,116 | 2025 | 237,408 |

The new 2025 zip contained a full copy of `2024.zip`, which was excluded to avoid double counting.

---

### 15

> **Martin:** *(uploaded 1990–2007 zips)* Do the same for these

**Claude:** Built 18 more workbooks, so 1990–2025 is complete.

| Year | Sales | Year | Sales |
|---|---|---|---|
| 1990 | 105,332 | 1999 | 216,660 |
| 1991 | 226,542 | 2000 | 183,908 |
| 1992 | 211,608 | 2001 | 208,894 |
| 1993 | 150,856 | 2002 | 262,539 |
| 1994 | 148,516 | 2003 | 266,800 |
| 1995 | 158,756 | 2004 | 234,386 |
| 1996 | 168,424 | 2005 | 183,750 |
| 1997 | 201,912 | 2006 | 184,936 |
| 1998 | 194,860 | 2007 | 207,651 |

- 1990–2000 use an **older format** with different columns, grouped by contract year.
- "Zone code" and "Component code" in those years are best-guess labels; check them against the archived format guide.
- 2001 mixes both formats and has a "Record format" column.
- Stray control characters were removed from 1991–1992 lot dimensions.

---

### 16

> **Martin:** if i were to combine all this data, what would be the most efficient way to store this data? in a CSV file?

**Claude:** About 7.2M sales in total:

| Format | Approx. size | Notes |
|---|---|---|
| Excel | — | Won't fit (~1M row limit) |
| CSV | ~1–1.2 GB | Universal, but slow and untyped; leading zeros can be lost |
| **Parquet** | ~120–200 MB | Compressed, typed, fast; pandas, R, DuckDB, Power BI |
| DuckDB | ~150–250 MB | Plain SQL in a single file |
| SQLite | ~1 GB | Compatible, slower for summaries |

Recommendation: **Parquet**, queried with DuckDB or pandas.

---

### 17

> **Martin:** what do you mean 1990-2000 use older format?

**Claude:** The Valuer General changed systems in 2001.

| | Older (1990 – Mar 2001) | Newer (29 Mar 2001 onwards) |
|---|---|---|
| Lines per sale | One | Several (B, C, D) |
| Date style | `13/12/1990` | `20250326` |
| Dates | Contract only | Contract and settlement |
| Property type | No | Yes |
| Strata lot | No (only "SP" in legal description) | Yes |
| Lot dimensions | Yes | No |
| File grouping | One file per year | One per council per week |

Old-format example: `B;204;ARCHIVE;T000627;;;34;SPRING ST;ABBOTSFORD;2046;13/12/1990;371000;LOT COR 8 DP12292;622;M;15.11X41.15;;;;;;`

---

### 18

> **Martin:** combine all file data into a single parquet file

**Claude:** Built **`NSW_property_sales_1990_2025.parquet`**: 7,215,915 sales, 224 MB.

- Columns use lowercase and underscores (`contract_date`, `purchase_price`, `suburb`, …), with proper dates and numbers.
- `record_format` (`archived`/`current`) and `file_year` columns.
- 9,306 sales that appeared in two years' files were counted once.
- Source quirks left as-is: 2,463 contract dates before 1980, 7 in the future, 496 missing; 52,842 sales with no or $0 price (9,445 in 1990).

Median Coogee house price (approximate before 2001): 1991 $315k · 1995 $420k · 2000 $775.5k · 2005 $1.38M · 2010 $1.74M · 2015 $2.585M · 2020 $3.125M · 2025 $4.85M.

---

### 19

> **Martin:** so i can open this with pandas through python?

**Claude:** Yes, after `pip install pandas pyarrow`:

```python
import pandas as pd
df = pd.read_parquet("NSW_property_sales_1990_2025.parquet")   # ~10 s, ~2.9 GB RAM

coogee = pd.read_parquet("NSW_property_sales_1990_2025.parquet",
    columns=["contract_date", "purchase_price", "suburb", "property_type",
             "unit_no", "house_no", "street", "record_format"],
    filters=[("suburb", "==", "COOGEE")])                        # 0.2 s, 15,169 rows
```

Suburb names are in capitals. Wrap `contract_date` in `pd.to_datetime()` before using `.dt`.

---

### 20

> **Martin:** where do i pip install again?

**Claude:** In a **terminal**, not inside Python. On Windows that's cmd or PowerShell; on Mac, Terminal.

```bash
pip install pandas pyarrow
pip3 install pandas pyarrow          # Mac alternative
python -m pip install pandas pyarrow # most reliable
%pip install pandas pyarrow          # inside a Jupyter cell
```

If Python isn't found, install it from python.org and tick "Add Python to PATH" on Windows.

---

### 21

> **Martin:** what does pip actually stand for?

**Claude:** **"pip installs packages"**, a recursive acronym (older explanation: "Pip Installs Python"). It installs packages from PyPI (pypi.org).

---

### 22

> **Martin:** ok i have pandas and the pandas pyarrow parquet reading package, how do i open this in VS Code?

**Claude:**

1. File → Open Folder on the folder containing the Parquet file.
2. Install the **Python** extension (Microsoft).
3. Ctrl+Shift+P → **Create: New Jupyter Notebook**, then **Select Kernel** → your Python, and install `ipykernel` if prompted.
4. Run the `read_parquet` code with Shift+Enter.

Optional: the **Data Wrangler** extension for a spreadsheet-style view. If you get "No module named pandas", use **Python: Select Interpreter** to pick the Python you installed it into.

---

### 23

> **Martin:** *(screenshot of garbled text)* this is all i see

**Claude:** That's normal. Parquet is a compressed binary format, so opening it in the editor shows garbage. Close the tab without saving, open the folder, create a notebook, select the kernel and run:

```python
import pandas as pd
df = pd.read_parquet(
    r"Q:\User Data\Martin\Misc\NSW Property Data\NSW_property_sales_1990_2025.parquet",
    filters=[("suburb", "==", "COOGEE")])
df.head(20)
```

---

### 24

> **Martin:** why do i need to open a Jupyter notebook? is Jupyter like VS Code?

**Claude:** VS Code is a code editor; **Jupyter notebook** is a file type (`.ipynb`) that runs code in cells and shows results under each one. You don't strictly need one, but for exploring data it's handy: load the big file once, then run many queries without reloading. A `.py` script runs top to bottom and only shows what you `print()`.

---

### 25

> **Martin:** what is a kernel? which kernel do i use? i have Python and VS Code installed

**Claude:** The **kernel** is the Python program that runs the notebook's cells and keeps your data in memory. Pick the Python you installed pandas into. To find its path:

```bash
python -c "import sys, pandas; print(sys.executable)"
```

Then Select Kernel → Python Environments… → choose that path, and install `ipykernel` if asked.

---

### 26

> **Martin:** i got this "D:\Users\mhg\AppData\Local\Programs\Python\Python314\python.exe"

**Claude:** That's Python 3.14 with pandas. Select it as the kernel and check:

```python
import pandas as pd, pyarrow
print(pd.__version__, pyarrow.__version__)
```

If pyarrow is missing:
`D:\Users\mhg\AppData\Local\Programs\Python\Python314\python.exe -m pip install pyarrow`

---

### 27

> **Martin:** *(screenshot of Extensions)* difference between the first two? 206ms vs 62m?

**Claude:**

- **Python** is the main extension (running code, interpreters, suggestions).
- **Python Debugger** handles breakpoints and stepping through code. Keep both.
- 206ms and 62ms are each extension's **startup time**, which is harmless.
- The Python path had been pasted into the **Extensions search**, which does nothing there. It goes in the notebook's Select Kernel instead.

---

### 28

> **Martin:** i click select kernel and paste the path but nothing happens

**Claude:** Select Kernel shows a list to pick from; typing only filters it. Options:

- Select Kernel → **Python Environments…** → click Python 3.14.
- Or Ctrl+Shift+P → **Python: Select Interpreter** → **+ Enter interpreter path…** → paste the path → Enter.
- If still missing, restart VS Code, or run a `.py` script directly with the full python.exe path.

---

### 29

> **Martin:** no list appears

**Claude:** Two likely causes:

1. The **Jupyter extension** (Microsoft) isn't installed. Install it, then run **Developer: Reload Window**.
2. **Restricted Mode**: trust the folder via **Workspaces: Manage Workspace Trust**.

Fallback: a script `analysis.py`, run with
`D:\...\Python314\python.exe "Q:\User Data\Martin\Misc\NSW Property Data\analysis.py"`

---

### 30

> **Martin:** how to check if Jupyter extension installed

**Claude:** Open Extensions (Ctrl+Shift+X), search **`@installed jupyter`**. **Jupyter** by Microsoft should be listed and enabled. If not, search `jupyter`, click Install, then reload the window.

---

### 31

> **Martin:** this shortcut does something else

**Claude:** Other ways to open Extensions: **View → Extensions**, the four-squares icon in the left bar, or Ctrl+Shift+P → **Extensions: Show Installed Extensions**. Search `jupyter`: an **Install** button means it's missing; a gear icon means it's installed.

---

### 32

> **Martin:** *(screenshot of notebook)* does this look ready now?

**Claude:** Yes: the kernel shows **Python 3.14.4**. Save the notebook in the data folder (Ctrl+S), then run:

```python
import pandas as pd
df = pd.read_parquet("NSW_property_sales_1990_2025.parquet",
                     filters=[("suburb", "==", "COOGEE")])
print(len(df), "Coogee sales")
df.head(20)
```

---

### 33

> **Martin:** *(screenshot)* is says "15169 Coogee Sales" but htere is only 20 rows

**Claude:** All 15,169 rows are loaded; `df.head(20)` just previews the first 20. Other views:

```python
df            # first and last 5
df.tail(20); df.sample(20); df.iloc[100:140]
pd.set_option("display.max_columns", None)   # show all 30 columns
```

The many $0 prices in 1990 mean no usable price, so filter them out with `df[df["purchase_price"] > 0]`. `None`/`NaN` means blank.

```python
sales = df[df["purchase_price"] > 0].copy()
sales["year"] = pd.to_datetime(sales["contract_date"], errors="coerce").dt.year
sales.groupby("year")["purchase_price"].agg(["count", "median"])
```

---

### 34

> **Martin:** i installed Data Wrangler, what do i type now to display everything

**Claude:** Run a cell containing just `df`, then click **"Open 'df' in Data Wrangler"** above the output. There you can scroll all rows, sort by header, filter, and see column summaries. Changes there don't affect the Parquet file.

---

### 35

> **Martin:** *(screenshot)* seems like second column "Settlement Dates" are missing values, however in the spreadsheet files they are there

**Claude:** The top rows are 1990 sales, and the old format never recorded settlement dates.

| Coogee sales | Rows | With settlement date |
|---|---|---|
| Older format (1990 – early 2001) | 5,229 | 0 |
| Newer format (2001+) | 9,940 | 9,940 |

Sort contract_date descending, or filter record_format to `current`, to see them.

Price outliers: $395.2M for 146 Coogee Bay Rd (2020, "Other"), $139.5M for 80 Mount St (2017, one strata lot), $77.1M for 88 Moverly Rd (2003). Use medians, or filter to residences.

---

### 36

> **Martin:** oh you're right, 2001 onwards has the values

**Claude:** Yes. For comparisons across all years, use the contract date. Time to settle (2001+):

```python
recent = df[df["record_format"] == "current"].copy()
recent["days_to_settle"] = (pd.to_datetime(recent["settlement_date"])
                            - pd.to_datetime(recent["contract_date"])).dt.days
recent["days_to_settle"].median()
```

---

### 37

> **Martin:** *(screenshot of download page)* for 2026 sales data, do I need to download and combine all weekly sales files?

**Claude:** Yes, until the 2026 annual file is published (probably early 2027). The weekly files use the same format, so they combine cleanly and duplicates are removed. Upload them all at once; a new weekly file comes out every Monday.

---

### 38

> **Martin:** *(uploaded 2026.zip)* combine data into spreadsheet

**Claude:** Built **`NSW_property_sales_2026.xlsx`**: 163,100 sales from 46 weekly files (5 Jan – 16 Nov 2026), 119,922 with 2026 contracts. Also rebuilt the combined file as **`NSW_property_sales_1990_2026.parquet`** (7,379,003 sales, 229 MB); 12 corrections of 2025 sales were counted once. Coogee 2026 so far: 35 house sales, median **$5,000,000**. One contract date reads as the year 225, a source typo.

---

### 39

> **Martin:** does the parquet file have all suburbs?

**Claude:** Yes, all of NSW:

| | Count |
|---|---|
| Distinct suburb names (1990–2026) | 7,220 |
| … last 5 years | 4,265 |
| Postcodes | 751 |
| Council codes | 223 |
| No suburb recorded | 65,456 (~0.9%) |

The extra names come from old or renamed suburbs, spelling variants and small localities. Names are in capitals, and `SOUTH COOGEE` is separate from `COOGEE`. To find variants:

```python
df[df["suburb"].str.contains("COOGEE", na=False)]["suburb"].value_counts()
```

---

### 40

> **Martin:** data wrangler just shows coogee even though i just run "df"

**Claude:** `df` only holds Coogee because it was loaded with `filters=[("suburb", "==", "COOGEE")]`. To load everything:

```python
df = pd.read_parquet("NSW_property_sales_1990_2026.parquet")   # ~7.4M rows, ~3 GB
```

Data Wrangler will struggle with 7.4M rows. Load or slice what you need instead:

```python
df = pd.read_parquet("NSW_property_sales_1990_2026.parquet",
                     filters=[("suburb", "in", ["COOGEE", "SOUTH COOGEE", "CLOVELLY", "RANDWICK"])])
df = pd.read_parquet("NSW_property_sales_1990_2026.parquet",
                     filters=[("postcode", "==", "2034")])

nsw = pd.read_parquet("NSW_property_sales_1990_2026.parquet")
view = nsw[(nsw["suburb"] == "BONDI") & (nsw["contract_date"] >= pd.Timestamp("2020-01-01").date())]
view
```

---

### 41

> **Martin:** split the parquet file into 3, 1990-1999, 2000-2009, 2010-2026

**Claude:** Split by contract year. 3,517 sales with missing or impossible contract dates were placed by their source file's year.

| File | Sales | Size |
|---|---|---|
| `NSW_property_sales_1990_1999.parquet` | 1,792,992 | 53 MB |
| `NSW_property_sales_2000_2009.parquet` | 2,169,187 | 67 MB |
| `NSW_property_sales_2010_2026.parquet` | 3,416,824 | 109 MB |

---

### 42

> **Martin:** split the parquet file into 4: 1990-1999, 2000-2009, 2010-2019, 2020-2026

**Claude:**

| File | Sales | Size |
|---|---|---|
| `NSW_property_sales_1990_1999.parquet` | 1,792,992 | 53 MB |
| `NSW_property_sales_2000_2009.parquet` | 2,169,187 | 67 MB |
| `NSW_property_sales_2010_2019.parquet` | 2,045,575 | 66 MB |
| `NSW_property_sales_2020_2026.parquet` | 1,371,249 | 44 MB |
| **Total** | **7,379,003** | |

The old `2010_2026` file is replaced by the last two and can be deleted.

---

### 43

> **Martin:** if i have multiple parquet files in a folder how does "df" know which one to open

**Claude:** `df` is just a variable name; the file is whatever you name inside `read_parquet()`, and each assignment replaces it.

```python
recent   = pd.read_parquet("NSW_property_sales_2020_2026.parquet")
nineties = pd.read_parquet("NSW_property_sales_1990_1999.parquet")

df = pd.read_parquet("parquet_files/", filters=[("suburb", "==", "COOGEE")])   # whole folder

files = ["NSW_property_sales_2010_2019.parquet", "NSW_property_sales_2020_2026.parquet"]
df = pd.concat([pd.read_parquet(f, filters=[("suburb", "==", "COOGEE")]) for f in files])
```

Don't keep the combined 1990–2026 file in the same folder as the split files if you read the whole folder, or every sale loads twice.

---

### 44

> **Martin:** what do i type to open NSW_property_sales_1990_2026.parquet

**Claude:**

```python
import pandas as pd
df = pd.read_parquet("NSW_property_sales_1990_2026.parquet")
len(df)   # 7,379,003 — ~10 s, ~3 GB RAM

# if "file not found":
df = pd.read_parquet(r"Q:\User Data\Martin\Misc\NSW Property Data\NSW_property_sales_1990_2026.parquet")

# just part of it:
df = pd.read_parquet("NSW_property_sales_1990_2026.parquet",
                     filters=[("suburb", "==", "COOGEE")])
```

---

### 45

> **Martin:** markdown this chat

**Claude:** Saved a condensed Markdown record of the chat (`NSW_property_sales_chat.md`).

---

### 46

> **Martin:** markdown the chat including my questions

**Claude:** This file: every question quoted as typed, with the answers condensed.

---

## Files produced

| File | Contents |
|---|---|
| Claude Sheet: *Coogee House Sales Nov 2023 – Nov 2026* | 156 web-scraped Coogee house sales plus a summary |
| `NSW_property_sales_<YEAR>.xlsx` (1990–2026) | One Excel workbook per year of NSW sales |
| `NSW_property_sales_1990_2026.parquet` | All 7,379,003 sales combined |
| `NSW_property_sales_1990_1999` / `2000_2009` / `2010_2019` / `2020_2026.parquet` | The same data split into four periods |

*Data: NSW Valuer General bulk Property Sales Information, CC BY-NC-ND 4.0.*
