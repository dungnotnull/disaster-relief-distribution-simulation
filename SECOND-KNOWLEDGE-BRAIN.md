# SECOND-KNOWLEDGE-BRAIN.md -- Skill #242: Disaster Relief Distribution Simulation & Optimization (NGO)

> **Self-Improving Knowledge Base** | Cluster: science-industry | Last crawl: 2026-06-19
> This document is the living domain knowledge repository for the disaster relief distribution simulation skill. It is updated weekly by `tools/knowledge_updater.py`. Do not edit manually except to correct errors -- additions come from the automated crawl pipeline.

---

## 1. Core Concepts & Frameworks

### 1.1 OCHA Humanitarian Principles
The four humanitarian principles established by UN General Assembly Resolution 46/182 (1991) and endorsed by all major NGOs:
- **Humanity:** Human suffering must be addressed wherever it is found; purpose is to protect life and health and ensure respect for human beings.
- **Neutrality:** Humanitarian actors must not take sides in hostilities or engage in controversies of a political, racial, religious, or ideological nature.
- **Impartiality:** Humanitarian action must be carried out solely on the basis of need, giving priority to the most urgent cases of distress without discrimination.
- **Independence:** Humanitarian action must be autonomous from political, economic, military, or other objectives any actor may hold.

**Operational implication for this skill:** Impartiality drives Tier 1 beneficiary prioritization (most vulnerable first, regardless of location accessibility). Independence means the skill must never optimize purely for donor visibility or political access when this conflicts with need-based distribution.

### 1.2 Sphere Standards (Sphere Handbook 2018)
The Sphere Project defines minimum humanitarian standards across 4 sectors:

**WASH (Water, Sanitation, Hygiene)**
- Minimum water quantity: 15 liters/person/day (survival minimum: 7.5 L/person/day in acute emergency)
- Toilet ratio: maximum 20 persons per latrine (gender-separated)
- Distance to water point: maximum 500 meters
- Handwashing facility: 1 per 100 persons (or 1 per household)

**Food Security & Nutrition**
- Minimum caloric intake: 2,100 kcal/person/day
- Protein: minimum 10% of total energy intake
- Fat: minimum 17% of total energy intake
- Therapeutic feeding threshold: Global Acute Malnutrition (GAM) > 15% triggers emergency nutrition response

**Shelter & Non-Food Items (NFI)**
- Covered floor area: minimum 3.5 m^2 per person (acute emergency); 4.5-5.5 m^2 for longer stays
- Thermal comfort: shelter must protect from prevailing weather
- Blankets: 1 per person minimum in cold climates
- Cooking set: 1 per household

**Health**
- Primary healthcare: 1 health post per 10,000 population
- Hospital beds: 1 per 1,000 in acute emergency
- Oral rehydration salts (ORS): available at all health points

### 1.3 Vehicle Routing Problem (VRP) -- Humanitarian Application
The VRP is an NP-hard combinatorial optimization problem: given a fleet of vehicles with limited capacity, find the optimal set of routes to deliver goods from one or more depots to geographically dispersed demand nodes.

**Variants relevant to humanitarian logistics:**
- **CVRP (Capacitated VRP):** Each vehicle has fixed capacity; fundamental model for aid distribution
- **VRPTW (VRP with Time Windows):** Delivery must occur within a time window; critical for medical supplies and food
- **Multi-Depot VRP:** Multiple warehouses/distribution hubs; common when pre-positioned stocks are used
- **Stochastic VRP:** Demand is uncertain; critical for acute disaster response where needs assessments are incomplete

**Clarke-Wright Savings Algorithm (practical heuristic):**
1. Start with a naive solution: one vehicle per demand node (direct routes from depot)
2. Calculate "savings" for merging two routes i and j: S(i,j) = d(depot,i) + d(depot,j) - d(i,j)
3. Sort all savings in decreasing order
4. Merge routes in savings order (subject to capacity constraints)
5. Result: typically within 5-15% of optimal; runs in polynomial time; field-implementable

