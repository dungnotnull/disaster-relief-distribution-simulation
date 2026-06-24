# CLAUDE.md -- Skill #242: Disaster Relief Distribution Simulation & Optimization (NGO)

## Skill Identity
- **Skill Name:** disaster-relief-distribution-simulation
- **Tagline:** Simulate, optimize, and operationalize emergency disaster relief distribution for NGOs using operations research and game theory
- **Source Idea:** #242 (ideas.md)
- **Cluster:** science-industry
- **Current Phase:** Phase 5 -- Integration & Cross-Skill Wiring (COMPLETE)
- **Last Updated:** 2026-06-24
- **Production Status:** Ready for open-source release

---

## Problem This Skill Solves

When a major disaster strikes -- earthquake, flood, cyclone, conflict displacement -- humanitarian NGOs face a race against time to deliver life-saving aid (food, water, shelter, medicine) to the right people, at the right place, at the right moment. The challenge is not just logistical: roads are destroyed, bridges are down, warehouses are flooded, hundreds of agencies compete for the same trucks, and demand surges unpredictably. Without a structured optimization approach, NGOs make costly, ad hoc decisions: duplicating deliveries in accessible areas while remote communities receive nothing, running vehicles on inefficient routes, and failing to pre-position supplies before the next weather event closes road access entirely.

This skill provides a full simulation and optimization workflow grounded in operations research (Vehicle Routing Problem, Linear Programming), game theory (Nash equilibrium for multi-agency coordination), and continuously updated real-world data (terrain maps, weather, situation reports from ReliefWeb/HDX). The output is a professional-grade operational distribution plan with scenario sensitivity analysis -- ready for NGO operations managers and logistics coordinators to act on immediately.

---

## Harness Flow Summary

```
[User invokes /disaster-relief-distribution-simulation]
       |
       v
Step 1: sub-profile-intake
       -- Collect disaster type, location, affected population, NGO capacity,
         available vehicles/warehouses/budget, time horizon, partner agencies
       |
       v
Step 2: sub-needs-assessment
       -- Apply Sphere Standards to quantify minimum needs per sector
       -- IPC classification for food security severity
       -- Beneficiary prioritization (women, children, elderly, disabled)
       -- Output: needs matrix (quantities by item, by location, by priority tier)
       |
       v
Step 3: sub-logistics-optimizer
       -- Run VRP/LP models: route planning, warehouse siting, distribution point selection
       -- Vehicle load optimization, delivery scheduling
       -- Multi-agency coordination via Nash equilibrium
       -- Output: optimized distribution plan with schedule and efficiency metrics
       |
       v
Step 4: sub-simulation-engine
       -- Scenario simulations: road blocked, budget cut, demand surge, weather event
       -- Sensitivity analysis on key constraints
       -- Contingency plan recommendations
       -- Output: scenario comparison table + recommended primary + fallback plans
       |
       v
Step 5: Quality Gate Review
       -- Verify Sphere Standards compliance in all outputs
       -- Verify humanitarian principles (humanity, neutrality, impartiality, independence)
       -- Verify all quantitative claims are traceable to inputs or cited frameworks
       |
       v
Step 6: Synthesize Final Deliverable
       -- Full operational distribution plan document
       -- Optimized route schedules
       -- Scenario analysis report
       -- IASC cluster coordination recommendations
```

---

## Sub-Skills List

| File | One-Line Description |
|------|---------------------|
| `skills/sub-profile-intake.md` | Collect and validate disaster context, NGO capacity, resource inventory, and time constraints |
| `skills/sub-needs-assessment.md` | Quantify humanitarian needs using Sphere Standards and IPC classification; output needs matrix |
| `skills/sub-logistics-optimizer.md` | Apply VRP/LP models and Nash equilibrium to generate optimized routes, warehouse plan, and delivery schedule |
| `skills/sub-simulation-engine.md` | Run multi-scenario simulations with sensitivity analysis to stress-test the distribution plan and generate contingency options |

---

## Tools Required
- **WebSearch** -- ReliefWeb situation reports, OCHA FTS updates, HDX datasets, weather/terrain data
- **WebFetch** -- Fetch specific ReliefWeb pages, HDX dataset pages, ALNAP learning documents
- **Read** -- Access SECOND-KNOWLEDGE-BRAIN.md for cached domain knowledge
- **Write** -- Generate operational plan documents and scenario reports
- **Bash** -- Run `tools/knowledge_updater.py` crawl pipeline

---

## Knowledge Sources (for crawl4ai pipeline)

| Source | Type | Domain |
|--------|------|--------|
| ReliefWeb (reliefweb.int) | Situation reports, maps | OCHA operational data |
| HDX (data.humdata.org) | Datasets: population, roads, warehouses | Humanitarian Data Exchange |
| OCHA FTS (fts.unocha.org) | Funding tracking | Financial context |
| ALNAP (alnap.org) | Learning reports, evaluations | Humanitarian learning |
| Journal of Humanitarian Logistics (Emerald) | Peer-reviewed OR research | Academic |
| Sphere Handbook (spherestandards.org) | Standards | Minimum standards |
| INFORM Risk Index (informindex.org) | Risk profiling | Disaster risk |
| ArXiv (cs.RO, math.OC) | Operations research preprints | Optimization algorithms |

---

## Supporting Python Tools

- `tools/knowledge_updater.py` -- crawl4ai-aware pipeline fetching from ReliefWeb, HDX, ALNAP, and humanitarian logistics journals; appends scored entries to SECOND-KNOWLEDGE-BRAIN.md weekly. Falls back to requests+BeautifulSoup if crawl4ai is unavailable.
- `tools/cron-setup.md` -- operating-system-specific scheduling instructions (Windows Task Scheduler / Linux cron).
- `tests/validate_skill.py` -- static validation harness that verifies skill structure, frontmatter YAML, quality gate coverage, and Scenario 1 computability without requiring live network calls.
- `requirements.txt` -- Python dependencies for the knowledge updater and validation harness.
- `README.md` -- open-source project overview, quick start, and validation instructions.

---

## Active Development Tasks

All build tasks are complete. The skill is registered and ready for invocation.

- [x] Write `skills/main.md` -- primary harness with full role, workflow, sub-skills, output format
- [x] Write `skills/sub-profile-intake.md`
- [x] Write `skills/sub-needs-assessment.md`
- [x] Write `skills/sub-logistics-optimizer.md`
- [x] Write `skills/sub-simulation-engine.md`
- [x] Write `PROJECT-detail.md`
- [x] Write `PROJECT-DEVELOPMENT-PHASE-TRACKING.md`
- [x] Write `SECOND-KNOWLEDGE-BRAIN.md`
- [x] Write `tools/knowledge_updater.py`
- [x] Write `tools/cron-setup.md`
- [x] Write `tests/test-scenarios.md`
- [x] Write `tests/validate_skill.py`
- [x] Register skill in `.claude/skills/disaster-relief-distribution-simulation.md`
- [x] Verify frontmatter YAML and cross-skill wiring

---

## Reference Docs
- `PROJECT-detail.md` -- full technical specification
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` -- phase-by-phase build roadmap (100% complete)
- `SECOND-KNOWLEDGE-BRAIN.md` -- domain knowledge base (self-improving)
- `tests/test-scenarios.md` -- 6 end-to-end test scenarios with expected outputs
- `tools/cron-setup.md` -- scheduling instructions for the knowledge updater
