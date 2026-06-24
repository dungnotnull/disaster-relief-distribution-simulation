# test-scenarios.md -- Skill #242: Disaster Relief Distribution Simulation & Optimization (NGO)

## Overview
This document defines 6 test scenarios for validating the disaster-relief-distribution-simulation skill. Each scenario specifies inputs, expected outputs, quality gate checks, and known failure modes. Scenarios cover different disaster types, geographies, resource constraints, and special cases.

---

## Scenario 1: Urban Earthquake -- Acute Phase, Single NGO
**Type:** Earthquake | **Phase:** Acute (Day 0-7) | **Agencies:** 1 NGO (IRC)

### Inputs
```
disaster_type: earthquake
location: Türkiye, Kahramanmaraş Province, Elbistan District
affected_population_total: 45,000 (in 8 displaced clusters across 3 km radius)
vehicles: 4 trucks (5 MT each), 6 motorcycles (100 kg each)
warehouses:
  - W1: Elbistan town centre, 50 MT capacity, 40 MT current stock
  - W2: Pre-positioned depot 12 km north, 20 MT capacity, 15 MT current stock
budget_usd: 180,000
time_horizon_days: 7
response_phase: acute
partner_agencies: none
access_constraints:
  - Main bridge collapsed (Road D360 blocked -- route to 3 eastern clusters severed)
  - 2 clusters in rubble zones (road score = 1, heavy equipment clearing required)
special_considerations: February -- cold climate; thermal blankets priority
```

### Expected Outputs

**sub-profile-intake:**
- All 5 mandatory fields populated
- ReliefWeb sitrep for "Türkiye earthquake Kahramanmaraş" fetched and cited
- Road condition: 3 eastern clusters unreachable by truck (bridge out) -> motorcycle/relay required
- Supply vs. need flag: 40+15=55 MT stock vs. ~63 MT needed (Sphere minimum x 45,000 x 7) -> WARN:️ WARNING: 12.7% gap

**sub-needs-assessment:**
- Water: 15 L x 45,000 = 675,000 L/day = 675 kL/day total over 7 days = 4,725 kL
- Food: 0.45+0.06+0.025+0.015 kg x 45,000 = 24.75 MT/day of dry food -> 173.25 MT over 7 days
- NFI kits: 45,000/5 = 9,000 HH x 20 kg = 180 MT (one-time; cold climate doubles blanket quantity)
- RUTF: IPC Phase 3 assumed (earthquake acute) -> 2% of u5 SAM = 0.02 x 0.15 x 45,000 ~ 135 SAM children -> 405 sachets/day
- WARN:️ COLD CLIMATE FLAG: blankets doubled to 4/HH; thermal clothing added to NFI
- IPC assumption flagged: WARN:️ IPC Phase 3 assumed -- not confirmed for this shock type

**sub-logistics-optimizer:**
- Clarke-Wright savings: 3 truck routes covering 5 accessible clusters; motorcycles serving 3 eastern clusters (relay via rubble zone)
- Day 1 route priority: Tier 1 clusters first (2 camp sites identified with elderly/children concentration)
- Nash equilibrium: N/A (single NGO)
- Modality: In-kind (market score = 1/10 -- markets destroyed in earthquake)
- QG-5 check: 4 trucks x 5 MT = 20 MT/day; with 6 motorcycle relays (0.1 MT each) = 0.6 MT/day additional
  - Tier 1 population (est. 30% of 45,000 = 13,500): Day 1 coverage estimate = 9,000/13,500 = 67% WARN:️ BELOW 80% threshold
  - Escalation: Alert user -- recommend requesting WFP common services vehicle hire (+2 trucks) to reach 80%

**sub-simulation-engine:**
- Scenario A (bridge further collapses): 3 eastern clusters lose motorcycle access -> 8,000 Tier 1 unreachable -> WARN:️ CRITICAL
  - Contingency: Coordinate helicopter access via Turkish government; store 5-day buffer at eastern edge before bridge collapses completely
