# PROJECT-detail.md -- Skill #242: Disaster Relief Distribution Simulation & Optimization (NGO)

## Executive Summary

This skill is a structured harness workflow for humanitarian NGO operations managers and logistics coordinators who need to simulate, optimize, and operationalize emergency disaster relief distribution. Grounded in operations research (Vehicle Routing Problem, Linear Programming), game theory (Nash equilibrium, Stackelberg games), OCHA Humanitarian Principles, and Sphere Standards, the skill transforms raw disaster context inputs into a professional-grade operational distribution plan complete with quantified needs, optimized routes, delivery schedules, and scenario sensitivity analysis.

The skill continuously self-improves by crawling ReliefWeb situation reports, OCHA FTS updates, Humanitarian Data Exchange (HDX) datasets, and peer-reviewed humanitarian logistics journals -- ensuring its recommendations reflect the current state of disaster response in the field.

---

## Problem Statement

### Domain Context
Emergency disaster relief distribution is one of the most complex logistics challenges in existence. Unlike commercial supply chains, humanitarian logistics operates under extreme uncertainty, compressed timelines, degraded infrastructure, partial information, multi-stakeholder coordination demands, and a moral imperative to prioritize human life over operational efficiency. The consequences of failure are measured in preventable deaths.

Key structural problems NGOs face:
1. **Needs quantification gap:** Without Sphere Standards-based calculation, NGO teams underestimate or mis-prioritize needs -- food rations calculated for average adults miss the needs of malnourished children; water quantities ignore hygiene needs.
2. **Route optimization failure:** Ad hoc route planning in damaged road networks leads to duplicated effort in easy-access areas, while hard-to-reach communities remain unreached.
3. **Multi-agency coordination failure:** When 20 NGOs arrive simultaneously with aid, they compete for the same transport corridors and beneficiary registration lists, creating chaos and duplication.
4. **Scenario blindness:** Distribution plans fail when one road closes, one truck breaks down, or demand surges by 30% -- because no contingency modeling was done.
5. **Information gap:** Terrain and weather data are not integrated into logistics planning, leading to convoys arriving at flooded crossings.

### Motivation
Operations research and game theory provide mature, rigorous solutions to all five problems -- but their application to humanitarian logistics is unevenly adopted. This skill operationalizes these methods in a Claude harness so any NGO team can use them without a PhD in optimization.

---

## Target Users & Use Cases

### Primary Users
- NGO Operations Managers (country/field level)
- Humanitarian Logistics Coordinators (UNHCR, WFP, MSF, IRC, Oxfam, etc.)
- OCHA Cluster Coordinators (Logistics, Food Security, WASH clusters)
- Disaster Risk Reduction (DRR) planners for pre-positioning scenarios

### Trigger Examples

| User says | Skill does |
|-----------|-----------|
| "Earthquake in Sulawesi, 45,000 displaced, 3 trucks, 2 warehouses, 7-day window" | Runs full intake -> needs assessment -> route optimization -> scenario analysis -> operational plan |
| "We have $200,000 in cash and need to decide between vouchers, cash transfers, or in-kind aid for flood victims in Bangladesh" | Cash vs. in-kind trade-off analysis using Sphere + cost-effectiveness frameworks |
| "What happens to our plan if Road 7 closes and our budget is cut by 20%?" | Runs simulation engine on those constraints and returns sensitivity analysis + contingency plan |
| "15 NGOs are all trying to reach the same 3 districts -- how do we coordinate?" | Nash equilibrium multi-agency coordination model |
| "We need to pre-position supplies before typhoon season in Philippines" | Pre-positioning optimization with INFORM risk data |

---

## Harness Architecture

