# Static validation harness for Skill #242.

"""
validate_skill.py -- Static validation harness for Skill #242.

This script performs a no-network validation of the disaster-relief-distribution-simulation
skill package. It checks that all markdown skill files have valid frontmatter, that every
required section is present, that all 10 quality gates are wired into the harness, and that
the Scenario 1 formulas are computable from the documented Sphere Standards constants.

Usage:
    python tests/validate_skill.py

Exit codes:
    0 -- all validation checks passed
    1 -- one or more checks failed
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
CLAUDE_SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
TOOLS_DIR = REPO_ROOT / "tools"
TESTS_DIR = REPO_ROOT / "tests"

REQUIRED_SKILL_FILES = [
    SKILLS_DIR / "main.md",
    SKILLS_DIR / "sub-profile-intake.md",
    SKILLS_DIR / "sub-needs-assessment.md",
    SKILLS_DIR / "sub-logistics-optimizer.md",
    SKILLS_DIR / "sub-simulation-engine.md",
]

SUB_SKILL_REQUIRED_SECTIONS = [
    "## Purpose",
    "## Inputs",
    "## Workflow",
    "## Outputs",
    "## Quality Gate",
]

MAIN_REQUIRED_SECTIONS = [
    "## Role & Persona",
    "## Workflow",
    "## Sub-skills Available",
    "## Tools",
    "## Output Format",
    "## Cross-Skill Wiring",
    "## Quality Gates",
]

QUALITY_GATE_IDS = [f"QG-{i}" for i in range(1, 11)]

SCENARIO_1_SPHERE_CONSTANTS = {
    "water_l_per_person_day": 15.0,
    "food_cereals_g_per_person_day": 450.0,
    "food_pulses_g_per_person_day": 60.0,
    "food_oil_g_per_person_day": 25.0,
    "food_sugar_g_per_person_day": 15.0,
    "shelter_m2_per_person": 3.5,
    "persons_per_household": 5.0,
}


class SkillValidator:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def validate_frontmatter(self, path: Path) -> dict:
        """Extract and validate YAML frontmatter from a skill markdown file."""
        content = path.read_text(encoding="utf-8-sig")
        if not content.startswith("---"):
            self.fail(f"{path.name}: missing opening frontmatter delimiter")
            return {}

        end_marker = content.find("---", 3)
        if end_marker == -1:
            self.fail(f"{path.name}: missing closing frontmatter delimiter")
            return {}

        fm_text = content[3:end_marker].strip()
        if not fm_text:
            self.fail(f"{path.name}: empty frontmatter")
            return {}

        if yaml is None:
            # Fallback: parse minimal `name:` and `description:` manually.
            parsed = {}
            for line in fm_text.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    parsed[key.strip()] = value.strip()
        else:
            try:
                parsed = yaml.safe_load(fm_text)
            except yaml.YAMLError as e:
                self.fail(f"{path.name}: invalid YAML frontmatter: {e}")
                return {}

        if not isinstance(parsed, dict):
            self.fail(f"{path.name}: frontmatter is not a YAML mapping")
            return {}

        for required_key in ("name", "description"):
            if required_key not in parsed or not parsed[required_key]:
                self.fail(f"{path.name}: frontmatter missing '{required_key}'")

        return parsed

    def validate_required_sections(self, path: Path, sections: list[str]) -> None:
        """Check that all required section headers exist in the file."""
        content = path.read_text(encoding="utf-8-sig")
        missing = [s for s in sections if s not in content]
        if missing:
            self.fail(
                f"{path.name}: missing required sections: {', '.join(missing)}"
            )

    def validate_quality_gates(self, main_path: Path, sub_paths: list[Path]) -> None:
        """Ensure every QG-1..QG-10 is referenced at least once across the skill files."""
        all_text = main_path.read_text(encoding="utf-8-sig")
        for p in sub_paths:
            all_text += p.read_text(encoding="utf-8-sig")

        for qg in QUALITY_GATE_IDS:
            if qg not in all_text:
                self.fail(f"Quality gate {qg} is not referenced in any skill file")

    def validate_registered_skill(self) -> None:
        """Check that the skill is registered under .claude/skills/."""
        registered = CLAUDE_SKILLS_DIR / "disaster-relief-distribution-simulation.md"
        if not registered.exists():
            self.fail("Skill is not registered at .claude/skills/disaster-relief-distribution-simulation.md")
            return

        # Verify the registered copy has valid frontmatter too.
        self.validate_frontmatter(registered)

    def validate_python_tools(self) -> None:
        """Compile-check Python tools."""
        updater = TOOLS_DIR / "knowledge_updater.py"
        if not updater.exists():
            self.fail("tools/knowledge_updater.py is missing")
            return

        try:
            compile(updater.read_text(encoding="utf-8-sig"), updater.name, "exec")
        except SyntaxError as e:
            self.fail(f"tools/knowledge_updater.py has a syntax error: {e}")

        cron_doc = REPO_ROOT / "tools" / "cron-setup.md"
        if not cron_doc.exists():
            self.fail("tools/cron-setup.md is missing")

    def validate_scenario_1_computability(self) -> None:
        """Recalculate Scenario 1 expected needs from the documented constants."""
        pop = 45_000
        days = 7
        c = SCENARIO_1_SPHERE_CONSTANTS

        total_water = c["water_l_per_person_day"] * pop * days
        daily_food_kg = (
            c["food_cereals_g_per_person_day"]
            + c["food_pulses_g_per_person_day"]
            + c["food_oil_g_per_person_day"]
            + c["food_sugar_g_per_person_day"]
        ) / 1000.0 * pop
        total_food = daily_food_kg * days / 1000.0  # MT
        nfi_kits = pop / c["persons_per_household"]
        nfi_mt = nfi_kits * 20.0 / 1000.0  # MT

        expected_water_kl = 4_725.0
        expected_food_mt = 173.25
        expected_nfi_mt = 180.0

        if abs(total_water - expected_water_kl * 1000) > 1.0:
            self.fail(
                f"Scenario 1 water mismatch: computed {total_water} L, expected {expected_water_kl * 1000} L"
            )
        if abs(total_food - expected_food_mt) > 0.1:
            self.fail(
                f"Scenario 1 food mismatch: computed {total_food:.2f} MT, expected {expected_food_mt} MT"
            )
        if abs(nfi_mt - expected_nfi_mt) > 0.1:
            self.fail(
                f"Scenario 1 NFI mismatch: computed {nfi_mt:.2f} MT, expected {expected_nfi_mt} MT"
            )

    def validate_knowledge_brain(self) -> None:
        """Check that SECOND-KNOWLEDGE-BRAIN.md has the required sections."""
        kb = REPO_ROOT / "SECOND-KNOWLEDGE-BRAIN.md"
        if not kb.exists():
            self.fail("SECOND-KNOWLEDGE-BRAIN.md is missing")
            return

        content = kb.read_text(encoding="utf-8-sig")
        required_sections = [
            "## 1. Core Concepts & Frameworks",
            "## 2. Key Research Papers",
            "## 3. State-of-the-Art Methods & Tools",
            "## 4. Authoritative Data Sources",
            "## 5. Analytical Frameworks",
            "## 6. Self-Update Protocol",
            "## 7. Knowledge Update Log",
        ]
        missing = [s for s in required_sections if s not in content]
        if missing:
            self.fail(
                f"SECOND-KNOWLEDGE-BRAIN.md missing sections: {', '.join(missing)}"
            )

        # Check for at least 10 seeded papers.
        paper_rows = re.findall(r"^\|\s*\d+\s*\|", content, re.MULTILINE)
        if len(paper_rows) < 10:
            self.fail(
                f"SECOND-KNOWLEDGE-BRAIN.md has only {len(paper_rows)} seeded papers (need >= 10)"
            )

    def validate_cross_skill_references(self, main_path: Path) -> None:
        """Ensure main.md references the required cluster shared sub-skills."""
        content = main_path.read_text(encoding="utf-8-sig")
        required_refs = [
            "sub-evaluation-framework-selector",
            "sub-scoring-engine",
            "sub-improvement-roadmap",
        ]
        missing = [r for r in required_refs if r not in content]
        if missing:
            self.fail(
                f"main.md missing cross-skill references: {', '.join(missing)}"
            )

    def run_all(self) -> bool:
        print("=" * 70)
        print("Skill #242 Static Validation Harness")
        print("=" * 70)

        main_path = SKILLS_DIR / "main.md"

        # Frontmatter on all skill files.
        for path in REQUIRED_SKILL_FILES:
            print(f"\n[FRONTMATTER] {path.name}")
            self.validate_frontmatter(path)
            if path == main_path:
                self.validate_required_sections(path, MAIN_REQUIRED_SECTIONS)
            else:
                self.validate_required_sections(path, SUB_SKILL_REQUIRED_SECTIONS)

        # Quality gate wiring.
        print("\n[QUALITY GATES]")
        self.validate_quality_gates(main_path, [p for p in REQUIRED_SKILL_FILES if p != main_path])

        # Skill registration.
        print("\n[REGISTRATION]")
        self.validate_registered_skill()

        # Python tools.
        print("\n[PYTHON TOOLS]")
        self.validate_python_tools()

        # Scenario 1 formulas.
        print("\n[SCENARIO 1 COMPUTABILITY]")
        self.validate_scenario_1_computability()

        # Knowledge brain.
        print("\n[KNOWLEDGE BRAIN]")
        self.validate_knowledge_brain()

        # Cross-skill wiring.
        print("\n[CROSS-SKILL WIRING]")
        self.validate_cross_skill_references(main_path)

        print("\n" + "=" * 70)
        if self.errors:
            print(f"FAILURES: {len(self.errors)}")
            for e in self.errors:
                print(f"  FAIL: {e}")
        else:
            print("All validation checks passed.")

        if self.warnings:
            print(f"\nWARNINGS: {len(self.warnings)}")
            for w in self.warnings:
                print(f"  WARN: {w}")
        print("=" * 70)
        return len(self.errors) == 0


if __name__ == "__main__":
    validator = SkillValidator()
    ok = validator.run_all()
    sys.exit(0 if ok else 1)