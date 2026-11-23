# NSW Property Analysis — chat record (23 Nov 2026)

Project: **NSW Property Analysis** · Data: four regional Valuer General sales files (City, Eastern Suburbs, Inner West, North Shore), plus BASIX certificate files.

---

## 1. Good value for houses and units, by region

**Method**
- Combined the four regional parquet files. Cleaning: residential (nature code R, current format), 2001 onwards, $30k–$40M, no multi-property dealings, address dedupe. Invalid contract dates replaced with settlement date minus 6 weeks.
- House = Torrens title; Unit = strata. Data runs to early Nov 2026, so "last 12 months" = Nov 2025 – Oct 2026.
- **Good value** = suburb's last-12-month median is below its region's median *and* 10-year growth (2015→2025 median) is at least the region's. Ranked by 40% cheapness + 35% 10-yr growth + 25% last-12m change (percentile ranks).
- **Trap** = below region median but 10-yr growth under 85% of the region's.
- Suburbs needed ≥15 sales in 2015, 2025 and the last 12 months.

**Region snapshot** (median last 12m · 10-yr growth · 12m change)

| Region | Houses | Land $/m² | Units | House ÷ unit |
|---|---|---|---|---|
| City | $2.23M · +64% · −2.8% | $19.6k | $955k · +31% · −5.0% | 2.3× |
| Eastern Suburbs | $3.84M · +84% · −2.8% | $14.3k | $1.42M · +65% · −2.0% | 2.7× |
| Inner West | $2.44M · +67% · −0.8% | $9.1k | $940k · +27% · +1.5% | 2.6× |
| North Shore | $3.52M · +84% · −4.3% | $5.1k | $1.22M · +53% · −0.4% | 2.9× |

**Cross-region**
- North Shore houses have the cheapest land (~$5k/m²) while matching the Eastern Suburbs' growth, and softened most this year.
- Eastern Suburbs and North Shore units grew roughly twice as fast as City and Inner West units. Large City/Inner West complexes grew ~2–3%/yr.
- Small strata (2–6 lots) grew about as fast as houses in every region (City +90%, ES +64%, IW +69%, NS +58% over 10 yrs), but cost $1.5–1.9M outside the City.

**Value picks** (median last 12m, 10-yr growth)

| Region | Houses | Units | Traps |
|---|---|---|---|
| City | Rosebery ($2.12M, +68%), Redfern ($2.13M, +63%) | Rosebery ($870k, +35%), Redfern ($935k, +61%), Alexandria ($950k, +45%) | Houses: Waterloo. Units: Ultimo, Chippendale, Potts Point, Surry Hills, Rushcutters Bay |
| Eastern Suburbs | Matraville ($2.70M, +84%), Chifley ($2.73M, +85%), Malabar ($3.26M, +96%), Paddington ($3.50M, +113%) | Randwick ($1.26M, +72%), Waverley ($1.20M, +71%) | Houses: Kingsford, Bondi Junction. Units: Kingsford, Kensington, Centennial Park, Paddington |
| Inner West | Sydenham ($1.80M, +83%), Tempe ($1.80M, +68%), Marrickville ($2.11M, +78%), Leichhardt ($2.14M, +78%), Hurlstone Park, Croydon Park, Dulwich Hill | Croydon Park ($810k, +35%), Ashfield ($910k, +32%); Dulwich Hill / Marrickville just above median (+47%) | Houses: St Peters, Erskineville, Newtown, Camperdown, Ashfield. Units: Homebush, Strathfield, Mortlake, Homebush West |
| North Shore | West Pymble ($2.78M, +93%), North Turramurra ($2.70M, +100%), Wahroonga ($2.62M, +92%), St Ives ($3.06M, +103%), Lane Cove West ($3.10M, +89%) | Wahroonga ($1.21M, +80%), North Sydney ($1.13M, +70%), Crows Nest ($1.22M, +67%), St Ives ($1.10M, +54%) | Houses: Neutral Bay, Chatswood West. Units: Gordon, Warrawee, Lane Cove, Turramurra |

