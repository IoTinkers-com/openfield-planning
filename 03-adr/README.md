# 03 · Registro de decisiones de arquitectura (ADR)

> Estado: 22/22 aceptadas · Tanda B + revisión UX/UI + presentación por activo + gestión de activos · OpenField (IoTinkers)

Cada ADR corresponde a una decisión de `DECISIONS.md`. Formato: Contexto, Decisión,
Alternativas consideradas, Consecuencias, Estado.

## Índice
| ADR | Título | Decisión | Estado |
| --- | --- | --- | --- |
| ADR-0001 | Térmica (contrato canónico T0–T3) | D1 | Aceptada |
| ADR-0002 | Georreferenciación (WGS84 + UTM/SIRGAS2000 Latam) | D2 | Aceptada |
| ADR-0003 | Identificación de activos | D3 | Aceptada |
| ADR-0004 | Conectividad (offline-first) | D4 | Aceptada |
| ADR-0005 | Despliegue | D5 | Aceptada |
| ADR-0006 | Estructuración (plantillas primero) | D6 | Aceptada |
| ADR-0007 | Audio a texto | D7 | Aceptada |
| ADR-0008 | App de captura (PWA primero) | D8 | Aceptada |
| ADR-0009 | Contratos de datos | D9 | Aceptada |
| ADR-0010 | Desarrollo guiado por simulación | D10 | Aceptada |
| ADR-0011 | Equipos de prueba y túnel HTTPS | D11 | Aceptada |
| ADR-0012 | Caso de uso principal | D12 | Aceptada |
| ADR-0013 | Usuarios y multiempresa | D13 | Aceptada |
| ADR-0014 | Licencias | D14 | Aceptada |
| ADR-0015 | Privacidad | D15 | Aceptada |
| ADR-0016 | Límite industrial (ATEX/IECEx) | D16 | Aceptada |
| ADR-0017 | Protocolo de captura y desambiguación de activos | D17 | Aceptada |
| ADR-0018 | Consistencia visual y navegación entre dashboard y captura (UX/UI) | D18 | Aceptada |
| ADR-0019 | Presentación centrada en el activo (asset dossier) | D19 | Aceptada |
| ADR-0020 | Registro de activos y ciclo de vida | D20 | Aceptada |
| ADR-0021 | Edición, baja lógica y auditoría de documentos | D21 | Aceptada |
| ADR-0022 | Precarga de activos por CSV y verificación en terreno | D22 | Aceptada |
| ADR-0023 | Entrada de texto/voz en terreno y selección de cámara | D23 | Aceptada |

## Regla de cambio
No se reabren decisiones. Un cambio exige un **ADR nuevo** que reemplace al anterior: el ADR
reemplazado pasa a estado `Reemplazado por ADR-XXXX` y se mantiene en el índice como histórico.
