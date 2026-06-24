---
name: disaster-relief-distribution-simulation/sub-logistics-optimizer
description: Apply Clarke-Wright VRP heuristic, Linear Programming, and Nash equilibrium multi-agency coordination to generate an optimized, day-by-day disaster relief distribution plan
---

## Purpose

This sub-skill is the quantitative optimization engine of the harness. It takes the needs matrix from sub-needs-assessment and the resource inventory from sub-profile-intake, then applies three mathematical frameworks to generate the best achievable distribution plan within the given constraints:

1. **Clarke-Wright Savings Algorithm** (VRP heuristic): Determines the optimal routes for each vehicle on each day, minimizing total distance while respecting vehicle capacity and road condition constraints.
2. **Linear Programming (LP)**: Allocates available supply from warehouses to distribution points across the time horizon, maximizing Tier 1 beneficiary coverage within budget.
3. **Nash Equilibrium coordination** (when multiple NGOs are present): Assigns geographic zones to agencies to eliminate duplication and ensure hard-to-reach areas are covered.

All optimization outputs are presented in actionable, field-implementable format -- not abstract mathematical notation.

---

## Inputs

**From sub-needs-assessment:**
- needs_matrix (item x cluster x tier x quantity x frequency)
- cluster priority schedule (Day 1 / Day 2-3 / Day 4-7 / UNREACHABLE)
- total supply weight per cluster per period
- special handling flags (cold chain, hazmat, oversize)

**From sub-profile-intake:**
- resources.vehicles (type, payload_mt, count)
- resources.warehouses (location, capacity_mt, current_stock_mt, coordinates)
- resources.budget_usd
- location_clusters (id, population, road_score, coordinates)
- partner_agencies (name, capacity)
- time_horizon_days
- access_constraints

**From external sources:**
- Road network data: WebSearch for HDX logistics/roads layer or OpenStreetMap data for the affected area
- Estimated inter-cluster distances: derived from geography (use straight-line distance x road condition factor if OSM data unavailable)

---

## Workflow

### Step LO-1: Build the Distance/Time Matrix
1.1 For each pair of supply nodes (warehouses) and demand nodes (distribution clusters), estimate travel time:
  - **Preferred:** Use OpenStreetMap road network data (WebSearch "osmnx [country] road network" or HDX roads layer)
  - **Fallback:** Use straight-line distance x terrain multiplier:
    - Flat terrain, intact road: 1.0x (speed ~60 km/h)
    - Hilly terrain or partially damaged road: 1.5x (speed ~40 km/h)
    - Heavily damaged road (road_score = 1): 3.0x (speed ~20 km/h)
    - Road_score = 0: Impassable -- remove from route network; flag cluster as requiring alternative access
1.2 Apply road condition multipliers from the profile's road_score values.
1.3 Build a distance matrix D[i][j] = estimated travel time in hours between node i and node j.
1.4 Flag any cluster pair with D[i][j] > 8 hours (single-day round trip limit for truck) as requiring overnight stay or relay depot.

### Step LO-2: Clarke-Wright Savings Algorithm (VRP Routing)
2.1 **Initialization:** Create a naive solution -- one route per cluster (depot -> cluster -> depot). Calculate total distance of naive solution.
2.2 **Savings calculation:** For each pair of clusters i, j:
  - Savings(i,j) = D[depot, i] + D[depot, j] - D[i, j]
  - A positive saving means combining i and j into one route is shorter than two separate routes
2.3 **Savings list:** Sort all (i,j) pairs in descending order of savings value.
2.4 **Route merging:** For each (i,j) pair (highest savings first):
  - Merge routes for i and j if:
    a. Neither i nor j is already an interior stop on an existing route
    b. Combined load does not exceed vehicle capacity
    c. Combined route time does not exceed daily operating window (typically 10 hours)
  - If capacity constraint prevents merge: split across multiple vehicles
2.5 **Result:** Set of optimized routes, one per vehicle (or per vehicle-day combination).
2.6 **Priority constraint overlay:** Regardless of savings optimization, ensure Tier 1 clusters (Day 1 priority) are served on Day 1 -- their delivery cannot be deferred for efficiency savings.
2.7 **Output:** For each route: sequence of clusters, total distance, estimated travel time, load manifest (what is loaded from which warehouse).