**Caveats**
- Enfield units excluded: a 2025 run of new stock more than doubled the median; like-for-like rise is closer to +33%.
- Unit medians are sensitive to new-stock mix; 12-month changes on fewer than ~40 sales are noisy.
- Inner West unit 12-month change here is +1.5% vs +3.8% in the earlier Inner West findings (different window and unit count).
- Saved to the project as `regional_value_findings.md`.

---

## 2. Was this all from the parquet data?

Yes — every figure was calculated from the four uploaded parquet files; no web data was used.

Without the files, I could only have given a general view from my own knowledge (current to mid-2026) or stitched together published medians from Domain, Cotality or NSW Rent & Sales, which use different definitions and don't publish land $/m², strata-size splits or this four-region split. The raw data allowed consistent rules everywhere and measures nobody publishes. The source is the NSW Valuer General's free property sales records.

---

## 3. What extra data does Cotality (formerly CoreLogic) have over the Valuer General?

The Valuer General records each **sale** (price, dates, address, land area, zoning, strata lot, purpose, dealing number). Cotality adds a description of each **property** and its **market**:

- **Property:** bedrooms, bathrooms, car spaces, floor area, building type, year built, apartment floor size, photos and listing descriptions.
- **Market:** listings (asking price, days on market, vendor discounting, auction results), ~550k rental records a year, owner-occupier vs investor signals, hazard and climate-risk overlays.
- **Estimates and indices:** valuation estimates for every property, rental estimates, a mix-adjusted home value index, and earlier reporting (agents report at contract; Valuer General data arrives after settlement).

The Valuer General data is still the complete official record of every transfer, free and in bulk. Cheaper gap-fillers: NSW Rent & Sales Report for rents; Domain's API for bedrooms and listings (with limits).

---

## 4. Example: Cotality data for one property

**148 Wilson Street, Newtown** (from the free CommBank Property Insights page, which shows Cotality data):

| Field | Cotality (via CommBank) | NSW Valuer General |
|---|---|---|
| Property type | House | Torrens title, "Residence" |
| Beds / baths / car | 4 / 2 / 0 | — |
| Land area | 113 m² | 112.6 m² |
| Photos / floor plan | 66 photos, floor plan | — |
| Estimated value | $1.99M – $2.07M – $2.16M | — |
| Suburb stats | Median $1.9M, rent $1,000/wk | — |
| Sale history | not on free page | 13 Jul 2026 $2.2M; 21 May 2010 $1.2M |
| Legal / admin | — | Lot 2 DP1062358, zoned R1 |

**Cleaning issue found:** the 2010 sale is coded "Other" rather than "Residential", so it was dropped. About 13k house/unit-purpose sales (~2%) across the four regions are coded this way, mostly 2001–2014. Unlikely to move the medians much; can be added back.

---

## 5. Does CBA own or pay for Cotality?

CBA doesn't own it; it's a paying customer. Cotality is owned by US private equity firms **Stone Point Capital and Insight Partners**, who bought CoreLogic for ~US$6B in June 2021; renamed Cotality in 2025. The Australian business (RP Data) has been part of it since 2013. Banks typically pay for customer-facing data, valuation estimates for lending and loan-book revaluation, and full valuations. All the big four buy from Cotality in some form.

---

## 6. Cost of all NSW data from Cotality

No published price for state-wide bulk data — it's a negotiated enterprise licence. Public RP Data subscription prices:

| Plan (12-month) | Approx. price incl. GST | Exports/month |
|---|---|---|
| Lite, single state | ~$180/month (~$2.2k/yr) | 500 |
| Base | ~$220/month (~$2.6k/yr) | 2,000 |
| Premium, national | ~$250/month (~$3.0k/yr) | 10,000 |
| Top tier | ~$300/month (~$3.6k/yr) | 50,000 |

- NSW has 3M+ properties: even 50k/month would take ~5 years, and the licence doesn't allow building a bulk copy.
- Routes for whole-state data: enterprise licence or API feed (my rough guess: tens of thousands of dollars a year at least — get a quote), Cotality's academic programme (university only), or Domain / PropTrack.
- **Correction made:** PropTrack belongs to REA; Domain's data business is separate.

