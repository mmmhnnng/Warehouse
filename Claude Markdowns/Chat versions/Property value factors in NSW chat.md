# NSW Property Value & Property Tool Idea — Chat Transcript

*Conversation from November 2026. Answers lightly condensed; source citations removed. Not financial or legal advice.*

---

## Q1. What are the top factors to determine the value of a property in NSW? obviously suburb, location, transport, sun access

Beyond the ones you've listed, these tend to move the needle most in NSW.

**Land and what you can do with it**
- **Zoning and development potential.** An R2 (low density) block that could be rezoned, or one that already allows dual occupancy, terraces or townhouses, is worth more than an identical block that can't be developed. The NSW low and mid-rise housing reforms and the transport-oriented development precincts have changed what's allowed near many stations and town centres, so check the current Local Environmental Plan (LEP) for the specific lot.
- **Land size, frontage and shape.** In Sydney especially, buyers are paying for the land and the house is secondary. Wide frontage, a regular rectangular shape and a block size that meets the minimum lot size for subdivision all add value.
- **Topography.** Flat or gently sloping land is cheaper to build on. A steep block, particularly one that falls away from the street, usually sells at a discount unless it has views.

**Risks and restrictions**
- **Hazard overlays.** Flood planning areas, bushfire-prone land and land contamination can hurt value and push insurance premiums up sharply. These show up on the Section 10.7 planning certificate.
- **Heritage.** A heritage listing or Heritage Conservation Area limits renovations and knockdowns, but protects streetscape character.
- **Easements and covenants.** Sewer mains, rights of way and restrictive covenants can limit what you can build.
- **Noise.** Aircraft flight paths (check ANEF contours, especially with Western Sydney Airport coming), main roads, rail lines and nearby commercial uses.

**Micro-location**
- **The specific street.** A quiet, leafy no-through-road can command a big premium over a busy street a block away.
- **School catchments.** In-zone for a sought-after public school is a significant price driver.
- **Walkability.** Distance to cafés, shops, parks, the beach or water, and views.

**The dwelling itself**
- **Condition, layout and age.** Bedrooms, bathrooms, off-street parking, livable floorplan.
- **Building quality.** For newer apartments, defect history matters a great deal since the Opal and Mascot Towers cases.

**Title type and strata**
- **Title type.** Torrens generally sells for more than strata; company title is least liquid.
- **Strata health (units).** Levies, sinking fund, by-laws, special levies, number of units. Smaller boutique blocks often hold value better.

**Market factors**
- **Comparable sales.** What valuers and banks anchor on.
- **Supply pipeline.** Lots of new apartment stock nearby can soften values.
- **Infrastructure announcements.** New Metro lines tend to lift prices once committed.

Most useful documents: Section 10.7 planning certificate, council LEP maps, strata report, and the NSW Valuer General's land value (land only, lags the market).

---

## Q2. isn't public transport access or driving time to CBD factor largely?

Yes, it's one of the biggest, arguably the single biggest after the suburb itself. I left it out only because you'd already listed transport.

Travel time to the CBD (and increasingly Parramatta, North Sydney, Macquarie Park, Chatswood) is one of the strongest predictors of land value. Prices track **commute time** more closely than distance, which is why a suburb 20 km out on fast rail can outprice one 12 km out relying on congested roads.

- **Walking distance to the station.** Within about 800 m / 10-minute walk is the sweet spot. Right next to the line can cut value due to noise, so the premium often peaks a few streets back.
- **Line quality.** Frequent, reliable, no-change services (Metro, North Shore express) are worth more than slow all-stops trains or buses. Light rail and ferries also carry premiums.
- **Road access.** Motorways (M2, M4, M5, WestConnex) matter more in outer, car-dependent areas. Tolls eat into the advantage; being too close brings noise.
- **Future infrastructure.** Committed projects (Metro West, Western Sydney Airport Metro, Southwest Metro extension) lift prices once funded and announced. Unfunded projects are riskier.
- **Changing work patterns.** Hybrid work softened the commute premium for people who go in a couple of days a week, but daily CBD access still commands a clear premium.

I'd put CBD and employment-hub access right at the top alongside land size and zoning.

---

## Q3. reorganise the entire list

**Tier 1: The big value drivers**
1. **Suburb and broader location** — sets the baseline price range.
2. **Access to the CBD and job hubs** — travel time, not distance.
3. **Public transport** — ~10-minute walk to a station on a fast, frequent line.
4. **Land size, frontage and shape.**
5. **Zoning and development potential** — expanded under the low and mid-rise housing reforms and TOD precincts.

**Tier 2: Strong secondary factors**

