#!/usr/bin/env python3
r"""Verifica trazabilidad backlog <-> ADR.

Reglas (definidas en 06-backlog-mvp.md, Tanda E):
- Cada requisito del backlog es una línea de tarea `- [ ] ...` / `- [x] ...`
  o un encabezado de historia `### ...`, y DEBE citar un ADR con el patrón `ADR-\d+`.
- Cada ADR citado debe existir como `03-adr/ADR-\d+*.md`.
- Cada ADR debe declarar un campo `Estado:`.

Salida: 0 = OK (o sin datos aún); 1 = violaciones.
"""
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

BACKLOG = Path("06-backlog-mvp.md")
ADR_DIR = Path("03-adr")

ADR_RE = re.compile(r"ADR-(\d+)")
ITEM_RE = re.compile(r"^\s*-\s+\[[ xX]\]\s+")
STORY_RE = re.compile(r"^###\s+")


def adr_files():
    if not ADR_DIR.is_dir():
        return {}
    out = {}
    for p in ADR_DIR.glob("*.md"):
        m = ADR_RE.search(p.name)
        if m:
            out[m.group(0)] = p
    return out


def main(argv):
    adrs = adr_files()

    if not BACKLOG.is_file():
        print("[skip] no existe 06-backlog-mvp.md; nada que verificar aún.")
        return 0

    violations = []

    # 1) Cada ADR declara Estado:
    for adr_id, p in sorted(adrs.items()):
        text = p.read_text(encoding="utf-8")
        if not re.search(r"^\s*Estado\s*:", text, re.MULTILINE):
            violations.append(f"{p} no declara 'Estado:'")

    # 2) Cada requisito cita un ADR.
    cited = set()
    items = 0
    for i, line in enumerate(BACKLOG.read_text(encoding="utf-8").splitlines(), 1):
        if ITEM_RE.match(line) or STORY_RE.match(line):
            items += 1
            m = ADR_RE.search(line)
            if not m:
                violations.append(f"{BACKLOG}:{i} requisito sin cita de ADR: {line.strip()}")
            else:
                cited.add(m.group(0))

    # 3) Todo ADR citado existe.
    for c in sorted(cited):
        if c not in adrs:
            violations.append(f"ADR citado pero inexistente: {c}")

    if items == 0:
        print("[skip] backlog sin requisitos detectados; revisa el formato de 06-backlog-mvp.md.")
        return 0

    if violations:
        print(f"FALLÓ ({len(violations)}):")
        for v in violations:
            print("  -", v)
        return 1

    print(f"OK: {items} requisito(s) con ADR; {len(adrs)} ADR(s) con estado.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
