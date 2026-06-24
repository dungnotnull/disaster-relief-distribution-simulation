---
name: disaster-relief-distribution-simulation/sub-simulation-engine
description: Stress-test the optimized distribution plan through multi-scenario simulations, sensitivity analysis, and weather integration -- producing contingency plans for each high-impact constraint
---

## Purpose

This sub-skill stress-tests the distribution plan produced by sub-logistics-optimizer against realistic constraint failures and disruptions. Disaster response plans routinely fail because they are built for ideal conditions: a road that was passable becomes blocked, a budget is cut by donors, demand surges when new population groups are identified, and a weather event closes the only access corridor. Without scenario analysis, operations managers discover these failures in the field -- too late to adapt.

This sub-skill runs a minimum of 4 defined scenario simulations, produces a sensitivity ranking of constraints, and generates specific, actionable contingency plans. It also integrates a 72-hour weather forecast to flag near-term route disruption risks.

---

## Inputs

**From sub-logistics-optimizer:**
- Optimized distribution plan (baseline plan): vehicle routes, load manifests, warehouse schedule, efficiency metrics
- Key baseline metrics: % Tier 1 coverage Day 1/3, cost/beneficiary, total tonnage

**From sub-profile-intake:**
- access_constraints (existing road blocks, security constraints)
- resources (vehicles, warehouses, budget)
- location_clusters (id, population, road_score)

**From sub-needs-assessment:**
- needs_matrix (total demand by cluster)
- Total beneficiary population by tier

**From external sources:**
- 72-hour weather forecast: WebSearch "weather forecast [location] precipitation wind 72 hours 2026"
- GDACS active alerts: WebFetch "https://gdacs.org/alerts/default.aspx" for latest disaster severity
- ReliefWeb for access updates: WebSearch "site:reliefweb.int [country] [disaster] access roads 2026"

---

## Workflow

### Step SE-1: Establish Baseline Metrics
1.1 Record the baseline plan performance metrics:
  - B1: % Tier 1 beneficiaries reached on Day 1
  - B2: % Tier 1 beneficiaries reached by Day 3
  - B3: % Total beneficiaries reached by end of time horizon
  - B4: Cost per beneficiary (USD)
  - B5: Total cost (USD)
  - B6: Days to full Tier 1 coverage
1.2 Identify the top 3 most-used roads in the baseline plan (highest traffic routes by vehicle x day).
1.3 Identify the highest-cost budget items in the plan (fuel, procurement, per-diem).

### Step SE-2: Scenario A -- Road Blocked
**Scenario:** The single highest-traffic road in the baseline plan is completely blocked (road_score -> 0).
2.1 Remove all routes that pass through the blocked road from the baseline plan.
2.2 Identify which location clusters are now unreachable (all routes to them required the blocked road).
2.3 Attempt rerouting:
  - Can affected clusters be reached via a longer alternative route? If so, calculate new travel time (add delay factor).
  - Can a motorcycle/boat/porter relay be added for critical Tier 1 clusters?
2.4 Recalculate efficiency metrics with the rerouted plan:
  - New % Tier 1 reached by Day 1 and Day 3
  - New cost/beneficiary (rerouting adds fuel + time cost)
  - Number of clusters made temporarily unreachable
2.5 Generate Contingency Plan A:
  - Specific alternative routes to use
  - Clusters requiring alt transport (motorcycle, boat)
  - Lead time to implement (hours) -- how quickly can the route change be communicated to drivers?
  - Decision trigger: "If [road name] is reported blocked, switch to Contingency Plan A immediately"

### Step SE-3: Scenario B -- Budget Cut (25%)
**Scenario:** Total available budget is reduced by 25% from the baseline (simulate donor funding shortfall or procurement price increase).
3.1 Reduce budget_usd by 25%. Calculate the resulting maximum sustainable supply volume.
3.2 Apply LP re-optimization with reduced budget:
  - Maintain Tier 1 at full Sphere quantities (non-negotiable)
  - Reduce Tier 2 quantities if needed (first: reduce frequency; second: reduce quantity toward Sphere minimum)
  - Reduce Tier 3 quantities or defer to later period
3.3 Evaluate modality switch: Would a switch to cash-based intervention (if market functionality allows) reduce costs sufficiently to maintain coverage?
3.4 Recalculate efficiency metrics:
  - New % total coverage (Tier 1 must be maintained; Tier 2-3 may drop)
  - New cost/beneficiary
  - Population left uncovered vs. baseline
3.5 Generate Contingency Plan B:
  - Specific scope reduction steps (which clusters deferred, which quantities reduced)
  - Modality switch recommendation if cost-saving
  - Emergency donor outreach recommendation (include OCHA FTS gap funding angle)
  - Decision trigger: "If [funding level] drops below USD [threshold], implement Plan B"

