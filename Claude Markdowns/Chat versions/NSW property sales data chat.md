# Loading and viewing NSW sales data in pandas: chat record (23 Nov 2026)

Project: **NSW Property Analysis** · File: `NSW_property_sales_1990_2026.parquet` · Tools: VS Code, Jupyter notebook, Data Wrangler

---

## 1

**Martin:**

> breakdown
>
> ```python
> import pandas as pd
>
> df = pd.read_parquet("NSW_property_sales_1990_2026.parquet")
>
> df
> ```

**Claude:**

I didn't get access to the PyCharmMiscProject folder, so I couldn't open the parquet file. Options:

1. Add the folder that holds the file using "Add folder" in the desktop app.
2. Attach the parquet file to the chat. It's large, so this may be slow.
3. Paste a summary from your session:

```python
print(df.shape)
df.info()
print(df.describe(include="all").T)
print(df.head(10).to_string())
```

From the project notes: some `contract_date` values are invalid (e.g. years 0015 and 2031), suburb names need cleaning before matching, and Sydney is split into four regions by postcodes 2000–2234.

Planned breakdown: columns and data types, missing values and invalid dates, sales volume by year, median prices over time, property types, top suburbs, and a comparison of the four regions.

---

## 2

**Martin:** do i need all 3 lines to tell Python which parquet file to open

**Claude:**

No. Only the middle line opens the file:

```python
df = pd.read_parquet("NSW_property_sales_1990_2026.parquet")
```

- `import pandas as pd` loads pandas. It doesn't pick the file, but you need it so that `pd` exists before you call `pd.read_parquet`.
- `df` on its own just displays the table. It only shows output in a notebook or console; in a `.py` script, use `print(df)`.

Python looks for the file in the folder the script runs from. Otherwise give a full path, e.g. `pd.read_parquet(r"C:\Users\you\Downloads\NSW_property_sales_1990_2026.parquet")`. The `r` stops Windows backslashes from being misread.

---

## 3

**Martin:** what does the first line do?

**Claude:**

`import pandas as pd` loads the pandas library so your script can use it.

- `import pandas` brings in pandas, an add-on library for working with tables of data.
- `as pd` gives it a short nickname, so you write `pd.read_parquet(...)` instead of `pandas.read_parquet(...)`.

Without it you get `NameError: name 'pd' is not defined`. If you get `ModuleNotFoundError: No module named 'pandas'`, install it with `pip install pandas pyarrow`. Pandas needs `pyarrow` to read parquet files.

---

## 4

**Martin:** so i do need the first line to load pandas to be able to read the parquet file?

**Claude:**

Yes. `read_parquet` is part of pandas, so the import has to come before the line that reads the file. Other libraries like `pyarrow` or `polars` can read parquet files too, but they also need their own import line.

---

## 5

**Martin:** what does the second line do?

**Claude:**

It reads the file and stores its contents in memory as a table.

- `pd.read_parquet(...)` opens a parquet file and turns it into a DataFrame.
- `"NSW_property_sales_1990_2026.parquet"` is the file to open.
- `df =` saves the table under the name `df`. Without it, the data would be loaded and then lost straight away. The name is just a convention; `sales =` would work the same.

Later changes to `df` don't touch the file on disk.

---

## 6

**Martin:** what does the last line do?

**Claude:**

`df` shows the table on screen; it doesn't change anything. In Jupyter or the interactive console, a bare variable name prints its contents. For a large table, pandas shows the first and last 5 rows with `...` in between, and a count like `[1234567 rows x 12 columns]`.

In a normal `.py` script a bare `df` does nothing; use `print(df)`. Alternatives: `df.head(20)` or `df.info()`.

---

## 7

**Martin:** how do i specify which suburbs to open in parquet file?

**Claude:**

Filter while reading:

```python
df = pd.read_parquet(
    "NSW_property_sales_1990_2026.parquet",
    filters=[("suburb", "in", ["BONDI", "COOGEE", "RANDWICK"])]
)
```

For one suburb: `filters=[("suburb", "==", "BONDI")]`. This uses less memory than loading the whole file.

Or load everything, then filter:

```python
df = df[df["suburb"].isin(["BONDI", "COOGEE", "RANDWICK"])]
```

Names must match exactly. Check the column name with `print(df.columns)` and the exact spellings with `print(sorted(df["suburb"].unique()))`.

---

## 8

**Martin:** explain the syntax here `filters=[("suburb", "in", ["BONDI", "COOGEE", "RANDWICK"])]`

**Claude:**

Read it from the outside in:

1. `filters=` is a named argument to `read_parquet`.
2. `[ ... ]`, the outer square brackets, make a list of conditions.
3. `( ... )`, the round brackets, make a tuple of three parts: the column (`"suburb"`), the comparison (`"in"`; others include `"=="`, `"!="`, `">"`, `"<"`, `">="`, `"<="`, `"not in"`), and the value to compare against.
4. `["BONDI", "COOGEE", "RANDWICK"]` is a list of text values.

