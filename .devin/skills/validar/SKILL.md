---
name: validar
description: Ejecuta los chequeos del arnés y reporta el resultado
---

Ejecuta los tres chequeos del arnés y resume si pasan o qué falla:

```sh
python scripts/validate_schemas.py
python scripts/check_traceability.py
python scripts/check_docs.py
```

Si algo falla, describe el problema y dónde corregirlo.
