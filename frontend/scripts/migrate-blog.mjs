// Script de migração do Blog (Fase F.5) -- LEITURA E DIAGNÓSTICO, não
// escreve nada em produção nem no Frappe. Lê a fonte real de código
// (vedium_core/blog_content.py) e cruza com a auditoria oficial já feita
// na planilha SEO/GEO v3 (aba Publicados_Auditoria, snapshot de
// 26/07/2026, já convertida para JSON em scripts/data/
// blog-publicados-auditoria.json), gerando o mapa de migração exigido em
// docs/frontend-v2/27-blog-url-migration-map.csv.
//
// REGRA ABSOLUTA (correção do usuário, 2026-08-30): a data de publicação
// (`date` no dict) NUNCA é sobrescrita por este script. Quando o dict e a
// auditoria discordam, o artigo é marcado DATE_CONFLICT = REVIEW
// REQUIRED -- nenhuma das duas datas é escolhida automaticamente como
// "a certa".
//
// Rodar com: node scripts/migrate-blog.mjs
// (dry run por natureza -- só lê e escreve o CSV de saída, não toca no
// Frappe nem em nenhum conteúdo já publicado.)

import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const BLOG_CONTENT_PATH = path.resolve(__dirname, "../../vedium_core/vedium_core/blog_content.py");
const AUDIT_JSON_PATH = path.resolve(__dirname, "data/blog-publicados-auditoria.json");
const OUT_CSV_PATH = path.resolve(__dirname, "../../docs/frontend-v2/27-blog-url-migration-map.csv");

// Pilares reais já aprovados no Next (Fases D/D.2-D.5/E.1) -- NÃO usar os
// slugs da planilha SEO/GEO v3 sem checar contra o que já existe: a
// planilha cita "/para-empresas" e "/en/brazilian-portuguese-course-
// online", nenhum dos dois confirmado por HTTP nesta sessão. B2B real é
// "/empresas" (Fase E.1). PLE em pt-BR real é "/portugues-para-
// estrangeiros" (Fase D.3); o pilar em inglês da planilha fica como
// REVIEW até ser confirmado.
const PILLAR_BY_FRENTE = {
  "Iorubá": "/curso-de-ioruba-online",
  "Inglês (curso)": "/curso-de-ingles-online",
  "Espanhol (curso)": "/curso-de-espanhol-online",
  "Hebraico (curso)": "/curso-de-hebraico-online",
  "Português para Estrangeiros - Base Global": "REVIEW: planilha cita /en/brazilian-portuguese-course-online, não confirmado por HTTP nesta sessão",
  "Português para Estrangeiros - Multilíngue": "REVIEW: planilha cita /en/brazilian-portuguese-course-online, não confirmado por HTTP nesta sessão",
};

const CLUSTER_BY_FRENTE = {
  "Iorubá": "Iorubá",
  "Inglês (curso)": "Inglês",
  "Espanhol (curso)": "Espanhol",
  "Hebraico (curso)": "Hebraico",
  "Português para Estrangeiros - Base Global": "PLE (inglês)",
  "Português para Estrangeiros - Multilíngue": "PLE (multilíngue -- frente congelada, ver Diagnóstico)",
};

