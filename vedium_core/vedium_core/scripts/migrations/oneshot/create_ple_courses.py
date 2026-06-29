"""Criação dos cursos PLE — Português para Estrangeiros (Básico, Intermediário, Avançado).

Grade curricular baseada em "Nota 10: Português do Brasil" (Dias & Frota, Lidel 2015).

Executar UMA VEZ no servidor após o deploy:
    bench execute vedium_core.scripts.migrations.oneshot.create_ple_courses.run
"""

import frappe

PLE_CATEGORY = "Português para Estrangeiros"
COURSE_PRICE = 240
CURRENCY = "BRL"


# ---------------------------------------------------------------------------
# Dados dos cursos
# ---------------------------------------------------------------------------

def _basico_chapters():
    return [
        {
            "title": "Módulo 1 — Primeiros Contatos e Informações Pessoais",
            "lessons": [
                "Introdução à Língua Portuguesa — Alfabeto e pronúncia do português brasileiro",
                "Saudações e despedidas — Bom dia, Boa tarde, Olá, Tchau",
                "Apresentação pessoal — Meu nome é..., Eu sou de...",
                "Oi! Tudo bem? — Cumprimentos e troca de informações pessoais",
                "Artigos, presente do indicativo e vocabulário de países e profissões",
                "Que lugar maravilhoso! — Localizar pessoas e objetos",
                "Verbos ser e estar, preposições de lugar e meios de transporte",
            ],
        },
        {
            "title": "Módulo 2 — O Dia a Dia e o Ambiente",
            "lessons": [
                "Seu primo é um gato! — Família e amigos",
                "Descrever pessoas — características físicas e de personalidade",
                "Gênero e número dos adjetivos, possessivos e vocabulário de família",
                "Tudo o Santo Dia — Rotinas diárias e horários",
                "Advérbios de frequência e verbos reflexivos",
                "Que comidinha boa! — Pedir comida e fazer compras de alimentos",
                "Imperativo básico e vocabulário de comidas, bebidas e restaurante",
            ],
        },
        {
            "title": "Módulo 3 — Interações e Cultura Brasileira",
            "lessons": [
                "O verão está chegando! — Clima, estações do ano e convites",
                "Estar + gerúndio e presente do indicativo com verbos irregulares",
                "Boas compras! — Fazer compras, pechinchar e falar de dinheiro",
                "Comparativos, demonstrativos e vocabulário de roupas e lojas",
                "Vire à esquerda e siga em frente! — Dar e pedir direções",
                "Imperativo avançado, preposições de movimento e pontos de referência",
            ],
        },
    ]


def _basico_description():
    return """<p>O curso <strong>PLE Básico</strong> é destinado a quem não tem nenhum conhecimento
ou tem contato muito limitado com o português. Com base no método
<em>Nota 10: Português do Brasil</em>, você aprenderá as estruturas essenciais
e o vocabulário necessário para se comunicar em situações do dia a dia, com
forte imersão na cultura brasileira.</p>
<p><strong>Ao final do curso você será capaz de:</strong></p>
<ul>
<li>Usar saudações, apresentações e despedidas</li>
<li>Fornecer e solicitar informações pessoais (nome, nacionalidade, idade, profissão)</li>
<li>Formular frases simples no presente do indicativo</li>
<li>Pedir em restaurantes, fazer compras e perguntar direções</li>
<li>Compreender aspectos culturais básicos do Brasil</li>
</ul>"""


