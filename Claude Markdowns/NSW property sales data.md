# Loading and viewing NSW sales data in pandas: chat record (23 Nov 2026)

Project: **NSW Property Analysis** · File: `NSW_property_sales_1990_2026.parquet` · Tools: VS Code, Jupyter notebook, Data Wrangler

---

## Final code

```python
import pandas as pd

# Settings
suburbs = ["BONDI", "COOGEE", "RANDWICK"]

column_order = [
    "contract_date", "settlement_date", "purchase_price",
    "unit_no", "house_no", "street", "suburb", "postcode",
    "council_code", "area", "area_unit", "zoning",
    "property_type", "primary_purpose", "strata_lot_no",
    "legal_description", "property_name", "nature_code",
    "property_id", "sale_counter", "dealing_number",
]

# Load
df = pd.read_parquet(
    "NSW_property_sales_1990_2026.parquet",
    columns=column_order,
    filters=[("suburb", "in", suburbs)],
)

# Tidy
df = df[column_order]

# Replace purchase_price with currency-formatted text (no longer numeric)
df["purchase_price"] = df["purchase_price"].map(
    lambda x: "" if pd.isna(x) else f"${x:,.0f}"
)

df
```

Result in the screenshot: 57,750 rows × 21 columns. The screenshot was taken before the formatting step was added.

---

## 1. Breakdown request

- Asked for a breakdown of the parquet file. It wasn't in the session workspace, and access to the PyCharmMiscProject folder was declined.
- Alternatives offered: add the folder, attach the file, or paste the output of `df.shape`, `df.info()`, `df.describe(include="all")` and `df.head()`.
- Planned breakdown: columns and data types, missing values and invalid dates, sales volume by year, median prices over time, property types, top suburbs, and a comparison of the four regions.

## 2. The three starting lines

- **`import pandas as pd`** loads the pandas library and gives it the short name `pd`. It's required: `read_parquet` belongs to pandas, and without the import you get `NameError: name 'pd' is not defined`. To install: `pip install pandas pyarrow`.
- **`df = pd.read_parquet("...")`** reads the file into an in-memory table (a DataFrame) and saves it as `df`. Changes to `df` don't touch the file. Use a full path such as `r"C:\...\file.parquet"` if the file isn't in the folder the script runs from.
- **`df`** displays the table. It only works in a notebook or console; in a `.py` script, use `print(df)`. You can swap it for `df.head(20)` or `df.info()`.

## 3. Choosing suburbs

```python
filters=[("suburb", "in", ["BONDI", "COOGEE", "RANDWICK"])]
```

- `filters=` is a named argument. The outer `[ ]` is a list of conditions, each `( )` is a tuple of (column, operator, value), and the inner `[ ]` is a list of values.
- Several tuples means every condition must match (AND).
- `"in"` keeps a row if its value matches any item in the list. `"not in"` does the opposite. Other operators: `==`, `!=`, `>`, `<`, `>=`, `<=`.
- Matches must be exact: `"BONDI"` doesn't match `"Bondi"` or `"BONDI BEACH"`. To see the exact spellings, run `sorted(df["suburb"].unique())`.
- Alternative: load everything, then filter with `df[df["suburb"].isin([...])]`.

## 4. Choosing and ordering columns

- `columns=column_order` loads only those columns. It's not documented to keep the order, though pyarrow usually does.
- `df = df[column_order]` guarantees the order. Square brackets with a list return those columns in list order, and `df =` saves the result.
- `df["x"]` gives one column; `df[["x", "y"]]` gives a table (outer brackets select, inner brackets make the list).
- To check the order: `list(df.columns) == column_order`.

## 5. Code order

- Python runs top to bottom, so a variable must be defined before it's used. Putting `column_order` after `read_parquet` gives `NameError`.
- In notebooks, an older definition from a previous run can hide this mistake until you restart.
- Layout used: imports, then settings, then load, then tidy, then display. `#` lines are comments.
- `read_parquet(...)` spans several lines because the open round bracket continues the statement. The file name is positional (it must come first); the named arguments can go in any order. A trailing comma after the last argument is optional.

## 6. Data Wrangler

- **Hide columns:** right-click a column header and choose **Drop column**, or use the **Select column** operation. There's no view-only hide.
- **Reorder:** no reorder operation found, so set the order in code.
- **Column width:** drag the header edge. No documented auto-fit or text wrap. VS Code's `Alt + Z` word wrap only works in the code editor.
- **Number formatting:** not supported. Workarounds: a formatted text column, a styled notebook table, or an Excel export.

## 7. Formatting options covered

**Styled notebook table (display only; prices stay numbers):**

```python
def accounting(x):
    if pd.isna(x):
        return ""
    if x == 0:
        return "$ -"
    if x < 0:
        return f"$ ({abs(x):,.0f})"
    return f"$ {x:,.0f}"

(
    df.head(100)
    .style
    .format({"purchase_price": accounting})
    .set_properties(**{"white-space": "nowrap"})
    .set_properties(subset=["purchase_price"], **{"text-align": "right"})
    .hide(axis="index")
)
```

- This is a chain: each line works on the result of the line above. `**{...}` unpacks display settings into named arguments.
- The output is a plain HTML table (no pages and no Data Wrangler link). Pandas styles at most about 262k cells by default, which is about 12k rows at 21 columns.
- Tried and then removed in favour of the plain `df` view.

**Excel export with auto-fit widths and accounting format:** used `pd.ExcelWriter(..., engine="openpyxl")`, sized each column to its longest value (`+ 4`, capped at 50), and applied the number format `'_-$* #,##0_-;-$* #,##0_-;_-$* "-"_-;_-@_-'` to the price column. Removed because no Excel file was wanted. The file must be closed in Excel before running, or you get `PermissionError`.

**Formatted text column next to the price:**

```python
df.insert(
    df.columns.get_loc("purchase_price") + 1,
    "price_display",
    df["purchase_price"].map(lambda x: "" if pd.isna(x) else f"${x:,.0f}"),
)
```

Replaced by overwriting `purchase_price` directly (see final code).

## 8. Effects of formatting `purchase_price` as text

- It sorts alphabetically, so `$900,000` comes after `$1,200,000`.
- Maths and numeric filters (`.mean()`, `> 1_000_000`) fail or give wrong results.
- Viewers left-align it. Number columns are right-aligned by default so that digits line up by place value; the `#` icon in the viewer marks a numeric column.
- Do any price sorting, filtering or calculations before the formatting step.

## 9. Data issues spotted in the screenshot

- Prices of `0` (rows 7–8).
- Bad contract dates: `1024-01-29`, and `1900-01-01`, which is likely a placeholder. This matches the invalid-date note in `region_definitions.md`.
- Filter these out before analysing prices.
