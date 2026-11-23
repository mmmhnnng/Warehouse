# Chat record: estimating bedrooms and bathrooms from land size and BASIX

*NSW Property Analysis project · 23 November 2026*

---

## Martin

> based on the parquet data files how accurately could you estimate number of rooms and bathrooms etc based on land size?

## Claude

The parquet files themselves can't tell you how accurate this would be. They come from Valuer General sales data, which has price, dates, land area, zoning and Lot/DP but no bedroom or bathroom counts. With nothing to compare against, any estimate based on land size alone can't be checked. (The parquet files from the earlier sessions also aren't in this workspace, but they'd lead to the same answer.)

**What I'd expect if we had the answers to check against**, based on how Sydney housing typically works rather than on your data:

- **Houses:** land size is a weak predictor. A 450 m² lot in Marrickville could hold a 2-bed cottage or a 5-bed knockdown-rebuild. A model using only land size would mostly guess 3 bedrooms and get the exact count right maybe 40–50% of the time, and land within one bedroom maybe 80% of the time. Bathrooms would be worse, because renovations change them independently of the lot.
- **Terraces (<200 m²)** are the most predictable group, usually 2–3 bed with 1–2 bath.
- **Units:** this approach mostly doesn't work. Strata lot area is recorded for only about 30% of sales, and it often includes car spaces and courtyards.

**What would make it work:**

1. **Get some real counts to check against.** BASIX certificates (bedrooms and floor area by Lot/DP) or a few hundred manual Domain lookups would let us measure accuracy properly rather than guess.
2. **Use better inputs than land size.** Price per m² against the suburb median, lot shape and frontage from the cadastre, and especially **building footprint from Microsoft footprints or NSW LiDAR**. Floor area predicts bedrooms far better than land does.
3. **Report ranges** like "3–4 bed, likely 3" rather than a single number.

With footprint, price and suburb included, you could realistically expect about 60–70% exact on bedrooms for houses. That's good enough for comparing segments, but not for valuing individual properties.

If you re-attach the parquet files or link the folder they're in, I can check how land size relates to price and footprint. I'd also need a labelled sample to measure the real accuracy.

---

## Martin

*Attached: `basix-single-dwelling-certificates-2011-2020.xlsx`, `basix-multi-dwelling-certificates-2011-2020.xlsx`, `sydney_inner_west_sales_1990_2026.parquet`*

> i have BASIX data here, can you use this to estimate bedrooms, bathrooms etc

## Claude

I used the BASIX data to estimate bedrooms for 77,478 Inner West house sales from 2001 onwards. I couldn't estimate bathrooms: neither BASIX file has a bathroom count.

**How accurate it is.** I tested the model on 3,400 BASIX certificates from Inner West, Canada Bay, Burwood and Strathfield. It doesn't see a certificate's own answer when predicting it.

| What the model uses | Exact | Within ±1 bedroom |
|---|---|---|
| Nothing (always guess 4) | 40% | 90% |
| Land area | 49% | 93% |
| Land area + suburb (**used for the sales**) | 52% | 94% |
| + floor area and storeys | 57% | 96% |

Land size helps, but not by much. Floor area adds only about 4 points.

**The main catch:** BASIX only covers homes built or rebuilt between 2011 and 2020, so the model has learned what gets built on a lot today. Older terraces and cottages on the same lot size probably have fewer bedrooms. For 350–600 m² lots the model mostly says 4 bedrooms, where many existing homes are likely 3. So treat the estimates as probably on the high side until we check them against Census bedroom counts by dwelling type.

**Other limits:**

- BASIX records suburb but not address or Lot/DP, so I couldn't match certificates to individual sales. The model learns patterns by suburb and lot size instead.
- **Units:** I didn't estimate bedrooms for individual unit sales. Strata lot area is recorded for only about 30% of them and often includes balconies and car spaces. The multi-dwelling file does give typical sizes for new units: about 83 m² for a 2-bed, 137 m² for a 3-bed and 187 m² for a 4-bed. In new developments in these councils plus the City of Sydney, 43% of units are 1-bed (this share includes studios and boarding-house rooms) and 46% are 2-bed.
- About 12% of house sales have no land area recorded, so they get no estimate.

For each sale the file gives the most likely bedroom count, a likely range, the average and the probability of each count. I've saved the method and these caveats to the project as `basix_bedroom_model.md`.

*Delivered: `inner_west_houses_bedroom_estimates.csv`*

---

## Martin

> let's say you use the BASIX to make an estimate of each property in the parquet file, and I slowly input accurate data points for property attributes, can you slowly and dynamically improve estimation?

## Claude

Yes. The BASIX estimate becomes the starting guess for each property, and each accurate data point you give me does two things:

1. **That property is fixed.** Its estimate is replaced with your figure.
2. **Similar properties get corrected.** Each data point shows how far off the starting guess was for that kind of property. I'd learn a correction by lot size and suburb, and keep it modest until there are enough data points to support it.

**How it would improve as data comes in** (the counts are rough):

| Data points | What it can learn |
|---|---|
| ~30–50 | The overall correction. The biggest early gain is fixing BASIX's lean toward new builds; a 450 m² cottage is likely 3 bed, not 4. |
| ~200–500 | Corrections by lot size and by housing type (terraces vs cottages vs rebuilds) |
| ~1,000+ | A model trained on your data directly, with the BASIX estimate as just one input. It can then use **sale price**, which BASIX doesn't have: a house that sold well above similar lots in its suburb was probably extended. |
| Per suburb | Corrections only kick in for suburbs with enough of their own data points |

**A few extras:**

- **Bathrooms and car spaces** have no BASIX starting point. They'd start as rough guesses based on bedrooms and lot size, and become useful once you've given me a few hundred of each.
- **Terrace rows and subdivisions** were often built identically on the same deposited plan, so one data point can partly fill in its neighbours.
- **I'd report accuracy after each batch**, tested on data points the model hasn't seen, so you can see whether it's actually improving.
- **I can suggest which properties to look up next.** The most useful are the ones where the model is least sure, or in lot sizes and suburbs you haven't covered yet.

**One risk: what you look up shapes what it learns.** If most of your data points come from recent listings, which tend to be renovated or extended homes, the corrections will lean that way. A mix of property types and sale years avoids this.

**In practice:**

- **Adding data:** paste lines like "12 Smith St Marrickville: 3 bed, 2 bath, 1 car", or upload a CSV. I'd match each one to its property and add it to a running data-point file.
- **Keeping it between sessions:** this session's workspace is temporary, so I'd save the data-point file and the model notes to the project. In a new session you'd need to re-attach the parquet and BASIX files. Alternatively, link a folder on your computer and I can keep everything there.

Want me to set this up now? I'd create the data-point file and the update script, then you can start with your first batch.

---

## Martin

> markdown this chat

## Claude

I've written up this chat as a markdown file: your three questions, the answers, and the accuracy and BASIX results tables. It isn't word-for-word: the answers are lightly condensed and reorganised under a heading for each question.

---

## Martin

> markdown the chat including my questions

## Claude

This file: the full chat with your questions quoted word for word.
