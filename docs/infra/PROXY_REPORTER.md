# Proxy de los reportes (Cloudflare Worker)

> **Para pegarle a Claude de escritorio:** este documento es autocontenido. Pegalo
> entero y pedile "guiame paso a paso con esto". Todo lo de acá se hace en las webs
> de Discord y de Cloudflare; el cambio en el código del juego lo hace Claude Code
> cuando tengas la URL del Worker (paso 4).

## Qué problema resuelve

El juego manda dos tipos de reporte a Discord, cada uno a su canal:

| Reporte | Qué manda | Constante en el juego |
|---|---|---|
| Errores (botón del crash) | JSON `{"content": ...}` | `JP_WEBHOOK_URL` en `game/script/core/utils/sistema_reporte_errores.rpy` |
| Feedback de jugadores | JSON, o multipart con una captura PNG | `JP_WEBHOOK_FEEDBACK_URL` en `game/script/core/utils/sistema_feedback.rpy` |

Hoy las dos URLs de webhook de Discord están **escritas tal cual en el código que
viaja con el juego** (y en el historial de git). Con esa URL cualquiera puede
postear en el canal, **borrar el webhook** o mencionar a @everyone. Además, un
script en texto plano que manda datos a `discord.com/api/webhooks/...` es de lo
que buscan los antivirus (alerta Wacatac del 2026-09-29).

La solución: el juego le manda el reporte a un **Worker de Cloudflare** (gratis) y
el Worker lo reenvía a Discord. Las URLs de Discord quedan guardadas como
**secretos** del Worker y no vuelven a aparecer en el juego.

---

## Paso 1 — Discord: crear dos webhooks NUEVOS

Se crean nuevos (no se regeneran los viejos todavía) para que las versiones del
juego que ya están publicadas sigan reportando hasta que salga la próxima.

1. Canal de **errores** → ⚙ Editar canal → **Integraciones** → **Webhooks** →
   **Nuevo webhook** → nombre `Japitown errores (proxy)` → **Copiar URL del webhook**.
   Guardala en un bloc de notas como `ERRORES = https://discord.com/api/webhooks/...`
2. Lo mismo en el canal de **feedback** → nombre `Japitown feedback (proxy)` →
   guardala como `FEEDBACK = ...`

Estas dos URLs **no se pegan en ningún otro lado** que no sea el paso 2.5.

## Paso 2 — Cloudflare: crear el Worker

1. Entrar a https://dash.cloudflare.com (crear cuenta gratis si no hay).
2. **Workers & Pages** → **Create** → **Create Worker** (plantilla "Hello World").
3. Nombre: `japitown-reporter` → **Deploy**.
4. **Edit code** → borrar todo lo que haya → pegar el código de abajo (sección
   *worker.js*) → **Deploy**.
5. Volver al Worker → **Settings** → **Variables and Secrets** → **Add**, dos veces:

   | Type | Variable name | Value |
   |---|---|---|
   | **Secret** | `DISCORD_WEBHOOK_ERRORES` | la URL `ERRORES` del paso 1 |
   | **Secret** | `DISCORD_WEBHOOK_FEEDBACK` | la URL `FEEDBACK` del paso 1 |

   Los nombres tienen que ser **exactamente** esos (mayúsculas y guion bajo).
   Tipo **Secret**, no "Text" — Text queda visible en el panel. **Deploy** al final.
6. Copiar la URL pública del Worker, arriba en su página. Tiene la forma
   `https://japitown-reporter.ALGO.workers.dev`

## Paso 3 — Probar que funciona (antes de tocar el juego)

En **PowerShell** de Windows (reemplazar la URL por la del paso 2.6):

```powershell
$w = "https://japitown-reporter.ALGO.workers.dev"
Invoke-RestMethod -Method Post -Uri "$w/error"    -ContentType "application/json" -Body '{"content":"prueba del proxy: errores"}'
Invoke-RestMethod -Method Post -Uri "$w/feedback" -ContentType "application/json" -Body '{"content":"prueba del proxy: feedback"}'
```

Cada comando tiene que responder `ok : True` y el mensaje tiene que aparecer en
**su** canal de Discord. Si responde otra cosa, ver *Si algo falla* abajo.

