# OpenField — Paquete de planificación

Documentación de planificación de la plataforma **OpenField** (IoTinkers): captura
georreferenciada de terreno (imagen/video RGB y térmicos, audio del operador a texto) para
documentar instalaciones e inventarios industriales.

## Qué hay aquí
- `AGENTS.md` — reglas para agentes (OpenCode y Devin).
- `DECISIONS.md` — fuente única de las 16 decisiones.
- `ROLES.md` — roles architect / writer / reviewer por capacidad.
- `scripts/` — arnés de validación (esquemas, trazabilidad, documentación).
- `00-09/` — documentos del paquete (se generan en las tandas A–F).
- `.opencode/` y `.devin/` — adaptadores finos por framework.

## Cómo validar
```sh
python scripts/validate_schemas.py
python scripts/check_traceability.py
python scripts/check_docs.py
```

## Estado
Planificación. Niveles: Maker / Pro / Industrial. Presupuesto ≈ US$0.
Repos futuros: `openfield-wearable`, `openfield-platform`, `openfield-connectors`.
