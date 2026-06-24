# Disaster Relief Distribution Simulation & Optimization (NGO)

**Skill #242 | Cluster: science-industry**

A Claude Code skill that simulates, optimizes, and operationalizes emergency disaster relief distribution for NGOs using operations research (VRP, LP), game theory (Nash equilibrium), Sphere Standards, and real-time humanitarian data.

---

## What it does

Given a disaster context (type, location, affected population, vehicles, warehouses, budget, time horizon), the skill produces a professional-grade **Operational Disaster Relief Distribution Plan** with:

1. **Profile intake** -- validated disaster context and resource inventory.
2. **Needs assessment** -- Sphere Standards-based needs matrix and IPC classification.
3. **Logistics optimization** -- Clarke-Wright VRP heuristic, LP allocation, Nash equilibrium multi-agency coordination, and cash vs. in-kind modality rubric.
4. **Scenario analysis** -- stress tests for road blocks, budget cuts, demand surges, and weather events, plus contingency plans.
5. **Quality gate review** -- Sphere compliance, humanitarian principles, and citation traceability.

## Repository layout

```
.
+-- .claude/skills/disaster-relief-distribution-simulation.md   # Skill registration for Claude Code CLI
+-- CLAUDE.md                                                 # Skill identity, harness flow, and active tasks
+-- PROJECT-detail.md                                        # Full technical specification
+-- PROJECT-DEVELOPMENT-PHASE-TRACKING.md                     # Phase-by-phase build roadmap (100% complete)
+-- SECOND-KNOWLEDGE-BRAIN.md                               # Self-improving domain knowledge base
+-- README.md                                                 # This file
+-- requirements.txt                                         # Python dependencies
+-- skills/
|   +-- main.md                                            # Primary harness entry point
|   +-- sub-profile-intake.md                              # Intake and validation sub-skill
|   +-- sub-needs-assessment.md                            # Sphere/IPC needs assessment sub-skill
|   +-- sub-logistics-optimizer.md                        # VRP/LP/Nash optimization sub-skill
|   +-- sub-simulation-engine.md                           # Scenario simulation sub-skill
+-- tests/
|   +-- test-scenarios.md                                 # 6 detailed end-to-end test scenarios
|   +-- validate_skill.py                                # Static validation harness
+-- tools/
    +-- knowledge_updater.py                               # crawl4ai-aware knowledge base updater
    +-- cron-setup.md                                      # Scheduling instructions
```

## Quick start

### Install dependencies
```bash
pip install -r requirements.txt
```

### Validate the skill package
```bash
python tests/validate_skill.py
```

### Update the knowledge base
```bash
# Dry run (no writes)
python tools/knowledge_updater.py --dry-run

# Live update (appends new entries to SECOND-KNOWLEDGE-BRAIN.md)
python tools/knowledge_updater.py

# Use crawl4ai for JavaScript-heavy sources (requires crawl4ai installed)
python tools/knowledge_updater.py --use-crawl4ai
```

### Schedule the updater
See `tools/cron-setup.md` for Windows Task Scheduler, Linux/macOS cron, and Kubernetes CronJob examples.

## Invoke the skill in Claude Code

Once the repository is in your Claude Code workspace:

```
/disaster-relief-distribution-simulation
```

Example prompt:
> "Earthquake in Turkiye, Kahramanmaras Province, 45,000 displaced, 4 trucks (5 MT each), 2 warehouses, 7-day window."

## Production notes

- **No live model inference or training is required.** All optimization is rule-based (Clarke-Wright, LP formulation, Nash equilibrium assignment).
- **Live network calls are optional.** The skill gracefully degrades to `SECOND-KNOWLEDGE-BRAIN.md` when WebSearch/WebFetch are unavailable.
- **Sphere Standards are non-negotiable.** Any plan that cannot meet minimums is flagged and escalated.
- **Rate limiting and retries** are built into `tools/knowledge_updater.py` to respect source servers.

## Validation

Run the static harness before any release:

```bash
python tests/validate_skill.py
```

Expected output:
```
======================================================================
Skill #242 Static Validation Harness
======================================================================
...
======================================================================
All validation checks passed.
======================================================================
```

## License

Open-source release. See the project tracker for attribution and citations.