---

## 7. Don't REA and Domain have bedrooms, parking and floor plans for most properties?

Mostly yes — for properties that have been **listed** for sale or rent. Coverage is high for homes that sold or were rented since ~2010.

Gaps: never-listed properties; details frozen at the last ad (renovations missed); kitchens and layouts are in photos/text, not structured fields; floor plans are images; agent-entered data is inconsistent. Access: both sites ban scraping; proper access is through PropTrack or Domain's paid products. Cotality's attributes also come largely from the same listing feeds.

---

## 8. Free and easiest way to get bedrooms, parking, bathrooms and floor plans for all NSW properties

No single free source does this. Options:

- **Free, bulk, by area:** ABS Census (bedrooms, dwelling type, vehicles by small area); NSW rental bond data (rents by bedrooms by postcode).
- **Free, bulk, by property but rough:** NSW cadastre (lot boundaries); Microsoft building footprints (× storeys ≈ floor area).
- **Free, one at a time:** onthehouse.com.au, CommBank Property Insights, realestate.com.au, Domain; DA plans on the Planning Portal and council sites.
- **Cheapest proper property-level route:** RP Data Lite (~$180/month) for a shortlist; Domain's developer API (check current free-tier terms).

---

## 9. I want it specific to each individual property

Then there's no free option — property-level bedrooms, bathrooms, parking and floor plans exist only in listing data held by REA (PropTrack), Domain and Cotality. No government body collects bedroom counts or floor plans for individual homes.

- **Paid:** request quotes from all three for a cut-down extract (addresses from our sales data; beds, baths, car spaces, floor area, latest floor plan). Check storage/bulk-analysis rights. Academic route is cheaper if available.
- **Free, measuring the building not the rooms:** lot size (have), building footprint (Microsoft), height/storeys (NSW LiDAR), strata lot area (have for ~30% of unit sales). Could model bedrooms from floor area — an estimate, not a record.
- **Free by hand:** look up a shortlist of a few dozen properties.

---

## 10. Domain's API

`GET /v1/properties/{id}` returns bedrooms, bathrooms, property type, area, features, lot/plan number, address ID, photos from past ads, and sale history (dates, prices, days on market, agency). Car spaces appear in listing endpoints. Fields available depend on your "data access level".

- **Cost:** not published; 13 API packages; property-data packages set up via an account manager. Free plans exist in the terms; historically the free tier covered listings, agents, auction results and address lookup only. Call limits set by Domain.
- **Restrictions (API terms):** approved purpose only (cl. 3.1, 7.3); no derivative works without written consent (cl. 7.6(g)); data must stay in Australia (cl. 7.6(j)); delete on termination (cl. 16.5); no reselling or sharing (cl. 7.6(d)).
- Third-party "Domain scrapers" breach Domain's terms — avoid.
- Verdict: a legitimate, cheaper way to test on a few thousand sold properties; not a free route to all of NSW.

---

## 11. Could I scrape slowly and in stages? Through the website listings?

Going slowly doesn't change it: scraping breaches Domain's and REA's terms, and the public listing pages are exactly what those terms cover. Spreading requests out to avoid blocking is the kind of workaround the terms prohibit. Additional risks: copyright in floor plans and photos; Privacy Act exposure for large address-linked datasets; IP bans and fragile scrapers. Not legal advice. I declined to help build a scraper.

---

## 12. Does manually viewing pages and recording the data count?

Looking at listings and noting details for your own analysis is normal use.

