# DECISIONS.md — fuente única de decisiones

> **Contexto:** IoTinkers · **OpenField**. Captura georreferenciada de terreno (imagen/video
> RGB y térmicos; audio del operador a texto) para documentar el estado de instalaciones e
> inventarios industriales. Niveles: **Maker / Pro / Industrial**. Etapas del flujo:
> captura → preprocesamiento → transporte → ingesta → almacenamiento → estructuración →
> presentación → integración externa.

## Repositorios (4)
Organización GitHub: `iotinkers-com` (los 4 repos viven bajo esta organización).

| Repo | Responsabilidad |
| --- | --- |
| `openfield-wearable` | Captura: app PWA, firmware y hardware de referencia. *(renombrado de `iotinkers-wearable`)* |
| `openfield-platform` | Backend, ingesta, almacenamiento, estructuración, UI, informes. |
| `openfield-connectors` | Adaptadores a dispositivos/sistemas externos + `simulators/`. |
| `openfield-planning` | Este paquete documental. |

## Decisiones (D1–D17)
Cada decisión tendrá un ADR en `03-adr/`. Regla de cambio: no reabrir; un cambio exige un
ADR nuevo que reemplace al anterior.

| # | Decisión | ADR |
| --- | --- | --- |
| D1 | **Térmica.** Visual (paleta) en Maker; radiométrica desde Pro. Contrato canónico de 4 niveles T0–T3. Todo adaptador normaliza a: matriz de temperaturas en °C + imagen renderizada + JSON (modelo de sensor, resolución, emisividad, temperatura reflejada, distancia, nivel T0–T3). El original propietario se conserva como evidencia. | ADR-0001 |
| D2 | **Georreferenciación.** GPS en exteriores; QR/TAG de activo en interiores. WGS84 (EPSG:4326) internamente; exportación a proyección UTM (zona según ubicación) sobre SIRGAS2000 / densificación nacional, para Latinoamérica (no limitado a Chile). | ADR-0002 |
| D3 | **Identificación de activos.** QR propio (generado por la plataforma), TAG/placa existente del cliente y OCR, como identificadores equivalentes del mismo activo. | ADR-0003 |
| D4 | **Conectividad.** Offline-first como base (ID único generado en el dispositivo, cola local, subidas reanudables con `tus`, sincronización de reloj). Live (RTMP/WebRTC) es opcional con tope de calidad y de datos configurable. Live a redes sociales es prioridad secundaria. | ADR-0004 |
| D5 | **Despliegue.** Desarrollo local con Docker; VPS pequeño para demos live. Presupuesto ≈ US$0. Diseñado para autohospedarse (on-premise) más adelante. | ADR-0005 |
| D6 | **Estructuración.** Plantillas de formulario/checklist configurables primero; IA como apoyo después, siempre con validación humana. | ADR-0006 |
| D7 | **Audio a texto.** Local si el dispositivo lo permite (p. ej. Whisper), con respaldo en la plataforma. Cada transcripción registra el motor que la generó. Audio original opcional por sesión. | ADR-0007 |
| D8 | **App de captura.** PWA primero; capa de acceso a hardware desacoplada para envolver con Capacitor o pasar a nativo después. Límites iOS/Safari documentados: sin Background Sync, IndexedDB puede purgarse, sin WebUSB/WebBluetooth, GPS solo en primer plano, Whisper local en WASM por validar. | ADR-0008 |
| D9 | **Contratos de datos.** JSON Schema propio versionado (`schema_version`; solo se agregan campos, nunca se rompen). Compatible con GeoJSON, STAC y OGC SensorThings. Exportación STAC y OGC API Features (lectura) desde Pro. SensorThings, OPC UA y ONVIF mediante conectores en Industrial. | ADR-0009 |
| D10 | **Desarrollo guiado por simulación.** Fase 0 sin hardware. Simuladores (cámara térmica T0–T2, repetición de sesiones grabadas, rutas GPX, inventario ficticio con QR/TAG, telemetría MQTT) son el conjunto de pruebas de contrato de los conectores reales. | ADR-0010 |
| D11 | **Equipos de prueba.** Emulador Android en PC; iPhone propio (validador de límites de Safari); Android prestado para pruebas puntuales. Teléfono ↔ máquina de desarrollo mediante túnel HTTPS (ADR; verificar condiciones vigentes de las opciones). | ADR-0011 |
| D12 | **Caso de uso principal (primeros 3 meses).** Inventario de equipos eléctricos/industriales. | ADR-0012 |
| D13 | **Usuarios.** Un solo usuario al inicio; `tenant_id` en el esquema para pasar a multiempresa sin migraciones. | ADR-0013 |
| D14 | **Licencias.** Apache 2.0 para software; CERN-OHL para hardware; módulos empresariales cerrados opcionales más adelante. | ADR-0014 |
| D15 | **Privacidad.** Indicador visible de grabación, registro de consentimiento, política de retención, minimizar captura de personas y audio ambiental de terceros. Verificar ley chilena de protección de datos personales vigente. | ADR-0015 |
| D16 | **Límite industrial.** Nunca presentar el sistema como apto para atmósferas explosivas ni como equipo de seguridad. ATEX/IECEx solo se menciona como requisito futuro del equipo completo, sin asumir certificación. | ADR-0016 |
| D17 | **Desambiguación de activos.** Protocolo de captura por activo (identificador explícito al inicio) + reglas/agentes de atribución; la IA es apoyo, nunca la fuente primaria de identidad, con validación humana. Deriva de D3 y D6. | ADR-0017 |
