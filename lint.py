#!/usr/bin/env python3
"""Linting tool for Tower of the Sorcerer roguelike game."""

import ast
import os
import sys
from pathlib import Path

SRC_DIR = Path(__file__).parent / "src"

LAYER_ORDER = ["types", "config", "repo", "service", "runtime", "ui", "providers", "utils"]

STDLIB_MODULES = {"enum", "typing", "builtins", "os", "sys", "math", "random", "string", "re"}

LAYER_IMPORTS = {
    "types": ["types"],
    "config": ["types", "config"],
    "repo": ["types", "config", "repo"],
    "service": ["types", "config", "repo", "providers", "service"],
    "runtime": ["types", "config", "repo", "service", "providers", "runtime"],
    "ui": ["types", "config", "service", "runtime", "providers", "ui"],
    "providers": ["types", "config", "utils", "providers"],
    "utils": ["utils"],
}

MAX_LINES = 300


def get_layer(filepath: Path) -> str | None:
    """Determine which layer a file belongs to."""
    rel_path = filepath.relative_to(SRC_DIR)
    parts = rel_path.parts
    if len(parts) > 0 and parts[0] in LAYER_ORDER:
        return parts[0]
    return None


def get_imports(filepath: Path) -> list[tuple[str, int]]:
    """Extract import statements from a Python file."""
    imports = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(filepath))
    except SyntaxError:
        return imports

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((alias.name, node.lineno))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append((node.module, node.lineno))
            elif node.level and node.names:
                imports.append((".", node.lineno))

    return imports


def check_layer_membership(all_files: list[Path]) -> list[tuple[Path, int, str]]:
    """Check that every file belongs to exactly one layer."""
    violations = []
    for filepath in all_files:
        layer = get_layer(filepath)
        if layer is None:
            violations.append((filepath, 1, f"File does not belong to any layer directory"))
    return violations


def check_imports(all_files: list[Path]) -> list[tuple[Path, int, str]]:
    """Check that imports respect layer dependency chain."""
    violations = []
    for filepath in all_files:
        layer = get_layer(filepath)
        if layer is None:
            continue

        allowed = LAYER_IMPORTS.get(layer, [])
        imports = get_imports(filepath)

        for module, lineno in imports:
            base_module = module.split(".")[0]
            if base_module in STDLIB_MODULES:
                continue
            if base_module not in allowed:
                violations.append(
                    (filepath, lineno, f"Import '{module}' violates layer dependencies (cannot import from {base_module})")
                )
    return violations


def check_utils_no_internal_imports(all_files: list[Path]) -> list[tuple[Path, int, str]]:
    """Check that utils files have no internal imports."""
    violations = []
    for filepath in all_files:
        layer = get_layer(filepath)
        if layer != "utils":
            continue

        imports = get_imports(filepath)
        if imports:
            for module, lineno in imports:
                violations.append(
                    (filepath, lineno, f"Utils file has illegal internal import '{module}'")
                )
    return violations


def check_line_limits(all_files: list[Path]) -> list[tuple[Path, int, str]]:
    """Check that no file exceeds MAX_LINES."""
    violations = []
    for filepath in all_files:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) > MAX_LINES:
            violations.append(
                (filepath, 1, f"File exceeds {MAX_LINES} lines ({len(lines)} lines)")
            )
    return violations


def main() -> int:
    """Run all lint checks."""
    all_files = []
    for root, _, files in os.walk(SRC_DIR):
        for filename in files:
            if filename.endswith(".py"):
                all_files.append(Path(root) / filename)

    all_violations = []

    all_violations.extend(check_layer_membership(all_files))
    all_violations.extend(check_imports(all_files))
    all_violations.extend(check_utils_no_internal_imports(all_files))
    all_violations.extend(check_line_limits(all_files))

    if all_violations:
        print("Lint violations found:\n")
        for filepath, lineno, message in all_violations:
            print(f"{filepath}:{lineno}: {message}")
        return 1

    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
