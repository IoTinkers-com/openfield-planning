# ADR-0018 · Consistencia visual y navegación entre dashboard y captura

Estado: Aceptada
Fecha: 2026-11-11
Origen: D18 (`DECISIONS.md`)

## Contexto
El dashboard (`openfield-platform`) y la PWA de captura (`openfield-wearable`, desplegada
también desde `openfield-platform/app/static/pwa/` en el mismo origen) son dos superficies
de UI separadas, construidas en HTML/CSS/JS plano sin framework (D8). La revisión de UX/UI
de Fase 0/1 encontró inconsistencia visual entre ambas (colores, botones, textos de estado)
y falta de navegación directa entre una y otra, lo que obliga al operador a conocer las URLs
de memoria.

## Decisión
- **Design tokens compartidos:** una hoja de estilos (`openfield.css` / `style.css`) con
  variables CSS (color, tipografía, espaciado, componentes: barra superior, tarjetas,
  botones, badges de estado, stepper, estados vacíos) se **duplica** entre repos, siguiendo
  el mismo patrón ya usado para la capa de hardware y `capture.js`/`sync.js`/`ids.js`
  (`openfield-wearable/app/` ≈ `openfield-platform/app/static/pwa/`): no se introduce un
  paquete npm/pip compartido en esta fase.
- **Navegación directa:** cada superficie incluye un enlace explícito a la otra en su barra
  superior. En `openfield-platform` (mismo origen, D8) el enlace es una ruta relativa
  (`/`, `/capture/`); en el modo de desarrollo standalone de `openfield-wearable`
  (servido aparte, ver ADR-0011) el enlace usa la URL absoluta de la plataforma
  (`http://localhost:8000/`), igual que ya hace `BASE_URL` en `app/sync.js`.
- **Estados visuales estándar:** una paleta reducida de estados (éxito, advertencia, error,
  pendiente) se aplica igual en ambas superficies para indicadores de grabación (D15),
  conexión/cola pendiente (D4) y pasos del flujo de captura (D8).

## Alternativas consideradas
- Extraer un paquete de UI compartido (`openfield-ui`) publicado en un registro propio
  (rechazado por ahora: añade infraestructura de build/publish antes de tener un segundo
  consumidor real más allá de las dos superficies actuales; revisar si aparece una tercera).
- Framework de frontend (React/Vue) con sistema de diseño propio (rechazado: D8 fija HTML/JS
  plano para mantener la capa de captura ligera y desacoplada; no hay justificación de
  producto para el costo de migración en Fase 0/1).
- No enlazar ambas superficies y documentar las URLs solo en el README (rechazado: obliga al
  operador a cambiar de pestaña de memoria; es la causa raíz del hallazgo de UX).

## Consecuencias
- Un cambio de diseño visual debe aplicarse en los 2-3 archivos CSS duplicados hasta que
  exista un tercer consumidor que justifique extraer un paquete compartido.
- La navegación entre apps no depende de favoritos ni de recordar puertos/URLs.
- Los textos de estado (éxito/advertencia/error) quedan centralizados en una convención de
  clases CSS, reduciendo inconsistencias de redacción en español entre ambas superficies.
- No cambia ningún contrato de datos (`04-esquemas/`) ni el flujo de las 8 etapas (`02-flujo-de-datos.md`).
