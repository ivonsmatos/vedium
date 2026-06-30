from urllib.parse import quote


BASE_URL = "https://vediums.com"
WHATSAPP_PHONE = "5511911293075"


LANDINGS = {
    "curso-de-ingles-online": {
        "title": "Curso de Inglês Online ao Vivo (A1 a C1) — Vedium",
        "short_title": "Curso de Inglês Online",
        "meta_description": "Curso de inglês online ao vivo da Vedium: aulas com professor em tempo real, do A1 ao C1, foco em conversação, certificado e plano por objetivo. A partir de R$ 240/mês.",
        "tagline": "Inglês do A1 ao C1",
        "h1": "Curso de inglês online ao vivo, com professor de verdade",
        "lead": "A Vedium ensina inglês em aulas ao vivo, não em vídeos gravados. Você evolui do A1 ao C1 com um professor que corrige sua fala em tempo real, turmas pequenas, plano por objetivo e foco em conversação desde a primeira aula.",
        "hero_image": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1920&q=80",
        "audience": "Iniciantes absolutos, quem travou na conversação, profissionais em recolocação, quem vai viajar ou morar fora, e estudantes que precisam de inglês para prova, trabalho ou faculdade.",
        "level": "A1 a C1 (CEFR)",
        "frequency": "1 a 4 aulas ao vivo por semana",
        "duration": "Plano contínuo por nível e objetivo",
        "summary": "Você é avaliado por nível CEFR, recebe um plano de estudo e estuda com aulas ao vivo, prática oral, correção individual, tarefas curtas e acompanhamento humano até atingir o objetivo.",
        "pain_title": "Por que tanta gente estuda anos e não destrava a fala",
        "pain_intro": "A maioria dos cursos entrega vídeo gravado e exercício solto. Sem alguém para ouvir e corrigir você falando, a conversação não evolui. A aula ao vivo resolve exatamente isso.",
        "pain_points": [
            "Entende inglês lendo e ouvindo, mas trava na hora de falar.",
            "Já tentou app e curso gravado e perdeu a constância sem acompanhamento.",
            "Não sabe ao certo o próprio nível nem por onde recomeçar.",
            "Precisa de inglês para uma meta concreta (entrevista, viagem, prova) e tem prazo.",
        ],
        "outcomes": [
            "Falar inglês com mais naturalidade e menos medo de errar.",
            "Saber exatamente seu nível CEFR e o caminho até o próximo.",
            "Ganhar vocabulário e estrutura aplicáveis ao seu objetivo real.",
            "Manter constância com aulas ao vivo e acompanhamento do professor.",
        ],
        "modules": [
            {"title": "Diagnóstico de nível", "text": "Teste e conversa inicial para situar você no CEFR (A1 a C1) e definir prioridades."},
            {"title": "Conversação guiada", "text": "Prática oral desde o início, com correção de pronúncia, ritmo e vocabulário."},
            {"title": "Gramática com uso real", "text": "Estruturas explicadas a partir de situações concretas, não de regras soltas."},
            {"title": "Listening e compreensão", "text": "Treino de escuta com áudios, diálogos e materiais autênticos por nível."},
            {"title": "Inglês para o seu objetivo", "text": "Trilhas para entrevista, negócios, viagem, atendimento ou tecnologia."},
            {"title": "Preparação para provas", "text": "Apoio para TOEFL, IELTS e provas de proficiência conforme a necessidade."},
        ],
        "format_items": [
            "Aulas online ao vivo, com professor e prática oral — não é vídeo gravado.",
            "Turmas pequenas e plano ajustado ao seu nível e prazo.",
            "Tarefas curtas entre as aulas para fixar o conteúdo.",
            "Certificado de conclusão conforme requisitos do curso livre.",
        ],
        "price_from": "240",
        "price_display": "A partir de R$ 240/mês",
        "price_note": "Valor de referência do plano leve (1 aula ao vivo por semana). Planos com mais aulas por semana têm valores diferentes — veja a página de Planos ou fale com a equipe para o valor do seu objetivo.",
        "workload": "PT2H",
        "seo_title": "Tudo sobre o curso de inglês online ao vivo da Vedium",
        "seo_sections": [
            {
                "heading": "Como funciona um curso de inglês online ao vivo",
                "body": [
                    "<p>No curso de inglês online da Vedium, cada aula acontece <strong>ao vivo, com um professor em tempo real</strong> — diferente de plataformas que entregam apenas vídeos gravados e exercícios automáticos. Essa é a diferença que mais impacta a fala: quando alguém ouve você falando e corrige na hora a pronúncia, o vocabulário e a estrutura, a conversação evolui de verdade. Em vídeo gravado, ninguém percebe que você está repetindo o mesmo erro há meses.</p>",
                    "<p>As aulas são em <strong>turmas pequenas</strong>, o que garante tempo de fala para cada aluno. Você começa com um diagnóstico de nível, recebe um plano de estudo orientado ao seu objetivo e segue uma trilha contínua, com tarefas curtas entre as aulas para fixar o conteúdo. O acompanhamento é humano: o professor sabe onde você está, o que precisa destravar e ajusta o ritmo conforme sua evolução.</p>",
                ],
            },
            {
                "heading": "Do A1 ao C1: o que significam os níveis de inglês",
                "body": [
                    "<p>A Vedium organiza o inglês pelo <strong>Quadro Europeu Comum de Referência (CEFR)</strong>, o padrão internacional usado para medir proficiência em idiomas. Saber seu nível evita recomeçar do zero sem necessidade ou pular etapas importantes:</p>",
                    "<ul><li><strong>A1 e A2 (básico):</strong> você se apresenta, fala sobre rotina, faz pedidos simples e entende frases do dia a dia.</li><li><strong>B1 e B2 (intermediário):</strong> você sustenta conversas, dá opiniões, lida com situações de trabalho e viagem e entende a maior parte de filmes e textos.</li><li><strong>C1 (avançado):</strong> você se comunica com fluência e naturalidade em contextos profissionais e acadêmicos, com vocabulário amplo e poucos travamentos.</li></ul>",
                    "<p>No primeiro contato, um <strong>teste de nível gratuito</strong> e uma conversa diagnóstica situam você no CEFR. A partir daí, o plano mostra com clareza onde você está e o que falta para o próximo nível.</p>",
                ],
            },
            {
                "heading": "Quanto tempo leva para aprender inglês?",
                "body": [
                    "<p>Não existe um número único, mas há uma referência honesta: avançar <strong>um nível do CEFR costuma exigir de 3 a 6 meses</strong> de estudo consistente, dependendo do ponto de partida, da frequência das aulas e da prática entre elas. Quem faz duas aulas por semana e revisa nos intervalos evolui mais rápido do que quem estuda de forma esparsa.</p>",
                    "<p>Os fatores que mais aceleram o aprendizado são <strong>constância, prática oral frequente e um objetivo claro</strong>. Por isso a Vedium trabalha com planos de 1 a 4 aulas por semana: a frequência certa é a que cabe na sua rotina e mantém você praticando sem grandes intervalos, que é quando o progresso costuma se perder.</p>",
                ],
            },
            {
                "heading": "Aula ao vivo ou aplicativo de idiomas: o que funciona melhor?",
                "body": [
                    "<p>Aplicativos de idiomas são ótimos para criar o hábito e treinar vocabulário em pequenas doses, mas têm um limite claro: <strong>eles não conversam de verdade com você</strong>. Reconhecimento de fala automático não percebe a entonação errada, não pergunta o que você quis dizer e não adapta a explicação ao seu contexto. É por isso que muita gente acumula meses de app e ainda trava numa conversa real.</p>",
                    "<p>A aula ao vivo cobre exatamente essa lacuna. Um professor humano <strong>ouve, corrige e provoca a fala</strong> — faz a pergunta de acompanhamento, puxa o assunto que interessa à sua carreira e ajusta o ritmo quando percebe uma dificuldade. Na prática, o melhor resultado costuma vir da combinação: o app para revisar entre as aulas e a aula ao vivo para destravar a conversação. Na Vedium, o foco está na aula ao vivo, porque é ali que a fluência realmente acontece.</p>",
                ],
            },
            {
                "heading": "Inglês para conversação, trabalho, viagem e provas",
                "body": [
                    "<p>O mesmo curso se adapta a objetivos diferentes. Se a sua meta é <strong>conversação</strong>, a prática oral guiada está no centro de cada aula. Se é <strong>carreira</strong>, há trilhas específicas como <a href=\"/ingles-para-entrevista\">inglês para entrevista de emprego</a>, <a href=\"/ingles-executivo\">inglês executivo</a> e <a href=\"/ingles-para-programadores\">inglês para programadores</a>. Para quem vai viajar, o <a href=\"/ingles-para-viagens\">inglês para viagens</a> prioriza situações reais de aeroporto, hotel e restaurante.</p>",
                    "<p>Quem precisa comprovar proficiência conta com apoio para <strong>TOEFL e IELTS</strong> e outras provas, com foco no formato do exame e nas habilidades cobradas. Em todos os casos, o ponto de partida é o mesmo: descobrir seu nível e montar um plano que leve do ponto atual até o objetivo, sem conteúdo genérico.</p>",
                ],
            },
            {
                "heading": "Quanto custa e como começar",
                "body": [
                    "<p>Os planos da Vedium começam <strong>a partir de R$ 240/mês</strong> no formato leve (uma aula ao vivo por semana). Planos com mais aulas semanais — indicados para quem tem prazo ou quer acelerar — têm valores proporcionais à frequência. Você não precisa decidir sozinho: a equipe recomenda o ritmo ideal a partir do seu nível, objetivo e disponibilidade.</p>",
                    "<p>Para começar, faça o <a href=\"/teste-de-nivel-ingles\">teste de nível de inglês gratuito</a> e, em seguida, fale com a equipe para a aula diagnóstica. É a forma mais segura de não começar por uma trilha desalinhada ao seu momento — e de já sair da primeira conversa com um plano claro.</p>",
                ],
            },
        ],
        "faqs": [
            {"q": "As aulas são ao vivo ou gravadas?", "a": "Ao vivo, com professor em tempo real e turmas pequenas. Você pratica a fala e é corrigido na hora — não é videoaula gravada."},
            {"q": "Como descubro meu nível de inglês?", "a": "Você faz o teste de nível gratuito e uma conversa diagnóstica com a equipe, que situam você no CEFR (A1 a C1) antes de definir o plano."},
            {"q": "Quanto custa o curso de inglês?", "a": "Os planos começam a partir de R$ 240/mês no formato leve (1 aula por semana). Planos com mais aulas têm valores proporcionais. A equipe recomenda a frequência ideal para o seu objetivo."},
            {"q": "Em quanto tempo eu evoluo?", "a": "Em média, avançar um nível do CEFR leva de 3 a 6 meses com estudo consistente. A frequência das aulas e a prática entre elas influenciam diretamente o ritmo."},
            {"q": "Preciso já saber alguma coisa de inglês?", "a": "Não. A trilha pode começar do zero (A1) ou continuar de onde você parou, conforme o resultado do diagnóstico."},
            {"q": "O curso tem certificado?", "a": "Sim, há certificado de conclusão conforme os requisitos do curso livre."},
        ],
        "whatsapp_text": "Olá, quero saber sobre o curso de inglês online ao vivo da Vedium.",
    },
    "ingles-para-entrevista": {
        "title": "Inglês para Entrevista de Emprego — Vedium",
        "short_title": "Inglês para Entrevista",
        "meta_description": "Prepare-se para entrevistas em inglês com aulas ao vivo, simulações, vocabulário profissional e feedback de fala.",
        "tagline": "Carreira internacional",
        "h1": "Inglês para entrevista de emprego com treino real de fala",
        "lead": "A trilha prepara você para entrevistas em inglês com segurança, clareza e repertório profissional. O foco é transformar respostas decoradas em comunicação natural, com simulações, feedback e vocabulário adequado ao seu cargo.",
        "hero_image": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=1920&q=80",
        "audience": "Profissionais em processo seletivo, entrevistas com RH, entrevistas técnicas, vagas internacionais, recolocação ou promoção.",
        "level": "A2 a B2",
        "frequency": "2 aulas ao vivo por semana",
        "duration": "Plano adaptado à data da entrevista",
        "summary": "Você pratica apresentação pessoal, trajetória, resultados, pontos fortes, perguntas comportamentais, perguntas técnicas e follow-up profissional.",
        "pain_title": "Por que preparar a entrevista com professor",
        "pain_intro": "Entrevistas exigem vocabulário, estrutura e presença. Mesmo quem entende inglês pode travar quando precisa falar sobre carreira sob pressão.",
        "pain_points": [
            "Dificuldade para explicar experiência profissional sem traduzir palavra por palavra.",
            "Insegurança com perguntas comportamentais como desafios, liderança e resultados.",
            "Falta de vocabulário para falar de projetos, métricas, tecnologia ou gestão.",
            "Medo de pronúncia, pausas longas e respostas curtas demais.",
        ],
        "outcomes": [
            "Apresentar seu perfil em inglês com clareza e objetividade.",
            "Responder perguntas comuns de RH usando estrutura STAR e exemplos reais.",
            "Explicar projetos, responsabilidades e resultados com vocabulário profissional.",
            "Ganhar fluidez por meio de simulações e correção individual.",
        ],
        "modules": [
            {"title": "Pitch profissional", "text": "Como se apresentar, resumir sua trajetória e conectar experiência ao cargo desejado."},
            {"title": "Perguntas de RH", "text": "Forças, fraquezas, conflitos, liderança, pressão, metas e tomada de decisão."},
            {"title": "Entrevista técnica", "text": "Vocabulário para explicar ferramentas, processos, projetos e problemas resolvidos."},
            {"title": "Pronúncia e fluidez", "text": "Correção de sons críticos, ritmo, pausas e respostas com mais naturalidade."},
            {"title": "Perguntas ao entrevistador", "text": "Como demonstrar interesse, maturidade e visão sobre a vaga."},
            {"title": "Simulado final", "text": "Entrevista completa com feedback de conteúdo, clareza, vocabulário e confiança."},
        ],
        "format_items": [
            "Aulas online ao vivo, com professor e prática oral.",
            "Roteiro personalizado para sua vaga, área e prazo.",
            "Tarefas curtas para preparar respostas entre as aulas.",
            "Indicação de próxima trilha após a entrevista: executivo, tecnologia ou fluência geral.",
        ],
        "faqs": [
            {"q": "Consigo me preparar mesmo com pouco tempo?", "a": "Sim. A trilha pode ser intensiva quando existe uma entrevista marcada, priorizando respostas de maior impacto."},
            {"q": "Preciso estar avançado?", "a": "Não. A preparação é ajustada ao seu nível, mas funciona melhor a partir de A2."},
            {"q": "Vocês ajudam com entrevista técnica?", "a": "Sim. O professor trabalha vocabulário, estrutura de resposta e simulação dentro do seu contexto."},
            {"q": "O teste de nível substitui a aula diagnóstica?", "a": "Não. O teste orienta a conversa inicial; a confirmação acontece na aula ou atendimento diagnóstico."},
        ],
        "whatsapp_text": "Olá, quero me preparar para entrevista em inglês na Vedium.",
    },
    "ingles-para-programadores": {
        "title": "Inglês para Programadores — Vedium",
        "short_title": "Inglês para Programadores",
        "meta_description": "Inglês para programadores com aulas ao vivo: entrevistas técnicas, documentação, reuniões, pair programming e comunicação global.",
        "tagline": "Tecnologia e carreira global",
        "h1": "Inglês para programadores que precisam trabalhar com times globais",
        "lead": "Uma trilha prática para devs, QA, produto, dados e tecnologia que precisam falar em reuniões, explicar soluções, ler documentação, escrever mensagens e passar por entrevistas técnicas em inglês.",
        "hero_image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=1920&q=80",
        "audience": "Desenvolvedores, analistas, tech leads, QA, produto, dados, suporte técnico e profissionais que querem vagas internacionais.",
        "level": "A2 a B2",
        "frequency": "1 ou 2 aulas ao vivo por semana",
        "duration": "Trilha por objetivo profissional",
        "summary": "Você pratica inglês aplicado a tecnologia: daily, code review, documentação, incidentes, entrevistas, arquitetura e colaboração em times remotos.",
        "pain_title": "Inglês técnico não é só vocabulário",
        "pain_intro": "O desafio costuma aparecer quando você precisa explicar raciocínio, negociar prazo, defender uma solução ou entender sotaques em uma call.",
        "pain_points": [
            "Entender documentação, mas travar para falar em reuniões.",
            "Dificuldade para explicar bugs, decisões técnicas e trade-offs.",
            "Insegurança em entrevistas técnicas internacionais.",
            "Mensagens em inglês pouco naturais para Slack, e-mail e tickets.",
        ],
        "outcomes": [
            "Participar de dailies, plannings e retrospectivas com mais confiança.",
            "Explicar problemas técnicos de forma simples e objetiva.",
            "Responder entrevistas técnicas com vocabulário e estrutura.",
            "Melhorar escrita profissional para tickets, commits e documentação.",
        ],
        "modules": [
            {"title": "Daily e reuniões", "text": "Status, impedimentos, prioridades, estimativas e comunicação objetiva."},
            {"title": "Documentação e tickets", "text": "Como ler, escrever e resumir requisitos, bugs e decisões."},
            {"title": "Entrevista técnica", "text": "Experiência, projetos, algoritmos, arquitetura, testes e resolução de problemas."},
            {"title": "Code review", "text": "Discordar com educação, sugerir melhorias e explicar escolhas técnicas."},
            {"title": "Incidentes e suporte", "text": "Reportar falhas, impacto, causa provável, mitigação e próximos passos."},
            {"title": "Carreira internacional", "text": "LinkedIn, currículo, pitch e conversas com recrutadores."},
        ],
        "format_items": [
            "Aulas ao vivo com roleplays de rotina técnica.",
            "Vocabulário aplicado à sua stack, cargo e objetivo.",
            "Feedback de speaking, clareza e escrita profissional.",
            "Plano para entrevista, trabalho remoto ou evolução contínua.",
        ],
        "faqs": [
            {"q": "Preciso saber programar em inglês?", "a": "Não. A trilha parte do seu contexto e melhora comunicação, vocabulário e segurança oral."},
            {"q": "Serve para entrevista internacional?", "a": "Sim. Há módulos para entrevista técnica, apresentação de projetos e conversa com recrutadores."},
            {"q": "Posso trazer situações reais do trabalho?", "a": "Sim. Reuniões, tickets e apresentações podem virar prática guiada em aula."},
            {"q": "O foco é conversação ou gramática?", "a": "Os dois aparecem, mas a gramática entra a serviço da comunicação profissional."},
        ],
        "whatsapp_text": "Olá, quero saber sobre inglês para programadores na Vedium.",
    },
    "ingles-executivo": {
        "title": "Inglês Executivo Online — Vedium",
        "short_title": "Inglês Executivo",
        "meta_description": "Inglês executivo online com aulas ao vivo para reuniões, liderança, apresentações, negociação e comunicação profissional.",
        "tagline": "Business English",
        "h1": "Inglês executivo para reuniões, liderança e negociação",
        "lead": "Aulas ao vivo para profissionais que precisam conduzir reuniões, apresentar resultados, negociar, escrever com precisão e representar a empresa em contextos internacionais.",
        "hero_image": "https://images.unsplash.com/photo-1556761175-b413da4baf72?w=1920&q=80",
        "audience": "Executivos, líderes, gestores, consultores, empreendedores, vendas B2B, RH e profissionais em expansão internacional.",
        "level": "B1 a C1",
        "frequency": "2 aulas ao vivo por semana",
        "duration": "Plano mensal com metas executivas",
        "summary": "A trilha combina vocabulário de negócios, comunicação intercultural, apresentações, negociação e tomada de decisão em inglês.",
        "pain_title": "O inglês executivo precisa ser preciso",
        "pain_intro": "Em ambientes corporativos, pequenos ruídos de linguagem podem afetar autoridade, clareza e negociação. O objetivo é falar melhor, não apenas falar mais.",
        "pain_points": [
            "Reuniões em inglês com pouca participação ativa.",
            "Apresentações com leitura excessiva de slides.",
            "Dificuldade para negociar, discordar ou alinhar expectativas.",
            "E-mails e mensagens com tom pouco natural ou pouco executivo.",
        ],
        "outcomes": [
            "Conduzir reuniões com pauta, abertura, transições e fechamento claros.",
            "Apresentar resultados, dados e recomendações com confiança.",
            "Negociar prazos, escopo, preço e prioridades com diplomacia.",
            "Escrever e-mails profissionais com tom adequado ao contexto.",
        ],
        "modules": [
            {"title": "Reuniões executivas", "text": "Abertura, alinhamento, interrupções, follow-up e decisões."},
            {"title": "Apresentações", "text": "Storyline, dados, transições, perguntas difíceis e conclusão."},
            {"title": "Negociação", "text": "Propostas, concessões, objeções, riscos e próximos passos."},
            {"title": "Liderança", "text": "Feedback, gestão de conflito, delegação e conversas difíceis."},
            {"title": "Escrita profissional", "text": "E-mails, mensagens, atas, resumos e comunicação com stakeholders."},
            {"title": "Interculturalidade", "text": "Tom, formalidade, clareza e etiqueta em contextos internacionais."},
        ],
        "format_items": [
            "Aulas ao vivo com simulações de reuniões e apresentações.",
            "Material adaptado ao setor, cargo e rotina do aluno.",
            "Correção de vocabulário, estrutura, tom e pronúncia.",
            "Possibilidade de formato B2B para equipes sob consulta.",
        ],
        "faqs": [
            {"q": "É indicado para líderes?", "a": "Sim. A trilha foi desenhada para comunicação corporativa, liderança e decisões em inglês."},
            {"q": "Posso preparar uma apresentação real?", "a": "Sim. O professor pode trabalhar roteiro, ensaio, vocabulário e perguntas."},
            {"q": "Atende empresas?", "a": "Sim, há possibilidade de proposta B2B conforme demanda e número de colaboradores."},
            {"q": "Preciso ser avançado?", "a": "Não. A trilha funciona a partir de B1, com metas ajustadas ao nível atual."},
        ],
        "whatsapp_text": "Olá, quero saber sobre inglês executivo na Vedium.",
    },
    "curso-de-ioruba-online": {
        "title": "Curso de Iorubá Online — Vedium",
        "short_title": "Curso de Iorubá Online",
        "alt": {"pt-BR": "curso-de-ioruba-online", "en": "learn-yoruba-online"},
        "meta_description": "Curso de iorubá online com aulas ao vivo, pronúncia, vocabulário, cultura e trilha estruturada para iniciantes.",
        "tagline": "Idioma e cultura",
        "h1": "Aprenda iorubá online com estrutura, pronúncia e contexto cultural",
        "lead": "A Vedium trata o iorubá como uma jornada de idioma, cultura e pertencimento. O curso combina aulas ao vivo, prática oral, vocabulário essencial e explicações culturais com responsabilidade.",
        "hero_image": "https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=1920&q=80",
        "audience": "Pessoas que querem começar iorubá do zero, estudar cultura afro-diaspórica, ampliar repertório linguístico ou se reconectar com raízes culturais.",
        "level": "Iniciante",
        "frequency": "1 ou 2 aulas ao vivo por semana",
        "duration": "Módulos progressivos",
        "summary": "Você aprende sons, tons, saudações, vocabulário de rotina, frases essenciais e fundamentos culturais para estudar com respeito e continuidade.",
        "pain_title": "Iorubá exige escuta, tom e orientação",
        "pain_intro": "Aprender sozinho pode gerar dúvidas de pronúncia e sentido. A aula ao vivo ajuda a corrigir sons, entender contexto e praticar com segurança.",
        "pain_points": [
            "Dificuldade para encontrar uma trilha organizada e confiável.",
            "Insegurança com tons, acentuação e pronúncia.",
            "Confusão entre vocabulário, cultura e uso real do idioma.",
            "Falta de acompanhamento para evoluir além de listas de palavras.",
        ],
        "outcomes": [
            "Pronunciar saudações e palavras iniciais com mais precisão.",
            "Construir frases simples para apresentação e rotina.",
            "Entender vocabulário com contexto cultural.",
            "Criar base para seguir para módulos intermediários.",
        ],
        "modules": [
            {"title": "Sons e tons", "text": "Introdução à pronúncia, escuta e diferenças sonoras importantes."},
            {"title": "Saudações", "text": "Cumprimentos, apresentações e expressões de respeito."},
            {"title": "Vocabulário essencial", "text": "Família, corpo, casa, rotina, números e objetos comuns."},
            {"title": "Frases iniciais", "text": "Estruturas para perguntar, responder e formar sentenças simples."},
            {"title": "Cultura em contexto", "text": "Uso social da língua, cuidado com significados e referências culturais."},
            {"title": "Prática oral", "text": "Repetição guiada, diálogos curtos e feedback do professor."},
        ],
        "format_items": [
            "Aulas online ao vivo com prática de pronúncia.",
            "Trilha gradual para quem começa do zero.",
            "Contexto cultural sem promessas religiosas ou sensacionalistas.",
            "Orientação para continuidade por módulos.",
        ],
        "faqs": [
            {"q": "Preciso ter conhecimento prévio?", "a": "Não. A trilha pode começar do zero, com foco em pronúncia e vocabulário inicial."},
            {"q": "O curso é religioso?", "a": "A proposta é educacional e linguística, com contexto cultural tratado com respeito."},
            {"q": "Iorubá tem certificado?", "a": "Sim, conforme conclusão e requisitos do curso livre."},
            {"q": "Como sei por onde começar?", "a": "Você pode falar com a equipe e fazer o diagnóstico inicial antes da matrícula."},
        ],
        "whatsapp_text": "Olá, quero saber sobre curso de iorubá online na Vedium.",
    },
    "ioruba-para-iniciantes": {
        "title": "Iorubá para Iniciantes — Vedium",
        "short_title": "Iorubá para Iniciantes",
        "meta_description": "Iorubá para iniciantes com aulas ao vivo: saudações, pronúncia, vocabulário básico, tons e contexto cultural.",
        "tagline": "Primeiros passos",
        "h1": "Comece iorubá do jeito certo: sons, tons, saudações e frases úteis",
        "lead": "Uma entrada guiada para quem quer aprender iorubá sem se perder. A trilha organiza os primeiros sons, palavras e estruturas para criar base real de estudo.",
        "hero_image": "https://images.unsplash.com/photo-1523805009345-7448845a9e53?w=1920&q=80",
        "audience": "Iniciantes absolutos, estudantes de cultura africana, brasileiros da diáspora e pessoas que buscam uma primeira experiência com o idioma.",
        "level": "Iniciante absoluto",
        "frequency": "1 ou 2 aulas ao vivo por semana",
        "duration": "Primeiro módulo introdutório",
        "summary": "Você aprende pronúncia, escuta inicial, saudações, números, frases de apresentação e vocabulário cotidiano.",
        "pain_title": "O começo define a base",
        "pain_intro": "No iorubá, aprender sons e tons desde o início evita vícios difíceis de corrigir depois.",
        "pain_points": [
            "Não saber como pronunciar corretamente.",
            "Estudar palavras soltas sem conseguir formar frases.",
            "Misturar referências culturais sem entender uso linguístico.",
            "Perder motivação por falta de sequência clara.",
        ],
        "outcomes": [
            "Reconhecer sons e tons iniciais com mais atenção.",
            "Usar saudações e apresentações simples.",
            "Construir frases curtas com vocabulário essencial.",
            "Entender como continuar para o próximo módulo.",
        ],
        "modules": [
            {"title": "Alfabeto e sons", "text": "Introdução aos sons e à escuta ativa."},
            {"title": "Tons", "text": "Primeira percepção de tom e significado."},
            {"title": "Saudações", "text": "Formas de cumprimentar e responder."},
            {"title": "Apresentação pessoal", "text": "Nome, origem, família e frases iniciais."},
            {"title": "Números e rotina", "text": "Vocabulário de uso prático."},
            {"title": "Diálogos guiados", "text": "Conversas curtas com feedback."},
        ],
        "format_items": [
            "Aulas ao vivo para corrigir pronúncia desde o início.",
            "Exercícios simples de repetição e escuta.",
            "Material organizado por tema.",
            "Próximos passos sugeridos ao fim do módulo.",
        ],
        "faqs": [
            {"q": "É para quem nunca estudou?", "a": "Sim. A página foi pensada para iniciantes absolutos."},
            {"q": "Vou aprender a falar ou só vocabulário?", "a": "A proposta é usar vocabulário em frases e diálogos simples."},
            {"q": "Preciso de material antes da aula?", "a": "Não. A orientação inicial é feita pela Vedium."},
            {"q": "Posso estudar em grupo?", "a": "A disponibilidade depende das turmas abertas e horários."},
        ],
        "whatsapp_text": "Olá, quero começar iorubá para iniciantes na Vedium.",
    },
    "portugues-para-estrangeiros": {
        "title": "Português para Estrangeiros — Vedium",
        "short_title": "Português para Estrangeiros",
        "alt": {"pt-BR": "portugues-para-estrangeiros", "en": "learn-portuguese-brazil"},
        "meta_description": "Português para estrangeiros com aulas ao vivo para morar, trabalhar, estudar e se comunicar melhor no Brasil.",
        "tagline": "Portuguese for foreigners",
        "h1": "Português para estrangeiros com foco em vida real no Brasil",
        "lead": "Aulas ao vivo para estrangeiros que precisam se comunicar em português no trabalho, estudos, serviços, viagens ou adaptação ao Brasil.",
        "hero_image": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=1920&q=80",
        "audience": "Estrangeiros no Brasil, expatriados, estudantes internacionais, profissionais remotos e pessoas que se relacionam com brasileiros.",
        "level": "A1 a B2",
        "frequency": "1 ou 2 aulas ao vivo por semana",
        "duration": "Plano por objetivo de adaptação",
        "summary": "Você pratica conversas reais, pronúncia, escuta, vocabulário brasileiro e situações do cotidiano.",
        "pain_title": "Português para viver, não apenas memorizar",
        "pain_intro": "O português do Brasil tem ritmo, expressões e contextos culturais que não aparecem em listas de vocabulário.",
        "pain_points": [
            "Dificuldade para entender brasileiros falando rápido.",
            "Insegurança em bancos, consultas, reuniões ou serviços.",
            "Confusão com gênero, verbos, preposições e pronúncia.",
            "Falta de vocabulário para trabalho e vida cotidiana.",
        ],
        "outcomes": [
            "Conversar em situações reais com mais autonomia.",
            "Entender instruções, perguntas e respostas comuns.",
            "Melhorar pronúncia e ritmo de fala.",
            "Ganhar vocabulário para trabalho, moradia e rotina.",
        ],
        "modules": [
            {"title": "Sobre mim", "text": "Apresentação, nacionalidade, profissão, família e interesses."},
            {"title": "Rotina no Brasil", "text": "Compras, transporte, alimentação, horários e serviços."},
            {"title": "Português no trabalho", "text": "Reuniões, mensagens, apresentações curtas e alinhamentos."},
            {"title": "Gramática prática", "text": "Verbos, gênero, número, perguntas e frases úteis."},
            {"title": "Cultura e expressões", "text": "Uso natural, informalidade e contexto brasileiro."},
            {"title": "Conversação", "text": "Simulações e correção de fala em tempo real."},
        ],
        "format_items": [
            "Aulas online ao vivo em português com suporte gradual.",
            "Explicações em inglês quando necessário.",
            "Trilha por objetivo: vida no Brasil, trabalho ou prova.",
            "Possibilidade de preparação para Celpe-Bras em trilha específica.",
        ],
        "faqs": [
            {"q": "The classes can include English support?", "a": "Yes. The teacher can use English support when needed, while progressively increasing Portuguese practice."},
            {"q": "Is it Brazilian Portuguese?", "a": "Yes. The focus is Portuguese as used in Brazil."},
            {"q": "Can I prepare for work situations?", "a": "Yes. We can include meetings, e-mails, presentations and daily professional vocabulary."},
            {"q": "Do I need a placement test?", "a": "The free test helps us estimate your level before recommending a path."},
        ],
        "whatsapp_text": "Hello, I want to learn Portuguese for foreigners with Vedium.",
    },
    "portugues-para-executivos": {
        "title": "Português para Executivos — Vedium",
        "short_title": "Português para Executivos",
        "meta_description": "Português para executivos estrangeiros com aulas ao vivo para reuniões, negócios, apresentações e adaptação cultural no Brasil.",
        "tagline": "Business Portuguese",
        "h1": "Português para executivos que trabalham com o Brasil",
        "lead": "Uma trilha para estrangeiros que precisam liderar reuniões, negociar, apresentar resultados e se comunicar com equipes, clientes ou parceiros brasileiros.",
        "hero_image": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=1920&q=80",
        "audience": "Executivos estrangeiros, expatriados, líderes regionais, investidores, consultores e profissionais globais com operação no Brasil.",
        "level": "A2 a C1",
        "frequency": "2 aulas ao vivo por semana",
        "duration": "Plano por agenda executiva",
        "summary": "Você pratica português de negócios, cultura corporativa brasileira, reuniões, negociação, apresentações e escrita profissional.",
        "pain_title": "Negócios no Brasil exigem língua e contexto",
        "pain_intro": "Além da gramática, executivos precisam entender tom, formalidade, ritmo de reunião e nuances culturais.",
        "pain_points": [
            "Participar de reuniões em português sem depender de tradução.",
            "Adaptar linguagem para equipes brasileiras.",
            "Negociar com clareza e diplomacia.",
            "Escrever mensagens e apresentações com tom profissional.",
        ],
        "outcomes": [
            "Conduzir conversas de negócio em português brasileiro.",
            "Apresentar dados, decisões e recomendações.",
            "Negociar prazos, escopo e alinhamentos.",
            "Ganhar repertório cultural para atuar no Brasil.",
        ],
        "modules": [
            {"title": "Reuniões", "text": "Abertura, pauta, alinhamento, decisões e follow-up."},
            {"title": "Apresentações", "text": "Resultados, indicadores, planos e perguntas."},
            {"title": "Negociação", "text": "Concordar, discordar, propor, conceder e encerrar."},
            {"title": "Escrita executiva", "text": "E-mails, mensagens, convites e resumos."},
            {"title": "Cultura empresarial", "text": "Formalidade, rapport, ritmo e relacionamento."},
            {"title": "Pronúncia", "text": "Clareza, ritmo e sons críticos do português brasileiro."},
        ],
        "format_items": [
            "Aulas ao vivo com simulações de rotina executiva.",
            "Conteúdo adaptado à indústria, cargo e agenda.",
            "Suporte em inglês quando necessário.",
            "Possibilidade de programa B2B para equipes.",
        ],
        "faqs": [
            {"q": "Is this course for foreigners?", "a": "Yes. It is designed for non-native Portuguese speakers working with Brazil."},
            {"q": "Can classes focus on my company context?", "a": "Yes. Meetings, presentations and vocabulary can be adapted to your role."},
            {"q": "Do you teach Brazilian business culture?", "a": "Yes. Cultural context is part of the communication training."},
            {"q": "Can this be offered to a team?", "a": "Yes, B2B formats can be discussed with the Vedium team."},
        ],
        "whatsapp_text": "Hello, I want Portuguese classes for executives with Vedium.",
    },
    "ingles-para-viagens": {
        "title": "Inglês para Viagens — Vedium",
        "short_title": "Inglês para Viagens",
        "meta_description": "Inglês para viagens com aulas ao vivo: aeroporto, hotel, restaurante, transporte, emergências e conversação prática.",
        "tagline": "Viagem com mais segurança",
        "h1": "Inglês prático para viajar com autonomia",
        "lead": "Treine situações reais de viagem antes de embarcar: aeroporto, imigração, hotel, transporte, restaurante, compras, emergências e conversas espontâneas.",
        "hero_image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1920&q=80",
        "audience": "Viajantes, intercambistas, famílias, profissionais em viagem de trabalho e pessoas que querem reduzir dependência de tradutor.",
        "level": "A1 a B1",
        "frequency": "1 ou 2 aulas ao vivo por semana",
        "duration": "Plano ajustado à data da viagem",
        "summary": "Você aprende frases úteis, escuta de instruções, vocabulário de viagem e respostas rápidas para situações comuns.",
        "pain_title": "Viagem exige resposta rápida",
        "pain_intro": "Na viagem, você não tem tempo para procurar cada palavra. O treino precisa ser prático, oral e focado em situações prováveis.",
        "pain_points": [
            "Medo de passar pela imigração sem entender perguntas.",
            "Dificuldade para pedir ajuda, comida, transporte ou informações.",
            "Insegurança para resolver problemas em hotel, voo ou bagagem.",
            "Dependência excessiva de aplicativo de tradução.",
        ],
        "outcomes": [
            "Responder perguntas comuns de imigração e check-in.",
            "Fazer pedidos, reservas e reclamações simples.",
            "Entender instruções de aeroporto, hotel e transporte.",
            "Ganhar confiança para conversar em situações curtas.",
        ],
        "modules": [
            {"title": "Aeroporto e imigração", "text": "Check-in, bagagem, embarque, perguntas e documentos."},
            {"title": "Hotel e hospedagem", "text": "Reserva, check-in, problemas no quarto e pedidos."},
            {"title": "Restaurantes", "text": "Cardápio, pedidos, restrições, conta e gorjeta."},
            {"title": "Transporte", "text": "Táxi, trem, metrô, mapas e direções."},
            {"title": "Emergências", "text": "Saúde, perda de documentos, compras e suporte."},
            {"title": "Conversas leves", "text": "Small talk, turismo, recomendações e interação social."},
        ],
        "format_items": [
            "Aulas ao vivo com simulações de viagem.",
            "Plano intensivo se a viagem estiver próxima.",
            "Vocabulário organizado por situação.",
            "Mensagens prontas para enviar no WhatsApp antes da matrícula.",
        ],
        "faqs": [
            {"q": "Serve para quem é iniciante?", "a": "Sim. A trilha é prática e pode começar em A1."},
            {"q": "Consigo estudar perto da viagem?", "a": "Sim. O plano pode priorizar situações essenciais."},
            {"q": "O foco é gramática?", "a": "O foco principal é comunicação prática, com gramática essencial quando necessário."},
            {"q": "Inclui imigração?", "a": "Sim. Perguntas comuns de imigração e respostas seguras fazem parte da trilha."},
        ],
        "whatsapp_text": "Olá, quero inglês para viagens na Vedium.",
    },
    "ingles-para-atendimento-ao-cliente": {
        "title": "Inglês para Atendimento ao Cliente — Vedium",
        "short_title": "Inglês para Atendimento",
        "meta_description": "Inglês para atendimento ao cliente, suporte, pós-venda e comunicação profissional com aulas online ao vivo.",
        "tagline": "Suporte e experiência do cliente",
        "h1": "Inglês para atender clientes internacionais com clareza",
        "lead": "Treine comunicação em inglês para suporte, CS, vendas, pós-venda e relacionamento com clientes. A trilha trabalha empatia, precisão, resolução de problemas e tom profissional.",
        "hero_image": "https://images.unsplash.com/photo-1556745757-8d76bdb6984b?w=1920&q=80",
        "audience": "Atendimento, suporte, customer success, vendas, recepção, hotelaria, turismo e empresas com clientes internacionais.",
        "level": "A2 a B2",
        "frequency": "1 ou 2 aulas ao vivo por semana",
        "duration": "Plano por função e setor",
        "summary": "Você pratica scripts flexíveis, escuta, respostas a objeções, linguagem de empatia, follow-up e resolução de conflitos.",
        "pain_title": "Atendimento em inglês precisa de tom e precisão",
        "pain_intro": "O cliente percebe quando a resposta é fria, confusa ou traduzida literalmente. O objetivo é ser claro, humano e eficiente.",
        "pain_points": [
            "Responder clientes sem parecer robótico.",
            "Explicar problemas técnicos ou comerciais com clareza.",
            "Lidar com reclamações, atrasos e objeções.",
            "Escrever mensagens de follow-up com tom profissional.",
        ],
        "outcomes": [
            "Abrir, conduzir e encerrar atendimentos em inglês.",
            "Usar linguagem de empatia e solução.",
            "Explicar processos, prazos e limitações com educação.",
            "Melhorar escrita de e-mails, chats e tickets.",
        ],
        "modules": [
            {"title": "Abertura de atendimento", "text": "Cumprimentos, identificação, motivo do contato e próximos passos."},
            {"title": "Empatia e tom", "text": "Como reconhecer frustração e responder com profissionalismo."},
            {"title": "Explicação de problemas", "text": "Causas, impactos, soluções, prazos e alternativas."},
            {"title": "Objeções e reclamações", "text": "Discordância, compensação, política e encaminhamento."},
            {"title": "Follow-up", "text": "E-mails, chats, tickets e mensagens de pós-atendimento."},
            {"title": "Simulações", "text": "Roleplays com cenários reais do seu setor."},
        ],
        "format_items": [
            "Aulas ao vivo com scripts adaptáveis.",
            "Vocabulário por setor e tipo de cliente.",
            "Prática de fala e escrita profissional.",
            "Possibilidade de treinamento B2B sob consulta.",
        ],
        "faqs": [
            {"q": "Serve para equipes?", "a": "Sim. A Vedium pode avaliar formato para grupos e empresas."},
            {"q": "Inclui chat e e-mail?", "a": "Sim. A trilha trabalha fala e escrita para canais de atendimento."},
            {"q": "É inglês técnico?", "a": "Depende do setor. O vocabulário pode ser adaptado ao produto ou serviço."},
            {"q": "Preciso ser fluente?", "a": "Não. A partir de A2 já é possível treinar atendimento estruturado."},
        ],
        "whatsapp_text": "Olá, quero inglês para atendimento ao cliente na Vedium.",
    },
    "ioruba-cultura-e-ancestralidade": {
        "title": "Iorubá, Cultura e Ancestralidade — Vedium",
        "short_title": "Iorubá e Cultura",
        "meta_description": "Aprenda iorubá online com contexto cultural, ancestralidade, saudações, pronúncia e prática guiada ao vivo.",
        "tagline": "Idioma com contexto",
        "h1": "Iorubá para aprender língua, memória e cultura",
        "lead": "Uma trilha para estudar iorubá com respeito ao idioma, à cultura e à ancestralidade. As aulas conectam pronúncia, vocabulário e contexto sem transformar o aprendizado em promessa simplista.",
        "hero_image": "https://images.unsplash.com/photo-1523805009345-7448845a9e53?w=1920&q=80",
        "audience": "Estudantes de cultura afro-diaspórica, iniciantes em iorubá, pesquisadores, artistas, educadores e pessoas em busca de reconexão cultural.",
        "level": "Iniciante a básico",
        "frequency": "1 ou 2 aulas ao vivo por semana",
        "duration": "Módulos por tema",
        "summary": "Você aprende língua em uso, pronúncia, saudações, expressões, vocabulário cultural e noções de contexto histórico e social.",
        "pain_title": "Cultura precisa de cuidado",
        "pain_intro": "Quando o idioma é separado do contexto, o aluno perde profundidade. Quando o contexto é tratado sem método, a aprendizagem fica confusa.",
        "pain_points": [
            "Querer aprender iorubá sem encontrar uma trilha séria.",
            "Ter dúvidas sobre pronúncia, tons e significados.",
            "Misturar referências culturais sem entender limites e usos.",
            "Precisar de professor para organizar estudo e prática.",
        ],
        "outcomes": [
            "Construir base linguística com respeito ao contexto.",
            "Entender saudações, expressões e vocabulário cultural.",
            "Praticar pronúncia e escuta com orientação.",
            "Seguir uma trilha de continuidade sem superficialidade.",
        ],
        "modules": [
            {"title": "Pronúncia e tons", "text": "Escuta, repetição guiada e atenção aos sons."},
            {"title": "Saudações e respeito", "text": "Formas de cumprimentar, responder e se apresentar."},
            {"title": "Família e comunidade", "text": "Vocabulário de relações, pertencimento e cotidiano."},
            {"title": "Expressões culturais", "text": "Palavras e usos com contexto educativo."},
            {"title": "História e diáspora", "text": "Conexões culturais apresentadas com cuidado e responsabilidade."},
            {"title": "Prática viva", "text": "Diálogos, leitura curta, escuta e feedback."},
        ],
        "format_items": [
            "Aulas ao vivo com prática e contextualização.",
            "Abordagem educativa, cultural e linguística.",
            "Conteúdo progressivo para iniciantes.",
            "Indicação de continuidade por objetivos.",
        ],
        "faqs": [
            {"q": "A trilha mistura idioma e cultura?", "a": "Sim, mas com foco educacional e sem prometer experiências fora do escopo de curso livre."},
            {"q": "Preciso saber iorubá antes?", "a": "Não. A trilha pode começar do zero."},
            {"q": "É indicado para educadores e artistas?", "a": "Sim, especialmente para quem busca repertório linguístico e cultural."},
            {"q": "Tem prática oral?", "a": "Sim. Pronúncia, escuta e fala são parte central da jornada."},
        ],
        "whatsapp_text": "Olá, quero iorubá com cultura e ancestralidade na Vedium.",
    },
    "preparatorio-celpe-bras": {
        "title": "Preparatório Celpe-Bras — Vedium",
        "short_title": "Preparatório Celpe-Bras",
        "meta_description": "Preparação para Celpe-Bras com português para estrangeiros, escrita, fala, compreensão e simulados orientados.",
        "tagline": "Português para certificação",
        "h1": "Preparação orientada para o Celpe-Bras",
        "lead": "Uma trilha para estrangeiros que precisam comprovar proficiência em português brasileiro. O foco é comunicação real, tarefas integradas, produção escrita, fala e interpretação.",
        "hero_image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1920&q=80",
        "audience": "Estrangeiros que pretendem prestar Celpe-Bras, estudantes internacionais, profissionais e pessoas que precisam comprovar português.",
        "level": "A2 a C1",
        "frequency": "2 aulas ao vivo por semana",
        "duration": "Plano conforme data da prova",
        "summary": "Você trabalha leitura, escuta, escrita, fala, repertório temático e simulados com feedback direcionado.",
        "pain_title": "Celpe-Bras avalia uso real da língua",
        "pain_intro": "Não basta memorizar gramática. O exame exige compreender textos, organizar ideias e responder a tarefas comunicativas.",
        "pain_points": [
            "Dificuldade para transformar leitura e áudio em resposta escrita.",
            "Falta de repertório para temas do Brasil e do cotidiano.",
            "Insegurança na interação oral.",
            "Textos sem organização, coesão ou adequação ao gênero pedido.",
        ],
        "outcomes": [
            "Entender melhor o formato e as tarefas do exame.",
            "Produzir textos com objetivo, organização e linguagem adequada.",
            "Responder oralmente com mais clareza e fluidez.",
            "Receber feedback sobre pontos prioritários antes da prova.",
        ],
        "modules": [
            {"title": "Diagnóstico", "text": "Mapeamento de nível, escrita, fala e prazo até a prova."},
            {"title": "Tarefas integradas", "text": "Leitura, áudio, interpretação e resposta comunicativa."},
            {"title": "Produção escrita", "text": "E-mail, carta, relato, opinião, solicitação e resumo."},
            {"title": "Interação oral", "text": "Perguntas, respostas, descrição, opinião e argumentação."},
            {"title": "Repertório brasileiro", "text": "Cultura, trabalho, educação, saúde, tecnologia e sociedade."},
            {"title": "Simulados", "text": "Prática orientada com feedback de desempenho."},
        ],
        "format_items": [
            "Aulas ao vivo com foco no exame.",
            "Plano ajustado ao nível e à data da prova.",
            "Correção de escrita e fala.",
            "Orientação para estudo entre as aulas.",
        ],
        "faqs": [
            {"q": "A Vedium aplica a prova Celpe-Bras?", "a": "Não. A Vedium oferece preparação; a inscrição e aplicação seguem os canais oficiais do exame."},
            {"q": "Preciso já falar português?", "a": "É recomendado ter base inicial. O diagnóstico indica a trilha adequada."},
            {"q": "Inclui simulado?", "a": "Sim, a preparação pode incluir tarefas simuladas e feedback."},
            {"q": "Can classes include English explanations?", "a": "Yes, when needed, but the goal is to increase Portuguese use progressively."},
        ],
        "whatsapp_text": "Olá, quero preparatório Celpe-Bras na Vedium.",
    },

    # =========================================================================
    # English landing pages (real, server-rendered) for international SEO.
    # Audiences for Yoruba (diaspora/heritage) and Portuguese-for-foreigners
    # are English-speaking, so these are native English pages — not auto-swaps.
    # =========================================================================
    "learn-yoruba-online": {
        "lang": "en",
        "alt": {"pt-BR": "curso-de-ioruba-online", "en": "learn-yoruba-online"},
        "title": "Learn Yoruba Online — Live Classes with Real Teachers | Vedium",
        "short_title": "Learn Yoruba Online",
        "meta_description": "Learn Yoruba online with live classes: pronunciation, tones, greetings, vocabulary and cultural context. A structured path for beginners and heritage learners.",
        "tagline": "Language and culture",
        "h1": "Learn Yoruba online with structure, pronunciation and real cultural context",
        "lead": "Vedium treats Yoruba as a journey of language, culture and belonging. Live classes combine speaking practice, essential vocabulary and respectful cultural context — guided by real teachers, at your own pace.",
        "hero_image": "https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=1920&q=80",
        "audience": "Heritage learners, the African diaspora, students of African culture, and anyone who wants to start Yoruba from scratch or reconnect with their roots.",
        "level": "Beginner to intermediate",
        "frequency": "1 or 2 live classes per week",
        "duration": "Progressive modules",
        "summary": "You learn sounds, tones, greetings, everyday vocabulary, essential phrases and cultural foundations — so you can study with respect and continuity.",
        "pain_title": "Yoruba needs listening, tone and guidance",
        "pain_intro": "Studying alone often leaves doubts about pronunciation and meaning. Live classes help you correct sounds, understand context and practice with confidence.",
        "pain_points": [
            "Hard to find an organized, trustworthy learning path.",
            "Uncertainty with tones, accents and pronunciation.",
            "Confusion between vocabulary, culture and real-world usage.",
            "No guidance to progress beyond word lists.",
        ],
        "outcomes": [
            "Pronounce greetings and first words more accurately.",
            "Build simple sentences for introductions and daily life.",
            "Understand vocabulary within its cultural context.",
            "Create a solid base to move on to intermediate modules.",
        ],
        "modules": [
            {"title": "Sounds and tones", "text": "Introduction to pronunciation, listening and key tonal differences."},
            {"title": "Greetings", "text": "Greetings, introductions and expressions of respect."},
            {"title": "Essential vocabulary", "text": "Family, body, home, routine, numbers and common objects."},
            {"title": "First sentences", "text": "Structures to ask, answer and form simple sentences."},
            {"title": "Culture in context", "text": "Social use of the language, meaning and cultural references handled with care."},
            {"title": "Speaking practice", "text": "Guided repetition, short dialogues and teacher feedback."},
        ],
        "format_items": [
            "Live online classes with pronunciation practice.",
            "A gradual path for absolute beginners.",
            "Cultural context — no religious or sensationalist claims.",
            "Guidance to continue through progressive modules.",
        ],
        "faqs": [
            {"q": "Do I need any prior knowledge?", "a": "No. The path can start from zero, focused on pronunciation and first vocabulary."},
            {"q": "Is the course religious?", "a": "It is educational and linguistic, with cultural context treated respectfully."},
            {"q": "Is there a certificate?", "a": "Yes, upon completion and according to the course requirements."},
            {"q": "How do I know where to start?", "a": "You can talk to our team and take a diagnostic assessment before enrolling."},
        ],
        "whatsapp_text": "Hello, I'd like to learn Yoruba online with Vedium.",
    },
    "learn-portuguese-brazil": {
        "lang": "en",
        "alt": {"pt-BR": "portugues-para-estrangeiros", "en": "learn-portuguese-brazil"},
        "title": "Learn Brazilian Portuguese Online — Classes for Foreigners | Vedium",
        "short_title": "Brazilian Portuguese for Foreigners",
        "meta_description": "Learn Brazilian Portuguese online with live classes for foreigners: real conversation, pronunciation, everyday vocabulary and culture to live, work and study in Brazil.",
        "tagline": "Portuguese for foreigners",
        "h1": "Brazilian Portuguese for foreigners, focused on real life in Brazil",
        "lead": "Live classes for foreigners who need to communicate in Portuguese at work, in their studies, with services, while traveling, or adapting to life in Brazil. English support is available whenever you need it.",
        "hero_image": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=1920&q=80",
        "audience": "Foreigners in Brazil, expats, international students, remote workers, and anyone who interacts with Brazilians.",
        "level": "A1 to B2",
        "frequency": "1 or 2 live classes per week",
        "duration": "Plan built around your adaptation goal",
        "summary": "You practice real conversations, pronunciation, listening, Brazilian vocabulary and everyday situations.",
        "pain_title": "Portuguese to live, not just to memorize",
        "pain_intro": "Brazilian Portuguese has a rhythm, expressions and cultural contexts that never show up in vocabulary lists.",
        "pain_points": [
            "Struggling to understand Brazilians speaking quickly.",
            "Feeling insecure at banks, appointments, meetings or services.",
            "Confusion with gender, verbs, prepositions and pronunciation.",
            "Lacking vocabulary for work and daily life.",
        ],
        "outcomes": [
            "Hold real conversations with more independence.",
            "Understand common instructions, questions and answers.",
            "Improve pronunciation and speaking rhythm.",
            "Gain vocabulary for work, housing and daily routine.",
        ],
        "modules": [
            {"title": "About me", "text": "Introductions, nationality, profession, family and interests."},
            {"title": "Daily life in Brazil", "text": "Shopping, transport, food, schedules and services."},
            {"title": "Portuguese at work", "text": "Meetings, messages, short presentations and check-ins."},
            {"title": "Practical grammar", "text": "Verbs, gender, number, questions and useful phrases."},
            {"title": "Culture and expressions", "text": "Natural usage, informality and Brazilian context."},
            {"title": "Conversation", "text": "Role-plays and real-time speaking correction."},
        ],
        "format_items": [
            "Live online classes in Portuguese with gradual support.",
            "English explanations whenever needed.",
            "A path by goal: life in Brazil, work, or exam prep.",
            "Optional Celpe-Bras preparation in a dedicated track.",
        ],
        "faqs": [
            {"q": "Can the classes include English support?", "a": "Yes. The teacher can use English support when needed, while progressively increasing Portuguese practice."},
            {"q": "Is it Brazilian Portuguese?", "a": "Yes. The focus is Portuguese as it is used in Brazil."},
            {"q": "Can I prepare for work situations?", "a": "Yes. We can include meetings, e-mails, presentations and daily professional vocabulary."},
            {"q": "Do I need a placement test?", "a": "The free test helps us estimate your level before recommending a path."},
        ],
        "whatsapp_text": "Hello, I want to learn Brazilian Portuguese for foreigners with Vedium.",
    },
}


