---
name: disaster-relief-distribution-simulation/sub-profile-intake
description: Structured intake and validation of disaster context, NGO capacity, resource inventory, and operational constraints -- the foundation for all downstream optimization
---

## Purpose

This sub-skill collects, validates, and enriches the operational profile that all downstream sub-skills depend on. It combines user-provided inputs with live data from ReliefWeb (situation reports), HDX (population/road data), and GDACS (disaster alerts) to produce a fully verified, structured profile. Without a complete and accurate profile, the optimization models will produce misleading outputs.

The sub-skill applies a structured intake form, cross-references external data sources to verify or fill gaps in user inputs, and flags any unverified assumptions before handing off to sub-needs-assessment.

---

## Inputs

**From user (free text or structured):**
- Disaster type (earthquake, flood, cyclone, conflict displacement, drought, other)
- Location (country, admin level 1 / province, admin level 2 / district, GPS coordinates if available)
- Estimated affected population (total number; breakdown by location cluster if known)
- Available vehicles (number, type, payload capacity in MT or m^3, fuel type)
- Warehouse locations (GPS or admin area; capacity in MT; current stock levels if known)
- Total budget (USD)
- Partner NGOs present (list with names and known capacity)
- Time horizon (number of days for this distribution plan)
- Known access constraints (specific roads blocked, bridge outages, security incidents)
- Response phase (acute/immediate, early recovery, preparedness/pre-positioning)
- Any special population considerations (refugee vs. IDP vs. host community; camp vs. non-camp)

**From external sources (fetched by this sub-skill):**
- Latest ReliefWeb situation report for the disaster (WebFetch)
- GDACS event page (WebFetch) for disaster severity, affected area, and population at risk
- HDX population data for affected admin units (WebSearch/WebFetch)
- HDX road network / logistics infrastructure layer (WebSearch)

---

## Workflow

### Step PI-1: Initial User Data Collection
1.1 Present the structured intake form to the user. Ask for all mandatory fields first, then optional fields.
1.2 Mandatory fields: disaster_type, location (at minimum country + admin1), affected_population_total, time_horizon_days, response_phase.
1.3 Optional but important fields: vehicle inventory, warehouse inventory, budget, partner_agencies, access_constraints.
1.4 If the user provides a narrative description rather than structured data, extract the relevant information from the narrative and confirm with the user.

**Intake Form Template:**
```
DISASTER PROFILE INTAKE
========================
1. DISASTER TYPE: [earthquake / flood / cyclone / conflict / drought / other]
2. LOCATION:
   - Country: ___
   - Province/Admin1: ___
   - District/Admin2 (if known): ___
   - GPS Coordinates (if known): ___
3. AFFECTED POPULATION:
   - Total estimated: ___ persons
   - In camps/collective centres: ___ persons
   - Dispersed/host community: ___ persons
   - Children under 5 (if known): ___ %
   - Pregnant/lactating women (if known): ___ %
4. AVAILABLE RESOURCES:
   - Vehicles: ___ trucks (payload: ___ MT each); ___ motorcycles; ___ boats (if applicable)
   - Warehouse 1: [Location], capacity [___ MT], current stock [___]
   - Warehouse 2: [Location], capacity [___ MT], current stock [___]
   - Total budget: USD ___
5. PARTNER AGENCIES: [List names and known capacity]
6. TIME HORIZON: ___ days
7. RESPONSE PHASE: [acute / early-recovery / preparedness]
8. ACCESS CONSTRAINTS: [road names blocked, bridge outages, security zones]
9. SPECIAL CONSIDERATIONS: [cold chain needed? religious/cultural dietary restrictions?]
```

### Step PI-2: External Data Enrichment
2.1 **ReliefWeb fetch:** WebSearch "site:reliefweb.int [disaster type] [country] situation report 2026" to find the latest sitrep. WebFetch the top result to extract: official affected population figure, displacement figures, access constraints, cluster coordination status.
2.2 **GDACS fetch:** WebSearch "GDACS [country] [disaster type] alert" to find the event. WebFetch the GDACS event page to extract: disaster severity (orange/red), estimated population at risk, affected area polygon.
2.3 **HDX population data:** WebSearch "HDX population [country admin1] dataset" to find population data. Note the source and date.
2.4 **HDX logistics data:** WebSearch "HDX logistics infrastructure roads [country]" to find road network data. Note if roads layer has been updated post-disaster.
2.5 **Weather:** WebSearch "weather forecast [location] next 72 hours" to flag any severe weather that may affect early distribution operations.

