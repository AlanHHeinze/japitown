# Proxy del reportador de errores (Cloudflare Worker)

Este proxy recibe el reporte del juego y lo reenvía a Discord. Sirve para **ocultar
la URL del webhook** (queda solo acá, no en el juego público) y agrega los headers
CORS necesarios.

> El juego postea a la URL del Worker; el Worker reenvía a Discord. El webhook de
> Discord NUNCA aparece en los archivos del juego.

---

## Paso a paso (gratis, ~5 min)

1. Entrá a https://dash.cloudflare.com (creá cuenta gratis si no tenés).
2. **Workers & Pages** → **Create** → **Create Worker**.
3. Ponele un nombre, ej. `japitown-reporter` → **Deploy**.
4. **Edit code**: borrá lo que haya y pegá el contenido de `worker.js` (abajo) → **Deploy**.
5. **Settings** → **Variables and Secrets** → **Add**:
   - Tipo: **Secret**
   - Name: `DISCORD_WEBHOOK_URL`
   - Value: la URL del webhook de Discord
   - **Deploy** / Save.
6. Copiá la URL pública del Worker (algo como
   `https://japitown-reporter.TU-SUBDOMINIO.workers.dev`).
7. **Pasámela** y yo cambio `JP_WEBHOOK_URL` en el juego para que apunte ahí.

### Seguridad (importante)
La URL del webhook de Discord actual **ya está en el repo público / historial de git**,
así que conviene:
- En Discord: **regenerar** (o borrar y crear de nuevo) el webhook del canal.
- Poner la URL **nueva** SOLO en el secret del Worker (`DISCORD_WEBHOOK_URL`).
- Así la URL vieja queda muerta y la nueva nunca toca el juego.

---

## worker.js

```js
export default {
  async fetch(request, env) {
    const cors = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Max-Age": "86400",
    };

    // Preflight CORS
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: cors });
    }
    if (request.method !== "POST") {
      return new Response("Method Not Allowed", { status: 405, headers: cors });
    }

    // Cuerpo (JSON del reporte). Límite defensivo de tamaño.
    let body = "";
    try { body = await request.text(); } catch (e) {}
    if (body.length > 4000) body = body.slice(0, 4000);

    // Reenviar a Discord
    try {
      const r = await fetch(env.DISCORD_WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body,
      });
      // Discord responde 204 al éxito. Devolvemos 200 para que renpy.fetch lo tome como OK.
      return new Response(JSON.stringify({ ok: r.ok, status: r.status }), {
        status: r.ok ? 200 : 502,
        headers: { ...cors, "Content-Type": "application/json" },
      });
    } catch (e) {
      return new Response(JSON.stringify({ ok: false, error: "forward_failed" }), {
        status: 502,
        headers: { ...cors, "Content-Type": "application/json" },
      });
    }
  },
};
```

---

## Del lado del juego
No hay que cambiar nada del código de envío: el juego ya postea el mismo JSON
(`{"content": ...}`) con `renpy.fetch`. Solo se cambia `JP_WEBHOOK_URL` a la URL del
Worker (lo hago yo cuando me pases la URL). El Worker reenvía ese body tal cual a Discord.