- Scenario B (budget cut 25% = $135,000): Can sustain Tier 1 food and WASH only; NFI deferred Day 5-7
- Scenario C (demand surge 30% = 58,500 persons): Additional 4,500 MT needed; request WFP emergency pipeline release
- Scenario D (weather -- February temperature drop): Pre-stock blankets and heating fuel by Day 3; no road closure risk (snow, not rain)
- Sensitivity: Access constraint (Scenario A) has highest impact (-23pp Tier 1 Day 3)

### Quality Gate Checks
- [ ] QG-1: All 5 mandatory fields in profile OK
- [ ] QG-3: Sphere minimums cited for water (15 L), food (2,100 kcal), shelter (3.5 m^2) OK
- [ ] QG-4: IPC Phase 3 flagged as WARN:️ assumption OK
- [ ] QG-5: QG-5 FAILS (67% < 80%) -> escalation to user presented with vehicle hire option OK
- [ ] QG-7: All 4 scenarios completed OK
- [ ] QG-9: Impartiality check -- eastern clusters not deprioritized despite inaccessibility OK

### Known Failure Modes
- Do NOT produce a plan that skips eastern clusters without flagging them -- impartiality violation
- Do NOT show water < 7.5 L/person/day even in Day 1 when truck capacity is stretched -- below Sphere survival minimum
- Do NOT recommend cash transfers when markets are confirmed destroyed

---

## Scenario 2: Coastal Cyclone -- Multi-Agency Coordination, Rural
**Type:** Cyclone | **Phase:** Acute + transition to early recovery | **Agencies:** 4 NGOs

### Inputs
```
disaster_type: cyclone
location: Bangladesh, Cox's Bazar District, coastal clusters
affected_population_total: 120,000 (12 coastal clusters)
  - Including 80,000 Rohingya refugees in camps (already camp-resident)
  - 40,000 host community
vehicles (combined fleet across 4 agencies):
  - Oxfam: 3 trucks (3 MT), 1 flatbed (8 MT)
  - IRC: 2 trucks (5 MT), 2 motorcycles
  - WFP: 5 trucks (10 MT), 2 warehouses registered with Logistics Cluster
  - UNICEF: 1 refrigerated van (RUTF/vaccines cold chain), 1 truck (3 MT)
warehouses:
  - WFP W1: Cox's Bazar town, 200 MT capacity, 150 MT current stock (WFP pipeline)
  - Oxfam W2: Teknaf, 30 MT capacity, 25 MT current stock
budget_usd: 850,000 (combined CERF + individual NGO budgets)
time_horizon_days: 14
response_phase: acute (Days 1-3) transitioning to early-recovery (Days 4-14)
partner_agencies: Oxfam, IRC, WFP, UNICEF
access_constraints:
  - Road T1 (coastal highway) partially flooded -- passable by 4WD only (road score 1)
  - 2 island clusters accessible only by boat
special_considerations: cold chain for UNICEF vaccines; Rohingya cultural dietary restrictions (no pork in rations)
```

### Expected Outputs

**sub-profile-intake:**
- 4-agency resource pooling table constructed
- Rohingya-specific note: pork excluded from all rations (Halal standard)
- Island clusters flagged: boat transport required; UNICEF coordinates with UNHCR boat service
- WFP common services already activated (Logistics Cluster lead role)

**sub-needs-assessment:**
- Separate needs matrix for camp population (80,000) vs. host community (40,000)
- Camp population IPC phase: likely Phase 3-4 (chronic pre-cyclone vulnerability + acute shock)
- Therapeutic nutrition: RUTF for SAM children in camp population (2% of camp u5 ~ 2% x 0.15 x 80,000 = 240 children -> 720 sachets/day)
- WASH: camp clusters have existing WASH infrastructure (partially damaged) -- needs partially met

**sub-logistics-optimizer:**
- Nash equilibrium zone assignment:
  - WFP: bulk food distribution for all 12 clusters (fleet scale + warehouse proximity)
  - Oxfam: WASH supplies (Teknaf warehouse proximity to southern clusters)
  - IRC: NFI + protection supplies (existing community relationships in 5 northern clusters)
  - UNICEF: cold chain RUTF + vaccine delivery (island clusters via boat coordination)
