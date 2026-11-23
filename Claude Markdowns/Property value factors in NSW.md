# NSW Property Value Factors & Property Tool Idea

*Notes compiled from a conversation, November 2026. Not financial or legal advice.*

---

## 1. Factors that determine property value in NSW

Ranked roughly by how much each tends to move price. The order shifts by property type: for apartments, strata health, building quality and transport rise; for houses, land size and zoning dominate.

### Tier 1: The big value drivers
1. **Suburb and broader location**: sets the baseline price range (reputation, demographics, amenity, long-term demand).
2. **Access to the CBD and job hubs**: commute time to the CBD, Parramatta, North Sydney, Macquarie Park etc. Travel time matters more than distance.
3. **Public transport**: within ~10-minute walk of a station on a fast, frequent line (Metro, express trains) carries a strong premium. Being right next to the tracks can reduce value (noise).
4. **Land size, frontage and shape**: in Sydney, buyers largely pay for land. Wide, regular, usable blocks are worth most.
5. **Zoning and development potential**: dual occupancy, townhouses, subdivision, higher density. Expanded under the NSW low and mid-rise housing reforms and transport-oriented development (TOD) precincts. Check the council's LEP.

### Tier 2: Strong secondary factors
6. **Specific street / micro-location**: quiet, leafy streets vs busy roads.
7. **School catchments**: in-zone for a sought-after public school.
8. **Aspect and sun access**: north-facing living areas and yards.
9. **Views and proximity to water**.
10. **Walkability and amenity**: shops, cafés, parks, medical services.
11. **Road access**: motorway proximity matters more in outer areas; tolls and noise offset some benefit.

### Tier 3: The property itself
12. **Dwelling size, layout and condition**: beds, baths, parking, livable floorplan.
13. **Topography**: flat/gentle slopes preferred; steep street-falling blocks discounted unless they have views.
14. **Build quality and defects**: especially newer apartments (post-Opal/Mascot Towers concerns).
15. **Title type**: Torrens > strata > company title (least liquid).
16. **Strata health (units)**: levies, sinking fund, special levies, by-laws, scheme size.

### Tier 4: Value detractors and risks
17. **Flood, bushfire and contamination overlays**: on the Section 10.7 planning certificate; affect insurance.
18. **Noise**: flight paths (ANEF contours, incl. Western Sydney Airport), main roads, rail, commercial uses.
19. **Heritage restrictions**: heritage listing or Heritage Conservation Area.
20. **Easements and covenants**: sewer mains, rights of way, restrictive covenants.

### Tier 5: Market context
21. **Comparable sales**: what valuers and banks anchor on.
22. **Future infrastructure**: committed projects (Metro West, Western Sydney Airport line) lift prices before opening; unfunded proposals are speculative.
23. **Local supply pipeline**: lots of new apartment stock can soften unit values.
24. **Work patterns**: hybrid work softened the commute premium somewhat; daily CBD access still commands a clear premium.

**Key documents for a specific property:** Section 10.7 planning certificate, council LEP maps, strata report (units), NSW Valuer General land value (land only, lags market).

---

## 2. Transport and CBD access in more detail

- Prices track **commute time** more closely than kilometres. A suburb 20 km out on fast rail can outprice one 12 km out reliant on congested roads.
- **Walking distance to the station:** ~800 m / 10-minute walk is the sweet spot; premium often peaks a few streets back from the line.
- **Line quality:** frequent, reliable, no-change services (Metro, North Shore express) worth more than all-stops trains or buses. Ferries and light rail add premiums.
- **Road access:** motorways (M2, M4, M5, WestConnex) matter more in car-dependent areas; tolls and noise offset.
- **Future infrastructure:** committed and funded projects lift prices early; unfunded ones are risky.
- **Hybrid work:** softened the premium for occasional commuters; daily access still valued.

---

## 3. What Cotality (formerly CoreLogic) has data for

Rough estimate; varies by product (RP Data, consumer reports, AVM).

| Coverage | Factors |
|---|---|
| **Well covered (~10)** | Suburb market data, land size, zoning, school catchments, title type, flood/bushfire/storm-surge hazards, easements (valuer tools), basic dwelling attributes (beds, baths, parking, floor area), comparable sales (licensed from NSW Valuer General), development pipeline (Cordell Connect) |
| **Partial / derivable (~7)** | CBD/job-hub access, public transport, road access, walkability (distance-based, not door-to-door travel time), topography, aspect, heritage, future infrastructure (research, not property-level) |
| **Weak / not covered (~7)** | Street quality, views, condition and layout, build quality/defects, strata health, noise, work-pattern shifts |

