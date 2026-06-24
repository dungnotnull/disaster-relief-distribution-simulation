---
name: disaster-relief-distribution-simulation/sub-needs-assessment
description: Quantify humanitarian needs using Sphere Standards minimums and IPC classification; segment beneficiaries into priority tiers; produce a needs matrix for logistics optimization
---

## Purpose

This sub-skill transforms the disaster profile from sub-profile-intake into a precise, Sphere Standards-compliant quantification of what needs to be distributed, to whom, where, and when. It produces the needs matrix -- the fundamental demand-side input for the logistics optimizer. Without accurate needs quantification, any optimization model will optimize toward the wrong target.

The sub-skill applies Sphere Handbook (2018) minimum standards as the non-negotiable floor for every quantity. It uses IPC food security classification to determine food aid severity. It segments beneficiaries into 3 vulnerability-based priority tiers and assigns quantities by tier and location cluster.

---

## Inputs

**From sub-profile-intake:**
- affected_population (total, by cluster, demographics: children u5 %, PLW %)
- location_clusters (id, population, road_score)
- response_phase (acute / early-recovery / preparedness)
- time_horizon_days
- special_considerations (cold chain, dietary restrictions)
- disaster_type (informs which sectors are most critical)

**From external sources (fetched by this sub-skill):**
- IPC food security phase map for the affected area (WebSearch: "IPC [country] [admin1] food security phase 2025 2026")
- WFP Situation Report (if available) for nutrition status data
- UNICEF WASH situation data if available
- SECOND-KNOWLEDGE-BRAIN.md Sphere Standards section (Read)

---

## Workflow

### Step NA-1: Beneficiary Tier Segmentation
1.1 Calculate total beneficiaries by tier based on profile demographics:
  - **Tier 1 (Highest Vulnerability):**
    - Severely malnourished children (SAM/MAM): estimated at 2-5% of children u5 in IPC Phase 3+
    - Children under 5 years: [children_u5_pct] x [total population]
    - Pregnant and lactating women (PLW): [plw_pct] x [total population]; if unknown, use 5% of total
    - Unaccompanied minors: if camp context, estimate 3-5% of camp population
    - Elderly (65+): estimate 5-8% of total if not provided
    - Persons with disabilities: estimate 15% of total per WHO global prevalence if not provided
    - Persons with acute medical conditions: estimate 2% of total in acute disaster
    - **Apply deduplication:** Total Tier 1 = sum of above but cap at realistic estimate (typical: 20-35% of total population in acute disaster)
  - **Tier 2 (General Displaced):** [total_population] x (1 - Tier1_pct - host_community_pct)
  - **Tier 3 (Host Community):** affected host community members; estimate 15-25% of total if camp context
1.2 Distribute tier populations across location clusters proportionally (unless cluster-specific demographic data is available).
1.3 Flag any cluster with road_score = 0 as "Tier 1 CRITICAL -- unreachable, requires alternative access mode (air, boat, porter)."

### Step NA-2: IPC Food Security Classification
2.1 WebSearch for "IPC [country] [admin1] [year] food security classification" to find current IPC phase for the affected area.
2.2 Map IPC phases to response actions:
  - Phase 1-2: General food security monitoring; no emergency food distribution required
  - Phase 3 (Crisis): Emergency general food distribution; prioritize Tier 1 for selective feeding
  - Phase 4 (Emergency): Urgent general food distribution + therapeutic feeding (RUTF) for SAM children
  - Phase 5 (Famine): Maximum mobilization; blanket supplementary feeding for all under-5 + PLW; RUTF for all SAM
2.3 If IPC data is unavailable: default to Phase 3 and flag as WARN:️ ASSUMPTION: IPC Phase 3 assumed -- verify with WFP/FAO country office.
2.4 Note IPC phase in the output for all food security sector calculations.

### Step NA-3: WASH Needs Calculation (Sphere Standards)
3.1 Apply Sphere minimum standards for water:
  - Survival minimum (acute emergency, day 1-3): 7.5 L/person/day
  - Standard minimum (day 4+): 15 L/person/day
  - **For this plan, use:** 15 L/person/day as the planning standard; flag if only survival minimum can be met
3.2 Calculate:
  - Daily water requirement: 15 L x [total population] = [X] liters/day
  - Total water volume for time horizon: [X] L/day x [N] days = [Y] liters total
  - If water trucking: volume per truck = truck payload / 1.0 kg/L (water density)