**For humanitarian use:** Apply distance matrix from HDX road network data; adjust for road condition multipliers (damaged road = 2-3x travel time factor).

### 1.4 Linear Programming (LP) for Resource Allocation
LP finds the optimal allocation of scarce resources to activities, subject to linear constraints.

**General humanitarian logistics LP formulation:**

```
Minimize: Σ(i,j) c_ij * x_ij  [total distribution cost or time]

Subject to:
  Σ_j x_ij <= S_i  for all supply nodes i  [supply capacity constraint]
  Σ_i x_ij >= D_j  for all demand nodes j  [demand satisfaction constraint]
  x_ij >= 0        for all i,j             [non-negativity]
```

Where:
- x_ij = quantity shipped from supply node i to demand node j
- c_ij = unit cost/time from i to j
- S_i = supply capacity at node i (warehouse stock)
- D_j = demand at node j (needs matrix output)

**Multi-objective variant:** When both cost minimization and coverage maximization matter, use weighted LP or lexicographic optimization (first maximize coverage of Tier 1 beneficiaries, then minimize cost within that constraint).

### 1.5 Game Theory -- Multi-Agency Coordination

**Nash Equilibrium:** In a game with n players, a Nash equilibrium is a strategy profile where no player can improve their payoff by unilaterally changing their strategy.

**Application to multi-NGO coordination:**
- Players: each NGO with independent logistics capacity
- Strategy: which geographic zones/beneficiary groups to target
- Payoff: beneficiaries reached (maximize), cost expended (minimize)
- Nash equilibrium assignment: each NGO is assigned zones where their comparative advantage (road access, existing relationships, supply chain) is highest, such that no NGO would benefit from switching zones

**Stackelberg Game for Donor-Recipient Dynamics:**
- Leader: donor (sets funding envelope and conditions)
- Follower: NGO (optimizes distribution plan within donor constraints)
- Solution: Stackelberg equilibrium -- NGO's best response to any donor strategy, anticipating donor behavior

**Coordination failure modes:** Without Nash equilibrium coordination, NGOs cluster in easy-access areas (dominant strategy for each individual NGO due to visibility/reporting incentives), leaving hard-to-reach communities uncovered -- a classic Prisoner's Dilemma outcome.

### 1.6 IPC (Integrated Food Security Phase Classification)
The IPC is a set of standardized tools and procedures to classify the severity and magnitude of food insecurity situations:

| Phase | Name | Description | Minimum Humanitarian Response |
|-------|------|-------------|-------------------------------|
| 1 | Minimal | Adequate food access | None required |
| 2 | Stressed | Minimal adequate food barely met | Preventive actions |
| 3 | Crisis | Food consumption gaps or loss of livelihood assets | Emergency food assistance |
| 4 | Emergency | Severe food consumption gaps, high acute malnutrition | Urgent life-saving food aid |
| 5 | Famine | Extreme food deprivation, death | Maximum humanitarian mobilization |

**For this skill:** IPC phase 3 or above triggers emergency food assistance in the needs matrix. Phase 4-5 triggers acute nutrition interventions (RUTF, therapeutic feeding).

### 1.7 INFORM Risk Index
The INFORM (Index for Risk Management) model classifies countries and sub-national areas by disaster risk:
- **Three composite dimensions:** Hazard & Exposure, Vulnerability (socio-economic & institutional), Lack of Coping Capacity
- **Score range:** 0-10 (10 = highest risk)
- **Use in this skill:** INFORM score for the affected area informs pre-positioning decisions and probability weighting in scenario simulations

### 1.8 IASC Cluster System
The Inter-Agency Standing Committee (IASC) organizes humanitarian response into functional clusters:

| Cluster | Lead Agency | Relevance to Distribution |
|---------|------------|--------------------------|
| Logistics | WFP | Coordinates common logistics services; manages shared warehouses |
| Food Security | WFP/FAO | Food aid distribution; cash/voucher programs |
| WASH | UNICEF | Water trucking, sanitation supply distribution |
| Shelter/NFI | UNHCR/IFRC | Non-food item distribution; shelter material |
| Health | WHO | Medical supply distribution |
| Nutrition | UNICEF | RUTF and therapeutic feeding supply chain |

