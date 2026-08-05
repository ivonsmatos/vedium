"""Idempotent Stripe to Frappe catalog synchronizer.

The synchronizer never creates customers, subscriptions, Checkout Sessions or
charges. It only creates/reuses recurring Prices and persists their verified
mapping in ``Vedium Course Price``.
"""

from __future__ import annotations

import hashlib
import os
from typing import Any

import frappe
from frappe import _
from frappe.custom.doctype.custom_field.custom_field import create_custom_field
from frappe.utils import now_datetime


EXPECTED_FREQUENCIES = {1, 2, 3, 4, 5}


def _value(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    getter = getattr(obj, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(obj, key, default)


def ensure_custom_contract_currency_field() -> None:
    """Create the enrollment currency field without committing the caller transaction."""
    if frappe.db.exists("Custom Field", "LMS Enrollment-custom_contract_currency"):
        return
    create_custom_field(
        "LMS Enrollment",
        {
            "fieldname": "custom_contract_currency",
            "label": "Moeda contratada",
            "fieldtype": "Data",
            "insert_after": "custom_contract_monthly_amount",
            "read_only": 1,
            "default": "BRL",
        },
    )


def build_expected_metadata(config: dict, period: str, price_def: dict) -> dict[str, str]:
    metadata = {
        "vedium_course_id": str(config["course_name"]),
        "classes_per_week": str(price_def["classes_per_week"]),
        "frequency_discount_percent": str(price_def["frequency_discount_percent"]),
        "interval": period,
        "minimum_term_months": "12" if period == "annual" else "0",
        "catalog_version": str(config["catalog_version"]),
        "system": "frappe",
    }
    if period == "annual":
        metadata["charge_count"] = "12"
    if config.get("pricing_basis"):
        metadata["pricing_basis"] = str(config["pricing_basis"])
    if config.get("unit_lesson_amount") is not None:
        metadata["unit_lesson_amount"] = str(config["unit_lesson_amount"])
    if config.get("annual_discount_months") is not None and period == "annual":
        metadata["annual_discount_months"] = str(config["annual_discount_months"])
    if price_def.get("classes_per_month") is not None:
        metadata["classes_per_month"] = str(price_def["classes_per_month"])
    return metadata


def validate_price_snapshot(
    price: Any,
    *,
    product_id: str,
    currency: str,
    unit_amount: int,
    lookup_key: str,
    expected_metadata: dict[str, str] | None = None,
) -> list[str]:
    """Validate a Stripe Price object without performing network or database I/O."""
    errors: list[str] = []
    recurring = _value(price, "recurring", {}) or {}

    checks = (
        (_value(price, "active") is True, "Price está inativo"),
        (_value(price, "livemode") is True, "Price não pertence ao ambiente live"),
        (_value(price, "product") == product_id, "Product ID divergente"),
        ((_value(price, "currency") or "").lower() == currency.lower(), "Moeda divergente"),
        (int(_value(price, "unit_amount", -1)) == int(unit_amount), "Valor divergente"),
        (_value(price, "lookup_key") == lookup_key, "Lookup key divergente"),
        (_value(price, "type") == "recurring", "Price não é recorrente"),
        (_value(price, "billing_scheme") == "per_unit", "Billing scheme divergente"),
        (_value(recurring, "interval") == "month", "Intervalo divergente"),
        (int(_value(recurring, "interval_count", 0)) == 1, "Interval count divergente"),
        (_value(recurring, "usage_type", "licensed") == "licensed", "Usage type divergente"),
    )
    for ok, message in checks:
        if not ok:
            errors.append(message)

    if expected_metadata is not None:
        current_metadata = dict(_value(price, "metadata", {}) or {})
        for key, expected in expected_metadata.items():
            if str(current_metadata.get(key, "")) != str(expected):
                errors.append(f"Metadata {key} divergente")
    return errors


def is_complete_catalog(rows: list[dict]) -> bool:
    """Return true only for ten validated rows covering 1..5 in both periods."""
    if len(rows) != 10:
        return False
    for period in ("monthly", "annual"):
        frequencies = {
            int(row["classes_per_week"])
            for row in rows
            if row.get("billing_period") == period and int(row.get("stripe_validated") or 0) == 1
        }
        if frequencies != EXPECTED_FREQUENCIES:
            return False
    return True


def _stripe_key() -> str:
    key = (frappe.conf.get("STRIPE_SECRET_KEY") or os.environ.get("STRIPE_SECRET_KEY") or "").strip()
    if not key:
        frappe.throw(_("STRIPE_SECRET_KEY não configurada."))
    if not key.startswith("sk_live_"):
        frappe.throw(_("A integração de produção exige uma chave Stripe sk_live_."))
    return key


def _resolve_lms_course(config: dict) -> str:
    preferred = config["course_name"]
    if frappe.db.exists("LMS Course", preferred):
        return preferred

    matches = frappe.get_all(
        "LMS Course",
        filters={"title": config["commercial_name"]},
        pluck="name",
        limit_page_length=3,
    )
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        frappe.throw(
            _("Mais de um LMS Course corresponde ao título {0}.").format(config["commercial_name"])
        )

    aliases = config.get("course_aliases") or []
    existing_aliases = [name for name in aliases if frappe.db.exists("LMS Course", name)]
    if len(existing_aliases) == 1:
        return existing_aliases[0]

    frappe.throw(
        _("LMS Course não encontrado para {0} ({1}).").format(
            config["commercial_name"], preferred
        )
    )


def _list_prices(stripe: Any, *, product_id: str, active: bool) -> list[Any]:
    prices: list[Any] = []
    starting_after = None
    while True:
        params: dict[str, Any] = {"product": product_id, "active": active, "limit": 100}
        if starting_after:
            params["starting_after"] = starting_after
        response = stripe.Price.list(**params)
        page = list(_value(response, "data", []) or [])
        prices.extend(page)
        if not _value(response, "has_more", False):
            return prices
        if not page:
            frappe.throw(_("Stripe retornou paginação inválida ao listar Prices."))
        starting_after = _value(page[-1], "id")


def _find_by_lookup_key(stripe: Any, lookup_key: str) -> tuple[list[Any], list[Any]]:
    active = list(_value(stripe.Price.list(lookup_keys=[lookup_key], active=True, limit=10), "data", []) or [])
    inactive = list(
        _value(stripe.Price.list(lookup_keys=[lookup_key], active=False, limit=10), "data", []) or []
    )
    return active, inactive


def _idempotency_key(config: dict, period: str, price_def: dict) -> str:
    payload = (
        f"live|{config['course_name']}|{period}|{price_def['classes_per_week']}|"
        f"{config['currency']}|{price_def['unit_amount']}|v{config['catalog_version']}"
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:32]
    return f"vedium-catalog-{digest}"


def _create_price(stripe: Any, config: dict, period: str, price_def: dict) -> Any:
    return stripe.Price.create(
        product=config["product_id"],
        currency=config["currency"].lower(),
        unit_amount=int(price_def["unit_amount"]),
        recurring={"interval": "month", "interval_count": 1, "usage_type": "licensed"},
        billing_scheme="per_unit",
        lookup_key=price_def["lookup_key"],
        transfer_lookup_key=False,
        nickname=price_def["nickname"],
        metadata=build_expected_metadata(config, period, price_def),
        idempotency_key=_idempotency_key(config, period, price_def),
    )


def _normalize_existing_price(stripe: Any, price: Any, config: dict, period: str, price_def: dict) -> Any:
    expected_metadata = build_expected_metadata(config, period, price_def)
    current_metadata = dict(_value(price, "metadata", {}) or {})
    merged_metadata = {**current_metadata, **expected_metadata}
    if current_metadata != merged_metadata or _value(price, "nickname") != price_def["nickname"]:
        stripe.Price.modify(
            _value(price, "id"),
            metadata=merged_metadata,
            nickname=price_def["nickname"],
        )
    return stripe.Price.retrieve(_value(price, "id"))


def _resolve_or_create_price(stripe: Any, config: dict, period: str, price_def: dict) -> tuple[Any, str]:
    lookup_key = price_def["lookup_key"]
    active_matches, inactive_matches = _find_by_lookup_key(stripe, lookup_key)
    if len(active_matches) > 1:
        frappe.throw(_("Lookup key duplicada no Stripe: {0}").format(lookup_key))
    if not active_matches and inactive_matches:
        ids = ", ".join(str(_value(price, "id")) for price in inactive_matches)
        frappe.throw(
            _("Lookup key {0} está ocupada por Price inativo: {1}").format(lookup_key, ids)
        )

    expected_metadata = build_expected_metadata(config, period, price_def)
    if active_matches:
        price = active_matches[0]
        errors = validate_price_snapshot(
            price,
            product_id=config["product_id"],
            currency=config["currency"],
            unit_amount=price_def["unit_amount"],
            lookup_key=lookup_key,
        )
        if errors:
            frappe.throw(_("Price {0} incompatível: {1}").format(lookup_key, "; ".join(errors)))
        price = _normalize_existing_price(stripe, price, config, period, price_def)
        action = "reused"
    else:
        price = _create_price(stripe, config, period, price_def)
        price = stripe.Price.retrieve(_value(price, "id"))
        action = "created"

    errors = validate_price_snapshot(
        price,
        product_id=config["product_id"],
        currency=config["currency"],
        unit_amount=price_def["unit_amount"],
        lookup_key=lookup_key,
        expected_metadata=expected_metadata,
    )
    if errors:
        frappe.throw(_("Validação final do Price {0} falhou: {1}").format(lookup_key, "; ".join(errors)))
    return price, action


def _upsert_catalog_row(
    *,
    config: dict,
    actual_course_name: str,
    period: str,
    price_def: dict,
    stripe_price: Any,
) -> str:
    frequency = int(price_def["classes_per_week"])
    version = int(config["catalog_version"])
    catalog_key = f"{actual_course_name}:{period}:{frequency}x:live:v{version}"
    name = frappe.db.exists("Vedium Course Price", {"catalog_key": catalog_key})
    doc = frappe.get_doc("Vedium Course Price", name) if name else frappe.new_doc("Vedium Course Price")

    doc.course = actual_course_name
    doc.commercial_name = config["commercial_name"]
    doc.catalog_key = catalog_key
    doc.catalog_version = version
    doc.enabled = 0
    doc.billing_period = period
    doc.classes_per_week = frequency
    doc.currency = config["currency"].upper()
    doc.minimum_term_months = 12 if period == "annual" else 0
    doc.charge_count = 12 if period == "annual" else 0
    doc.amount = float(price_def["amount"])
    doc.unit_amount = float(price_def["amount"])
    doc.subtotal = float(price_def["subtotal"])
    doc.frequency_discount_percent = float(price_def["frequency_discount_percent"])
    doc.stripe_environment = "live"
    doc.stripe_product_id = config["product_id"]
    doc.stripe_price_id = _value(stripe_price, "id")
    doc.stripe_lookup_key = price_def["lookup_key"]
    doc.stripe_validated = 1
    doc.last_stripe_validation = now_datetime()
    doc.notes = "Catálogo canônico sincronizado e validado pela API Stripe."
    doc.save(ignore_permissions=True)
    return doc.name


def _activate_complete_catalog(actual_course_name: str, catalog_version: int) -> list[str]:
    filters = {
        "course": actual_course_name,
        "catalog_version": catalog_version,
        "stripe_environment": "live",
    }
    rows = frappe.get_all(
        "Vedium Course Price",
        filters=filters,
        fields=["name", "billing_period", "classes_per_week", "stripe_validated"],
        limit_page_length=50,
    )
    frappe.db.set_value("Vedium Course Price", filters, "enabled", 0, update_modified=False)
    if not is_complete_catalog(rows):
        frappe.throw(
            _("Catálogo incompleto para {0}; nenhuma opção foi ativada.").format(actual_course_name)
        )

    activated: list[str] = []
    for row in rows:
        doc = frappe.get_doc("Vedium Course Price", row["name"])
        doc.enabled = 1
        doc.save(ignore_permissions=True)
        activated.append(doc.name)
    return activated


def _validate_config(config: dict) -> None:
    required = {
        "course_name",
        "commercial_name",
        "product_id",
        "currency",
        "catalog_version",
        "monthly_prices",
        "annual_prices",
    }
    missing = sorted(required.difference(config))
    if missing:
        frappe.throw(_("Configuração de catálogo incompleta: {0}").format(", ".join(missing)))
    if config["currency"].lower() not in {"brl", "usd"}:
        frappe.throw(_("Moeda de catálogo inválida."))
    for period in ("monthly", "annual"):
        rows = config[f"{period}_prices"]
        frequencies = {int(row["classes_per_week"]) for row in rows}
        if len(rows) != 5 or frequencies != EXPECTED_FREQUENCIES:
            frappe.throw(_("{0}: o período {1} deve conter frequências 1 a 5.").format(config["course_name"], period))


def sync_course_catalog(config: dict[str, Any], execute_apply: bool = False) -> dict[str, Any]:
    """Audit or apply one complete course catalog.

    ``execute_apply=False`` is read-only. ``True`` may create Stripe Prices and
    upsert Frappe mappings, but never creates a charge or subscription.
    """
    _validate_config(config)

    import stripe

    stripe.api_key = _stripe_key()
    account = stripe.Account.retrieve()
    product = stripe.Product.retrieve(config["product_id"])
    if _value(product, "active") is not True:
        frappe.throw(_("Stripe Product está inativo: {0}").format(config["product_id"]))
    if _value(product, "livemode") is not True:
        frappe.throw(_("Stripe Product não pertence ao ambiente live."))
    if _value(product, "type") != "service":
        frappe.throw(_("Stripe Product deve ser do tipo service."))

    actual_course_name = _resolve_lms_course(config)
    active_product_prices = _list_prices(stripe, product_id=config["product_id"], active=True)
    inactive_product_prices = _list_prices(stripe, product_id=config["product_id"], active=False)

    report: dict[str, Any] = {
        "course": actual_course_name,
        "commercial_name": config["commercial_name"],
        "product_id": config["product_id"],
        "account_id": _value(account, "id"),
        "mode": "apply" if execute_apply else "audit",
        "active_product_prices": len(active_product_prices),
        "inactive_product_prices": len(inactive_product_prices),
        "legacy_price_ids": list(config.get("legacy_price_ids") or []),
        "prices": [],
    }

    for period in ("monthly", "annual"):
        for price_def in config[f"{period}_prices"]:
            active_matches, inactive_matches = _find_by_lookup_key(stripe, price_def["lookup_key"])
            row = {
                "period": period,
                "classes_per_week": price_def["classes_per_week"],
                "lookup_key": price_def["lookup_key"],
                "unit_amount": price_def["unit_amount"],
                "active_matches": [_value(price, "id") for price in active_matches],
                "inactive_matches": [_value(price, "id") for price in inactive_matches],
            }
            if active_matches:
                row["planned_action"] = "reuse"
                row["validation_errors"] = validate_price_snapshot(
                    active_matches[0],
                    product_id=config["product_id"],
                    currency=config["currency"],
                    unit_amount=price_def["unit_amount"],
                    lookup_key=price_def["lookup_key"],
                )
            elif inactive_matches:
                row["planned_action"] = "blocked_inactive_lookup"
                row["validation_errors"] = ["Lookup key ocupada por Price inativo"]
            else:
                row["planned_action"] = "create"
                row["validation_errors"] = []
            report["prices"].append(row)

    blocking = [row for row in report["prices"] if row["validation_errors"]]
    if blocking:
        details = "; ".join(
            f"{row['lookup_key']}: {', '.join(row['validation_errors'])}" for row in blocking
        )
        frappe.throw(_("Auditoria bloqueou o catálogo: {0}").format(details))

    if not execute_apply:
        return report

    ensure_custom_contract_currency_field()
    try:
        for row in report["prices"]:
            period = row["period"]
            price_def = next(
                definition
                for definition in config[f"{period}_prices"]
                if definition["lookup_key"] == row["lookup_key"]
            )
            stripe_price, action = _resolve_or_create_price(stripe, config, period, price_def)
            row["action"] = action
            row["stripe_price_id"] = _value(stripe_price, "id")
            _upsert_catalog_row(
                config=config,
                actual_course_name=actual_course_name,
                period=period,
                price_def=price_def,
                stripe_price=stripe_price,
            )

        report["activated_records"] = _activate_complete_catalog(
            actual_course_name, int(config["catalog_version"])
        )
        frappe.db.commit()
    except Exception:
        frappe.db.rollback()
        raise

    report["status"] = "active"
    return report
