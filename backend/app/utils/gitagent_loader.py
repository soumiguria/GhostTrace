"""Load agent prompts from GitAgent skill definitions (single source of truth)."""

import re
from pathlib import Path

# Repo root: backend/app/utils -> backend -> repo root
REPO_ROOT = Path(__file__).resolve().parents[3]
GITAGENT_DIR = REPO_ROOT / "gitagent"
SKILLS_DIR = GITAGENT_DIR / "skills"

# Maps legacy prompt names to GitAgent skill folder names
SKILL_MAP = {
    "entity_extraction": "entity-extraction",
    "reputation": "reputation-analysis",
    "risk_scoring": "risk-scoring",
    "report_generator": "report-generation",
}


def _strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter from SKILL.md."""
    if content.startswith("---"):
        match = re.match(r"^---\s*\n.*?\n---\s*\n", content, re.DOTALL)
        if match:
            return content[match.end() :].strip()
    return content.strip()


def load_skill_prompt(name: str) -> str | None:
    """
    Load investigation prompt from gitagent/skills/{skill}/SKILL.md.
    Returns None if skill file is missing (caller falls back to services/prompts/).
    """
    skill_dir = SKILL_MAP.get(name, name.replace("_", "-"))
    skill_path = SKILLS_DIR / skill_dir / "SKILL.md"
    if not skill_path.is_file():
        return None
    return _strip_frontmatter(skill_path.read_text(encoding="utf-8"))


def gitagent_root() -> Path:
    return GITAGENT_DIR
