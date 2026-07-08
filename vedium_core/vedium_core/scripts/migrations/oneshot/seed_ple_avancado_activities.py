# -*- coding: utf-8 -*-
"""
Vedium — Atividades, exercícios de fixação e prova final do PLE Avançado

Conteúdo 100% original. Ver seed_ple_basico_activities.py pro mesmo padrão
e docstring completa (banco de 80 questões, sorteia 40, 70% pra passar,
3 tentativas, embaralha ordem; fixação com 10 questões por módulo, sem gate).

Fonte pedagógica: Nota 10 — Português do Brasil, nível elementar A1/A2.
Como este livro cobre as unidades 0 a 14, o curso avançado usa revisão
e aprofundamento das unidades finais do próprio livro, sem introduzir
conteúdos externos ao material.

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.seed_ple_avancado_activities.run
"""
import frappe

from vedium_core.scripts.migrations.oneshot.seed_ple_intermediario_activities import (
    EXAM_QUESTIONS as NOTA10_FINAL_UNITS_EXAM,
    MODULE_FIXATION as NOTA10_FINAL_UNITS_FIXATION,
)
from vedium_core.scripts.migrations.oneshot.seed_ple_basico_activities import (
    _make_quiz,
)

COURSE = "portugues-para-estrangeiros-avancado"

