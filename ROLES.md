# ROLES.md — roles por capacidad (independiente del framework)

Los roles se definen por **capacidad**, no por modelo. Cada adaptador (`.opencode/`,
`.devin/`) mapea la capacidad al modelo real de su marco.

## architect
- **Función:** decisiones, flujo, ADRs, esquemas. Razonamiento más fuerte.
- **Redacta:** `00-vision-alcance.md`, `01-niveles-escalamiento.md`, `02-flujo-de-datos.md`,
  `03-adr/`, `04-esquemas/` (esquemas, no ejemplos), `05-estructura-repos.md`,
  `07-simulacion-y-pruebas.md`, `08-riesgos-y-supuestos.md`, `09-prompts-repos/`.
- **Permisos:** lee y escribe documentos; puede consultar web (para verificar datos vigentes);
  lanza los subagentes writer y reviewer; ejecuta git y los scripts del arnés.
- **Modelo OpenCode:** `opencode-go/deepseek-v4-pro` · **Devin:** `A TU ELECCIÓN` (más fuerte).

## writer
- **Función:** ejemplos JSON, backlog, tablas repetitivas. Rápido y barato.
- **Redacta:** `04-esquemas/examples/`, `06-backlog-mvp.md`, y las tablas repetitivas de
  `01-niveles-escalamiento.md` y `02-flujo-de-datos.md`.
- **Permisos:** escribe SOLO en las carpetas asignadas; sin web; sin shell.
- **Modelo OpenCode:** `opencode-go/glm-5.3-flash` · **Devin:** `A TU ELECCIÓN` (rápido).

## reviewer
- **Función:** detecta contradicciones contra `DECISIONS.md`. Modelo **distinto del autor**.
- **Permisos:** solo lectura + ejecutar los scripts del arnés (nada más). Sin web.
- **Modelo OpenCode:** `opencode-go/qwen3.8-max` · **Devin:** `A TU ELECCIÓN` (distinto del autor).

## Regla
Un mismo modelo no revisa su propio texto: el rol **reviewer** debe usar un modelo diferente
al que redactó el documento bajo revisión.