When you put several tuples in the list, a row must match all of them:

```python
filters=[
    ("suburb", "in", ["BONDI", "COOGEE"]),
    ("purchase_price", ">", 1_000_000),
]
```

Python ignores the underscores in `1_000_000`; they're there to make the number easier to read.

---

## 9

**Martin:** explain "in"

**Claude:**

`"in"` means "matches any value in this list." It's shorthand for several `"=="` checks joined by "or". `"not in"` does the opposite.

- The value must be a list, even for one item: `["BONDI"]`.
- The match is exact. `"BONDI"` doesn't match `"Bondi"` or `"BONDI BEACH"`.
- Python also has its own `in` keyword without quotes (`"BONDI" in my_list` gives `True` or `False`), which means the same idea.

---

## 10

**Martin:** how do i hide columns in data wrangler or rearrange?

**Claude:**

There's no view-only hide button. To remove columns, right-click a column header and choose **Drop column**, or use the **Drop column** or **Select column** operation. This only changes Data Wrangler's copy, not the file.

I couldn't find a reorder feature in Data Wrangler's documentation, so set the order in code:

```python
df = df[["suburb", "contract_date", "purchase_price", "area"]]
```

Or choose columns at load time:

```python
df = pd.read_parquet(
    "NSW_property_sales_1990_2026.parquet",
    columns=["suburb", "contract_date", "purchase_price"],
    filters=[("suburb", "in", ["BONDI", "COOGEE"])],
)
```

`columns=` doesn't reliably set the order, so add `df = df[[...]]` afterwards if the order matters.

---

## 11

**Martin:** so if this is my code below at the moment, how would you write it so it loads the columns in this order: contract_date, settlement_date, purchase_price, unit_no, house_no, street, suburb, postcode, council_code, area, area_unit, zoning, property_type, primary_purpose, strata_lot_no, legal_description, property_name, nature_code, property_id, sale_counter, dealing_number

> ```python
> import pandas as pd
>
> df = pd.read_parquet(
>     "NSW_property_sales_1990_2026.parquet",
>     filters=[("suburb", "in", ["BONDI", "COOGEE", "RANDWICK"])]
> )
>
> df
> ```

**Claude:**

```python
import pandas as pd

column_order = [
    "contract_date", "settlement_date", "purchase_price",
    "unit_no", "house_no", "street", "suburb", "postcode",
    "council_code", "area", "area_unit", "zoning",
    "property_type", "primary_purpose", "strata_lot_no",
    "legal_description", "property_name", "nature_code",
    "property_id", "sale_counter", "dealing_number",
]

df = pd.read_parquet(
    "NSW_property_sales_1990_2026.parquet",
    columns=column_order,
    filters=[("suburb", "in", ["BONDI", "COOGEE", "RANDWICK"])],
)

df = df[column_order]

df
```

- `column_order = [...]` stores the list once, so you don't have to type it twice.
- `columns=column_order` loads only those columns.
- `df = df[column_order]` puts them in exactly that order.

A misspelled name gives an error naming the missing column.

---

## 12

**Martin:** explain this line `df = df[column_order]`

**Claude:**

It means "make a new table using only these columns, in this order, and save it back as `df`."

- `df[column_order]`: square brackets after a table mean "pick from this table." A list of names returns those columns in list order.
- `df =` replaces the old table with the new one. Without it, the reordered table would be thrown away.

What you put in the brackets decides what you get:

- `df["suburb"]` gives one column.
- `df[["suburb", "postcode"]]` gives a table. The outer brackets mean "pick" and the inner pair makes the list.
- `df[column_order]` does the same with a list stored in a variable, so only one pair is needed.

---

## 13

**Martin:** does it make more sense logically to order code this way

**Claude:**

Yes. Imports, then settings, then load, then tidy, then show. Each step depends on the one before it, and Python runs top to bottom. I suggested moving the suburb list into the settings too:

```python
import pandas as pd

# Settings
suburbs = ["BONDI", "COOGEE", "RANDWICK"]

column_order = [ ... ]

# Load
df = pd.read_parquet(
    "NSW_property_sales_1990_2026.parquet",
    columns=column_order,
    filters=[("suburb", "in", suburbs)],
)

# Tidy
df = df[column_order]

df
```

Lines starting with `#` are comments; Python ignores them.

---

## 14

**Martin:** or does below make more sense (with `column_order` defined after `read_parquet`)

**Claude:**

No, that version won't work. When Python reaches `columns=column_order`, `column_order` doesn't exist yet, and you get `NameError: name 'column_order' is not defined`.