EXAM_QUESTIONS = [
    # Módulo 1 — subjuntivo, hipóteses, orações condicionais
    ("Complete: \"Espero que você ___ (conseguir) o emprego.\" (subjuntivo)", ["consiga", "consegue", "conseguirá", "conseguiu"], 0),
    ("Qual conjunção exige o subjuntivo?", ["talvez", "porque", "e", "mas"], 0),
    ("Complete: \"Se eu ___ (ter) mais tempo, viajaria mais.\" (imperfeito do subjuntivo)", ["tivesse", "tenho", "tive", "terei"], 0),
    ("\"Duvido que ele ___ (chegar) a tempo\" -- qual verbo completa?", ["chegue", "chega", "chegou", "chegará"], 0),
    ("Complete: \"Se choveresse, nós ___ (ficar) em casa.\" (futuro do pretérito)", ["ficaríamos", "ficamos", "ficaremos", "ficávamos"], 0),
    ("Qual expressão de dúvida exige subjuntivo?", ["\"É possível que...\"", "\"É certo que...\"", "\"Sei que...\"", "\"Tenho certeza que...\""], 0),
    ("Complete: \"Quando eu ___ (ter) tempo, te ligo.\" (futuro do subjuntivo)", ["tiver", "tenho", "tinha", "terei"], 0),
    ("\"Formular uma hipótese sobre o futuro\" pode usar:", ["\"Se eu fosse rico, viajaria o mundo.\"", "\"Eu vou trabalhar amanhã.\"", "\"Eu trabalhei ontem.\"", "\"Eu trabalho todo dia.\""], 0),
    ("Complete: \"Talvez ela ___ (vir) à festa.\" (subjuntivo)", ["venha", "vem", "veio", "virá"], 0),
    ("Qual oração exige subjuntivo: \"Quero que vocês ___ (estudar) mais\"?", ["estudem", "estudam", "estudarão", "estudaram"], 0),
    ("Complete: \"Se eu soubesse, eu não ___ (fazer) isso.\" (futuro do pretérito)", ["teria feito", "faço", "fiz", "farei"], 0),
    ("\"Debater sobre tecnologia e sociedade\" envolve:", ["argumentar com base em fatos e opiniões", "apenas concordar com o outro", "falar sem escutar", "evitar o assunto"], 0),
    ("Complete: \"É importante que todos ___ (participar) da reunião.\" (subjuntivo)", ["participem", "participam", "participarão", "participaram"], 0),
    ("Qual verbo completa: \"Caso ela ___ (precisar), me avise.\" (futuro do subjuntivo)", ["precise", "precisa", "precisou", "precisará"], 0),
    ("\"Analisar um cenário hipotético\" significa:", ["imaginar uma situação e suas consequências", "descrever um fato passado", "narrar uma rotina diária", "listar nomes próprios"], 0),
    ("Complete: \"Se tivéssemos mais recursos, ___ (investir) em pesquisa.\" (futuro do pretérito)", ["investiríamos", "investimos", "investiremos", "investíamos"], 0),
    ("Qual conjunção condicional introduz uma hipótese?", ["se", "porque", "mas", "e"], 0),
    ("Complete: \"Não acho que isso ___ (ser) verdade.\" (subjuntivo)", ["seja", "é", "foi", "será"], 0),
    ("\"Ponderar prós e contras de uma decisão\" é um exemplo de:", ["análise crítica", "narração de fatos", "descrição física", "saudação formal"], 0),
    ("Complete: \"Ainda que ___ (chover), sairemos.\" (subjuntivo)", ["chova", "chove", "choveu", "choverá"], 0),
    # Módulo 2 — voz passiva, discurso indireto avançado, literatura, movimentos culturais
    ("Complete na voz passiva: \"O livro ___ (escrever) por um autor famoso.\"", ["foi escrito", "escreveu", "escreve", "escreverá"], 0),
    ("Qual é a voz passiva sintética de \"Vendem-se casas\"?", ["já está na voz passiva sintética", "Casas são vendidas por alguém", "Alguém vende casas", "nenhuma das anteriores"], 0),
    ("Complete: \"Ele afirmou que ___ (ter) terminado o projeto.\" (discurso indireto)", ["tinha", "tem", "teve", "terá"], 0),
    ("\"Analisar um conto literário\" envolve observar:", ["personagens, enredo e narrador", "apenas a capa do livro", "só o preço do livro", "o número de páginas"], 0),
    ("Complete: \"A reportagem ___ (publicar) ontem gerou debate.\" (particípio)", ["publicada", "publicou", "publica", "publicando"], 0),
    ("Qual movimento cultural brasileiro surgiu nos anos 1960 e misturou influências internacionais?", ["Tropicália", "Barroco", "Romantismo Europeu", "Neoclassicismo"], 0),
    ("Complete: \"Segundo o autor, o personagem ___ (representar) a sociedade da época.\"", ["representa", "representou", "representará", "representaria"], 0),
    ("\"Interpretar uma crônica\" significa:", ["compreender a crítica social por trás do texto curto", "apenas ler em voz alta", "traduzir palavra por palavra", "memorizar o texto"], 0),
    ("Complete na voz passiva: \"As leis ___ (aprovar) pelo congresso.\"", ["foram aprovadas", "aprovaram", "aprovam", "aprovarão"], 0),
    ("Qual gênero literário é caracterizado por versos e ritmo?", ["poesia", "reportagem", "manual técnico", "contrato"], 0),
    ("Complete: \"O jornalista disse que a notícia ___ (ser) verificada.\" (discurso indireto)", ["seria", "é", "foi", "será"], 0),
    ("\"Bossa Nova\" é um movimento associado a qual arte?", ["música", "pintura", "arquitetura", "escultura"], 0),
    ("Complete: \"O quadro ___ (pintar) no século XIX.\" (voz passiva)", ["foi pintado", "pintou", "pinta", "pintará"], 0),
    ("Qual recurso narrativo apresenta a fala de um personagem sem aspas, integrada ao texto?", ["discurso indireto livre", "diálogo direto", "narração em terceira pessoa apenas", "monólogo interior explícito"], 0),
    ("Complete: \"Ela contou que ___ (ir) viajar em breve.\" (discurso indireto)", ["iria", "vai", "foi", "irá"], 0),
    ("\"Fazer uma leitura crítica de uma reportagem\" envolve:", ["questionar fontes e possíveis vieses", "aceitar tudo como verdade absoluta", "ignorar o conteúdo", "focar só no título"], 0),
    ("Complete na voz passiva: \"O prêmio ___ (entregar) ao vencedor.\"", ["foi entregue", "entregou", "entrega", "entregará"], 0),
    ("Qual autor é associado à literatura brasileira contemporânea (resposta genérica correta pro nível avançado)?", ["um autor(a) brasileiro(a) reconhecido(a) nacionalmente", "apenas autores estrangeiros", "só autores do século XV", "nenhum, o Brasil não tem literatura própria"], 0),
    ("Complete: \"Os resultados ___ (divulgar) na próxima semana.\" (voz passiva, futuro)", ["serão divulgados", "divulgam", "divulgaram", "divulgariam"], 0),
    ("\"Revisar os tempos do passado numa narrativa literária\" ajuda a entender:", ["a sequência temporal dos eventos", "só a gramática isolada", "apenas o vocabulário novo", "a pontuação do texto"], 0),
    # Módulo 3 — mundo do trabalho, pronomes relativos complexos, variação linguística, internet
    ("Complete: \"A reunião ___ (discutir) as metas do trimestre.\"", ["vai discutir", "discute (sozinho, sem contexto claro)", "discutiu (sem contexto claro)", "discutirá (menos natural aqui)"], 0),
    ("Qual pronome relativo completa: \"O projeto, ___ resultado superou expectativas, foi aprovado.\"?", ["cujo", "que", "quem", "onde"], 0),
    ("Complete um e-mail formal: \"Prezado(a) Sr(a)., venho por meio deste ___ solicitar...\"", ["e-mail", "carta informal", "mensagem de texto", "recado verbal"], 0),
    ("\"Elaborar um currículo profissional\" deve incluir:", ["experiência, formação e habilidades", "apenas o nome e a idade", "só uma foto", "nenhuma informação de contato"], 0),
    ("Complete: \"A pessoa ___ falei ontem é minha colega.\" (pronome relativo)", ["com quem", "que", "cujo", "onde"], 0),
    ("Qual expressão da internet significa \"em resumo\"?", ["\"TL;DR\" (ou equivalente em português)", "\"BRB\"", "\"LOL\"", "\"AFK\""], 0),
    ("Complete: \"Negociar um contrato\" exige:", ["comunicação clara e argumentação", "silêncio total", "assinatura sem leitura", "apenas gestos"], 0),
    ("\"Colocação pronominal formal\" prefere qual posição em início de frase?", ["ênclise (verbo-pronome)", "próclise sempre, mesmo em contexto formal de início de frase", "mesóclise sempre", "nenhuma regra existe"], 0),
    ("Complete: \"Este é o motivo ___ eu decidi mudar de emprego.\" (pronome relativo)", ["pelo qual", "que", "quem", "cujo"], 0),
    ("Qual variação regional é comum no português falado no Nordeste do Brasil (exemplo genérico correto)?", ["vocabulário e sotaque próprios da região", "não existe variação regional no Brasil", "só existe variação em Portugal", "todas as regiões falam de forma idêntica"], 0),
    ("Complete: \"Fazer uma apresentação de negócios\" envolve:", ["organizar dados e comunicar com clareza", "apenas ler um texto decorado", "falar o mais rápido possível", "evitar contato visual"], 0),
    ("Qual pronome relativo indica lugar?", ["onde", "que", "quem", "cujo"], 0),
    ("Complete: \"Os candidatos ___ currículos foram selecionados receberão um e-mail.\" (relativo possessivo)", ["cujos", "que", "quem", "onde"], 0),
    ("\"Regência verbal avançada\" trata de:", ["qual preposição cada verbo exige", "apenas conjugação no presente", "só pronomes pessoais", "somente plural e singular"], 0),
    ("Complete: \"Assistimos ___ um documentário interessante.\" (regência do verbo assistir)", ["a", "o", "para", "por"], 0),
    ("\"Identidade linguística\" está relacionada a:", ["como o sotaque e o vocabulário refletem origem cultural", "apenas gramática formal", "somente ortografia", "nenhuma das anteriores"], 0),
    ("Complete: \"Aspiro ___ um cargo de liderança.\" (regência)", ["a", "para", "com", "de"], 0),
    ("Qual linguagem é típica das redes sociais?", ["abreviações e informalidade", "apenas linguagem jurídica", "somente vocabulário acadêmico", "só citações formais"], 0),
    ("Complete: \"O relatório ___ o qual nos baseamos está desatualizado.\" (pronome relativo)", ["sobre", "que", "quem", "onde"], 0),
    ("\"Adaptar a linguagem ao contexto (formal/informal)\" é uma habilidade chamada:", ["registro linguístico", "sotaque", "conjugação verbal", "ortografia"], 0),
    # Reforço geral avançado
    ("Complete: \"Ainda que eu ___ (discordar), respeito sua opinião.\" (subjuntivo)", ["discorde", "discordo", "discordei", "discordarei"], 0),
    ("Qual figura de linguagem compara duas coisas usando \"como\"?", ["comparação (símile)", "metáfora direta sem \"como\"", "hipérbole", "eufemismo"], 0),
    ("Complete: \"O texto foi ___ (revisar) antes da publicação.\" (voz passiva)", ["revisado", "revisou", "revisa", "revisará"], 0),
    ("Qual conectivo indica contraste?", ["no entanto", "além disso", "portanto", "assim"], 0),
    ("Complete: \"Por mais que ele ___ (tentar), não conseguiu.\" (subjuntivo)", ["tentasse", "tenta", "tentou", "tentará"], 0),
    ("\"Argumentar com base em dados\" fortalece um texto porque:", ["dá credibilidade à opinião apresentada", "torna o texto mais longo apenas", "confunde o leitor de propósito", "não tem nenhum efeito"], 0),
    ("Complete: \"Espera-se que os alunos ___ (entregar) o trabalho na sexta.\" (subjuntivo)", ["entreguem", "entregam", "entregarão", "entregaram"], 0),
    ("Qual conectivo introduz uma conclusão?", ["portanto", "embora", "caso", "enquanto"], 0),
    ("Complete: \"Caso houvesse mais tempo, ___ (revisar) o texto de novo.\" (futuro do pretérito)", ["revisaríamos", "revisamos", "revisaremos", "revisávamos"], 0),
    ("\"Sintetizar as ideias principais de um texto longo\" é fazer:", ["um resumo", "uma cópia integral", "uma tradução literal", "uma lista de palavras aleatórias"], 0),
    ("Complete: \"É fundamental que a empresa ___ (investir) em inovação.\" (subjuntivo)", ["invista", "investe", "investiu", "investirá"], 0),
    ("Qual figura de linguagem atribui características humanas a algo não humano?", ["personificação", "comparação", "hipérbole", "eufemismo"], 0),
    ("Complete: \"Caso a proposta ___ (ser) aceita, começaremos na segunda.\" (futuro do subjuntivo)", ["seja", "é", "foi", "será"], 0),
    ("\"Redigir um parecer técnico\" exige:", ["linguagem objetiva e fundamentada", "opiniões pessoais sem embasamento", "linguagem coloquial e gírias", "informalidade excessiva"], 0),
    ("Complete: \"O acordo ___ (assinar) pelas duas partes na quinta-feira.\" (voz passiva, futuro)", ["será assinado", "assina", "assinou", "assinaria"], 0),
    ("Qual conectivo introduz uma ressalva/objeção?", ["apesar de", "além disso", "portanto", "assim"], 0),
    ("Complete: \"Se o mercado ___ (permitir), expandiremos os negócios.\" (futuro do subjuntivo)", ["permitir", "permite", "permitiu", "permitirá"], 0),
    ("\"Interpretar uma metáfora num poema\" significa:", ["entender o sentido figurado, não literal", "traduzir palavra por palavra", "contar as sílabas", "ignorar o significado"], 0),
    ("Complete: \"Nós ___ (esperar) que o projeto seja aprovado.\" (presente)", ["esperamos", "esperávamos", "esperaremos", "esperaríamos"], 0),
    ("Qual recurso argumentativo apresenta dados estatísticos como prova?", ["argumento de autoridade/dados", "apelo emocional apenas", "opinião sem embasamento", "repetição sem conteúdo"], 0),
]