**For this skill:** IASC cluster leads are natural coordination partners. The skill recommends routing all distribution plans through the relevant cluster coordination meetings.

---

## 2. Key Research Papers

| # | Title | Authors | Year | Venue | DOI/Link | Relevance |
|---|-------|---------|------|-------|---------|-----------|
| 1 | Humanitarian logistics: Advanced purchasing and pre-positioning of relief items | Balcik, B. & Beamon, B. | 2008 | International Journal of Production Economics | 10.1016/j.ijpe.2007.10.014 | Pre-positioning optimization model; direct framework reference |
| 2 | A review of operations research and management science literature on humanitarian logistics | Caunhye, A.M. et al. | 2012 | Socio-Economic Planning Sciences | 10.1016/j.seps.2011.05.002 | Comprehensive OR literature review; taxonomy of humanitarian logistics models |
| 3 | Last mile distribution in humanitarian relief | Balcik, B. et al. | 2008 | Journal of Intelligent Transportation Systems | 10.1080/15472450801901564 | Last-mile delivery problem formulation with uncertain demand |
| 4 | Nash bargaining for log-convex problems | Qin, C.Z. et al. | 2015 | Economic Theory | 10.1007/s00199-014-0848-y | Nash bargaining solution for multi-agency resource sharing |
| 5 | A multi-objective programming model for multi-echelon network design in a natural disaster situation | Afshar, A. & Haghani, A. | 2012 | Transportation Research Part E | 10.1016/j.tre.2012.06.009 | Multi-depot, multi-period distribution network optimization |
| 6 | Pre-positioning disaster response facilities at safe locations | Rawls, C.G. & Turnquist, M.A. | 2010 | Transportation Research Part B | 10.1016/j.trb.2010.02.003 | Stochastic pre-positioning model with demand uncertainty |
| 7 | Integrated vehicle and crew scheduling in humanitarian logistics | Ortuño, M.T. et al. | 2011 | TOP (Journal of the Spanish Society of Statistics) | 10.1007/s11750-010-0157-z | Multi-vehicle, multi-period scheduling for disaster relief |
| 8 | Relief supply chain management for disasters: Humanitarian, aid and emergency logistics | Tatham, P. & Pettit, S. | 2010 | Emerald (Book chapter) | N/A | Practical humanitarian logistics framework; good framework overview |
| 9 | A bi-objective optimization model for humanitarian response considering time and cost | Vitoriano, B. et al. | 2011 | Journal of Global Optimization | 10.1007/s10898-010-9601-1 | Bi-objective VRP variant specifically for humanitarian response |
| 10 | Coordination in humanitarian logistics through clusters | Tomasini, R.M. & Van Wassenhove, L.N. | 2009 | Production and Operations Management | 10.1111/j.1937-5956.2009.01114.x | IASC cluster system coordination effectiveness analysis |
| 11 | Cash versus in-kind: Evidence from a randomized control trial in Niger | Aker, J.C. et al. | 2016 | American Economic Review | 10.1257/app.20140362 | Empirical evidence on cash transfer vs. in-kind effectiveness |
| 12 | The vehicle routing problem: Latest advances and new challenges | Golden, B.L. et al. (eds) | 2008 | Springer | 10.1007/978-0-387-77778-8 | Comprehensive VRP reference including VRPTW, stochastic variants |

---

## 3. State-of-the-Art Methods & Tools

### 3.1 Optimization Tools
- **OR-Tools (Google):** Open-source VRP solver; supports CVRP, VRPTW, multi-depot; Python API. URL: developers.google.com/optimization
- **CPLEX/Gurobi:** Commercial LP/MIP solvers; high-performance for large-scale allocation; require license
- **PuLP (Python):** Free LP library for resource allocation formulation; simple to use; recommended for field teams
- **NetworkX (Python):** Graph algorithms for road network analysis; Clarke-Wright implementation available

