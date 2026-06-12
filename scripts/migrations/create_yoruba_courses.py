"""
Script de cadastro do Professor e dos 3 cursos de Iorubá na plataforma Vedium (Frappe LMS).

Professor: Busayo Frank Alonge
  Email:    busayo@vediums.com
  Telefone: 11 97714-9640
  Idioma:   Iorubá

Cursos:
  1. Iorubá - Básico        — 3 módulos, 9 lições
  2. Iorubá - Intermediário — 3 módulos, 7 lições
  3. Iorubá - Avançado      — 3 módulos, 9 lições

Tabela de preços (Iorubá):
  1 aula/semana → R$ 320,00/mês
  2 aulas/semana → R$  600,00/mês
  3 aulas/semana → R$  900,00/mês
  4 aulas/semana → R$ 1.180,00/mês
  Hora-professor: R$ 30,00 | Duração: 1h | Níveis: Básico / Intermediário / Avançado

Referências:
  - Fakinlede, Kayode J. Beginner's Yoruba. Hippocrene Books, Inc., 2005.
  - Awobuluyi, Oladele. Essentials of Yoruba Grammar. Oxford University Press Nigeria, 1978.
  - Akintoye, Stephen Adebanji. A History of the Yoruba People. Amalion Publishing, 2014.

Uso dentro do container Frappe:
  bench --site vediums.com execute scripts.migrations.create_yoruba_courses.execute

Ou via bench console:
  bench --site vediums.com console
  >>> import create_yoruba_courses; create_yoruba_courses.execute()
"""

import frappe

# ─────────────────────────────────────────────────────────────────────────────
# DADOS DO PROFESSOR
# ─────────────────────────────────────────────────────────────────────────────
INSTRUCTOR_EMAIL = "busayo@vediums.com"
INSTRUCTOR_FIRST = "Busayo Frank"
INSTRUCTOR_LAST = "Alonge"
INSTRUCTOR_PHONE = "11977149640"
INSTRUCTOR_BIO = (
    "Professor nativo de Iorubá com profundo conhecimento da língua, cultura e "
    "filosofia iorubá. Especialista em ensino comunicativo e imersão cultural, "
    "conduz os alunos desde os fundamentos até a fluência acadêmica e a conexão "
    "com as raízes ancestrais africanas."
)


# ─────────────────────────────────────────────────────────────────────────────
# IMAGENS (Unsplash free — temática africana/educação)
# ─────────────────────────────────────────────────────────────────────────────
IMAGES = {
    # Jovem mulher negra sorrindo com livro — aprendizado inicial acolhedor
    "basico": "https://images.unsplash.com/photo-1529390079861-591de354faf5?w=1280&q=80",
    # Duas mulheres negras em conversa animada — troca cultural / nível médio
    "intermediario": "https://images.unsplash.com/photo-1573496799652-408c2ac9fe98?w=1280&q=80",
    # Mulher negra, sorriso confiante, contexto profissional/acadêmico
    "avancado": "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=1280&q=80",
}

# Preço exibido no card (menor barreira de entrada: 1 aula/semana)
COURSE_PRICE = 320.00