- **Generally fine:** a shortlist (dozens to a couple of hundred) recorded in your own spreadsheet; facts like bedroom counts aren't copyright; viewing floor plans on screen.
- **Grey:** saving many floor plans/photos; large-scale manual collection (terms ban systematic collection however it's done); sharing or selling the data.
- Suggested workflow: use the value rankings to pick target suburbs, then check the best 30–50 recent sales by hand.

---

## 13. NSW Planning Portal DAs and the NSW cadastre

**Planning Portal**
- All NSW councils must use it for DAs since July 2021 (patchy before). Also holds complying development certificates and post-consent certificates.
- **Online DA Data API:** free, CC BY, daily, all DAs lodged since 2019; key via the data broker. Records include address, lot/plan, council, work description, cost, status, dates.
- Floor plans are PDFs per application; many councils don't publish internal floor plans online (privacy); architects hold copyright.
- Uses for us: renovation/extension flags, fixing mix distortions (e.g. Enfield), knock-down rebuilds and subdivisions, future unit supply.

**Cadastre (NSW Spatial Services, Land Parcel and Property Theme)**
- Official map of every NSW parcel, updated daily, free under CC BY. Lots with lot/plan numbers, strata plans, property boundaries linked to Valuer General property IDs.
- Gives lot shape and area, frontage, corner and battle-axe lots, and a base for zoning, heritage, flood, bushfire, LiDAR and footprint overlays.
- No owners, buildings or rooms. Survey plan documents come from NSW Land Registry Services for a fee.

Combining sales + cadastre + DA records gives a free property-level dataset with sale history, lot geometry, zoning/heritage and renovation history.

---

## 14. Can I get the number of rooms from DAs?

Not from the DA feed itself (no bedroom field), but yes from **BASIX certificates** attached to DAs and complying development certificates — public PDFs on the Planning Portal. Each records:

- number of bedrooms; conditioned and unconditioned floor area; site and roof area; address and lot/plan number;
- for alterations, the number of bedrooms in the existing dwelling;
- for apartment/townhouse projects, bedrooms and floor area for every unit.

Example: a 2025 new house in Kingsgrove — 4 bedrooms, 267.6 m² conditioned floor area, 544 m² site, lot 124 DP14903.

Limits: only new builds and significant renovations since ~2004–06; on the Portal mostly from 2019–21; shows what was approved, not necessarily built. Best bulk route: ask the Department of Planning, Housing and Infrastructure for lot-level BASIX data. Saved source summary to the project as `property_attribute_sources.md`.

---

## 15. What's in the BASIX datasets?

The Planning Portal blocked downloads from my workspace, so I confirmed from listings only: **BASIX Single Dwelling Certificates 2011–2020** and **BASIX Multi Dwelling Certificates 2011–2020** (Excel, CC BY), plus an older single-dwelling file. Contents: hot water, cooling and general dwelling information including bedrooms; filterable by completion receipt. Level of detail and fields were unclear until the files were uploaded.

---

## 16. Do the BASIX files cover all NSW properties?

No — new homes only, with no address.

- **Single dwellings:** 299,019 certificates (275k separate houses, 22.5k attached, 1k single units). Bedrooms, total floor area, site area, storeys, appliances, solar.
- **Multi dwellings:** 36,014 projects covering 478k dwellings; project totals only (dwellings with 1/2/3/4+ bedrooms, total floor area, building heights).
- Financial years 2011-12 to 2019-20.
- Approvals, not completions: 54% of single and 38% of multi certificates have a completion receipt.
- Location only to council area, suburb and postcode.
- **Our four regions:** ~11.5k new single dwellings (e.g. Sydenham 21, Tempe 69, St Ives 215) and ~112k new apartments/townhouses (39k in the City of Sydney).

Uses: suburb-level new-build profiles; a possible match to sales for new houses on suburb + postcode + near-identical site area + sale after completion (test match rate first).

---

## 17. Can Project IDs be matched to properties?

No. The Project ID is BASIX's internal reference; the sales data has no BASIX field; it isn't the public certificate number (e.g. 1791058S); no public lookup exists; the DA feed doesn't carry it. The addresses were likely removed to keep the dataset anonymous.

Best route: ask the department's data team (data.broker@environment.nsw.gov.au) for the same 2011–2020 files with Lot/DP or G-NAF address ID added, plus post-2020 data. Meanwhile, the lot-size match can be run as an interim.

---

## Open next steps
- Draft the BASIX lot-level data request to the department.
- Run the lot-size match between BASIX single-dwelling certificates and new-house sales.
- Add back the ~13k residential sales coded "Other" and re-run the value scores.
- Add rents and yields from NSW rental bond data.
- Pull DA / complying-development records and flag renovated properties in the value analysis.
