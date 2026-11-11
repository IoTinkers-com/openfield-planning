#!/usr/bin/env python3
"""Chequea documentación: enlaces relativos rotos y etiquetas VERIFICAR pendientes.

Analiza los documentos producidos (00-09). Ignora el arnés mismo (AGENTS.md, DECISIONS.md,
ROLES.md, README.md, .opencode/, .devin/).

Salida:
- 0 = OK.
- 1 = hay enlaces rotos (siempre), o quedan VERIFICAR pendientes con `--strict`.
"""
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

LINK_RE = re.compile(r"\]\(([^)]+)\)")
VERIF_RE = re.compile(r"\[VERIFICAR\]")

SKIP_DIRS = {".opencode", ".devin", ".git"}
SKIP_FILES = {"AGENTS.md", "DECISIONS.md", "ROLES.md", "README.md"}


def is_local(target: str) -> bool:
    t = target.strip()
    return not t.startswith(("http://", "https://", "mailto:", "#", "<"))


def main(argv):
    strict = "--strict" in argv
    root = Path(".")
    md_files = []
    for p in root.rglob("*.md"):
        if p.parts[0] in SKIP_DIRS or str(p) in SKIP_FILES:
            continue
        md_files.append(p)
    md_files.sort()

    broken = []
    verif_locations = []

    for f in md_files:
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, line in enumerate(lines, 1):
            if VERIF_RE.search(line):
                verif_locations.append(f"{f}:{i}")
            for m in LINK_RE.finditer(line):
                target = m.group(1).strip()
                if not is_local(target):
                    continue
                target = target.split("#")[0]
                if not target:
                    continue
                if not (f.parent / target).resolve().exists():
                    broken.append(f"{f}:{i} -> {target}")

    if broken:
        print(f"ENLACES ROTOS ({len(broken)}):")
        for b in broken:
            print("  -", b)

    print(f"VERIFICAR pendientes: {len(verif_locations)}")
    for loc in verif_locations:
        print("  -", loc)

    if broken:
        print("FALLÓ: hay enlaces rotos.")
        return 1
    if strict and verif_locations:
        print("FALLÓ (--strict): quedan VERIFICAR sin resolver.")
        return 1
    print("OK: sin enlaces rotos.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