3.3 Sanitation: 1 latrine unit per 20 persons (gender-separated). Calculate: [total_population] / 20 = [N] latrine units
3.4 Hygiene kits: 1 kit per household (average 5 persons per HH). [total_population] / 5 = [N] hygiene kits
3.5 Convert to weight for logistics: hygiene kit avg weight = 4 kg. [N] kits x 4 kg = [Y] MT

### Step NA-4: Food & Nutrition Needs Calculation (Sphere Standards)
4.1 General food ration: 2,100 kcal/person/day (Sphere minimum)
  - Standard WFP emergency ration (as reference): 450g cereals + 60g pulses + 25g oil + 15g sugar = 2,100 kcal/person/day
  - Adjust for IPC phase: Phase 4-5 -> add supplementary ration of 500 kcal/person/day for all u5 and PLW
4.2 Calculate daily food quantities:
  - Cereals: 0.45 kg/person/day x [total population] = [X] kg/day
  - Pulses: 0.06 kg/person/day x [total population] = [X] kg/day
  - Edible oil: 0.025 kg/person/day x [total population] = [X] kg/day
  - Sugar: 0.015 kg/person/day x [total population] = [X] kg/day
  - Salt: 0.005 kg/person/day x [total population] = [X] kg/day
  - Total food weight/day: sum of above
4.3 Therapeutic nutrition (if IPC Phase 3+):
  - RUTF sachets for SAM children: 3 sachets/day x [SAM_children_count] = [X] sachets/day
  - RUSF/CSB++ for MAM children and PLW: 200g/person/day x [MAM+PLW count] = [X] kg/day
  - Note: RUTF requires cold chain if temperature > 30 degC -- flag in special_considerations
4.4 Total food + nutrition weight per day: [X] MT/day

### Step NA-5: Shelter & NFI Needs Calculation (Sphere Standards)
5.1 Shelter:
  - Covered floor area: 3.5 m^2/person x [total displaced population] = [X] m^2 minimum
  - Tarpaulins: 1 per household (HH) for emergency shelter; [total_population / 5] tarpaulins
  - Tent: 1 per 2 households in camp context if family tents used
5.2 NFI package (standard WFP/UNHCR): 1 kit per household containing:
  - Blankets: 2 per HH (more in cold climate)
  - Plastic sheeting: 1 x 4m x 6m per HH
  - Cooking set: 1 per HH (pots, plates, cups, spoons, jerry can)
  - Sleeping mat: 2 per HH
  - Estimated weight per NFI kit: 18-22 kg -> use 20 kg/kit
  - [total_population / 5] HH x 20 kg = [Y] MT for NFI
5.3 Total shelter + NFI weight: [Y] MT (one-time delivery)

### Step NA-6: Health Supply Needs
6.1 Basic health supplies (IEHK -- Interagency Emergency Health Kit):
  - 1 IEHK basic unit per 1,000 population for acute emergency
  - 1 IEHK supplementary unit per 10,000 population
  - IEHK basic unit weight: ~50 kg; supplementary: ~500 kg
  - [total_population / 1,000] x 50 kg + [total_population / 10,000] x 500 kg = [X] kg
6.2 Oral rehydration salts (ORS): 10 sachets per person at-risk of cholera/diarrhea (especially relevant for flood/cyclone contexts)
6.3 Cold chain requirement: Note if vaccines or cold-chain medicines are needed (requires refrigerated transport)

### Step NA-7: Build the Needs Matrix
7.1 Aggregate all sector needs into a unified needs matrix.
7.2 Apply priority tier multipliers to distribution sequencing:
  - Tier 1 clusters: first delivery, full Sphere quantity
  - Tier 2 clusters: second delivery, full Sphere quantity
  - Tier 3 clusters: third delivery, full Sphere quantity (subject to remaining budget)
  - If budget insufficient for all tiers: apply LP prioritization (cover Tier 1 fully first, then Tier 2)
7.3 Calculate total weight/volume by commodity and by cluster for each delivery cycle.
7.4 Flag any item requiring special handling: cold chain (RUTF, vaccines), hazmat (bleaching powder), oversize (tarpaulins).

### Step NA-8: Final Output Assembly
8.1 Write the needs matrix table.
8.2 Calculate total supply weight/volume needed per day and cumulatively.
8.3 Check if available warehouse stock + procurement budget covers the total need. If not, calculate the gap and flag.
8.4 Confirm Sphere Standards compliance for every sector.

