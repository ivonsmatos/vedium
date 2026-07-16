# -*- coding: utf-8 -*-
"""SUPERSEDIDO em 2026-07-16 por update_course_seo_texts.py, que grava os
mesmos 6 títulos -- achado de revisão de tom de voz: travessão em título
não lê natural em PT, então o separador "[CEFR]: [Nível]" abaixo usa
dois-pontos, não travessão. NÃO rodar este script depois daquele, ou o
travessão volta. Mantido só como registro histórico; COURSE_TITLES abaixo
já foi atualizado pra não reintroduzir o problema se alguém rodar por
engano.

Renomeia o título (LMS Course.title) dos 6 cursos de Inglês, tirando os
termos em inglês soltos no meio do nome ("Inglês - Beginner", "Inglês -
Upper Intermediário" etc.) e adotando o padrão comercial: "[Idioma] Online
ao Vivo [CEFR]: [Nível em português]".

Motivação (achado real do prompt-mestre de SEO/GEO, 2026-07): nomes de
curso em português com palavra em inglês solta ("Beginner", "Elementary",
"Upper Intermediário") soam amadores pra um site em PT-BR e atrapalham
busca/CTR. O código CEFR (A1, A2, B1, B1+, B2, C1) já aparece explícito no
novo título, o que também simplifica a extração de nível em courses.py e
www/*/index.py (ver commit que acompanha este oneshot).

Registros afetados (name = identificador interno, não muda; só o title):
    - ingl-s-beginner              "Inglês - Beginner"              -> A1
    - ingl-s-elementary            "Inglês - Elementary"            -> A2
    - ingl-s-pr-intermedi-rio      "Inglês - Pré-Intermediário"     -> B1
    - ingl-s-intermedi-rio         "Inglês - Intermediário"         -> B1+
    - ingl-s-upper-intermedi-rio   "Inglês - Upper Intermediário"   -> B2
    - ingl-s-avan-ado              "Inglês - Avançado"              -> C1

O slug público (/curso/ingles-basico-a1 etc, ver course_urls.py) já usa a
nomenclatura nova e não muda. Certificados futuros passam a imprimir o
título novo; certificados já emitidos não são retroativamente alterados
(o PDF já gerado não é re-renderizado por este script).

Rodar (idempotente — reaplica o valor, sem duplicar nada):
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.rename_english_course_titles.run

Nota: como usa frappe.db.set_value diretamente (sem doc.save()), os
doc_events de LMS Course não disparam — o cache de /catalogo e das
landings (courses.py, CACHE_TTL=300s) só reflete o novo título depois que
o TTL de 5 minutos expira sozinho.
"""

import frappe

COURSE_TITLES = {
    "ingl-s-beginner": "Inglês Online ao Vivo A1: Iniciante",
    "ingl-s-elementary": "Inglês Online ao Vivo A2: Básico",
    "ingl-s-pr-intermedi-rio": "Inglês Online ao Vivo B1: Pré-Intermediário",
    "ingl-s-intermedi-rio": "Inglês Online ao Vivo B1+: Intermediário",
    "ingl-s-upper-intermedi-rio": "Inglês Online ao Vivo B2: Intermediário Avançado",
    "ingl-s-avan-ado": "Inglês Online ao Vivo C1: Avançado",
}


def run():
    for course, title in COURSE_TITLES.items():
        if not frappe.db.exists("LMS Course", course):
            print(f"  AVISO: curso '{course}' não existe, pulando.")
            continue
        frappe.db.set_value("LMS Course", course, "title", title)
        print(f"  ✓ '{course}' → título: {title}")

    frappe.db.commit()
    print("\n✓ Títulos dos cursos de Inglês atualizados.")