### 3.2 Data Tools & Platforms
- **Humanitarian Data Exchange (HDX):** hdx-python-api for programmatic access; major source for population, road, warehouse, and displacement data
- **OCHA COD (Common Operational Datasets):** Admin boundaries, population data per country; available via HDX
- **OpenStreetMap (OSM):** Road network data; osmnx Python library extracts OSM data for routing
- **GDACS API:** Real-time disaster alerts including affected area polygons, severity scores; JSON API
- **OpenWeatherMap API:** Current and forecast weather (precipitation, wind, temperature) for route planning
- **ReliefWeb API:** Structured access to situation reports, maps, funding data

### 3.3 Coordination Platforms
- **OSOCC Virtual (Virtual On-Site Operations Coordination Centre):** UN-managed platform for disaster coordination; disaster-specific information sharing
- **Kobo Toolbox:** ODK-based beneficiary registration and needs survey tool; used by major NGOs
- **LogISTICS (WFP):** WFP's logistics information management platform; warehouse tracking, truck dispatch
- **iHAY (Information Hub for Aid and Yourself):** OCHA platform for logistics capacity tracking

---

## 4. Authoritative Data Sources

| Source | URL | Data Available | Access |
|--------|-----|----------------|--------|
| ReliefWeb | reliefweb.int | Situation reports, maps, funding news | Free; API available |
| HDX (Humanitarian Data Exchange) | data.humdata.org | Population, displacement, roads, warehouses, facilities | Free; API available |
| OCHA FTS (Financial Tracking Service) | fts.unocha.org | Humanitarian funding flows | Free; API available |
| ALNAP | alnap.org | Evaluation reports, learning documents | Free |
| Sphere Standards Handbook | spherehandbook.org | Minimum standards (WASH, food, shelter, health) | Free PDF |
| INFORM Risk Index | informindex.org | Country/subnational risk scores | Free download |
| IPC Global Platform | ipcinfo.org | IPC food security phase maps | Free |
| GDACS | gdacs.org | Real-time disaster alerts, severity, affected areas | Free; RSS + API |
| OSOCC Virtual | virtual.osocc.unocha.org | Disaster coordination information | Registered users |
| Journal of Humanitarian Logistics | emerald.com/insight/publication/issn/2042-6747 | Peer-reviewed research | Subscription/open access |
| Disasters (journal) | onlinelibrary.wiley.com/journal/14677717 | Humanitarian practice research | Subscription/open access |

---

## 5. Analytical Frameworks

### 5.1 Clarke-Wright Savings Algorithm (VRP Heuristic)
**Citation:** Clarke, G. & Wright, J.W. (1964). Scheduling of Vehicles from a Central Depot to a Number of Delivery Points. Operations Research, 12(4), 568-581. DOI: 10.1287/opre.12.4.568
**Application:** Route planning for aid distribution vehicles; reduces total distance by 15-25% vs. naive routing; runs in O(n^2 log n)

### 5.2 Sphere Minimum Standards
**Citation:** Sphere Association (2018). The Sphere Handbook: Humanitarian Charter and Minimum Standards in Humanitarian Response. Geneva: Sphere Association. ISBN: 978-1-908176-40-4
**Application:** All needs calculations use Sphere minimums as the non-negotiable lower bound for distribution quantities

### 5.3 IPC Food Security Phase Classification
**Citation:** IPC Global Partners (2021). IPC Technical Manual Version 3.1. Rome: IPC Global Support Unit.
**Application:** Determines severity of food insecurity needs and appropriate response modality

### 5.4 INFORM Risk Index
**Citation:** De Groeve, T. et al. (2015). Index for Risk Management - INFORM: Concept and Methodology Version 2015. JRC Technical Reports. Luxembourg: Publications Office of the EU. DOI: 10.2788/183937
**Application:** Disaster risk profiling for pre-positioning decisions and scenario probability weighting

### 5.5 Nash Equilibrium (Coordination)
**Citation:** Nash, J. (1951). Non-cooperative games. Annals of Mathematics, 54(2), 286-295. DOI: 10.2307/1969529
**Application:** Multi-agency zone assignment optimization to prevent duplicated effort and coverage gaps