### Step PI-3: Data Reconciliation & Gap Filling
3.1 Compare user-provided population figure with ReliefWeb/GDACS official figure. If they differ by > 20%, flag discrepancy and use the higher figure as conservative estimate.
3.2 If vehicle inventory is unknown, note as a gap -- sub-logistics-optimizer will need to use minimum available fleet.
3.3 If warehouse locations are unknown, flag as critical gap -- the optimizer cannot run without at least one supply node.
3.4 Assign each distribution location a road condition score:
  - 0 = Road confirmed destroyed/impassable
  - 1 = Road heavily damaged (4WD only, 2-3x normal travel time)
  - 2 = Road partially damaged (standard trucks, 1.5x normal travel time)
  - 3 = Road intact (normal travel time)
3.5 Build the location cluster map: group beneficiary locations into clusters of 500-5,000 persons each (adjust based on context). Assign GPS coordinates (centroid) or admin area reference to each cluster.

### Step PI-4: Profile Validation
4.1 Run through the mandatory field checklist. Any missing mandatory field -> return to Step PI-1 with a specific re-prompt.
4.2 Flag all unverified or assumed values with WARN:️ ASSUMPTION.
4.3 Calculate total supply capacity (sum of all warehouse stocks and procurement budget) vs. total estimated need (rough estimate using Sphere minimums x population x days). Flag if supply < need by > 40% -- this will require scope prioritization.
4.4 Note the access constraint summary: number of clusters with road score 0, 1, 2, 3.

### Step PI-5: Structure and Hand Off
5.1 Produce the structured profile block (JSON-like) for downstream sub-skills.
5.2 Present the profile summary to the user and ask for confirmation before proceeding.
5.3 Hand off to sub-needs-assessment.

---

## Outputs

**Structured Profile Block:**
```
DISASTER PROFILE
================
disaster_type: [type]
location:
  country: [name]
  admin1: [name]
  admin2: [name or "multiple"]
  coordinates: [lat, lon or "N/A"]
affected_population:
  total: [N]
  in_camps: [N or "unknown"]
  dispersed: [N or "unknown"]
  children_u5_pct: [% or "unknown"]
  plw_pct: [% or "unknown"]
location_clusters:
  - id: C1, location: [name], population: [N], road_score: [0-3], coordinates: [lat,lon]
  - id: C2, ...
resources:
  vehicles:
    - type: truck, payload_mt: [N], count: [N]
    - type: motorcycle, payload_mt: 0.1, count: [N]
  warehouses:
    - id: W1, location: [name], capacity_mt: [N], stock_mt: [N], coordinates: [lat,lon]
    - id: W2, ...
  budget_usd: [N]
partner_agencies:
  - name: [NGO name], capacity: [description]
time_horizon_days: [N]
response_phase: [acute / early-recovery / preparedness]
access_constraints:
  - type: road_blocked, location: [road name or cluster], severity: [high/medium/low]
  - type: security, location: [area], severity: [high/medium/low]
special_considerations: [list]
data_sources:
  - ReliefWeb: [URL]
  - GDACS: [URL or "N/A"]
  - HDX: [URL]
assumptions:
  - [WARN:️ ASSUMPTION: description]
supply_vs_need_flag: [OK / WARNING: supply < estimated need by X%]
```

**Profile Summary Card** (for user confirmation):
A 10-line plain-language summary of the key profile parameters for user review.

---

## Quality Gate

Before handing off to sub-needs-assessment, verify:

- [ ] **QG-1:** All 5 mandatory fields populated (disaster_type, location_country, affected_population_total, time_horizon_days, response_phase)
- [ ] **QG-2:** At least one data source consulted from ReliefWeb, GDACS, or HDX -- no population figure used without source attribution
- [ ] All WARN:️ ASSUMPTION flags are documented in the profile
- [ ] At least one warehouse location defined (sub-logistics-optimizer cannot run without a supply node)
- [ ] Road condition scores assigned to all location clusters
- [ ] Supply vs. need flag calculated; user alerted if WARNING

If QG-1 fails: re-prompt user with the specific missing fields highlighted.
If QG-2 fails: note clearly that all downstream estimates are unverified; recommend field data collection as a parallel action.