def _intermediario_chapters():
    return [
        {
            "title": "Módulo 1 — Narrativa e Experiências Passadas",
            "lessons": [
                "Enfim, Férias! — Planos de viagem, sugestões e concordâncias",
                "Pretérito perfeito simples e pronomes oblíquos átonos (objeto direto)",
                "Quanto é o aluguel? — Moradia, comparações e preferências",
                "Pretérito mais-que-perfeito e pronomes oblíquos (objeto indireto)",
                "É hora da malhação! — Esportes e atividades físicas",
                "Pretérito imperfeito do indicativo e pronomes reflexivos",
            ],
        },
        {
            "title": "Módulo 2 — Saúde, Trabalho e Vida Social",
            "lessons": [
                "A que horas é a consulta? — Saúde, bem-estar e consultas médicas",
                "Verbo doer, pronomes oblíquos em combinações e particípios passados",
                "Hoje é dia de trabalho! — Profissões e entrevista de emprego",
                "Discurso direto e indireto, pronomes relativos invariáveis",
            ],
        },
        {
            "title": "Módulo 3 — Cultura, Opinião e Variação Linguística",
            "lessons": [
                "Gostarias de conhecer outros países lusófonos? — Lusofonia e diversidade cultural",
                "Futuro do pretérito e vocabulário de países lusófonos e expressões regionais",
                "Expressão de opiniões e argumentação em português",
                "Leitura e discussão de notícias e artigos de interesse geral",
                "Produção de textos narrativos e descritivos",
                "Cultura popular brasileira — música, festas e culinária",
            ],
        },
    ]


def _intermediario_description():
    return """<p>O curso <strong>PLE Intermediário</strong> é para quem já tem uma base sólida em
português e deseja expandir a capacidade de comunicação em contextos mais variados
e complexos. Com base no livro <em>Nota 10: Português do Brasil</em>, este nível
aprofunda a gramática, amplia o vocabulário e desenvolve a fluência em situações
sociais e profissionais.</p>
<p><strong>Ao final do curso você será capaz de:</strong></p>
<ul>
<li>Participar de conversas longas e detalhadas sobre variados tópicos</li>
<li>Dominar os tempos verbais do passado (perfeito, imperfeito e mais-que-perfeito)</li>
<li>Lidar com situações como planejar viagens, procurar moradia e falar sobre saúde</li>
<li>Ler e compreender textos de dificuldade moderada (notícias, artigos de opinião)</li>
<li>Reconhecer e discutir aspectos culturais aprofundados do Brasil</li>
</ul>"""


def _avancado_chapters():
    return [
        {
            "title": "Módulo 1 — Opinião, Hipótese e Argumentação",
            "lessons": [
                "Expressando opiniões e dúvidas — debates sobre meio ambiente, tecnologia e sociedade",
                "Presente do subjuntivo — expressão de desejo, dúvida e emoção",
                "Hipóteses e condições — cenários hipotéticos e planejamento futuro",
                "Pretérito imperfeito e futuro do subjuntivo — orações condicionais (Se...)",
            ],
        },
        {
            "title": "Módulo 2 — Cultura, Sociedade e Mídia",
            "lessons": [
                "A mídia e a informação — análise de notícias e reportagens brasileiras",
                "Voz passiva analítica e sintética, discurso indireto avançado",
                "Arte e literatura brasileira — contos, crônicas e poemas",
                "Movimentos culturais brasileiros — Bossa Nova, Tropicália e outros",
                "Revisão e aprofundamento dos tempos do passado na narrativa literária",
            ],
        },
        {
            "title": "Módulo 3 — Contextos Profissionais e Acadêmicos",
            "lessons": [
                "O mundo do trabalho e negócios — reuniões, apresentações e negociações",
                "Elaboração de currículos, e-mails formais e relatórios em português",
                "Pronomes relativos complexos (cujo, o qual) e regência verbal avançada",
                "Variação linguística e identidade — sotaques e dialetos do Brasil",
                "Linguagem da internet e das redes sociais em português",
                "Colocação pronominal em contextos formais e informais",
            ],
        },
    ]


def _avancado_description():
    return """<p>O curso <strong>PLE Avançado</strong> é para quem já tem fluência significativa
e deseja aprimorar o uso da língua em contextos acadêmicos, profissionais e culturais
complexos. Além do <em>Nota 10</em>, este nível expande consideravelmente o escopo,
com o modo subjuntivo, análise de textos autênticos e aprofundamento na cultura
e sociedade brasileiras.</p>
<p><strong>Ao final do curso você será capaz de:</strong></p>
<ul>
<li>Compreender e produzir textos complexos — artigos de opinião, ensaios e relatórios</li>
<li>Dominar o modo subjuntivo em suas diversas formas</li>
<li>Participar ativamente de debates sobre temas abstratos e controversos</li>
<li>Utilizar expressões idiomáticas, gírias e nuances da linguagem coloquial e formal</li>
<li>Analisar criticamente aspectos da história, política, literatura e artes do Brasil</li>
</ul>"""