MODULE_FIXATION = {
    "Módulo 1 — Opinião, Hipótese e Argumentação": [
        ("Complete: \"Espero que você ___ (conseguir) o emprego.\"", ["consiga", "consegue", "conseguirá", "conseguiu"], 0),
        ("Qual conjunção exige subjuntivo?", ["talvez", "porque", "e", "mas"], 0),
        ("Complete: \"Se eu ___ (ter) mais tempo, viajaria mais.\"", ["tivesse", "tenho", "tive", "terei"], 0),
        ("Complete: \"Duvido que ele ___ (chegar) a tempo.\"", ["chegue", "chega", "chegou", "chegará"], 0),
        ("Qual verbo completa: \"Quando eu ___ (ter) tempo, te ligo.\" (futuro do subjuntivo)", ["tiver", "tenho", "tinha", "terei"], 0),
        ("\"Formular uma hipótese\" pode ser:", ["\"Se eu fosse rico, viajaria o mundo.\"", "\"Eu trabalho todo dia.\"", "\"Eu trabalhei ontem.\"", "\"Vou trabalhar amanhã.\""], 0),
        ("Complete: \"Talvez ela ___ (vir) à festa.\"", ["venha", "vem", "veio", "virá"], 0),
        ("Qual verbo completa: \"Quero que vocês ___ (estudar) mais.\"?", ["estudem", "estudam", "estudarão", "estudaram"], 0),
        ("Complete: \"Se eu soubesse, eu não ___ (fazer) isso.\"", ["teria feito", "faço", "fiz", "farei"], 0),
        ("Qual conjunção condicional introduz uma hipótese?", ["se", "porque", "mas", "e"], 0),
    ],
    "Módulo 2 — Cultura, Sociedade e Mídia": [
        ("Complete na voz passiva: \"O livro ___ (escrever) por um autor famoso.\"", ["foi escrito", "escreveu", "escreve", "escreverá"], 0),
        ("Complete: \"Ele afirmou que ___ (ter) terminado o projeto.\"", ["tinha", "tem", "teve", "terá"], 0),
        ("Qual movimento cultural brasileiro é associado à música dos anos 1960?", ["Tropicália", "Barroco", "Romantismo Europeu", "Neoclassicismo"], 0),
        ("Complete na voz passiva: \"As leis ___ (aprovar) pelo congresso.\"", ["foram aprovadas", "aprovaram", "aprovam", "aprovarão"], 0),
        ("Qual gênero literário tem versos e ritmo?", ["poesia", "reportagem", "manual técnico", "contrato"], 0),
        ("Complete: \"O jornalista disse que a notícia ___ (ser) verificada.\"", ["seria", "é", "foi", "será"], 0),
        ("\"Bossa Nova\" é associada a qual arte?", ["música", "pintura", "arquitetura", "escultura"], 0),
        ("Complete: \"Ela contou que ___ (ir) viajar em breve.\"", ["iria", "vai", "foi", "irá"], 0),
        ("\"Leitura crítica de uma reportagem\" envolve:", ["questionar fontes e vieses", "aceitar tudo sem questionar", "ignorar o texto", "ler só o título"], 0),
        ("Complete na voz passiva: \"O prêmio ___ (entregar) ao vencedor.\"", ["foi entregue", "entregou", "entrega", "entregará"], 0),
    ],
    "Módulo 3 — Contextos Profissionais e Acadêmicos": [
        ("Qual pronome relativo completa: \"O projeto, ___ resultado superou expectativas...\"?", ["cujo", "que", "quem", "onde"], 0),
        ("\"Elaborar um currículo\" deve incluir:", ["experiência, formação e habilidades", "só nome e idade", "apenas uma foto", "nenhuma informação de contato"], 0),
        ("Complete: \"A pessoa ___ falei ontem é minha colega.\"", ["com quem", "que", "cujo", "onde"], 0),
        ("\"Negociar um contrato\" exige:", ["comunicação clara e argumentação", "silêncio total", "assinatura sem leitura", "apenas gestos"], 0),
        ("Complete: \"Este é o motivo ___ eu decidi mudar de emprego.\"", ["pelo qual", "que", "quem", "cujo"], 0),
        ("Qual pronome relativo indica lugar?", ["onde", "que", "quem", "cujo"], 0),
        ("\"Regência verbal\" trata de:", ["qual preposição cada verbo exige", "apenas conjugação no presente", "só pronomes pessoais", "plural e singular apenas"], 0),
        ("Complete: \"Assistimos ___ um documentário interessante.\"", ["a", "o", "para", "por"], 0),
        ("\"Adaptar a linguagem ao contexto\" é chamado de:", ["registro linguístico", "sotaque", "conjugação verbal", "ortografia"], 0),
        ("Complete: \"Aspiro ___ um cargo de liderança.\"", ["a", "para", "com", "de"], 0),
    ],
}