function normalizeTitle(title) {
  return title
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "") // remove acentos
    .replace(/[^a-z0-9\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function readBlogContentEntries() {
  const src = readFileSync(BLOG_CONTENT_PATH, "utf8");
  const cutIdx = src.indexOf("BLOG_INDEX_COPY");
  const body = src.slice(0, cutIdx);

  const slugRe = /^ {4}"([a-z0-9-]+)":\s*\{/gm;
  const matches = [...body.matchAll(slugRe)];
  const entries = [];

  for (let i = 0; i < matches.length; i++) {
    const slug = matches[i][1];
    const start = matches[i].index;
    const end = i + 1 < matches.length ? matches[i + 1].index : body.length;
    const block = body.slice(start, end);

    const titleMatch = block.match(/['"]title['"]:\s*\(?\s*"([^"]*)"|['"]title['"]:\s*\(?\s*'([^']*)'/);
    const dateMatch = block.match(/['"]date['"]:\s*['"](\d{4}-\d{2}-\d{2})['"]/);
    const categoryMatch = block.match(/['"]category['"]:\s*['"]([a-z0-9-]+)['"]/);
    const tagMatch = block.match(/['"]tag['"]:\s*['"]([^'"]*)['"]/);

    entries.push({
      slug,
      title: titleMatch ? (titleMatch[1] ?? titleMatch[2] ?? "") : "",
      date: dateMatch ? dateMatch[1] : "",
      category: categoryMatch ? categoryMatch[1] : "",
      tag: tagMatch ? tagMatch[1] : "",
    });
  }
  return entries;
}

function loadAudit() {
  const raw = readFileSync(AUDIT_JSON_PATH, "utf8").replace(/^﻿/, "");
  return JSON.parse(raw);
}

function csvEscape(value) {
  const s = String(value ?? "");
  if (s.includes(",") || s.includes('"') || s.includes("\n")) {
    return `"${s.replace(/"/g, '""')}"`;
  }
  return s;
}

function main() {
  const blogEntries = readBlogContentEntries();
  const audit = loadAudit();
  const auditByNormTitle = new Map();
  for (const row of audit) {
    const norm = normalizeTitle(row.titulo);
    // Titulos em escrita nao-latina (russo, chines, etc.) ficam vazios ou
    // quase vazios apos a normalizacao ([a-z0-9] so) -- casar por essa
    // chave gera falso positivo (2 titulos diferentes colidindo no mesmo
    // "" ou string curta). So indexa se sobrou conteudo latino real.
    if (norm.length >= 8) auditByNormTitle.set(norm, row);
  }

  // Deteccao de duplicidade: agrupa por (idioma inferido do slug/tag +
  // 3 primeiras palavras significativas do titulo normalizado). Heuristica
  // conservadora -- serve para SINALIZAR candidatos, nao para decidir
  // sozinha (missao secao 6: nunca DELETE automatico).
  const STOPWORDS = new Set(["a", "o", "as", "os", "de", "da", "do", "em", "e", "que", "para", "com", "the", "how", "to", "of", "for", "and"]);
  function topicKey(entry) {
    const norm = normalizeTitle(entry.title);
    // Escrita nao-latina normaliza pra quase nada -- usa o slug como
    // chave unica pra nao colidir por acidente com outro titulo curto.
    if (norm.length < 8) return `__unique__${entry.slug}`;
    const words = norm.split(" ").filter((w) => w && !STOPWORDS.has(w));
    return words.slice(0, 3).join(" ");
  }
  const groups = new Map();
  for (const entry of blogEntries) {
    const key = topicKey(entry);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(entry);
  }

  const rows = [];
  let dateConflicts = 0;
  let missingDates = 0;
  let duplicateCandidates = 0;

  for (const entry of blogEntries) {
    const entryNorm = normalizeTitle(entry.title);
    const auditMatch = entryNorm.length >= 8 ? auditByNormTitle.get(entryNorm) : undefined;
    const hasCategory = Boolean(entry.category);
    const currentUrl = hasCategory ? `/blog/${entry.category}/${entry.slug}` : `/blog/${entry.slug}`;
    // Canonical = a mesma URL (P0: preservar). Se tem categoria, a URL
    // plana antiga (so /blog/<slug>) e um alias que precisa continuar
    // redirecionando 301 pra essa (confirmado por HTTP nesta sessao pra
    // varios exemplos, ex.: hebraico-moderno-x-hebraico-biblico).
    const newUrl = currentUrl;
    const redirectCode = hasCategory ? "301" : "";
    const redirectTarget = hasCategory ? currentUrl : "";

    let dateConflict = "NO";
    if (!entry.date) {
      missingDates++;
    }
    if (auditMatch) {
      if (auditMatch.realDate && entry.date && auditMatch.realDate !== entry.date) {
        dateConflict = "REVIEW REQUIRED";
        dateConflicts++;
      }
    }

    const group = groups.get(topicKey(entry));
    const isDuplicateCandidate = group && group.length > 1;
    if (isDuplicateCandidate && group[0] === entry) duplicateCandidates++; // conta 1x por grupo

    let action = "KEEP EXACT";
    let notes = [];
    if (dateConflict === "REVIEW REQUIRED") {
      action = "REVIEW";
      notes.push(`DATE_CONFLICT: blog_content.py=${entry.date} vs Publicados_Auditoria=${auditMatch.realDate} (nao alterado automaticamente)`);
    }
    if (isDuplicateCandidate) {
      action = action === "KEEP EXACT" ? "REVIEW" : action;
      notes.push(`DUPLICATE_CANDIDATE: mesmo topico de [${group.filter((g) => g !== entry).map((g) => g.slug).join(", ")}] -- decisao humana necessaria (KEEP/MERGE+301/CANONICAL REVIEW)`);
    }
    if (auditMatch && auditMatch.acao === "REVISAR") {
      action = "REVIEW";
      notes.push("Marcado REVISAR na auditoria (Iorubá -- revisão do professor responsável antes de manter indexado).");
    }
    if (!auditMatch) {
      notes.push("Sem correspondência direta na auditoria de 94 (Publicados_Auditoria) -- não cruzado, confiar apenas no dado do código.");
    }
    if (!entry.date) {
      action = "REVIEW";
      notes.push("FAIL: sem publishedAt -- não migrar sem decisão humana (não inventar data).");
    }

    const frente = auditMatch ? auditMatch.frente : "";
    const cluster = CLUSTER_BY_FRENTE[frente] || (entry.tag ? entry.tag : "REVIEW: frente não identificada na auditoria");
    const pillar = PILLAR_BY_FRENTE[frente] || "REVIEW: pilar não identificado";
    const language = auditMatch ? auditMatch.idioma : "REVIEW: idioma não confirmado";

    rows.push({
      current_url: currentUrl,
      new_url: newUrl,
      status_current: "LIVE (ver nota de verificação em 24-blog-source-of-truth.md)",
      action,
      redirect_code: redirectCode,
      target_url: redirectTarget,
      current_title: entry.title,
      new_title: entry.title, // preservado -- nenhuma reescrita nesta fase
      canonical: currentUrl,
      cluster,
      pillar,
      language,
      published_at_original: entry.date,
      published_at_audit: auditMatch ? auditMatch.realDate : "",
      date_conflict: dateConflict,
      index_status: "index (não verificado individualmente por robots/sitemap nesta sessão)",
      notes: notes.join(" | "),
    });
  }

  const headers = [
    "current_url", "new_url", "status_current", "action", "redirect_code", "target_url",
    "current_title", "new_title", "canonical", "cluster", "pillar", "language",
    "published_at_original", "published_at_audit", "date_conflict", "index_status", "notes",
  ];
  const csvLines = [headers.join(",")];
  for (const row of rows) {
    csvLines.push(headers.map((h) => csvEscape(row[h])).join(","));
  }
  writeFileSync(OUT_CSV_PATH, csvLines.join("\n") + "\n", "utf8");

  console.log(JSON.stringify({
    totalArticlesInCode: blogEntries.length,
    totalAuditRows: audit.length,
    matchedAgainstAudit: blogEntries.filter((e) => auditByNormTitle.has(normalizeTitle(e.title))).length,
    dateConflicts,
    missingDates,
    duplicateTopicGroups: duplicateCandidates,
    outputCsv: OUT_CSV_PATH,
  }, null, 2));
}

main();