```
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+          /disaster-relief-distribution-simulation (main.md)         +
+                    Role: Humanitarian Logistics Expert               +
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                               +
              ++++++++++++++++++++++++++++++++++
              +     STAGE 1: INTAKE             +
              +   sub-profile-intake.md         +
              + - Disaster type & location      +
              + - Affected population (size,    +
              +   demographics, locations)      +
              + - Available resources           +
              +   (vehicles, warehouses, budget)+
              + - Partner NGOs & capacity       +
              + - Time horizon                  +
              +++++++++++++++++++++++++++++++++++
                               +
              ++++++++++++++++++++++++++++++++++
              +   STAGE 2: NEEDS ASSESSMENT     +
              +   sub-needs-assessment.md       +
              + - Sphere Standards minimums     +
              + - IPC food security class       +
              + - Beneficiary prioritization    +
              + - Needs matrix by sector        +
              +++++++++++++++++++++++++++++++++++
                               +
              ++++++++++++++++++++++++++++++++++
              +  STAGE 3: LOGISTICS OPTIMIZER   +
              +  sub-logistics-optimizer.md     +
              + - VRP route optimization        +
              + - LP resource allocation        +
              + - Warehouse siting model        +
              + - Nash equilibrium coordination +
              + - Delivery schedule output      +
              +++++++++++++++++++++++++++++++++++
                               +
              ++++++++++++++++++++++++++++++++++
              +  STAGE 4: SIMULATION ENGINE     +
              +  sub-simulation-engine.md       +
              + - Scenario: road blocked        +
              + - Scenario: budget cut          +
              + - Scenario: demand surge        +
              + - Scenario: weather event       +
              + - Sensitivity analysis          +
              + - Contingency recommendations   +
              +++++++++++++++++++++++++++++++++++
                               +
              ++++++++++++++++++++++++++++++++++
              +   QUALITY GATE (main harness)   +
              + - Sphere Standards compliance   +
              + - OCHA Humanitarian Principles  +
              + - Quantitative traceability     +
              + - Safety/access risk flagging   +
              +++++++++++++++++++++++++++++++++++
                               +
              ++++++++++++++++++++++++++++++++++
              +  FINAL DELIVERABLE (main.md)    +
              + - Operational Distribution Plan +
              + - Optimized Route Schedules     +
              + - Scenario Analysis Report      +
              + - IASC Cluster Coordination Rec +
              +++++++++++++++++++++++++++++++++++
```

---

## Full Sub-Skill Catalog

### 1. `sub-profile-intake.md`
- **Purpose:** Structured intake of all contextual parameters needed for optimization
- **Inputs:** User-provided disaster description (free text or structured form)
- **Outputs:** Validated profile JSON/structured data block including: disaster_type, location (coordinates/admin levels), affected_population (total, by demographic, by location cluster), resources (vehicles by type/capacity, warehouses by location/capacity, total_budget), partner_agencies (list + capacity), time_horizon (days), access_constraints (road damage level, security incidents), response_phase (acute/immediate/early-recovery)
- **Tools:** WebSearch (HDX for population/road data), WebFetch (ReliefWeb situation reports for current access constraints)
- **Quality Gate:** All mandatory fields populated; population figures sourced from HDX or official government data; access constraints verified against latest ReliefWeb sitrep

### 2. `sub-needs-assessment.md`
- **Purpose:** Quantify minimum humanitarian needs per sector using Sphere Standards and IPC classification
- **Inputs:** Profile from sub-profile-intake (population size, demographics, location clusters, response_phase)
- **Outputs:** Needs matrix (quantity of each item type by location cluster by priority tier), beneficiary priority ranking (Tier 1: highest vulnerability; Tier 2: general displaced; Tier 3: host community), sector coverage recommendations (WASH, food security, shelter, health), IPC phase classification per location cluster, total volume/weight tonnage required per sector
- **Tools:** Read (SECOND-KNOWLEDGE-BRAIN.md for Sphere minimums), WebSearch (IPC mapping data for the affected area), WebFetch (WFP Situation Report if available)
- **Quality Gate:** Every quantity traceable to Sphere Standards minimum (liters/person/day, kcal/person/day, m^2/person); IPC classification cited; vulnerable group weighting applied

### 3. `sub-logistics-optimizer.md`
- **Purpose:** Apply VRP, LP, and game theory to generate an optimized multi-day distribution plan
- **Inputs:** Needs matrix from sub-needs-assessment, resource inventory from sub-profile-intake, road network data, warehouse locations
- **Outputs:** Optimized route plan per vehicle per day (waypoints, load manifest, estimated time), warehouse replenishment schedule, distribution point locations and coverage zones, efficiency metrics (% beneficiaries reached per day, cost per beneficiary, vehicle utilization rate), multi-agency task division (Nash equilibrium solution if multiple NGOs present), cash vs. in-kind modality recommendation
- **Tools:** Read (SECOND-KNOWLEDGE-BRAIN.md for VRP algorithm references), WebSearch (OpenStreetMap road data for affected area, HDX logistics infrastructure layer)
- **Quality Gate:** Total planned coverage >= 80% of Tier 1 beneficiaries within 72 hours; all routes validated against current road access data; cost-per-beneficiary calculated and benchmarked against sector norms