In Jupyter it might appear to work if `column_order` was defined in an earlier run, because Python remembers variables between runs. Then it breaks the next time you start fresh.

---

## 15

**Martin:** explain this line (the multi-line `read_parquet` call)

**Claude:**

It's one statement over several lines. Python knows it continues because the round bracket hasn't been closed yet.

- `df =` stores the result.
- `pd.read_parquet(` calls the function. Everything up to the closing `)` is the arguments, separated by commas.
- `"NSW_property_sales_1990_2026.parquet",` is the file. It isn't labelled, because the file always comes first.
- `columns=column_order,` says which columns to load.
- `filters=[...],` says which rows to load.
- The comma after the last argument is optional.

The labelled arguments can go in any order; the file name has to come first.

---

## 16

**Martin:** doesnt the "columns=column_order" argument in this line already define column order? why do i still need this line "df = df[column_order]"?

**Claude:**

You often won't need it. `columns=` is documented as choosing which columns to load, not their order. pyarrow usually returns them in the order you list, but the pandas docs don't promise it. The extra line is a cheap guarantee and makes your intent clear.

To check on your setup, remove the line and run `print(list(df.columns) == column_order)`.

---

## 17

**Martin:** is there a quick way to wrap data wrangler column widths?

**Claude:**

I couldn't find a wrap-text or auto-fit option in Data Wrangler's documentation. Workarounds:

- Drag a column header edge to resize.
- Check the settings: press `Ctrl + ,` and search "Data Wrangler".
- Print a long value in full: `print(df["legal_description"].iloc[0])`.
- Drop wide columns you don't need.

`Alt + Z` word wrap only works in the code editor. Exporting with `df.to_csv(...)` and opening the file in Excel lets you use Wrap Text.

---

## 18

**Martin:** instead of resizing manually by hand

**Claude:**

