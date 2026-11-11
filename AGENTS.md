# AGENTS.md — OpenField (IoTinkers)

Reglas persistentes del paquete de planificación. Aplican por igual a **OpenCode** y **Devin**.
Fuente única de decisiones: `DECISIONS.md` · Roles: `ROLES.md` · Arnés: `scripts/`.

## Reglas de redacción (SIEMPRE)
1. Español; términos técnicos en inglés cuando sea estándar.
2. No inventar precios, versiones, licencias ni capacidades. Si un dato depende de
   información vigente, márcalo con la etiqueta VERIFICAR (entre corchetes) y cita la
   fuente si hay búsqueda web disponible.
3. Separar en cada documento: **Decisión tomada / Supuesto / Pregunta abierta**.
4. Incluir tabla **Maker | Pro | Industrial** cuando aplique (tecnología, protocolo y
   estándar por nivel).
5. Preferir componentes open source maduros; indicar licencia, riesgo de abandono y
   alternativa para cada uno.

## Reglas de cambio
6. No reabrir decisiones. Un cambio exige un ADR nuevo que **reemplace** al anterior
   (estado `Reemplazado por ADR-XXXX`).
7. Un sensor nuevo no puede exigir cambios en plataforma: solo un adaptador que cumpla
   el contrato canónico.

## Definición de terminado (por tanda)
8. Pasan `python scripts/validate_schemas.py`, `python scripts/check_traceability.py`
   y `python scripts/check_docs.py`.
9. No quedan contradicciones abiertas contra `DECISIONS.md`, ni etiquetas VERIFICAR sin
   resolver, antes de generar `09-prompts-repos/`.

## Límites de esta fase
10. Prohibido: código de aplicación, y comprar o recomendar compras de hardware.
    Solo plataformas, protocolos, estándares y flujo por nivel de madurez.
11. Git: un commit por tanda. No ejecutar comandos de red ni instalar paquetes sin
    confirmación explícita del usuario.

## Estructura mínima
- `DECISIONS.md` — las 17 decisiones (fuente única).
- `ROLES.md` — architect / writer / reviewer por capacidad (no por modelo).
- `scripts/` — validación de esquemas, trazabilidad y chequeo de documentación.
- `00-09/` — documentos del paquete (se crean en las tandas A–F).
- `.opencode/` y `.devin/` — adaptadores finos por framework.

## Estado
Fase de planificación. Repos futuros: `openfield-wearable`, `openfield-platform`,
`openfield-connectors`. Niveles: Maker / Pro / Industrial. Presupuesto ≈ US$0.