### 4. `sub-simulation-engine.md`
- **Purpose:** Stress-test the optimized plan against realistic constraint scenarios and generate contingency options
- **Inputs:** Optimized distribution plan from sub-logistics-optimizer, key constraint parameters (budget, road network, vehicle fleet, demand figures)
- **Outputs:** Scenario comparison table (baseline vs. each scenario: % reach, cost, time), sensitivity ranking (which constraints have the largest impact on plan performance), recommended contingency plans (one per high-impact constraint), go/no-go decision framework for real-time plan adjustment, weather integration (likely road closures from forecast)
- **Tools:** WebSearch (weather forecasts for affected area, OpenWeatherMap API, GDACS alerts), WebFetch (latest GDACS event page for active disaster), Read (SECOND-KNOWLEDGE-BRAIN.md for disaster-type-specific disruption patterns)
- **Quality Gate:** Minimum 4 scenarios simulated; sensitivity analysis covers at least: road access, budget, vehicle availability, demand; contingency plan for each scenario rated by feasibility and lead time

---

## Skill File Format Specification

### Frontmatter Schema (all skill files)
```yaml
---
name: <slug>
description: <one-line summary for /help display>
---
```

### main.md Required Sections
1. `## Role & Persona` -- who Claude becomes
2. `## Workflow` -- numbered steps, each referencing which sub-skill is invoked
3. `## Sub-skills Available` -- list of sub-skill files with one-liner
4. `## Tools` -- tool list with usage context
5. `## Output Format` -- exact structure of the final deliverable
6. `## Quality Gates` -- checklist Claude must pass before presenting final output

### Sub-skill Required Sections
1. `## Purpose` -- what this sub-skill accomplishes
2. `## Inputs` -- expected inputs (from user or prior sub-skills)
3. `## Workflow` -- numbered steps
4. `## Outputs` -- structured outputs this sub-skill produces
5. `## Quality Gate` -- pass criteria before handing off to next stage

---

## E2E Execution Flow

```
1. User invokes /disaster-relief-distribution-simulation

2. main.md activates Role & Persona (Humanitarian Logistics Expert)

3. Invoke sub-profile-intake:
   a. Present structured intake form to user (disaster type, location, population, resources, time)
   b. WebSearch for HDX population/road data to supplement user inputs
   c. WebFetch latest ReliefWeb sitrep for the affected area
   d. Validate and structure the profile
   e. QG: all mandatory fields populated -> if not, re-prompt user

4. Invoke sub-needs-assessment:
   a. Apply Sphere Standards minimums to calculate quantities by sector
   b. IPC food security classification for affected area
   c. Prioritize beneficiary groups into 3 tiers
   d. Build needs matrix (item x location x priority tier x quantity)
   e. QG: every quantity citable to Sphere -> if not, flag assumption

5. Invoke sub-logistics-optimizer:
   a. Map distribution points to beneficiary clusters
   b. Apply VRP to plan routes for each vehicle per day
   c. Apply LP for resource allocation across warehouses and distribution points
   d. If multi-agency: compute Nash equilibrium coordination strategy
   e. Compute efficiency metrics
   f. Recommend cash vs. in-kind modality
   g. QG: >= 80% Tier 1 coverage within 72h, cost benchmarked -> escalate if infeasible

6. Invoke sub-simulation-engine:
   a. Define baseline = optimized plan from Step 5
   b. Run 4+ constraint scenarios
   c. Rank sensitivity of constraints
   d. Generate contingency plan per high-impact constraint
   e. Integrate weather forecast for next 72h
   f. QG: all 4 scenario types covered, weather checked

7. Quality Gate Review (main harness):
   a. Humanitarian principles check (impartiality -- Tier 1 prioritized without bias)
   b. Sphere Standards compliance check (all minimums met in plan)
   c. Quantitative traceability (every number linked to source or formula)
   d. Access/safety risk flag (any route through high-security-risk areas flagged)
   e. If any QG fails: return to relevant sub-skill to remediate

8. Synthesize Final Deliverable:
   a. Section 1: Situation Summary (disaster context, affected population, response window)
   b. Section 2: Needs Assessment Summary (needs matrix, IPC phase, priority tiers)
   c. Section 3: Optimized Distribution Plan (route schedules, warehouse plan, delivery calendar)
   d. Section 4: Multi-Agency Coordination (Nash equilibrium task division if applicable)
   e. Section 5: Scenario Analysis (table + contingency plans)
   f. Section 6: Recommendations (top 5 actionable recommendations with rationale)
   g. Section 7: Knowledge Sources (all citations from ReliefWeb, Sphere, HDX, academic)
```

---

## SECOND-KNOWLEDGE-BRAIN Integration