## Paso 4 — Pasarle la URL a Claude Code

Pasarle a Claude Code (en VS Code) la URL del Worker del paso 2.6. Claude Code
cambia las dos constantes del juego a:

```
JP_WEBHOOK_URL          = "https://japitown-reporter.ALGO.workers.dev/error"
JP_WEBHOOK_FEEDBACK_URL = "https://japitown-reporter.ALGO.workers.dev/feedback"
```

y se prueba desde el juego: un feedback con captura y uno sin captura.

## Paso 5 — Cuando la versión nueva ya esté publicada: borrar los webhooks viejos

En Discord, **borrar** los dos webhooks viejos (los que no dicen "proxy"). Recién
ahí la URL filtrada queda muerta. Las versiones viejas del juego dejan de poder
reportar — es el precio, y por eso se hace después de publicar.

---

## worker.js

```js
// Proxy de reportes de Japitown -> Discord.
// El juego postea a /error o /feedback; el Worker reenvia el cuerpo TAL CUAL
// (bytes, no texto: el feedback puede traer una captura PNG en multipart) al
// webhook que corresponde, guardado como secreto.

const RUTAS = {
  "/error": "DISCORD_WEBHOOK_ERRORES",
  "/feedback": "DISCORD_WEBHOOK_FEEDBACK",
};

// Discord acepta hasta 10 MB por mensaje sin boost; una captura 1920x1080 en
// PNG anda por 1-4 MB.
const MAX_BYTES = 9 * 1024 * 1024;

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400",
};

function responder(estado, cuerpo) {
  return new Response(JSON.stringify(cuerpo), {
    status: estado,
    headers: { ...CORS, "Content-Type": "application/json" },
  });
}

export default {
  async fetch(request, env) {
    // Preflight CORS (el build web del juego corre en el navegador)
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS });
    }
    if (request.method !== "POST") {
      return responder(405, { ok: false, error: "metodo" });
    }

    const secreto = RUTAS[new URL(request.url).pathname];
    if (!secreto || !env[secreto]) {
      return responder(404, { ok: false, error: "ruta" });
    }

    // Solo los dos formatos que manda el juego
    const tipo = request.headers.get("Content-Type") || "";
    if (!tipo.startsWith("application/json") && !tipo.startsWith("multipart/form-data")) {
      return responder(415, { ok: false, error: "tipo" });
    }

    const cuerpo = await request.arrayBuffer();
    if (cuerpo.byteLength > MAX_BYTES) {
      return responder(413, { ok: false, error: "tamanio" });
    }

    try {
      const r = await fetch(env[secreto], {
        method: "POST",
        // Se reenvia el Content-Type original: en multipart lleva el boundary.
        headers: { "Content-Type": tipo },
        body: cuerpo,
      });
      // Discord responde 204 al exito; se devuelve 200 para que el juego lo tome como OK.
      return responder(r.ok ? 200 : 502, { ok: r.ok, status: r.status });
    } catch (e) {
      return responder(502, { ok: false, error: "reenvio" });
    }
  },
};
```

---

## Si algo falla

| Respuesta | Causa |
|---|---|
| `404 ruta` | La URL no termina en `/error` o `/feedback`, o el secreto de esa ruta no existe o tiene el nombre mal escrito (paso 2.5). |
| `502` con `status: 401` o `404` | La URL de Discord guardada en el secreto está mal copiada o el webhook se borró. |
| `502` con `status: 400` | Discord rechazó el contenido (ej. mensaje de más de 2000 caracteres). |
| `415 tipo` | La prueba no mandó `-ContentType "application/json"`. |
| Error de red / DNS | El Worker no está desplegado, o la URL tiene un typo. |

## Lo que el proxy NO resuelve

La URL del Worker también queda en el juego: cualquiera puede mandarle mensajes y
llegan a Discord. Lo que sí se gana: no pueden borrar ni editar el webhook, no
se ve la URL de Discord, y si alguien abusa se puede cortar desde Cloudflare sin
tocar Discord. Un token compartido no serviría (también viajaría en el juego).
