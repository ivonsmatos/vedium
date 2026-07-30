"""Testes puros do contrato Frappe → Brevo."""

from pathlib import Path

from vedium_core.brevo_payload import (
    build_contact_payload,
    normalize_list_ids,
)

CORE = Path(__file__).resolve().parents[1]
INTEGRATIONS = (CORE / "integrations.py").read_text(encoding="utf-8")
PUBLIC_FUNNEL = (CORE / "public_funnel.py").read_text(encoding="utf-8")


def test_contact_payload_uses_canonical_course_attribute():
    payload = build_contact_payload(
        " aluno@example.com ",
        first_name=" Ana ",
        last_name=" Silva ",
        course=" Inglês B1 ",
        list_ids="12, 34,12",
    )

    assert payload == {
        "email": "aluno@example.com",
        "attributes": {
            "FIRSTNAME": "Ana",
            "LASTNAME": "Silva",
            "COURSE": "Inglês B1",
        },
        "updateEnabled": True,
        "listIds": [12, 34],
    }
    assert "COURSE_INTEREST" not in payload["attributes"]


def test_contact_payload_omits_blank_optional_attributes_and_lists():
    payload = build_contact_payload(
        "aluno@example.com",
        first_name="",
        course=None,
    )

    assert payload == {
        "email": "aluno@example.com",
        "attributes": {},
        "updateEnabled": True,
    }


def test_list_ids_must_be_positive_integers():
    assert normalize_list_ids([7, "8", 7]) == [7, 8]

    for invalid in (0, -1, "abc", True):
        try:
            normalize_list_ids(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(f"valor inválido aceito: {invalid!r}")


def test_enrollment_and_public_interest_sync_to_brevo():
    assert "sync_contact_to_brevo(" in INTEGRATIONS
    assert 'course=course_title' in INTEGRATIONS
    assert '"vedium_core.brevo.sync_contact_to_brevo"' in PUBLIC_FUNNEL
    assert "course=course or None" in PUBLIC_FUNNEL