# ─────────────────────────────────────────────────────────────────────────────
# SUBCATEGORIAS IORUBÁ
# ─────────────────────────────────────────────────────────────────────────────
YORUBA_LEVELS = [
    {
        "title": "Iorubá - Básico",
        "parent_category": "Iorubá",
        "description": (
            "Nível Básico. Saudações, alfabeto, tons, pronomes, verbos essenciais, "
            "numerais e diálogos cotidianos. Base sólida para comunicação prática."
        ),
        "sort_order": 1,
    },
    {
        "title": "Iorubá - Intermediário",
        "parent_category": "Iorubá",
        "description": (
            "Nível Intermediário. Classes de palavras, verbos seriais, aspectos verbais, "
            "expressões idiomáticas, leitura e conversação avançada."
        ),
        "sort_order": 2,
    },
    {
        "title": "Iorubá - Avançado",
        "parent_category": "Iorubá",
        "description": (
            "Nível Avançado. Gramática complexa, literatura, discurso formal, "
            "tradução, história e filosofia iorubá. Fluência acadêmica e cultural."
        ),
        "sort_order": 3,
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# CURRÍCULO COMPLETO — 3 NÍVEIS
# ─────────────────────────────────────────────────────────────────────────────
YORUBA_CURRICULUM = [
    # ─── 1. BÁSICO ────────────────────────────────────────────────────────────
    {
        "title": "Iorubá - Básico",
        "category": "Iorubá - Básico",
        "level_code": "Básico",
        "image": IMAGES["basico"],
        "course_price": COURSE_PRICE,
        "short_description": (
            "Nível Básico | Saudações, alfabeto, tons, pronomes, numerais e "
            "diálogos cotidianos em 3 módulos e 9 lições progressivas."
        ),
        "long_description": (
            "<p>O curso <strong>Iorubá Básico</strong> apresenta os fundamentos da "
            "língua e cultura iorubá, capacitando o aluno a interagir em situações "
            "cotidianas e construir base sólida para o aprendizado contínuo.</p>"
            "<p>Baseado em <em>Beginner's Yoruba</em> de Kayode J. Fakinlede (2005), "
            "você vai dominar:</p>"
            "<ul>"
            "<li>Saudações, despedidas e expressões de cortesia</li>"
            "<li>Apresentações pessoais — nome e origem</li>"
            "<li>Alfabeto Iorubá e os 3 tons (alto, médio, baixo)</li>"
            "<li>Pronomes pessoais e verbos de alta frequência</li>"
            "<li>Frases afirmativas e negativas simples</li>"
            "<li>Numerais de 1 a 10 e expressões de quantidade</li>"
            "<li>Adjetivos comuns e descrição de pessoas/objetos</li>"
            "<li>Provérbios simples e aspectos culturais</li>"
            "</ul>"
            "<p><strong>Preço:</strong> a partir de R$ 320/mês (1 aula/semana). "
            "Planos de 1 a 4 aulas/semana disponíveis.</p>"
            "<p><strong>Certificado:</strong> incluso ao concluir todas as unidades.</p>"
        ),
        "units": [
            # ── Módulo 1 ──────────────────────────────────────────────────────
            {
                "title": "Módulo 1 – Introdução ao Iorubá",
                "topics": [
                    "Lição 1: Primeiros Contatos — Saudações e despedidas (Ẹ káàárọ̀, Ẹ káàsán, Ó dàbọ̀)",
                    "Lição 1: Apresentações pessoais — nome e origem",
                    "Lição 1: Expressões de cortesia (Ẹ jọ̀wọ́, Ẹ ṣeun)",
                    "Lição 2: Sons e Tons — O alfabeto Iorubá e pronúncia",
                    "Lição 2: Introdução aos tons (alto, médio, baixo) e marcações",
                    "Lição 2: Prática de pronúncia com diferentes tons",
                    "Lição 3: Nomes Iorubá e Cultura — Significado de nomes comuns",
                    "Lição 3: Breve introdução à geografia e ao povo Iorubá",
                ],
            },
            # ── Módulo 2 ──────────────────────────────────────────────────────
            {
                "title": "Módulo 2 – Construindo Frases Básicas",
                "topics": [
                    "Lição 4: Pronomes e Verbos Essenciais — Pronomes pessoais (èmi, ìwọ, òun)",
                    "Lição 4: Verbos de alta frequência (jẹ, lọ, wá)",
                    "Lição 4: Formação de frases afirmativas e negativas simples",
                    "Lição 5: Numerais e Quantidades — Contagem de 1 a 10 e além",
                    "Lição 5: Expressões de quantidade",
                    "Lição 5: Diálogos envolvendo compras e preços",
                    "Lição 6: Descrições e Adjetivos — Adjetivos comuns (ńlá, kékeré, dúdú)",
                    "Lição 6: Descrevendo pessoas e objetos",
                ],
            },
            # ── Módulo 3 ──────────────────────────────────────────────────────
            {
                "title": "Módulo 3 – Interação e Contexto",
                "topics": [
                    "Lição 7: Diálogos Cotidianos — Conversas sobre família e amigos",
                    "Lição 7: Perguntas e respostas simples",
                    "Lição 7: Expressões de tempo (dias da semana, partes do dia)",
                    "Lição 8: Cultura e Provérbios — Provérbios simples e seus significados",
                    "Lição 8: Canções e poesias Iorubá básicas",
                    "Lição 9: Revisão e Consolidação — Revisão de gramática e vocabulário",
                    "Lição 9: Simulações de conversação",
                    "Lição 9: Avaliação final do nível Básico",
                ],
            },
        ],
    },
    # ─── 2. INTERMEDIÁRIO ─────────────────────────────────────────────────────
    {
        "title": "Iorubá - Intermediário",
        "category": "Iorubá - Intermediário",
        "level_code": "Intermediário",
        "image": IMAGES["intermediario"],
        "course_price": COURSE_PRICE,
        "short_description": (
            "Nível Intermediário | Classes de palavras, verbos seriais, aspectos "
            "verbais, expressões idiomáticas e conversação avançada. 3 módulos."
        ),
        "long_description": (
            "<p>O curso <strong>Iorubá Intermediário</strong> aprofunda a gramática e "
            "a estrutura da língua, permitindo expressar ideias mais complexas e "
            "participar de conversas elaboradas.</p>"
            "<p>Baseado em <em>Essentials of Yoruba Grammar</em> de Oladele Awobuluyi "
            "(1978), você vai dominar:</p>"
            "<ul>"
            "<li>Substantivos: categorias humanos/não-humanos, quantidade, lugar, compostos</li>"
            "<li>Qualificadores: numerais, demonstrativos, relativos, genitivos</li>"
            "<li>Verbos seriais (serial verbs) e verbos de divisão (splitting verbs)</li>"
            "<li>Aspectos verbais: progressivo e perfectivo</li>"
            "<li>Provérbios complexos e expressões idiomáticas</li>"
            "<li>Leitura de textos curtos em Iorubá (contos, notícias)</li>"
            "<li>Debates, simulações e apresentações orais</li>"
            "</ul>"
            "<p><strong>Preço:</strong> a partir de R$ 320/mês (1 aula/semana).</p>"
            "<p><strong>Certificado:</strong> incluso ao concluir todas as unidades.</p>"
        ),
        "units": [
            # ── Módulo 1 ──────────────────────────────────────────────────────
            {
                "title": "Módulo 1 – Aprofundamento nas Classes de Palavras",
                "topics": [
                    "Lição 1: Substantivos — Categorias humanos e não-humanos",
                    "Lição 1: Substantivos de quantidade e valor",
                    "Lição 1: Substantivos de lugar e interrogativos",
                    "Lição 1: Substantivos polimórficos e compostos",
                    "Lição 2: Qualificadores — Numerais e demonstrativos",
                    "Lição 2: Qualificadores relativos e adjetivos",
                    "Lição 2: Qualificadores genitivos e tópicos",
                    "Lição 2: Concorrência de qualificadores",
                ],
            },
            # ── Módulo 2 ──────────────────────────────────────────────────────
            {
                "title": "Módulo 2 – Estruturas Verbais e Frasais",
                "topics": [
                    "Lição 3: Verbos Seriais e de Divisão — Conceito e uso de serial verbs",
                    "Lição 3: Verbos de divisão (splitting verbs) e suas aplicações",
                    "Lição 3: Formação de frases complexas com múltiplos verbos",
                    "Lição 4: Aspectos e Tempos Verbais — Revisão e aprofundamento",
                    "Lição 4: Aspectos verbais (progressivo, perfectivo)",
                    "Lição 4: Expressão de ações contínuas e concluídas",
                ],
            },
            # ── Módulo 3 ──────────────────────────────────────────────────────
            {
                "title": "Módulo 3 – Comunicação e Contexto Cultural",
                "topics": [
                    "Lição 5: Expressões Idiomáticas e Provérbios complexos",
                    "Lição 5: Contexto cultural dos provérbios",
                    "Lição 5: Introdução a expressões idiomáticas comuns",
                    "Lição 6: Leitura e Compreensão — Textos curtos (contos, notícias)",
                    "Lição 6: Desenvolvimento de estratégias de leitura",
                    "Lição 7: Conversação Avançada — Debates e discussões",
                    "Lição 7: Simulações de situações cotidianas e formais",
                    "Lição 7: Apresentações orais curtas",
                ],
            },
        ],
    },
    # ─── 3. AVANÇADO ──────────────────────────────────────────────────────────
    {
        "title": "Iorubá - Avançado",
        "category": "Iorubá - Avançado",
        "level_code": "Avançado",
        "image": IMAGES["avancado"],
        "course_price": COURSE_PRICE,
        "short_description": (
            "Nível Avançado | Gramática complexa, literatura, história e filosofia "
            "iorubá. Fluência em contextos acadêmicos, profissionais e culturais."
        ),
        "long_description": (
            "<p>O curso <strong>Iorubá Avançado</strong> é destinado a alunos com "
            "domínio sólido da língua que buscam fluência e proficiência plena.</p>"
            "<p>Baseado em <em>Essentials of Yoruba Grammar</em> (Awobuluyi, 1978) e "
            "<em>A History of the Yoruba People</em> (Akintoye, 2014), você vai "
            "dominar:</p>"
            "<ul>"
            "<li>Orações subordinadas, coordenadas, voz passiva/ativa</li>"
            "<li>Morfologia e derivação: prefixos, sufixos, infixos</li>"
            "<li>Partículas modais e aspectuais avançadas</li>"
            "<li>Análise de textos literários (contos, poesias, peças teatrais)</li>"
            "<li>Retórica, oratória e discurso formal em Iorubá</li>"
            "<li>Princípios de tradução Iorubá ↔ Português</li>"
            "<li>História dos reinos e impérios iorubá</li>"
            "<li>Orishas, cosmovisão e filosofia (Àṣẹ, Ìwà pẹ̀lẹ́)</li>"
            "<li>Sociedade iorubá contemporânea e diáspora</li>"
            "</ul>"
            "<p><strong>Preço:</strong> a partir de R$ 320/mês (1 aula/semana).</p>"
            "<p><strong>Certificado:</strong> incluso ao concluir todas as unidades.</p>"
        ),
        "units": [
            # ── Módulo 1 ──────────────────────────────────────────────────────
            {
                "title": "Módulo 1 – Gramática e Sintaxe Avançada",
                "topics": [
                    "Lição 1: Estruturas Frasais Complexas — Orações subordinadas e coordenadas",
                    "Lição 1: Voz passiva e ativa em Iorubá",
                    "Lição 1: Construções causativas e recíprocas",
                    "Lição 2: Morfologia e Derivação — Prefixos, sufixos e infixos",
                    "Lição 2: Análise morfológica de verbos e substantivos complexos",
                    "Lição 2: Processos de nominalização e verbalização",
                    "Lição 3: Partículas e Advérbios de Nuance — Uso avançado de partículas modais/aspectuais",
                    "Lição 3: Advérbios de tempo, lugar, modo e suas posições na frase",
                ],
            },
            # ── Módulo 2 ──────────────────────────────────────────────────────
            {
                "title": "Módulo 2 – Literatura e Discurso",
                "topics": [
                    "Lição 4: Análise de Textos Literários — Contos, poesias e peças teatrais",
                    "Lição 4: Autores iorubá proeminentes e suas obras",
                    "Lição 5: Retórica e Discurso Formal — Técnicas de oratória e persuasão",
                    "Lição 5: Análise de discursos políticos e religiosos",
                    "Lição 5: Prática de apresentação e debate",
                    "Lição 6: Tradução e Interpretação — Iorubá ↔ Português",
                    "Lição 6: Interpretação simultânea e consecutiva em contextos formais",
                ],
            },
            # ── Módulo 3 ──────────────────────────────────────────────────────
            {
                "title": "Módulo 3 – Cultura, História e Filosofia Iorubá",
                "topics": [
                    "Lição 7: História do Povo Iorubá — Origens, reinos e impérios",
                    "Lição 7: Impacto da colonização e a diáspora iorubá",
                    "Lição 7: Figuras históricas e eventos marcantes",
                    "Lição 8: Religião e Cosmovisão Iorubá — Os Orishas e o sistema de crenças",
                    "Lição 8: Rituais, cerimônias e festivais",
                    "Lição 8: Filosofia iorubá — Àṣẹ, Ìwà pẹ̀lẹ́ e conceitos centrais",
                    "Lição 9: Sociedade e Contemporaneidade — Estrutura social e familiar",
                    "Lição 9: Desafios e perspectivas da língua iorubá no século XXI",
                    "Lição 9: Projetos de pesquisa e estudo independente",
                ],
            },
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# FUNÇÕES AUXILIARES
# ─────────────────────────────────────────────────────────────────────────────


def _get_or_create_instructor() -> str:
    """Cria o usuário-instrutor Busayo Frank Alonge se não existir. Retorna o email."""
    if not frappe.db.exists("User", INSTRUCTOR_EMAIL):
        user = frappe.get_doc(
            {
                "doctype": "User",
                "email": INSTRUCTOR_EMAIL,
                "first_name": INSTRUCTOR_FIRST,
                "last_name": INSTRUCTOR_LAST,
                "mobile_no": INSTRUCTOR_PHONE,
                "send_welcome_email": 0,
                "user_type": "Website User",
                "bio": INSTRUCTOR_BIO,
            }
        )
        user.insert(ignore_permissions=True)
        frappe.db.commit()
        print(
            f"  ✓ Professor criado: {INSTRUCTOR_FIRST} {INSTRUCTOR_LAST} <{INSTRUCTOR_EMAIL}>"
        )
    else:
        print(f"  → Professor já existe: {INSTRUCTOR_EMAIL}")

    return INSTRUCTOR_EMAIL


def _create_or_update_category(data: dict, parent: str = None) -> None:
    """Cria uma LMS Category (subcategoria de idioma)."""
    category_name = data["title"]

    if frappe.db.exists("LMS Category", category_name):
        print(f"  → Categoria já existe: {category_name}")
        return

    doc = frappe.get_doc(
        {
            "doctype": "LMS Category",
            "category": category_name,
            "description": data.get("description", ""),
        }
    )

    try:
        meta = frappe.get_meta("LMS Category")
        field_names = [f.fieldname for f in meta.fields]
        if "parent_category" in field_names and parent:
            doc.parent_category = parent
        if "sort_order" in field_names and "sort_order" in data:
            doc.sort_order = data["sort_order"]
    except Exception:
        pass

    doc.insert(ignore_if_duplicate=True)
    frappe.db.commit()
    print(f"  ✓ Categoria criada: {category_name}")


def _build_chapter_lesson(course_name: str, unit: dict, unit_idx: int) -> None:
    """Cria Course Chapter e os Course Lesson vinculados."""
    chapter_title = unit["title"]

    existing = frappe.get_all(
        "Course Chapter",
        filters={"course": course_name, "title": chapter_title},
        fields=["name"],
        limit=1,
    )
    if existing:
        return

    chapter = frappe.get_doc(
        {
            "doctype": "Course Chapter",
            "title": chapter_title,
            "course": course_name,
        }
    )
    chapter.insert(ignore_permissions=True)
    chapter_name = chapter.name

    for _i, topic in enumerate(unit["topics"], start=1):
        lesson = frappe.get_doc(
            {
                "doctype": "Course Lesson",
                "title": topic,
                "chapter": chapter_name,
                "course": course_name,
                "body": f"<p>{topic}</p>",
            }
        )
        lesson.insert(ignore_permissions=True)
        chapter.append("lessons", {"lesson": lesson.name})

    chapter.save(ignore_permissions=True)


def _create_course(data: dict, instructor: str) -> None:
    """Cria um LMS Course completo com chapters e lessons."""
    existing = frappe.get_all(
        "LMS Course",
        filters={"title": data["title"]},
        fields=["name"],
        limit=1,
    )

    if existing:
        course_name = existing[0]["name"]
        print(f"  → Já existe: {data['title']} (name={course_name})")
    else:
        doc = frappe.get_doc(
            {
                "doctype": "LMS Course",
                "title": data["title"],
                "short_introduction": data["short_description"][:140],
                "description": data["long_description"],
                "image": data["image"],
                "category": data["category"],
                "paid_course": 1,
                "course_price": data["course_price"],
                "currency": "BRL",
                "published": 1,
                "enable_certification": 1,
            }
        )
        doc.append("instructors", {"instructor": instructor})
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        course_name = doc.name
        print(
            f"  ✓ Curso criado: {data['title']} ({data['level_code']}) name={course_name}"
        )

    for i, unit in enumerate(data["units"], start=1):
        try:
            _build_chapter_lesson(course_name, unit, i)
        except Exception as e:
            print(f"    ⚠ Erro no módulo '{unit['title']}': {e}")

    frappe.db.commit()
    print(f"    → {len(data['units'])} módulos configurados")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────


def execute():
    """
    Entry point para:
      bench --site vediums.com execute scripts.migrations.create_yoruba_courses.execute
    """
    print("\n🌍 Cadastrando Programa de Iorubá — 3 Níveis (Frappe LMS)")
    print("=" * 62)

    # 1. Professor
    print("\n[ Professor ]")
    instructor = _get_or_create_instructor()

    # 2. Categorias LMS
    print("\n[ Categorias LMS — Iorubá ]")
    for level in YORUBA_LEVELS:
        _create_or_update_category(level, parent="Iorubá")

    # 3. Cursos
    print("\n[ Cursos ]")
    for course_data in YORUBA_CURRICULUM:
        print(f"\n  [{course_data['level_code']}] {course_data['title']}")
        try:
            _create_course(course_data, instructor)
        except Exception as e:
            print(f"  ✗ Erro ao criar curso: {e}")
            frappe.log_error(str(e), "create_yoruba_courses")

    print("\n✅ Programa de Iorubá cadastrado com sucesso!")
    print(f"   Professor: {INSTRUCTOR_FIRST} {INSTRUCTOR_LAST} <{INSTRUCTOR_EMAIL}>")
    print(f"   Cursos: {len(YORUBA_CURRICULUM)} (Básico, Intermediário, Avançado)")
    print(f"   Preço base: R$ {COURSE_PRICE:,.2f}/mês (1 aula/semana)")
    print(f"   Tabela completa:")
    print(f"     1 aula/sem → R$ 320,00/mês  |  hora-prof: R$ 30,00")
    print(f"     2 aulas/sem → R$ 600,00/mês")
    print(f"     3 aulas/sem → R$ 900,00/mês")
    print(f"     4 aulas/sem → R$ 1.180,00/mês")
    print("=" * 62)


if __name__ == "__main__":
    execute()
