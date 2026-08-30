import { NextRequest, NextResponse } from "next/server";

/**
 * Route Handler intermediário para o formulário de `/contato` (Fase F.3).
 *
 * Nunca React -> DocType Frappe diretamente (missão seção 12). Este
 * handler roda no servidor Next, valida o payload (inclusive o
 * honeypot), e só então repassa para o endpoint real já auditado em
 * `docs/frontend-v2/23-contact-form-integration-audit.md`:
 *
 *   POST https://app.vediums.com/api/method/vedium_core.public_funnel.submit_public_intent
 *
 * `intent` usa só os valores reais de `ALLOWED_INTENTS`
 * (vedium_core/public_funnel.py) -- "lead" ou "b2b" nesta página, nunca
 * um valor inventado.
 */

const FRAPPE_ENDPOINT = "https://app.vediums.com/api/method/vedium_core.public_funnel.submit_public_intent";
const ALLOWED_INTENTS = new Set(["lead", "b2b"]);
const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

interface ContactPayload {
  name?: string;
  email?: string;
  phone?: string;
  intent?: string;
  goal?: string;
  language?: string;
  message?: string;
  // Honeypot -- campo invisível para humanos (ver ContactForm.tsx). Se
  // vier preenchido, é bot: reportamos sucesso sem repassar nada ao
  // backend real (nem gasta a cota de rate-limit do Frappe com lixo).
  companyWebsite?: string;
}

export async function POST(request: NextRequest) {
  let body: ContactPayload;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ ok: false, field: null, message: "Não foi possível ler os dados enviados." }, { status: 400 });
  }

  if (body.companyWebsite) {
    return NextResponse.json({ ok: true });
  }

  const name = (body.name || "").trim();
  const email = (body.email || "").trim();
  const intent = ALLOWED_INTENTS.has(body.intent || "") ? body.intent! : "lead";

  if (!name) {
    return NextResponse.json({ ok: false, field: "name", message: "Informe seu nome." }, { status: 422 });
  }
  if (!email || !EMAIL_RE.test(email)) {
    return NextResponse.json({ ok: false, field: "email", message: "Informe um e-mail válido." }, { status: 422 });
  }

  const goalParts = [body.goal, body.language && body.language !== "Não sei ainda" ? `Idioma: ${body.language}` : null].filter(Boolean);

  const forwardBody = {
    intent,
    name,
    email,
    phone: (body.phone || "").trim(),
    goal: goalParts.join(" | "),
    message: (body.message || "").trim(),
    source: "https://vediums.com/contato",
  };

  let upstream: Response;
  try {
    upstream = await fetch(FRAPPE_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(forwardBody),
    });
  } catch {
    return NextResponse.json({ ok: false, field: null, message: "Não foi possível enviar agora. Você também pode chamar no WhatsApp." }, { status: 502 });
  }

  if (!upstream.ok) {
    let message = "Não foi possível enviar agora. Você também pode chamar no WhatsApp.";
    try {
      const errorBody = await upstream.json();
      const serverMessage = extractFrappeMessage(errorBody);
      if (serverMessage) message = serverMessage;
    } catch {
      // resposta não era JSON -- mantém a mensagem genérica
    }
    const status = upstream.status === 429 ? 429 : 502;
    return NextResponse.json({ ok: false, field: null, message }, { status });
  }

  return NextResponse.json({ ok: true });
}

function extractFrappeMessage(errorBody: unknown): string | null {
  if (!errorBody || typeof errorBody !== "object") return null;
  const body = errorBody as Record<string, unknown>;
  if (typeof body._server_messages === "string") {
    try {
      const parsed = JSON.parse(body._server_messages) as string[];
      const first = parsed[0];
      if (first) {
        const inner = JSON.parse(first) as { message?: string };
        if (inner.message) return inner.message.replace(/<[^>]+>/g, "");
      }
    } catch {
      // ignora -- cai no fallback abaixo
    }
  }
  if (typeof body.exception === "string") {
    const parts = body.exception.split(":");
    return parts[parts.length - 1]?.trim() || null;
  }
  return null;
}