- Efficiency: Combined fleet can reach all 12 clusters within 48h; Tier 1 coverage Day 1 = 88% OK
- Modality: Days 1-3 in-kind; Days 7-14 evaluate cash (Cox's Bazar markets partially restored)

**sub-simulation-engine:**
- Scenario A (coastal highway fully floods): IRC reroutes to inland tracks; adds 3h per trip
- Scenario D (second weather event -- monsoon rain within 72h): Pre-position 5-day supplies in all island clusters before rain

### Quality Gate Checks
- [ ] QG-6: Cost/beneficiary = $850,000 / 120,000 = $7.08/person/14 days; WFP norm $40-80/person/month -> reasonable OK
- [ ] Nash equilibrium coordination plan presented OK
- [ ] Dietary restriction (Halal) applied to all ration calculations OK
- [ ] Cold chain tracked separately for UNICEF items OK

### Known Failure Modes
- Do NOT assign all 4 NGOs to the same easiest-access clusters -- this is the coordination failure mode the Nash equilibrium prevents
- Do NOT omit island clusters from the plan (impartiality -- remote does not mean lower priority)

---

## Scenario 3: Riverine Flood -- Cash vs. In-Kind Decision, Urban Context
**Type:** Flood | **Phase:** Early recovery (Day 10 post-flood) | **Agencies:** 2 NGOs

### Inputs
```
disaster_type: flood
location: Nigeria, Anambra State, Onitsha city
affected_population_total: 35,000 (urban displaced; living with host families)
vehicles: 2 trucks (5 MT), 3 motorcycles
warehouses:
  - W1: Onitsha Main Market area, 25 MT capacity, 20 MT current stock
budget_usd: 250,000
time_horizon_days: 21 (early recovery period)
response_phase: early-recovery
partner_agencies: ACF, World Vision
access_constraints: No major road damage -- urban context, markets partially open (60% of normal capacity)
special_considerations: Non-camp, dispersed population; beneficiary verification challenging; mobile money penetration 65%
```

### Expected Outputs

**sub-profile-intake:**
- Urban non-camp context noted -- beneficiary registration approach critical (Kobo Toolbox + community leaders)
- Market functionality noted: 60% operational -> signals cash transfer viability

**sub-needs-assessment:**
- IPC assessment: WebSearch for "IPC Nigeria Anambra 2025 2026 food security" -- likely Phase 2-3
- Urban population: likely to need NFI and food cash vouchers more than in-kind (markets operating)
- Host-family accommodation: shelter need partially met by host families; focus on NFI kit (cooking, blankets)

**sub-logistics-optimizer:**
- Cash vs. in-kind modality assessment:
  - Market functionality: 6/10 (60% operational) -> score 1
  - Security: good (urban area) -> score 2
  - Beneficiary preference: mobile money available 65% -> score 2
  - Admin capacity: ACF has mobile money partner (MTN Mobile Money) -> score 2
  - OCHA guidance: OCHA Nigeria recommends CBI in urban contexts -> score 2
  - Total: 9/10 -> RECOMMEND CASH/VOUCHER TRANSFER
- In-kind retained for: RUTF (no market substitute), IEHK health kits, latrine materials (market does not carry)
- Delivery plan: mobile money transfers to 35,000/5 = 7,000 HH; monthly transfer USD 35/HH/month
- In-kind distribution: 1 truck run for RUTF + health kits to distribution points identified with community leaders

**sub-simulation-engine:**
- Scenario A: Mobile money system down -> fallback to voucher system at 3 partner retailers (pre-agreed)
- Scenario C (demand surge): Additional registrations -> scale mobile money at marginal cost (low incremental cost for CBI)

### Quality Gate Checks
- [ ] Cash vs. in-kind decision documented with 5-criteria rubric scores OK
- [ ] In-kind exceptions documented (RUTF, IEHK) with rationale OK
- [ ] Beneficiary verification approach described (Kobo registration + community leader validation) OK
- [ ] Fallback to voucher system if mobile money fails included OK

### Known Failure Modes
- Do NOT recommend in-kind food when modality score is 9/10 -- this ignores beneficiary dignity and market recovery
- Do NOT omit beneficiary verification approach in urban context -- fraud risk is higher

---

## Scenario 4: Conflict Displacement -- Security-Constrained Access
**Type:** Conflict displacement | **Phase:** Acute | **Agencies:** 2 NGOs (MSF, NRC)

### Inputs
```
disaster_type: conflict_displacement
location: Sudan, North Darfur State, El Fasher District
affected_population_total: 80,000 IDPs (in 4 displacement clusters near El Fasher)
vehicles:
  - MSF: 4 armored trucks (3 MT each -- medical supplies only), 2 standard trucks (5 MT)
  - NRC: 3 trucks (5 MT), 2 motorcycles
warehouses:
  - MSF W1: El Fasher compound (within secure UN perimeter), 40 MT capacity, 35 MT stock
  - NRC W2: 8 km east of El Fasher, 20 MT capacity, 18 MT stock
budget_usd: 420,000
time_horizon_days: 10
response_phase: acute
partner_agencies: MSF, NRC
access_constraints:
  - HIGH SECURITY RISK: Active conflict within 15 km of two displacement clusters
  - Movement requires UN security clearance (UNDSS approval) before each convoy
  - Night movement prohibited
  - 1 cluster (C4) -- currently inaccessible due to armed group presence (road score = 0)
special_considerations: Neutrality -- MSF cannot accept military escort (humanitarian principles); access negotiations ongoing for C4
```

### Expected Outputs

**sub-profile-intake:**
- SECURITY FLAG: Active conflict zone -- all routes to C4 suspended until access negotiated
- MSF armored trucks allocated ONLY to medical supply runs (organization policy)
- UNDSS clearance noted as mandatory process (adds 24-48h lead time to each convoy)
- C4 flagged as WARN:️ UNREACHABLE -- access negotiations with armed group ongoing

**sub-needs-assessment:**
- IPC Phase 4 expected (conflict displacement in Darfur -- chronic emergency + acute shock)
- High acute malnutrition likely: assume GAM > 20% in IDP population (Darfur context)
- RUTF quantities: elevated -- assume 5% SAM among u5 (vs. standard 2%)
- Security implication: no independent beneficiary registration possible in high-risk areas -> remote verification required

**sub-logistics-optimizer:**
- Security-constrained routing:
  - All convoy routes MUST stay within UN security corridors
  - Maximum time in transit: 6 hours (must return to compound before dusk)
  - Nash equilibrium: MSF covers health/nutrition (cold chain capability); NRC covers food and shelter
  - C4 -- no distribution plan possible at this time; flag and monitor
- Efficiency: 3 accessible clusters x 60,000 persons -> Tier 1 coverage Day 3 = 71% WARN:️ (C4 = 20,000 persons excluded)
  - Escalate: User informed that 20,000 persons in C4 unreachable; access negotiations must be prioritized
- OCHA CERF allocation: Recommend flagging C4 funding gap to OCHA Sudan

**sub-simulation-engine:**
- Scenario A: Road to C2 blocked after armed incident -> reroute within UN corridor; 2h delay only
- Scenario D: Dust storm (Haboob -- common in Darfur) -> suspend all convoys; pre-stock 3 days at C1, C2, C3
- Contingency for C4 access: When access granted, pre-position 5-day emergency stock within 24h

### Quality Gate Checks
- [ ] All routes through conflict zones flagged with WARN:️ SECURITY RISK OK
- [ ] Neutrality principle maintained -- MSF humanitarian principles documented OK
- [ ] UNDSS clearance requirement noted in every convoy plan OK
- [ ] C4 inaccessibility escalated -- not silently omitted from plan OK
- [ ] QG-9: Impartiality check -- C4 population not de-prioritized, actively escalated OK

### Known Failure Modes
- Do NOT recommend military escort routes -- this violates humanitarian neutrality principle
- Do NOT omit C4 from the analysis -- the 20,000 unreachable persons must appear in the output even if the plan cannot serve them yet
- Do NOT assign MSF armored vehicles to food distribution -- respect organization-specific operational policies

---

## Scenario 5: Pre-Positioning -- Typhoon Season Preparedness (Philippines)
**Type:** Pre-positioning (preparedness) | **Phase:** Pre-event | **Agencies:** 3 NGOs + WFP

### Inputs
```
disaster_type: preparedness_pre-positioning
location: Philippines, Eastern Samar Province (typhoon landfall zone)
affected_population_at_risk: 200,000 (estimated from INFORM Risk Index + historical typhoon track data)
vehicles: (to be deployed from Manila pre-positioned fleet)
  - WFP: 8 trucks (10 MT), 2 boats (5 MT)
  - DSWD (Philippines Gov): 10 trucks (5 MT), 5 motorcycles
  - CARE: 3 trucks (3 MT)
warehouses (pre-positioning targets):
  - W1: Borongan City, current empty (50 MT capacity)
  - W2: Guiuan, current empty (30 MT capacity)
  - W3: Mercedes, current empty (20 MT capacity)
budget_usd: 1,200,000 (pre-positioning budget from CERF Early Action)
time_horizon_days: 30 (pre-position in next 14 days; distribute within 72h of typhoon impact)
response_phase: preparedness
typhoon_track_forecast: Projected PAGASA landfall in Eastern Samar in 10-12 days
INFORM Risk Index: Eastern Samar = 7.2/10 (high risk)
special_considerations: Coastal areas require boat access; earthquake and tsunami secondary hazard possible
```

### Expected Outputs

**sub-profile-intake:**
- INFORM Risk Index 7.2/10 noted -- justifies pre-positioning
- Typhoon track forecast integrated: 10-12 day window for pre-positioning
- 3 warehouse locations assessed for strategic positioning relative to projected landfall and road network
- Secondary hazard flag: coastal warehouses at W2 (Guiuan) tsunami risk -- recommend elevated storage

**sub-needs-assessment:**
- Pre-positioning calculation:
  - 200,000 persons at risk x 14 days (initial buffer stock post-typhoon) x Sphere minimums
  - Food: 200,000 x 0.55 kg/day x 14 days = 1,540 MT of mixed rations
  - NFI: 200,000/5 = 40,000 HH kits x 20 kg = 800 MT (one-time, acute)
  - Total pre-position target: ~2,400 MT across 3 warehouses (combined capacity = 100 MT -- significantly below need)
  - WARN:️ WARNING: 100 MT warehouse capacity = 4.2% of need -- recommend emergency warehouse rental or school gymnasium requisition
- IPC: Non-applicable (pre-disaster); flag that food security will depend on typhoon damage to agriculture/markets

**sub-logistics-optimizer:**
- Pre-positioning optimization (warehouse siting):
  - W1 Borongan: largest capacity, inland-accessible -- optimal for bulk pre-positioning
  - W2 Guiuan: coastal -- boats required post-impact; pre-position NFI and RUTF here (small, critical items)
  - W3 Mercedes: northern access -- cover northern clusters post-typhoon
  - Recommended pre-positioning split: W1=70%, W2=20%, W3=10%
- Convoy schedule: 3 supply runs from Manila over 14 days (before typhoon impact)
- Post-typhoon activation plan: Within 2h of typhoon passing, activate all 3 depots simultaneously

**sub-simulation-engine:**
- Scenario A: W2 Guiuan directly hit by typhoon eye -- warehouse destroyed -> activate W1 as primary, request air drops to W2 coverage area
- Scenario D: Typhoon intensity increases (Cat 4->5) -> accelerate pre-positioning to complete in 7 days, not 14
- Pre-event surge recommendation: Complete all pre-positioning by Day 7 (not Day 14) to allow safety margin

### Quality Gate Checks
- [ ] INFORM Risk Index integrated and cited OK
- [ ] Typhoon track forecast integrated OK
- [ ] Warehouse tsunami risk flagged for coastal W2 OK
- [ ] Pre-positioning supply target calculated vs. warehouse capacity gap escalated OK
- [ ] Post-typhoon activation plan (72-hour deployment protocol) included OK

### Known Failure Modes
- Do NOT plan warehouse at W2 Guiuan for critical supplies without tsunami risk mitigation
- Do NOT assume warehouse capacity is sufficient -- always calculate total need vs. capacity
- Do NOT wait for typhoon impact to start planning -- pre-positioning mode means acting NOW

---

## Scenario 6: Multi-Hazard Compound Emergency -- Earthquake + Cholera Outbreak
**Type:** Compound (earthquake + cholera) | **Phase:** Acute transition | **Agencies:** 3 NGOs + UNICEF

### Inputs
```
disaster_type: compound_earthquake_cholera
location: Haiti, Artibonite Department
affected_population_total: 95,000
  - 70,000 earthquake displaced (5 clusters)
  - 25,000 cholera-affected (3 clusters overlapping with displacement)
vehicles: 3 trucks (5 MT), 1 refrigerated van (MSF -- cold chain), 4 motorcycles
warehouses:
  - W1: Saint-Marc, 60 MT capacity, 45 MT stock (general supplies)
  - W2: MSF depot, 5 MT capacity, cold chain capability (ORS, cholera kits, vaccines)
budget_usd: 380,000
time_horizon_days: 14
response_phase: acute
partner_agencies: MSF, Concern, UNICEF
access_constraints:
  - Damaged roads in 2 clusters (road score 1)
  - Cholera clusters require PPE for distribution teams (increases time per delivery by 30%)
special_considerations:
  - Cold chain for cholera kits and ORS -- critical
  - Distribution teams need PPE (gown, gloves, boots, chlorine spray station at distribution point)
  - Cholera transmission risk at crowded distribution points -- crowd management protocol required
```

### Expected Outputs

**sub-profile-intake:**
- HEALTH HAZARD FLAG: Cholera active in 3 clusters -- all distribution operations require infection prevention measures
- Cold chain integrity documented for W2 MSF depot
- PPE requirement added to vehicle load manifests (reduces payload by est. 5%)
- Distribution point design: cholera-affected clusters require separate entry/exit, handwashing stations, ORS distribution alongside other items

**sub-needs-assessment:**
- WASH needs elevated due to cholera:
  - Water quantity: 20 L/person/day (above Sphere 15 L minimum -- elevated for cholera response)
  - Chlorination: 2 mg/L residual chlorine -- calculate bleaching powder quantities
  - ORS: 10 sachets per cholera-affected person (25,000 x 10 = 250,000 ORS sachets for 14 days)
- Health supplies elevated: cholera kits in addition to IEHK
- Health flag: Mass cholera vaccination (OCV) should be coordinated with Haiti MSPP and UNICEF

**sub-logistics-optimizer:**
- Separate distribution channels for cholera clusters vs. general displaced:
  - General food distribution: standard routes
  - Cholera cluster distribution: PPE-equipped teams only; MSF refrigerated van carries ORS/cholera kits
  - UNICEF: oral cholera vaccine (OCV) campaign coordination
- Nash equilibrium: MSF covers health/cholera response; Concern covers food + NFI; UNICEF covers OCV campaign

**sub-simulation-engine:**
- Scenario: Cholera spreads to 2 more clusters -- scale ORS and cholera kit quantities immediately
- Contingency: If refrigerated van breaks down, cold chain supplies must reach MSF depot within 6h for repackaging -- pre-identify repair contractor

### Quality Gate Checks
- [ ] Health hazard (cholera) flagged and infection prevention protocol included in all distribution plans OK
- [ ] Cold chain integrity tracked through each delivery step OK
- [ ] WASH quantities elevated above Sphere minimum with rationale for cholera context OK
- [ ] OCV coordination with UNICEF noted as parallel action OK
- [ ] Distribution point crowd management protocol described OK

### Known Failure Modes
- Do NOT plan crowded group food distribution in cholera-active clusters without PPE and crowd management -- this will amplify transmission
- Do NOT use the same distribution point for cholera kits and general food without separate flow design
- Do NOT omit ORS cold chain tracking -- broken cold chain in cholera response is a critical failure