### Step SE-4: Scenario C -- Demand Surge (30%)
**Scenario:** Total affected population increases by 30% above baseline estimate (new displacement wave, previously unregistered population discovered).
4.1 Increase all demand figures in the needs matrix by 30%.
4.2 Attempt to re-optimize with existing resources:
  - Can the existing fleet serve 30% more demand by adding delivery days or increasing loads?
  - Are warehouses sufficient to store additional supplies?
4.3 Calculate the additional supply gap: additional procurement needed (quantity and estimated cost).
4.4 Calculate additional vehicle trips needed vs. available fleet.
4.5 Determine: Can 30% surge be absorbed within current resources? If no, identify the breakpoint (at what % surge does Tier 1 coverage fall below 80%?).
4.6 Generate Contingency Plan C:
  - Emergency procurement quantities and estimated lead time (WFP Pipeline request / local market)
  - Temporary fleet augmentation options (vehicle rental, WFP common services request)
  - Beneficiary registration surge response (additional teams, Kobo registration forms)
  - Decision trigger: "If registration exceeds [N] persons, initiate additional procurement within 24 hours"

### Step SE-5: Scenario D -- Weather Event
**Scenario:** A significant weather event (heavy rain, flood, cyclone approach) disrupts road access during the distribution window.
5.1 Fetch 72-hour weather forecast for the affected area via WebSearch: "weather forecast [location] [country] precipitation wind speed 72 hours"
5.2 Apply road closure probability thresholds:
  - Precipitation > 50mm/24h: Low-lying roads likely flooded (road_score 2 -> 0 for routes crossing floodplains)
  - Wind > 80 km/h: Routes in coastal areas or exposed ridgelines suspended
  - Flash flood warning active: All routes in flood zone suspended until all-clear
5.3 If active GDACS alert for the area: WebFetch GDACS event page for updated severity and affected zones.
5.4 Model the road closures as in Scenario A but use the weather-derived road_score overrides.
5.5 Calculate new operational window: how many usable distribution days remain before weather peak?
5.6 Evaluate: Should pre-event distribution be accelerated (push maximum supplies to clusters before storm arrives)?
5.7 Recalculate efficiency metrics with weather-adjusted road availability.
5.8 Generate Contingency Plan D:
  - Pre-event surge delivery schedule (maximize delivery in windows before weather peak)
  - Clusters to pre-stock (deliver extra rations before storm to allow 3+ day coverage without re-supply)
  - Post-event priority re-entry sequence (which clusters first after roads re-open)
  - Decision trigger: "If forecast shows precipitation > 50mm within 48h, initiate pre-event surge delivery"
  - Weather monitoring: Recommend continuous 6-hour weather check during active event

### Step SE-6: Sensitivity Ranking
6.1 Compare baseline vs. all 4 scenarios on the key metric: % Tier 1 beneficiaries reached within 72 hours.
6.2 Calculate impact of each scenario:
  - Impact(scenario) = B2_baseline - B2_scenario
6.3 Rank scenarios from highest to lowest impact on Tier 1 coverage.
6.4 Identify the highest-sensitivity constraint: the one whose change causes the largest drop in Tier 1 coverage.
6.5 Flag: "Your plan is most sensitive to [constraint]. Prioritize contingency planning for this constraint first."
6.6 Present secondary finding: Which clusters are "fragile" -- appearing in 2+ scenario failure modes? These clusters need special attention (pre-positioning or alternative access pre-arranged).

### Step SE-7: Combined Scenario (Stress Test)
7.1 Run one combined scenario: apply the two highest-impact constraints simultaneously (e.g., Road blocked + 25% budget cut).
7.2 Recalculate minimum viable plan: what is the minimum scope that can still deliver Sphere minimums to at least Tier 1 beneficiaries?
7.3 This is the "floor plan" -- the absolute minimum the NGO must maintain no matter what.
7.4 Present the floor plan with its assumptions and constraints.

### Step SE-8: Assemble Simulation Report
8.1 Build the scenario comparison table (all 5 scenarios + combined).
8.2 Write contingency plans A, B, C, D in clear, field-implementable language.
8.3 Include decision triggers for each contingency plan.
8.4 Note fragile clusters requiring special attention.
8.5 Verify all quality gates before handing off to main.md for synthesis.

---

## Outputs