The weak factors are what a physical inspection or local agent picks up, which is why automated valuations can miss badly on unusual properties.

---

## 4. Building your own travel-time data

### Public transport (very doable)
- **Data:** TfNSW Open Data publishes full GTFS timetables for all modes plus real-time feeds (free API key). Check the data licence page; generally Creative Commons attribution.
- **Routing engines (don't build your own):**
  - **OpenTripPlanner**: complete multimodal router.
  - **R5 / r5r**: built for fast travel-time matrices (many origins, few destinations).
- **Design choices:**
  - Calculate across a departure window (e.g. every minute 7:00–9:00am weekday) and take the **median**.
  - Include walking to/from stops, so station proximity is captured.

### Car commute (possible, congestion is the hard part)
- OpenStreetMap + OSRM or Valhalla gives free-flow times, which **badly underestimate peak trips**.
- TfNSW has traffic counts and incident feeds, but no obvious network-wide historical speed dataset.
- Options:
  - **Commercial APIs with historical traffic** (Google Distance Matrix with departure time, TomTom, HERE). Per-request cost.
  - **Free-flow + congestion multipliers** by corridor/time. Cheap but rough.
- Account for **tolls** (e.g. WestConnex).

### The grid approach (saves cost and computation)
- Per-property calculation is wasteful: ~2 million Sydney dwellings × 120 departure times × 4 destinations ≈ **1 billion** route calculations.
- Instead, overlay a **250 m × 250 m grid** (or use ABS **SA1** zones), calculate once per cell centre, and assign each property its cell's value via a spatial join (GeoPandas, QGIS).
  - Grid: uniform, consistent for travel time.
  - SA1: aligns with census data but varies in size.
  - Skip empty cells (parks, industrial land, water). Use smaller cells (~100 m) near stations.
- Calculate to **multiple destinations** (CBD, Parramatta, North Sydney, Macquarie Park, airport etc.) to capture job access. Keep separate columns, take the minimum, or weight by job counts.

### How Domain's "My Commutes" compares
- Domain doesn't publicly name its provider. It's almost certainly an **on-demand third-party routing API lookup** (Google, HERE, TomTom, Mapbox and similar sell this). You can check via browser dev tools → Network tab.
- Login-gated and desktop-only, likely to control per-request API costs.
- Answers one trip at a time for one departure time. Your approach pre-computes peak-window medians for whole areas, enabling filtering, heatmaps, street comparisons and use as a price-model input.

---

## 5. Free data available in NSW

### Sales and land values
- **NSW Valuer General bulk property sales**: back to 1990; price, dates, address, area, zoning code, strata/non-strata. ~8-week lag after settlement.
- **Bulk land values**: from July 2017, Creative Commons Attribution 4.0.

### Location and access
- **TfNSW GTFS timetables** + real-time feeds.
- **OpenStreetMap**: roads, walking paths, amenities (supermarkets, shops, parks). Spot-check coverage.
- **NSW Health** facility locations.
- **G-NAF** (national address file) and **NSW Spatial Services** cadastre (lot boundaries → land size, frontage, shape).

### Planning and risk
- **NSW Planning Portal** spatial layers: zoning, minimum lot size, height, FSR, heritage.
- **Bushfire-prone land** statewide layer.
- **Geoscience Australia ELVIS**: elevation/LiDAR → slope and aspect.

### Schools and neighbourhood
- **NSW Department of Education** school intake zones.
- **ABS census** data and boundaries (SA1 etc.).
- **BOCSAR** crime statistics.
- **NSW Fair Trading** rental bond data (median rents by postcode).

### Not free or not clean
- **Property attributes** (beds, baths, parking, condition, photos): controlled by REA, Domain, Cotality. Biggest gap.
- **Peak car travel times**: paid APIs.
- **Flood mapping**: council-held, inconsistent formats.
- **School performance (NAPLAN)**: My School data not freely bulk-downloadable.
- **Strata health**: individual strata records.
- **Aircraft noise (ANEF)**: mostly maps/PDFs; would need digitising.

---

## 6. The product idea

### Core concept
**Accurate access measures + custom priorities + a price model that flags undervalued locations.**

### Extension: personal vs market priorities
- A **hedonic pricing model** breaks prices into implicit prices per factor (e.g. "10 minutes less commute adds ~6%", "top catchment adds ~8%"). These are the **market baseline priorities**.
- Compare with the user's own priorities:
  - **User values more than market** → bargains *for them*.
  - **Market pays for, user doesn't care about** → where they're overpaying (e.g. a childless couple paying for a catchment).
- Show: market value, asking/sale price, personal value score, plus a dollar breakdown (e.g. "~$110k of this price reflects the school catchment, which you marked unimportant").

### Caveats
1. **Resale risk**: buying what the market undervalues means the next buyer also pays market prices. Frame as "value for living here," not "better investment."
2. **Market priorities vary by area and time**: estimate by sub-market and refresh regularly.
3. **Missing house data distorts estimates**: location factors may get credit for house quality.
4. **Correlated factors**: transport, schools and amenity cluster together; show ranges.

### Smarter comparable sales
- Comparable sales per property are **already common** (RP Data, Pricefinder CMAs, Cotality reports, Microburbs, REA/property.com.au, Domain).
- Room to improve:
  1. **Smarter selection**: match on commute, catchment, zoning, aspect, not just beds and distance.
  2. **Adjusted comps**: e.g. "Comp sold $1.52M; 9 min further from station (−$45k), larger block (+$70k) → implies ~$1.50M for your property."

### Attribute values by suburb
- Same hedonic model: "What is an extra bedroom / bathroom / shorter commute worth here?"
- Small suburb samples → use **multilevel (hierarchical) models** or **geographically weighted models**, plus multiple years of time-adjusted sales.
- Commute varies mostly *between* areas, so frame CBD-commute value regionally; station walking distance varies *within* suburbs and can be estimated locally.
- Bedroom/bathroom effects need attribute data: license it, use **building footprint** proxies (floor area often predicts better anyway), or collect from users.
- Present **ranges with sample sizes** (e.g. "$70k–$110k, based on ~900 sales over three years"). Values aren't simply additive.
- **One engine powers three features:** priority comparison, adjusted comps, attribute values.

---

## 7. Competitive landscape

| Area | Existing players | Gap |
|---|---|---|
| Commute times on listings | Domain My Commutes; overseas portals offer commute search | Peak-window, door-to-door, area-wide measures |
| Weighted suburb ranking | Microburbs (street-block level), HtAG (~150 metrics, ~$237/mo Professional plan), Suburbs Finder, Propertybuyer's Suburb Selector (in-house), Aussie LocationIQ (in-house, priority-based matching) | Mostly investment-focused (growth, yield); no dollar breakdown of factor values or personal-vs-market comparison |
| Valuation | Cotality RP Data/AVM, Domain Pricefinder, REA PropTrack | Single value, not personalised or explained |
| Development potential | Archistar (from ~$495/mo), Landchecker Site Finder | Well served; edge would need to be the price model and access measures |

**The gap:** an **owner-occupier lifestyle value tool** answering "where do I get the most of what I care about for my money?" rather than "where will prices grow?" Caveat: internal tools at agencies and lenders aren't fully visible.

---

## 8. Potential

- **Realistic outcome:** solid niche data business, possible acquisition target, lower chance of a very large standalone company.
- **Market signal:** CoStar completed its acquisition of Domain in August 2025 (~A$2.5B for the remaining 83%) and plans further investment in tools. That's both validation and a competitive threat.

### Customers
| Segment | Notes |
|---|---|
| Home buyers | Intense but infrequent use; already on REA/Domain; weakest business |
| **Buyers' agents** | Best starting point; repeat users, need to justify recommendations; supports hundreds of thousands to low millions in annual revenue alone |
| Developers / site finders | Highest value per insight, but crowded (Archistar, Landchecker) |
| Lenders, insurers, investors | Later stage: data licensing; needs proven accuracy |

### Key risks
1. **Portals copying visible features** (Domain under CoStar is well resourced). Defence: depth and serving professionals.
2. **Data quality** without property attributes; "undervalued" flags may just be renovators.
3. **"Undervalued" is a strong claim**: reputational/regulatory risk. Frame as value for the buyer's priorities, not investment advice.

### What would make it bigger
- Expansion beyond NSW.
- A dataset that improves over time (tracking how flagged properties performed).
- Becoming the go-to tool for one professional segment.

### Cheap validation
Build for one corridor (e.g. Parramatta–Hills), show to ~10 buyers' agents and a few small developers. If several would pay, or the flags match their instincts, proceed.