### Step LO-3: LP Resource Allocation
3.1 **Formulate the allocation problem:**
  ```
  Decision variables: x[w][c][t] = quantity shipped from warehouse w to cluster c on day t
  
  Objective: Maximize Σ(beneficiaries reached) 
             = Maximize Σ[c,t] (min(x[w][c][t], demand[c][t]) / demand[c][t]) x population[c] x priority_weight[tier(c)]
  
  Where priority_weight: Tier 1 = 3.0, Tier 2 = 1.5, Tier 3 = 1.0
  
  Subject to:
    Supply: Σ[c,t] x[w][c][t] <= stock[w] + procurement[w][t]   (for each warehouse w)
    Demand: Σ[w] x[w][c][t] >= demand[c][t]  (if within budget and capacity)
    Vehicle: Σ[c] x[w][c][t] <= fleet_capacity[w][t]             (vehicle capacity constraint per depot per day)
    Budget: Σ[w][c][t] cost[w][c][t] <= budget_usd               (total budget constraint)
    Non-negativity: x[w][c][t] >= 0
  ```
3.2 **Solve:** Apply LP iteratively (greedy approach for field use):
  - Day 1: Allocate to all Tier 1 clusters first (highest priority weight), up to vehicle capacity
  - Day 2: Allocate remaining Tier 1 demand + begin Tier 2 clusters
  - Days 3+: Continue until time horizon or stock exhausted
3.3 Calculate total cost: procurement costs + transport costs (fuel + driver per-diem per route)
3.4 Calculate and report: total quantities allocated by item and cluster; variance from needs matrix (quantity gap)

### Step LO-4: Warehouse Replenishment Schedule
4.1 Calculate daily stock drawdown per warehouse based on vehicle routes and load manifests.
4.2 Identify when each warehouse stock falls below 2 days of supply (replenishment trigger point).
4.3 Calculate replenishment quantities needed and recommend procurement timing.
4.4 Flag any warehouse that will run out before the end of the time horizon -> escalate to user.

### Step LO-5: Cash vs. In-Kind Modality Assessment
5.1 Evaluate cash-based interventions (CBI) against in-kind distribution using a 5-criteria rubric:

| Criterion | Assessment | Score (0-2) |
|-----------|-----------|-------------|
| Market functionality | Are local markets operating? Can beneficiaries buy needed goods? | 0=No/destroyed; 1=Partially; 2=Yes |
| Security | Can beneficiaries safely travel to markets/ATMs? | 0=No; 1=Partial; 2=Yes |
| Beneficiary preference | Do beneficiaries prefer cash for dignity/flexibility? | 0=No preference; 1=Some; 2=Strong preference |
| Administrative capacity | Does NGO have cash delivery mechanism (mobile money, vouchers, hawala)? | 0=No; 1=Partial; 2=Full |
| OCHA/cluster guidance | Is cash recommended by the relevant cluster for this context? | 0=No; 1=Neutral; 2=Yes |

5.2 Interpretation:
  - Score 8-10: Recommend cash/voucher transfer
  - Score 5-7: Recommend hybrid (cash for food + in-kind for NFI/WASH)
  - Score 0-4: Recommend in-kind aid
5.3 Note: Regardless of modality score, items with no market substitute (e.g., RUTF, vaccines, tarpaulins in acute emergency) must always be delivered in-kind.

### Step LO-6: Nash Equilibrium Multi-Agency Coordination (if applicable)
6.1 **Applicable when:** 2+ NGOs are present in the response with distinct logistics capacity.
6.2 **Zone assignment game:**
  - Players: each NGO (n players)
  - Strategies: which location clusters to cover (a subset of the total cluster list)
  - Payoff: beneficiaries reached in assigned clusters (each NGO maximizes coverage in their zones)
  - Constraint: each cluster must be covered by exactly one agency (no duplication)
  - Objective: find the assignment that maximizes total beneficiaries reached across all agencies
