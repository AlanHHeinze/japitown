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
