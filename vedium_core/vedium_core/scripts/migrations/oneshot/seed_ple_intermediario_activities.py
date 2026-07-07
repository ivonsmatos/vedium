# -*- coding: utf-8 -*-
"""
Vedium — Atividades, exercícios de fixação e prova final do PLE Intermediário

Conteúdo 100% original. Ver seed_ple_basico_activities.py pro mesmo padrão
e docstring completa (banco de 80 questões, sorteia 40, 70% pra passar,
3 tentativas, embaralha ordem; fixação por módulo sem gate).

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.seed_ple_intermediario_activities.run
"""
import frappe

from vedium_core.scripts.migrations.oneshot.seed_ple_basico_activities import (
    _make_quiz,
)

COURSE = "portugues-para-estrangeiros-intermediario"

EXAM_QUESTIONS = [
    # Módulo 1 — pretérito perfeito, pronomes oblíquos, viagens
    ("Complete: \"Eu ___ (viajar) para o Brasil ano passado.\"", ["viajei", "viajo", "viajava", "viajarei"], 0),
    ("Qual pronome substitui \"o livro\" em \"Eu comprei o livro\"?", ["comprei-o", "comprei-lhe", "comprei-me", "comprei-te"], 0),
    ("Complete: \"Nós ___ (visitar) meus avós no domingo.\" (passado)", ["visitamos", "visitávamos", "visitaremos", "visitamos (presente)"], 0),
    ("\"Sugerir um plano de viagem\" é dizer:", ["\"Que tal irmos à praia?\"", "\"Não gosto de viajar.\"", "\"Isso é impossível.\"", "\"Não sei onde fica.\""], 0),
    ("Complete: \"Ele ___ (comprar) o aluguel em dia.\" (pretérito perfeito)", ["pagou", "paga", "pagava", "pagará"], 0),
    ("Qual pronome oblíquo indica objeto indireto em \"Dei o presente a ela\"?", ["lhe", "o", "a", "me"], 0),
    ("Complete: \"Quando eu era criança, eu ___ (morar) em outra cidade.\" (imperfeito)", ["morava", "morei", "morarei", "moro"], 0),
    ("\"Comparar preços de aluguel\" envolve o uso de:", ["comparativos (mais/menos/tão... que)", "apenas adjetivos", "apenas verbos no futuro", "apenas substantivos"], 0),
    ("Complete: \"Nós ___ (fazer) exercício todos os dias no ano passado.\" (imperfeito)", ["fazíamos", "fizemos", "faremos", "fazemos"], 0),
    ("Qual pronome reflexivo completa: \"Eles ___ machucaram jogando futebol\"?", ["se", "lhe", "o", "me"], 0),
    ("Complete: \"Antes de sair, eu já ___ (terminar) o trabalho.\" (mais-que-perfeito)", ["tinha terminado", "terminei", "terminarei", "termino"], 0),
    ("\"Preferir um apartamento a uma casa\" usa qual estrutura?", ["prefiro X a Y", "prefiro X que Y", "prefiro X do que Y", "nenhuma das anteriores"], 0),
    ("Complete: \"Ela ___ (correr) todas as manhãs quando morava lá.\" (imperfeito)", ["corria", "correu", "correrá", "corre"], 0),
    ("Qual verbo no pretérito perfeito completa: \"Nós ___ (ir) ao cinema ontem\"?", ["fomos", "íamos", "iremos", "vamos"], 0),
    ("\"Malhar\" é sinônimo de:", ["fazer exercício físico", "cozinhar", "estudar", "dormir"], 0),
    ("Complete: \"Eu me ___ (levantar) muito cedo hoje.\" (pretérito perfeito)", ["levantei", "levanto", "levantava", "levantarei"], 0),
    ("Qual expressão indica preferência por atividade física?", ["\"Adoro correr pela manhã.\"", "\"Detesto sair de casa.\"", "\"Não sei nadar.\"", "\"Prefiro ficar parado.\""], 0),
    ("Complete: \"Quando cheguei, eles já ___ (sair).\" (mais-que-perfeito)", ["tinham saído", "saíram", "saem", "sairão"], 0),
    ("\"Fazer academia\" e \"praticar esportes\" são exemplos de:", ["atividades físicas", "profissões", "refeições", "documentos"], 0),
    ("Complete: \"Nós ___ (querer) alugar um apartamento maior.\" (presente)", ["queremos", "quisemos", "queríamos", "quereremos"], 0),
    # Módulo 2 — saúde, particípios, discurso direto/indireto, trabalho
    ("Complete: \"A que horas ___ a consulta?\"", ["é", "são", "está", "estão"], 0),
    ("Qual verbo completa: \"Minha cabeça ___ muito hoje.\" (doer)", ["dói", "doe", "doem", "doeu"], 0),
    ("\"Marcar uma consulta médica\" é:", ["agendar um horário com o médico", "cancelar um compromisso", "pedir receita sem médico", "comprar remédio sem prescrição"], 0),
    ("Complete o particípio: \"O documento já foi ___ (assinar).\"", ["assinado", "assinando", "assina", "assinar"], 0),
    ("Qual pronome oblíquo combinado substitui \"deu o livro para mim\"?", ["deu-mo", "deu-lhe", "deu-o", "deu-me"], 0),
    ("Complete: \"Estou preparando meu currículo para a ___.\" (entrevista)", ["entrevista", "entrevistado", "entrevistando", "entrevistou"], 0),
    ("\"Ele disse que estava doente\" é um exemplo de:", ["discurso indireto", "discurso direto", "imperativo", "subjuntivo"], 0),
    ("Complete: \"Estas são as pessoas ___ trabalham comigo.\" (pronome relativo)", ["que", "quem", "cujo", "onde"], 0),
    ("Qual verbo completa: \"O médico ___ (receitar) um antibiótico.\" (pretérito perfeito)", ["receitou", "receita", "receitava", "receitará"], 0),
    ("\"Estou com dor de garganta\" descreve:", ["um sintoma de saúde", "uma opinião", "um plano futuro", "uma profissão"], 0),
    ("Complete o discurso direto -> indireto: Ele disse: \"Estou cansado\" -> Ele disse que ___ cansado.", ["estava", "está", "esteve", "estará"], 0),
    ("Qual particípio completa: \"A carta foi ___ (escrever) ontem.\"?", ["escrita", "escrevendo", "escreve", "escreveu"], 0),
    ("Complete: \"Preciso marcar uma consulta ___ dentista.\"", ["com o", "no", "para", "pelo"], 0),
    ("\"Fazer uma entrevista de emprego\" envolve responder sobre:", ["experiência profissional", "receitas médicas", "previsão do tempo", "trajetos de ônibus"], 0),
    ("Complete: \"Os pacientes ___ (ser) atendidos por ordem de chegada.\" (presente passivo)", ["são", "é", "está", "estão"], 0),
    ("Qual pronome relativo completa: \"A empresa ___ eu trabalho é grande.\"?", ["onde", "que", "quem", "cujo"], 0),
    ("Complete: \"Minhas costas ___ depois do treino.\" (doer, presente)", ["doem", "dói", "doeram", "doerá"], 0),
    ("\"Contratar\" um funcionário significa:", ["dar emprego a alguém", "demitir alguém", "pedir demissão", "reclamar do chefe"], 0),
    ("Complete: \"Ela me perguntou se eu ___ (poder) ajudá-la.\" (discurso indireto)", ["podia", "posso", "poderei", "pude"], 0),
    ("Qual verbo completa: \"O paciente já foi ___ (examinar).\"?", ["examinado", "examinando", "examina", "examinou"], 0),
    # Módulo 3 — lusofonia, futuro do pretérito, opinião, textos, cultura
    ("Complete no futuro do pretérito: \"Eu ___ (gostar) de conhecer Moçambique.\"", ["gostaria", "gosto", "gostei", "gostarei"], 0),
    ("Qual país é lusófono (fala português)?", ["Angola", "México", "Peru", "Itália"], 0),
    ("Complete: \"Na sua opinião, o que ___ (dever) mudar no país?\"", ["deveria", "deve", "devia (informal apenas)", "deverá (só formal)"], 0),
    ("\"Expressar uma opinião com educação\" pode começar com:", ["\"Na minha opinião...\"", "\"Você está errado.\"", "\"Isso é bobagem.\"", "\"Não quero falar sobre isso.\""], 0),
    ("Complete: \"Nós ___ (adorar) participar do festival de música.\" (futuro do pretérito)", ["adoraríamos", "adoramos", "adoraremos", "adorávamos"], 0),
    ("Qual expressão regional é tipicamente usada em Portugal (não no Brasil)?", ["\"Fixe!\"", "\"Legal!\"", "\"Maneiro!\"", "\"Da hora!\""], 0),
    ("Complete: \"Se eu tivesse tempo, eu ___ (viajar) mais.\"", ["viajaria", "viajo", "viajei", "viajarei"], 0),
    ("\"Debater um tema com argumentos\" requer:", ["apresentar razões e exemplos", "apenas concordar com tudo", "mudar de assunto", "ficar em silêncio"], 0),
    ("Complete: \"A música brasileira ___ muito diversa.\" (ser)", ["é", "está", "são", "estão"], 0),
    ("Qual é um movimento cultural brasileiro?", ["Bossa Nova", "Barroco Espanhol", "Renascimento Italiano", "Impressionismo Francês"], 0),
    ("Complete: \"Eu ___ (ler) esse artigo interessante ontem.\" (pretérito perfeito)", ["li", "leio", "lia", "lerei"], 0),
    ("\"Discutir uma notícia\" significa:", ["conversar e analisar o que foi noticiado", "ignorar completamente a notícia", "escrever a notícia", "traduzir a notícia"], 0),
    ("Complete: \"Muitos brasileiros ___ (celebrar) o Carnaval em fevereiro.\" (presente)", ["celebram", "celebra", "celebrei", "celebrará"], 0),
    ("Qual verbo completa: \"Se pudesse, eu ___ (morar) em outro país.\"?", ["moraria", "moro", "morei", "morarei"], 0),
    ("\"Produzir um texto narrativo\" significa:", ["contar uma história com começo, meio e fim", "escrever apenas uma lista", "traduzir um poema", "copiar um texto pronto"], 0),
    ("Complete: \"A culinária brasileira é conhecida pela sua ___.\" (diversidade)", ["diversidade", "diversidades", "diverso", "diversos"], 0),
    ("Qual festa popular é celebrada em junho no Brasil?", ["Festa Junina", "Carnaval", "Réveillon", "Independência"], 0),
    ("Complete: \"Nós ___ (discutir) esse assunto na próxima reunião.\" (futuro)", ["discutiremos", "discutimos", "discutíamos", "discutiríamos"], 0),
    ("\"Ter uma visão crítica sobre um texto\" envolve:", ["analisar e questionar o conteúdo", "aceitar tudo sem questionar", "ignorar o texto", "decorar o texto"], 0),
    ("Complete: \"Eles ___ (gostar) de visitar países lusófonos.\" (futuro do pretérito)", ["gostariam", "gostam", "gostaram", "gostarão"], 0),
    # Reforço geral intermediário
    ("Qual tempo verbal expressa uma ação habitual no passado?", ["pretérito imperfeito", "pretérito perfeito", "futuro do presente", "presente do subjuntivo"], 0),
    ("Complete: \"Ontem ___ (chover) o dia inteiro.\" (pretérito perfeito)", ["choveu", "chove", "chovia", "choverá"], 0),
    ("Qual conjunção introduz uma condição?", ["se", "mas", "porque", "e"], 0),
    ("Complete: \"Eu gostaria de saber ___ ele chegou.\" (indireta)", ["se", "que", "quem", "onde"], 0),
    ("\"Pedir desculpas formalmente\" pode ser:", ["\"Peço desculpas pelo atraso.\"", "\"Foi mal, cara.\"", "\"Não ligo pra isso.\"", "\"Problema seu.\""], 0),
    ("Complete: \"Quando eu ___ (chegar), ele já tinha saído.\" (pretérito perfeito)", ["cheguei", "chego", "chegava", "chegarei"], 0),
    ("Qual verbo completa: \"Nós ___ (precisar) conversar sobre isso.\" (presente)", ["precisamos", "precisávamos", "precisaremos", "precisaríamos"], 0),
    ("\"Fazer um comentário construtivo\" significa:", ["dar uma sugestão útil e respeitosa", "criticar sem motivo", "ignorar o outro", "mudar de assunto"], 0),
    ("Complete: \"Ela trabalha ___ segunda a sexta.\"", ["de", "desde", "para", "por"], 0),
    ("Qual pronome substitui \"para o Pedro e para a Maria\" em \"Entreguei o convite para eles\"?", ["lhes", "os", "as", "me"], 0),
    ("Complete: \"Nós já ___ (terminar) o relatório quando o chefe chegou.\" (mais-que-perfeito)", ["tínhamos terminado", "terminamos", "terminaremos", "terminávamos"], 0),
    ("Qual verbo completa: \"Ontem à noite, ___ (chover) muito.\" (pretérito perfeito)", ["choveu", "chove", "chovia", "choverá"], 0),
    ("Complete: \"Eu ___ (achar) que ela tinha razão.\" (pretérito imperfeito)", ["achava", "achei", "acharei", "acho"], 0),
    ("\"Fazer um planejamento financeiro\" envolve:", ["organizar receitas e despesas", "gastar sem controle", "ignorar o orçamento", "pedir empréstimo sem necessidade"], 0),
    ("Complete: \"Se eu ___ (saber) antes, teria avisado você.\" (imperfeito do subjuntivo)", ["soubesse", "sei", "sabia", "saberei"], 0),
    ("Qual verbo completa: \"Nós ___ (decidir) mudar de cidade no ano passado.\"", ["decidimos", "decidíamos", "decidiremos", "decidiríamos"], 0),
    ("Complete: \"Este é o restaurante ___ jantamos ontem.\" (pronome relativo)", ["onde", "que", "quem", "cujo"], 0),
    ("\"Comparar dois apartamentos antes de alugar\" é um exemplo de:", ["tomar uma decisão informada", "agir por impulso", "ignorar o preço", "não pesquisar nada"], 0),
    ("Complete: \"Quando ele me ligou, eu já ___ (sair) de casa.\" (mais-que-perfeito)", ["tinha saído", "saí", "saio", "sairei"], 0),
    ("Qual verbo completa: \"Nós ___ (assistir) a um filme muito bom ontem.\"", ["assistimos", "assistíamos", "assistiremos", "assistiríamos"], 0),
]

