"""Importador idempotente de conteúdo para o Frappe Wiki da Vedium.

Uso no servidor:

    bench --site app.vediums.com execute \
      vedium_core.wiki_import.import_manifest \
      --kwargs '{"manifest_path":"apps/vedium/vedium_core/vedium_core/wiki_content/manifest.json","dry_run":true}'

Depois de revisar a saída, execute novamente com ``dry_run=false``.

O importador tenta se adaptar a pequenas diferenças de versão do app Wiki,
inspecionando os campos dos DocTypes antes de gravar. Nenhum documento é
apagado. Registros existentes são atualizados somente quando encontrados por
rota/título e pertencem ao mesmo espaço.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import frappe
from frappe.utils import cint


SPACE_DOCTYPE_CANDIDATES = ("Wiki Space", "WikiSpace")
PAGE_DOCTYPE_CANDIDATES = ("Wiki Page", "WikiPage")


def _resolve_doctype(candidates: tuple[str, ...]) -> str:
    for name in candidates:
        if frappe.db.exists("DocType", name):
            return name
    raise frappe.ValidationError(
        f"Nenhum DocType compatível encontrado. Tentativas: {', '.join(candidates)}"
    )


def _fieldnames(doctype: str) -> set[str]:
    return {df.fieldname for df in frappe.get_meta(doctype).fields}


def _first_field(fields: set[str], *candidates: str) -> str | None:
    return next((name for name in candidates if name in fields), None)


def _load_manifest(manifest_path: str) -> dict[str, Any]:
    path = Path(manifest_path)
    if not path.is_absolute():
        path = Path(frappe.get_app_path("vedium_core")) / path
    if not path.exists():
        raise FileNotFoundError(f"Manifesto não encontrado: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _find_existing(doctype: str, filters_list: list[dict[str, Any]]) -> str | None:
    for filters in filters_list:
        filters = {k: v for k, v in filters.items() if k and v not in (None, "")}
        if not filters:
            continue
        name = frappe.db.get_value(doctype, filters, "name")
        if name:
            return name
    return None


def _upsert_space(space: dict[str, Any], dry_run: bool) -> tuple[str | None, str]:
    doctype = _resolve_doctype(SPACE_DOCTYPE_CANDIDATES)
    fields = _fieldnames(doctype)

    title_field = _first_field(fields, "title", "space_name", "name1")
    route_field = _first_field(fields, "route", "slug")
    published_field = _first_field(fields, "published", "is_published")

    title = space["title"].strip()
    route = space["route"].strip()

    filters = []
    if route_field:
        filters.append({route_field: route})
    if title_field:
        filters.append({title_field: title})

    existing = _find_existing(doctype, filters)
    action = "update" if existing else "create"

    if dry_run:
        return existing, f"{action} space: {title} ({route})"

    doc = frappe.get_doc(doctype, existing) if existing else frappe.new_doc(doctype)
    if title_field:
        doc.set(title_field, title)
    if route_field:
        doc.set(route_field, route)
    if published_field:
        doc.set(published_field, cint(space.get("published", 1)))

    doc.flags.ignore_permissions = True
    doc.save()
    return doc.name, f"{action} space: {title} ({route})"


def _upsert_page(
    page: dict[str, Any],
    space_name: str | None,
    space_route: str,
    dry_run: bool,
) -> str:
    doctype = _resolve_doctype(PAGE_DOCTYPE_CANDIDATES)
    fields = _fieldnames(doctype)

    title_field = _first_field(fields, "title", "page_title")
    route_field = _first_field(fields, "route", "slug")
    content_field = _first_field(fields, "content", "markdown", "content_md")
    space_field = _first_field(fields, "wiki_space", "space", "parent_space")
    published_field = _first_field(fields, "published", "is_published")
    order_field = _first_field(fields, "idx", "sort_order", "position")

    title = page["title"].strip()
    route = page["route"].strip()
    content = page.get("content", "").rstrip() + "\n"

    filters = []
    if route_field:
        filters.append({route_field: route})
    if title_field and space_field and space_name:
        filters.append({title_field: title, space_field: space_name})
    if title_field:
        filters.append({title_field: title})

    existing = _find_existing(doctype, filters)
    action = "update" if existing else "create"

    if dry_run:
        return f"{action} page: {space_route}/{route} — {title}"

    doc = frappe.get_doc(doctype, existing) if existing else frappe.new_doc(doctype)
    if title_field:
        doc.set(title_field, title)
    if route_field:
        doc.set(route_field, route)
    if content_field:
        doc.set(content_field, content)
    if space_field and space_name:
        doc.set(space_field, space_name)
    if published_field:
        doc.set(published_field, cint(page.get("published", 1)))
    if order_field and page.get("order") is not None:
        doc.set(order_field, cint(page["order"]))

    doc.flags.ignore_permissions = True
    doc.save()
    return f"{action} page: {space_route}/{route} — {title}"


@frappe.whitelist()
def import_manifest(manifest_path: str = "wiki_content/manifest.json", dry_run: bool = True):
    """Cria ou atualiza espaços e páginas descritos em um manifesto JSON.

    Por segurança, ``dry_run`` é verdadeiro por padrão.
    """

    manifest = _load_manifest(manifest_path)
    logs: list[str] = []

    for space in manifest.get("spaces", []):
        space_name, message = _upsert_space(space, bool(dry_run))
        logs.append(message)

        for page in space.get("pages", []):
            logs.append(
                _upsert_page(
                    page=page,
                    space_name=space_name,
                    space_route=space["route"],
                    dry_run=bool(dry_run),
                )
            )

    if not dry_run:
        frappe.db.commit()

    result = {
        "dry_run": bool(dry_run),
        "operations": len(logs),
        "logs": logs,
    }
    frappe.logger("vedium_wiki_import").info(result)
    return result
