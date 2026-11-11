#!/usr/bin/env python3
"""Valida ejemplos contra los JSON Schemas de 04-esquemas/.

Convención de nombres (definida en 04-esquemas/README.md):
- Esquemas:                04-esquemas/<stem>.schema.json
- Ejemplo válido:          04-esquemas/examples/valid/<stem>.<desc>.json   -> debe VALIDAR
- Ejemplo inválido:        04-esquemas/examples/invalid/<stem>.<desc>.json -> debe FALLAR

Un ejemplo inválido debe ser JSON bien formado (parseable); lo que falla es la
validación contra el esquema, no el parseo.

Salida: 0 = todo OK (o nada que validar aún); 1 = alguna violación.
"""
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from jsonschema import Draft202012Validator, validators
    from jsonschema import exceptions as jsonschema_exc
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


def validator_for(schema: dict):
    """Elige el validador según $schema declarado; por defecto draft 2020-12."""
    if "$schema" in schema:
        try:
            return validators.validator_for(schema)
        except Exception:
            pass
    return Draft202012Validator


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def stem_of(name: str) -> str:
    """`session.valid.json` -> `session`; `session.otro.json` -> `session`."""
    return name.split(".")[0]


def main(argv):
    root = Path(argv[1]) if len(argv) > 1 else Path("04-esquemas")
    if not root.is_dir():
        print(f"[skip] no existe {root}; nada que validar aún.")
        return 0

    schemas = {p.name.split(".")[0]: load_json(p) for p in sorted(root.glob("*.schema.json"))}
    if not schemas:
        print("[skip] sin esquemas (*.schema.json); nada que validar aún.")
        return 0

    if not HAS_JSONSCHEMA:
        print("ERROR: falta la librería 'jsonschema'. Instálala con:  pip install jsonschema")
        return 1

    errors = []

    def collect(d: Path):
        m = {}
        if d.is_dir():
            for p in sorted(d.glob("*.json")):
                m.setdefault(stem_of(p.name), []).append(p)
        return m

    valid_map = collect(root / "examples" / "valid")
    invalid_map = collect(root / "examples" / "invalid")

    # 1) Todo ejemplo válido debe validar.
    for stem, paths in valid_map.items():
        if stem not in schemas:
            errors.append(f"ejemplo válido sin esquema correspondiente: {stem}")
            continue
        vcls = validator_for(schemas[stem])
        for p in paths:
            try:
                vcls(schemas[stem]).validate(load_json(p))
            except jsonschema_exc.ValidationError as e:
                errors.append(f"VÁLIDO que falla: {p.relative_to(root)} -> {e.message}")
            except Exception as e:  # pragma: no cover
                errors.append(f"error inesperado en {p.relative_to(root)}: {e}")

    # 2) Todo ejemplo inválido debe FALLAR (y ser JSON bien formado).
    for stem, paths in invalid_map.items():
        if stem not in schemas:
            errors.append(f"ejemplo inválido sin esquema correspondiente: {stem}")
            continue
        vcls = validator_for(schemas[stem])
        for p in paths:
            try:
                data = load_json(p)
            except json.JSONDecodeError as e:
                errors.append(f"INVÁLIDO mal formado (no es JSON): {p.relative_to(root)} -> {e}")
                continue
            try:
                vcls(schemas[stem]).validate(data)
                errors.append(f"INVÁLIDO que SÍ valida: {p.relative_to(root)}")
            except jsonschema_exc.ValidationError:
                pass  # correcto: debe fallar
            except Exception as e:  # pragma: no cover
                errors.append(f"error inesperado en {p.relative_to(root)}: {e}")

    # 3) Cada esquema debe tener al menos 1 ejemplo válido y 1 inválido.
    for stem in schemas:
        if stem not in valid_map:
            errors.append(f"esquema sin ejemplo válido: {stem}")
        if stem not in invalid_map:
            errors.append(f"esquema sin ejemplo inválido: {stem}")

    if errors:
        print(f"FALLÓ ({len(errors)} problema(s)):")
        for e in errors:
            print("  -", e)
        return 1

    print(f"OK: {len(schemas)} esquema(s); ejemplos válidos/inválidos correctos.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
