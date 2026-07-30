"""Construção pura do payload de contatos enviado ao Brevo."""


def normalize_list_ids(value):
    """Normaliza BREVO_LIST_IDS para uma lista de IDs inteiros únicos."""
    if value in (None, "", (), []):
        return []
    if isinstance(value, str):
        values = [item.strip() for item in value.split(",") if item.strip()]
    elif isinstance(value, (list, tuple, set)):
        values = value
    else:
        values = [value]

    list_ids = []
    for item in values:
        if isinstance(item, bool):
            raise ValueError("BREVO_LIST_IDS deve conter somente IDs inteiros")
        try:
            list_id = int(item)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "BREVO_LIST_IDS deve conter somente IDs inteiros"
            ) from exc
        if list_id <= 0:
            raise ValueError("BREVO_LIST_IDS deve conter somente IDs positivos")
        if list_id not in list_ids:
            list_ids.append(list_id)
    return list_ids


def build_contact_payload(
    email,
    *,
    first_name=None,
    last_name=None,
    course=None,
    list_ids=None,
):
    """Monta o contrato canônico Frappe → Brevo para um contato."""
    email = (email or "").strip()
    if not email:
        raise ValueError("email é obrigatório para sincronizar com o Brevo")

    attributes = {}
    if first_name and first_name.strip():
        attributes["FIRSTNAME"] = first_name.strip()
    if last_name and last_name.strip():
        attributes["LASTNAME"] = last_name.strip()
    if course and course.strip():
        attributes["COURSE"] = course.strip()

    payload = {
        "email": email,
        "attributes": attributes,
        "updateEnabled": True,
    }
    normalized_list_ids = normalize_list_ids(list_ids)
    if normalized_list_ids:
        payload["listIds"] = normalized_list_ids
    return payload
