# ADR-0011 · Equipos de prueba y túnel HTTPS

Estado: Aceptada
Fecha: 2026-11-11
Origen: D11 (`DECISIONS.md`)

## Contexto
Se dispone de un emulador Android en PC, un iPhone propio (validador de límites de Safari) y
un Android prestado. Para probar la PWA en el iPhone es necesario HTTPS con certificado válido;
la máquina de desarrollo no es accesible desde el teléfono sin un túnel.

## Decisión
- Equipos: emulador Android (PC), iPhone propio (validador de límites de Safari), Android
  prestado (pruebas puntuales).
- Acceso del teléfono a la máquina de desarrollo mediante **túnel HTTPS**.

Opciones verificadas (nov-2026):
- **Cloudflare Tunnel** (`cloudflared`, Apache-2.0): gratis en todos los planes, 1.000 túneles,
  sin cuota de ancho de banda. Un túnel con nombre necesita un dominio en Cloudflare; el
  *Quick Tunnel* (trycloudflare.com) no necesita dominio ni cuenta, pero da URL aleatoria por
  ejecución, tope de 200 peticiones en vuelo y sin garantía de uptime.
- **ngrok** (propietario): free = 1 dominio estático (ngrok-free.app), 1 GB y 20.000 peticiones/
  mes, y un *interstitial* en tráfico HTML del navegador (molesto para probar la PWA en iPhone).
- **Tailscale Funnel** (cliente open source): gratis en plan Personal, HTTPS público, pero en
  beta y con límites de puertos/banda.

## Alternativas consideradas
- ngrok free para todo (rechazado para PWA: el interstitial interfiere con la UI en el teléfono).
- Tailscale Funnel como única opción (rechazado: beta; se usa como complemento).

## Consecuencias
- Para pruebas puntuales: **Cloudflare Quick Tunnel** (sin cuenta/dominio, sin interstitial).
- Para URL estable: túnel con nombre de Cloudflare (requiere dominio) o Tailscale Funnel.
- Las condiciones cambian; se revisan antes de cada tanda que requiera HTTPS en el teléfono.
