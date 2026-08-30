import { NextResponse } from "next/server";

/**
 * Health check do Next, separado do `/health` do Frappe (Fase G.2, Parte
 * B, seção 31). Só status -- nenhuma versão, stack ou dado de config.
 */
export async function GET() {
  return NextResponse.json({ status: "ok" });
}
