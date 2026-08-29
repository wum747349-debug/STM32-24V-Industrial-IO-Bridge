#!/usr/bin/env python3
"""Validate a Framework v1 standalone hardware project repository."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


REQUIRED_FILES = (
    "AGENTS.md",
    "FRAMEWORK.md",
    "PROJECT_RULES.md",
    "README.md",
    "requirements.md",
    "block_diagram.md",
    "design_notes.md",
    "references.md",
    "docs/README.md",
    "hardware/README.md",
    "references/README.md",
    "scripts/validate_project_repository.py",
)

REQUIRED_DIRECTORIES = {
    "docs",
    "hardware",
    "references",
    "scripts",
}

FRAMEWORK_FIELDS = (
    "Framework Repository",
    "Framework Release",
    "Framework Commit",
    "Project Structure Version",
    "Repository Model",
    "Initialization Framework Release",
    "Initialization Status",
)

TEMPLATE_BINDING = {
    "Framework Repository": "<FRAMEWORK_REPOSITORY>",
    "Framework Release": "<FRAMEWORK_RELEASE>",
    "Framework Commit": "<FRAMEWORK_COMMIT>",
    "Project Structure Version": "<PROJECT_STRUCTURE_VERSION>",
    "Repository Model": "Standalone Project",
    "Initialization Framework Release": "<INITIALIZATION_FRAMEWORK_RELEASE>",
    "Initialization Status": "<INITIALIZATION_STATUS>",
}

EXPECTED_TEMPLATE_PLACEHOLDERS = {
    "<PROJECT_NAME>",
    "<HARDWARE_REVISION>",
    "<FRAMEWORK_REPOSITORY>",
    "<FRAMEWORK_RELEASE>",
    "<FRAMEWORK_COMMIT>",
    "<PROJECT_STRUCTURE_VERSION>",
    "<INITIALIZATION_FRAMEWORK_RELEASE>",
    "<INITIALIZATION_STATUS>",
}

STAGES = {
    1: "Requirements Definition",
    2: "Critical Component Selection",
    3: "Schematic Module Design and Capture",
    4: "Schematic Review",
    5: "PCB Layout",
    6: "Routing and Copper",
    7: "PCB Release Review",
    8: "Assembly, Bring-up and Hardware Test",
}

STAGE_FILES = {
    2: ("docs/component_selection_plan.md",),
    4: ("docs/schematic_review.md",),
    5: ("docs/pcb_design_rules.md",),
    6: ("docs/pcb_review.md",),
}

ACTIVITY_ENABLED_FILES = (
    "docs/bringup_log.md",
    "docs/test_report.md",
    "docs/revision_history.md",
)

ALL_STAGE_PATHS = (
    *(path for paths in STAGE_FILES.values() for path in paths),
    *ACTIVITY_ENABLED_FILES,
)

GATE_REQUIREMENT_SECTIONS = (
    "Project Goal",
    "Out of Scope",
    "Functional Boundary",
    "Module Boundary",
    "Power Requirements",
    "Interface Requirements",
    "Safety Boundary",
    "Manufacturing Baseline",
    "Acceptance Criteria",
    "Open Questions",
)

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PLACEHOLDER = re.compile(r"<[A-Z][A-Z0-9_]*>")
ABSOLUTE_LOCAL_PATH = re.compile(
    r"(?i)(?<![A-Za-z0-9])(?:[A-Z]:[\\/]|/Users/|/home/|/mnt/[a-z]/)"
)
FRAMEWORK_RUNTIME_DEPENDENCY = re.compile(
    r"(?i)^\s*(?:[-*]\s*)?(?:Framework|Monorepo)\s+Runtime\s+(?:Path|Dependency)\s*:\s*(.*?)\s*$"
)
NO_RUNTIME_DEPENDENCY = {"", "none", "n/a", "not required", "无", "不需要"}
DEVELOPMENT_RELEASE = re.compile(r"development-v(?:0\.9|\d+\.\d+\.\d+)")
FORMAL_RELEASE = re.compile(r"hardware-project-framework-v\d+\.\d+\.\d+(?:-rc\d+)?")
FULL_SHA = re.compile(r"[0-9a-fA-F]{40}")


class Validator:
    def __init__(self, root: Path, template_mode: bool, gate_1_5: bool) -> None:
        self.root = root.resolve()
        self.template_mode = template_mode
        self.gate_1_5 = gate_1_5
        self.errors: list[str] = []
        self.check_count = 0
        self.binding: dict[str, str] = {}
        self.stage_number: int | None = None
        self.stage_text = ""

    def check(self, condition: bool, path: str, reason: str) -> None:
        self.check_count += 1
        if not condition:
            self.errors.append(f"{path}: {reason}")

    def read(self, relative_path: str) -> str:
        return (self.root / relative_path).read_text(encoding="utf-8")


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if " " in target and not target.startswith(("http://", "https://")):
        target = target.split(" ", 1)[0]
    return unquote(target.split("#", 1)[0])


def check_required_structure(validator: Validator) -> None:
    validator.check(validator.root.is_dir(), str(validator.root), "project root does not exist")
    for relative_path in REQUIRED_FILES:
        validator.check(
            (validator.root / relative_path).is_file(),
            relative_path,
            "missing Required file",
        )

    if validator.template_mode:
        actual_files = {
            path.relative_to(validator.root).as_posix()
            for path in validator.root.rglob("*")
            if path.is_file()
        }
        validator.check(
            actual_files == set(REQUIRED_FILES),
            ".",
            "Template must contain exactly the Required files; Conditional and Stage-enabled files are not pre-created",
        )
        actual_directories = {
            path.relative_to(validator.root).as_posix()
            for path in validator.root.rglob("*")
            if path.is_dir()
        }
        validator.check(
            actual_directories == REQUIRED_DIRECTORIES,
            ".",
            "Template must contain exactly the Required directories; empty Conditional and Stage-enabled directories are not pre-created",
        )


def parse_binding(validator: Validator) -> None:
    path = validator.root / "FRAMEWORK.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    for field in FRAMEWORK_FIELDS:
        values = re.findall(
            rf"^{re.escape(field)}:\s*(.*?)\s*$", text, flags=re.MULTILINE
        )
        validator.check(len(values) == 1, "FRAMEWORK.md", f"field must appear exactly once: {field}")
        if len(values) == 1:
            validator.binding[field] = values[0]

    if len(validator.binding) != len(FRAMEWORK_FIELDS):
        return

    if validator.template_mode:
        for field, expected in TEMPLATE_BINDING.items():
            validator.check(
                validator.binding[field] == expected,
                "FRAMEWORK.md",
                f"Template binding field must be {expected}: {field}",
            )
        return

    repository = validator.binding["Framework Repository"]
    release = validator.binding["Framework Release"]
    commit = validator.binding["Framework Commit"]
    structure_version = validator.binding["Project Structure Version"]
    model = validator.binding["Repository Model"]
    initialization_release = validator.binding["Initialization Framework Release"]
    status = validator.binding["Initialization Status"]

    validator.check(bool(repository) and not ABSOLUTE_LOCAL_PATH.search(repository), "FRAMEWORK.md", "Framework Repository must be a repository identity, not a local path")
    validator.check(DEVELOPMENT_RELEASE.fullmatch(release) is not None or FORMAL_RELEASE.fullmatch(release) is not None, "FRAMEWORK.md", "Framework Release must be development-v0.9, development-vX.Y.Z, or a versioned published Framework release")
    validator.check(FULL_SHA.fullmatch(commit) is not None, "FRAMEWORK.md", "Framework Commit must be a full 40-character Git SHA")
    validator.check(structure_version == "1", "FRAMEWORK.md", "Project Structure Version must be 1")
    validator.check(model == "Standalone Project", "FRAMEWORK.md", "Repository Model must be Standalone Project")
    validator.check(DEVELOPMENT_RELEASE.fullmatch(initialization_release) is not None or FORMAL_RELEASE.fullmatch(initialization_release) is not None, "FRAMEWORK.md", "Initialization Framework Release must be development-v0.9, development-vX.Y.Z, or a versioned published Framework release")
    validator.check(status in {"Bootstrap Draft", "Gate 1.5 Pending", "Initialized", "Development Bootstrap"}, "FRAMEWORK.md", "invalid Initialization Status")


def parse_stage(validator: Validator) -> None:
    path = validator.root / "README.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    values = re.findall(r"^Current Project Stage:\s*(.*?)\s*$", text, flags=re.MULTILINE)
    validator.check(len(values) == 1, "README.md", "Current Project Stage must appear exactly once")
    if len(values) != 1:
        return
    value = values[0]
    validator.stage_text = value
    if value == "Bootstrap":
        return
    match = re.fullmatch(r"Stage ([1-8]) — (.+)", value)
    validator.check(match is not None, "README.md", "invalid Current Project Stage format")
    if match is None:
        return
    number = int(match.group(1))
    validator.check(match.group(2) == STAGES[number], "README.md", "stage number and canonical name do not match")
    if match.group(2) == STAGES[number]:
        validator.stage_number = number


def check_stage_enabled(validator: Validator) -> None:
    if validator.template_mode or validator.stage_number is None:
        return
    for threshold, paths in STAGE_FILES.items():
        if validator.stage_number >= threshold:
            for relative_path in paths:
                validator.check(
                    (validator.root / relative_path).is_file(),
                    relative_path,
                    f"Stage {validator.stage_number} requires this Stage-enabled file",
                )
    if validator.stage_number >= 3:
        module_root = validator.root / "docs/module_design"
        module_files = list(module_root.glob("*.md")) if module_root.is_dir() else []
        validator.check(bool(module_files), "docs/module_design", f"Stage {validator.stage_number} requires at least one module design document")


def check_initialization_state(validator: Validator) -> None:
    if validator.template_mode or not validator.binding:
        return
    status = validator.binding.get("Initialization Status")
    if validator.stage_text == "Bootstrap":
        validator.check(
            status in {"Bootstrap Draft", "Development Bootstrap"},
            "FRAMEWORK.md",
            "Bootstrap requires Initialization Status: Bootstrap Draft or Development Bootstrap",
        )
    elif validator.stage_number == 1:
        validator.check(
            status in {"Gate 1.5 Pending", "Initialized"},
            "FRAMEWORK.md",
            "Stage 1 requires Initialization Status: Gate 1.5 Pending or Initialized",
        )
    elif validator.stage_number is not None:
        validator.check(
            status == "Initialized",
            "FRAMEWORK.md",
            f"Stage {validator.stage_number} requires Initialization Status: Initialized",
        )


def check_placeholders(validator: Validator) -> None:
    found: set[str] = set()
    for path in validator.root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        relative_path = path.relative_to(validator.root).as_posix()
        if relative_path == "scripts/validate_project_repository.py":
            continue
        found.update(PLACEHOLDER.findall(text))
        validator.check(
            ABSOLUTE_LOCAL_PATH.search(text) is None,
            relative_path,
            "contains a local absolute path",
        )

    if validator.template_mode:
        validator.check(found == EXPECTED_TEMPLATE_PLACEHOLDERS, ".", "Template placeholder set does not match the Contract")
    else:
        validator.check(not found, ".", f"unreplaced Template placeholder(s): {', '.join(sorted(found))}")


def check_markdown_links(validator: Validator) -> None:
    for markdown_file in validator.root.rglob("*.md"):
        text = markdown_file.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in MARKDOWN_LINK.finditer(line):
                target = normalize_link_target(match.group(1))
                if not target or target.startswith("#"):
                    continue
                if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
                    continue
                target_path = (markdown_file.parent / target).resolve()
                try:
                    target_path.relative_to(validator.root)
                except ValueError:
                    validator.check(False, f"{markdown_file.relative_to(validator.root)}:{line_number}", f"relative link escapes project root: {match.group(1)}")
                    continue
                validator.check(target_path.exists(), f"{markdown_file.relative_to(validator.root)}:{line_number}", f"relative link target does not exist: {match.group(1)}")


def check_standalone_independence(validator: Validator) -> None:
    for markdown_file in validator.root.rglob("*.md"):
        text = markdown_file.read_text(encoding="utf-8")
        relative_path = markdown_file.relative_to(validator.root).as_posix()
        for line_number, line in enumerate(text.splitlines(), start=1):
            match = FRAMEWORK_RUNTIME_DEPENDENCY.match(line)
            if match is None:
                continue
            value = match.group(1).strip().lower()
            validator.check(
                value in NO_RUNTIME_DEPENDENCY,
                f"{relative_path}:{line_number}",
                "Standalone Project must not declare a Framework or monorepo runtime path/dependency",
            )


def check_runtime_contract(validator: Validator) -> None:
    agents = validator.root / "AGENTS.md"
    rules = validator.root / "PROJECT_RULES.md"
    if agents.is_file():
        text = agents.read_text(encoding="utf-8")
        for phrase in ("Read `FRAMEWORK.md` first", "bound Framework Release", "Do not default to Framework `main`", "Do not read another Project"):
            validator.check(phrase in text, "AGENTS.md", f"missing startup routing contract: {phrase}")
    if rules.is_file():
        text = rules.read_text(encoding="utf-8")
        validator.check(len(re.findall(r"^\d+\. ", text, flags=re.MULTILINE)) == 10, "PROJECT_RULES.md", "Project Runtime Rules must contain the ten Contract rules")
        for phrase in ("facts come only from this repository", "Framework version", "Pinned Framework Evaluation", "Compatible Framework Sync", "Framework Contract Migration", ".SchDoc", ".PcbDoc", "current Project stage only", "Stage Skill"):
            validator.check(phrase in text, "PROJECT_RULES.md", f"missing Project Runtime Rule coverage: {phrase}")


def check_gate_1_5(validator: Validator) -> None:
    if not validator.gate_1_5:
        return
    validator.check(not validator.template_mode, "--gate-1-5", "Gate mode cannot be combined with Template mode")
    validator.check(validator.stage_number == 1, "README.md", "Gate 1.5 requires Current Project Stage to be Stage 1")
    validator.check(validator.binding.get("Initialization Status") == "Gate 1.5 Pending", "FRAMEWORK.md", "Gate 1.5 validation requires Initialization Status: Gate 1.5 Pending")

    readme_path = validator.root / "README.md"
    if readme_path.is_file():
        text = readme_path.read_text(encoding="utf-8")
        identities = re.findall(r"^Project Identity:\s*(.*?)\s*$", text, flags=re.MULTILINE)
        validator.check(len(identities) == 1 and identities[0] not in {"", "TBD", "待确认"}, "README.md", "Gate 1.5 requires one real Project Identity")

    requirements_path = validator.root / "requirements.md"
    if requirements_path.is_file():
        text = requirements_path.read_text(encoding="utf-8")
        for section in GATE_REQUIREMENT_SECTIONS:
            validator.check(re.search(rf"^##\s+{re.escape(section)}\s*$", text, flags=re.MULTILINE) is not None, "requirements.md", f"Gate 1.5 missing Requirements Baseline section: {section}")

    for relative_path in ALL_STAGE_PATHS:
        validator.check(not (validator.root / relative_path).exists(), relative_path, "Stage-enabled file must not be pre-created at Gate 1.5")
    validator.check(not (validator.root / "docs/module_design").exists(), "docs/module_design", "Stage-enabled module directory must not be pre-created at Gate 1.5")

    premature = re.compile(r"(?im)^(?:ERC|DRC|Manufacturing|Bring-up|Test)\s*(?:Status|Result)?\s*:\s*(?:PASS|Passed|Complete|Completed|通过|完成)\s*$")
    for markdown_file in validator.root.rglob("*.md"):
        text = markdown_file.read_text(encoding="utf-8")
        validator.check(premature.search(text) is None, markdown_file.relative_to(validator.root).as_posix(), "Gate 1.5 contains a premature downstream result claim")


def validate(root: Path, template_mode: bool = False, gate_1_5: bool = False) -> Validator:
    validator = Validator(root, template_mode, gate_1_5)
    check_required_structure(validator)
    parse_binding(validator)
    parse_stage(validator)
    check_initialization_state(validator)
    check_stage_enabled(validator)
    check_placeholders(validator)
    check_markdown_links(validator)
    check_standalone_independence(validator)
    check_runtime_contract(validator)
    check_gate_1_5(validator)
    return validator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_path", nargs="?", help="Project repository root; defaults to the repository containing this script")
    parser.add_argument("--template", action="store_true", help="validate the uninitialized Framework Template and its required placeholders")
    parser.add_argument("--gate-1-5", action="store_true", help="validate the Stage 1 Gate 1.5 structural contract")
    args = parser.parse_args(argv)

    root = Path(args.project_path).resolve() if args.project_path else Path(__file__).resolve().parents[1]
    validator = validate(root, template_mode=args.template, gate_1_5=args.gate_1_5)
    if validator.errors:
        print(f"Project repository validation failed: {len(validator.errors)} error(s)")
        for error in validator.errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Project repository validation passed ({validator.check_count} checks).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
