#!/usr/bin/env python3
"""Build the canonical Data Analytics artifact for the blog duplicate audit."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "audits" / "blog-duplicates-20260725"
OUTPUT = AUDIT / "artifact.json"
GENERATED_AT = "2026-07-25T20:48:44.692412+00:00"


def read_csv(name: str) -> list[dict]:
    with (AUDIT / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def source(
    source_id: str, label: str, path: str, description: str, sql: str
) -> dict:
    return {
        "id": source_id,
        "label": label,
        "path": path,
        "query": {
            "description": description,
            "engine": "duckdb",
            "language": "sql",
            "executed_at": GENERATED_AT,
            "sql": sql,
            "tables_used": [path],
            "filters": [
                "Leitura somente; nenhuma alteração no banco ou no site",
            ],
        },
    }


def main() -> int:
    summary = json.loads((AUDIT / "summary.json").read_text(encoding="utf-8"))
    counts = summary["counts"]
    checks = read_csv("duplicate_url_checks.csv")
    redirects = [
        row
        for row in read_csv("redirect_dry_run.csv")
        if row["action"] == "planned_301_to_catalog_canonical"
    ]
    anomalies = read_csv("title_anomalies.csv")
    cannibalization = read_csv("cannibalization_review.csv")

    checks_by_group: dict[str, list[dict]] = defaultdict(list)
    for row in checks:
        for group_id in row["group_ids"].split("|"):
            checks_by_group[group_id].append(row)
    groups_with_different_hashes = sum(
        len({row["rendered_content_hash"] for row in rows}) > 1
        for rows in checks_by_group.values()
    )
    canonical_mismatches = sum(
        row["canonical_matches_catalog"] == "no" for row in checks
    )

    sources = [
        source(
            "audit-summary",
            "Resumo reproduzível da auditoria",
            "docs/audits/blog-duplicates-20260725/summary.json",
            "Contagens consolidadas do catálogo versionado, listagem e sitemap ao vivo.",
            "SELECT counts.* FROM read_json_auto('docs/audits/blog-duplicates-20260725/summary.json');",
        ),
        source(
            "live-url-checks",
            "Verificação HTTP e canonical das URLs duplicadas",
            "docs/audits/blog-duplicates-20260725/duplicate_url_checks.csv",
            "GET sem alteração de estado nas URLs encontradas na listagem ao vivo.",
            "SELECT * FROM read_csv_auto('docs/audits/blog-duplicates-20260725/duplicate_url_checks.csv', header = true);",
        ),
        source(
            "redirect-plan",
            "Plano de redirecionamento em dry run",
            "docs/audits/blog-duplicates-20260725/redirect_dry_run.csv",
            "Mapeamento provisório baseado na arquitetura do catálogo versionado; não aplicado.",
            "SELECT * FROM read_csv_auto('docs/audits/blog-duplicates-20260725/redirect_dry_run.csv', header = true) WHERE action = 'planned_301_to_catalog_canonical';",
        ),
        source(
            "catalog-audit",
            "Inventário e anomalias do catálogo versionado",
            "docs/audits/blog-duplicates-20260725/article_inventory.csv",
            "Inventário dos artigos definidos em vedium_core/vedium_core/blog_content.py.",
            "SELECT * FROM read_csv_auto('docs/audits/blog-duplicates-20260725/article_inventory.csv', header = true);",
        ),
        source(
            "human-review",
            "Grupos de canibalização para revisão humana",
            "docs/audits/blog-duplicates-20260725/cannibalization_review.csv",
            "Comparação dos quatro pares explicitamente protegidos contra consolidação automática.",
            "SELECT * FROM read_csv_auto('docs/audits/blog-duplicates-20260725/cannibalization_review.csv', header = true);",
        ),
    ]

    metrics = [
        {"metric": "Cards", "value": counts["live_cards"]},
        {"metric": "URLs únicas", "value": counts["live_unique_card_urls"]},
        {"metric": "Títulos únicos", "value": counts["live_unique_card_titles"]},
        {"metric": "Catálogo", "value": counts["versioned_articles"]},
    ]
    redirects_table = [
        {
            "grupo": row["group_id"],
            "tipo": "alias de rota",
            "acao": "301 (bloqueado)",
            "status": "bloqueado",
        }
        for row in redirects
    ]
    anomalies_table = [
        {
            "artigo": f"Anomalia {index}",
            "titulo_atual": row["title"],
            "problema": "metadado ou extensão importada",
        }
        for index, row in enumerate(anomalies, 1)
    ]
    review_table = [
        {
            "grupo": row["group"],
            "similaridade": float(row["shingle_jaccard"]),
            "recomendacao": (
                "manter até revisão"
                if row["recommendation"] == "keep_pending_human_review"
                else "comparar intenção e desempenho"
            ),
            "status": row["decision_status"],
        }
        for row in cannibalization
    ]

    manifest = {
        "version": 1,
        "surface": "report",
        "title": "Auditoria de duplicidade do blog Vedium",
        "description": "Dry run técnico, reproduzível e sem alterações destrutivas.",
        "generatedAt": GENERATED_AT,
        "sources": sources,
        "cards": [
            {
                "id": "cards-live",
                "description": "Total de cards coletados nas 11 páginas da listagem.",
                "dataset": "headline_cards",
                "sourceId": "audit-summary",
                "metrics": [{"label": "Cards ao vivo", "field": "value", "format": "number"}],
            },
            {
                "id": "duplicate-components",
                "description": "Componentes ligados por título normalizado ou URL idêntica.",
                "dataset": "headline_components",
                "sourceId": "audit-summary",
                "metrics": [{"label": "Grupos duplicados", "field": "value", "format": "number"}],
            },
            {
                "id": "redirects-blocked",
                "description": "Aliases candidatos a 301, ainda sem alteração de produção.",
                "dataset": "headline_redirects",
                "sourceId": "redirect-plan",
                "metrics": [{"label": "301 bloqueados", "field": "value", "format": "number"}],
            },
            {
                "id": "human-review-count",
                "description": "Pares protegidos contra consolidação automática.",
                "dataset": "headline_review",
                "sourceId": "human-review",
                "metrics": [{"label": "Revisões humanas", "field": "value", "format": "number"}],
            },
        ],
        "charts": [
            {
                "id": "listing-counts",
                "title": "Contagens da listagem e do catálogo do blog",
                "subtitle": "A diferença entre cards, URLs e títulos mostra duplicação visual e por rota.",
                "intent": "comparison",
                "question": "Quantos registros permanecem em cada nível de deduplicação?",
                "rationale": "Barras simples permitem comparar as contagens categóricas no mesmo eixo.",
                "comparisonContext": {
                    "grain": "contagem de registros",
                    "unit": "registros",
                    "denominator": "listagem ao vivo e catálogo versionado",
                },
                "type": "bar",
                "dataset": "listing_metrics",
                "sourceId": "audit-summary",
                "encodings": {
                    "x": {
                        "field": "metric",
                        "type": "nominal",
                        "aggregate": "none",
                        "label": "Métrica",
                    },
                    "y": {
                        "field": "value",
                        "type": "quantitative",
                        "aggregate": "none",
                        "format": "number",
                        "label": "Quantidade",
                    },
                },
                "xAxisTitle": "",
                "yAxisTitle": "Quantidade",
                "valueFormat": "number",
                "layout": "full",
            }
        ],
        "blocks": [
            {
                "id": "title",
                "type": "markdown",
                "body": "# Auditoria de duplicidade do blog Vedium\n\nDry run técnico para decisão antes de qualquer exclusão, alteração de banco ou redirecionamento.",
                "layout": "full",
            },
            {
                "id": "summary",
                "type": "markdown",
                "body": (
                    "## Resumo técnico\n\n"
                    f"A listagem ao vivo contém **{counts['live_cards']} cards**, "
                    f"**{counts['live_unique_card_urls']} URLs únicas** e "
                    f"**{counts['live_unique_card_titles']} títulos únicos**. "
                    f"Foram encontrados **{counts['duplicate_card_components']} componentes duplicados**, "
                    f"que representam **{counts['extra_duplicate_cards']} cards excedentes**. "
                    f"Os {len(checks)} endereços testados responderam 200; "
                    f"{canonical_mismatches} não usam a canonical prevista pelo catálogo."
                ),
                "layout": "full",
                "sourceId": "audit-summary",
            },
            {
                "id": "headline",
                "type": "metric-strip",
                "cardIds": [
                    "cards-live",
                    "duplicate-components",
                    "redirects-blocked",
                    "human-review-count",
                ],
                "layout": "full",
            },
            {
                "id": "visual-heading",
                "type": "markdown",
                "body": "## Evidência quantitativa\n\nA contagem progressiva separa repetição visual, aliases de URL e o catálogo controlado por código.",
                "layout": "full",
            },
            {
                "id": "visual",
                "type": "chart",
                "chartId": "listing-counts",
                "layout": "full",
            },
            {
                "id": "diagnosis",
                "type": "markdown",
                "body": (
                    "## Diagnóstico da causa\n\n"
                    "O site é uma aplicação Frappe. O controlador de artigo consulta apenas o `slug` e "
                    "não valida se idioma e categoria da rota correspondem ao artigo. Um teste com uma "
                    "categoria inexistente retornou 200 e o mesmo H1. Nos 31 grupos, nenhuma comparação "
                    f"entre URLs apresentou hash renderizado divergente ({groups_with_different_hashes} grupos divergentes). "
                    "A branch atual já prioriza registros versionados sobre cópias do banco na listagem, "
                    "mas essa proteção ainda não está refletida no site auditado."
                ),
                "layout": "full",
                "sourceId": "live-url-checks",
            },
            {
                "id": "methodology",
                "type": "markdown",
                "body": (
                    "## Escopo e método\n\n"
                    "Foram inventariados 97 artigos versionados; título, H1, idioma, categoria, URL e "
                    "conteúdo normalizado foram registrados. O corpo foi convertido em texto, normalizado "
                    "e resumido por SHA-256; proximidade foi medida por Jaccard de shingles de cinco palavras. "
                    "A listagem paginada, o sitemap e cada URL duplicada foram consultados em modo somente leitura."
                ),
                "layout": "full",
                "sourceId": "catalog-audit",
            },
            {
                "id": "redirect-heading",
                "type": "markdown",
                "body": (
                    "## Plano de 301 — dry run\n\n"
                    f"Há {len(redirects)} aliases candidatos a 301. Todos permanecem bloqueados até existir "
                    "backup restaurável do banco e revisão de Search Console/backlinks. Nenhum redirecionamento foi aplicado."
                ),
                "layout": "full",
                "sourceId": "redirect-plan",
            },
            {
                "id": "anomaly-heading",
                "type": "markdown",
                "body": (
                    "## Títulos a corrigir\n\n"
                    "Três títulos do catálogo contêm prefixo de importação ou extensão de arquivo: "
                    "um artigo em inglês com `Título SEO:` e dois artigos com sufixo `.md`. "
                    "Os valores completos e os slugs estão no CSV de anomalias."
                ),
                "layout": "full",
                "sourceId": "catalog-audit",
            },
            {
                "id": "review-heading",
                "type": "markdown",
                "body": (
                    "## Canibalização\n\n"
                    "Os grupos A, B, C e D permanecem como `REVISÃO HUMANA`; similaridade lexical "
                    "isolada não autoriza fusão. A matriz completa está no CSV de canibalização."
                ),
                "layout": "full",
                "sourceId": "human-review",
            },
            {
                "id": "limitations",
                "type": "markdown",
                "body": (
                    "## Limitações e bloqueios\n\n"
                    "O checkout não possui `bench`, configuração do site ou cliente MariaDB; o Docker local "
                    "também está sem daemon. Portanto, não foi possível gerar backup do banco, exportar IDs "
                    "internos nem confirmar registros não publicados. Google Search Console e dados de backlinks "
                    "também não estão disponíveis. Essas lacunas são materiais para escolher a URL de maior valor."
                ),
                "layout": "full",
            },
            {
                "id": "next",
                "type": "markdown",
                "body": (
                    "## Próximos passos recomendados\n\n"
                    "1. Gerar e testar um backup completo do banco e exportar a tabela de artigos.\n"
                    "2. Fornecer exportações de Search Console e backlinks por URL.\n"
                    "3. Aprovar a matriz de URL principal e os quatro pares de canibalização.\n"
                    "4. Implementar validação de rota e 301 direto, corrigir os três títulos e despublicar apenas cópias confirmadas.\n"
                    "5. Regerar sitemap/cache e executar os testes de URL, conteúdo, SEO, listagem e paginação."
                ),
                "layout": "full",
            },
        ],
    }
    snapshot = {
        "version": 1,
        "generatedAt": GENERATED_AT,
        "status": "partial",
        "datasets": {
            "headline_cards": [{"value": counts["live_cards"]}],
            "headline_components": [{"value": counts["duplicate_card_components"]}],
            "headline_redirects": [{"value": len(redirects)}],
            "headline_review": [
                {"value": counts["cannibalization_groups_for_human_review"]}
            ],
            "listing_metrics": metrics,
            "redirects": redirects_table,
            "anomalies": anomalies_table,
            "human_review": review_table,
        },
        "accessIssues": [
            {
                "id": "database-unavailable",
                "scope": "backup, IDs internos e registros de produção",
                "message": "Banco/bench indisponível neste checkout; alterações destrutivas estão bloqueadas.",
            },
            {
                "id": "search-console-unavailable",
                "scope": "escolha da URL principal",
                "message": "Cliques, impressões, posição e cobertura não puderam ser comparados.",
            },
            {
                "id": "backlinks-unavailable",
                "scope": "autoridade por URL",
                "message": "Backlinks não puderam ser usados na decisão de canonical.",
            },
        ],
    }
    artifact = {
        "surface": "report",
        "manifest": manifest,
        "snapshot": snapshot,
        "sources": sources,
    }
    OUTPUT.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