Try double-clicking a column header edge (common in grids, but I couldn't confirm it for Data Wrangler). Otherwise:

Jupyter, with wrapped text:

```python
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)
df.head(50).style.set_properties(**{"white-space": "pre-wrap"})
```

Excel, with widths set automatically:

```python
with pd.ExcelWriter("bondi_sales.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, index=False)
    sheet = writer.sheets["Sheet1"]
    for col in sheet.columns:
        longest = max(len(str(cell.value or "")) for cell in col)
        sheet.column_dimensions[col[0].column_letter].width = min(longest + 2, 50)
```

---

## 19

**Martin:** can I add finance accounting format to a cell for money figures?

**Claude:**

Data Wrangler has no cell formatting.

Jupyter (display only):

```python
df.head(50).style.format({"purchase_price": "${:,.0f}"})
```

Excel accounting format, added inside the `with` block:

```python
    accounting = '_-$* #,##0_-;-$* #,##0_-;_-$* "-"_-;_-@_-'
    price_col = df.columns.get_loc("purchase_price") + 1
    for row in sheet.iter_rows(min_row=2, min_col=price_col, max_col=price_col):
        for cell in row:
            cell.number_format = accounting
```

The cells stay real numbers in Excel.

---

## 20

**Martin:** how do i add this to existing code?

**Claude:**

I gave the full script with an `output_file` setting and an `# Export to Excel` block after the tidy step, with auto-fit widths (`longest + 4`) and the accounting format. Close the file in Excel before running, or you get `PermissionError`. If you get `No module named 'openpyxl'`, run `pip install openpyxl`.

---

## 21

**Martin:** what is the export to excel step?

**Claude:**

It saves `df` as an Excel file and tidies how it looks:

- `with pd.ExcelWriter(...) as writer:` opens a new Excel file, and saves and closes it automatically when the indented block ends.
- `df.to_excel(writer, index=False)` writes the table without pandas' row numbers.
- `sheet = writer.sheets["Sheet1"]` gets the worksheet.
- The auto-fit loop sizes each column to its longest value plus 4, capped at 50.
- The accounting loop applies the format to every price cell, skipping the header row. Pandas counts columns from 0 and Excel from 1, hence the `+ 1`.

---

## 22

**Martin:** do i take this out if i dont want to write it to excel?

**Claude:**

Yes. Delete the whole export block and the `output_file` setting, and keep `df` at the end. Or comment the block out with `Ctrl + /`.

---

## 23

**Martin:** i meant how do i add auto-column width and accounting number formatting in VS Code / Jupyer notebook display only?

**Claude:**

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

- `accounting` shows prices as `$ 1,250,000`, negatives as `$ (5,000)`, zero as `$ -`, and missing values as blank.
- `head(100)`: pandas won't style more than about 262k cells, roughly 12k rows with 21 columns.
- `nowrap` lets columns size to their contents, `text-align: right` lines up prices, and `.hide(axis="index")` hides row numbers.

To format every number in every table: `pd.set_option("display.float_format", "${:,.0f}".format)`. This also affects `postcode` and `area`.

---

## 24

**Martin:** *(screenshot of the VS Code notebook showing 57,750 rows × 21 cols)* so where do i paste this code?

**Claude:**

In a new cell below your current one: click **+ Code**, paste, and run with `Shift + Enter`. This way you load once and can re-run the display as often as you like.

The styled output is a plain HTML table, without pages or the Data Wrangler link. Keep `df` in the first cell if you still want the interactive viewer.

The screenshot showed some bad values: prices of `0` (rows 7–8), and contract dates of `1024-01-29` and `1900-01-01` (likely a placeholder for unknown).

---

## 25

**Martin:** can i not add this to main code?

**Claude:**

Yes. Replace the final `df` with the display block, and put the `accounting` function near the top. One cell is simpler but reloads the file each time (about 1.2 s); two cells let you load once.

---

## 26

**Martin:** what's this "rows_to_show = 100"

**Claude:**

It's a setting I added that controls how many rows `df.head(rows_to_show)` displays. It only affects what's shown, not the data. Writing `df.head(100)` directly works the same.

---

## 27

**Martin:** remove this setting

**Claude:**

Gave the full code again with `df.head(100)` written directly.

---

## 28

**Martin:** what is the last block for? *(the `# Display` block)*

**Claude:**

It controls how the table looks when displayed; it doesn't change the data. It's a chain, where each line works on the result of the line above:

- `df.head(100)` takes the first 100 rows.
- `.style` switches to display mode.
- `.format(...)` applies the price format.
- `nowrap` keeps text on one line.
- The right-align line applies to `purchase_price` only.
- `.hide(axis="index")` hides row numbers.

`**{...}` unpacks the dictionary into named settings.

---

## 29

**Martin:** so i can remove this?

**Claude:**

Yes. Put `df` back as the last line and delete the `accounting` function too. You get the interactive viewer back, without the `$` formatting.

---

## 30

**Martin:** how do i set the auto-column width and accounting formatting for data wrangler? or can i not

**Claude:**

As far as I can tell, you can't. Data Wrangler has no number formatting or auto-fit. The workaround is a separate formatted text column:

```python
df["price_display"] = df["purchase_price"].map(
    lambda x: "" if pd.isna(x) else f"${x:,.0f}"
)
```

It's text, so it sorts alphabetically (`$900,000` after `$1,200,000`) and you can't do maths with it. Keep `purchase_price` for sorting and filtering.

---

## 31

**Martin:** how do i implement this to the code?

**Claude:**

Add this after the tidy step:

```python
df.insert(
    df.columns.get_loc("purchase_price") + 1,
    "price_display",
    df["purchase_price"].map(lambda x: "" if pd.isna(x) else f"${x:,.0f}"),
)
```

`df.insert` takes the position (right after `purchase_price`), the name, and the values. `column_order` stays unchanged. Running it twice without reloading gives `ValueError: cannot insert price_display, already exists`.

---

## 32

**Martin:** how do i replace the price column with the formatted column?

**Claude:**

```python
df["purchase_price"] = df["purchase_price"].map(
    lambda x: "" if pd.isna(x) else f"${x:,.0f}"
)
```

The column keeps its name and position. It becomes text: sorting goes alphabetically, maths and numeric filters fail, and the original numbers are gone until you reload. Do any analysis before this step.

---

## 33

**Martin:** show the full code

**Claude:**

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

# Format purchase_price as currency text
df["purchase_price"] = df["purchase_price"].map(
    lambda x: "" if pd.isna(x) else f"${x:,.0f}"
)

df
```

---

## 34

**Martin:** does this pseudo code make more sense? `# Replace purchase-price column with currency formatted column`

**Claude:**

That's a comment rather than pseudocode, and yes, it's clearer because it says the column is being replaced. Suggested tweak:

```python
# Replace purchase_price with currency-formatted text (no longer numeric)
```

The underscore matches the real column name, and "(no longer numeric)" warns that sorting and maths won't work after this line.

---

## 35

**Martin:** why is the purchase_price column inherently right aligned?

**Claude:**

Because it holds numbers. Viewers right-align number columns and left-align text; the `#` icon marks a numeric column. Right-aligning lines digits up by place value, so bigger numbers stick out further left:

```
 2100000
  950000
   27750
    5000
```

Excel does the same. Once `purchase_price` is converted to text, it will be left-aligned.

---

## 36

**Martin:** markdown this chat

**Claude:** Wrote a summary record to `pandas_parquet_chat_2026-11-23.md` and saved a copy to the project.

## 37

**Martin:** markdown the chat including my questions

**Claude:** Rewrote this file as a question-by-question record, with each question as written and the answers given.