**Scenario Analysis Report:**
```
SCENARIO ANALYSIS REPORT
==========================
Baseline Plan | [Date] | [Disaster Name]

SCENARIO COMPARISON TABLE:
Scenario          | % Tier1 D1 | % Tier1 D3 | Cost/ben | Total cost | Delta from baseline
Baseline          | [X]%       | [X]%       | $[X]     | $[X]       | --
A: Road blocked   | [X]%       | [X]%       | $[X]     | $[X]       | -[X]pp
B: Budget cut 25% | [X]%       | [X]%       | $[X]     | $[X]       | -[X]pp
C: Demand +30%    | [X]%       | [X]%       | $[X]     | $[X]       | -[X]pp
D: Weather event  | [X]%       | [X]%       | $[X]     | $[X]       | -[X]pp
AB: Combined      | [X]%       | [X]%       | $[X]     | $[X]       | -[X]pp

SENSITIVITY RANKING (by impact on % Tier 1 coverage at Day 3):
1. [Highest impact constraint]: -[X]pp Tier 1 coverage
2. [Second highest]: -[X]pp
3. [Third]: -[X]pp
4. [Lowest]: -[X]pp
WARN:️ CRITICAL: Your plan is most sensitive to [constraint].

FRAGILE CLUSTERS (appear in 2+ failure scenarios):
  - Cluster [C?]: unreachable in Scenarios A and D -- pre-position emergency stock NOW
  - Cluster [C?]: below Sphere minimum in Scenarios B and C -- priority for donor advocacy

CONTINGENCY PLAN A: If [road] Is Blocked
  Decision trigger: [road] blocked -> activate immediately
  Alternative route: [specific route with turn-by-turn if possible]
  Alt transport for C2: 3 motorcycles carrying RUTF + ORS only
  Lead time to implement: 2 hours
  Impact: Day 1 Tier 1 coverage drops from [X]% to [Y]% -> recover by Day 2

CONTINGENCY PLAN B: If Budget Cut 25%
  Decision trigger: Available budget drops below USD [threshold]
  Scope reduction steps:
    1. Switch C5 and C6 (Tier 2) to cash voucher -- saves USD [X]
    2. Reduce Tier 3 frequency from daily to every-other-day
    3. Request emergency funding via OCHA FTS/CERF -- submit within 24h
  Maintained: All Tier 1 clusters at full Sphere quantities (non-negotiable)
  Impact: Tier 2 coverage Day 3 drops from [X]% to [Y]%

CONTINGENCY PLAN C: If Demand Surges 30%
  Decision trigger: Total registered population exceeds [N + 30%]
  Immediate actions:
    1. Request WFP pipeline emergency release: [X] MT food + [Y] MT NFI
    2. Contact [logistics cluster lead] for additional vehicle hire
    3. Deploy additional Kobo registration teams to verify surge
  Expected lead time for additional supplies: [N] days
  Gap coverage period: Days [X] to [Y] -- Tier 1 maintained at minimum quantities

CONTINGENCY PLAN D: Weather Event Response
  Weather forecast summary: [extracted from WebSearch]
  Pre-event surge: Deploy all available trucks to C1, C2, C3 (Tier 1) TODAY
  Pre-stock quantity: 3-day supply buffer for all Tier 1 clusters
  Suspended routes during event: [list]
  Re-entry priority after weather clears: [ordered list of clusters]
  Decision trigger: Precipitation > 50mm/24h forecast -> activate pre-event surge

FLOOR PLAN (Minimum Viable):
  Scope: Tier 1 only, Sphere minimums only
  Clusters covered: [list Tier 1 clusters only]
  Resources required: [minimum fleet, budget]
  This plan must be maintained regardless of resource constraints.

WEATHER INTEGRATION (72-hour):
  Forecast source: [WebSearch result]
  Precipitation forecast: [X mm/24h -- Low/Medium/High disruption risk]
  Wind: [X km/h -- Low/Medium/High]
  WARN:️ Disruption risk: [None/Low/Medium/High]
  Action recommended: [None / Pre-event surge / Immediate suspension of [routes]]
```

---

## Quality Gate

Before handing off to main.md quality gate review, verify:

- [ ] **QG-7:** All 4 mandatory scenario types completed (road blocked, budget cut, demand surge, weather); none skipped
- [ ] **QG-8:** 72-hour weather forecast integrated; flagged as unavailable if data could not be fetched
- [ ] Sensitivity ranking calculated and highest-impact constraint identified
- [ ] At least one combined scenario (two constraints simultaneously) run
- [ ] All 4 contingency plans include a specific decision trigger and lead time estimate
- [ ] Fragile clusters identified (those appearing in 2+ failure scenarios)
- [ ] Floor plan (minimum viable plan) defined
- [ ] Weather data source cited; disruption risk level assigned