6. **Specific street and micro-location.**
7. **School catchments.**
8. **Aspect and sun access.**
9. **Views and proximity to water.**
10. **Walkability and amenity.**
11. **Road access.**

**Tier 3: The property itself**

12. **Dwelling size, layout and condition.**
13. **Topography.**
14. **Build quality and defects.**
15. **Title type.**
16. **Strata health (units).**

**Tier 4: Value detractors and risks**

17. **Flood, bushfire and contamination overlays.**
18. **Noise** (ANEF contours incl. Western Sydney Airport, roads, rail).
19. **Heritage restrictions.**
20. **Easements and covenants.**

**Tier 5: Market context**

21. **Comparable sales.**
22. **Future infrastructure.**
23. **Local supply pipeline.**
24. **Work patterns.**

The order shifts by property type: for apartments, strata health, building quality and transport rise; for houses, land size and zoning dominate.

---

## Q4. how many of these factors would Cotality have data for?

Roughly a third well covered, a third partially, and the rest largely not. Varies by product (RP Data Professional, consumer reports, AVM).

**Well covered (~10 of 24):** Cotality licenses NSW sales data from the Valuer General, so comparable sales (#21), suburb market data (#1), land size (#4) and title type (#15) are solid. Its Property Confidence Report covers flood, bushfire and storm-surge exposure, planning constraints, zoning, school catchments and NBN (#5, #7, #17). Its ValConnect valuer platform shows easements (#20). Property records hold core attributes like beds, baths, parking and floor area (#12). Cordell Connect tracks the development pipeline (#23).

**Partially covered (~7):** CBD/job access (#2), public transport (#3), road access (#11) and walkability (#10) can be approximated from distance, but not door-to-door commute time. Topography (#13), aspect (#8) and heritage (#19) may exist as layers but aren't headline fields. Future infrastructure (#22) appears in research rather than property-level data.

**Weak or not covered (~7):** Street quality (#6), views (#9), condition and layout, build quality (#14), strata health (#16), noise (#18), work patterns (#24).

Cotality notes its AVM estimates are computer-generated without physical inspection, which is why they can be well off for unusual properties.

---

## Q5. I can get transport data from Opendata Transport NSW, and probably build my own database to estimate commute time by car right? and can i use publicly available train and bus timetables to estimate public transport times?

Yes to both, with a caveat on the car side.

**Public transport: very doable**

TfNSW publishes full GTFS timetables for trains, Metro, buses, ferries and light rail, plus real-time feeds (free API key). Check the data licence page; generally Creative Commons attribution.

Don't write your own routing logic. Feed GTFS plus an OpenStreetMap extract into:
- **OpenTripPlanner** — complete multimodal router.
- **R5 / r5r** — built for fast travel-time matrices from many origins to few destinations.

Design choices: calculate across a departure window (e.g. every minute 7:00–9:00am) and take the median; include the walk to the station.

**Car commute: possible, but congestion is the hard part**

OpenStreetMap + OSRM or Valhalla gives free-flow times, which badly underestimate peak trips. TfNSW has traffic counts and incident feeds but I'm not aware of a network-wide historical speed dataset. Options:
- **Commercial APIs with historical traffic** (Google Distance Matrix with departure time, TomTom, HERE). Per-request cost.
- **Free-flow times plus congestion multipliers.** Cheap but rough.

Account for tolls (e.g. WestConnex).

**Tip:** don't calculate for every property. Calculate for a grid (e.g. 250 m cells) or ABS SA1 areas, assign each property its cell's value, and do it to several destinations (CBD, Parramatta, North Sydney, Macquarie Park).

---

## Q6. explain the last bit

**Why per-property calculation is wasteful:** Greater Sydney has ~2 million dwellings. 120 departure times × 4 destinations ≈ 1 billion route calculations. Neighbouring houses have almost identical commutes.

**How the grid works:** overlay 250 m × 250 m squares (a 2–3 minute walk across). Tens of thousands of cells vs two million homes. Calculate once from each cell centre; properties inherit their cell's value via a spatial join (GeoPandas, QGIS).

**SA1 alternative:** ABS census areas of ~200–800 people. They line up with census data but vary in size. Skip empty cells (parks, industrial land, water). Use smaller cells (~100 m) near stations.

**Trade-off:** a house at a cell edge may be a minute or two off; usually fine for valuation.

**Multiple destinations:** someone in Baulkham Hills may work in Macquarie Park or Parramatta. Keep each destination as a column, take the shortest, or weight by job counts.

**Why it beats Cotality:** standard data gives distance, not travel time. Two suburbs equidistant from the CBD can have very different commutes. Peak door-to-door time captures that.

---

## Q7. if i could put public transport, walking time, car commute time, plus add access too school catchments, public amenities & infrastructure like hospitals and shopping centres / grocery shops, comparable sales data, would this provide strong value that isn't already available? as well as add customisable ranking of factors for users

Honestly, the individual pieces mostly already exist. The opportunity is in combination and the question you answer.

**Already out there**
- **Commute times on listings:** Domain's "My Commutes."
- **Weighted suburb ranking:** Microburbs offers a Suburb Finder with user-weighted priorities, works at a sub-suburb level (~400 people), and covers schools, catchments, travel times and comparable sales.
- **Catchments, amenities, comps:** standard on Domain, REA/property.com.au, Cotality reports, Microburbs.

**Where there's a genuine gap**
1. **Rigorous peak-hour door-to-door travel time** — a feature, not a business on its own.
2. **Connecting scores to price** — flag properties that look cheap relative to what they offer (e.g. "same commute and catchment as the next suburb, sells for 15% less").
3. **Personal weighting applied to price** — rank listings or streets by value for money on the user's priorities.

**Data catch:** catchments, amenities, travel times and sales prices are accessible. Property attributes (beds, baths, condition, photos) are controlled by REA, Domain and Cotality. Scraping portals breaches their terms. Focus on land and location-driven value, or license data.

**Business question:** home buyers use tools briefly and start on REA/Domain. Better customers: buyers' agents, brokers, investors, developers.

**Overall:** data stack alone isn't differentiated; "accurate access measures + custom priorities + a price model that flags undervalued locations" could be. Test in one region (e.g. Parramatta–Hills) with buyers' agents first.

---

## Q8. how does Domain provide My Commute times?

Domain doesn't publicly say which routing engine it uses. Its help page describes adding a destination and transport mode on a listing's map, then showing route, distance and travel time.

It's almost certainly an **on-demand route lookup through a third-party mapping API** (Google Maps Platform, HERE, TomTom, Mapbox and similar sell this). Many Australian portals build on Google, but I couldn't confirm Domain's provider. You can check via browser dev tools → Network tab when adding a commute.

The feature requires login and is desktop-only, likely to control per-request API costs.

**Difference from your approach:** Domain answers one trip at a time, for one departure time. Yours would pre-compute peak-window medians from every grid cell to several hubs, enabling area ranking, heatmaps, street comparisons and price-model inputs — helping people decide where to look, not just evaluate one listing.

---

## Q9. data access, summarise what I easily have access to for free

*(Generally NSW Government open data under Creative Commons Attribution; check each licence.)*

**Sales and land values**
- **NSW Valuer General bulk property sales** back to 1990: price, dates, address, area, zoning code, strata/non-strata. ~8-week lag after settlement.
- **Bulk land values** from July 2017 (CC BY 4.0).

**Location and access**
- **TfNSW GTFS** timetables and real-time feeds.
- **OpenStreetMap** roads, paths and amenities.
- **NSW Health** facility locations.
- **G-NAF** addresses and **NSW Spatial Services** lot boundaries.

**Planning and risk**
- **NSW Planning Portal** layers: zoning, minimum lot size, height, FSR, heritage.
- **Bushfire-prone land** layer.
- **Geoscience Australia ELVIS** elevation/LiDAR → slope and aspect.

**Schools and neighbourhood**
- **NSW Department of Education** school intake zones.
- **ABS census** data and boundaries.
- **BOCSAR** crime statistics.
- **NSW Fair Trading** rental bond data.

**Not free or not clean**
- Property attributes (beds, baths, condition, photos).
- Peak-hour car travel times.
- Flood mapping (council-held, inconsistent).
- School performance (NAPLAN / My School not bulk downloadable).
- Strata health.
- Aircraft noise (ANEF maps/PDFs).

You can cover location, access, land, zoning, catchments, hazards (except flood) and prices well for free. Gaps are mostly about the house itself.

---

## Q10. so if the data stack alone isn't differentiated enough, but "accurate access measures + custom priorities + a price model that flags undervalued locations", i could also add custom priorities comparison to baseline market priorities and value of properties

Yes, and that's a genuinely stronger idea: **"Where do my priorities differ from the market's, and how can I use that gap?"**

**How it works:** a **hedonic pricing model** breaks prices into implicit prices per factor (e.g. 10 minutes less commute ≈ +6%, top catchment ≈ +8%, north-facing ≈ +3%). These are the **market baseline priorities**. Compare with the user's:
- **User cares more than market** → bargains for them.
- **Market pays for, user doesn't care** → where they overpay.

**What the user sees:** market value, asking/sale price, and a personal value score, plus a breakdown (e.g. "~$110k of this $1.4M reflects the school catchment, which you marked unimportant").

**Watch out for**
1. **Resale risk** — frame as "better value for living here," not "better investment."
2. **Market priorities vary by area and time** — estimate by sub-market, refresh regularly.
3. **Missing house data distorts estimates.**
4. **Factors move together** — show ranges.

**Why differentiated:** existing tools score locations or estimate values, but don't connect them through the user's own priorities. Also a compelling tool for buyers' agents.

---

## Q11. what is the potential of this idea?

Solid potential as a niche data business, a realistic acquisition target, lower chance of a very large standalone company.

**Why real:** high-stakes decisions made with blunt tools. CoStar completed its Domain acquisition in August 2025 (A$2.5B for the remaining 83%) and plans further investment in digital tools — both demand signal and potential acquirer.

**Customers**
- **Home buyers** — weakest business: infrequent use, high marketing cost.
- **Buyers' agents** — best start; subscription; likely hundreds of thousands to low millions in annual revenue alone.
- **Developers / site finders** — highest value per insight, especially with NSW housing reforms.
- **Lenders, insurers, investors** — later-stage data licensing.

**Risks**
1. Portals copying visible features (Domain under CoStar is well resourced).
2. Data quality without property attributes.
3. "Undervalued" is a strong claim — reputational/regulatory risk.

**Making it bigger:** expand beyond NSW, build a track record of flagged properties' outcomes, own a professional segment.

**Test cheaply:** build one corridor (Parramatta–Hills), show 10 buyers' agents and a few small developers.

---

## Q12. is anyone doing this at the moment?

Not in the exact form, as far as I can find.

**Personalised suburb matching:** Aussie's in-house LocationIQ for its buyer's agents matches suburbs to client priorities — conceptually closest, but internal and no market-vs-personal comparison. HtAG targets buyer's agents (~$237/month Professional plan, up to 150 metrics). Microburbs offers weighted comparison at street-block level. Propertybuyer uses an in-house "Suburb Selector." These are mostly **investment-focused** (growth, yield, vacancy).

**Valuation:** Cotality RP Data/AVM, Domain Pricefinder, REA PropTrack — single values, not breakdowns or personalised.

**Development potential:** Archistar (site reports, development potential; from ~$495/month) and Landchecker Site Finder — well served.

**The gap:** an **owner-occupier lifestyle value tool** showing in dollars what the market pays for each factor, how the user's priorities differ, and which properties are good value for them. Caveat: internal tools at agencies and lenders aren't fully visible.

---

## Q13. is there anyone that based on a selected property, show examples of comparable property sales nearby rather than a suburb median?

Yes, very common.

- **Professional tools:** Cotality RP Data and Domain Pricefinder are built around comparative market analyses (CMAs).
- **Consumer reports:** Cotality's Property Value reports, Microburbs property reports.
- **Portals:** realestate.com.au / property.com.au and Domain show recently sold nearby properties.

**Room to improve:** most tools pick comps by physical similarity and distance, ignoring catchment boundaries, station distance etc.
1. **Smarter selection** — match on commute, catchment, zoning, aspect.
2. **Adjusted comps** — e.g. "Comp sold $1.52M; same catchment, 9 min further from station (≈ −$45k), larger block (≈ +$70k) → implies ~$1.50M for your property."

Adjustments come straight from the market's implicit prices, turning a list of sales into an explanation of why properties sold for what they did.

---

## Q14. what about estimating property attributes, such as what an extra bedroom or extra bathroom or 20min shorter commute is worth in a particular suburb?

That's exactly what the hedonic model produces. Cotality publishes one-off studies (e.g. solar adds ~2.7% nationally, ~$23,100; school catchment premiums), but I'm not aware of a public tool giving these values per suburb on demand.

**Making it suburb-specific (small samples):**
- **Multilevel (hierarchical) models** — Sydney-wide values with suburb deviations, shrinking small samples toward regional averages.
- **Geographically weighted models** — values change smoothly across the city.
- Use several years of time-adjusted sales.

**Commute subtlety:** bedrooms vary within a suburb; CBD commute mostly varies between areas. Frame "20 minutes shorter commute" regionally. Station walking distance varies within suburbs, so estimate that locally.

**Data problem:** Valuer General data lacks beds, baths, parking. Options: license attribute data, use building-footprint proxies (floor area often predicts better), or collect from users.

**Presentation:** ranges with sample sizes (e.g. "$70k–$110k, based on ~900 sales over three years"). Values aren't additive.

**One engine, three features:** priority comparison, adjusted comps, attribute values.

---

## Q15. markdown this chat

*(Produced a structured topic-based Markdown summary: `nsw-property-value-tool-notes.md`.)*

## Q16. markdown the chat including my questions

*(This file.)*