MODULE_FIXATION = {
    "Módulo 1 — Narrativa e Experiências Passadas": [
        ("Complete: \"Eu ___ (comprar) uma passagem ontem.\"", ["comprei", "compro", "comprava", "comprarei"], 0),
        ("Qual tempo indica hábito no passado?", ["pretérito imperfeito", "pretérito perfeito", "futuro", "presente"], 0),
        ("Complete: \"Quando eu era criança, eu ___ (brincar) muito.\"", ["brincava", "brinquei", "brincarei", "brinco"], 0),
        ("Qual pronome substitui \"o carro\" em \"Eu vendi o carro\"?", ["vendi-o", "vendi-lhe", "vendi-me", "vendi-te"], 0),
        ("Complete: \"Antes de você chegar, eu já ___ (sair).\"", ["tinha saído", "saí", "saio", "sairei"], 0),
        ("\"Malhar\" significa:", ["fazer exercício", "cozinhar", "dormir", "estudar"], 0),
        ("Complete: \"Nós ___ (correr) todos os dias no ano passado.\"", ["corríamos", "corremos", "correremos", "corremos (presente)"], 0),
        ("Qual estrutura expressa preferência?", ["prefiro X a Y", "prefiro X sem Y", "prefiro X contra Y", "nenhuma"], 0),
        ("Complete: \"Ela ___ (viajar) para o Rio no mês passado.\"", ["viajou", "viaja", "viajava", "viajará"], 0),
        ("Qual é o oposto de \"alugar\"?", ["comprar/vender", "morar", "visitar", "trabalhar"], 0),
    ],
    "Módulo 2 — Saúde, Trabalho e Vida Social": [
        ("Complete: \"Minha cabeça ___ hoje.\" (doer)", ["dói", "doe", "doeu", "doerá"], 0),
        ("Qual verbo completa: \"O documento foi ___ (assinar).\"?", ["assinado", "assinando", "assina", "assinou"], 0),
        ("\"Marcar uma consulta\" significa:", ["agendar um horário médico", "cancelar um plano", "comprar remédio", "ir ao hospital sem hora marcada"], 0),
        ("Complete: \"Ele disse que ___ cansado.\" (discurso indireto)", ["estava", "está", "esteve", "estará"], 0),
        ("Qual pronome relativo completa: \"A empresa ___ trabalho é grande.\"?", ["onde", "que", "quem", "cujo"], 0),
        ("Complete: \"Estou preparando meu currículo para a ___.\"", ["entrevista", "entrevistado", "entrevistando", "entrevistou"], 0),
        ("\"Contratar alguém\" significa:", ["dar emprego", "demitir", "pedir demissão", "reclamar"], 0),
        ("Complete: \"Os pacientes ___ atendidos por ordem de chegada.\"", ["são", "é", "está", "estão"], 0),
        ("Qual sintoma se descreve com \"Estou com dor de garganta\"?", ["um sintoma de saúde", "uma opinião", "um plano", "uma profissão"], 0),
        ("Complete: \"Ela me perguntou se eu ___ ajudá-la.\" (discurso indireto)", ["podia", "posso", "poderei", "pude"], 0),
    ],
    "Módulo 3 — Cultura, Opinião e Variação Linguística": [
        ("Complete: \"Eu ___ (gostar) de conhecer Angola.\" (futuro do pretérito)", ["gostaria", "gosto", "gostei", "gostarei"], 0),
        ("Qual país é lusófono?", ["Moçambique", "México", "Peru", "Itália"], 0),
        ("\"Expressar opinião com educação\" pode começar com:", ["\"Na minha opinião...\"", "\"Você está errado.\"", "\"Isso é bobagem.\"", "\"Cala a boca.\""], 0),
        ("Complete: \"Se eu tivesse tempo, eu ___ mais.\" (viajar)", ["viajaria", "viajo", "viajei", "viajarei"], 0),
        ("Qual é um movimento cultural brasileiro?", ["Tropicália", "Barroco Espanhol", "Renascimento Italiano", "Impressionismo Francês"], 0),
        ("Complete: \"Muitos brasileiros ___ o Carnaval.\" (celebrar)", ["celebram", "celebra", "celebrei", "celebrará"], 0),
        ("\"Debater com argumentos\" requer:", ["apresentar razões e exemplos", "só concordar", "mudar de assunto", "ficar calado"], 0),
        ("Complete: \"Nós ___ esse assunto na próxima reunião.\" (discutir, futuro)", ["discutiremos", "discutimos", "discutíamos", "discutiríamos"], 0),
        ("Qual festa é celebrada em junho no Brasil?", ["Festa Junina", "Carnaval", "Réveillon", "Independência"], 0),
        ("Complete: \"Eles ___ de visitar países lusófonos.\" (gostar, futuro do pretérito)", ["gostariam", "gostam", "gostaram", "gostarão"], 0),
    ],
}


def run():
    if not frappe.db.exists("LMS Course", COURSE):
        print(f"Curso '{COURSE}' não existe -- rode create_ple_courses.run primeiro.")
        return

    _make_quiz(
        title="Prova Final — Português Intermediário (PLE)",
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

    # Gate: Intermediário só libera conteúdo depois de certificado no Básico.
    frappe.db.set_value(
        "LMS Course", COURSE, "custom_prerequisite_course",
        "portugues-para-estrangeiros-basico",
    )

    frappe.db.commit()
    print("\n✓ Atividades do PLE Intermediário concluídas (+ gate configurado).")
