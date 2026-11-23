# Estimating bedrooms and bathrooms for NSW property sales: chat record

*NSW Property Analysis project · 23 November 2026*

---

## 1. How accurately can rooms be estimated from land size?

**Question:** Based on the parquet data files, how accurately could you estimate number of rooms and bathrooms etc. based on land size?

**Answer:**

The parquet files can't answer this on their own. They come from Valuer General sales data: price, dates, land area, zoning and Lot/DP, but **no bedroom or bathroom counts**. With nothing to compare against, a land-size-only estimate can't be checked.

Expected accuracy if we had actual counts to compare against (general Sydney patterns, not measured):

- **Houses:** land size is a weak predictor. A 450 m² Marrickville lot could hold a 2-bed cottage or a 5-bed rebuild. A land-only model would mostly guess 3 bed: about 40–50% exactly right, about 80% within ±1. Bathrooms would be worse.
- **Terraces (<200 m²)** are the most predictable group, usually 2–3 bed with 1–2 bath.
- **Units:** this approach mostly doesn't work. Strata lot area is recorded for only about 30% of sales and often includes car spaces and courtyards.

What would make it work:

1. Get real counts to check against: BASIX certificates or a few hundred manual lookups.
2. Use better inputs: price relative to the suburb, lot shape and frontage from the cadastre, and especially **building footprint** (Microsoft building footprints or NSW LiDAR).
3. Report ranges like "3–4 bed, likely 3" rather than a single number.

Rough ceiling with footprint, price and suburb included: about 60–70% exact for house bedrooms. That's good enough for comparing segments, but not for valuing individual properties.

---

## 2. Using BASIX data to estimate bedrooms

**Files supplied:**

- `basix-single-dwelling-certificates-2011-2020.xlsx` (299,019 rows)
- `basix-multi-dwelling-certificates-2011-2020.xlsx` (36,014 projects)
- `sydney_inner_west_sales_1990_2026.parquet` (349,867 rows)

### What BASIX contains

- Bedrooms, site area, floor area, storeys and dwelling type (Separate House / Attached Dwelling / Single Unit).
- **No address or Lot/DP**, only suburb, postcode and LGA, so certificates can't be linked to individual sales.
- **No bathroom count**, so bathrooms can't be estimated from this data.

### House model

- **Training data:** 30,007 single-dwelling certificates from 18 inner-ring LGAs. Kept Separate House and Attached Dwelling; dropped floor area <80 m² (granny flats); site area 60–5,000 m²; bedrooms capped at 6+.
- **Testing:** 5-fold cross-validation on 3,400 Inner West, Canada Bay, Burwood and Strathfield certificates. The model never sees a certificate's own answer when predicting it.

| What the model uses | Exact | Within ±1 | Avg error (bedrooms) |
|---|---|---|---|
| Nothing (always guess 4) | 39.7% | 89.8% | 0.71 |
| Land area only | 48.8% | 93.0% | 0.59 |
| Land + suburb/LGA (**used for the sales**) | 52.4% | 94.1% | 0.54 |
| + attached/detached | 53.2% | 94.3% | 0.53 |
| + floor area | 56.1% | 96.1% | 0.48 |
| + storeys | 56.8% | 96.0% | 0.47 |

Land size helps modestly. Floor area adds about 4 points.

### Applied to Inner West house sales

- 77,478 clean Torrens sales from 2001 on (48,904 properties). About 12% of Torrens sales have no land area and get no estimate.
- Average predicted bedrooms by lot size: **<200 m² 3.0 · 200–350 m² 3.7 · 350–600 m² 4.2 · 600+ m² 4.5**.
- Output: `inner_west_houses_bedroom_estimates.csv`, with columns `bed_likely`, `bed_low`, `bed_high`, `bed_expected` and `p_bed1` … `p_bed6+`.

### Main caveat: new-build bias

BASIX covers only homes built or rebuilt in 2011–2020, so the model has learned what gets built on a lot *today*. Older terraces and cottages on the same lot likely have fewer bedrooms, so the estimates probably run high (e.g. 4 predicted where many existing homes are 3). They haven't yet been checked against Census bedroom counts by dwelling type (ABS TableBuilder).

### Units (multi-dwelling certificates)

- Bedroom mix of new units in Inner West, Canada Bay, Burwood, Strathfield and City of Sydney: **1-bed 43%, 2-bed 46%, 3-bed 10%, 4-bed 1.5%**. The 1-bed share includes studios and boarding-house rooms.
- Typical floor area per new unit (Sydney metro): **2-bed ~83 m², 3-bed ~137 m², 4-bed ~187 m²**. 1-bed figures are distorted by studios (~45 m² estimated).
- Not applied to individual unit sales: strata lot area is sparse (~30%), often includes balconies and car spaces, and there's nothing to check the estimates against.

The method was saved to the project as `claude/basix_bedroom_model.md`.

---

## 3. Improving the estimates as accurate data points come in

**Question:** If you use BASIX to make an estimate for each property, and I slowly input accurate data points, can you slowly and dynamically improve the estimates?

**Answer:** Yes. The BASIX estimate becomes the starting guess, and each accurate data point:

1. **Fixes that property:** its estimate is replaced with the actual figure.
2. **Corrects similar properties:** each data point shows how far off the starting guess was for that kind of property. Corrections are learned by lot size and suburb, and kept modest until there are enough data points to support them.

### How it improves as data comes in (rough counts)

| Data points | What it can learn |
|---|---|
| ~30–50 | The overall correction. The biggest early gain is fixing the new-build lean (a 450 m² cottage → 3 bed, not 4). |
| ~200–500 | Corrections by lot size and by housing type (terraces vs cottages vs rebuilds) |
| ~1,000+ | A model trained on the data points directly, with the BASIX estimate as one input. It can add **sale price** (a house selling well above similar lots in its suburb was probably extended). |
| Per suburb | Corrections only kick in for suburbs with enough of their own data points |

### Extras

- **Bathrooms and car spaces:** no BASIX starting point. They'd start as rough guesses from bedrooms and lot size, and become useful after a few hundred data points each.
- **Terrace rows and subdivisions:** properties on the same deposited plan were often built identically, so one data point partly fills in its neighbours.
- **Accuracy reporting:** after each batch, tested on data points the model hasn't seen.
- **What to look up next:** suggestions focus on the properties where the model is least sure, or on lot sizes and suburbs not yet covered.

### Risk: what gets looked up shapes what it learns

If most data points come from recent listings, which tend to be renovated or extended homes, the corrections will lean that way. A mix of property types and sale years avoids this.

### In practice

- **Adding data:** paste lines such as "12 Smith St Marrickville: 3 bed, 2 bath, 1 car", or upload a CSV. Each is matched to its property and added to a running data-point file.
- **Keeping it between sessions:** the session workspace is temporary, so the data-point file and model notes would be saved to the project. New sessions need the parquet and BASIX files re-attached, or a folder on your computer linked to keep everything there.

**Next step offered:** set up the data-point file and update script, then start with the first batch.

---

### Source

- ABS / .id community profile, Inner West dwelling types (2021): <https://profile.id.com.au/inner-west/dwellings>