### 5.6 IASC Cluster Approach
**Citation:** IASC (2015). Reference Module for Cluster Coordination at the Country Level. IASC.
**Application:** Aligning distribution plans with cluster coordination structures for field coordination

---

## 6. Self-Update Protocol

### Crawl4ai Configuration
```python
# Run: python tools/knowledge_updater.py
# Schedule: Weekly (Sundays 00:00 UTC) via cron or Windows Task Scheduler

SOURCES = [
    {
        "name": "ReliefWeb Situation Reports",
        "url": "https://reliefweb.int/updates?format=sitrep&page=0",
        "type": "sitrep",
        "frequency": "weekly",
        "relevance_keywords": ["logistics", "distribution", "supply chain", "relief", "aid delivery"]
    },
    {
        "name": "HDX New Datasets",
        "url": "https://data.humdata.org/api/3/action/package_search?q=logistics+humanitarian&rows=20&sort=metadata_created+desc",
        "type": "dataset",
        "frequency": "weekly",
        "relevance_keywords": ["logistics", "warehouse", "roads", "transport", "supply"]
    },
    {
        "name": "OCHA FTS Updates",
        "url": "https://fts.unocha.org/",
        "type": "funding",
        "frequency": "weekly",
        "relevance_keywords": ["humanitarian", "emergency", "response"]
    },
    {
        "name": "ALNAP Learning",
        "url": "https://www.alnap.org/resources/publications",
        "type": "report",
        "frequency": "weekly",
        "relevance_keywords": ["logistics", "distribution", "last mile", "supply chain", "coordination"]
    },
    {
        "name": "GDACS Active Alerts",
        "url": "https://www.gdacs.org/Alerts/default.aspx",
        "type": "alert",
        "frequency": "daily",
        "relevance_keywords": []  # All active alerts are relevant
    },
    {
        "name": "JHL Emerald",
        "url": "https://www.emerald.com/insight/publication/issn/2042-6747",
        "type": "journal",
        "frequency": "weekly",
        "relevance_keywords": ["vehicle routing", "distribution", "optimization", "NGO", "disaster"]
    },
    {
        "name": "ArXiv Humanitarian Logistics",
        "url": "https://arxiv.org/search/?searchtype=all&query=humanitarian+logistics+optimization&start=0",
        "type": "preprint",
        "frequency": "weekly",
        "relevance_keywords": ["humanitarian", "disaster", "VRP", "routing", "relief distribution"]
    },
    {
        "name": "Sphere Standards Updates",
        "url": "https://spherestandards.org/news/",
        "type": "standards",
        "frequency": "monthly",
        "relevance_keywords": ["update", "revision", "minimum standards", "WASH", "food", "shelter"]
    }
]

KNOWLEDGE_BRAIN_PATH = "D:\\Dungchan\\skill_adv\\242\\SECOND-KNOWLEDGE-BRAIN.md"
RELEVANCE_SCORE_THRESHOLD = 5  # Minimum score (0-10) to include entry
```

### Entry Scoring Criteria
- **Recency score (0-4):** < 1 month = 4; < 6 months = 3; < 1 year = 2; < 3 years = 1; older = 0
- **Keyword relevance score (0-4):** Count of domain keywords matched in title+abstract; cap at 4
- **Source authority score (0-2):** Peer-reviewed journal = 2; official UN/NGO report = 2; news = 1; blog = 0
- **Total relevance score:** Sum of above (0-10); minimum threshold = 5 to append

---

## 7. Knowledge Update Log

### [2026-06-19] Initial Seeding
- **Action:** Manual seeding of foundational knowledge base
- **Entries added:** 12 research papers, 8 data sources, 8 analytical frameworks, 6 operational tools
- **Source:** Curated from Sphere Handbook (2018), IASC documentation, humanitarian logistics literature review
- **Curator:** Skill #242 build process
- **Next scheduled crawl:** 2026-06-26 (weekly via knowledge_updater.py)