# O PDF fornecido (Nota 10 — Português do Brasil 2) é A1/A2 e termina na
# Unidade 14. Para garantir que o "Avançado" não use conteúdo fora do livro,
# substituímos o banco antigo por uma revisão/profundamento das unidades
# finais do próprio Nota 10 (férias, moradia, esportes, saúde, trabalho e
# lusofonia/português europeu vs português do Brasil).
EXAM_QUESTIONS = list(NOTA10_FINAL_UNITS_EXAM)
MODULE_FIXATION = {
    "Módulo 1 — Opinião, Hipótese e Argumentação": NOTA10_FINAL_UNITS_FIXATION[
        "Módulo 1 — Narrativa e Experiências Passadas"
    ],
    "Módulo 2 — Cultura, Sociedade e Mídia": NOTA10_FINAL_UNITS_FIXATION[
        "Módulo 2 — Saúde, Trabalho e Vida Social"
    ],
    "Módulo 3 — Contextos Profissionais e Acadêmicos": NOTA10_FINAL_UNITS_FIXATION[
        "Módulo 3 — Cultura, Opinião e Variação Linguística"
    ],
}


def run():
    if not frappe.db.exists("LMS Course", COURSE):
        print(f"Curso '{COURSE}' não existe -- rode create_ple_courses.run primeiro.")
        return

    _make_quiz(
        title="Prova Final — Português Avançado (PLE)",
        course=COURSE,
        lesson=None,
        questions=EXAM_QUESTIONS,
        max_attempts=3,
        passing_percentage=70,
        shuffle_questions=True,
        limit_questions_to=40,
        total_marks=40,
    )

    for chapter_title, questions in MODULE_FIXATION.items():
        chapter_name = frappe.db.get_value(
            "Course Chapter", {"course": COURSE, "title": chapter_title}
        )
        if not chapter_name:
            print(f"  AVISO: capítulo '{chapter_title}' não encontrado, pulando fixação.")
            continue
        last_lesson = frappe.db.get_value(
            "Course Lesson", {"chapter": chapter_name}, "name", order_by="idx desc"
        )
        _make_quiz(
            title=f"Exercícios de Fixação — {chapter_title}",
            course=COURSE,
            lesson=last_lesson,
            questions=questions,
            max_attempts=0,
            passing_percentage=70,
            shuffle_questions=True,
            limit_questions_to=0,
            total_marks=len(questions),
        )

    # Gate: Avançado só libera conteúdo depois de certificado no Intermediário.
    frappe.db.set_value(
        "LMS Course", COURSE, "custom_prerequisite_course",
        "portugues-para-estrangeiros-intermediario",
    )

    frappe.db.commit()
    print("\n✓ Atividades do PLE Avançado concluídas (+ gate configurado).")
