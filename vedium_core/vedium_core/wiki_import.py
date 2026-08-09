"""Importador idempotente de conteúdo para o Frappe Wiki da Vedium.

Uso no servidor:

    bench --site app.vediums.com execute \\
      vedium_core.wiki_import.import_manifest \\
      --kwargs '{"manifest_path":"wiki_content/manifest.json","dry_run":true}'

Depois de revisar a saída, execute novamente com ``dry_run=false``.

Hierarquia suportada:
  Espaço (Wiki Space)
    └─ Grupo (Wiki Sidebar / Wiki Group)
         └─ Página (Wiki Page)

O importador:
- descobre DocTypes e campos em runtime via frappe.get_meta();
- localiza registros por rota e depois por título (nunca duplica);
- atualiza conteúdo somente quando diferente do existente;
- nunca apaga registros;
- faz rollback por espaço em caso de erro;
- retorna contadores: created, updated, skipped, errors.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import frappe
from frappe.utils import cint


# ---------------------------------------------------------------------------
# DocType candidates (adaptativo por versão do app Wiki)
# ---------------------------------------------------------------------------

SPACE_DOCTYPE_CANDIDATES = ("Wiki Space", "WikiSpace")
GROUP_DOCTYPE_CANDIDATES = ("Wiki Sidebar", "Wiki Group", "WikiSidebar", "WikiGroup")
PAGE_DOCTYPE_CANDIDATES = ("Wiki Document", "Wiki Page", "WikiPage")


# ---------------------------------------------------------------------------
# Helpers de schema
# ---------------------------------------------------------------------------

def _resolve_doctype(candidates: tuple[str, ...]) -> str | None:
    """Retorna o primeiro DocType da lista que existir, ou None."""
    for name in candidates:
        if frappe.db.exists("DocType", name):
            return name
    return None


def _require_doctype(candidates: tuple[str, ...]) -> str:
    found = _resolve_doctype(candidates)
    if not found:
        raise frappe.ValidationError(
            f"Nenhum DocType compatível encontrado. Tentativas: {', '.join(candidates)}"
        )
    return found


def _fieldnames(doctype: str) -> set[str]:
    return {df.fieldname for df in frappe.get_meta(doctype).fields}


def _first_field(fields: set[str], *candidates: str) -> str | None:
    return next((name for name in candidates if name in fields), None)


# ---------------------------------------------------------------------------
# Carregamento do manifesto
# ---------------------------------------------------------------------------

def _load_manifest(manifest_path: str) -> dict[str, Any]:
    # Sempre resolve DENTRO do app; rejeita path absoluto/traversal — senão um
    # caller poderia fazer json.loads de qualquer arquivo do servidor. QA 2026-08-09.
    base = Path(frappe.get_app_path("vedium_core")).resolve()
    path = (base / manifest_path).resolve()
    if not str(path).startswith(str(base)):
        frappe.throw("Caminho de manifesto inválido.", frappe.ValidationError)
    if not path.exists():
        raise FileNotFoundError(f"Manifesto não encontrado: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Pesquisa idempotente
# ---------------------------------------------------------------------------

def _find_existing(doctype: str, filters_list: list[dict[str, Any]]) -> str | None:
    for filters in filters_list:
        clean = {k: v for k, v in filters.items() if k and v not in (None, "")}
        if not clean:
            continue
        name = frappe.db.get_value(doctype, clean, "name")
        if name:
            return name
    return None


# ---------------------------------------------------------------------------
# Upsert: Espaço
# ---------------------------------------------------------------------------

def _upsert_space(
    space: dict[str, Any],
    dry_run: bool,
    counters: dict[str, int],
) -> tuple[str | None, str]:
    doctype = _require_doctype(SPACE_DOCTYPE_CANDIDATES)
    fields = _fieldnames(doctype)

    title_field = _first_field(fields, "title", "space_name", "name1")
    route_field = _first_field(fields, "route", "slug")
    published_field = _first_field(fields, "published", "is_published")

    title = space["title"].strip()
    route = space.get("route", "").strip()

    filters: list[dict] = []
    if route_field and route:
        filters.append({route_field: route})
    if title_field:
        filters.append({title_field: title})

    existing = _find_existing(doctype, filters)

    if space.get("existing") and not existing:
        counters["skipped"] += 1
        return None, f"SKIP (espaço existente não encontrado): {title}"

    action = "update" if existing else "create"

    if dry_run:
        counters["created" if not existing else "updated"] += 1
        return existing or f"dry:{route}", f"[DRY] {action} espaço: {title} ({route})"

    doc = frappe.get_doc(doctype, existing) if existing else frappe.new_doc(doctype)
    if title_field:
        doc.set(title_field, title)
    if route_field and route:
        doc.set(route_field, route)
    if published_field:
        doc.set(published_field, cint(space.get("published", 1)))

    doc.flags.ignore_permissions = True
    doc.save()
    counters["created" if not existing else "updated"] += 1
    return doc.name, f"{action} espaço: {title} ({route})"


# ---------------------------------------------------------------------------
# Upsert: Grupo
# ---------------------------------------------------------------------------

def _upsert_group(
    group: dict[str, Any], space_name: str | None, space_route: str, dry_run: bool, counters: dict
) -> tuple[str | None, str]:
    title = group["title"].strip()
    
    doctype = _resolve_doctype(GROUP_DOCTYPE_CANDIDATES)
    if not doctype or frappe.get_meta(doctype).istable:
        counters["skipped"] += 1
        return None, f"SKIP (Grupo é child table ou inexistente): {title}"

    fields = _fieldnames(doctype)
    title_field = _first_field(fields, "title", "group_title", "name1")
    space_field = _first_field(fields, "wiki_space", "space", "parent_space")
    order_field = _first_field(fields, "idx", "sort_order", "position", "sequence")

    filters: list[dict] = []
    if title_field and space_field and space_name:
        filters.append({title_field: title, space_field: space_name})
    if title_field:
        filters.append({title_field: title})

    existing = _find_existing(doctype, filters)
    action = "update" if existing else "create"

    if dry_run:
        counters["created" if not existing else "updated"] += 1
        return existing or f"dry:group:{title}", f"[DRY] {action} grupo: {space_route} / {title}"

    doc = frappe.get_doc(doctype, existing) if existing else frappe.new_doc(doctype)
    if title_field:
        doc.set(title_field, title)
    if space_field and space_name:
        doc.set(space_field, space_name)
    if order_field and group.get("order") is not None:
        doc.set(order_field, cint(group["order"]))

    doc.flags.ignore_permissions = True
    doc.save()
    counters["created" if not existing else "updated"] += 1
    return doc.name, f"{action} grupo: {space_route} / {title}"


# ---------------------------------------------------------------------------
# Upsert: Página
# ---------------------------------------------------------------------------

def _upsert_page(
    page: dict[str, Any],
    space_name: str | None,
    space_route: str,
    group_name: str | None,
    dry_run: bool,
    counters: dict[str, int],
) -> str:
    doctype = _require_doctype(PAGE_DOCTYPE_CANDIDATES)
    fields = _fieldnames(doctype)

    title_field = _first_field(fields, "title", "page_title")
    route_field = _first_field(fields, "route", "slug")
    content_field = _first_field(fields, "content", "markdown", "content_md")
    space_field = _first_field(fields, "wiki_space", "space", "parent_space")
    group_field = _first_field(fields, "sidebar", "wiki_sidebar", "group", "wiki_group")
    published_field = _first_field(fields, "published", "is_published")
    order_field = _first_field(fields, "idx", "sort_order", "position")

    title = page["title"].strip()
    route = page.get("route", "").strip()
    content = page.get("content", "").rstrip() + "\n"

    filters: list[dict] = []
    if route_field and route:
        filters.append({route_field: route})
    if title_field and space_field and space_name:
        filters.append({title_field: title, space_field: space_name})
    if title_field:
        filters.append({title_field: title})

    existing = _find_existing(doctype, filters)
    action = "update" if existing else "create"

    # Verifica se atualização é necessária
    if existing and content_field:
        current = frappe.db.get_value(doctype, existing, content_field) or ""
        if current.rstrip() == content.rstrip():
            counters["skipped"] += 1
            return f"SKIP (sem alteração): {space_route}/{route} — {title}"

    if dry_run:
        counters["created" if not existing else "updated"] += 1
        return f"[DRY] {action} página: {space_route}/{route} — {title}"

    doc = frappe.get_doc(doctype, existing) if existing else frappe.new_doc(doctype)
    if title_field:
        doc.set(title_field, title)
    if route_field and route:
        doc.set(route_field, route)
    if content_field:
        doc.set(content_field, content)
    if space_field and space_name:
        doc.set(space_field, space_name)
    if group_field and group_name:
        doc.set(group_field, group_name)
    if published_field:
        has_pending_confirmation = "[A CONFIRMAR]" in content
        should_publish = not has_pending_confirmation and cint(page.get("published", 1))
        doc.set(published_field, 1 if should_publish else 0)
    if order_field and page.get("order") is not None:
        doc.set(order_field, cint(page["order"]))

    doc.flags.ignore_permissions = True
    doc.save()
    counters["created" if not existing else "updated"] += 1
    return f"{action} página: {space_route}/{route} — {title}"


# ---------------------------------------------------------------------------
# Ponto de entrada público
# ---------------------------------------------------------------------------

@frappe.whitelist()
def import_manifest(
    manifest_path: str = "wiki_content/manifest.json",
    dry_run: bool = True,
) -> dict[str, Any]:
    """Cria ou atualiza espaços, grupos e páginas do manifesto JSON.

    Por segurança, ``dry_run`` é verdadeiro por padrão.
    """
    # Função de manutenção que escreve Wiki com ignore_permissions → SÓ gestão.
    # Sem isto, qualquer usuário logado alteraria/despublicaria a wiki. QA 2026-08-09.
    if not set(frappe.get_roles()) & {"System Manager", "Administrator"}:
        frappe.throw("Acesso restrito à equipe.", frappe.PermissionError)

    manifest = _load_manifest(manifest_path)
    logs: list[str] = []
    counters: dict[str, int] = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}
    space_errors: list[str] = []

    for space_def in manifest.get("spaces", []):
        space_name = None
        space_route = space_def.get("route", "")

        try:
            space_name, msg = _upsert_space(space_def, bool(dry_run), counters)
            logs.append(msg)

            # Processar grupos dentro do espaço
            for grp_idx, group_def in enumerate(space_def.get("groups", []), start=1):
                group_def.setdefault("order", grp_idx)
                group_name, gmsg = _upsert_group(
                    group_def, space_name, space_route, bool(dry_run), counters
                )
                logs.append(gmsg)

                for pg_idx, page_def in enumerate(group_def.get("pages", []), start=1):
                    page_def.setdefault("order", pg_idx)
                    logs.append(
                        _upsert_page(
                            page=page_def,
                            space_name=space_name,
                            space_route=space_route,
                            group_name=group_name,
                            dry_run=bool(dry_run),
                            counters=counters,
                        )
                    )

            # Páginas diretas no espaço (sem grupo)
            for pg_idx, page_def in enumerate(space_def.get("pages", []), start=1):
                page_def.setdefault("order", pg_idx)
                logs.append(
                    _upsert_page(
                        page=page_def,
                        space_name=space_name,
                        space_route=space_route,
                        group_name=None,
                        dry_run=bool(dry_run),
                        counters=counters,
                    )
                )

        except Exception as exc:
            if not dry_run:
                frappe.db.rollback()
            counters["errors"] += 1
            err = f"ERRO no espaço '{space_route}': {type(exc).__name__}: {exc}"
            logs.append(err)
            space_errors.append(err)
            frappe.log_error(err, "Vedium.wiki_import")

    if not dry_run and not space_errors:
        frappe.db.commit()

    result: dict[str, Any] = {
        "dry_run": bool(dry_run),
        "version": manifest.get("version", 1),
        "counters": counters,
        "total_operations": sum(counters.values()),
        "errors": space_errors,
        "logs": logs,
    }
    frappe.logger("vedium_wiki_import").info(result)
    return result