### Knowledge Sources
| Source | URL | Crawl Method | Frequency |
|--------|-----|-------------|-----------|
| ReliefWeb Situation Reports | reliefweb.int/updates?format=sitrep | crawl4ai -> parse latest sitreps | Weekly |
| HDX Datasets (logistics) | data.humdata.org/dataset?tags=logistics | crawl4ai -> new dataset metadata | Weekly |
| OCHA FTS | fts.unocha.org | crawl4ai -> funding flow updates | Weekly |
| ALNAP Learning | alnap.org/resources | crawl4ai -> new evaluations/reports | Weekly |
| Sphere Standards | spherehandbook.org | Read on-demand (stable) | Monthly |
| Emerald/JHL | emerald.com/insight/publication/issn/2042-6747 | crawl4ai -> new article abstracts | Weekly |
| GDACS | gdacs.org/alerts | crawl4ai -> active disaster alerts | Daily |
| ArXiv (math.OC, cs.RO) | arxiv.org/search/?searchtype=all&query=humanitarian+logistics | crawl4ai -> new preprints | Weekly |

### Append Format (SECOND-KNOWLEDGE-BRAIN.md)
```markdown
### [YYYY-MM-DD] Entry: {title}
- **Source:** {source_name} | {url}
- **Type:** {sitrep | dataset | paper | report}
- **Relevance Score:** {0-10}
- **Key Finding:** {1-2 sentence summary}
- **DOI/ID:** {doi or unique id for deduplication}
```

---

## Quality Gates Definition

A quality gate is a hard stop -- Claude must resolve the failure before proceeding to the next stage.

| Gate ID | Stage | Condition | Failure Action |
|---------|-------|-----------|---------------|
| QG-1 | post-intake | All mandatory profile fields populated | Re-prompt user for missing fields |
| QG-2 | post-intake | Population figures sourced from official/HDX data | Flag assumptions; request user confirmation |
| QG-3 | post-needs | Every quantity traceable to Sphere Standards minimum | Flag as assumption; mark with WARN:️ |
| QG-4 | post-needs | IPC phase cited for food security sector | Default to Phase 3 with warning if unavailable |
| QG-5 | post-optimizer | >= 80% Tier 1 beneficiaries reachable within 72h | Escalate: alert user, offer resource increase or scope reduction |
| QG-6 | post-optimizer | Cost-per-beneficiary calculated and benchmarked | Proceed with flagged caveat if benchmark data unavailable |
| QG-7 | post-simulation | Minimum 4 scenarios simulated | Do not skip any scenario type |
| QG-8 | post-simulation | Weather forecast integrated for next 72h | Use GDACS/weather API; flag if unavailable |
| QG-9 | final | All OCHA Humanitarian Principles satisfied | Flag any impartiality concern in the output |
| QG-10 | final | All citations traceable to named source | No unsourced claims in final deliverable |

---

## Test Scenarios

See `tests/test-scenarios.md` for 5+ detailed test scenarios.

---

## Key Design Decisions

1. **Sphere Standards as the non-negotiable floor:** All needs calculations use Sphere minimums as a hard lower bound -- not aspirational targets. The skill never recommends distributions below Sphere minimums.
2. **Humanitarian imperative over efficiency:** When efficiency (cost-minimization) conflicts with humanitarian imperative (reach most vulnerable first), the skill always prioritizes the humanitarian imperative and flags the trade-off explicitly.
3. **VRP simplified for field use:** Full VRP is NP-hard -- the skill uses Clarke-Wright Savings Algorithm heuristic (fast, well-understood, field-tested) rather than exact solvers, ensuring practicality for operations managers without a mathematical background.
4. **Nash equilibrium for multi-agency coordination:** When multiple NGOs are present, the skill models coordination as a non-cooperative game and computes the Nash equilibrium assignment to avoid duplicating effort in accessible areas at the expense of hard-to-reach communities.
5. **Cash vs. in-kind modality decision:** The skill evaluates cash-based interventions against in-kind aid using a structured rubric (market functionality, security, beneficiary preference, administrative capacity) before defaulting to either modality.
6. **Real-time data integration:** The skill always attempts to pull current data (weather, road status, sitreps) before generating any plan -- and clearly signals when falling back to SECOND-KNOWLEDGE-BRAIN cached knowledge.
7. **IASC cluster system integration:** Outputs are structured to align with the IASC cluster system (Logistics, Food Security, WASH, Shelter, Health clusters) so they can be directly presented in cluster coordination meetings.
8. **Pre-positioning mode:** The skill supports both acute response (post-disaster) and preparedness (pre-positioning before predicted events -- typhoons, monsoon floods) via the response_phase field in the profile.
