---
name: trazabilidad
description: Verifica trazabilidad backlog <-> ADR
---

Ejecuta la verificación de trazabilidad y reporta el mapeo backlog <-> ADR:

```sh
python scripts/check_traceability.py
```

Si hay requisitos sin ADR, o ADR citados que no existen, lista cada uno con su línea.