# ---------------------------------------------------------------------------
# Criação no banco
# ---------------------------------------------------------------------------

COURSES = [
    {
        "slug": "portugues-para-estrangeiros-basico",
        "title": "Português para Estrangeiros — Nível Básico (PLE)",
        "short_introduction": (
            "Para quem está começando do zero. Aprenda saudações, vocabulário essencial e "
            "comunicação básica do português brasileiro com imersão cultural desde a primeira aula."
        ),
        "description_fn": _basico_description,
        "chapters_fn": _basico_chapters,
    },
    {
        "slug": "portugues-para-estrangeiros-intermediario",
        "title": "Português para Estrangeiros — Nível Intermediário (PLE)",
        "short_introduction": (
            "Para quem já tem base em português. Domine os tempos do passado, amplie o "
            "vocabulário e conquiste fluência em situações sociais e profissionais."
        ),
        "description_fn": _intermediario_description,
        "chapters_fn": _intermediario_chapters,
    },
    {
        "slug": "portugues-para-estrangeiros-avancado",
        "title": "Português para Estrangeiros — Nível Avançado (PLE)",
        "short_introduction": (
            "Para quem já tem fluência e quer se aperfeiçoar. Domine o subjuntivo, textos "
            "autênticos e o português em contextos acadêmicos e profissionais."
        ),
        "description_fn": _avancado_description,
        "chapters_fn": _avancado_chapters,
    },
]


def run():
    """Cria os 3 cursos PLE na plataforma. Idempotente — pula o que já existir."""
    _ensure_ple_category()
    cat_name = frappe.db.get_value("LMS Category", {"category": PLE_CATEGORY}, "name")

    for course_data in COURSES:
        _create_course(course_data, cat_name)

    frappe.db.commit()
    print("\n✓ Cursos PLE criados com sucesso.")
    print("  Acesse o desk → LMS Course para publicar, adicionar imagens e ajustar preços.")


def _ensure_ple_category():
    if frappe.db.exists("LMS Category", {"category": PLE_CATEGORY}):
        return
    frappe.get_doc({
        "doctype": "LMS Category",
        "category": PLE_CATEGORY,
    }).insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  ✓ Categoria '{PLE_CATEGORY}' criada.")


def _create_course(data, category_name):
    slug = data["slug"]

    if frappe.db.exists("LMS Course", slug):
        print(f"  — Curso '{slug}' já existe, pulando.")
        return

    course = frappe.get_doc({
        "doctype": "LMS Course",
        "name": slug,
        "title": data["title"],
        "short_introduction": data["short_introduction"],
        "description": data["description_fn"](),
        "paid_course": 1,
        "course_price": COURSE_PRICE,
        "currency": CURRENCY,
        "published": 1,
        "category": category_name,
    })
    course.insert(ignore_permissions=True)
    print(f"\n  ✓ Curso '{slug}' criado.")

    for idx, chapter_data in enumerate(data["chapters_fn"](), start=1):
        chapter = frappe.get_doc({
            "doctype": "Course Chapter",
            "title": chapter_data["title"],
            "course": slug,
        })
        chapter.insert(ignore_permissions=True)

        for lesson_title in chapter_data["lessons"]:
            frappe.get_doc({
                "doctype": "Course Lesson",
                "title": lesson_title,
                "chapter": chapter.name,
                "course": slug,
                "content": f"<p>{lesson_title}</p>",
            }).insert(ignore_permissions=True)

        print(f"    Módulo {idx}: {chapter_data['title']} — {len(chapter_data['lessons'])} aulas")
