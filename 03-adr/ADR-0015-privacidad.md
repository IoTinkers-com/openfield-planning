# ADR-0015 · Privacidad

Estado: Aceptada
Fecha: 2026-11-11
Origen: D15 (`DECISIONS.md`)

## Contexto
La captura en terreno puede incluir personas y audio ambiental de terceros. La normativa
chilena de datos personales está en transición.

## Decisión
- Indicador **visible** de grabación.
- Registro de **consentimiento**.
- Política de **retención**.
- Minimizar la captura de personas y del audio ambiental de terceros.

Normativa verificada (nov-2026):
- Rige **Ley 19.628** (sobre protección de la vida privada, 1999).
- **Ley 21.719** (publicada 13-dic-2024) modifica la Ley 19.628 y crea la **Agencia de
  Protección de Datos Personales**. Entra en vigor el **1-dic-2026**; existe un proyecto
  (Boletín 18.623-07, aprobado en el Senado) que la posterga al **15-oct-2027**.
- Con alcance multi-país Latam, la privacidad se verifica **por país** (no solo Chile).

## Alternativas consideradas
- Tratar privacidad como opcional (rechazado: riesgo legal y de confianza del cliente).

## Consecuencias
- El flujo de captura incluye consentimiento y señal de grabación antes de capturar.
- La retención se configura por tenant; el audio se guarda solo si se habilita (ADR-0007).
- Fecha exacta de vigencia de la Ley 21.719 a confirmar al momento de implementar.