---

## Outputs

**Needs Matrix (primary output):**
```
NEEDS MATRIX -- [Disaster Name] -- [Date]
IPC Phase: [X] ([area name])
Response Phase: [acute / early-recovery]

BENEFICIARY TIERS:
  Tier 1 (Highest Vulnerability): [N] persons ([X]% of total)
  Tier 2 (General Displaced): [N] persons ([X]% of total)
  Tier 3 (Host Community): [N] persons ([X]% of total)
  TOTAL: [N] persons

DAILY NEEDS BY SECTOR (per 1,000 persons basis):
Sector    | Item          | Per-person/day | Standard Source   | Daily (total pop) | Period Total
WASH      | Water         | 15 L           | Sphere 2018 section 5.1  | [X] kL/day        | [X] kL
WASH      | Latrine units | 1/20 persons   | Sphere 2018 section 6.2  | [N] units (once)  | [N] units
WASH      | Hygiene kits  | 1/5 persons    | Sphere 2018 section 7    | [N] kits (once)   | [N] kits
Food      | Cereals       | 450 g          | Sphere 2018 section 8.1  | [X] MT/day        | [X] MT
Food      | Pulses        | 60 g           | Sphere 2018 section 8.1  | [X] MT/day        | [X] MT
Food      | Edible oil    | 25 g           | Sphere 2018 section 8.1  | [X] MT/day        | [X] MT
Nutrition | RUTF          | 3 sachets/SAM  | CMAM Protocol     | [X] sachets/day   | [X] sachets
Shelter   | Tarpaulin     | 1/HH           | Sphere 2018 section 11   | [N] units (once)  | [N] units
NFI       | NFI Kit       | 1/HH           | UNHCR NFI Std     | [N] kits (once)   | [N] kits
Health    | IEHK Basic    | 1/1,000        | WHO IEHK 2017     | [N] units (once)  | [N] units

CLUSTER-LEVEL BREAKDOWN:
Cluster | Pop  | Tier | Road | Water/day | Food/day | NFI (once) | Priority
C1      | [N]  | 1    | 2    | [X] kL    | [X] MT   | [N] kits   | DAY 1
C2      | [N]  | 1    | 0    | [X] kL    | [X] MT   | [N] kits   | WARN:️ UNREACHABLE -- alt mode needed
C3      | [N]  | 2    | 3    | [X] kL    | [X] MT   | [N] kits   | DAY 2-3
...

TOTAL SUPPLY REQUIREMENT:
  Total weight to be delivered (food + NFI): [X] MT
  Total water volume: [X] kL
  Budget required at current norms: USD [X]
  Budget available: USD [X]
  Gap: [X] MT / USD [X] WARN:️ or OK Within budget

SPHERE STANDARDS COMPLIANCE:
  WASH: OK Meets 15 L/person/day standard | WARN:️ Exception: [if any]
  Food: OK Meets 2,100 kcal/person/day | WARN:️ Exception: [if any]
  Shelter: OK Meets 3.5 m^2/person | WARN:️ Exception: [if any]
  Health: OK IEHK units calculated per 1,000 | WARN:️ Exception: [if any]

DATA SOURCES:
  IPC Phase: [URL or "WARN:️ ASSUMPTION: Phase 3 assumed -- not confirmed"]
  Population: [Source from profile]
  Sphere Standards: Sphere Handbook 2018, ISBN 978-1-908176-40-4
```

---

## Quality Gate

Before handing off to sub-logistics-optimizer, verify:

- [ ] **QG-3:** Every quantity in the needs matrix is traceable to Sphere Standards minimum or a cited source; all assumptions flagged with WARN:️
- [ ] **QG-4:** IPC food security phase cited for food sector; if unavailable, Phase 3 assumed and flagged
- [ ] Total daily supply weight calculated and compared against available truck fleet capacity x time horizon
- [ ] All clusters assigned to a delivery priority (Day 1, Day 2-3, Day 4-7, or "UNREACHABLE -- alt mode")
- [ ] Any cold chain, hazmat, or oversize items flagged for special handling
- [ ] Budget vs. total need gap calculated and flagged if supply < need

If any Sphere minimum cannot be met within available resources: flag explicitly with WARN:️ BELOW SPHERE MINIMUM and escalate to user before proceeding to optimization.