# Prefixo de URL por idioma (pt-BR é a raiz; demais idiomas ganham /<lang>/).
LANG_URL_PREFIX = {
    "pt-BR": "",
    "en": "en/",
}

# Código hreflang correspondente a cada idioma do conteúdo.
LANG_HREFLANG = {
    "pt-BR": "pt-br",
    "en": "en",
}


def _landing_url(slug, lang):
    prefix = LANG_URL_PREFIX.get(lang, "")
    return f"{BASE_URL}/{prefix}{slug}"


def apply_landing_context(context, slug):
    landing = get_marketing_landing(slug)
    context.title = landing["title"]
    context.description = landing["meta_description"]
    context.landing = landing


def get_marketing_landing(slug):
    landing = dict(LANDINGS[slug])
    lang = landing.get("lang", "pt-BR")
    landing["slug"] = slug
    landing["lang"] = lang
    landing["lang_code"] = LANG_HREFLANG.get(lang, "pt-br")
    landing["url"] = _landing_url(slug, lang)
    landing["whatsapp_url"] = (
        f"https://wa.me/{WHATSAPP_PHONE}?text={quote(landing['whatsapp_text'])}"
    )

    # Versões alternativas em outros idiomas (hreflang). "alt" mapeia idioma -> slug.
    # Inclui a própria página + x-default (sempre o pt-BR quando existir).
    alt = landing.get("alt")
    alternates = []
    if alt:
        for alt_lang, alt_slug in alt.items():
            alternates.append({
                "hreflang": LANG_HREFLANG.get(alt_lang, alt_lang),
                "href": _landing_url(alt_slug, alt_lang),
            })
        x_default_slug = alt.get("pt-BR") or alt.get("en")
        if x_default_slug:
            x_default_lang = "pt-BR" if "pt-BR" in alt else "en"
            alternates.append({
                "hreflang": "x-default",
                "href": _landing_url(x_default_slug, x_default_lang),
            })
    landing["alternates"] = alternates
    return landing


get_landing_for_template = get_marketing_landing