6.3 **Solution approach (Kuhn-Munkres / Hungarian Algorithm for assignment):**
  - Build a payoff matrix: row = NGO, column = cluster, value = % of cluster population the NGO can efficiently reach (based on NGO's warehouse proximity, access road alignment, existing community relationships)
  - Apply the assignment algorithm to find the optimal assignment
  - This produces the Nash equilibrium: no NGO can improve its coverage by unilaterally switching zones
6.4 **Present coordination plan:**
  - Table: Agency -> Assigned Clusters -> Estimated coverage -> Required vehicles
  - Shared resource agreements: which logistics assets can be pooled (WFP common services, shared warehouses)
6.5 **Note:** Frame as a recommendation for the IASC Logistics Cluster coordination meeting, not a binding assignment. Participation is voluntary but in each agency's self-interest (the Nash equilibrium is individually rational).

### Step LO-7: Efficiency Metrics Calculation
7.1 Calculate for the optimized plan:
  - **% Tier 1 beneficiaries reached by Day 1:** (Tier 1 pop covered on Day 1) / (Total Tier 1 pop) x 100%
  - **% Tier 1 beneficiaries reached by Day 3:** (Tier 1 pop covered by Day 3) / (Total Tier 1 pop) x 100%
  - **% Total beneficiaries reached by end of time horizon:** (Total pop covered) / (Total pop in needs matrix) x 100%
  - **Cost per beneficiary (USD):** Total plan cost / Total beneficiaries reached
  - **Vehicle utilization rate:** (Actual load per trip / Vehicle payload capacity) x 100% average
  - **Sphere compliance rate:** % of clusters receiving >= Sphere minimum quantities
  - **Benchmark comparison:** Compare cost/beneficiary to WFP emergency response norm (typically USD 40-80/person/month for food alone in acute emergency)

### Step LO-8: Assemble and Validate Distribution Plan
8.1 Compile the full distribution plan document (see Outputs).
8.2 Verify QG-5: % Tier 1 coverage within 72h >= 80%. If not, flag and present options:
  - Option A: Add more vehicles
  - Option B: Reduce time window assumption
  - Option C: Pre-position supplies closer to Tier 1 clusters
  - Option D: Use alternative transport (motorcycle for hard-to-reach)
8.3 Verify QG-6: Cost/beneficiary calculated and benchmarked.
8.4 Hand off to sub-simulation-engine.

---

## Outputs

**Optimized Distribution Plan:**
```
OPTIMIZED DISTRIBUTION PLAN
=============================
Plan Date: [Date]
Total Beneficiaries: [N] | Time Horizon: [N] days
Optimization Algorithm: Clarke-Wright Savings (VRP heuristic) + LP allocation

VEHICLE ROUTE SCHEDULE:
Day 1:
  Vehicle 1 (Truck, 5 MT):
    Depot: W1 [Warehouse 1]
    Route: W1 -> C2 (Tier 1, road score 2) -> C4 (Tier 1, road score 3) -> W1
    Load: [400 kg cereals, 60 kg pulses, 50 kg oil, 200 L hygiene kit water, ...]
    Estimated travel time: [X] hours | Distance: [X] km
    Beneficiaries served: C2=[N], C4=[N] | Total this run: [N]
  Vehicle 2 (Truck, 3 MT):
    ...
  Vehicle 3 (Motorcycle x 3, 0.1 MT each):
    Route: W1 -> C7 (Tier 1, road score 1 -- damaged road, 4WD only)
    Load: [RUTF sachets, ORS, emergency health kit]
    ...

Day 2:
  ...

WAREHOUSE REPLENISHMENT SCHEDULE:
  W1: Stock at Day 0 = [X] MT; projected stock at Day 3 = [Y] MT
  Replenishment trigger: Day 3 | Recommended order quantity: [Z] MT
  ...

DISTRIBUTION POINT SUMMARY:
  Cluster | Day(s) | Beneficiaries | Items Delivered | Vehicle | Sphere Compliance
  C1      | 1      | [N]           | Water, Food, NFI| V1      | OK
  C2      | 1      | [N]           | Water, Food     | V1      | OK
  C3      | 1-2    | [N]           | Water only D1   | V2      | WARN:️ Food Day 2
  ...

MODALITY RECOMMENDATION:
  Assessment score: [X/10]
  Recommendation: [In-kind / Hybrid / Cash]
  Rationale: [Market functionality, security, capacity assessment]
  CBI items (if hybrid): [Food ration -> cash/voucher]
  In-kind only: [RUTF, tarpaulin, IEHK -- no market substitute]

EFFICIENCY METRICS:
  % Tier 1 reached by Day 1: [X]%  | Target: >= 80%  | Status: OK/WARN:️
  % Tier 1 reached by Day 3: [X]%  | Target: >= 95%  | Status: OK/WARN:️
  % Total pop reached by Day [N]: [X]%
  Cost per beneficiary: USD [X]    | Sector benchmark: USD [range]  | Status: OK/WARN:️
  Vehicle utilization rate: [X]%
  Total tonnage delivered: [X] MT
  Sphere compliance rate: [X]% of clusters at/above minimums
```

---

## Quality Gate

Before handing off to sub-simulation-engine, verify:

- [ ] **QG-5:** >= 80% of Tier 1 beneficiaries are reachable within 72 hours under the optimized plan; if not, escalate with options
- [ ] **QG-6:** Cost-per-beneficiary calculated; compared against WFP/UNHCR sector norms
- [ ] All vehicle routes validated against current road access data (road scores from profile)
- [ ] Modality decision (cash vs. in-kind) made using the 5-criteria rubric with rationale
- [ ] Multi-agency Nash equilibrium coordination plan included if >= 2 NGOs present
- [ ] Warehouse replenishment schedule calculated for full time horizon
- [ ] All efficiency metrics calculated and presented
- [ ] No cluster below Sphere Standards in the plan (or exception explicitly noted)
