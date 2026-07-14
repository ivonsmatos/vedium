"""Conteúdo do blog da Vedium — posts ricos (SEO/GEO) renderizados pelo
template compartilhado templates/includes/blog_post.html.

Há DUAS fontes de posts, e ambas caem no mesmo template:
1. Este dict BLOG_POSTS — posts "de código" (SEO/GEO trabalhados a fundo,
   com várias seções), editados por nós via commit/deploy.
2. O doctype "Vedium Blog Post" — posts que QUALQUER pessoa com acesso ao
   Frappe Desk publica sozinha, em /app/vedium-blog-post, sem precisar de
   código nem de deploy. É o caminho recomendado para conteúdo novo.

Toda URL /blog/<slug> passa por www/blog_post.py, que procura primeiro no
doctype (post publicado pelo painel) e só then cai neste dict. O índice em
/blog (www/blog.py) lista os dois juntos, ordenados por data.

Convenção de conteúdo: corpo em HTML controlado por nós (parágrafos,
listas e tabelas), com no mínimo ~900 palavras por post, headings H2 e
um bloco de FAQs para rich snippet.
"""

BASE_URL = "https://vediums.com"
WHATSAPP_PHONE = "5511911293075"


BLOG_POSTS = {
    "alfabeto-ioruba": {
        "alt": {"pt-BR": "alfabeto-ioruba", "en": "yoruba-alphabet-guide"},
        "title": "Alfabeto iorubá: as 25 letras, vogais e tons (guia para iniciantes)",
        "meta_description": "Conheça o alfabeto iorubá completo: as 25 letras, as 7 vogais orais, as vogais nasais, os sons especiais como gb, p e ṣ, e os três tons do idioma.",
        "h1": "Alfabeto iorubá: as 25 letras, as vogais e os tons",
        "date": "2026-06-30",
        "date_display": "30 de junho de 2026",
        "hero_image": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1100&h=560&fit=crop&q=80",
        "hero_alt": "Estudo do alfabeto iorubá na Vedium",
        "tag": "Iorubá",
        "lead": "O alfabeto iorubá é o ponto de partida de quem quer aprender o idioma. Ele tem 25 letras, sons que não existem em português e um sistema de três tons que muda o significado das palavras. Neste guia, você entende a estrutura do alfabeto, as vogais orais e nasais, os sons especiais e por que a pronúncia precisa ser treinada com áudio.",
        "sections": [
            {
                "heading": "Quantas letras tem o alfabeto iorubá?",
                "body": [
                    "<p>O alfabeto iorubá moderno, padronizado a partir do trabalho do bispo Samuel Ajayi Crowther no século XIX, tem <strong>25 letras</strong>. Ele usa o mesmo alfabeto latino do português, mas com diferenças importantes: algumas letras têm um <strong>ponto subscrito</strong> (como ẹ, ọ e ṣ), que indica um som diferente, e várias letras do português simplesmente não existem.</p>",
                    "<p>As 25 letras são: <strong>a, b, d, e, ẹ, f, g, gb, h, i, j, k, l, m, n, o, ọ, p, r, s, ṣ, t, u, w, y</strong>. Repare que <strong>c, q, v, x e z não fazem parte</strong> do iorubá, e que <em>gb</em> é tratado como uma única letra, com um som próprio.</p>",
                ],
            },
            {
                "heading": "As 7 vogais orais do iorubá",
                "body": [
                    "<p>O iorubá tem <strong>sete vogais orais</strong>, duas a mais que o português escrito. A diferença está nas vogais médias, que se dividem em abertas e fechadas:</p>",
                    "<ul>"
                    "<li><strong>a</strong> — como em \"casa\";</li>"
                    "<li><strong>e</strong> — fechado, como em \"você\";</li>"
                    "<li><strong>ẹ</strong> (e com ponto) — aberto, como o \"é\" de \"pé\";</li>"
                    "<li><strong>i</strong> — como em \"vida\";</li>"
                    "<li><strong>o</strong> — fechado, como em \"avô\";</li>"
                    "<li><strong>ọ</strong> (o com ponto) — aberto, como o \"ó\" de \"avó\";</li>"
                    "<li><strong>u</strong> — como em \"luz\".</li>"
                    "</ul>",
                    "<p>O ponto embaixo do <strong>ẹ</strong> e do <strong>ọ</strong> é essencial: ele indica um som mais aberto e pode mudar completamente a palavra. Confundir <em>e</em> com <em>ẹ</em> é um dos primeiros pontos que um professor corrige nas aulas.</p>",
                ],
            },
            {
                "heading": "Vogais nasais",
                "body": [
                    "<p>Além das vogais orais, o iorubá tem <strong>vogais nasais</strong> — sons em que o ar passa pelo nariz, parecidos com o que acontece em palavras portuguesas como \"sim\" e \"bom\". Na escrita, costumam aparecer seguidas de <strong>n</strong>, como em <em>an</em>, <em>ẹn</em>, <em>in</em>, <em>ọn</em> e <em>un</em>.</p>",
                    "<p>Para o ouvido brasileiro, as vogais nasais são mais fáceis do que para falantes de inglês, justamente porque o português já tem nasalização. Ainda assim, a posição exata da nasal em iorubá precisa ser ouvida e repetida para soar natural.</p>",
                ],
            },
            {
                "heading": "Sons especiais: gb, p e ṣ",
                "body": [
                    "<p>Três sons costumam surpreender quem começa:</p>",
                    "<ul>"
                    "<li><strong>gb</strong> — um som único, produzido com os dois lábios e a parte de trás da língua ao mesmo tempo. Não existe equivalente direto em português e precisa ser demonstrado;</li>"
                    "<li><strong>p</strong> — em iorubá, a letra <em>p</em> sozinha soa como <strong>\"kp\"</strong>, e não como o \"p\" do português;</li>"
                    "<li><strong>ṣ</strong> (s com ponto) — tem o som de <strong>\"x\"</strong>/\"sh\", como em \"chave\".</li>"
                    "</ul>",
                    "<p>Esses três sons são um bom exemplo de por que aprender iorubá só por listas escritas é arriscado: a letra não corresponde ao som que um falante de português esperaria.</p>",
                ],
            },
            {
                "heading": "Os três tons do iorubá",
                "body": [
                    "<p>Esta é a característica que mais diferencia o iorubá das línguas europeias: ele é uma <strong>língua tonal</strong>, com três tons que mudam o significado da palavra. São eles:</p>",
                    "<ul>"
                    "<li><strong>tom alto</strong> — marcado com acento agudo (´);</li>"
                    "<li><strong>tom médio</strong> — sem acento;</li>"
                    "<li><strong>tom baixo</strong> — marcado com acento grave (`).</li>"
                    "</ul>",
                    "<p>Na prática, isso significa que a mesma sequência de letras pode ter sentidos completamente diferentes dependendo do tom. Um exemplo clássico é a sílaba <em>ọkọ</em>, que muda de significado conforme a combinação de tons — podendo se referir a coisas tão distintas quanto \"marido\", \"enxada\" ou \"veículo\". É por isso que treinar tom desde o início, ouvindo e repetindo, é indispensável.</p>",
                    "<p>Para um falante de português, que nunca usou o tom para mudar o significado de uma palavra, esse é o conceito mais novo do iorubá — e também o mais recompensador de dominar. A boa notícia é que o ouvido se acostuma com a prática: depois de algumas semanas escutando e repetindo, o cérebro começa a perceber as diferenças que no início pareciam invisíveis. Na escrita digital, vale lembrar de usar os acentos e os pontos subscritos sempre que possível, porque eles carregam informação real sobre o som.</p>",
                ],
            },
            {
                "heading": "Como treinar a pronúncia do iorubá",
                "body": [
                    "<p>O alfabeto iorubá é totalmente aprendível por iniciantes — mas a parte que faz a diferença (tons, vogais abertas e fechadas, sons como <em>gb</em> e <em>p</em>) depende de <strong>ouvir e ser corrigido</strong>. Um aplicativo mostra a letra; ele não percebe quando você produziu o tom errado. Por isso, a forma mais segura de começar é com áudio e prática guiada.</p>",
                    "<p>Na Vedium, o iorubá é ensinado em <a href=\"/curso-de-ioruba-online\">aulas ao vivo, do zero ao avançado</a>, começando exatamente por sons e tons, com correção em tempo real. Depois do alfabeto, os próximos passos naturais são as <a href=\"/blog/saudacoes-em-ioruba\">saudações em iorubá</a> e os <a href=\"/blog/numeros-em-ioruba\">números em iorubá</a>.</p>",
                ],
            },
        ],
        "faqs": [
            {"q": "Quantas letras tem o alfabeto iorubá?", "a": "São 25 letras: a, b, d, e, ẹ, f, g, gb, h, i, j, k, l, m, n, o, ọ, p, r, s, ṣ, t, u, w, y. As letras c, q, v, x e z não existem no iorubá."},
            {"q": "Quantas vogais o iorubá tem?", "a": "Sete vogais orais (a, e, ẹ, i, o, ọ, u) mais as vogais nasais. As versões com ponto (ẹ, ọ) têm som mais aberto."},
            {"q": "O iorubá é difícil de pronunciar?", "a": "O maior desafio é o sistema de três tons (alto, médio e baixo), que muda o significado das palavras, além de sons como gb e o p (pronunciado kp). Com áudio e correção ao vivo, a pronúncia é totalmente aprendível."},
            {"q": "Dá para aprender o alfabeto iorubá sozinho?", "a": "Você consegue memorizar as letras, mas os tons e os sons especiais precisam ser ouvidos e treinados com um professor para não fixar uma pronúncia incorreta."},
        ],
        "cta_title": "Quer aprender iorubá com pronúncia correta desde o início?",
        "cta_text": "Na Vedium, o iorubá é ensinado em aulas ao vivo, do zero ao avançado, com foco em tons e conversação.",
        "cta_label": "Conhecer o curso de iorubá",
        "cta_url": "/curso-de-ioruba-online",
    },
    "saudacoes-em-ioruba": {
        "alt": {"pt-BR": "saudacoes-em-ioruba", "en": "yoruba-greetings"},
        "title": "Saudações em iorubá: como cumprimentar (bom dia, obrigado e mais)",
        "meta_description": "Aprenda as principais saudações em iorubá: bom dia, boa tarde, boa noite, como vai, obrigado e bem-vindo, com a forma respeitosa e a informal.",
        "h1": "Saudações em iorubá: bom dia, obrigado e os cumprimentos do dia a dia",
        "date": "2026-06-30",
        "date_display": "30 de junho de 2026",
        "hero_image": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1100&h=560&fit=crop&q=80",
        "hero_alt": "Pessoas se cumprimentando — saudações em iorubá",
        "tag": "Iorubá",
        "lead": "Na cultura iorubá, cumprimentar bem é mais do que educação: é um sinal de respeito, especialmente com pessoas mais velhas. Este guia reúne as saudações essenciais — bom dia, boa tarde, boa noite, como vai, obrigado e bem-vindo — e explica a diferença entre a forma respeitosa e a informal, que muda o jeito de falar.",
        "sections": [
            {
                "heading": "Por que as saudações são tão importantes no iorubá",
                "body": [
                    "<p>Entre os iorubás, a saudação ocupa um lugar central na convivência. Existem cumprimentos específicos para quase toda situação — para quem está trabalhando, comendo, voltando de viagem ou realizando uma tarefa. Cumprimentar de forma adequada demonstra <strong>respeito e boa educação</strong>, e deixar de fazê-lo pode soar frio.</p>",
                    "<p>Um detalhe muda tudo logo de início: o iorubá distingue a forma <strong>respeitosa/plural</strong> da <strong>informal/singular</strong>. A maioria das saudações começa com <strong>\"Ẹ\"</strong> quando você fala com alguém mais velho, com uma autoridade ou com mais de uma pessoa. Com amigos e pessoas da mesma idade, usa-se <strong>\"O\"</strong> ou simplesmente a forma curta.</p>",
                ],
            },
            {
                "heading": "Bom dia, boa tarde e boa noite em iorubá",
                "body": [
                    "<p>As saudações ligadas ao período do dia são as primeiras que todo iniciante aprende:</p>",
                    "<ul>"
                    "<li><strong>Ẹ kàárọ̀</strong> — bom dia (de manhã);</li>"
                    "<li><strong>Ẹ kàásàn</strong> — boa tarde;</li>"
                    "<li><strong>Ẹ kúùrọ̀lẹ́</strong> — boa tarde/noitinha (fim de tarde);</li>"
                    "<li><strong>Ẹ kúalẹ́</strong> — boa noite (à noite).</li>"
                    "</ul>",
                    "<p>Com amigos, você pode usar as mesmas expressões trocando o <em>Ẹ</em> respeitoso pela forma informal. Para se despedir à noite, no sentido de \"até amanhã\", usa-se <strong>O dàárọ̀</strong>. Como o iorubá é uma língua tonal, os acentos sobre as palavras marcam o tom — e o tom certo faz parte da saudação soar natural.</p>",
                ],
            },
            {
                "heading": "Como vai? Perguntando como a pessoa está",
                "body": [
                    "<p>Depois do cumprimento inicial, vem a pergunta sobre como a pessoa está:</p>",
                    "<ul>"
                    "<li><strong>Báwo ni?</strong> — como vai? / tudo bem?;</li>"
                    "<li><strong>Ṣé àlàáfíà ni?</strong> — está tudo em paz/bem?;</li>"
                    "<li><strong>Ṣé dáadáa ni?</strong> — está tudo bem?</li>"
                    "</ul>",
                    "<p>Uma resposta comum e positiva é <strong>Mo wà dáadáa</strong> (\"estou bem\") ou simplesmente <strong>Àlàáfíà</strong> (\"paz\", no sentido de \"tudo em paz\"). A palavra <em>àlàáfíà</em>, aliás, aparece bastante: ela carrega a ideia de bem-estar e tranquilidade, e é usada tanto para cumprimentar quanto para responder.</p>",
                ],
            },
            {
                "heading": "Obrigado, bem-vindo e até logo",
                "body": [
                    "<p>Estas três expressões completam o kit básico de cortesia:</p>",
                    "<ul>"
                    "<li><strong>Ẹ ṣé</strong> — obrigado (respeitoso); com amigos, <strong>O ṣé</strong>;</li>"
                    "<li><strong>Ẹ káàbọ̀</strong> — bem-vindo(a);</li>"
                    "<li><strong>Ó dàbọ̀</strong> — adeus / até logo.</li>"
                    "</ul>",
                    "<p>Há ainda saudações situacionais muito usadas, como <strong>Ẹ kú iṣẹ́</strong>, dita a quem está trabalhando, e variações para quem está realizando alguma atividade. Esse repertório de cumprimentos \"para cada ocasião\" é uma das marcas mais bonitas da língua — e mostra como o iorubá e a cultura andam juntos.</p>",
                ],
            },
            {
                "heading": "Cumprimentar quem é mais velho: um gesto de respeito",
                "body": [
                    "<p>Na cultura iorubá, a forma de cumprimentar pessoas mais velhas vai além das palavras. Tradicionalmente, ao saudar um mais velho, os <strong>meninos e homens fazem o <em>ìdọ̀bálẹ̀</em></strong> (uma reverência inclinando-se ou deitando-se levemente), enquanto as <strong>meninas e mulheres fazem o <em>ìkúnlẹ̀</em></strong> (ajoelhar-se levemente). Em contextos urbanos e do dia a dia, esse gesto costuma ser simbólico — uma leve inclinação do corpo —, mas a intenção de respeito permanece muito presente.</p>",
                    "<p>É por isso que a forma respeitosa com <strong>\"Ẹ\"</strong> importa tanto: usar o cumprimento certo com a pessoa certa demonstra que você entende não só a língua, mas também a cortesia iorubá. Tratar um mais velho pela forma informal pode soar como falta de educação, mesmo que a frase esteja \"correta\" gramaticalmente. Esse é um dos pontos em que aprender com um professor faz diferença: ele ensina não apenas o que dizer, mas <strong>com quem e como</strong> dizer.</p>",
                ],
            },
            {
                "heading": "Treinando as saudações com a pronúncia certa",
                "body": [
                    "<p>Você pode memorizar a lista acima hoje mesmo, mas a parte que faz a saudação soar natural — o <strong>tom</strong> e a diferença entre vogais abertas e fechadas — só se ganha ouvindo e repetindo. Antes das saudações, vale entender o <a href=\"/blog/alfabeto-ioruba\">alfabeto iorubá e seus tons</a>; depois, um bom próximo passo são os <a href=\"/blog/numeros-em-ioruba\">números em iorubá</a>.</p>",
                    "<p>Na Vedium, as saudações entram já nas primeiras aulas de <a href=\"/curso-de-ioruba-online\">iorubá ao vivo</a>, com o professor corrigindo a pronúncia e o tom em tempo real — do jeito que se aprende a cumprimentar de verdade.</p>",
                ],
            },
        ],
        "faqs": [
            {"q": "Como se diz bom dia em iorubá?", "a": "Bom dia é \"Ẹ kàárọ̀\" na forma respeitosa (com pessoas mais velhas ou em grupo). Com amigos, usa-se a forma informal."},
            {"q": "Como se diz obrigado em iorubá?", "a": "\"Ẹ ṣé\" na forma respeitosa e \"O ṣé\" na forma informal, com amigos e pessoas da mesma idade."},
            {"q": "Qual a diferença entre Ẹ e O nas saudações?", "a": "\"Ẹ\" é a forma respeitosa e plural, usada com pessoas mais velhas, autoridades ou mais de uma pessoa. \"O\" é a forma informal, usada com amigos e pessoas da mesma idade."},
            {"q": "Preciso acertar o tom das saudações?", "a": "Sim. O iorubá é uma língua tonal, e o tom faz parte da palavra. Por isso vale treinar as saudações com áudio e correção ao vivo, e não só pela escrita."},
        ],
        "cta_title": "Quer aprender a cumprimentar (e conversar) em iorubá?",
        "cta_text": "As aulas ao vivo da Vedium começam pelas saudações e pela pronúncia correta, com professor especializado.",
        "cta_label": "Conhecer o curso de iorubá",
        "cta_url": "/curso-de-ioruba-online",
    },
    "numeros-em-ioruba": {
        "alt": {"pt-BR": "numeros-em-ioruba", "en": "yoruba-numbers-1-to-20"},
        "title": "Números em iorubá de 1 a 20: como contar (e a lógica de base 20)",
        "meta_description": "Aprenda os números em iorubá de 1 a 20, com a pronúncia aproximada e a curiosa lógica vigesimal (base 20) que usa subtração para formar 15 a 19.",
        "h1": "Números em iorubá de 1 a 20",
        "date": "2026-06-30",
        "date_display": "30 de junho de 2026",
        "hero_image": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80",
        "hero_alt": "Aprender a contar — números em iorubá",
        "tag": "Iorubá",
        "lead": "Contar em iorubá é mais interessante do que parece. O idioma usa um sistema vigesimal — de base 20 — e, a partir do 15, forma os números por subtração. Neste guia você aprende os números de 1 a 20, entende essa lógica e descobre por que a pronúncia precisa de prática.",
        "sections": [
            {
                "heading": "Números em iorubá de 1 a 10",
                "body": [
                    "<p>A base de tudo são os dez primeiros números. Eles são a parte mais direta de aprender:</p>",
                    "<ul>"
                    "<li>1 — <strong>ọ̀kan</strong></li>"
                    "<li>2 — <strong>èjì</strong></li>"
                    "<li>3 — <strong>ẹ̀ta</strong></li>"
                    "<li>4 — <strong>ẹ̀rin</strong></li>"
                    "<li>5 — <strong>àrún</strong></li>"
                    "<li>6 — <strong>ẹ̀fà</strong></li>"
                    "<li>7 — <strong>èje</strong></li>"
                    "<li>8 — <strong>ẹ̀jọ</strong></li>"
                    "<li>9 — <strong>ẹ̀sán</strong></li>"
                    "<li>10 — <strong>ẹ̀wá</strong></li>"
                    "</ul>",
                    "<p>Vale repetir um alerta importante: os acentos não são enfeite. O iorubá é tonal, e o acento marca o tom de cada sílaba. Por isso, a grafia acima serve de guia, mas a pronúncia precisa ser ouvida para sair natural.</p>",
                ],
            },
            {
                "heading": "Números de 11 a 14",
                "body": [
                    "<p>De 11 a 14, o iorubá soma sobre o dez, com um sufixo que significa \"a mais\" (relacionado a <em>-lá</em>):</p>",
                    "<ul>"
                    "<li>11 — <strong>ọ̀kànlá</strong> (dez e um)</li>"
                    "<li>12 — <strong>èjìlá</strong> (dez e dois)</li>"
                    "<li>13 — <strong>ẹ̀talá</strong> (dez e três)</li>"
                    "<li>14 — <strong>ẹ̀rìnlá</strong> (dez e quatro)</li>"
                    "</ul>",
                    "<p>Repare que você reconhece o número de base (èjì, ẹ̀ta, ẹ̀rin) dentro da palavra. Essa lógica de \"montar\" números a partir das raízes é o que torna o sistema iorubá organizado, mesmo sendo diferente do nosso.</p>",
                ],
            },
            {
                "heading": "Números de 15 a 20: a lógica da subtração",
                "body": [
                    "<p>Aqui está a parte mais curiosa. A partir do 15, o iorubá tende a formar os números <strong>subtraindo a partir do vinte</strong>, em vez de somar a partir do dez. A palavra <em>dín</em> traz a ideia de \"menos\":</p>",
                    "<ul>"
                    "<li>15 — <strong>ẹ̀ẹ́dógún</strong> (vinte menos cinco)</li>"
                    "<li>16 — <strong>ẹ̀rìndínlógún</strong> (vinte menos quatro)</li>"
                    "<li>17 — <strong>ẹ̀tàdínlógún</strong> (vinte menos três)</li>"
                    "<li>18 — <strong>èjìdínlógún</strong> (vinte menos dois)</li>"
                    "<li>19 — <strong>ọ̀kàndínlógún</strong> (vinte menos um)</li>"
                    "<li>20 — <strong>ogún</strong></li>"
                    "</ul>",
                    "<p>Ou seja, em vez de dizer \"dez e nove\" para 19, o iorubá diz algo como \"vinte menos um\". Esse é o coração do <strong>sistema vigesimal (base 20)</strong>, que organiza a contagem tradicional iorubá em torno de múltiplos de vinte.</p>",
                ],
            },
            {
                "heading": "Por que o iorubá conta de 20 em 20",
                "body": [
                    "<p>Muitas culturas desenvolveram sistemas de contagem ligados ao corpo e ao comércio. O sistema vigesimal iorubá é um dos mais elaborados do mundo: números maiores são construídos a partir de vinte, com somas e subtrações encadeadas. Isso explica por que aprender a contar em iorubá é também uma pequena aula de <strong>raciocínio e cultura</strong>, não apenas de vocabulário.</p>",
                    "<p>Para o dia a dia, os números de 1 a 20 já cobrem muitas situações — idade, quantidades, horários e preços simples. À medida que você avança, o professor mostra como os múltiplos de dez e de vinte se combinam para formar números maiores.</p>",
                ],
            },
            {
                "heading": "Os múltiplos de dez: 10, 20, 30 e 40",
                "body": [
                    "<p>Depois do 20, a lógica de base 20 fica ainda mais visível nos múltiplos de dez. Vale conhecer os principais:</p>",
                    "<ul>"
                    "<li>10 — <strong>ẹ̀wá</strong></li>"
                    "<li>20 — <strong>ogún</strong></li>"
                    "<li>30 — <strong>ọgbọ̀n</strong></li>"
                    "<li>40 — <strong>ogójì</strong> (literalmente \"dois vintes\", ou seja, 2 × 20)</li>"
                    "</ul>",
                    "<p>Repare em algo interessante: enquanto o 30 (<em>ọgbọ̀n</em>) tem uma palavra própria, o 40 já é construído como <strong>\"dois vintes\"</strong>. A partir daí, os múltiplos maiores continuam girando em torno do vinte — 60 são \"três vintes\", e assim por diante. Esse encadeamento é o que dá ao sistema iorubá sua fama de engenhoso: com poucas raízes e duas operações (somar e subtrair), constrói-se toda a contagem.</p>",
                    "<p>Para quem está começando, não é preciso dominar tudo de uma vez. Os números de 1 a 20 já resolvem a maior parte das situações do dia a dia, e os múltiplos de dez entram naturalmente conforme você avança.</p>",
                ],
            },
            {
                "heading": "Como praticar os números em iorubá",
                "body": [
                    "<p>Memorizar a lista é o primeiro passo; usar os números em frases (\"tenho X anos\", \"quero X\") é o que fixa de verdade. E, como sempre no iorubá, o <strong>tom</strong> precisa de treino com áudio. Se você ainda não viu, comece pelo <a href=\"/blog/alfabeto-ioruba\">alfabeto iorubá</a> e pelas <a href=\"/blog/saudacoes-em-ioruba\">saudações em iorubá</a>.</p>",
                    "<p>Na Vedium, os números entram nas primeiras aulas de <a href=\"/curso-de-ioruba-online\">iorubá ao vivo</a>, com prática de pronúncia e uso em situações reais — do jeito que se aprende a contar e a conversar.</p>",
                ],
            },
        ],
        "faqs": [
            {"q": "Como se conta de 1 a 5 em iorubá?", "a": "1 é ọ̀kan, 2 èjì, 3 ẹ̀ta, 4 ẹ̀rin e 5 àrún. Os acentos marcam os tons, que fazem parte da pronúncia correta."},
            {"q": "Por que o iorubá usa base 20?", "a": "O iorubá tem um sistema de contagem vigesimal (base 20), em que números maiores são formados a partir de múltiplos de vinte, com somas e subtrações. Por isso, de 15 a 19, a contagem costuma ser feita por subtração a partir do vinte."},
            {"q": "Como se diz 20 em iorubá?", "a": "Vinte é \"ogún\". Números como 19 são formados como \"vinte menos um\" (ọ̀kàndínlógún), o que mostra a lógica de base 20."},
            {"q": "Os números em iorubá são difíceis?", "a": "Os números de 1 a 14 seguem um padrão direto. De 15 a 19, a lógica de subtração exige um pouco mais de atenção. Com prática e áudio, todos são aprendíveis por iniciantes."},
        ],
        "cta_title": "Quer aprender a contar e conversar em iorubá?",
        "cta_text": "Nas aulas ao vivo da Vedium, os números e a pronúncia são treinados desde o início, com professor especializado.",
        "cta_label": "Conhecer o curso de iorubá",
        "cta_url": "/curso-de-ioruba-online",
    },
    # --- Posts migrados de HTML standalone (2026-06-02) para este dict, sem
    # reescrever o texto original — só reorganizados no formato de seções. ---
    "aprender-ioruba-lingua-e-cultura": {
        "alt": {"pt-BR": "aprender-ioruba-lingua-e-cultura", "en": "yoruba-language-and-culture"},
        "title": "Iorubá: conheça o idioma e por que aprendê-lo",
        "meta_description": "O iorubá é falado por milhões na África Ocidental e tem forte presença na cultura brasileira. Conheça o idioma.",
        "h1": "Iorubá: conheça o idioma e por que aprendê-lo",
        "date": "2026-06-02",
        "date_display": "2 de junho de 2026",
        "hero_image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1100&h=560&fit=crop&q=80",
        "hero_alt": "Aula de Iorubá: língua e cultura na Vedium",
        "tag": "Iorubá",
        "lead": "O iorubá é uma das línguas mais faladas da África Ocidental, com milhões de falantes na Nigéria, no Benim e no Togo, além de uma grande comunidade na diáspora — inclusive no Brasil. É um idioma vivo, com tom, ritmo e uma cultura riquíssima por trás.",
        "sections": [
            {
                "heading": "Uma língua ligada ao Brasil",
                "body": [
                    "<p>A presença iorubá é forte na história e na cultura brasileiras, especialmente na música, na culinária e nas tradições de matriz africana. Aprender o idioma é também uma forma de se reconectar com essa herança e entendê-la na fonte.</p>",
                ],
            },
            {
                "heading": "Por que estudar iorubá",
                "body": [
                    "<ul>"
                    "<li>Reconexão com raízes culturais e religiosas;</li>"
                    "<li>Acesso a músicas, provérbios e literatura no original;</li>"
                    "<li>Comunicação com falantes na África e na diáspora;</li>"
                    "<li>Um diferencial cultural e acadêmico.</li>"
                    "</ul>",
                ],
            },
            {
                "heading": "Como é o curso na Vedium",
                "body": [
                    "<p>Na Vedium, o iorubá é ensinado em <strong>aulas ao vivo</strong>, do básico ao avançado, com o professor Busayo Frank Alonge. As aulas trazem o idioma e a cultura de forma viva e acessível, com foco em você falar de verdade.</p>",
                ],
            },
        ],
        "faqs": [],
        "cta_title": "Quer aprender iorubá do zero?",
        "cta_text": "Conheça as aulas ao vivo de iorubá, com foco em cultura e conversação real.",
        "cta_label": "Conhecer o curso de Iorubá",
        "cta_url": "/curso-de-ioruba-online",
    },

    # =========================================================================
    # English posts (real, server-rendered) — traduções dos 4 posts do
    # cluster Iorubá acima. Público: diáspora / fora do Brasil, não fala PT.
    # Mesma URL flat /blog/<slug>, distinguidos pelo slug em inglês + "lang".
    # =========================================================================
    "yoruba-alphabet-guide": {
        "lang": "en",
        "alt": {"pt-BR": "alfabeto-ioruba", "en": "yoruba-alphabet-guide"},
        "title": "Yoruba alphabet: the 25 letters, vowels and tones (a beginner's guide)",
        "meta_description": "Learn the full Yoruba alphabet: the 25 letters, the 7 oral vowels, nasal vowels, special sounds like gb, p and ṣ, and the three tones of the language.",
        "h1": "Yoruba alphabet: the 25 letters, the vowels and the tones",
        "date": "2026-07-02",
        "date_display": "July 2, 2026",
        "hero_image": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1100&h=560&fit=crop&q=80",
        "hero_alt": "Studying the Yoruba alphabet with Vedium",
        "tag": "Yoruba",
        "lead": "The Yoruba alphabet is where anyone learning the language starts. It has 25 letters, sounds that don't exist in English, and a three-tone system that changes the meaning of words. In this guide, you'll learn the structure of the alphabet, the oral and nasal vowels, the special sounds, and why pronunciation needs to be trained with audio.",
        "sections": [
            {
                "heading": "How many letters does the Yoruba alphabet have?",
                "body": [
                    "<p>The modern Yoruba alphabet, standardized from the 19th-century work of Bishop Samuel Ajayi Crowther, has <strong>25 letters</strong>. It uses the same Latin alphabet as English, but with important differences: some letters carry a <strong>subdot</strong> (like ẹ, ọ and ṣ), which marks a different sound, and several letters common in English simply don't exist.</p>",
                    "<p>The 25 letters are: <strong>a, b, d, e, ẹ, f, g, gb, h, i, j, k, l, m, n, o, ọ, p, r, s, ṣ, t, u, w, y</strong>. Notice that <strong>c, q, v, x and z are not part of</strong> Yoruba, and that <em>gb</em> is treated as a single letter, with its own sound.</p>",
                ],
            },
            {
                "heading": "The 7 oral vowels of Yoruba",
                "body": [
                    "<p>Yoruba has <strong>seven oral vowels</strong>, two more than written English typically distinguishes. The difference lies in the mid vowels, which split into open and closed:</p>",
                    "<ul>"
                    "<li><strong>a</strong> — as in \"father\";</li>"
                    "<li><strong>e</strong> — closed, similar to the \"e\" in \"café\";</li>"
                    "<li><strong>ẹ</strong> (e with a subdot) — open, closer to the \"e\" in \"bed\";</li>"
                    "<li><strong>i</strong> — as in \"machine\";</li>"
                    "<li><strong>o</strong> — closed, similar to the \"o\" in \"go\";</li>"
                    "<li><strong>ọ</strong> (o with a subdot) — open, closer to the \"o\" in \"law\";</li>"
                    "<li><strong>u</strong> — as in \"flute\".</li>"
                    "</ul>",
                    "<p>The dot under <strong>ẹ</strong> and <strong>ọ</strong> is essential: it marks a more open sound and can completely change a word's meaning. Confusing <em>e</em> with <em>ẹ</em> is one of the first things a teacher corrects in class.</p>",
                ],
            },
            {
                "heading": "Nasal vowels",
                "body": [
                    "<p>Besides the oral vowels, Yoruba has <strong>nasal vowels</strong> — sounds where air passes through the nose, somewhat like the nasalized vowels found in French. In writing, they're usually followed by <strong>n</strong>, as in <em>an</em>, <em>ẹn</em>, <em>in</em>, <em>ọn</em> and <em>un</em>.</p>",
                    "<p>For English speakers, nasal vowels can take a bit more practice than for speakers of languages with built-in nasalization. Even so, the exact placement of the nasal sound in Yoruba needs to be heard and repeated to sound natural.</p>",
                ],
            },
            {
                "heading": "Special sounds: gb, p and ṣ",
                "body": [
                    "<p>Three sounds tend to surprise beginners:</p>",
                    "<ul>"
                    "<li><strong>gb</strong> — a unique sound, produced with both lips and the back of the tongue at the same time. There's no direct equivalent in English, and it needs to be demonstrated;</li>"
                    "<li><strong>p</strong> — in Yoruba, the letter <em>p</em> on its own sounds like <strong>\"kp\"</strong>, not like the English \"p\";</li>"
                    "<li><strong>ṣ</strong> (s with a subdot) — has the sound of <strong>\"sh\"</strong>, as in \"shoe\".</li>"
                    "</ul>",
                    "<p>These three sounds are a good example of why learning Yoruba from written word lists alone is risky: the letter doesn't correspond to the sound an English speaker would expect.</p>",
                ],
            },
            {
                "heading": "The three tones of Yoruba",
                "body": [
                    "<p>This is the feature that sets Yoruba apart the most from English: it's a <strong>tonal language</strong>, with three tones that change the meaning of a word. They are:</p>",
                    "<ul>"
                    "<li><strong>high tone</strong> — marked with an acute accent (´);</li>"
                    "<li><strong>mid tone</strong> — unmarked;</li>"
                    "<li><strong>low tone</strong> — marked with a grave accent (`).</li>"
                    "</ul>",
                    "<p>In practice, this means the same sequence of letters can carry completely different meanings depending on the tone. A classic example is the syllable <em>ọkọ</em>, which changes meaning depending on the tone pattern — it can refer to things as different as \"husband,\" \"hoe,\" or \"vehicle.\" That's why training tone from the very start, by listening and repeating, is essential.</p>",
                    "<p>For an English speaker, who has never used tone to change a word's meaning, this is the newest concept in Yoruba — and also the most rewarding to master. The good news is that your ear adjusts with practice: after a few weeks of listening and repeating, your brain starts to notice differences that seemed invisible at first. When typing in Yoruba, remember to use the accents and subdots whenever you can, since they carry real information about the sound.</p>",
                ],
            },
            {
                "heading": "How to train your Yoruba pronunciation",
                "body": [
                    "<p>The Yoruba alphabet is entirely learnable by beginners — but the part that makes the real difference (tones, open and closed vowels, sounds like <em>gb</em> and <em>p</em>) depends on <strong>listening and being corrected</strong>. An app can show you the letter; it can't tell when you've produced the wrong tone. That's why the safest way to start is with audio and guided practice.</p>",
                    "<p>At Vedium, Yoruba is taught in <a href=\"/en/learn-yoruba-online\">live classes, from scratch to advanced</a>, starting exactly with sounds and tones, with real-time correction. After the alphabet, the natural next steps are <a href=\"/blog/yoruba-greetings\">Yoruba greetings</a> and <a href=\"/blog/yoruba-numbers-1-to-20\">Yoruba numbers</a>.</p>",
                ],
            },
        ],
        "faqs": [
            {"q": "How many letters does the Yoruba alphabet have?", "a": "25 letters: a, b, d, e, ẹ, f, g, gb, h, i, j, k, l, m, n, o, ọ, p, r, s, ṣ, t, u, w, y. The letters c, q, v, x and z don't exist in Yoruba."},
            {"q": "How many vowels does Yoruba have?", "a": "Seven oral vowels (a, e, ẹ, i, o, ọ, u) plus nasal vowels. The dotted versions (ẹ, ọ) have a more open sound."},
            {"q": "Is Yoruba hard to pronounce?", "a": "The biggest challenge is the three-tone system (high, mid and low), which changes word meaning, plus sounds like gb and p (pronounced kp). With audio and live correction, the pronunciation is fully learnable."},
            {"q": "Can I learn the Yoruba alphabet on my own?", "a": "You can memorize the letters, but the tones and special sounds need to be heard and practiced with a teacher so you don't lock in an incorrect pronunciation."},
        ],
        "cta_title": "Want to learn Yoruba with correct pronunciation from day one?",
        "cta_text": "At Vedium, Yoruba is taught in live classes, from scratch to advanced, with a focus on tones and real conversation.",
        "cta_label": "Learn about the Yoruba course",
        "cta_url": "/en/learn-yoruba-online",
    },
    "yoruba-greetings": {
        "lang": "en",
        "alt": {"pt-BR": "saudacoes-em-ioruba", "en": "yoruba-greetings"},
        "title": "Yoruba greetings: how to say good morning, thank you and more",
        "meta_description": "Learn the essential Yoruba greetings: good morning, good afternoon, good evening, how are you, thank you and welcome — plus the respectful and informal forms.",
        "h1": "Yoruba greetings: good morning, thank you and everyday courtesies",
        "date": "2026-07-02",
        "date_display": "July 2, 2026",
        "hero_image": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1100&h=560&fit=crop&q=80",
        "hero_alt": "People greeting each other — Yoruba greetings",
        "tag": "Yoruba",
        "lead": "In Yoruba culture, greeting someone well is more than politeness — it's a sign of respect, especially toward elders. This guide covers the essential greetings — good morning, good afternoon, good evening, how are you, thank you and welcome — and explains the difference between the respectful and informal forms, which changes how you speak.",
        "sections": [
            {
                "heading": "Why greetings matter so much in Yoruba",
                "body": [
                    "<p>Among the Yoruba people, greeting holds a central place in daily life. There are specific greetings for almost every situation — for someone who is working, eating, returning from a trip, or carrying out a task. Greeting properly shows <strong>respect and good manners</strong>, and skipping it can come across as cold.</p>",
                    "<p>One detail changes everything from the start: Yoruba distinguishes the <strong>respectful/plural</strong> form from the <strong>informal/singular</strong> one. Most greetings begin with <strong>\"Ẹ\"</strong> when you're speaking to someone older, to an authority figure, or to more than one person. With friends and peers, you use <strong>\"O\"</strong> or simply the short form.</p>",
                ],
            },
            {
                "heading": "Good morning, good afternoon and good evening in Yoruba",
                "body": [
                    "<p>The greetings tied to the time of day are the first ones every beginner learns:</p>",
                    "<ul>"
                    "<li><strong>Ẹ kàárọ̀</strong> — good morning;</li>"
                    "<li><strong>Ẹ kàásàn</strong> — good afternoon;</li>"
                    "<li><strong>Ẹ kúùrọ̀lẹ́</strong> — good (late) afternoon/early evening;</li>"
                    "<li><strong>Ẹ kúalẹ́</strong> — good evening/good night.</li>"
                    "</ul>",
                    "<p>With friends, you can use the same expressions, swapping the respectful <em>Ẹ</em> for the informal form. To say goodnight in the sense of \"see you tomorrow,\" you use <strong>O dàárọ̀</strong>. Since Yoruba is a tonal language, the accent marks over the words indicate the tone — and getting the tone right is part of what makes a greeting sound natural.</p>",
                ],
            },
            {
                "heading": "How are you? Asking how someone is doing",
                "body": [
                    "<p>After the initial greeting comes the question about how the person is doing:</p>",
                    "<ul>"
                    "<li><strong>Báwo ni?</strong> — how's it going? / how are you?;</li>"
                    "<li><strong>Ṣé àlàáfíà ni?</strong> — is everything at peace/well?;</li>"
                    "<li><strong>Ṣé dáadáa ni?</strong> — is everything okay?</li>"
                    "</ul>",
                    "<p>A common, positive answer is <strong>Mo wà dáadáa</strong> (\"I'm well\") or simply <strong>Àlàáfíà</strong> (\"peace,\" in the sense of \"all is well\"). The word <em>àlàáfíà</em>, in fact, comes up often: it carries the idea of well-being and calm, and is used both to greet and to respond.</p>",
                ],
            },
            {
                "heading": "Thank you, welcome and goodbye",
                "body": [
                    "<p>These three expressions round out the basic courtesy kit:</p>",
                    "<ul>"
                    "<li><strong>Ẹ ṣé</strong> — thank you (respectful); with friends, <strong>O ṣé</strong>;</li>"
                    "<li><strong>Ẹ káàbọ̀</strong> — welcome;</li>"
                    "<li><strong>Ó dàbọ̀</strong> — goodbye / see you later.</li>"
                    "</ul>",
                    "<p>There are also widely used situational greetings, such as <strong>Ẹ kú iṣẹ́</strong>, said to someone who is working, with variations for someone carrying out other activities. This repertoire of \"a greeting for every occasion\" is one of the most beautiful traits of the language — and shows how closely Yoruba and its culture are intertwined.</p>",
                ],
            },
            {
                "heading": "Greeting elders: a gesture of respect",
                "body": [
                    "<p>In Yoruba culture, the way you greet elders goes beyond words. Traditionally, when greeting an elder, <strong>boys and men perform the <em>ìdọ̀bálẹ̀</em></strong> (a bow, prostrating or lying down slightly), while <strong>girls and women perform the <em>ìkúnlẹ̀</em></strong> (kneeling briefly). In urban, everyday contexts, this gesture is often symbolic — a slight bow of the body — but the intention of respect remains very much present.</p>",
                    "<p>This is exactly why the respectful form with <strong>\"Ẹ\"</strong> matters so much: using the right greeting with the right person shows that you understand not just the language, but also Yoruba etiquette. Addressing an elder with the informal form can come across as impolite, even if the sentence is grammatically \"correct.\" This is one of the areas where learning with a teacher makes a real difference — they teach you not just what to say, but <strong>to whom and how</strong> to say it.</p>",
                ],
            },
            {
                "heading": "Practicing greetings with the right pronunciation",
                "body": [
                    "<p>You can memorize the list above today, but the part that makes a greeting sound natural — the <strong>tone</strong> and the difference between open and closed vowels — only comes from listening and repeating. Before greetings, it's worth understanding the <a href=\"/blog/yoruba-alphabet-guide\">Yoruba alphabet and its tones</a>; after that, a good next step is <a href=\"/blog/yoruba-numbers-1-to-20\">Yoruba numbers</a>.</p>",
                    "<p>At Vedium, greetings come up right in the first classes of <a href=\"/en/learn-yoruba-online\">live Yoruba</a>, with the teacher correcting pronunciation and tone in real time — the way you actually learn to greet someone for real.</p>",
                ],
            },
        ],
        "faqs": [
            {"q": "How do you say good morning in Yoruba?", "a": "Good morning is \"Ẹ kàárọ̀\" in the respectful form (with elders or in a group). With friends, the informal form is used."},
            {"q": "How do you say thank you in Yoruba?", "a": "\"Ẹ ṣé\" in the respectful form, and \"O ṣé\" in the informal form, with friends and peers."},
            {"q": "What's the difference between Ẹ and O in greetings?", "a": "\"Ẹ\" is the respectful and plural form, used with elders, authority figures or more than one person. \"O\" is the informal form, used with friends and peers."},
            {"q": "Do I need to get the tone right in greetings?", "a": "Yes. Yoruba is a tonal language, and tone is part of the word itself. It's worth practicing greetings with audio and live correction, not just from text."},
        ],
        "cta_title": "Want to learn how to greet (and chat) in Yoruba?",
        "cta_text": "Vedium's live classes start with greetings and correct pronunciation, taught by a specialized teacher.",
        "cta_label": "Learn about the Yoruba course",
        "cta_url": "/en/learn-yoruba-online",
    },
    "yoruba-numbers-1-to-20": {
        "lang": "en",
        "alt": {"pt-BR": "numeros-em-ioruba", "en": "yoruba-numbers-1-to-20"},
        "title": "Yoruba numbers 1 to 20: how to count (and the base-20 logic)",
        "meta_description": "Learn Yoruba numbers from 1 to 20, with approximate pronunciation and the fascinating vigesimal (base-20) logic that uses subtraction to form 15 through 19.",
        "h1": "Yoruba numbers 1 to 20",
        "date": "2026-07-02",
        "date_display": "July 2, 2026",
        "hero_image": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80",
        "hero_alt": "Learning to count — Yoruba numbers",
        "tag": "Yoruba",
        "lead": "Counting in Yoruba is more interesting than it sounds. The language uses a vigesimal system — base 20 — and, starting at 15, forms numbers through subtraction. In this guide, you'll learn the numbers from 1 to 20, understand that logic, and find out why the pronunciation takes practice.",
        "sections": [
            {
                "heading": "Yoruba numbers 1 to 10",
                "body": [
                    "<p>The foundation for everything is the first ten numbers. They're the most straightforward part to learn:</p>",
                    "<ul>"
                    "<li>1 — <strong>ọ̀kan</strong></li>"
                    "<li>2 — <strong>èjì</strong></li>"
                    "<li>3 — <strong>ẹ̀ta</strong></li>"
                    "<li>4 — <strong>ẹ̀rin</strong></li>"
                    "<li>5 — <strong>àrún</strong></li>"
                    "<li>6 — <strong>ẹ̀fà</strong></li>"
                    "<li>7 — <strong>èje</strong></li>"
                    "<li>8 — <strong>ẹ̀jọ</strong></li>"
                    "<li>9 — <strong>ẹ̀sán</strong></li>"
                    "<li>10 — <strong>ẹ̀wá</strong></li>"
                    "</ul>",
                    "<p>Worth repeating: the accent marks aren't decoration. Yoruba is tonal, and the accent marks the tone of each syllable. So the spelling above is a guide, but the pronunciation needs to be heard to come out naturally.</p>",
                ],
            },
            {
                "heading": "Numbers 11 to 14",
                "body": [
                    "<p>From 11 to 14, Yoruba adds onto ten, with a suffix meaning \"plus\" (related to <em>-lá</em>):</p>",
                    "<ul>"
                    "<li>11 — <strong>ọ̀kànlá</strong> (ten and one)</li>"
                    "<li>12 — <strong>èjìlá</strong> (ten and two)</li>"
                    "<li>13 — <strong>ẹ̀talá</strong> (ten and three)</li>"
                    "<li>14 — <strong>ẹ̀rìnlá</strong> (ten and four)</li>"
                    "</ul>",
                    "<p>Notice that you can recognize the base number (èjì, ẹ̀ta, ẹ̀rin) inside the word. This logic of \"building\" numbers from their roots is what makes the Yoruba system organized, even though it's different from what English speakers are used to.</p>",
                ],
            },
            {
                "heading": "Numbers 15 to 20: the subtraction logic",
                "body": [
                    "<p>Here's the most fascinating part. Starting at 15, Yoruba tends to form numbers by <strong>subtracting from twenty</strong>, instead of adding onto ten. The word <em>dín</em> carries the idea of \"minus\":</p>",
                    "<ul>"
                    "<li>15 — <strong>ẹ̀ẹ́dógún</strong> (twenty minus five)</li>"
                    "<li>16 — <strong>ẹ̀rìndínlógún</strong> (twenty minus four)</li>"
                    "<li>17 — <strong>ẹ̀tàdínlógún</strong> (twenty minus three)</li>"
                    "<li>18 — <strong>èjìdínlógún</strong> (twenty minus two)</li>"
                    "<li>19 — <strong>ọ̀kàndínlógún</strong> (twenty minus one)</li>"
                    "<li>20 — <strong>ogún</strong></li>"
                    "</ul>",
                    "<p>In other words, instead of saying \"ten and nine\" for 19, Yoruba says something like \"twenty minus one.\" That's the heart of the <strong>vigesimal (base-20) system</strong>, which organizes traditional Yoruba counting around multiples of twenty.</p>",
                ],
            },
            {
                "heading": "Why Yoruba counts in twenties",
                "body": [
                    "<p>Many cultures developed counting systems tied to the body and to trade. The Yoruba vigesimal system is one of the most elaborate in the world: larger numbers are built from twenty, through chained addition and subtraction. That's why learning to count in Yoruba is also a small lesson in <strong>logic and culture</strong>, not just vocabulary.</p>",
                    "<p>For everyday use, the numbers from 1 to 20 already cover plenty of situations — age, quantities, times and simple prices. As you progress, a teacher will show you how multiples of ten and twenty combine to form larger numbers.</p>",
                ],
            },
            {
                "heading": "The multiples of ten: 10, 20, 30 and 40",
                "body": [
                    "<p>After 20, the base-20 logic becomes even clearer in the multiples of ten. Worth knowing the main ones:</p>",
                    "<ul>"
                    "<li>10 — <strong>ẹ̀wá</strong></li>"
                    "<li>20 — <strong>ogún</strong></li>"
                    "<li>30 — <strong>ọgbọ̀n</strong></li>"
                    "<li>40 — <strong>ogójì</strong> (literally \"two twenties,\" i.e. 2 × 20)</li>"
                    "</ul>",
                    "<p>Notice something interesting: while 30 (<em>ọgbọ̀n</em>) has its own word, 40 is already built as <strong>\"two twenties.\"</strong> From there, the larger multiples keep revolving around twenty — 60 is \"three twenties,\" and so on. This chaining is what gives the Yoruba system its reputation for ingenuity: with just a few roots and two operations (adding and subtracting), the whole counting system is built.</p>",
                    "<p>If you're just starting out, you don't need to master all of this at once. The numbers from 1 to 20 already handle most everyday situations, and the multiples of ten come naturally as you progress.</p>",
                ],
            },
            {
                "heading": "How to practice Yoruba numbers",
                "body": [
                    "<p>Memorizing the list is the first step; using the numbers in sentences (\"I am X years old,\" \"I want X\") is what really locks them in. And, as always in Yoruba, <strong>tone</strong> needs practice with audio. If you haven't already, start with the <a href=\"/blog/yoruba-alphabet-guide\">Yoruba alphabet</a> and <a href=\"/blog/yoruba-greetings\">Yoruba greetings</a>.</p>",
                    "<p>At Vedium, numbers come up in the first classes of <a href=\"/en/learn-yoruba-online\">live Yoruba</a>, with pronunciation practice and use in real situations — the way you actually learn to count and to converse.</p>",
                ],
            },
        ],
        "faqs": [
            {"q": "How do you count from 1 to 5 in Yoruba?", "a": "1 is ọ̀kan, 2 is èjì, 3 is ẹ̀ta, 4 is ẹ̀rin and 5 is àrún. The accent marks indicate the tones, which are part of correct pronunciation."},
            {"q": "Why does Yoruba use base 20?", "a": "Yoruba has a vigesimal (base-20) counting system, where larger numbers are formed from multiples of twenty, using addition and subtraction. That's why, from 15 to 19, counting is usually done by subtracting from twenty."},
            {"q": "How do you say 20 in Yoruba?", "a": "Twenty is \"ogún\". Numbers like 19 are formed as \"twenty minus one\" (ọ̀kàndínlógún), which shows the base-20 logic."},
            {"q": "Are Yoruba numbers hard to learn?", "a": "Numbers 1 through 14 follow a straightforward pattern. From 15 to 19, the subtraction logic needs a bit more attention. With practice and audio, they're all learnable by beginners."},
        ],
        "cta_title": "Want to learn to count and converse in Yoruba?",
        "cta_text": "In Vedium's live classes, numbers and pronunciation are practiced from the very start, with a specialized teacher.",
        "cta_label": "Learn about the Yoruba course",
        "cta_url": "/en/learn-yoruba-online",
    },
    "yoruba-language-and-culture": {
        "lang": "en",
        "alt": {"pt-BR": "aprender-ioruba-lingua-e-cultura", "en": "yoruba-language-and-culture"},
        "title": "Yoruba: get to know the language and why you should learn it",
        "meta_description": "Yoruba is spoken by millions in West Africa and has a strong presence in Brazilian culture. Get to know the language.",
        "h1": "Yoruba: get to know the language and why you should learn it",
        "date": "2026-07-02",
        "date_display": "July 2, 2026",
        "hero_image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1100&h=560&fit=crop&q=80",
        "hero_alt": "Yoruba class: language and culture at Vedium",
        "tag": "Yoruba",
        "lead": "Yoruba is one of the most widely spoken languages in West Africa, with millions of speakers in Nigeria, Benin and Togo, plus a large diaspora community around the world — including in Brazil. It's a living language, with tone, rhythm and an incredibly rich culture behind it.",
        "sections": [
            {
                "heading": "A language connected to the diaspora",
                "body": [
                    "<p>Yoruba's presence runs deep in the culture and traditions of the African diaspora, especially in music, cuisine and Afro-diasporic spiritual traditions found across the Americas — most visibly in Brazil. Learning the language is also a way to reconnect with that heritage and understand it at the source.</p>",
                ],
            },
            {
                "heading": "Why study Yoruba",
                "body": [
                    "<ul>"
                    "<li>Reconnection with cultural and religious roots;</li>"
                    "<li>Access to music, proverbs and literature in the original language;</li>"
                    "<li>Communication with speakers across Africa and the diaspora;</li>"
                    "<li>A cultural and academic differentiator.</li>"
                    "</ul>",
                ],
            },
            {
                "heading": "What the course is like at Vedium",
                "body": [
                    "<p>At Vedium, Yoruba is taught in <strong>live classes</strong>, from beginner to advanced, with teacher Busayo Frank Alonge. Classes bring the language and culture to life in an accessible way, with a focus on helping you actually speak.</p>",
                ],
            },
        ],
        "faqs": [],
        "cta_title": "Want to learn Yoruba from scratch?",
        "cta_text": "Discover Vedium's live Yoruba classes, focused on culture and real conversation.",
        "cta_label": "Learn about the Yoruba course",
        "cta_url": "/en/learn-yoruba-online",
    },

    # ==========================================================================
    # Lote publicado em 2026-07-14: 33 posts do calendario editorial (Cliente/
    # Vedium/Artigos/Postados), com "category" para as paginas de categoria novas
    # (/blog/ingles, /blog/ioruba, /en/blog/brazilian-portuguese,
    # /es/blog/portugues-brasileno). Posts em de/fr/ru/zh-CN ficam em URL plana
    # (/blog/<slug>), sem "category", pois o site ainda nao tem paginas de
    # categoria/prefixo de idioma para esses 4 idiomas (ver LANG_BLOG_PREFIXES em
    # hooks.py e PLE_CATEGORY_BY_LANG acima).
    # ==========================================================================
    "como-saber-seu-nivel-real-de-ingles-antes-de-escolher-um-curso": {'title': 'Como saber seu nível real de inglês antes de escolher um curso',
     'meta_description': 'Aprenda a identificar seu nível real de inglês antes de escolher um curso '
                         'online ao vivo e evoluir com segurança, prática e sem fidelidade.',
     'h1': 'Como saber seu nível real de inglês antes de escolher um curso',
     'date': '2025-01-06',
     'date_display': '6 de janeiro de 2025',
     'hero_image': 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aula de inglês na Vedium',
     'tag': 'Inglês',
     'category': 'ingles',
     'lead': 'Saber seu nível real de inglês antes de escolher um curso evita frustração, perda de '
             'tempo e escolhas erradas. O ponto principal não é decorar se você é “básico”, '
             '“intermediário” ou “avançado”, mas entender o que você consegue fazer com o idioma em '
             'situações reais: falar, ouvir, ler, escrever, participar de reuniões, viajar, estudar ou '
             'trabalhar.',
     'sections': [{'heading': '',
                   'body': ['<p>Para quem quer evoluir de verdade, especialmente com foco em carreira, '
                            'conversação e confiança, o nivelamento precisa ir além de um teste rápido '
                            'de múltipla escolha. Ele deve avaliar compreensão, vocabulário, gramática '
                            'aplicada, pronúncia, fluência e capacidade de se comunicar sob pressão '
                            'leve. É por isso que um <a href="/teste-de-nivel-ingles">curso de inglês '
                            'online ao vivo</a>, com professor em tempo real, costuma dar uma leitura '
                            'mais fiel do seu ponto de partida.</p>',
                            '<p>Na Vedium, a lógica é simples: você não precisa se encaixar em uma '
                            'turma aleatória. Você precisa começar no lugar certo, com prática real, '
                            'acompanhamento e liberdade para continuar porque percebe resultado — não '
                            'porque ficou preso a um contrato longo.</p>']},
                  {'heading': 'Por que saber seu nível real de inglês trava tanta gente',
                   'body': ['<p>A maioria dos alunos trava porque confunde “conhecimento passivo” com '
                            '“capacidade de comunicação”. Você pode entender séries, reconhecer '
                            'palavras e até acertar questões de gramática, mas ainda assim sentir '
                            'dificuldade para responder uma pergunta simples em uma conversa.</p>',
                            '<p>Esse é um dos maiores problemas na hora de escolher um curso de '
                            'inglês. Muita gente se define assim:</p>',
                            '<ul><li>“Eu sou básico, mas entendo bastante coisa.”</li><li>“Eu sou '
                            'intermediário, mas não consigo falar.”</li><li>“Eu fiz anos de curso, mas '
                            'esqueci quase tudo.”</li><li>“Eu leio bem, mas em reunião fico '
                            'inseguro.”</li><li>“Eu sei gramática, mas minha conversação não '
                            'anda.”</li></ul>',
                            '<p>Essas frases mostram que o nível real não cabe em uma etiqueta '
                            'simples. O aluno pode estar em um nível para leitura, outro para escuta e '
                            'outro completamente diferente para fala. No ambiente profissional, isso '
                            'fica ainda mais claro: alguém pode ler e-mails em inglês, mas travar em '
                            'uma call internacional; pode entender apresentações, mas não conseguir '
                            'defender uma ideia; pode saber vocabulário técnico, mas não ter '
                            'naturalidade para small talk.</p>',
                            '<p>É por isso que escolher um curso apenas pelo nome da turma — básico, '
                            'intermediário ou avançado — pode ser uma armadilha. O ideal é identificar '
                            'o nível funcional: aquilo que você consegue fazer hoje e o que precisa '
                            'desenvolver para chegar ao próximo estágio.</p>']},
                  {'heading': 'O que é nível CEFR e por que ele ajuda na escolha do curso',
                   'body': ['<p>O CEFR é uma referência internacional que organiza a proficiência em '
                            'idiomas em níveis de A1 a C2. Para quem está escolhendo um curso, ele '
                            'ajuda a transformar uma percepção vaga em um mapa de evolução mais '
                            'claro.</p>',
                            '<p>De forma simples:</p>',
                            '<ul><li><strong>A1:</strong> você entende e usa frases muito básicas, com '
                            'apoio.</li><li><strong>A2:</strong> você se comunica em situações simples '
                            'e previsíveis.</li><li><strong>B1:</strong> você já consegue lidar com '
                            'temas familiares e manter conversas mais '
                            'funcionais.</li><li><strong>B2:</strong> você se comunica com mais '
                            'independência, inclusive em contextos '
                            'profissionais.</li><li><strong>C1:</strong> você usa o inglês com '
                            'fluidez, precisão e segurança em situações '
                            'complexas.</li><li><strong>C2:</strong> você tem domínio muito próximo ao '
                            'de um usuário altamente proficiente.</li></ul>',
                            '<p>Para a maioria dos alunos adultos, especialmente a persona Bruno — '
                            'profissional em ascensão, com rotina cheia e desejo de crescer na '
                            'carreira — o objetivo costuma ser sair da sensação de “eu entendo, mas '
                            'não falo” e avançar até um B1, B2 ou C1 funcional. O problema é que esse '
                            'caminho não acontece apenas assistindo vídeos ou fazendo exercícios '
                            'soltos. Ele exige prática, correção, repetição e situações reais de '
                            'fala.</p>',
                            '<p>Um bom nivelamento deve usar o CEFR como referência, mas não como '
                            'rótulo frio. O mais importante é responder: em que nível você está para '
                            'conversar, argumentar, ouvir, improvisar e se expressar com '
                            'clareza?</p>']},
                  {'heading': 'Como avaliar seu inglês antes de escolher uma turma',
                   'body': ['<p>Você pode começar avaliando seu inglês por quatro habilidades: escuta, '
                            'fala, leitura e escrita. A resposta mais honesta costuma aparecer quando '
                            'você separa essas habilidades, em vez de tentar resumir tudo em uma única '
                            'palavra.</p>',
                            '<p>Faça esta análise inicial:</p>',
                            '<h3>1. Escuta: você entende inglês em velocidade natural?</h3>',
                            '<p>A pergunta não é apenas se você entende palavras isoladas. É se '
                            'consegue acompanhar uma conversa real, com ritmo, sotaques, cortes, '
                            'expressões e mudanças de assunto. Quem está em nível inicial entende '
                            'frases previsíveis. Quem está em nível intermediário começa a captar '
                            'ideias gerais. Quem está em nível mais avançado compreende detalhes, '
                            'intenção e nuance.</p>',
                            '<h3>2. Fala: você consegue responder sem traduzir tudo mentalmente?</h3>',
                            '<p>A fala é o ponto em que muitos alunos descobrem que seu nível real é '
                            'diferente do nível que imaginavam. Se você demora muito para montar '
                            'frases, trava por medo de errar ou evita conversas, provavelmente precisa '
                            'de uma turma que priorize conversação guiada, não apenas conteúdo '
                            'gramatical.</p>',
                            '<h3>3. Leitura: você entende textos do seu universo?</h3>',
                            '<p>Ler posts, notícias, e-mails, apresentações e materiais profissionais '
                            'ajuda a medir vocabulário e estrutura. Mas cuidado: leitura costuma ser a '
                            'habilidade mais confortável para brasileiros, porque permite mais tempo '
                            'de processamento. Ler bem não significa automaticamente falar bem.</p>',
                            '<h3>4. Escrita: você consegue comunicar ideias com clareza?</h3>',
                            '<p>A escrita mostra domínio de estrutura, vocabulário e organização. Para '
                            'profissionais, escrever e-mails, mensagens e comentários em inglês pode '
                            'ser uma necessidade real. Um curso bem escolhido deve considerar isso, '
                            'mesmo que o foco principal seja conversação.</p>',
                            '<p>Depois dessa autoavaliação, o ideal é fazer um teste de nível com '
                            'orientação humana. Um formulário ajuda, mas uma conversa ao vivo revela '
                            'muito mais: pronúncia, segurança, velocidade de resposta, vocabulário '
                            'ativo e capacidade de manter interação.</p>']},
                  {'heading': 'Como praticar de forma objetiva antes da aula experimental',
                   'body': ['<p>A melhor forma de descobrir seu nível real é colocar o inglês em uso. '
                            'Antes de uma aula experimental ou teste de nível, faça pequenos '
                            'exercícios práticos que simulem situações reais.</p>',
                            '<p>Você pode começar com três práticas simples:</p>',
                            '<ol><li><strong>Apresente-se em inglês por um minuto.</strong> Fale seu '
                            'nome, área de trabalho, rotina, objetivos e por que quer estudar inglês. '
                            'Grave no celular e escute depois. Observe se você trava, repete palavras '
                            'ou perde clareza.</li></ol>',
                            '<ol><li><strong>Explique um problema do seu trabalho em inglês.</strong> '
                            'Não precisa ser complexo. Pode ser algo como “I need to improve my '
                            'English because I want to participate in meetings with international '
                            'clients.” O objetivo é perceber se você consegue conectar '
                            'ideias.</li></ol>',
                            '<ol><li><strong>Assista a um vídeo curto e resuma em voz alta.</strong> '
                            'Escolha um vídeo de até três minutos. Depois, tente explicar o que '
                            'entendeu sem escrever antes. Esse exercício testa escuta, memória, '
                            'vocabulário e fala.</li></ol>',
                            '<p>Essas práticas não substituem um nivelamento profissional, mas ajudam '
                            'você a chegar mais consciente. Também mostram se você precisa de uma '
                            'turma mais focada em base, conversação, vocabulário profissional ou '
                            'fluência.</p>']},
                  {'heading': 'O que observar em um curso de inglês online ao vivo',
                   'body': ['<p>Um bom curso de inglês online ao vivo deve ajudar você a evoluir com '
                            'clareza, não apenas consumir aulas. Antes de escolher, observe se a '
                            'escola oferece diagnóstico, prática real e acompanhamento.</p>',
                            '<p>Procure por estes pontos:</p>',
                            '<ul><li><strong>Aulas ao vivo de verdade:</strong> com professor, '
                            'interação e correção em tempo real.</li><li><strong>Turmas '
                            'pequenas:</strong> para você falar mais e receber '
                            'atenção.</li><li><strong>Nivelamento claro:</strong> para entrar na turma '
                            'certa.</li><li><strong>Foco em conversação:</strong> especialmente se seu '
                            'objetivo é carreira, viagens ou reuniões.</li><li><strong>Evolução por '
                            'níveis:</strong> com metas visíveis e progresso '
                            'acompanhado.</li><li><strong>Flexibilidade:</strong> para estudar no seu '
                            'ritmo, sem amarras desnecessárias.</li><li><strong>Sem '
                            'fidelidade:</strong> porque a permanência deve vir do resultado, não de '
                            'multa.</li></ul>',
                            '<p>Esse último ponto é importante. Muitos alunos já começaram cursos '
                            'longos, pagaram caro e desistiram porque não sentiam evolução. Na Vedium, '
                            'a proposta é diferente: aulas ao vivo, evolução real e liberdade. Você '
                            'continua porque percebe avanço aula após aula.</p>']},
                  {'heading': 'Próximo passo no curso ao vivo',
                   'body': ['<p>O próximo passo é fazer um teste de nível e conversar com alguém que '
                            'consiga interpretar seu inglês na prática. Não escolha sua turma apenas '
                            'pela sensação de “acho que sou intermediário”. Escolha com base no que '
                            'você consegue fazer hoje e no que precisa construir para alcançar seu '
                            'objetivo.</p>',
                            '<p>Na Vedium, o curso de inglês foi pensado para quem quer sair da '
                            'enrolação e praticar de verdade. As aulas são ao vivo, com '
                            'acompanhamento, foco em conversação e evolução do A1 ao C1. Para o '
                            'profissional que precisa crescer, participar de reuniões, destravar o '
                            'speaking ou buscar oportunidades melhores, isso faz diferença.</p>',
                            '<p>Além disso, estudar sem fidelidade reduz o medo de começar. Você pode '
                            'testar, sentir a dinâmica e continuar porque a experiência faz sentido '
                            'para sua rotina. Em vez de promessas milagrosas, o caminho é consistente: '
                            'diagnóstico correto, aula ao vivo, prática real, correção e '
                            'progresso.</p>']},
                  {'heading': 'Checklist rápido para descobrir se você está na turma certa',
                   'body': ['<p>Antes de se matricular, responda com sinceridade:</p>',
                            '<ul><li>Eu consigo me apresentar em inglês sem decorar?</li><li>Consigo '
                            'manter uma conversa simples por três minutos?</li><li>Entendo perguntas '
                            'em inglês sem pedir repetição o tempo todo?</li><li>Sei explicar minha '
                            'profissão, rotina e objetivos?</li><li>Tenho vocabulário suficiente para '
                            'situações reais?</li><li>Receberei correção ao vivo durante as '
                            'aulas?</li><li>A turma tem nível compatível com meu '
                            'momento?</li><li>Existe um plano claro para eu evoluir?</li><li>Posso '
                            'começar sem contrato de fidelidade?</li></ul>',
                            '<p>Se a maioria das respostas for incerta, você não precisa desistir. '
                            'Você precisa de um nivelamento melhor e de uma turma adequada. O erro não '
                            'está em não saber tudo; está em começar no lugar errado.</p>']},
                  {'heading': 'Conclusão com CTA forte',
                   'body': ['<p>Saber seu nível real de inglês é o primeiro passo para parar de '
                            'estudar no escuro. Quando você entende onde está, fica mais fácil '
                            'escolher a turma certa, praticar com objetivo e medir sua evolução. Para '
                            'quem quer inglês de verdade para carreira, viagens, estudos ou confiança '
                            'pessoal, a combinação entre nivelamento, aulas ao vivo e conversação '
                            'guiada é muito mais eficiente do que seguir conteúdos soltos.</p>',
                            '<p>A Vedium oferece inglês online ao vivo, com evolução do A1 ao C1, '
                            'turmas pequenas e sem fidelidade. Aqui, você não fica preso por contrato: '
                            'você continua porque percebe resultado.</p>',
                            '<p><strong>Faça seu teste de nível grátis e descubra qual é o melhor '
                            'ponto de partida para o seu inglês:</strong> <a '
                            'href="/curso-de-ingles-online">https://vediums.com/</a></p>']}],
     'faqs': [{'q': 'Como saber se meu inglês é básico, intermediário ou avançado?',
               'a': 'Você deve avaliar o que consegue fazer com o idioma em situações reais. Se '
                    'entende frases simples e precisa de muito apoio, tende ao básico. Se conversa '
                    'sobre temas familiares, está no intermediário. Se consegue argumentar, participar '
                    'de reuniões e se expressar com fluidez, está mais próximo do avançado.'},
              {'q': 'O teste de nível online é suficiente para escolher uma turma?',
               'a': 'Um teste online ajuda, mas o ideal é combinar perguntas objetivas com uma '
                    'conversa ao vivo. A interação com professor revela pronúncia, fluência, '
                    'vocabulário ativo e segurança para responder em tempo real.'},
              {'q': 'O que significa estudar inglês do A1 ao C1?',
               'a': 'Significa seguir uma progressão baseada em níveis de proficiência. O A1 '
                    'representa o início do aprendizado, enquanto o C1 indica uso avançado e '
                    'independente do inglês em situações profissionais, acadêmicas e sociais.'},
              {'q': 'Curso de inglês online ao vivo funciona melhor para conversação?',
               'a': 'Para muitos alunos, sim. A aula ao vivo permite interação, correção imediata, '
                    'prática de fala e adaptação ao nível da turma. Isso é especialmente importante '
                    'para quem entende inglês, mas trava na hora de falar.'},
              {'q': 'A Vedium tem fidelidade no curso de inglês?',
               'a': 'Não. A Vedium trabalha com aulas ao vivo e sem contratos longos de fidelidade. A '
                    'ideia é que você continue porque percebe evolução real, não porque está preso a '
                    'uma multa ou obrigação contratual.'}],
     'cta_title': 'Quer saber seu nível real de inglês?',
     'cta_text': 'Faça o teste de nível grátis da Vedium e descubra por onde começar.',
     'cta_label': 'Conhecer o curso de Inglês',
     'cta_url': '/curso-de-ingles-online'},
    "ingles-ao-vivo-ou-gravado-o-que-muda-na-evolucao-do-speaking": {'title': 'Inglês ao vivo ou gravado: o que muda na evolução do speaking',
     'meta_description': 'Compare inglês ao vivo ou gravado e entenda o que muda no speaking, na '
                         'correção e na evolução com aulas online ao vivo.',
     'h1': 'Inglês ao vivo ou gravado: o que muda na evolução do speaking',
     'date': '2025-01-13',
     'date_display': '13 de janeiro de 2025',
     'hero_image': 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aula de inglês na Vedium',
     'tag': 'Inglês',
     'category': 'ingles',
     'lead': 'Escolher entre inglês ao vivo ou gravado muda diretamente a velocidade, a consistência e '
             'a qualidade da sua evolução no speaking. A diferença principal é simples: em uma aula '
             'gravada, você assiste; em uma aula ao vivo, você participa, responde, erra, recebe '
             'correção e aprende a usar o idioma em tempo real.',
     'sections': [{'heading': '',
                   'body': ['<p>Para quem quer aprender inglês de verdade, especialmente com foco em '
                            'carreira, reuniões, entrevistas, viagens ou oportunidades internacionais, '
                            'o speaking não melhora apenas com exposição passiva. Vídeos, aplicativos '
                            'e cursos gravados podem ajudar no vocabulário e na revisão de conteúdo, '
                            'mas não substituem a conversa real. Falar inglês exige interação, '
                            'improviso, escuta ativa, confiança e feedback.</p>',
                            '<p>É aqui que entra a proposta da <a '
                            'href="/teste-de-nivel-ingles">Vedium</a>: aulas de inglês online ao vivo, '
                            'com prática real, evolução por nível e liberdade para estudar sem '
                            'contrato de fidelidade. Você não precisa ficar preso a um método que não '
                            'conversa com sua rotina. Precisa encontrar um formato que faça você falar '
                            'mais, corrigir melhor e perceber avanço aula após aula.</p>']},
                  {'heading': 'Inglês ao vivo ou gravado: qual é a diferença real?',
                   'body': ['<p>A diferença real é que o inglês ao vivo transforma o aluno em '
                            'participante ativo, enquanto o gravado tende a colocar o aluno em posição '
                            'de espectador. Essa diferença parece pequena no começo, mas pesa muito '
                            'quando o objetivo é desenvolver speaking.</p>',
                            '<p>Em uma aula gravada, o conteúdo já está pronto. Você pode pausar, '
                            'voltar, acelerar e assistir quando quiser. Isso é útil para revisar '
                            'estruturas, aprender vocabulário e ter contato inicial com temas '
                            'específicos. O problema aparece quando você precisa responder uma '
                            'pergunta sem legenda, sustentar uma conversa ou adaptar uma frase ao '
                            'contexto.</p>',
                            '<p>Já em uma aula ao vivo, o professor percebe como você fala, onde '
                            'trava, quais sons confunde, quais palavras evita e quais estruturas ainda '
                            'não domina. A interação obriga o cérebro a fazer o que realmente acontece '
                            'em uma conversa: ouvir, processar, decidir o que dizer e falar com '
                            'clareza.</p>',
                            '<p>Na prática, a comparação fica assim:</p>',
                            '<ul><li><strong>Curso gravado:</strong> bom para contato inicial, revisão '
                            'e autonomia de estudo.</li><li><strong>Aula ao vivo:</strong> melhor para '
                            'conversação, correção, ritmo, confiança e evolução '
                            'orientada.</li><li><strong>Formato ideal:</strong> usar materiais de '
                            'apoio como complemento, mas manter a prática ao vivo como centro do '
                            'desenvolvimento.</li></ul>',
                            '<p>Para o aluno adulto, com pouco tempo e objetivo claro, essa diferença '
                            'evita um ciclo comum: consumir muito conteúdo, sentir que “estudou '
                            'bastante”, mas continuar travando na hora de falar.</p>']},
                  {'heading': 'Por que o speaking evolui mais com prática ao vivo',
                   'body': ['<p>O speaking evolui mais com prática ao vivo porque falar é uma '
                            'habilidade de performance, não apenas de memorização. Você pode saber a '
                            'regra, mas só descobre se consegue usá-la quando precisa se comunicar em '
                            'tempo real.</p>',
                            '<p>Muitos alunos brasileiros passam anos acumulando teoria. Sabem o '
                            'verbo, reconhecem a frase, entendem o texto, mas ficam inseguros quando '
                            'precisam abrir o microfone. Isso acontece porque o conhecimento está '
                            'passivo: ele existe na memória, mas ainda não virou resposta '
                            'automática.</p>',
                            '<p>A aula ao vivo ajuda justamente nessa transição. O aluno precisa '
                            'falar, reformular, perguntar, ouvir colegas e lidar com situações menos '
                            'previsíveis. O professor pode ajustar a rota durante a aula, propor uma '
                            'pergunta mais simples, aumentar o desafio, corrigir uma pronúncia ou '
                            'mostrar uma forma mais natural de dizer a mesma ideia.</p>',
                            '<p>Esse processo cria três ganhos importantes:</p>',
                            '<ol><li><strong>Vocabulário ativo:</strong> você deixa de apenas '
                            'reconhecer palavras e passa a usá-las.</li><li><strong>Fluência '
                            'funcional:</strong> você aprende a manter a conversa mesmo sem falar '
                            'perfeitamente.</li><li><strong>Confiança progressiva:</strong> você '
                            'percebe que errar faz parte do avanço e não precisa travar por '
                            'isso.</li></ol>',
                            '<p>Para quem busca inglês para carreira, essa prática é decisiva. Em uma '
                            'reunião, entrevista ou apresentação, ninguém entrega uma lista de '
                            'alternativas para você escolher. Você precisa entender a pergunta e '
                            'responder. Por isso, estudar inglês online ao vivo com foco em '
                            'conversação aproxima o treino da vida real.</p>']},
                  {'heading': 'O que muda na correção de erros entre aula gravada e aula ao vivo',
                   'body': ['<p>Na aula ao vivo, a correção acontece no momento em que o erro aparece; '
                            'no curso gravado, o aluno precisa perceber sozinho o que errou. Essa é '
                            'uma das diferenças mais importantes para quem quer melhorar o '
                            'speaking.</p>',
                            '<p>Em conteúdos gravados, o professor explica para uma audiência ampla. '
                            'Ele antecipa dúvidas comuns, mas não escuta a sua pronúncia, não vê sua '
                            'hesitação e não identifica padrões individuais. Se você pronuncia uma '
                            'palavra de forma pouco clara ou usa uma estrutura de forma repetida, o '
                            'vídeo não interrompe para orientar.</p>',
                            '<p>Na aula ao vivo, a correção é personalizada. E isso não significa '
                            'corrigir tudo de forma pesada ou constrangedora. Um bom professor sabe '
                            'escolher o momento certo: às vezes corrige na hora; às vezes deixa a '
                            'conversa fluir e comenta depois; às vezes transforma o erro em exercício '
                            'para a turma inteira.</p>',
                            '<p>Essa correção faz diferença em pontos como:</p>',
                            '<ul><li>pronúncia e sons difíceis para falantes de '
                            'português;</li><li>ordem das palavras nas frases;</li><li>uso de tempos '
                            'verbais em contexto;</li><li>vocabulário mais natural para ambiente '
                            'profissional;</li><li>excesso de tradução mental;</li><li>frases longas '
                            'demais que poderiam ser mais simples;</li><li>vícios de fala que o aluno '
                            'não percebe sozinho.</li></ul>',
                            '<p>A correção ao vivo reduz o risco de cristalizar erros. Quando o aluno '
                            'repete a mesma estrutura errada por meses, depois fica mais difícil '
                            'mudar. Já com feedback constante, ele entende o erro, pratica a '
                            'alternativa correta e ganha mais clareza sobre sua evolução.</p>']},
                  {'heading': 'Curso gravado serve para aprender inglês?',
                   'body': ['<p>Curso gravado pode ajudar no aprendizado, mas normalmente não é '
                            'suficiente para desenvolver speaking com segurança. Ele funciona melhor '
                            'como apoio, não como único caminho para quem precisa falar.</p>',
                            '<p>Vídeos gravados são úteis quando o aluno quer revisar uma regra, '
                            'estudar em horários muito específicos ou reforçar temas entre uma aula e '
                            'outra. Eles também ajudam na exposição ao idioma: ouvir explicações, '
                            'exemplos e diálogos amplia repertório.</p>',
                            '<p>O limite está na ausência de troca. O aluno pode assistir a uma aula '
                            'excelente e ainda assim não conseguir produzir uma frase sob pressão. '
                            'Isso não significa falta de inteligência ou falta de esforço. Significa '
                            'que a habilidade exigida é outra.</p>',
                            '<p>Pense em atividades práticas. Você não aprende a nadar apenas vendo '
                            'vídeos sobre natação. Não aprende a dirigir apenas estudando placas. Não '
                            'desenvolve apresentação em público apenas lendo técnicas. Em todos esses '
                            'casos, a teoria ajuda, mas a evolução real exige prática orientada.</p>',
                            '<p>Com inglês acontece o mesmo. O conteúdo gravado pode explicar. A aula '
                            'ao vivo faz você usar. Para quem está na fase de decisão e quer escolher '
                            'um curso com mais chance de resultado, a pergunta não deve ser apenas '
                            '“tem bom conteúdo?”, mas também:</p>',
                            '<ul><li>Vou falar em toda aula?</li><li>Alguém vai corrigir minha '
                            'pronúncia?</li><li>A turma tem nível compatível com o meu?</li><li>O '
                            'professor acompanha minha evolução?</li><li>O curso me prepara para '
                            'conversas reais?</li><li>Posso começar sem ficar preso a um contrato '
                            'longo?</li></ul>',
                            '<p>Essas respostas ajudam a separar consumo de conteúdo de aprendizagem '
                            'com prática.</p>']},
                  {'heading': 'Como escolher um curso de inglês online ao vivo',
                   'body': ['<p>Para escolher um curso de inglês online ao vivo, procure um formato '
                            'que combine conversação, nivelamento, turmas adequadas e acompanhamento '
                            'de progresso. O melhor curso para speaking é aquele que coloca você para '
                            'falar com frequência e segurança.</p>',
                            '<p>Antes de se matricular, observe se a escola oferece um teste de nível '
                            'ou uma conversa inicial. Isso evita entrar em uma turma fácil demais, '
                            'onde você se acomoda, ou difícil demais, onde você se frustra. O nível '
                            'correto deve desafiar sem paralisar.</p>',
                            '<p>Também vale analisar a dinâmica da aula. Em uma boa aula ao vivo, o '
                            'professor não passa o tempo inteiro explicando enquanto os alunos só '
                            'escutam. Há perguntas, diálogos, simulações, correção, vocabulário em '
                            'contexto e espaço para prática. O aluno precisa sair da aula com a '
                            'sensação de que usou o idioma, não apenas assistiu.</p>',
                            '<p>Alguns sinais positivos:</p>',
                            '<ul><li>aulas em tempo real, com professor presente;</li><li>foco em '
                            'conversação desde os primeiros níveis;</li><li>turmas pequenas ou '
                            'dinâmica que permita participação;</li><li>progressão clara do A1 ao '
                            'C1;</li><li>materiais de apoio para estudar entre as '
                            'aulas;</li><li>feedback sobre erros recorrentes;</li><li>liberdade para '
                            'continuar mês a mês, sem fidelidade.</li></ul>',
                            '<p>A proposta da Vedium se encaixa nesse caminho: inglês online ao vivo, '
                            'com prática real e evolução no seu ritmo. Para o aluno que já tentou '
                            'estudar sozinho, comprou cursos que não terminou ou sente que entende '
                            'mais do que fala, a aula ao vivo cria compromisso, orientação e contato '
                            'humano.</p>']},
                  {'heading': 'Por que o modelo sem fidelidade ajuda na decisão',
                   'body': ['<p>O modelo sem fidelidade ajuda porque reduz o medo de começar e coloca '
                            'o resultado no centro da relação. Em vez de continuar por obrigação '
                            'contratual, o aluno permanece porque percebe valor na experiência.</p>',
                            '<p>Muita gente adia o estudo de inglês porque já teve experiências '
                            'frustrantes: contratos longos, promessas exageradas, aulas massificadas '
                            'ou métodos que não conversavam com sua rotina. Quando existe multa ou '
                            'amarra, a decisão pesa mais. O aluno pensa: “E se eu não gostar?”, “E se '
                            'meu horário mudar?”, “E se eu não conseguir acompanhar?”.</p>',
                            '<p>Em uma escola sem fidelidade, a lógica muda. Você pode testar, '
                            'participar, sentir a metodologia e avaliar se está evoluindo. Isso exige '
                            'mais responsabilidade da escola, porque a retenção precisa vir da '
                            'qualidade da aula, da relação com o professor e do progresso '
                            'percebido.</p>',
                            '<p>Para o speaking, isso é especialmente importante. O aluno precisa '
                            'sentir que está falando mais, travando menos e recebendo orientação útil. '
                            'Quando isso acontece, continuar se torna uma consequência natural.</p>',
                            '<p>Na Vedium, a mensagem é direta: você fica porque quer, porque está '
                            'evoluindo, não porque assinou um contrato longo. Essa liberdade combina '
                            'com a realidade de quem trabalha, estuda, tem rotina cheia e precisa de '
                            'um curso sério, mas flexível.</p>']},
                  {'heading': 'Próximo passo para destravar seu speaking',
                   'body': ['<p>O próximo passo é descobrir seu nível real e experimentar uma aula ao '
                            'vivo. Antes de decidir entre inglês ao vivo ou gravado, faça uma pergunta '
                            'prática: qual formato realmente vai me colocar para falar?</p>',
                            '<p>Se seu objetivo é apenas revisar conteúdo, materiais gravados podem '
                            'ajudar. Mas se você quer responder melhor em reuniões, se apresentar com '
                            'confiança, viajar com mais autonomia, participar de entrevistas ou '
                            'alcançar níveis mais altos de proficiência, a conversação precisa estar '
                            'no centro.</p>',
                            '<p>Comece avaliando três pontos:</p>',
                            '<ul><li>Você fala inglês em toda sessão de estudo ou só '
                            'escuta?</li><li>Recebe correção humana sobre pronúncia, frase e '
                            'clareza?</li><li>Tem um plano de evolução por nível, com próximo passo '
                            'definido?</li></ul>',
                            '<p>Se a resposta for “não”, talvez o problema não seja sua capacidade. '
                            'Talvez seja o formato do curso.</p>',
                            '<p>A Vedium oferece aulas ao vivo para quem quer sair da enrolação e '
                            'transformar inglês em prática. Com nivelamento, conversação e evolução no '
                            'seu ritmo, o speaking deixa de ser uma promessa distante e passa a ser '
                            'construído aula após aula.</p>']},
                  {'heading': 'Conclusão com CTA forte',
                   'body': ['<p>Inglês ao vivo ou gravado não são formatos iguais com nomes '
                            'diferentes. Eles geram experiências diferentes. O gravado pode informar, '
                            'revisar e complementar. O ao vivo faz você interagir, improvisar, errar '
                            'com acompanhamento e desenvolver confiança para falar em situações '
                            'reais.</p>',
                            '<p>Para quem quer evolução no speaking, a escolha mais estratégica é '
                            'estudar com prática ao vivo, professor presente e acompanhamento de '
                            'nível. É isso que transforma conhecimento passivo em comunicação '
                            'real.</p>',
                            '<p>Na Vedium, você aprende inglês com aulas ao vivo, turmas pensadas para '
                            'evolução e liberdade para continuar sem fidelidade. A retenção vem do '
                            'resultado, não de contrato longo.</p>',
                            '<p><strong>Faça seu teste de nível grátis e descubra qual turma combina '
                            'com seu momento:</strong> <a '
                            'href="/curso-de-ingles-online">https://vediums.com/</a></p>']}],
     'faqs': [{'q': 'Aula de inglês gravada ajuda no speaking?',
               'a': 'Ajuda como complemento, principalmente para revisar conteúdo e ampliar '
                    'vocabulário. Mas, para desenvolver speaking, o aluno precisa falar, receber '
                    'correção e praticar conversas reais, algo que acontece melhor em aulas ao vivo.'},
              {'q': 'Inglês ao vivo é melhor que curso gravado?',
               'a': 'Para conversação, geralmente sim. A aula ao vivo permite interação, feedback, '
                    'ajuste de pronúncia e prática em tempo real. O curso gravado pode ser útil como '
                    'apoio, mas não substitui a troca com professor e turma.'},
              {'q': 'Como saber se preciso de aula ao vivo para destravar o inglês?',
               'a': 'Se você entende mais do que consegue falar, trava em conversas, demora para '
                    'responder ou sente medo de errar, a aula ao vivo tende a ser mais indicada. Ela '
                    'cria prática orientada e correção constante.'},
              {'q': 'O curso de inglês da Vedium tem fidelidade?',
               'a': 'Não. A Vedium trabalha com aulas ao vivo e sem contrato de fidelidade. Você '
                    'continua porque percebe evolução e valor na experiência, não porque está preso a '
                    'uma multa ou contrato longo.'},
              {'q': 'Qual é o primeiro passo para começar inglês ao vivo na Vedium?',
               'a': 'O primeiro passo é fazer um teste de nível grátis. Assim, você entende seu ponto '
                    'de partida e pode entrar em uma turma compatível com seu momento, seu objetivo e '
                    'sua rotina.'}],
     'cta_title': 'Quer saber seu nível real de inglês?',
     'cta_text': 'Faça o teste de nível grátis da Vedium e descubra por onde começar.',
     'cta_label': 'Conhecer o curso de Inglês',
     'cta_url': '/curso-de-ingles-online'},
    "como-combinar-leitura-escuta-fala-e-escrita-no-mesmo-plano": {'title': 'Como combinar leitura, escuta, fala e escrita no mesmo plano',
     'meta_description': 'Aprenda a combinar leitura, escuta, fala e escrita em um plano de inglês '
                         'eficiente, com conversação e evolução por nível CEFR.',
     'h1': 'Como combinar leitura, escuta, fala e escrita no mesmo plano',
     'date': '2026-06-15',
     'date_display': '15 de junho de 2026',
     'hero_image': 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aula de inglês na Vedium',
     'tag': 'Inglês',
     'category': 'ingles',
     'lead': 'Combinar leitura, escuta, fala e escrita no mesmo plano é uma das formas mais eficientes '
             'de evoluir no inglês porque o idioma passa a ser praticado como habilidade completa, não '
             'como um conjunto de exercícios soltos. A leitura aumenta vocabulário e estrutura; a '
             'escuta treina compreensão real; a fala desenvolve confiança e velocidade; e a escrita '
             'organiza pensamento, gramática e precisão.',
     'sections': [{'heading': '',
                   'body': ['<p>O erro de muitos alunos é estudar apenas uma habilidade por muito '
                            'tempo. Alguns passam meses lendo e fazendo exercícios, mas travam na '
                            'conversação. Outros assistem vídeos em inglês todos os dias, mas não '
                            'conseguem escrever um e-mail simples. Há também quem tente falar sem '
                            'construir repertório suficiente de vocabulário e acaba repetindo sempre '
                            'as mesmas frases. O resultado é uma evolução desequilibrada.</p>',
                            '<p>Para o Bruno — profissional que precisa de inglês de verdade para '
                            'crescer na carreira, participar de reuniões, fazer entrevistas, viajar ou '
                            'buscar oportunidades internacionais — o ideal é um plano integrado. Ele '
                            'não precisa escolher entre reading, listening, speaking e writing. '
                            'Precisa aprender a usar uma habilidade para fortalecer a outra.</p>',
                            '<p>Neste artigo, você vai entender por que integrar as quatro habilidades '
                            'destrava o aprendizado, como montar um plano prático por semana, como '
                            'adaptar a rotina ao seu nível CEFR e por que o inglês online ao vivo '
                            'acelera a evolução quando há conversação, correção e '
                            'acompanhamento.</p>']},
                  {'heading': 'Por que combinar as quatro habilidades acelera o inglês?',
                   'body': ['<p>Combinar as quatro habilidades acelera o inglês porque cria repetição '
                            'em contextos diferentes. Você encontra uma palavra na leitura, ouve essa '
                            'palavra em um áudio, usa na fala e depois escreve uma frase com ela. Esse '
                            'ciclo transforma vocabulário passivo em comunicação real.</p>',
                            '<p>Aprender inglês não é apenas “saber regras”. É conseguir usar o idioma '
                            'quando precisa. Para isso, o cérebro precisa reconhecer, recuperar e '
                            'produzir informação. Cada habilidade participa desse processo:</p>',
                            '<ul><li><strong>Leitura:</strong> amplia vocabulário, mostra estrutura de '
                            'frases e ajuda na compreensão de textos.</li><li><strong>Escuta:</strong> '
                            'acostuma o ouvido a sons, ritmo, sotaques e velocidade '
                            'natural.</li><li><strong>Fala:</strong> treina resposta rápida, '
                            'pronúncia, confiança e improviso.</li><li><strong>Escrita:</strong> '
                            'consolida gramática, clareza e organização de ideias.</li></ul>',
                            '<p>Quando essas habilidades ficam separadas, o aluno pode evoluir em uma '
                            'área e continuar inseguro em outra. Por exemplo, ele pode ler bem e não '
                            'falar. Pode entender vídeos, mas não escrever. Pode falar frases básicas, '
                            'mas não compreender um texto profissional.</p>',
                            '<p>Quando elas são combinadas, o aprendizado ganha profundidade. Um mesmo '
                            'tema pode ser trabalhado de quatro formas. Se o tema da semana é “job '
                            'interview”, o aluno pode ler um texto sobre entrevistas, ouvir um '
                            'diálogo, praticar respostas em voz alta e escrever um pequeno e-mail de '
                            'agradecimento depois da entrevista. Esse método é mais próximo da vida '
                            'real.</p>']},
                  {'heading': 'Por que isso trava tantos alunos?',
                   'body': ['<p>Isso trava tantos alunos porque eles estudam inglês em blocos '
                            'desconectados. Em vez de construir uma rotina em que as habilidades se '
                            'apoiam, pulam de vídeo em vídeo, de aplicativo em aplicativo e de lista '
                            'em lista sem uma sequência clara.</p>',
                            '<p>Os bloqueios mais comuns são:</p>',
                            '<h3>1. Ler muito, mas falar pouco</h3>',
                            '<p>O aluno até reconhece palavras e entende textos simples, mas sente '
                            'medo de abrir a boca. Isso acontece porque leitura não substitui produção '
                            'oral. Para desenvolver conversação, é preciso falar com frequência.</p>',
                            '<h3>2. Ouvir muito, mas não responder</h3>',
                            '<p>Assistir séries, vídeos e podcasts pode ajudar, mas se o aluno só '
                            'consome conteúdo, o inglês continua passivo. Ele entende algumas coisas, '
                            'mas não treina formular respostas.</p>',
                            '<h3>3. Escrever sem receber correção</h3>',
                            '<p>A escrita ajuda muito, mas precisa de feedback. Caso contrário, o '
                            'aluno pode repetir erros de estrutura, vocabulário ou tradução literal '
                            'sem perceber.</p>',
                            '<h3>4. Falar sempre os mesmos assuntos</h3>',
                            '<p>Muitos alunos conseguem se apresentar, falar da rotina e pedir '
                            'informações, mas travam em temas profissionais. Isso acontece porque não '
                            'praticam novos contextos.</p>',
                            '<h3>5. Não saber qual habilidade priorizar por nível</h3>',
                            '<p>Um aluno A1 precisa de um plano diferente de um aluno B2. Sem '
                            'diagnóstico, ele pode estudar conteúdo fácil demais, difícil demais ou '
                            'desalinhado com seu objetivo.</p>',
                            '<p>Um curso de inglês online ao vivo ajuda justamente porque organiza '
                            'esse caminho. O aluno sabe seu nível, pratica com professor, recebe '
                            'correção e entende qual habilidade precisa de mais atenção em cada '
                            'etapa.</p>',
                            '<p>CTA: Quer saber qual habilidade mais trava seu inglês hoje? Faça o '
                            'teste de nível grátis em <a '
                            'href="/curso-de-ingles-online">https://vediums.com/</a> e descubra seu '
                            'próximo passo com aulas ao vivo.</p>']},
                  {'heading': 'Como montar um plano integrado de inglês?',
                   'body': ['<p>Para montar um plano integrado, escolha um tema por semana e pratique '
                            'as quatro habilidades em torno dele. Isso dá foco, cria repetição '
                            'inteligente e evita a sensação de estudar coisas aleatórias.</p>',
                            '<p>O método é simples:</p>',
                            '<ol><li>Escolha um tema real.</li><li>Leia algo curto sobre o '
                            'tema.</li><li>Ouça um áudio ou vídeo relacionado.</li><li>Fale sobre o '
                            'tema em frases ou conversa.</li><li>Escreva um pequeno texto usando o '
                            'vocabulário.</li><li>Leve dúvidas para aula ao vivo.</li><li>Revise e '
                            'repita com outro tema.</li></ol>',
                            '<p>Exemplos de temas úteis:</p>',
                            '<ul><li>apresentação pessoal;</li><li>rotina de '
                            'trabalho;</li><li>reunião;</li><li>entrevista de '
                            'emprego;</li><li>viagem;</li><li>e-mail profissional;</li><li>atendimento '
                            'ao cliente;</li><li>networking;</li><li>apresentação de '
                            'projeto;</li><li>opiniões e argumentos;</li><li>planos '
                            'futuros;</li><li>experiências passadas.</li></ul>',
                            '<p>O segredo é não estudar reading em um universo, listening em outro, '
                            'speaking em outro e writing em outro. O mesmo tema deve atravessar todas '
                            'as habilidades.</p>',
                            '<p>Veja um exemplo com o tema “reunião de trabalho”:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Habilidade</th><th>Atividade</th></tr></thead><tbody><tr><td>Leitura</td><td>Ler '
                            'um texto curto sobre como participar de reuniões em '
                            'inglês</td></tr><tr><td>Escuta</td><td>Ouvir um diálogo de reunião com '
                            'frases como “Can we align the next '
                            'steps?”</td></tr><tr><td>Fala</td><td>Praticar respostas para concordar, '
                            'discordar e fazer perguntas</td></tr><tr><td>Escrita</td><td>Escrever um '
                            'resumo da reunião ou um e-mail de follow-up</td></tr></tbody></table>',
                            '<p>Esse modelo prepara o aluno para usar o inglês de forma completa. Não '
                            'é estudo por estudo. É prática aplicada.</p>']},
                  {'heading': 'Como combinar leitura e escuta?',
                   'body': ['<p>Leitura e escuta devem trabalhar juntas porque a leitura mostra a '
                            'forma da palavra e a escuta mostra como ela soa. Muitos brasileiros '
                            'reconhecem uma palavra escrita, mas não entendem quando ela aparece em '
                            'fala natural. Isso acontece porque o inglês falado tem ritmo, redução de '
                            'sons, ligação entre palavras e entonação.</p>',
                            '<p>Uma rotina eficiente é:</p>',
                            '<ol><li>Leia um texto curto.</li><li>Marque palavras '
                            'novas.</li><li>Escute um áudio sobre o mesmo tema.</li><li>Identifique '
                            'palavras que já apareceram na leitura.</li><li>Repita frases importantes '
                            'em voz alta.</li></ol>',
                            '<p>Por exemplo, se você está estudando “job interview”, pode ler um texto '
                            'com frases como:</p>',
                            '<ul><li>“Tell me about yourself.”</li><li>“What are your '
                            'strengths?”</li><li>“Why are you interested in this '
                            'position?”</li><li>“Can you describe a challenge you faced?”</li></ul>',
                            '<p>Depois, ouça um diálogo de entrevista e tente identificar essas '
                            'estruturas. Ao fazer isso, você conecta forma escrita e som real.</p>',
                            '<p>Para alunos A1 e A2, os textos e áudios devem ser curtos. Para B1 e '
                            'B2, já é possível usar vídeos, podcasts lentos, notícias adaptadas e '
                            'materiais profissionais. Para C1, o aluno pode trabalhar com artigos, '
                            'entrevistas longas e debates.</p>']},
                  {'heading': 'Como transformar leitura e escuta em fala?',
                   'body': ['<p>Para transformar leitura e escuta em fala, você precisa produzir '
                            'frases logo depois de consumir conteúdo. Não espere “aprender tudo” para '
                            'começar a falar. O ideal é usar o vocabulário do dia em respostas '
                            'curtas.</p>',
                            '<p>Depois de ler e ouvir sobre um tema, responda perguntas como:</p>',
                            '<ul><li>What is the main idea?</li><li>What did you learn?</li><li>Do you '
                            'agree or disagree?</li><li>How does this apply to your work?</li><li>Can '
                            'you give an example?</li><li>What would you say in this '
                            'situation?</li></ul>',
                            '<p>Se o tema for entrevista de emprego, pratique:</p>',
                            '<ul><li>“I have experience in...”</li><li>“My main strength '
                            'is...”</li><li>“I’m interested in this position because...”</li><li>“One '
                            'challenge I faced was...”</li><li>“I solved this problem by...”</li></ul>',
                            '<p>O aluno deve falar mesmo com frases simples. A conversação melhora '
                            'quando o cérebro aprende a recuperar palavras rapidamente. Isso acontece '
                            'pela prática, não pela espera.</p>',
                            '<p>Em uma aula ao vivo, o professor pode transformar o mesmo conteúdo em '
                            'perguntas, role-play e correção. Esse é o ponto em que o inglês online ao '
                            'vivo se destaca: você não apenas consome frases, você precisa responder, '
                            'ajustar e tentar de novo.</p>']},
                  {'heading': 'Como usar a escrita para melhorar a fala?',
                   'body': ['<p>A escrita melhora a fala porque ajuda a organizar ideias antes da '
                            'conversa. Muitos alunos travam não apenas por falta de vocabulário, mas '
                            'porque não sabem estruturar o que querem dizer. Escrever pequenos textos '
                            'ajuda a criar repertório.</p>',
                            '<p>Depois de praticar um tema, escreva:</p>',
                            '<ul><li>5 frases sobre o assunto;</li><li>um parágrafo curto;</li><li>um '
                            'e-mail simples;</li><li>um resumo de áudio;</li><li>uma opinião com '
                            'justificativa;</li><li>perguntas para uma conversa.</li></ul>',
                            '<p>Exemplo com tema “rotina de trabalho”:</p>',
                            '<p><strong>Texto curto:</strong></p>',
                            '<p>“I work from Monday to Friday. I usually start at 9 a.m. and finish at '
                            '6 p.m. I have meetings in the morning and I answer emails in the '
                            'afternoon. I want to improve my English because I need to speak with '
                            'international clients.”</p>',
                            '<p>Depois, transforme esse texto em fala. Leia em voz alta, grave sua voz '
                            'e tente repetir sem olhar. Esse exercício cria ponte entre writing e '
                            'speaking.</p>',
                            '<p>Para alunos intermediários, a escrita pode evoluir para:</p>',
                            '<ul><li>e-mails profissionais;</li><li>resumos de '
                            'reuniões;</li><li>mensagens no LinkedIn;</li><li>respostas de '
                            'entrevista;</li><li>apresentações curtas;</li><li>opiniões sobre temas de '
                            'trabalho.</li></ul>',
                            '<p>A escrita não deve ser um exercício isolado. Ela deve preparar o aluno '
                            'para falar melhor e comunicar ideias com mais clareza.</p>']},
                  {'heading': 'Plano semanal para combinar as quatro habilidades',
                   'body': ['<p>Um plano semanal eficaz pode ser simples. O aluno não precisa estudar '
                            'horas por dia. Precisa ter consistência e clareza.</p>',
                            '<h3>Segunda-feira: leitura guiada</h3>',
                            '<p>Escolha um texto curto no seu nível. Leia uma vez para entender a '
                            'ideia geral. Depois, leia novamente e marque palavras úteis. Não tente '
                            'traduzir tudo.</p>',
                            '<p>Objetivo: ampliar vocabulário e reconhecer estruturas.</p>',
                            '<h3>Terça-feira: escuta relacionada</h3>',
                            '<p>Ouça um áudio ou vídeo sobre o mesmo tema. Pode ser curto, de 2 a 5 '
                            'minutos. O foco é identificar palavras e frases que apareceram na '
                            'leitura.</p>',
                            '<p>Objetivo: conectar texto escrito ao som real.</p>',
                            '<h3>Quarta-feira: fala curta</h3>',
                            '<p>Responda de 3 a 5 perguntas sobre o tema. Grave sua voz ou pratique em '
                            'aula ao vivo.</p>',
                            '<p>Objetivo: transformar vocabulário em conversação.</p>',
                            '<h3>Quinta-feira: escrita prática</h3>',
                            '<p>Escreva um parágrafo, mensagem ou e-mail usando as palavras da '
                            'semana.</p>',
                            '<p>Objetivo: consolidar gramática e clareza.</p>',
                            '<h3>Sexta-feira: revisão ativa</h3>',
                            '<p>Revise sem olhar as respostas. Tente lembrar vocabulário, frases e '
                            'ideias. Depois, confira e corrija.</p>',
                            '<p>Objetivo: fortalecer memória.</p>',
                            '<h3>Sábado ou domingo: aula ao vivo</h3>',
                            '<p>Use a aula para praticar conversação, tirar dúvidas, receber feedback '
                            'e conectar o tema ao seu nível CEFR.</p>',
                            '<p>Objetivo: corrigir, falar e avançar com direção.</p>',
                            '<p>Esse modelo é sustentável para quem trabalha ou estuda. Ele evita '
                            'maratonas e cria progresso constante.</p>']},
                  {'heading': 'Como adaptar o plano ao nível CEFR?',
                   'body': ['<p>O nível CEFR ajuda a ajustar dificuldade, tema e expectativa. O mesmo '
                            'método funciona para todos os níveis, mas o tamanho das tarefas muda.</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Nível</th><th>Leitura</th><th>Escuta</th><th>Fala</th><th>Escrita</th></tr></thead><tbody><tr><td>A1</td><td>Frases '
                            'curtas</td><td>Áudios lentos</td><td>Apresentação simples</td><td>5 '
                            'frases básicas</td></tr><tr><td>A2</td><td>Textos curtos</td><td>Diálogos '
                            'previsíveis</td><td>Rotina e necessidades</td><td>Parágrafo '
                            'simples</td></tr><tr><td>B1</td><td>Artigos adaptados</td><td>Vídeos '
                            'curtos</td><td>Opiniões simples</td><td>E-mails e '
                            'resumos</td></tr><tr><td>B2</td><td>Textos profissionais</td><td>Podcasts '
                            'e reuniões</td><td>Argumentação</td><td>Relatórios e mensagens '
                            'formais</td></tr><tr><td>C1</td><td>Artigos complexos</td><td>Debates e '
                            'entrevistas</td><td>Fluidez em temas abstratos</td><td>Escrita avançada e '
                            'estratégica</td></tr></tbody></table>',
                            '<p>Um aluno A1 não deve tentar debater economia internacional em inglês. '
                            'Um aluno B2 não deve ficar apenas repetindo “my name is”. O plano precisa '
                            'respeitar o nível atual e empurrar o aluno um passo acima, sem '
                            'sobrecarregar.</p>',
                            '<p>Por isso, fazer um teste de nível é importante. Ele mostra onde você '
                            'está e evita perda de tempo.</p>']},
                  {'heading': 'Como praticar de forma objetiva?',
                   'body': ['<p>Praticar de forma objetiva significa definir uma tarefa pequena para '
                            'cada habilidade. Não diga apenas “vou estudar inglês”. Diga exatamente o '
                            'que fará.</p>',
                            '<p>Exemplos:</p>',
                            '<table class="vd-table"><thead><tr><th>Habilidade</th><th>Prática '
                            'objetiva</th></tr></thead><tbody><tr><td>Leitura</td><td>Ler um texto de '
                            '300 palavras e marcar 8 expressões</td></tr><tr><td>Escuta</td><td>Ouvir '
                            '3 minutos e anotar 5 palavras '
                            'reconhecidas</td></tr><tr><td>Fala</td><td>Gravar 1 minuto respondendo '
                            'uma pergunta</td></tr><tr><td>Escrita</td><td>Escrever um e-mail de 80 '
                            'palavras</td></tr><tr><td>Revisão</td><td>Repetir 10 frases sem '
                            'consultar</td></tr></tbody></table>',
                            '<p>Esse formato reduz dispersão. O aluno sabe quando começou, o que '
                            'precisa fazer e quando terminou.</p>',
                            '<p>Outra dica é usar sempre o mesmo tema durante a semana. Isso permite '
                            'repetir palavras em situações diferentes. A repetição em contexto é mais '
                            'eficiente do que estudar temas aleatórios todos os dias.</p>']},
                  {'heading': 'Exemplo prático: tema “entrevista de emprego”',
                   'body': ['<p>Veja como combinar as quatro habilidades no tema “entrevista de '
                            'emprego”:</p>',
                            '<h3>Leitura</h3>',
                            '<p>Leia um texto sobre perguntas comuns em entrevistas. Marque expressões '
                            'como:</p>',
                            '<ul><li>strengths;</li><li>weaknesses;</li><li>experience;</li><li>position;</li><li>challenge;</li><li>achievement;</li><li>teamwork;</li><li>leadership.</li></ul>',
                            '<h3>Escuta</h3>',
                            '<p>Ouça um diálogo de entrevista e identifique perguntas como:</p>',
                            '<ul><li>“Tell me about yourself.”</li><li>“Why do you want this '
                            'job?”</li><li>“What are your strengths?”</li><li>“Can you describe a '
                            'challenge?”</li></ul>',
                            '<h3>Fala</h3>',
                            '<p>Pratique respostas:</p>',
                            '<ul><li>“I have experience in customer service.”</li><li>“My main '
                            'strength is communication.”</li><li>“I want this position '
                            'because...”</li><li>“One challenge I faced was...”</li></ul>',
                            '<h3>Escrita</h3>',
                            '<p>Escreva um pequeno texto:</p>',
                            '<p>“I am interested in this position because I want to grow '
                            'professionally. I have experience in project management and I enjoy '
                            'working with teams. One of my strengths is solving problems under '
                            'pressure.”</p>',
                            '<h3>Aula ao vivo</h3>',
                            '<p>Na aula, peça para o professor simular uma entrevista. Você responde, '
                            'recebe correção e tenta novamente.</p>',
                            '<p>Esse processo é muito mais completo do que apenas decorar perguntas de '
                            'entrevista. Ele cria vocabulário, escuta, fala e escrita em torno de uma '
                            'necessidade real.</p>']},
                  {'heading': 'Próximo passo no curso ao vivo',
                   'body': ['<p>O próximo passo no curso ao vivo é transformar o plano integrado em '
                            'acompanhamento. Estudar sozinho pode funcionar por um tempo, mas o aluno '
                            'muitas vezes não sabe se está pronunciando bem, escrevendo naturalmente '
                            'ou avançando no nível certo.</p>',
                            '<p>Em uma aula de inglês online ao vivo, você pode:</p>',
                            '<ul><li>praticar conversação com professor e turma;</li><li>receber '
                            'correção de pronúncia e estrutura;</li><li>trabalhar temas do seu '
                            'objetivo profissional;</li><li>acompanhar evolução por nível '
                            'CEFR;</li><li>tirar dúvidas na hora;</li><li>ganhar '
                            'constância;</li><li>sair do estudo passivo.</li></ul>',
                            '<p>Na Vedium, as aulas são ao vivo, com foco em evolução real e sem '
                            'contrato de fidelidade. Você continua porque percebe resultado, não '
                            'porque está preso a uma obrigação longa.</p>',
                            '<p>CTA: Faça o teste de nível grátis em <a '
                            'href="/teste-de-nivel-ingles">https://vediums.com/</a> e descubra como '
                            'combinar leitura, escuta, fala e escrita em um plano de inglês ao vivo '
                            'feito para seu momento.</p>']},
                  {'heading': 'Conclusão com CTA forte',
                   'body': ['<p>Combinar leitura, escuta, fala e escrita no mesmo plano é a forma mais '
                            'inteligente de estudar inglês porque aproxima o aprendizado da vida real. '
                            'Você lê para ganhar repertório, escuta para entender o som, fala para '
                            'criar confiança e escreve para organizar ideias. Quando essas quatro '
                            'habilidades trabalham juntas, o inglês deixa de ser conteúdo solto e vira '
                            'comunicação.</p>',
                            '<p>Para quem busca crescimento profissional, viagens, estudos ou '
                            'oportunidades internacionais, esse equilíbrio é essencial. Não basta '
                            'entender textos se você não fala. Não basta assistir vídeos se você não '
                            'escreve. Não basta decorar regras se você não usa o idioma.</p>',
                            '<p>A Vedium oferece inglês online ao vivo, com prática de conversação, '
                            'acompanhamento por nível CEFR e liberdade para estudar sem fidelidade. '
                            'Você aprende com gente real, em tempo real, e fica porque sente '
                            'evolução.</p>',
                            '<p>Faça seu teste de nível grátis em <a '
                            'href="/curso-de-ingles-online">https://vediums.com/</a> e comece a montar '
                            'um plano de inglês completo, prático e conectado ao seu objetivo.</p>']}],
     'faqs': [{'q': 'É melhor estudar leitura, escuta, fala e escrita separadamente ou juntas?',
               'a': 'O ideal é combinar as quatro habilidades em torno do mesmo tema. Isso cria '
                    'repetição em contextos diferentes e ajuda o aluno a transformar vocabulário '
                    'passivo em comunicação real.'},
              {'q': 'Como melhorar a conversação usando leitura e escuta?',
               'a': 'Leia e escute conteúdos sobre o mesmo tema, marque frases úteis e depois responda '
                    'perguntas em voz alta. Em aula ao vivo, use esse material para conversar e '
                    'receber correção.'},
              {'q': 'A escrita ajuda a falar melhor em inglês?',
               'a': 'Sim. A escrita organiza ideias, fortalece gramática e cria repertório. Quando '
                    'você escreve frases e depois as pratica em voz alta, melhora a clareza e ganha '
                    'mais segurança para falar.'},
              {'q': 'Como o nível CEFR ajuda no plano de estudos?',
               'a': 'O nível CEFR mostra o que o aluno já consegue fazer e qual deve ser o próximo '
                    'passo. Ele ajuda a escolher textos, áudios, temas de conversação e tarefas de '
                    'escrita adequados ao nível.'},
              {'q': 'A Vedium oferece inglês online ao vivo?',
               'a': 'Sim. A Vedium oferece aulas de inglês online ao vivo, com conversação, evolução '
                    'por nível, prática real e sem contrato de fidelidade. O aluno continua porque '
                    'percebe resultado.'}],
     'cta_title': 'Quer saber seu nível real de inglês?',
     'cta_text': 'Faça o teste de nível grátis da Vedium e descubra por onde começar.',
     'cta_label': 'Conhecer o curso de Inglês',
     'cta_url': '/curso-de-ingles-online'},
    "ingles-para-quem-quer-estudar-fora-vocabulario-academico-inicial": {'title': 'Inglês para quem quer estudar fora: vocabulário acadêmico inicial',
     'meta_description': 'Aprenda o vocabulário acadêmico inicial em inglês para estudar fora, '
                         'participar de aulas, escrever e falar com confiança.',
     'h1': 'Inglês para quem quer estudar fora: vocabulário acadêmico inicial',
     'date': '2026-06-22',
     'date_display': '22 de junho de 2026',
     'hero_image': 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aula de inglês na Vedium',
     'tag': 'Inglês',
     'category': 'ingles',
     'lead': 'Quem quer estudar fora precisa de inglês acadêmico inicial para entender aulas, '
             'participar de discussões, escrever trabalhos, falar com professores, apresentar ideias e '
             'lidar com a rotina de uma universidade internacional. O ponto principal é simples: não '
             'basta saber inglês “de viagem” ou frases básicas de conversação. Para estudar em outro '
             'país, você precisa construir um vocabulário voltado a sala de aula, pesquisa, '
             'avaliações, prazos, orientação acadêmica e comunicação formal.',
     'sections': [{'heading': '',
                   'body': ['<p>Esse tema é especialmente importante para brasileiros que estão '
                            'planejando intercâmbio, graduação, pós-graduação, curso técnico, MBA, '
                            'especialização ou até programas de curta duração no exterior. Muitas '
                            'pessoas conseguem se virar em situações turísticas, mas travam quando '
                            'precisam dizer “entregar um trabalho”, “participar de um seminário”, '
                            '“pedir feedback”, “citar uma fonte”, “revisar um rascunho” ou “marcar uma '
                            'reunião com o orientador”.</p>',
                            '<p>O objetivo deste artigo é mostrar o vocabulário acadêmico inicial mais '
                            'útil para quem quer estudar fora, explicar por que essa área trava tantos '
                            'alunos e indicar como praticar de forma objetiva. A Vedium oferece inglês '
                            'online ao vivo, com foco em conversação, evolução por nível CEFR e '
                            'prática real para quem precisa usar o idioma na carreira, nos estudos e '
                            'em oportunidades internacionais.</p>']},
                  {'heading': 'Por que o inglês acadêmico é diferente do inglês comum?',
                   'body': ['<p>O inglês acadêmico é diferente porque exige precisão, organização de '
                            'ideias, leitura crítica, vocabulário formal e capacidade de participar de '
                            'situações educacionais específicas. Você não usa apenas frases de '
                            'sobrevivência. Você precisa acompanhar explicações, fazer perguntas, '
                            'defender opiniões, escrever com estrutura e compreender instruções de '
                            'professores.</p>',
                            '<p>No inglês comum, você pode dizer frases como:</p>',
                            '<ul><li>“I want coffee.”</li><li>“Where is the station?”</li><li>“I’m '
                            'from Brazil.”</li><li>“Can you help me?”</li></ul>',
                            '<p>Essas frases ajudam em viagens, mas não bastam para estudar fora. Em '
                            'uma universidade, você precisa entender e usar frases como:</p>',
                            '<ul><li>“When is the assignment due?”</li><li>“Could you clarify the '
                            'grading criteria?”</li><li>“I would like to schedule a meeting with my '
                            'advisor.”</li><li>“The main argument of the article is...”</li><li>“I '
                            'need to revise my draft before submission.”</li></ul>',
                            '<p>Perceba a diferença: o contexto acadêmico pede vocabulário de tarefas, '
                            'avaliação, pesquisa, leitura, escrita e interação institucional.</p>',
                            '<p>Para quem está entre A2, B1 ou B2 no nível CEFR, esse salto pode '
                            'assustar. O aluno até entende conversas simples, mas sente insegurança '
                            'quando entra em um contexto mais formal. Por isso, o inglês acadêmico '
                            'precisa ser treinado de forma gradual, com palavras e situações reais, '
                            'não apenas com listas soltas.</p>']},
                  {'heading': 'Quando esse vocabulário se torna essencial?',
                   'body': ['<p>Esse vocabulário se torna essencial antes mesmo de você chegar ao '
                            'exterior. Ele aparece em e-mails de candidatura, entrevistas, '
                            'formulários, aulas online, reuniões de orientação, instruções de '
                            'matrícula e comunicação com universidades.</p>',
                            '<p>Você vai precisar dele em momentos como:</p>',
                            '<ul><li>inscrição em programas internacionais;</li><li>entrevista com '
                            'universidade ou bolsa;</li><li>leitura de edital e '
                            'requisitos;</li><li>envio de documentos;</li><li>contato com admissions '
                            'office;</li><li>escolha de disciplinas;</li><li>primeira semana de '
                            'aula;</li><li>trabalhos escritos;</li><li>apresentações;</li><li>feedback '
                            'de professor;</li><li>reuniões com orientador;</li><li>provas e '
                            'avaliações.</li></ul>',
                            '<p>Se você espera chegar ao exterior para começar a aprender esse '
                            'vocabulário, corre o risco de enfrentar estresse desnecessário. O melhor '
                            'caminho é preparar o terreno antes: entender as palavras mais usadas, '
                            'praticar perguntas acadêmicas e treinar conversação ao vivo para ganhar '
                            'segurança.</p>',
                            '<p>CTA: Quer saber se seu inglês está pronto para estudar fora? Faça o '
                            'teste de nível grátis em <a '
                            'href="/curso-de-ingles-online">https://vediums.com/</a> e descubra o '
                            'próximo passo no inglês online ao vivo da Vedium.</p>']},
                  {'heading': 'Vocabulário acadêmico inicial: sala de aula e rotina',
                   'body': ['<p>O primeiro grupo de palavras envolve a rotina de aula. Esse '
                            'vocabulário aparece desde o primeiro dia em uma escola, faculdade ou '
                            'universidade internacional.</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Inglês</th><th>Português</th><th>Exemplo</th></tr></thead><tbody><tr><td>class</td><td>aula</td><td>I '
                            'have class at 9 a.m.</td></tr><tr><td>course</td><td>curso / '
                            'disciplina</td><td>I’m taking a course in '
                            'economics.</td></tr><tr><td>subject</td><td>matéria / '
                            'assunto</td><td>This subject is '
                            'difficult.</td></tr><tr><td>lecture</td><td>aula expositiva / '
                            'palestra</td><td>The lecture starts at '
                            '10.</td></tr><tr><td>seminar</td><td>seminário</td><td>We have a seminar '
                            'on Friday.</td></tr><tr><td>workshop</td><td>oficina / aula '
                            'prática</td><td>The workshop is '
                            'mandatory.</td></tr><tr><td>syllabus</td><td>plano de curso</td><td>The '
                            'syllabus explains the '
                            'assignments.</td></tr><tr><td>schedule</td><td>horário / '
                            'cronograma</td><td>The schedule '
                            'changed.</td></tr><tr><td>attendance</td><td>presença</td><td>Attendance '
                            'is required.</td></tr><tr><td>deadline</td><td>prazo</td><td>The deadline '
                            'is next Monday.</td></tr></tbody></table>',
                            '<p>Frases úteis:</p>',
                            '<ul><li>“What time does the class start?”</li><li>“Is attendance '
                            'mandatory?”</li><li>“Where can I find the syllabus?”</li><li>“Has the '
                            'schedule changed?”</li><li>“When is the deadline?”</li></ul>',
                            '<p>Essas frases parecem simples, mas fazem diferença. Em vez de ficar '
                            'perdido, você consegue confirmar informações essenciais.</p>']},
                  {'heading': 'Vocabulário para trabalhos, provas e avaliação',
                   'body': ['<p>O segundo grupo envolve tarefas acadêmicas. Quem estuda fora precisa '
                            'entender rapidamente o que deve entregar, como será avaliado e quais '
                            'critérios serão usados.</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Inglês</th><th>Português</th><th>Exemplo</th></tr></thead><tbody><tr><td>assignment</td><td>trabalho '
                            '/ tarefa</td><td>The assignment is due '
                            'tomorrow.</td></tr><tr><td>homework</td><td>lição de casa</td><td>I need '
                            'to finish my homework.</td></tr><tr><td>essay</td><td>redação acadêmica / '
                            'ensaio</td><td>The essay must have 1,500 '
                            'words.</td></tr><tr><td>paper</td><td>artigo / trabalho '
                            'escrito</td><td>I’m writing a paper about '
                            'education.</td></tr><tr><td>exam</td><td>prova</td><td>The final exam is '
                            'in June.</td></tr><tr><td>test</td><td>teste</td><td>We have a test next '
                            'week.</td></tr><tr><td>grade</td><td>nota</td><td>I received a good '
                            'grade.</td></tr><tr><td>grading criteria</td><td>critérios de '
                            'avaliação</td><td>Could you explain the grading '
                            'criteria?</td></tr><tr><td>feedback</td><td>retorno / comentário '
                            'avaliativo</td><td>I need feedback on my '
                            'draft.</td></tr><tr><td>submission</td><td>entrega / envio</td><td>The '
                            'submission is online.</td></tr></tbody></table>',
                            '<p>Frases essenciais:</p>',
                            '<ul><li>“When is the assignment due?”</li><li>“How many words should the '
                            'essay have?”</li><li>“Can I submit it online?”</li><li>“Could you give me '
                            'feedback on my draft?”</li><li>“What are the grading criteria?”</li></ul>',
                            '<p>No Brasil, muitos alunos estão acostumados a perguntar informalmente '
                            'para colegas. Em universidades internacionais, especialmente em contextos '
                            'mais formais, saber perguntar diretamente ao professor ou à secretaria '
                            'acadêmica é uma habilidade importante.</p>']},
                  {'heading': 'Vocabulário para leitura, pesquisa e fontes',
                   'body': ['<p>O terceiro grupo é fundamental para quem vai ler artigos, escrever '
                            'trabalhos e participar de discussões acadêmicas.</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Inglês</th><th>Português</th><th>Exemplo</th></tr></thead><tbody><tr><td>article</td><td>artigo</td><td>I '
                            'read an article about climate '
                            'policy.</td></tr><tr><td>source</td><td>fonte</td><td>You need reliable '
                            'sources.</td></tr><tr><td>reference</td><td>referência</td><td>Add the '
                            'references at the '
                            'end.</td></tr><tr><td>citation</td><td>citação</td><td>This citation '
                            'needs a page '
                            'number.</td></tr><tr><td>research</td><td>pesquisa</td><td>My research '
                            'focuses on public '
                            'health.</td></tr><tr><td>topic</td><td>tema</td><td>What is your research '
                            'topic?</td></tr><tr><td>argument</td><td>argumento</td><td>The author’s '
                            'argument is '
                            'strong.</td></tr><tr><td>evidence</td><td>evidência</td><td>You need more '
                            'evidence.</td></tr><tr><td>data</td><td>dados</td><td>The data supports '
                            'the conclusion.</td></tr><tr><td>conclusion</td><td>conclusão</td><td>The '
                            'conclusion is clear.</td></tr></tbody></table>',
                            '<p>Frases úteis:</p>',
                            '<ul><li>“What is the main argument of the article?”</li><li>“Which '
                            'sources should I use?”</li><li>“Do I need more evidence?”</li><li>“How '
                            'should I cite this reference?”</li><li>“My research topic is related to '
                            'technology.”</li></ul>',
                            '<p>Esse vocabulário ajuda o aluno a sair da leitura passiva. Ele passa a '
                            'conseguir comentar textos, fazer perguntas e participar de debates.</p>']},
                  {'heading': 'Vocabulário para apresentações e participação oral',
                   'body': ['<p>Estudar fora quase sempre envolve apresentações, debates, trabalhos em '
                            'grupo e participação em aula. Aqui entra a conversação acadêmica, uma das '
                            'áreas que mais travam alunos brasileiros.</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Inglês</th><th>Português</th><th>Exemplo</th></tr></thead><tbody><tr><td>presentation</td><td>apresentação</td><td>I '
                            'have a presentation tomorrow.</td></tr><tr><td>group '
                            'project</td><td>trabalho em grupo</td><td>We are working on a group '
                            'project.</td></tr><tr><td>discussion</td><td>discussão / '
                            'debate</td><td>The discussion was '
                            'interesting.</td></tr><tr><td>question</td><td>pergunta</td><td>I have a '
                            'question.</td></tr><tr><td>opinion</td><td>opinião</td><td>In my opinion, '
                            'this is important.</td></tr><tr><td>point of view</td><td>ponto de '
                            'vista</td><td>From my point of '
                            'view...</td></tr><tr><td>topic</td><td>tópico</td><td>Today’s topic is '
                            'culture.</td></tr><tr><td>slide</td><td>slide</td><td>The next slide '
                            'shows the results.</td></tr><tr><td>summary</td><td>resumo</td><td>I’ll '
                            'give a short '
                            'summary.</td></tr><tr><td>conclusion</td><td>conclusão</td><td>In '
                            'conclusion, we need more research.</td></tr></tbody></table>',
                            '<p>Frases para participar:</p>',
                            '<ul><li>“I have a question about the reading.”</li><li>“Could you explain '
                            'this point again?”</li><li>“In my opinion, the author is '
                            'right.”</li><li>“I agree with your point.”</li><li>“I’m not sure I '
                            'understood the question.”</li><li>“Can I add something?”</li><li>“The '
                            'main point of my presentation is...”</li></ul>',
                            '<p>O aluno não precisa esperar ter inglês perfeito para participar. Ele '
                            'precisa de blocos de fala que permitam entrar na conversa com '
                            'segurança.</p>']},
                  {'heading': 'Por que isso trava o aluno?',
                   'body': ['<p>Isso trava o aluno porque ele tenta estudar fora usando o mesmo inglês '
                            'que aprendeu para situações gerais. Ele sabe cumprimentar, pedir comida, '
                            'falar de rotina e talvez responder perguntas simples, mas não treinou o '
                            'idioma usado em ambiente acadêmico.</p>',
                            '<p>Os principais bloqueios são:</p>',
                            '<h3>Falta de vocabulário específico</h3>',
                            '<p>O aluno conhece “work”, mas não conhece “assignment”, “paper”, '
                            '“deadline”, “draft” e “submission”. Como resultado, não entende '
                            'instruções importantes.</p>',
                            '<h3>Medo de falar em sala</h3>',
                            '<p>Mesmo alunos intermediários podem travar quando precisam participar de '
                            'uma discussão. O medo de errar na frente de colegas internacionais '
                            'aumenta a ansiedade.</p>',
                            '<h3>Dificuldade com perguntas formais</h3>',
                            '<p>Perguntar “What is this?” pode ser fácil. Mas dizer “Could you clarify '
                            'the grading criteria?” exige repertório mais específico.</p>',
                            '<h3>Pouca prática de escuta acadêmica</h3>',
                            '<p>A fala de professores, apresentações e seminários pode ser mais longa, '
                            'mais rápida e mais estruturada do que diálogos de aplicativo.</p>',
                            '<h3>Falta de feedback</h3>',
                            '<p>O aluno estuda sozinho, mas não sabe se está pronunciando bem, se a '
                            'frase soa natural ou se está usando um tom adequado.</p>',
                            '<p>A solução não é decorar 500 palavras de uma vez. O caminho é aprender '
                            'vocabulário por situação, praticar frases úteis e fazer aulas ao vivo '
                            'para transformar conhecimento em uso real.</p>']},
                  {'heading': 'Como praticar de forma objetiva?',
                   'body': ['<p>Para praticar de forma objetiva, escolha uma situação acadêmica por '
                            'vez e treine o vocabulário dentro de frases completas. Não memorize '
                            'palavras isoladas. Transforme cada palavra em uma ação que você realmente '
                            'precisará fazer.</p>',
                            '<p>Veja um método simples:</p>',
                            '<h3>Passo 1: escolha uma situação</h3>',
                            '<p>Exemplos:</p>',
                            '<ul><li>pedir feedback;</li><li>confirmar prazo;</li><li>perguntar sobre '
                            'critérios de avaliação;</li><li>participar de '
                            'discussão;</li><li>apresentar um trabalho;</li><li>escrever e-mail para '
                            'professor;</li><li>falar com orientador;</li><li>explicar tema de '
                            'pesquisa.</li></ul>',
                            '<h3>Passo 2: selecione 10 palavras úteis</h3>',
                            '<p>Se o tema for “entrega de trabalho”, as palavras podem ser:</p>',
                            '<ul><li>assignment;</li><li>deadline;</li><li>submission;</li><li>draft;</li><li>feedback;</li><li>grading '
                            'criteria;</li><li>essay;</li><li>paper;</li><li>reference;</li><li>word '
                            'count.</li></ul>',
                            '<h3>Passo 3: crie frases reais</h3>',
                            '<p>Não escreva apenas a tradução. Escreva frases:</p>',
                            '<ul><li>“When is the assignment due?”</li><li>“Can I submit the draft by '
                            'email?”</li><li>“What is the word count?”</li><li>“Could you give me '
                            'feedback?”</li><li>“Do I need more references?”</li></ul>',
                            '<h3>Passo 4: pratique em voz alta</h3>',
                            '<p>Leia as frases em voz alta, grave sua voz e repita. O vocabulário '
                            'acadêmico precisa sair da página e virar fala.</p>',
                            '<h3>Passo 5: simule uma aula ao vivo</h3>',
                            '<p>Peça para um professor fazer perguntas realistas, como:</p>',
                            '<ul><li>“What is your research topic?”</li><li>“Can you summarize the '
                            'article?”</li><li>“What is your opinion?”</li><li>“How will you support '
                            'your argument?”</li></ul>',
                            '<p>Esse tipo de treino prepara o aluno para o ambiente real.</p>',
                            '<p>CTA: Na Vedium, você pode praticar inglês online ao vivo com foco no '
                            'seu objetivo. Faça o teste de nível grátis em <a '
                            'href="/teste-de-nivel-ingles">https://vediums.com/</a> e veja como '
                            'evoluir para estudar fora com mais confiança.</p>']},
                  {'heading': 'Como o nível CEFR ajuda quem quer estudar fora?',
                   'body': ['<p>O nível CEFR ajuda porque mostra o que o aluno consegue fazer em '
                            'inglês e qual distância existe entre o nível atual e o objetivo '
                            'acadêmico. Para estudar fora, muitas situações exigem pelo menos um nível '
                            'intermediário funcional, mas o ideal varia conforme o curso, o país e a '
                            'instituição.</p>',
                            '<p>De forma prática:</p>',
                            '<table class="vd-table"><thead><tr><th>Nível CEFR</th><th>Relação com '
                            'estudos no exterior</th></tr></thead><tbody><tr><td>A1</td><td>Entende '
                            'frases muito básicas, ainda insuficiente para estudo '
                            'acadêmico</td></tr><tr><td>A2</td><td>Consegue lidar com situações '
                            'simples, mas precisa evoluir muito para '
                            'aulas</td></tr><tr><td>B1</td><td>Começa a se comunicar com mais '
                            'autonomia em contextos previsíveis</td></tr><tr><td>B2</td><td>Participa '
                            'melhor de aulas, discussões e trabalhos '
                            'acadêmicos</td></tr><tr><td>C1</td><td>Lida com textos complexos, '
                            'apresentações e comunicação acadêmica avançada</td></tr></tbody></table>',
                            '<p>Quem quer estudar fora deve buscar clareza sobre seu nível. O aluno '
                            'pode estar em B1 para conversação geral, mas em A2 para escrita '
                            'acadêmica. Ou pode ter bom reading, mas travar no speaking. Por isso, um '
                            'teste de nível bem orientado é importante.</p>']},
                  {'heading': 'Vocabulário para e-mails acadêmicos',
                   'body': ['<p>E-mails são parte da rotina de quem estuda fora. Você vai escrever '
                            'para professores, secretaria, colegas, orientadores e departamentos.</p>',
                            '<p>Vocabulário útil:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Inglês</th><th>Português</th></tr></thead><tbody><tr><td>professor</td><td>professor '
                            'universitário</td></tr><tr><td>advisor</td><td>orientador</td></tr><tr><td>department</td><td>departamento</td></tr><tr><td>admissions '
                            'office</td><td>setor de '
                            'admissões</td></tr><tr><td>request</td><td>solicitação</td></tr><tr><td>appointment</td><td>reunião '
                            '/ '
                            'horário</td></tr><tr><td>availability</td><td>disponibilidade</td></tr><tr><td>attached</td><td>anexado</td></tr><tr><td>regarding</td><td>sobre '
                            '/ referente '
                            'a</td></tr><tr><td>sincerely</td><td>atenciosamente</td></tr></tbody></table>',
                            '<p>Modelo simples de e-mail:</p>',
                            '<p><strong>Subject:</strong> Question about the assignment</p>',
                            '<p><strong>Dear Professor Smith,</strong></p>',
                            '<p>I hope you are well. I have a question about the assignment due next '
                            'week. Could you clarify the grading criteria?</p>',
                            '<p>Thank you for your help.</p>',
                            '<p><strong>Sincerely,</strong><br>[Your name]</p>',
                            '<p>Esse modelo é simples, direto e educado. O importante é evitar '
                            'traduções literais do português e aprender estruturas comuns.</p>']},
                  {'heading': 'Vocabulário para falar com orientador ou professor',
                   'body': ['<p>Falar com professor ou orientador exige clareza e respeito. Você pode '
                            'usar frases como:</p>',
                            '<ul><li>“I would like to schedule a meeting.”</li><li>“I need help with '
                            'my research topic.”</li><li>“Could you give me feedback on my '
                            'draft?”</li><li>“I’m having difficulty understanding this '
                            'concept.”</li><li>“Do you have any recommendations?”</li><li>“What should '
                            'I focus on next?”</li><li>“Could you suggest some sources?”</li></ul>',
                            '<p>Essas frases são extremamente úteis para quem está em graduação, '
                            'pós-graduação ou programas acadêmicos de curta duração.</p>']},
                  {'heading': 'Próximo passo no curso ao vivo',
                   'body': ['<p>O próximo passo no curso ao vivo é transformar vocabulário acadêmico '
                            'em prática de conversação e produção real. Isso significa simular '
                            'situações que você encontrará fora do Brasil.</p>',
                            '<p>Em uma aula ao vivo, você pode treinar:</p>',
                            '<ul><li>apresentação pessoal acadêmica;</li><li>perguntas em '
                            'sala;</li><li>reunião com professor;</li><li>discussão sobre '
                            'artigo;</li><li>explicação de tema de pesquisa;</li><li>apresentação de '
                            'slides;</li><li>entrevista de admissão;</li><li>e-mail '
                            'acadêmico;</li><li>feedback sobre escrita.</li></ul>',
                            '<p>Esse tipo de prática é difícil de fazer sozinho. Você precisa de '
                            'alguém que corrija pronúncia, naturalidade, vocabulário e estrutura. A '
                            'aula ao vivo também cria constância, algo essencial para sair do estudo '
                            'passivo.</p>',
                            '<p>Na Vedium, o inglês é ensinado com prática real, evolução por nível e '
                            'sem fidelidade. Você não precisa se prender a contratos longos. Você '
                            'continua porque percebe que está avançando.</p>']},
                  {'heading': 'Plano de 4 semanas para começar o vocabulário acadêmico',
                   'body': ['<p>Aqui está um plano inicial para quem quer começar agora:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Semana</th><th>Foco</th><th>Prática</th></tr></thead><tbody><tr><td>1</td><td>Rotina '
                            'de aula</td><td>Aprender class, course, lecture, syllabus, '
                            'schedule</td></tr><tr><td>2</td><td>Trabalhos e '
                            'avaliação</td><td>Praticar assignment, deadline, essay, feedback, '
                            'grade</td></tr><tr><td>3</td><td>Pesquisa e leitura</td><td>Usar article, '
                            'source, evidence, argument, '
                            'reference</td></tr><tr><td>4</td><td>Conversação '
                            'acadêmica</td><td>Treinar perguntas, opiniões e apresentação '
                            'curta</td></tr></tbody></table>',
                            '<p>Em cada semana, faça três ações:</p>',
                            '<ol><li>Aprenda 10 palavras.</li><li>Crie 10 frases '
                            'próprias.</li><li>Pratique as frases em voz alta ou em aula ao '
                            'vivo.</li></ol>',
                            '<p>Essa rotina é mais eficiente do que tentar decorar uma lista enorme. O '
                            'vocabulário acadêmico precisa ser usado, não apenas reconhecido.</p>']},
                  {'heading': 'Conclusão com CTA forte',
                   'body': ['<p>Inglês para estudar fora exige mais do que frases básicas. Você '
                            'precisa de vocabulário acadêmico inicial para entender aulas, acompanhar '
                            'prazos, escrever trabalhos, falar com professores, participar de '
                            'discussões e se posicionar com confiança.</p>',
                            '<p>O segredo é começar pelas situações reais: sala de aula, trabalhos, '
                            'provas, pesquisa, apresentações, e-mails e reuniões com orientador. '
                            'Depois, transformar cada palavra em frase, cada frase em fala e cada fala '
                            'em prática ao vivo.</p>',
                            '<p>A Vedium oferece inglês online ao vivo para quem quer evoluir com '
                            'objetivo claro, seja para carreira, estudos internacionais ou crescimento '
                            'pessoal. As aulas têm prática real, acompanhamento por nível CEFR e '
                            'liberdade para continuar sem contrato de fidelidade. Você fica porque '
                            'sente resultado.</p>',
                            '<p>Faça seu teste de nível grátis em <a '
                            'href="/curso-de-ingles-online">https://vediums.com/</a> e descubra como '
                            'preparar seu inglês para estudar fora com mais segurança.</p>']}],
     'faqs': [{'q': 'Qual vocabulário em inglês é mais importante para estudar fora?',
               'a': 'O mais importante é o vocabulário de sala de aula, trabalhos, prazos, avaliação, '
                    'pesquisa, apresentações, e-mails e comunicação com professores. Palavras como '
                    'assignment, deadline, syllabus, feedback e research são essenciais.'},
              {'q': 'Preciso estar em qual nível CEFR para estudar fora?',
               'a': 'Depende do curso e da instituição, mas B2 costuma ser uma meta mais segura para '
                    'acompanhar aulas e participar melhor. Alunos em B1 podem começar a se preparar, '
                    'mas geralmente precisam fortalecer speaking, listening e escrita acadêmica.'},
              {'q': 'Como praticar inglês acadêmico sem estar no exterior?',
               'a': 'Você pode simular situações reais: apresentar um tema, discutir um artigo, '
                    'escrever e-mail para professor, pedir feedback e explicar um projeto. Aulas ao '
                    'vivo ajudam porque trazem correção e interação.'},
              {'q': 'Inglês acadêmico é só gramática avançada?',
               'a': 'Não. Inglês acadêmico envolve vocabulário, clareza, organização de ideias, '
                    'leitura, escrita, participação oral e comunicação formal. A gramática ajuda, mas '
                    'precisa estar conectada ao uso real.'},
              {'q': 'A Vedium ajuda quem quer estudar fora?',
               'a': 'Sim. A Vedium oferece inglês online ao vivo, com prática de conversação, evolução '
                    'por nível CEFR e foco em objetivos reais, como estudar fora, crescer na carreira '
                    'e ganhar confiança no idioma.'}],
     'cta_title': 'Quer saber seu nível real de inglês?',
     'cta_text': 'Faça o teste de nível grátis da Vedium e descubra por onde começar.',
     'cta_label': 'Conhecer o curso de Inglês',
     'cta_url': '/curso-de-ingles-online'},
    "como-a-pratica-constante-supera-maratonas-de-estudo-em-ingles": {'title': 'Como a prática constante supera maratonas de estudo em inglês',
     'meta_description': 'Entenda por que estudar inglês com constância supera maratonas e veja como '
                         'evoluir com prática objetiva e aulas ao vivo.',
     'h1': 'Como a prática constante supera maratonas de estudo em inglês',
     'date': '2026-06-29',
     'date_display': '29 de junho de 2026',
     'hero_image': 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aula de inglês na Vedium',
     'tag': 'Inglês',
     'category': 'ingles',
     'lead': 'A prática constante supera maratonas de estudo em inglês porque o idioma precisa de '
             'repetição, uso ativo e contato frequente para virar habilidade real. Estudar cinco horas '
             'em um único dia pode dar sensação de produtividade, mas dificilmente constrói fluência '
             'se o aluno passa o resto da semana sem falar, ouvir, revisar ou receber correção. Para '
             'evoluir de verdade, especialmente na conversação, o inglês precisa entrar na rotina em '
             'pequenas doses bem orientadas.',
     'sections': [{'heading': '',
                   'body': ['<p>Essa diferença é decisiva para quem tem pouco tempo, trabalha, estuda, '
                            'busca crescimento profissional e já tentou começar um curso várias vezes. '
                            'O problema, na maioria dos casos, não é falta de inteligência. É falta de '
                            'método sustentável. O aluno até se anima, faz uma maratona no fim de '
                            'semana, assiste vídeos, baixa materiais, anota regras, mas não cria '
                            'continuidade. Na semana seguinte, o conteúdo se perde, a confiança '
                            'diminui e o ciclo recomeça.</p>',
                            '<p>A Vedium trabalha com uma visão mais realista: aulas ao vivo, prática '
                            'de conversação, evolução por nível e liberdade para estudar sem '
                            'fidelidade. O aluno permanece porque sente progresso, não porque está '
                            'preso a um contrato longo. Neste artigo, você vai entender por que a '
                            'constância funciona melhor do que maratonas, como isso afeta a evolução '
                            'no nível CEFR e como organizar uma rotina objetiva de inglês online ao '
                            'vivo.</p>']},
                  {'heading': 'Por que maratonas de estudo parecem funcionar, mas não sustentam '
                              'fluência?',
                   'body': ['<p>Maratonas parecem funcionar porque geram sensação imediata de esforço. '
                            'O aluno passa horas estudando e sente que “rendeu”. Mas fluência não é '
                            'construída apenas por exposição intensa em um dia; ela depende de '
                            'recuperação, repetição e uso real ao longo do tempo.</p>',
                            '<p>Quando você estuda por muitas horas seguidas, costuma acontecer uma '
                            'mistura de cansaço, excesso de informação e baixa retenção. O cérebro até '
                            'reconhece o conteúdo no momento, mas isso não significa que conseguirá '
                            'usar o inglês em uma conversa real dias depois. Existe uma diferença '
                            'enorme entre “entendi quando vi” e “consigo falar quando preciso”.</p>',
                            '<p>Em inglês, essa diferença aparece principalmente no speaking. O aluno '
                            'pode assistir três horas de aula gravada sobre passado simples e ainda '
                            'travar quando precisa dizer “I went to a meeting yesterday” de forma '
                            'espontânea. Isso acontece porque falar exige velocidade mental, memória '
                            'ativa, pronúncia, escuta e confiança. Essas habilidades não se formam em '
                            'uma única maratona. Elas se constroem com prática frequente.</p>',
                            '<p>As maratonas também costumam falhar por três motivos:</p>',
                            '<ul><li><strong>Excesso de conteúdo passivo:</strong> o aluno assiste '
                            'muito e pratica pouco.</li><li><strong>Pouca repetição '
                            'distribuída:</strong> o conteúdo não volta em dias '
                            'diferentes.</li><li><strong>Ausência de correção:</strong> erros de '
                            'pronúncia e estrutura passam despercebidos.</li></ul>',
                            '<p>Isso não significa que estudar por mais tempo seja sempre ruim. Um '
                            'bloco maior pode ser útil para revisão, leitura ou preparação para prova. '
                            'O problema é quando a maratona substitui a rotina. Para aprender inglês '
                            'de verdade, o que muda o jogo é a prática constante, não o esforço '
                            'isolado.</p>']},
                  {'heading': 'Por que a prática constante funciona melhor no aprendizado de inglês?',
                   'body': ['<p>A prática constante funciona porque transforma o inglês em hábito e '
                            'reduz o tempo entre aprender, lembrar e usar. Quanto menor o intervalo '
                            'entre os contatos com o idioma, maior a chance de o conteúdo permanecer '
                            'ativo na memória.</p>',
                            '<p>Aprender inglês envolve várias camadas:</p>',
                            '<ul><li>reconhecer sons;</li><li>lembrar palavras;</li><li>montar '
                            'frases;</li><li>entender respostas;</li><li>responder com '
                            'naturalidade;</li><li>corrigir erros;</li><li>repetir até ganhar '
                            'segurança.</li></ul>',
                            '<p>Essas camadas precisam de contato frequente. Se você estuda '
                            'segunda-feira e só volta no domingo, o idioma precisa ser “reativado” a '
                            'cada semana. Isso cria a sensação de estar sempre recomeçando. Já a '
                            'prática constante mantém o inglês presente, mesmo que em sessões '
                            'curtas.</p>',
                            '<p>Por exemplo, compare dois alunos:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Perfil</th><th>Rotina</th><th>Resultado '
                            'provável</th></tr></thead><tbody><tr><td>Aluno A</td><td>Estuda 4 horas '
                            'no domingo</td><td>Entende bastante no dia, mas esquece parte durante a '
                            'semana</td></tr><tr><td>Aluno B</td><td>Estuda 30 minutos de segunda a '
                            'sexta</td><td>Mantém contato frequente e consolida melhor o '
                            'uso</td></tr><tr><td>Aluno C</td><td>Faz aula ao vivo + prática curta '
                            'semanal</td><td>Recebe correção, pratica fala e mantém evolução '
                            'guiada</td></tr></tbody></table>',
                            '<p>O aluno C tende a evoluir melhor porque une constância, orientação e '
                            'prática ativa. Não basta apenas “estar em contato” com inglês. É preciso '
                            'usar o idioma de forma objetiva.</p>',
                            '<p>Para o Bruno, persona da Vedium que busca crescimento profissional, '
                            'isso é essencial. Ele não quer estudar inglês como passatempo. Ele '
                            'precisa usar o idioma para carreira, entrevistas, reuniões, viagens, '
                            'networking e oportunidades. Uma rotina constante permite avançar sem '
                            'depender de grandes janelas de tempo.</p>']},
                  {'heading': 'Como a constância impacta a conversação?',
                   'body': ['<p>A constância impacta diretamente a conversação porque falar inglês '
                            'exige treino muscular, mental e emocional. Você precisa acostumar a boca '
                            'aos sons, o ouvido ao ritmo e a mente à construção rápida de frases.</p>',
                            '<p>Muitos alunos dizem: “Eu até entendo, mas travo na hora de falar.” '
                            'Esse é um sinal clássico de prática passiva em excesso. A pessoa ouviu, '
                            'leu e estudou regras, mas não teve oportunidades suficientes de produzir '
                            'o idioma em tempo real.</p>',
                            '<p>A conversação melhora quando você pratica pequenas respostas com '
                            'frequência. Não precisa começar com debates complexos. No início, o ideal '
                            'é treinar frases úteis:</p>',
                            '<ul><li>“I work in marketing.”</li><li>“I need to improve my '
                            'speaking.”</li><li>“Can you repeat, please?”</li><li>“I had a meeting '
                            'yesterday.”</li><li>“I’m preparing for a job interview.”</li><li>“In my '
                            'opinion, this is important.”</li><li>“I don’t know the exact word, but I '
                            'can explain.”</li></ul>',
                            '<p>Essas frases criam repertório para situações reais. Com o tempo, o '
                            'aluno deixa de montar tudo palavra por palavra e passa a falar em blocos. '
                            'Isso reduz travas.</p>',
                            '<p>A prática constante também diminui o medo de errar. Quem fala inglês '
                            'apenas uma vez por mês sente cada tentativa como um teste. Quem pratica '
                            'toda semana começa a encarar o erro como parte normal da evolução. Em '
                            'aulas ao vivo, esse processo fica mais seguro porque o professor corrige, '
                            'ajusta e mostra o próximo passo.</p>',
                            '<p>CTA: Quer saber seu nível real e começar a praticar conversação com '
                            'orientação? Faça o teste de nível grátis em <a '
                            'href="/curso-de-ingles-online">https://vediums.com/</a> e conheça as '
                            'aulas de inglês online ao vivo da Vedium.</p>']},
                  {'heading': 'O que isso tem a ver com nível CEFR?',
                   'body': ['<p>O CEFR é uma referência internacional que organiza o aprendizado de '
                            'idiomas em níveis como A1, A2, B1, B2 e C1. Na prática, ele ajuda o aluno '
                            'a entender onde está e o que precisa desenvolver para avançar.</p>',
                            '<p>A constância é importante porque cada nível exige domínio progressivo '
                            'de habilidades. Não basta “ver conteúdo de B1” para ser B1. É preciso '
                            'conseguir usar o idioma em situações compatíveis com esse nível.</p>',
                            '<p>De forma simplificada:</p>',
                            '<table class="vd-table"><thead><tr><th>Nível CEFR</th><th>O aluno '
                            'consegue fazer</th></tr></thead><tbody><tr><td>A1</td><td>Usar frases '
                            'simples, se apresentar e entender informações '
                            'básicas</td></tr><tr><td>A2</td><td>Falar sobre rotina, necessidades '
                            'imediatas e situações previsíveis</td></tr><tr><td>B1</td><td>Manter '
                            'conversas simples, explicar experiências e resolver situações '
                            'comuns</td></tr><tr><td>B2</td><td>Argumentar, participar de reuniões e '
                            'compreender conteúdos mais '
                            'complexos</td></tr><tr><td>C1</td><td>Comunicar-se com fluidez em '
                            'contextos profissionais e acadêmicos exigentes</td></tr></tbody></table>',
                            '<p>A evolução entre esses níveis depende de prática consistente. Um aluno '
                            'A2, por exemplo, não avança para B1 apenas estudando listas de verbos. '
                            'Ele precisa conversar sobre rotina, passado, planos, opiniões, problemas '
                            'e experiências. Precisa entender perguntas e responder com mais '
                            'autonomia.</p>',
                            '<p>Da mesma forma, quem busca B2 ou C1 precisa de prática frequente em '
                            'temas mais complexos: reuniões, apresentações, entrevistas, negociação, '
                            'leitura crítica, escrita profissional e argumentação. Maratonas isoladas '
                            'não dão tempo suficiente para consolidar esse repertório.</p>',
                            '<p>Um curso estruturado de inglês online ao vivo ajuda porque conecta o '
                            'nível atual do aluno ao próximo objetivo. Em vez de estudar '
                            'aleatoriamente, ele entende: “Estou em A2, preciso fortalecer speaking, '
                            'passado, vocabulário profissional e listening para chegar ao B1.”</p>']},
                  {'heading': 'Por que isso trava o aluno?',
                   'body': ['<p>O aluno trava porque tenta transformar inglês em um projeto gigante, e '
                            'não em uma rotina possível. Ele acredita que precisa de muito tempo '
                            'livre, muito material e muita motivação. Quando a vida fica corrida, '
                            'abandona.</p>',
                            '<p>Esse ciclo é comum:</p>',
                            '<ol><li>O aluno decide voltar a estudar inglês.</li><li>Monta uma rotina '
                            'pesada demais.</li><li>Estuda muito nos primeiros dias.</li><li>Cansa ou '
                            'perde um dia.</li><li>Sente culpa.</li><li>Para de '
                            'estudar.</li><li>Recomeça semanas ou meses depois.</li></ol>',
                            '<p>O problema não é falta de vontade. É desenho errado da rotina. Uma '
                            'rotina boa precisa sobreviver a semanas imperfeitas. Se o plano só '
                            'funciona quando tudo está tranquilo, ele não serve para a vida real.</p>',
                            '<p>Outro ponto que trava o aluno é a falta de prática com pessoas. '
                            'Estudar sozinho parece confortável, mas também permite fugir da fala. O '
                            'aluno assiste aulas, faz exercícios, entende a teoria, mas não enfrenta a '
                            'etapa mais importante: usar o idioma.</p>',
                            '<p>Para destravar, ele precisa de três mudanças:</p>',
                            '<ul><li>estudar menos conteúdo por vez;</li><li>praticar mais produção '
                            'ativa;</li><li>ter contato ao vivo com correção.</li></ul>',
                            '<p>Essa combinação reduz ansiedade e aumenta progresso. O aluno percebe '
                            'que não precisa esperar “estar pronto” para falar. Ele fica pronto '
                            'falando, errando e ajustando.</p>']},
                  {'heading': 'Como praticar inglês de forma objetiva?',
                   'body': ['<p>Praticar inglês de forma objetiva significa definir uma habilidade, '
                            'uma situação e uma meta curta para cada sessão. Em vez de “vou estudar '
                            'inglês hoje”, diga: “vou praticar 10 frases para falar sobre minha rotina '
                            'de trabalho” ou “vou treinar respostas para entrevista”.</p>',
                            '<p>A prática objetiva tem começo, meio e fim. Ela evita a sensação de '
                            'dispersão. Veja exemplos:</p>',
                            '<table class="vd-table"><thead><tr><th>Objetivo vago</th><th>Objetivo '
                            'objetivo</th></tr></thead><tbody><tr><td>Estudar inglês</td><td>Praticar '
                            '15 minutos de perguntas no presente simples</td></tr><tr><td>Melhorar '
                            'listening</td><td>Ouvir 2 minutos de áudio e anotar 5 '
                            'expressões</td></tr><tr><td>Treinar speaking</td><td>Gravar 1 minuto '
                            'falando sobre meu trabalho</td></tr><tr><td>Revisar '
                            'gramática</td><td>Criar 10 frases usando passado '
                            'simples</td></tr><tr><td>Aprender vocabulário</td><td>Usar 8 palavras '
                            'novas em frases próprias</td></tr></tbody></table>',
                            '<p>Para quem quer evoluir na conversação, uma rotina semanal pode seguir '
                            'este modelo:</p>',
                            '<h3>Segunda-feira: vocabulário útil</h3>',
                            '<p>Escolha um tema real: trabalho, viagem, reunião, entrevista, '
                            'apresentação, rotina ou atendimento. Anote 8 a 10 palavras e crie '
                            'frases.</p>',
                            '<h3>Terça-feira: escuta curta</h3>',
                            '<p>Ouça um áudio curto em inglês. Não tente entender tudo. Foque em '
                            'identificar palavras conhecidas e perceber o ritmo.</p>',
                            '<h3>Quarta-feira: fala guiada</h3>',
                            '<p>Responda três perguntas em voz alta. Grave sua voz se estiver sozinho. '
                            'Em aula ao vivo, pratique com professor e turma.</p>',
                            '<h3>Quinta-feira: revisão ativa</h3>',
                            '<p>Tente lembrar frases sem olhar. Depois, confira e corrija. Revisão '
                            'ativa é mais forte do que reler anotações.</p>',
                            '<h3>Sexta-feira: situação real</h3>',
                            '<p>Simule uma situação: entrevista, reunião, pedido de informação, '
                            'apresentação pessoal ou conversa casual.</p>',
                            '<h3>Sábado ou domingo: aula ao vivo ou conversação</h3>',
                            '<p>Use a aula para consolidar, tirar dúvidas, receber correção e entender '
                            'o próximo passo.</p>',
                            '<p>Essa rotina é simples, mas funciona porque repete o contato com o '
                            'idioma em formatos diferentes.</p>']},
                  {'heading': 'Prática constante significa estudar todos os dias?',
                   'body': ['<p>Não necessariamente. Prática constante não significa estudar muitas '
                            'horas todos os dias. Significa manter uma frequência suficiente para o '
                            'inglês não desaparecer da sua rotina.</p>',
                            '<p>Para muitos alunos, estudar três a cinco vezes por semana já é um '
                            'ótimo começo. O ideal é combinar sessões curtas com uma ou mais aulas ao '
                            'vivo. A constância precisa ser realista.</p>',
                            '<p>Uma boa lógica é ter três versões de rotina:</p>',
                            '<ul><li><strong>Rotina mínima:</strong> 5 minutos de '
                            'revisão.</li><li><strong>Rotina média:</strong> 20 a 30 minutos de '
                            'prática.</li><li><strong>Rotina completa:</strong> aula ao vivo + estudo '
                            'complementar.</li></ul>',
                            '<p>Nos dias corridos, faça a rotina mínima. Isso mantém o hábito. Nos '
                            'dias melhores, faça a média ou completa. O importante é evitar o '
                            'pensamento “já que não posso estudar uma hora, não vou estudar nada”.</p>',
                            '<p>Cinco minutos podem parecer pouco, mas servem para revisar frases, '
                            'ouvir um áudio curto ou repetir expressões. Essa microprática mantém o '
                            'inglês ativo e reduz a dificuldade de voltar.</p>']},
                  {'heading': 'O papel das aulas ao vivo na evolução',
                   'body': ['<p>As aulas ao vivo aceleram a evolução porque transformam o estudo em '
                            'interação. Inglês é comunicação. Por isso, a prática com gente real, em '
                            'tempo real, tem um impacto diferente de apenas assistir conteúdo '
                            'gravado.</p>',
                            '<p>Em uma aula ao vivo, o aluno:</p>',
                            '<ul><li>responde perguntas;</li><li>escuta sotaques e ritmos '
                            'reais;</li><li>recebe correção;</li><li>pratica '
                            'pronúncia;</li><li>percebe erros recorrentes;</li><li>tira dúvidas na '
                            'hora;</li><li>ganha confiança para falar;</li><li>acompanha sua evolução '
                            'por nível.</li></ul>',
                            '<p>Esse formato é especialmente importante para quem sente que já tentou '
                            'estudar sozinho, mas não conseguiu manter constância. A aula cria '
                            'compromisso e reduz a necessidade de decidir tudo sozinho. O professor '
                            'organiza o caminho e mostra o que priorizar.</p>',
                            '<p>Na Vedium, as aulas são online e ao vivo. Isso significa que o aluno '
                            'tem flexibilidade sem perder interação. A proposta é unir praticidade e '
                            'conversa real. Além disso, não há contrato de fidelidade. A permanência '
                            'vem do resultado percebido, não de amarras.</p>',
                            '<p>CTA: Se você quer sair do estudo solto e praticar inglês com direção, '
                            'faça seu teste de nível grátis em <a '
                            'href="/teste-de-nivel-ingles">https://vediums.com/</a> e veja qual turma '
                            'combina com seu momento.</p>']},
                  {'heading': 'Comparativo: maratona de estudo x prática constante',
                   'body': ['<p>A melhor forma de entender a diferença é comparar os dois modelos:</p>',
                            '<table class="vd-table"><thead><tr><th>Critério</th><th>Maratona de '
                            'estudo</th><th>Prática '
                            'constante</th></tr></thead><tbody><tr><td>Frequência</td><td>Baixa e '
                            'concentrada</td><td>Regular e '
                            'distribuída</td></tr><tr><td>Retenção</td><td>Menor, por excesso de '
                            'informação</td><td>Maior, por '
                            'repetição</td></tr><tr><td>Speaking</td><td>Pouca prática '
                            'real</td><td>Contato frequente com '
                            'fala</td></tr><tr><td>Motivação</td><td>Alta no início, instável '
                            'depois</td><td>Mais sustentável</td></tr><tr><td>Correção</td><td>Rara ou '
                            'inexistente</td><td>Pode acontecer toda semana</td></tr><tr><td>Evolução '
                            'CEFR</td><td>Desorganizada</td><td>Mais mensurável</td></tr><tr><td>Risco '
                            'de abandono</td><td>Alto</td><td>Menor</td></tr></tbody></table>',
                            '<p>A maratona dá sensação de avanço. A constância cria avanço real. Essa '
                            'é a diferença central.</p>',
                            '<p>Para um profissional que busca inglês para carreira, o objetivo não é '
                            '“sentir que estudou”. É conseguir falar melhor em uma reunião, entender '
                            'um e-mail, responder em uma entrevista, apresentar uma ideia ou conversar '
                            'com alguém de outro país. Isso exige habilidade, não apenas esforço '
                            'pontual.</p>']},
                  {'heading': 'Próximo passo no curso ao vivo',
                   'body': ['<p>O próximo passo para sair das maratonas e entrar na prática constante '
                            'é descobrir seu nível real. Sem isso, o aluno pode estudar conteúdo fácil '
                            'demais, difícil demais ou desalinhado com seu objetivo.</p>',
                            '<p>Um teste de nível ajuda a responder:</p>',
                            '<ul><li>Estou em A1, A2, B1, B2 ou C1?</li><li>Minha maior dificuldade é '
                            'speaking, listening, gramática ou vocabulário?</li><li>Preciso de inglês '
                            'para carreira, viagem, entrevista ou rotina?</li><li>Qual turma faz '
                            'sentido para meu momento?</li><li>Quanto tempo por semana consigo '
                            'dedicar?</li></ul>',
                            '<p>Depois disso, o aluno pode entrar em uma rotina mais clara. Em vez de '
                            'acumular vídeos e promessas, passa a ter caminho, prática e '
                            'acompanhamento.</p>',
                            '<p>Na Vedium, o curso de inglês online ao vivo foi pensado para quem quer '
                            'evoluir de verdade, com aulas em tempo real e sem fidelidade. Você testa, '
                            'sente a experiência e continua porque percebe progresso.</p>']},
                  {'heading': 'Como montar uma rotina antifalha de inglês?',
                   'body': ['<p>Uma rotina antifalha é aquela que continua mesmo quando sua semana não '
                            'é perfeita. Ela precisa ser pequena o suficiente para caber na vida real '
                            'e clara o suficiente para gerar progresso.</p>',
                            '<p>Siga este modelo:</p>',
                            '<ol><li><strong>Escolha um objetivo principal.</strong> Exemplo: melhorar '
                            'conversação para reuniões.</li><li><strong>Defina uma frequência '
                            'mínima.</strong> Exemplo: três práticas curtas por '
                            'semana.</li><li><strong>Tenha uma aula ao vivo como âncora.</strong> Ela '
                            'organiza o restante.</li><li><strong>Pratique situações reais.</strong> '
                            'Não estude apenas regras soltas.</li><li><strong>Revise em '
                            'ciclos.</strong> Volte aos mesmos temas em semanas '
                            'diferentes.</li><li><strong>Meça evolução por uso.</strong> Pergunte: '
                            '“consigo falar melhor do que antes?”</li></ol>',
                            '<p>A rotina não precisa ser perfeita. Precisa ser repetível.</p>']},
                  {'heading': 'Conclusão com CTA forte',
                   'body': ['<p>A prática constante supera maratonas de estudo em inglês porque '
                            'fluência nasce do uso repetido, da correção e da conversa real. Maratonas '
                            'podem até parecer produtivas, mas são frágeis quando não existe '
                            'continuidade. O inglês precisa voltar à sua rotina várias vezes por '
                            'semana, em pequenas doses objetivas e conectadas ao que você realmente '
                            'quer fazer com o idioma.</p>',
                            '<p>Se você quer evoluir na conversação, avançar no nível CEFR e usar '
                            'inglês para carreira, não espere ter uma agenda perfeita. Comece com um '
                            'plano possível, uma rotina sustentável e aulas ao vivo que deem direção '
                            'ao seu estudo.</p>',
                            '<p>Na Vedium, você aprende inglês online ao vivo, com prática real e sem '
                            'contrato de fidelidade. Você fica porque evolui, não porque está '
                            'preso.</p>',
                            '<p>Faça agora seu teste de nível grátis em <a '
                            'href="/curso-de-ingles-online">https://vediums.com/</a> e descubra o '
                            'próximo passo para falar inglês com mais confiança.</p>']}],
     'faqs': [{'q': 'É melhor estudar inglês todos os dias ou fazer uma maratona no fim de semana?',
               'a': 'É melhor manter prática constante durante a semana. Sessões curtas e frequentes '
                    'ajudam mais na retenção, na conversação e na confiança do que uma maratona '
                    'isolada no fim de semana.'},
              {'q': 'Quantos minutos por dia são suficientes para evoluir no inglês?',
               'a': 'De 20 a 30 minutos bem usados já podem gerar progresso, principalmente quando '
                    'combinados com aula ao vivo, revisão ativa e prática de fala.'},
              {'q': 'Como a prática constante ajuda na conversação?',
               'a': 'Ela aumenta o contato com o idioma, reduz o medo de errar e treina respostas em '
                    'tempo real. A fala melhora quando o aluno pratica com frequência, recebe correção '
                    'e repete situações reais.'},
              {'q': 'O que é nível CEFR no inglês?',
               'a': 'CEFR é uma referência internacional que organiza a proficiência em níveis como '
                    'A1, A2, B1, B2 e C1. Ele ajuda a entender o nível atual do aluno e os próximos '
                    'objetivos de aprendizado.'},
              {'q': 'A Vedium oferece inglês online ao vivo sem fidelidade?',
               'a': 'Sim. A Vedium oferece aulas de inglês online ao vivo, com foco em prática real, '
                    'evolução por nível e sem contrato de fidelidade. O aluno continua porque percebe '
                    'resultado.'}],
     'cta_title': 'Quer saber seu nível real de inglês?',
     'cta_text': 'Faça o teste de nível grátis da Vedium e descubra por onde começar.',
     'cta_label': 'Conhecer o curso de Inglês',
     'cta_url': '/curso-de-ingles-online'},
    "como-escrever-mensagens-curtas-e-claras-em-ingles-corporativo": {'title': 'Como escrever mensagens curtas e claras em inglês corporativo.md',
     'meta_description': 'Precisa melhorar sua escrita no trabalho? Aprenda técnicas essenciais para '
                         'escrever mensagens curtas, claras e profissionais em inglês com a Vedium.',
     'h1': 'Como escrever mensagens curtas e claras em inglês corporativo.md',
     'date': '2026-06-08',
     'date_display': '8 de junho de 2026',
     'hero_image': 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aula de inglês na Vedium',
     'tag': 'Inglês',
     'category': 'ingles',
     'lead': '',
     'sections': [{'heading': 'Por que a comunicação escrita trava o aluno no inglês corporativo?',
                   'body': ['<p>A maior trava para o profissional brasileiro que precisa do inglês não '
                            'é a gramática complexa, mas a insegurança de não soar "natural" ou '
                            '"profissional" o suficiente em comunicações rápidas — como e-mails, '
                            'mensagens de Slack ou Teams. Frequentemente, o aluno tenta traduzir '
                            'literalmente o pensamento do português para o inglês, o que resulta em '
                            'frases longas, excessivamente formais ou, pior, com falhas de clareza que '
                            'podem ser interpretadas no ambiente global como falta de autoridade ou '
                            'descaso.</p>',
                            '<p>Para a <a href="/teste-de-nivel-ingles">Vedium</a>, entendemos que o '
                            'inglês corporativo vai muito além de gramática; trata-se de '
                            '<strong>Inteligência Cultural</strong>. Não basta saber o vocabulário; é '
                            'preciso compreender como o ambiente corporativo global espera que uma '
                            'mensagem seja entregue. O medo de cometer um erro simples faz com que '
                            'muitos profissionais gastem tempo excessivo revisando textos ou, por '
                            'outro lado, enviem mensagens que não transmitem a urgência ou o '
                            'profissionalismo necessários.</p>',
                            '<p>No mundo corporativo moderno, o tempo é o recurso mais escasso. '
                            'Mensagens que não são imediatamente compreensíveis acabam sendo ignoradas '
                            'ou geram uma série de perguntas de esclarecimento, atrasando processos e '
                            'projetos. A habilidade de escrever de forma curta e direta não é apenas '
                            'uma questão de idioma, é uma competência de produtividade e liderança que '
                            'a Vedium ajuda você a desenvolver através de prática constante.</p>']},
                  {'heading': 'O impacto real da clareza na sua carreira global',
                   'body': ['<p>Mensagens curtas e diretas demonstram respeito pelo tempo do receptor '
                            'e absoluta confiança na sua própria capacidade. Em um ambiente global e '
                            'multicultural, a concisão é um ativo de alto valor. Profissionais que '
                            'dominam a escrita corporativa em inglês conseguem:</p>',
                            '<ul><li><strong>Reduzir mal-entendidos:</strong> Frases curtas e bem '
                            'estruturadas deixam menos margem para interpretações ambíguas entre times '
                            'de diferentes países.</li><li><strong>Aumentar a produtividade:</strong> '
                            'Menos tempo é gasto em trocas desnecessárias de e-mails para esclarecer '
                            'pontos que poderiam ter sido expostos em uma única frase bem '
                            'escrita.</li><li><strong>Transmitir autoridade:</strong> A capacidade de '
                            'resumir ideias complexas em poucas linhas é um sinal clássico de '
                            'senioridade e domínio do tema.</li></ul>',
                            '<p>Se você sente que trava ao escrever, o problema provavelmente não é o '
                            'seu nível de vocabulário, mas a falta de prática em <strong>cenários '
                            'reais</strong>. A Vedium foca em simular essas interações cotidianas do '
                            'mundo corporativo, onde você aprende o "como dizer" de forma objetiva, '
                            'garantindo que sua mensagem chegue ao destino com a precisão exigida pelo '
                            'mercado internacional.</p>']},
                  {'heading': 'Passo a passo: Como escrever com objetividade e impacto',
                   'body': ['<p>Para alcançar a clareza, a técnica mais eficaz é o método "um '
                            'parágrafo, uma ideia". Ao redigir, siga estas orientações práticas que '
                            'aplicamos em nossas turmas:</p>',
                            '<ol><li><strong>Vá direto ao ponto (The Bottom Line Up Front - '
                            'BLUF):</strong> Em inglês corporativo, a conclusão ou o pedido principal '
                            'deve aparecer na primeira ou segunda frase. Não esconda o objetivo da '
                            'mensagem no meio de um parágrafo longo.</li><li><strong>Use frases '
                            'curtas:</strong> Tente limitar cada frase a, no máximo, 15 a 20 palavras. '
                            'Utilize pontos finais em vez de vírgulas excessivas para separar '
                            'pensamentos.</li><li><strong>Priorize verbos de ação:</strong> Evite '
                            'transformar verbos em substantivos (nominalização), o que deixa o texto '
                            'pesado. Prefira dizer "We decided to increase the budget" em vez de "We '
                            'made a decision regarding an increase in the '
                            'budget".</li><li><strong>Seja específico com prazos:</strong> Evite '
                            'termos vagos como "soon" ou "later". Se precisar de uma resposta, diga '
                            'claramente: "Please confirm by 2 PM, Wednesday".</li></ol>',
                            '<h3>Como praticar de forma objetiva</h3>',
                            '<p>A melhor maneira de internalizar essas regras é através da aplicação '
                            'prática com feedback imediato. Em cursos gravados, você absorve a teoria, '
                            'mas não tem quem corrija o seu "jeito" de escrever. Na Vedium, o '
                            'diferencial é a aula ao vivo: você pode trazer e-mails ou mensagens que '
                            'precisa enviar no trabalho para a aula, e seu professor ajuda você a '
                            'ajustar o tom e a estrutura para soar mais natural, direto e '
                            'profissional.</p>']},
                  {'heading': 'A importância da prática em aulas ao vivo',
                   'body': ['<p>Você pode ler diversos livros sobre "Business English", mas a escrita '
                            'corporativa é uma habilidade que se refina com a interação. O erro comum '
                            'do profissional que busca cursos de inglês é acreditar que o método '
                            'passivo de absorção trará fluência na escrita. A fluência corporativa '
                            'nasce da <strong>conversação real</strong> e do exercício de traduzir '
                            'intenções culturais para a língua inglesa de maneira rápida.</p>',
                            '<p>A Vedium oferece um ambiente onde você evolui nível a nível, com '
                            'acompanhamento real. Como não trabalhamos com contratos de fidelidade, '
                            'nosso compromisso é 100% com a sua evolução. Você permanece conosco '
                            'porque vê resultado prático, porque suas mensagens no trabalho passaram a '
                            'ser elogiadas e porque você finalmente se sente confortável e seguro ao '
                            'lidar com times globais, independentemente da complexidade da '
                            'demanda.</p>',
                            '<p>Além disso, o aprendizado ao vivo permite que você desenvolva a '
                            '"Inteligência Cultural" necessária para saber quando ser mais formal ou '
                            'informal, adaptando sua escrita para colegas de diferentes culturas, algo '
                            'que nenhum aplicativo consegue replicar com a mesma profundidade.</p>']},
                  {'heading': 'A barreira da tradução literal',
                   'body': ['<p>Muitos brasileiros falham ao escrever em inglês corporativo porque '
                            'tentam manter a estrutura de polidez do português, que é naturalmente '
                            'mais prolixa. Em inglês, especialmente no ambiente de negócios americano '
                            'ou europeu, o valor está na eficiência. Aprender a escrever de forma '
                            'curta não é ser rude; é ser profissional.</p>',
                            '<p>Nossos professores na Vedium são especialistas em identificar esses '
                            '"vícios" de tradução e mostrar como substitui-los por estruturas nativas. '
                            'Essa mudança de mentalidade é o que transforma um aluno que tem medo de '
                            'escrever em um profissional que domina a comunicação corporativa.</p>']},
                  {'heading': 'Conclusão: Comece hoje sua evolução profissional',
                   'body': ['<p>Dominar a escrita em inglês corporativo é um diferencial competitivo '
                            'que coloca você em outro patamar de carreira. Não deixe que a insegurança '
                            'com a língua limite suas oportunidades globais ou atrase o seu '
                            'crescimento dentro da empresa. Se você quer aprender a se comunicar de '
                            'forma clara, curta e profissional, venha conhecer nossa metodologia '
                            'baseada em aulas ao vivo.</p>',
                            '<p><strong>Pronto para dar o próximo passo?</strong> Na Vedium, você '
                            'encontra um ambiente de aprendizado focado no seu sucesso profissional e '
                            'no seu ritmo. <a href="/curso-de-ingles-online">Faça um teste de nível '
                            'grátis</a> e descubra como podemos levar sua comunicação corporativa para '
                            'o próximo nível.</p>']}],
     'faqs': [{'q': 'É possível aprender a escrever mensagens corporativas sem decorar regras '
                    'gramaticais complexas?',
               'a': 'Sim. Nosso foco é na comunicação funcional. Você aprende a gramática necessária '
                    'através do uso prático, focando nas estruturas que realmente resolvem o seu dia a '
                    'dia profissional.'},
              {'q': 'Quanto tempo leva para sentir segurança escrevendo em inglês no trabalho?',
               'a': 'Com a nossa metodologia de aulas ao vivo e prática constante, a maioria dos '
                    'alunos sente uma melhora significativa na confiança já nas primeiras semanas. A '
                    'constância no ambiente de sala de aula ao vivo é o segredo.'},
              {'q': 'Por que a Vedium não exige contrato de fidelidade?',
               'a': 'Acreditamos que o seu aprendizado é o maior vínculo. Se você está evoluindo e '
                    'tendo resultados, não precisa de multas ou contratos longos para continuar. O '
                    'resultado é o que mantém nossos alunos conosco.'},
              {'q': 'As aulas da Vedium servem para quem precisa de Inglês específico para TI ou '
                    'Finanças?',
               'a': 'Com certeza. Nossos professores trabalham com o seu contexto profissional. Se '
                    'você precisa escrever e-mails técnicos ou relatórios de finanças, traremos esses '
                    'cenários para o centro da aula, garantindo que o aprendizado seja aplicável.'},
              {'q': 'Como faço para agendar uma aula experimental?',
               'a': 'É simples! Basta acessar nosso site em https://vediums.com/, realizar seu teste '
                    'de nível e entrar em contato com nossa equipe para agendar sua primeira '
                    'experiência ao vivo.'}],
     'cta_title': 'Quer saber seu nível real de inglês?',
     'cta_text': 'Faça o teste de nível grátis da Vedium e descubra por onde começar.',
     'cta_label': 'Conhecer o curso de Inglês',
     'cta_url': '/curso-de-ingles-online'},
    "ingles-para-conversas-por-telefone-e-chamadas-de-video": {'title': 'Inglês para conversas por telefone e chamadas de vídeo: Guia Prático de Fluência',
     'meta_description': 'Ganhe confiança nas suas reuniões em inglês. Aprenda técnicas essenciais '
                         'para dominar conversas por telefone e chamadas de vídeo com a Vedium.',
     'h1': 'Inglês para conversas por telefone e chamadas de vídeo: Guia Prático de Fluência',
     'date': '2026-06-01',
     'date_display': '1 de junho de 2026',
     'hero_image': 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aula de inglês na Vedium',
     'tag': 'Inglês',
     'category': 'ingles',
     'lead': '',
     'sections': [{'heading': 'Por que o Inglês para chamadas de vídeo e telefone trava o aluno?',
                   'body': ['<p>A barreira do "telefone" ou das videochamadas é um dos desafios mais '
                            'comuns no inglês corporativo. Ao contrário de uma conversa presencial, '
                            'onde a linguagem corporal e o contexto físico ajudam a decifrar a '
                            'mensagem, a chamada de vídeo ou o telefone limitam você ao canal '
                            'auditivo. O aluno muitas vezes trava porque sente que não tem o "tempo de '
                            'processamento" necessário: em uma reunião de Zoom ou Teams, a resposta '
                            'precisa ser imediata, e qualquer pequena hesitação gera uma ansiedade que '
                            'paralisa o raciocínio.</p>',
                            '<p>Para a <a href="/teste-de-nivel-ingles">Vedium</a>, entendemos que o '
                            'problema não é a sua falta de conhecimento gramatical, mas sim a falta de '
                            '<strong>treino em cenários de alta pressão</strong>. Quando você depende '
                            'apenas de cursos gravados, você nunca experimenta a dinâmica de um '
                            'ambiente onde a conexão falha, o áudio corta ou um falante nativo fala '
                            'rápido demais. A fluência nessas ferramentas é um componente crítico da '
                            'sua Inteligência Cultural, pois demonstra que você consegue manter o '
                            'controle e o profissionalismo independentemente do formato da '
                            'comunicação.</p>']},
                  {'heading': 'O impacto real da fluência digital na sua carreira',
                   'body': ['<p>Dominar chamadas em inglês não é apenas sobre vocabulário; é sobre '
                            'construir autoridade em um mundo de trabalho distribuído. Profissionais '
                            'que superam essa trava conseguem:<br>*   <strong>Transmitir confiança '
                            'imediata:</strong> A capacidade de responder de forma clara e assertiva '
                            'em uma videochamada eleva a percepção de competência da sua '
                            'liderança.<br>*   <strong>Gerir conflitos e negociações com '
                            'precisão:</strong> Em chamadas, o tom de voz e a escolha das palavras '
                            'corretas evitam mal-entendidos que poderiam custar negócios.<br>*   '
                            '<strong>Conectar-se com times globais:</strong> A fluência digital '
                            'permite que você participe ativamente de reuniões estratégicas, mesmo '
                            'estando a milhares de quilômetros de distância.</p>',
                            '<p>Se você sente que trava ao ver o ícone de uma chamada entrando ou ao '
                            'precisar participar de uma reunião global, a Vedium oferece a solução '
                            'através de aulas ao vivo que simulam exatamente esses desafios.</p>']},
                  {'heading': 'Passo a passo: Como praticar conversação de forma objetiva',
                   'body': ['<p>Para perder o medo e ganhar naturalidade em inglês por telefone ou '
                            'vídeo, você não precisa decorar manuais de inglês; você precisa de um '
                            '"playbook" de atuação profissional. Aplique estas estratégias:</p>',
                            '<ol><li><strong>Prepare o seu "Script de Abertura":</strong> Tenha frases '
                            'prontas para situações comuns: "Can you hear me clearly?", "Let me '
                            'rephrase that for you" ou "Could you please elaborate on that point?". '
                            'Ter esses "buffers" na ponta da língua reduz a ansiedade '
                            'inicial.</li><li><strong>Foque na estrutura, não na perfeição:</strong> '
                            'Em uma chamada, a clareza vence a gramática. Use frases diretas, evite '
                            'gírias desconhecidas e confirme a compreensão frequentemente: "Does that '
                            'make sense?".</li><li><strong>Use a escuta ativa:</strong> Se não '
                            'entendeu algo, não finja que compreendeu. Peça educadamente para repetir: '
                            '"Sorry, the connection was a bit unstable, could you repeat that?". Isso '
                            'demonstra profissionalismo, não fraqueza.</li><li><strong>Treine o seu '
                            'ouvido:</strong> Utilize podcasts ou vídeos de reuniões (como no TED '
                            'Talks ou reuniões corporativas públicas) para se acostumar com o ritmo de '
                            'fala em diferentes sotaques.</li></ol>',
                            '<h3>Próximo passo no curso ao vivo</h3>',
                            '<p>A melhor forma de aplicar essas técnicas é através de '
                            '<strong>simulações controladas</strong>. Em uma aula na Vedium, seu '
                            'professor atuará como seu interlocutor em uma chamada de vídeo. Vocês '
                            'praticarão cenários como dar um update de projeto, lidar com um cliente '
                            'difícil ou participar de um brainstorm global. Esse ambiente de '
                            '"laboratório" é o que transforma o seu medo em performance real.</p>']},
                  {'heading': 'A importância da prática em aulas ao vivo',
                   'body': ['<p>Você pode investir horas em aplicativos de idiomas, mas a dinâmica de '
                            'uma conversa por telefone é algo que se aprende na prática. Apps fornecem '
                            'input, mas não fornecem o "stress" positivo de uma conversa real. Na '
                            'Vedium, nosso compromisso é com a sua evolução através da conversa real. '
                            'Como não acreditamos em contratos de fidelidade, nosso sucesso é medido '
                            'pelo seu sucesso: você evolui nível a nível, ganhando a segurança que o '
                            'mundo corporativo exige, e fica conosco porque os resultados são visíveis '
                            'em cada reunião que você participa.</p>',
                            '<p>A nossa metodologia de "Inteligência Cultural" garante que você não '
                            'apenas fale inglês, mas entenda como se portar em diferentes culturas '
                            'corporativas durante uma chamada, respeitando os tempos de fala e as '
                            'etiquetas de cada região do globo.</p>']},
                  {'heading': 'Conclusão: Domine as videochamadas e eleve sua carreira',
                   'body': ['<p>O medo de falar inglês em chamadas de vídeo é uma trava comum, mas que '
                            'pode ser superada com a estratégia correta e o acompanhamento de quem '
                            'entende o seu desafio profissional. Não deixe que uma barreira de '
                            'comunicação limite suas chances de ascensão internacional ou de conexão '
                            'com as lideranças globais da sua empresa.</p>',
                            '<p><strong>Pronto para transformar sua confiança?</strong> Na Vedium, '
                            'nossas aulas ao vivo são personalizadas para garantir que você esteja '
                            'preparado para os desafios mais complexos do dia a dia corporativo. <a '
                            'href="/curso-de-ingles-online">Faça um teste de nível grátis</a> e '
                            'descubra como nossos professores podem ajudar você a alcançar a fluência '
                            'que sua carreira exige.</p>']}],
     'faqs': [{'q': 'Como posso praticar inglês para chamadas de vídeo se não tenho com quem falar?',
               'a': 'Nas aulas ao vivo da Vedium, seu professor assume o papel de um colega ou cliente '
                    'internacional, criando cenários de simulação perfeitos para você ganhar confiança '
                    'em um ambiente seguro de aprendizado.'},
              {'q': 'O inglês por telefone é mais difícil do que pessoalmente?',
               'a': 'Sim, porque perdemos as pistas visuais e a linguagem corporal. É por isso que o '
                    'treino focado em audição e estrutura de frases curtas, que enfatizamos em nossos '
                    'cursos, é tão importante para o sucesso nessas chamadas.'},
              {'q': 'Preciso de um nível avançado para participar de reuniões?',
               'a': 'Não necessariamente. Você precisa de "Inglês Funcional" para reuniões. Nós '
                    'ajudamos você a dominar as frases-chave e a estrutura de raciocínio necessária '
                    'para participar com segurança, mesmo sendo um estudante de nível intermediário.'},
              {'q': 'Por que a Vedium é a melhor escolha para quem tem pouco tempo?',
               'a': 'Nossas aulas são 100% ao vivo e focadas no que você precisa. Nada de conteúdo '
                    'genérico ou excesso de teoria; aplicamos diretamente o que você precisa para o '
                    'seu trabalho, tornando o aprendizado extremamente eficiente.'},
              {'q': 'Como agendar uma aula experimental de conversação corporativa?',
               'a': 'Acesse nosso site em https://vediums.com/, faça o seu teste de nível e entre em '
                    'contato com nossa equipe para agendar sua primeira aula focada em conversação '
                    'corporativa. Estamos prontos para ajudar você a destravar sua carreira.'}],
     'cta_title': 'Quer saber seu nível real de inglês?',
     'cta_text': 'Faça o teste de nível grátis da Vedium e descubra por onde começar.',
     'cta_label': 'Conhecer o curso de Inglês',
     'cta_url': '/curso-de-ingles-online'},
    "o-papel-do-professor-qualificado-no-ensino-de-ioruba": {'title': 'O papel do professor qualificado no ensino de iorubá',
     'meta_description': 'Entenda por que um professor qualificado é essencial para aprender Iorubá '
                         'com respeito, profundidade cultural e domínio da tradição.',
     'h1': 'O papel do professor qualificado no ensino de iorubá',
     'date': '2026-06-05',
     'date_display': '5 de junho de 2026',
     'hero_image': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Estudo de iorubá na Vedium',
     'tag': 'Iorubá',
     'category': 'ioruba',
     'lead': '',
     'sections': [{'heading': 'Por que a qualificação do professor é o pilar do aprendizado de Iorubá?',
                   'body': ['<p>Quando alguém busca aprender Iorubá, geralmente não está apenas atrás '
                            'de um sistema linguístico, mas em busca de uma reconexão com sua '
                            'ancestralidade. O professor qualificado no ensino de Iorubá é quem '
                            'garante que o aprendizado não seja meramente mecânico, mas sim uma '
                            'experiência imersiva e respeitosa. Enquanto aplicativos e vídeos soltos '
                            'podem ensinar palavras isoladas, apenas um educador que domina tanto a '
                            'língua quanto o contexto sociocultural é capaz de explicar o "porquê" por '
                            'trás de cada expressão.</p>',
                            '<p>Na <a href="/blog/alfabeto-ioruba">Vedium</a>, compreendemos que o '
                            'ensino de Iorubá exige sensibilidade. Um professor qualificado atua como '
                            'uma ponte entre o aluno e a sabedoria contida nas cantigas e rezas, '
                            'evitando que o conteúdo se torne raso ou, pior, desrespeitoso com a '
                            'tradição. Se você deseja aprender não apenas vocabulário, mas o sentido '
                            'profundo que conecta você às suas raízes, o acompanhamento de um '
                            'especialista ao vivo é um diferencial indispensável.</p>']},
                  {'heading': 'A importância da profundidade cultural no ensino',
                   'body': ['<p>O Iorubá é uma língua tonal onde a entonação pode alterar '
                            'completamente o significado de uma palavra. Mais do que isso, é uma '
                            'língua que carrega a história e a cosmovisão de um povo. Um professor '
                            'qualificado traz para a sala de aula essa bagagem, transformando a '
                            'aprendizagem em um exercício de respeito.</p>',
                            '<p>Quando falamos sobre o papel do educador, destacamos três pilares de '
                            'atuação:</p>',
                            '<ul><li><strong>Curadoria do conhecimento:</strong> O professor seleciona '
                            'materiais autênticos que honram a tradição, filtrando informações que '
                            'poderiam ser distorcidas em fontes amadoras.</li><li><strong>Atenção aos '
                            'tons e fonética:</strong> O aprendizado ao vivo permite que o professor '
                            'corrija nuances na pronúncia que são vitais para o significado real das '
                            'palavras, algo que o aluno sozinho dificilmente '
                            'perceberia.</li><li><strong>Transmissão de valores:</strong> O ensino de '
                            'Iorubá não está desassociado dos valores morais e espirituais da cultura. '
                            'Um bom professor ensina a língua contextualizada, respeitando a '
                            'sacralidade dos temas abordados.</li></ul>',
                            '<p>Na Vedium, nossas aulas ao vivo são desenhadas para garantir que esse '
                            'aprendizado seja profundo, porém acessível. Entendemos que você busca '
                            'seriedade, e nossos professores são selecionados justamente pelo domínio '
                            'técnico e pela vivência cultural.</p>']},
                  {'heading': 'Como o aprendizado ao vivo acelera a sua jornada',
                   'body': ['<p>Muitos estudantes perdem tempo tentando aprender sozinhos, enfrentando '
                            'dificuldades com a complexidade tonal da língua e desistindo por não '
                            'verem evolução ou por sentirem falta de um guia. O aprendizado ao vivo '
                            'com um professor qualificado elimina essas barreiras.</p>',
                            '<p>O aluno que estuda conosco ganha:<br>1.  <strong>Feedback '
                            'imediato:</strong> Você não precisa esperar para saber se sua pronúncia '
                            'de uma cantiga está correta. O professor orienta em tempo real.<br>2.  '
                            '<strong>Segurança na prática:</strong> O ambiente de aula é um espaço '
                            'seguro para errar, aprender e se sentir acolhido.<br>3.  '
                            '<strong>Progresso monitorado:</strong> Você acompanha sua evolução nível '
                            'a nível, com uma estrutura que faz sentido para sua rotina.</p>',
                            '<p>A Vedium acredita na liberdade: sem contratos de fidelidade, você '
                            'evolui de verdade porque o resultado e a qualidade da aula fazem você '
                            'querer continuar.</p>']},
                  {'heading': 'Contexto cultural: O iorubá é mais que uma língua',
                   'body': ['<p>A cultura iorubá é vibrante e complexa. Aprender o idioma significa '
                            'compreender as expressões usadas em contextos rituais, acadêmicos e '
                            'cotidianos. Um professor qualificado sabe navegar entre esses mundos, '
                            'garantindo que o aluno aprenda a forma correta de se expressar em '
                            'diferentes situações.</p>',
                            '<p>É comum que o aluno inicie sua jornada com muitas dúvidas sobre a '
                            'tradição. O professor não apenas ensina a gramática, mas contextualiza a '
                            'origem das palavras, ajudando a dissipar conceitos errados que muitas '
                            'vezes circulam na internet. É um aprendizado que constrói identidade.</p>',
                            '<h3>Como praticar com respeito</h3>',
                            '<p>A prática deve ser diária, mas deve ser guiada. Ao estudar em casa, '
                            'foque em ouvir áudios de fontes confiáveis, repetir as palavras '
                            'enfatizando os tons aprendidos na aula e, acima de tudo, mantenha a '
                            'curiosidade intelectual viva. Use o tempo entre as aulas ao vivo para '
                            'revisar os significados culturais discutidos com seu professor.</p>']},
                  {'heading': 'Próximo passo: A próxima turma de Iorubá',
                   'body': ['<p>A fluência começa na primeira aula, mas a autoridade do seu '
                            'aprendizado é definida pelo seu mentor. Se você busca aprender Iorubá com '
                            'quem entende a profundidade da tradição, a Vedium é o seu lugar. '
                            'Oferecemos aulas ao vivo, turmas pequenas e todo o suporte necessário '
                            'para que você honre sua raiz com o conhecimento correto.</p>',
                            '<p><strong>Não aprenda Iorubá de forma superficial.</strong> Junte-se a '
                            'uma escola que respeita a ancestralidade e prioriza a excelência técnica. '
                            'Entre em contato conosco para agendar uma aula experimental e conheça '
                            'nossos professores especializados. <a '
                            'href="/curso-de-ioruba-online">Clique aqui e saiba mais sobre nossa '
                            'próxima turma de Iorubá</a>.</p>']}],
     'faqs': [{'q': 'Por que é tão difícil aprender Iorubá sozinho?',
               'a': 'O Iorubá é uma língua tonal e ligada a um contexto cultural profundo. Sem um '
                    'professor, é quase impossível identificar erros de entonação e compreender os '
                    'significados reais por trás de expressões e cantigas tradicionais.'},
              {'q': 'A Vedium ensina Iorubá para iniciantes?',
               'a': 'Sim! Nossos professores são capacitados para guiar desde quem não conhece nada do '
                    'idioma até quem busca aprofundar conhecimentos específicos. Começamos do início, '
                    'respeitando seu ritmo de aprendizado.'},
              {'q': 'Como sei que o professor é realmente qualificado?',
               'a': 'Na Vedium, selecionamos professores que possuem não apenas o domínio linguístico '
                    'do Iorubá, mas também uma sólida vivência e respeito pela cultura e tradições '
                    'afro-brasileiras, garantindo um aprendizado responsável e ético.'},
              {'q': 'As aulas ao vivo da Vedium são gravadas?',
               'a': 'Não. Nossas aulas são 100% ao vivo. Acreditamos que a interação em tempo real com '
                    'o professor e a turma é o que garante o aprendizado real e a melhor experiência '
                    'possível para o aluno.'},
              {'q': 'Como agendar uma aula experimental de Iorubá?',
               'a': 'É muito simples. Acesse nosso site https://vediums.com/, preencha os dados e '
                    'entre em contato para agendar uma aula de teste. Você poderá sentir a metodologia '
                    'e conhecer nossos professores antes de tomar qualquer decisão.'}],
     'cta_title': 'Quer aprender iorubá com pronúncia correta desde o início?',
     'cta_text': 'Aulas ao vivo, do zero ao avançado, com foco em tons e conversação real.',
     'cta_label': 'Conhecer o curso de Iorubá',
     'cta_url': '/curso-de-ioruba-online'},
    "como-avaliar-se-um-conteudo-de-ioruba-e-serio-e-responsavel": {'title': 'Como avaliar se um conteúdo de iorubá é sério e responsável',
     'meta_description': 'Aprenda a avaliar se um conteúdo de iorubá é sério, responsável e respeitoso '
                         'com a língua, a cultura e a tradição.',
     'h1': 'Como avaliar se um conteúdo de iorubá é sério e responsável',
     'date': '2026-06-26',
     'date_display': '26 de junho de 2026',
     'hero_image': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Estudo de iorubá na Vedium',
     'tag': 'Iorubá',
     'category': 'ioruba',
     'lead': 'Um conteúdo de iorubá é sério e responsável quando trata a língua com precisão, respeita '
             'o contexto cultural, explica limites de tradução, valoriza a pronúncia correta e evita '
             'transformar tradição em enfeite. Para quem busca aprender iorubá por ancestralidade, '
             'pesquisa, religiosidade, cultura ou identidade, essa avaliação é essencial: nem todo '
             'material disponível na internet ensina com profundidade, cuidado e responsabilidade.',
     'sections': [{'heading': '',
                   'body': ['<p>Hoje é fácil encontrar vídeos, listas de palavras, traduções rápidas, '
                            'posts em redes sociais e promessas de aprendizado acelerado. O problema é '
                            'que o iorubá não deve ser tratado como um conjunto de frases soltas. É '
                            'uma língua tonal, viva, ligada a povos, histórias, comunidades, '
                            'oralidade, nomes, cantigas, rezas, literatura e memória afro-diaspórica. '
                            'Quando alguém ensina sem contexto, pode gerar confusão, pronúncias '
                            'erradas e interpretações rasas.</p>',
                            '<p>Para a persona Adá — quem deseja entender o que canta, reza ou '
                            'pesquisa, honrando sua raiz — esse cuidado é ainda mais importante. '
                            'Aprender iorubá não é apenas “saber o significado” de uma palavra. É '
                            'compreender como ela soa, quando é usada, em que contexto aparece e qual '
                            'responsabilidade existe ao repeti-la.</p>',
                            '<p>Neste artigo, você verá critérios práticos para avaliar se um conteúdo '
                            'de iorubá é confiável, o que observar em cursos, professores e materiais '
                            'online, quais sinais de alerta evitar e por que aulas ao vivo podem '
                            'oferecer um caminho mais seguro para aprender com respeito.</p>']},
                  {'heading': 'Por que é importante avaliar a seriedade de um conteúdo de iorubá?',
                   'body': ['<p>Avaliar a seriedade de um conteúdo de iorubá é importante porque erros '
                            'de pronúncia, tradução e contexto podem mudar completamente a compreensão '
                            'da língua. No iorubá, não basta reconhecer letras ou decorar palavras: os '
                            'tons, a oralidade e o uso cultural precisam ser tratados com cuidado.</p>',
                            '<p>Muitas pessoas chegam ao estudo do iorubá depois de tentativas '
                            'frustradas com vídeos soltos, apostilas sem referência, traduções '
                            'automáticas ou conteúdos que prometem explicar cantigas e rezas de forma '
                            'superficial. Isso pode até despertar curiosidade, mas raramente constrói '
                            'uma base segura.</p>',
                            '<p>Um conteúdo irresponsável pode causar três problemas principais:</p>',
                            '<ul><li><strong>Erro linguístico:</strong> pronúncia, tom ou estrutura '
                            'ensinados de forma incorreta.</li><li><strong>Erro cultural:</strong> '
                            'explicações que ignoram contexto, tradição e uso '
                            'adequado.</li><li><strong>Erro de expectativa:</strong> promessa de '
                            'domínio rápido, sem estudo, prática ou orientação.</li></ul>',
                            '<p>A consequência é que o aluno acredita que aprendeu, mas leva adiante '
                            'uma forma distorcida do idioma. Em uma língua ligada à memória ancestral '
                            'e a práticas culturais profundas, isso não é um detalhe. É uma questão de '
                            'respeito.</p>',
                            '<p>Um conteúdo sério não precisa ser complicado ou elitista. Pelo '
                            'contrário: ele pode ser claro, acolhedor e acessível. A diferença é que '
                            'ele não simplifica de modo irresponsável. Ele explica o que sabe, '
                            'reconhece limites e orienta o aluno a avançar com cuidado.</p>']},
                  {'heading': 'Quais sinais mostram que um conteúdo de iorubá é confiável?',
                   'body': ['<p>Um conteúdo confiável de iorubá apresenta fonte, contexto, explicação '
                            'de pronúncia e compromisso cultural. Ele não entrega apenas uma tradução '
                            'rápida; ele ajuda o aluno a entender como a palavra vive dentro da '
                            'língua.</p>',
                            '<p>Veja os principais sinais positivos:</p>',
                            '<h3>1. Explica pronúncia e tons</h3>',
                            '<p>O iorubá é uma língua tonal. Isso significa que a variação de tom pode '
                            'alterar o sentido de uma palavra. Um conteúdo sério não ignora esse '
                            'ponto. Ele mostra que pronúncia não é detalhe, mas parte do '
                            'significado.</p>',
                            '<p>Se um material apresenta apenas palavras escritas, sem orientação '
                            'sonora, sem marcação tonal ou sem alerta sobre pronúncia, ele pode ser '
                            'insuficiente para o aprendizado real.</p>',
                            '<h3>2. Diferencia tradução de interpretação</h3>',
                            '<p>Tradução literal nem sempre dá conta da profundidade cultural. Um '
                            'conteúdo responsável mostra quando uma palavra tem aproximações em '
                            'português, mas não uma equivalência perfeita. Isso é especialmente '
                            'importante em nomes, saudações, cantigas, rezas e expressões ligadas à '
                            'tradição.</p>',
                            '<p>Uma boa explicação costuma dizer algo como: “este termo pode ser '
                            'entendido como...”, “neste contexto significa...”, “a tradução aproximada '
                            'é...”, “o uso depende da situação...”.</p>',
                            '<h3>3. Apresenta contexto de uso</h3>',
                            '<p>Aprender uma palavra sem saber quando usá-la é perigoso. Um conteúdo '
                            'sério mostra se a expressão é cotidiana, formal, religiosa, cultural, '
                            'histórica, poética ou ritual. Também explica se há cuidados ao repetir '
                            'determinada expressão.</p>',
                            '<p>Contexto é o que impede o aluno de usar a língua de forma decorativa '
                            'ou inadequada.</p>',
                            '<h3>4. Respeita a cultura iorubá e afro-diaspórica</h3>',
                            '<p>O conteúdo responsável não exotiza, não transforma símbolos em '
                            'estética vazia e não usa a tradição como chamariz sensacionalista. Ele '
                            'fala com reverência, precisão e simplicidade.</p>',
                            '<p>Respeitar a cultura não significa tornar o aprendizado distante. '
                            'Significa reconhecer que a língua carrega história e que o aluno deve se '
                            'aproximar com humildade.</p>',
                            '<h3>5. Tem professor, curadoria ou referência qualificada</h3>',
                            '<p>Um bom curso de iorubá online deve indicar quem ensina, qual é a '
                            'experiência da pessoa, como o conteúdo é estruturado e como a prática '
                            'acontece. Quando não há nenhuma informação sobre autoria, formação, '
                            'vivência ou curadoria, é preciso ter cautela.</p>',
                            '<p>CTA: Se você procura aprender iorubá com profundidade cultural e '
                            'prática ao vivo, fale com a Vedium sobre a próxima turma em <a '
                            'href="/curso-de-ioruba-online">https://vediums.com/</a>.</p>']},
                  {'heading': 'Quais sinais de alerta indicam conteúdo raso ou irresponsável?',
                   'body': ['<p>Conteúdos rasos geralmente prometem muito, explicam pouco e ignoram o '
                            'contexto cultural. Eles podem parecer atraentes nas redes sociais, mas '
                            'não sustentam um aprendizado sério.</p>',
                            '<p>Fique atento aos sinais de alerta:</p>',
                            '<h3>1. Promessas de fluência rápida</h3>',
                            '<p>Frases como “aprenda iorubá em poucos dias” ou “domine cantigas sem '
                            'esforço” devem ser vistas com desconfiança. Toda língua exige tempo, '
                            'prática, escuta e correção. No caso do iorubá, a atenção aos tons e ao '
                            'contexto torna esse processo ainda mais cuidadoso.</p>',
                            '<h3>2. Listas de palavras sem pronúncia</h3>',
                            '<p>Listas podem ajudar como apoio, mas não devem ser o centro do '
                            'aprendizado. Se o conteúdo apresenta “palavra em iorubá = palavra em '
                            'português” sem áudio, tom, exemplo e contexto, ele é incompleto.</p>',
                            '<h3>3. Traduções absolutas de cantigas ou rezas</h3>',
                            '<p>Cantigas e rezas exigem muita responsabilidade. Um conteúdo que '
                            'apresenta traduções definitivas, sem explicar variações, contexto e '
                            'limites de interpretação, pode induzir o aluno ao erro.</p>',
                            '<p>O melhor caminho é estudar pequenos trechos com orientação, entendendo '
                            'vocabulário, som, ritmo, função e contexto.</p>',
                            '<h3>4. Uso da cultura como estética</h3>',
                            '<p>Quando a cultura aparece apenas como imagem, mistério ou “conteúdo '
                            'exótico”, há um problema. A língua iorubá não deve ser usada como enfeite '
                            'de marketing. Ela merece ser tratada como patrimônio vivo.</p>',
                            '<h3>5. Falta de espaço para dúvidas</h3>',
                            '<p>Um conteúdo gravado pode ser útil, mas quando não há possibilidade de '
                            'perguntar, corrigir pronúncia ou aprofundar pontos delicados, o '
                            'aprendizado fica limitado. Para iniciantes, especialmente, a interação ao '
                            'vivo é muito importante.</p>']},
                  {'heading': 'Como comparar um curso de iorubá online?',
                   'body': ['<p>Para comparar um curso de iorubá online, observe se ele oferece aula '
                            'ao vivo, professor qualificado, progressão clara, prática de pronúncia, '
                            'contexto cultural e espaço para perguntas. O melhor curso não é '
                            'necessariamente o que promete mais conteúdo, mas o que ajuda você a '
                            'aprender com consistência e respeito.</p>',
                            '<p>Use este checklist:</p>',
                            '<table class="vd-table"><thead><tr><th>Critério</th><th>O que '
                            'observar</th></tr></thead><tbody><tr><td>Aula ao vivo</td><td>Há '
                            'interação real com professor ou é só vídeo '
                            'gravado?</td></tr><tr><td>Pronúncia</td><td>O curso trabalha sons, tons e '
                            'correção?</td></tr><tr><td>Cultura</td><td>O conteúdo explica contexto e '
                            'uso responsável?</td></tr><tr><td>Progressão</td><td>Existe caminho do '
                            'básico ao avançado?</td></tr><tr><td>Prática</td><td>O aluno fala, '
                            'repete, pergunta e recebe '
                            'retorno?</td></tr><tr><td>Transparência</td><td>O formato, valores e '
                            'condições são claros?</td></tr><tr><td>Sem fidelidade</td><td>O aluno '
                            'pode continuar pelo resultado, não por '
                            'contrato?</td></tr></tbody></table>',
                            '<p>Na Vedium, o diferencial está em unir aulas ao vivo, profundidade '
                            'cultural e liberdade para o aluno estudar sem fidelidade. Isso reduz a '
                            'insegurança de começar e valoriza o que realmente importa: evolução '
                            'percebida, respeito à tradição e contato humano em tempo real.</p>']},
                  {'heading': 'Como avaliar conteúdos sobre cantigas, rezas e termos sagrados?',
                   'body': ['<p>Conteúdos sobre cantigas, rezas e termos sagrados devem ser avaliados '
                            'com ainda mais rigor. Eles exigem contexto, prudência e orientação de '
                            'quem entende a língua e a tradição.</p>',
                            '<p>Antes de confiar em uma explicação, pergunte:</p>',
                            '<ul><li>A pessoa explica de onde vem a interpretação?</li><li>Ela '
                            'diferencia tradução literal de sentido cultural?</li><li>Ela fala sobre '
                            'pronúncia e tons?</li><li>Ela reconhece limites do que pode ser explicado '
                            'publicamente?</li><li>Ela evita sensacionalismo?</li><li>Ela trata a '
                            'tradição com respeito?</li><li>Ela orienta o aluno a buscar estudo '
                            'contínuo?</li></ul>',
                            '<p>Nem tudo deve ser reduzido a um post. Algumas dúvidas precisam de '
                            'aula, conversa, contexto e escuta. Isso não é barreira ao aprendizado; é '
                            'proteção contra a superficialidade.</p>',
                            '<p>Para quem busca compreender cantigas e rezas, o estudo do iorubá deve '
                            'ser gradual. Primeiro, construa base de sons, saudações, vocabulário e '
                            'estrutura. Depois, avance para textos, expressões e trechos com '
                            'orientação. Esse caminho torna a compreensão mais profunda e evita '
                            'interpretações apressadas.</p>']},
                  {'heading': 'Como praticar iorubá com respeito?',
                   'body': ['<p>Praticar iorubá com respeito significa ouvir antes de repetir, '
                            'perguntar antes de interpretar e aceitar correção como parte do cuidado '
                            'com a língua. O respeito aparece tanto na intenção quanto no método.</p>',
                            '<p>Aqui estão práticas recomendadas:</p>',
                            '<h3>Ouça com atenção</h3>',
                            '<p>Antes de repetir uma palavra, escute várias vezes. Observe som, ritmo, '
                            'pausas e tons. A pressa para falar pode criar vícios difíceis de corrigir '
                            'depois.</p>',
                            '<h3>Anote contexto, não só tradução</h3>',
                            '<p>Ao criar seu caderno de estudo, evite anotar apenas equivalências. Use '
                            'colunas como:</p>',
                            '<table class="vd-table"><thead><tr><th>Palavra ou '
                            'expressão</th><th>Pronúncia</th><th>Significado '
                            'aproximado</th><th>Contexto</th><th>Dúvidas</th></tr></thead><tbody></tbody></table>',
                            '<p>Esse formato ajuda a lembrar que cada termo vive dentro de uma '
                            'situação.</p>',
                            '<h3>Pergunte quando não tiver certeza</h3>',
                            '<p>Uma pergunta honesta é melhor do que uma certeza errada. Se você não '
                            'sabe se uma expressão é adequada, pergunte ao professor.</p>',
                            '<h3>Evite usar termos culturais como adorno</h3>',
                            '<p>Não use palavras iorubás apenas para parecer profundo, místico ou '
                            'diferente. Use com consciência e, quando necessário, explique o '
                            'contexto.</p>',
                            '<h3>Pratique em aula ao vivo</h3>',
                            '<p>Aula ao vivo permite corrigir pronúncia, entender nuances e fazer '
                            'perguntas no momento em que a dúvida aparece. Isso é essencial para '
                            'construir uma base responsável.</p>',
                            '<p>CTA: Quer praticar iorubá com orientação e respeito cultural? Fale com '
                            'a Vedium sobre a próxima turma em <a '
                            'href="/blog/alfabeto-ioruba">https://vediums.com/</a>.</p>']},
                  {'heading': 'Exercício para aula ao vivo: checklist de avaliação de conteúdo',
                   'body': ['<p>Antes de levar um material de iorubá como referência, faça este '
                            'exercício. Ele ajuda a avaliar se o conteúdo merece confiança e prepara '
                            'boas perguntas para a aula ao vivo.</p>',
                            '<p>Escolha um vídeo, post, apostila ou lista de palavras e responda:</p>',
                            '<ol><li>Quem criou esse conteúdo?</li><li>A pessoa informa experiência, '
                            'fonte ou curadoria?</li><li>Há áudio ou orientação de '
                            'pronúncia?</li><li>Os tons são explicados?</li><li>A tradução é '
                            'apresentada como absoluta ou aproximada?</li><li>O contexto cultural é '
                            'explicado?</li><li>Há exemplos de uso?</li><li>O conteúdo diferencia uso '
                            'cotidiano, religioso, cultural ou histórico?</li><li>Existe espaço para '
                            'dúvidas?</li><li>O material trata a cultura com respeito ou como '
                            'curiosidade exótica?</li></ol>',
                            '<p>Depois, leve três dúvidas para a aula:</p>',
                            '<ul><li>“Essa pronúncia está correta?”</li><li>“Esse significado depende '
                            'de contexto?”</li><li>“Essa expressão pode ser usada em conversa '
                            'comum?”</li></ul>',
                            '<p>Esse tipo de exercício forma alunos mais críticos e conscientes. Em '
                            'vez de consumir qualquer material, você aprende a avaliar, comparar e '
                            'aprofundar.</p>']},
                  {'heading': 'Curso gravado, conteúdo gratuito ou aula ao vivo: o que escolher?',
                   'body': ['<p>Conteúdos gratuitos e aulas gravadas podem ajudar na descoberta, mas '
                            'não substituem a aula ao vivo quando o objetivo é aprender iorubá com '
                            'base sólida. Cada formato tem um papel.</p>',
                            '<table class="vd-table"><thead><tr><th>Formato</th><th>Pode ajudar '
                            'em</th><th>Limitação</th></tr></thead><tbody><tr><td>Posts e vídeos '
                            'curtos</td><td>Curiosidade, primeiro contato, vocabulário '
                            'inicial</td><td>Pouco contexto e pouca correção</td></tr><tr><td>Aulas '
                            'gravadas</td><td>Revisão e exposição ao conteúdo</td><td>Não corrigem '
                            'pronúncia nem respondem '
                            'dúvidas</td></tr><tr><td>Apostilas</td><td>Organização de '
                            'estudo</td><td>Podem ficar frias sem áudio e '
                            'prática</td></tr><tr><td>Aula ao vivo</td><td>Pronúncia, interação, '
                            'dúvidas, cultura e prática</td><td>Exige compromisso de '
                            'presença</td></tr></tbody></table>',
                            '<p>O ideal é usar conteúdos gratuitos como porta de entrada e aula ao '
                            'vivo como caminho de estruturação. Assim, você aproveita a curiosidade '
                            'inicial sem ficar preso a materiais soltos.</p>',
                            '<p>Para a Adá, que deseja honrar sua raiz e compreender o sentido por '
                            'trás das palavras, a aula ao vivo é especialmente valiosa. Ela permite '
                            'aprender com alguém que explica, escuta, corrige e contextualiza.</p>']},
                  {'heading': 'O que um conteúdo sério nunca deve prometer?',
                   'body': ['<p>Um conteúdo sério nunca deve prometer fluência imediata, tradução '
                            'definitiva de tudo, domínio cultural sem vivência ou aprendizado profundo '
                            'sem prática. Essas promessas podem até chamar atenção, mas não respeitam '
                            'o processo real.</p>',
                            '<p>Desconfie de promessas como:</p>',
                            '<ul><li>“Aprenda tudo sobre iorubá em uma semana.”</li><li>“Tradução '
                            'completa e definitiva de qualquer cantiga.”</li><li>“Método secreto para '
                            'dominar sem professor.”</li><li>“Não precisa aprender '
                            'tons.”</li><li>“Basta decorar esta lista.”</li><li>“Use estas palavras '
                            'para impressionar.”</li></ul>',
                            '<p>Um conteúdo responsável prefere prometer caminho, não milagre. Ele '
                            'diz: “vamos começar com base”, “vamos entender o contexto”, “vamos '
                            'praticar pronúncia”, “vamos respeitar a tradição” e “vamos evoluir passo '
                            'a passo”.</p>',
                            '<p>Essa postura é mais honesta e mais eficaz.</p>']},
                  {'heading': 'Como a Vedium se posiciona no ensino de iorubá?',
                   'body': ['<p>A Vedium entende o iorubá como língua, cultura e memória. Por isso, a '
                            'proposta não é entregar conteúdo raso ou apenas aulas gravadas, mas criar '
                            'uma experiência ao vivo em que o aluno possa aprender com profundidade e '
                            'respeito.</p>',
                            '<p>A comunicação da Vedium parte de quatro pilares:</p>',
                            '<ul><li>aula ao vivo de verdade;</li><li>idioma junto com '
                            'cultura;</li><li>evolução real;</li><li>sem amarras de contrato '
                            'longo.</li></ul>',
                            '<p>No iorubá, isso significa ensinar com cuidado cultural, valorizar a '
                            'tradição e criar espaço para dúvidas. A retenção do aluno não vem de '
                            'fidelidade obrigatória. Vem da confiança construída aula após aula.</p>',
                            '<p>Para quem já tentou aprender por vídeos soltos, essa diferença é '
                            'grande. Em vez de acumular fragmentos, o aluno encontra um caminho. Em '
                            'vez de repetir sem saber, aprende a perguntar. Em vez de buscar respostas '
                            'rápidas, constrói compreensão.</p>']},
                  {'heading': 'Conclusão com CTA forte',
                   'body': ['<p>Avaliar se um conteúdo de iorubá é sério e responsável é uma etapa '
                            'essencial para quem deseja aprender com respeito. O melhor material não é '
                            'o que promete respostas fáceis, mas o que reconhece a profundidade da '
                            'língua, explica pronúncia e tons, contextualiza expressões, evita '
                            'exotização e valoriza a cultura iorubá como algo vivo.</p>',
                            '<p>Se você busca iorubá por ancestralidade, fé, pesquisa, identidade ou '
                            'amor à cultura, escolha um caminho que honre esse motivo. Comece com bons '
                            'critérios, desconfie de simplificações exageradas e procure orientação ao '
                            'vivo para construir base sólida.</p>',
                            '<p>A Vedium oferece aulas de iorubá ao vivo, com profundidade cultural e '
                            'sem fidelidade. Você aprende no seu ritmo, pergunta, pratica e evolui com '
                            'quem respeita o que está ensinando.</p>',
                            '<p>Fale sobre a próxima turma de Iorubá em <a '
                            'href="/curso-de-ioruba-online">https://vediums.com/</a> e comece a '
                            'aprender além das palavras.</p>']}],
     'faqs': [{'q': 'Como saber se um conteúdo de iorubá é confiável?',
               'a': 'Um conteúdo confiável explica pronúncia, tons, contexto cultural, exemplos de uso '
                    'e limites de tradução. Também deve ter autoria, curadoria ou professor '
                    'qualificado.'},
              {'q': 'Posso aprender iorubá apenas com vídeos gratuitos?',
               'a': 'Vídeos gratuitos podem ajudar no primeiro contato, mas são limitados. Para '
                    'aprender pronúncia, tons, contexto e uso responsável, aulas ao vivo com correção '
                    'são mais seguras.'},
              {'q': 'Por que traduções de cantigas em iorubá exigem cuidado?',
               'a': 'Porque cantigas podem ter camadas linguísticas, culturais, poéticas e religiosas. '
                    'Traduções rápidas podem perder sentido, contexto e nuances importantes.'},
              {'q': 'O que evitar ao estudar cultura iorubá online?',
               'a': 'Evite conteúdos sensacionalistas, promessas de fluência rápida, listas sem '
                    'pronúncia, traduções absolutas e materiais que tratam a cultura como exotismo ou '
                    'enfeite.'},
              {'q': 'A Vedium oferece curso de iorubá online ao vivo?',
               'a': 'Sim. A Vedium oferece aulas de iorubá ao vivo, com foco em língua, cultura, '
                    'respeito à tradição e evolução real, sem contrato de fidelidade.'}],
     'cta_title': 'Quer aprender iorubá com pronúncia correta desde o início?',
     'cta_text': 'Aulas ao vivo, do zero ao avançado, com foco em tons e conversação real.',
     'cta_label': 'Conhecer o curso de Iorubá',
     'cta_url': '/curso-de-ioruba-online'},
    "como-manter-constancia-no-estudo-de-uma-lingua-de-heranca": {'title': 'Como manter constância no estudo de uma língua de herança',
     'meta_description': 'Aprenda como manter constância no estudo de uma língua de herança com rotina '
                         'realista, respeito cultural e aulas ao vivo.',
     'h1': 'Como manter constância no estudo de uma língua de herança',
     'date': '2026-05-29',
     'date_display': '29 de maio de 2026',
     'hero_image': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Estudo de iorubá na Vedium',
     'tag': 'Iorubá',
     'category': 'ioruba',
     'lead': 'Manter constância no estudo de uma língua de herança exige mais do que disciplina: exige '
             'vínculo, rotina possível, orientação respeitosa e um método que conecte idioma, memória '
             'e cultura. Quando falamos de iorubá, essa constância ganha uma camada ainda mais '
             'profunda, porque muitas pessoas não estão estudando apenas uma língua estrangeira. Estão '
             'tentando se aproximar de uma raiz, compreender cantigas, rezas, nomes, saudações, '
             'histórias e sentidos que atravessam a cultura afro-diaspórica.',
     'sections': [{'heading': '',
                   'body': ['<p>A grande dificuldade é que o entusiasmo inicial nem sempre se '
                            'transforma em continuidade. A pessoa começa motivada, salva vídeos, anota '
                            'palavras, pesquisa significados, acompanha conteúdos nas redes sociais e '
                            'promete estudar todos os dias. Mas, com o tempo, a rotina aperta, as '
                            'dúvidas aumentam, a pronúncia parece difícil e o estudo vira uma coleção '
                            'de fragmentos. O resultado é frustração: muito interesse, mas pouca '
                            'evolução real.</p>',
                            '<p>A constância nasce quando o estudo deixa de depender apenas da '
                            'motivação e passa a ter estrutura. Para aprender uma língua de herança '
                            'com respeito, especialmente o iorubá, é preciso criar uma rotina que '
                            'caiba na vida real, valorize a oralidade, respeite os contextos culturais '
                            'e tenha momentos de prática ao vivo. Aulas ao vivo ajudam porque oferecem '
                            'correção, acolhimento, aprofundamento e compromisso. O aluno não fica '
                            'sozinho diante de traduções soltas.</p>',
                            '<p>Neste artigo, você vai entender como manter constância no estudo de '
                            'uma língua de herança, por que isso importa no aprendizado de iorubá, '
                            'como praticar com respeito e qual próximo passo seguir em um curso de '
                            'iorubá online ao vivo.</p>']},
                  {'heading': 'O que é uma língua de herança e por que a constância é diferente?',
                   'body': ['<p>Uma língua de herança é uma língua ligada à história, à '
                            'ancestralidade, à identidade familiar, comunitária ou cultural de uma '
                            'pessoa ou grupo. Ela pode não ser falada no dia a dia pelo aluno, mas '
                            'carrega pertencimento, memória e desejo de reconexão.</p>',
                            '<p>No caso do iorubá, muitos brasileiros e pessoas da diáspora '
                            'afrodescendente se aproximam do idioma por motivos que vão além da '
                            'comunicação prática. Algumas querem compreender melhor cantigas e rezas. '
                            'Outras buscam honrar uma raiz cultural. Há quem estude por pesquisa, '
                            'religião, identidade, música, história, nomes ou interesse profundo na '
                            'cultura iorubá e afro-brasileira.</p>',
                            '<p>Essa motivação é poderosa, mas também delicada. Diferente de alguém '
                            'que estuda um idioma apenas para viagem ou trabalho, quem estuda uma '
                            'língua de herança costuma carregar expectativa emocional. O aluno pode '
                            'sentir que “deveria” aprender mais rápido, que está atrasado, que precisa '
                            'honrar algo importante ou que não pode errar. Essa pressão pode '
                            'atrapalhar a constância.</p>',
                            '<p>Por isso, o estudo precisa ser firme, mas acolhedor. Constância não '
                            'significa estudar horas todos os dias. Significa manter uma relação '
                            'regular, respeitosa e consciente com a língua. É melhor estudar 20 '
                            'minutos, três vezes por semana, com escuta e revisão, do que fazer uma '
                            'maratona intensa e abandonar por um mês.</p>']},
                  {'heading': 'Por que a constância trava no estudo de iorubá?',
                   'body': ['<p>A constância trava porque o aluno muitas vezes começa pelo caminho '
                            'mais difícil: conteúdos soltos, traduções sem contexto e ausência de '
                            'correção. O iorubá exige atenção a sons, tons, escrita, oralidade, '
                            'significado e uso cultural. Sem orientação, o estudante pode se sentir '
                            'perdido rapidamente.</p>',
                            '<p>Os principais motivos de bloqueio são:</p>',
                            '<h3>1. Excesso de conteúdo solto</h3>',
                            '<p>A internet oferece muitos vídeos, listas de palavras e explicações '
                            'curtas. Isso pode despertar interesse, mas também fragmenta o '
                            'aprendizado. O aluno aprende uma saudação hoje, uma cantiga amanhã, uma '
                            'palavra de origem iorubá depois, mas não entende a sequência.</p>',
                            '<h3>2. Dificuldade com pronúncia e tons</h3>',
                            '<p>O iorubá é uma língua tonal. A forma de pronunciar pode alterar o '
                            'sentido. Para quem fala português, esse é um desafio importante. Quando o '
                            'aluno não tem feedback, pode ficar inseguro e evitar falar.</p>',
                            '<h3>3. Falta de rotina realista</h3>',
                            '<p>Muitas pessoas criam planos impossíveis: estudar todos os dias por uma '
                            'hora, memorizar grandes listas e entender cantigas complexas logo no '
                            'início. Quando não conseguem cumprir, desanimam.</p>',
                            '<h3>4. Medo de desrespeitar a cultura</h3>',
                            '<p>Esse medo pode ser positivo quando leva ao cuidado, mas pode virar '
                            'paralisia. O aluno quer aprender com respeito, mas não sabe por onde '
                            'começar, o que pode repetir, o que deve evitar e quando precisa '
                            'perguntar.</p>',
                            '<h3>5. Falta de aula ao vivo</h3>',
                            '<p>Sem aula ao vivo, o aluno não consegue tirar dúvidas no momento certo. '
                            'Aprende passivamente, mas não pratica. Escuta conteúdos, mas não sabe se '
                            'está pronunciando bem. Isso reduz a confiança e enfraquece a '
                            'continuidade.</p>',
                            '<p>CTA: Se você quer estudar iorubá com orientação e respeito cultural, '
                            'fale com a Vedium sobre a próxima turma em <a '
                            'href="/curso-de-ioruba-online">https://vediums.com/</a>.</p>']},
                  {'heading': 'Como criar uma rotina realista para uma língua de herança?',
                   'body': ['<p>Para criar uma rotina realista, comece pequeno e repita com '
                            'regularidade. A constância nasce de um plano que cabe na vida real, não '
                            'de uma promessa idealizada.</p>',
                            '<p>Um bom plano semanal para iorubá pode ter três pilares:</p>',
                            '<ul><li><strong>Escuta:</strong> ouvir palavras, saudações, sons e '
                            'trechos curtos.</li><li><strong>Registro:</strong> anotar vocabulário com '
                            'contexto, não apenas tradução.</li><li><strong>Prática ao vivo:</strong> '
                            'participar de aula, repetir, perguntar e receber correção.</li></ul>',
                            '<p>Uma rotina simples:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Dia</th><th>Atividade</th><th>Tempo</th></tr></thead><tbody><tr><td>Segunda-feira</td><td>Ouvir '
                            'e repetir 5 palavras ou expressões</td><td>15 '
                            'min</td></tr><tr><td>Quarta-feira</td><td>Revisar anotações e escrever '
                            'dúvidas culturais</td><td>20 '
                            'min</td></tr><tr><td>Sexta-feira</td><td>Praticar pronúncia e gravar '
                            'áudio curto</td><td>15 min</td></tr><tr><td>Sábado ou '
                            'domingo</td><td>Aula ao vivo ou revisão guiada</td><td>60 '
                            'min</td></tr></tbody></table>',
                            '<p>Esse plano parece simples, mas funciona porque mantém contato '
                            'frequente com a língua. O objetivo não é estudar tudo. É não deixar o '
                            'vínculo esfriar.</p>',
                            '<p>Para uma língua de herança, o estudo também pode incluir um momento de '
                            'reflexão. Pergunte:</p>',
                            '<ul><li>O que essa palavra desperta em mim?</li><li>Em que contexto ela '
                            'aparece?</li><li>Que cuidado cultural devo ter?</li><li>Que dúvida quero '
                            'levar para aula?</li><li>Como posso praticar sem pressa?</li></ul>',
                            '<p>Essa abordagem une técnica e sentido. O aluno aprende com método, mas '
                            'sem apagar a dimensão emocional e cultural do idioma.</p>']},
                  {'heading': 'Como praticar com respeito sem cair na paralisia?',
                   'body': ['<p>Praticar com respeito não significa ter medo de estudar. Significa '
                            'estudar com humildade, escuta e disposição para corrigir. O respeito não '
                            'impede a prática; ele orienta a prática.</p>',
                            '<p>Aqui estão algumas atitudes importantes:</p>',
                            '<h3>Ouça antes de repetir</h3>',
                            '<p>No iorubá, som e tom importam. Antes de repetir uma palavra, escute '
                            'várias vezes. Observe ritmo, vogais, pausas e entonação. Depois, repita '
                            'devagar.</p>',
                            '<h3>Anote contexto junto com significado</h3>',
                            '<p>Evite registrar apenas “palavra = tradução”. Use um glossário mais '
                            'completo:</p>',
                            '<table class="vd-table"><thead><tr><th>Palavra ou '
                            'expressão</th><th>Pronúncia / tom</th><th>Significado '
                            'aproximado</th><th>Contexto de '
                            'uso</th><th>Dúvida</th></tr></thead><tbody></tbody></table>',
                            '<p>Esse formato ajuda a lembrar que a palavra vive dentro de uma '
                            'situação.</p>',
                            '<h3>Pergunte antes de afirmar</h3>',
                            '<p>Quando não souber se uma expressão pode ser usada em qualquer '
                            'contexto, pergunte. Quando não tiver certeza sobre o sentido de uma '
                            'cantiga, leve a dúvida para a aula. Perguntar é parte do respeito.</p>',
                            '<h3>Não transforme cultura em enfeite</h3>',
                            '<p>Evite usar palavras iorubás apenas para parecer profundo, místico ou '
                            'diferente. Antes de publicar, explicar ou usar uma expressão '
                            'culturalmente sensível, confirme se você entendeu o contexto.</p>',
                            '<h3>Aceite correção</h3>',
                            '<p>Correção não é ataque. Em uma língua de herança, correção é cuidado '
                            'com a palavra. O professor ajuda a proteger o sentido, a pronúncia e o '
                            'respeito ao idioma.</p>']},
                  {'heading': 'O papel da aula ao vivo na constância',
                   'body': ['<p>A aula ao vivo mantém a constância porque cria compromisso, interação '
                            'e direção. Quando o aluno estuda sozinho, precisa decidir tudo: o que '
                            'estudar, como revisar, se está pronunciando certo, qual material usar e '
                            'quando avançar. Isso cansa. A aula ao vivo organiza o caminho.</p>',
                            '<p>Em um curso de iorubá online ao vivo, o aluno pode:</p>',
                            '<ul><li>praticar pronúncia com correção;</li><li>entender '
                            'tons;</li><li>perguntar sobre contexto cultural;</li><li>receber '
                            'orientação sobre o que estudar;</li><li>revisar com '
                            'segurança;</li><li>aprender com interação real;</li><li>manter '
                            'compromisso semanal;</li><li>sentir acolhimento no processo.</li></ul>',
                            '<p>Esse formato é especialmente importante para quem já tentou aprender '
                            'por vídeos soltos. O problema dos vídeos não é que sejam inúteis. Eles '
                            'podem ajudar na descoberta. Mas, sem estrutura, o aluno acumula '
                            'fragmentos e não constrói base.</p>',
                            '<p>Na Vedium, a proposta é unir aulas ao vivo, profundidade cultural e '
                            'liberdade sem contrato de fidelidade. O aluno continua porque sente '
                            'evolução e valor, não porque está preso a uma obrigação longa. Isso '
                            'combina com o estudo de uma língua de herança: o vínculo precisa ser '
                            'verdadeiro, não forçado.</p>',
                            '<p>CTA: Quer transformar seu interesse por iorubá em rotina de '
                            'aprendizado? Fale com a Vedium sobre a próxima turma em <a '
                            'href="/blog/alfabeto-ioruba">https://vediums.com/</a>.</p>']},
                  {'heading': 'Como manter constância mesmo com pouco tempo?',
                   'body': ['<p>Para manter constância com pouco tempo, use uma rotina mínima. Em vez '
                            'de abandonar o estudo quando a semana estiver corrida, reduza a tarefa ao '
                            'essencial.</p>',
                            '<p>A rotina mínima pode ser:</p>',
                            '<ul><li>ouvir uma saudação por 3 minutos;</li><li>repetir uma palavra com '
                            'atenção;</li><li>revisar uma anotação;</li><li>escrever uma dúvida para a '
                            'próxima aula;</li><li>ouvir um áudio curto antes de dormir;</li><li>reler '
                            'seu glossário por 5 minutos.</li></ul>',
                            '<p>A regra é: não quebre o contato. Pouco estudo não é inútil quando '
                            'mantém o vínculo ativo. Em línguas de herança, a interrupção longa '
                            'costuma ser mais prejudicial do que uma semana de prática leve.</p>',
                            '<p>Uma estratégia prática é criar três versões de rotina:</p>',
                            '<table class="vd-table"><thead><tr><th>Tipo de rotina</th><th>Quando '
                            'usar</th><th>Exemplo</th></tr></thead><tbody><tr><td>Mínima</td><td>Semana '
                            'corrida</td><td>5 minutos de '
                            'revisão</td></tr><tr><td>Regular</td><td>Semana normal</td><td>20 '
                            'minutos, 3 vezes por semana</td></tr><tr><td>Completa</td><td>Semana '
                            'favorável</td><td>Aula ao vivo + revisão + prática de '
                            'áudio</td></tr></tbody></table>',
                            '<p>Isso evita o pensamento “já que não posso estudar direito, não vou '
                            'estudar nada”. O progresso vem da continuidade.</p>']},
                  {'heading': 'Como usar a motivação ancestral sem depender só dela?',
                   'body': ['<p>A motivação ancestral é uma força importante, mas não deve ser a única '
                            'base da rotina. Ela dá sentido, mas a constância precisa de método. Se o '
                            'aluno depender apenas da emoção inicial, pode oscilar muito.</p>',
                            '<p>Use a motivação como fonte de direção:</p>',
                            '<ul><li>quero entender melhor uma cantiga;</li><li>quero honrar minha '
                            'raiz;</li><li>quero aprender saudações com respeito;</li><li>quero '
                            'compreender nomes e sentidos;</li><li>quero estudar cultura iorubá com '
                            'profundidade.</li></ul>',
                            '<p>Depois, transforme isso em tarefa concreta:</p>',
                            '<ul><li>nesta semana vou aprender 5 saudações;</li><li>neste mês vou '
                            'praticar sons e tons básicos;</li><li>nesta aula vou perguntar sobre uma '
                            'expressão;</li><li>vou revisar meu glossário toda '
                            'quarta-feira;</li><li>vou gravar minha pronúncia uma vez por '
                            'semana.</li></ul>',
                            '<p>A emoção vira prática quando ganha forma. Esse é o ponto central da '
                            'constância.</p>']},
                  {'heading': 'Comparação: estudo solto x curso estruturado',
                   'body': ['<p>Para quem está decidindo se deve continuar sozinho ou entrar em um '
                            'curso de iorubá online, vale comparar os dois caminhos.</p>',
                            '<table class="vd-table"><thead><tr><th>Critério</th><th>Estudo '
                            'solto</th><th>Curso estruturado ao '
                            'vivo</th></tr></thead><tbody><tr><td>Organização</td><td>Depende do '
                            'aluno</td><td>Sequência guiada</td></tr><tr><td>Pronúncia</td><td>Sem '
                            'correção frequente</td><td>Correção em tempo '
                            'real</td></tr><tr><td>Cultura</td><td>Pode ficar '
                            'superficial</td><td>Contexto '
                            'explicado</td></tr><tr><td>Constância</td><td>Fácil '
                            'abandonar</td><td>Compromisso '
                            'semanal</td></tr><tr><td>Dúvidas</td><td>Ficam '
                            'acumuladas</td><td>Respondidas em aula</td></tr><tr><td>Cantigas e '
                            'rezas</td><td>Risco de interpretação rasa</td><td>Estudo com '
                            'cuidado</td></tr><tr><td>Evolução</td><td>Difícil medir</td><td>Mais '
                            'visível e acompanhada</td></tr></tbody></table>',
                            '<p>O estudo solto pode abrir a porta. O curso estruturado ajuda a '
                            'atravessar o caminho. Para uma língua de herança, essa diferença é '
                            'importante porque o aluno não busca apenas informação: busca orientação '
                            'confiável.</p>']},
                  {'heading': 'Exercício para aula ao vivo: plano de constância cultural',
                   'body': ['<p>Este exercício foi pensado para quem quer estudar iorubá com '
                            'regularidade e respeito. Leve para a aula ao vivo e preencha com o '
                            'professor.</p>',
                            '<h3>1. Meu motivo principal</h3>',
                            '<p>Complete:</p>',
                            '<p>“Eu quero estudar iorubá porque...”</p>',
                            '<p>Exemplos:</p>',
                            '<ul><li>quero entender cantigas com mais respeito;</li><li>quero me '
                            'reconectar com minha ancestralidade;</li><li>quero estudar cultura iorubá '
                            'com profundidade;</li><li>quero aprender saudações e vocabulário '
                            'inicial;</li><li>quero compreender melhor palavras que ouço em minha '
                            'comunidade.</li></ul>',
                            '<h3>2. Minha rotina possível</h3>',
                            '<p>Escolha uma opção realista:</p>',
                            '<ul><li>5 minutos por dia;</li><li>15 minutos, 3 vezes por '
                            'semana;</li><li>30 minutos, 2 vezes por semana;</li><li>aula ao vivo '
                            'semanal + revisão curta.</li></ul>',
                            '<p>Não escolha o plano mais bonito. Escolha o plano que você consegue '
                            'cumprir.</p>',
                            '<h3>3. Meu foco do mês</h3>',
                            '<p>Escolha um foco:</p>',
                            '<ul><li>sons e tons;</li><li>saudações;</li><li>vocabulário de família e '
                            'comunidade;</li><li>perguntas culturais;</li><li>glossário de palavras '
                            'iniciais;</li><li>trecho curto de cantiga com orientação;</li><li>revisão '
                            'de pronúncia.</li></ul>',
                            '<h3>4. Minha prática de respeito</h3>',
                            '<p>Defina uma regra:</p>',
                            '<ul><li>vou perguntar antes de afirmar;</li><li>vou anotar contexto junto '
                            'com tradução;</li><li>vou evitar publicar explicações sem '
                            'confirmar;</li><li>vou praticar pronúncia com correção;</li><li>vou '
                            'estudar sem pressa.</li></ul>',
                            '<h3>5. Minha pergunta para a próxima aula</h3>',
                            '<p>Escreva uma pergunta cultural ou linguística para levar ao '
                            'professor.</p>',
                            '<p>Exemplos:</p>',
                            '<ul><li>Essa palavra é usada em qual contexto?</li><li>Qual é o tom '
                            'correto?</li><li>Essa tradução é literal ou aproximada?</li><li>Posso '
                            'usar essa expressão em conversa comum?</li><li>Que cuidado devo ter com '
                            'esse termo?</li></ul>',
                            '<p>Esse exercício transforma intenção em plano. E um plano simples, '
                            'repetido com respeito, vale mais do que uma promessa grandiosa abandonada '
                            'depois de poucos dias.</p>']},
                  {'heading': 'Como medir evolução em uma língua de herança?',
                   'body': ['<p>Medir evolução em uma língua de herança não significa apenas contar '
                            'quantas palavras você sabe. Significa perceber se sua relação com a '
                            'língua está mais consciente, respeitosa e estruturada.</p>',
                            '<p>Você está evoluindo quando:</p>',
                            '<ul><li>reconhece sons que antes não percebia;</li><li>entende a '
                            'importância dos tons;</li><li>sabe fazer perguntas culturais '
                            'melhores;</li><li>pronuncia palavras com mais cuidado;</li><li>cria um '
                            'glossário com contexto;</li><li>reconhece saudações;</li><li>entende que '
                            'algumas traduções são aproximadas;</li><li>consegue explicar o que ainda '
                            'não sabe;</li><li>mantém uma rotina mínima;</li><li>participa de aulas '
                            'com dúvidas mais maduras.</li></ul>',
                            '<p>Esse tipo de progresso é real. Ele pode parecer menos espetacular do '
                            'que “aprenda tudo em 30 dias”, mas é muito mais sólido.</p>']},
                  {'heading': 'O que evitar para não perder constância?',
                   'body': ['<p>Para não perder constância, evite planos exagerados, comparação com '
                            'outras pessoas e consumo desorganizado de conteúdo. Esses três fatores '
                            'quebram a rotina.</p>',
                            '<h3>Evite planos impossíveis</h3>',
                            '<p>Não prometa estudar duas horas por dia se sua rotina não permite. '
                            'Comece menor. A constância nasce do possível.</p>',
                            '<h3>Evite comparar sua jornada</h3>',
                            '<p>Cada pessoa chega ao iorubá por uma história. Algumas têm contato '
                            'religioso, outras acadêmico, outras cultural, outras familiar. Comparação '
                            'pode gerar culpa e paralisar.</p>',
                            '<h3>Evite acumular material sem praticar</h3>',
                            '<p>Salvar vídeos não é estudar. Comprar livros não é estudar. Ter listas '
                            'não é estudar. Estudar é ouvir, repetir, perguntar, revisar e usar com '
                            'orientação.</p>',
                            '<h3>Evite fugir da pronúncia</h3>',
                            '<p>A pronúncia pode intimidar, mas precisa ser enfrentada desde cedo. '
                            'Falar com erro faz parte, desde que haja correção.</p>',
                            '<h3>Evite buscar respostas rápidas para temas profundos</h3>',
                            '<p>Cantigas, rezas, nomes e expressões culturais exigem cuidado. '
                            'Constância também é aceitar que algumas respostas vêm com tempo.</p>']},
                  {'heading': 'Conclusão com CTA forte',
                   'body': ['<p>Manter constância no estudo de uma língua de herança é um ato de '
                            'cuidado. No caso do iorubá, esse cuidado envolve disciplina, mas também '
                            'escuta, respeito, memória e orientação cultural. Não se trata de correr '
                            'para acumular palavras. Trata-se de construir uma relação viva com a '
                            'língua, entendendo sons, tons, sentidos e contextos.</p>',
                            '<p>Se você já tentou estudar por vídeos soltos e sentiu que faltava '
                            'direção, talvez o próximo passo seja entrar em uma aula ao vivo. Com '
                            'professor, correção e sequência, a constância deixa de depender apenas da '
                            'sua força de vontade e passa a fazer parte de uma experiência de '
                            'aprendizado.</p>',
                            '<p>A Vedium oferece aulas de iorubá ao vivo, com profundidade cultural e '
                            'sem contrato de fidelidade. Você aprende no seu ritmo, com respeito à '
                            'tradição e foco em evolução real. A permanência vem do resultado, da '
                            'confiança e do valor de aprender além das palavras.</p>',
                            '<p>Fale com a Vedium sobre a próxima turma de Iorubá em <a '
                            'href="/curso-de-ioruba-online">https://vediums.com/</a> e transforme seu '
                            'vínculo com a língua em uma rotina possível, respeitosa e '
                            'constante.</p>']}],
     'faqs': [{'q': 'O que é uma língua de herança?',
               'a': 'Língua de herança é uma língua ligada à ancestralidade, identidade, memória '
                    'familiar, comunitária ou cultural de uma pessoa ou grupo, mesmo quando ela não é '
                    'falada no dia a dia pelo aluno.'},
              {'q': 'Como manter constância no estudo de iorubá?',
               'a': 'Mantenha uma rotina pequena e repetível, com escuta, revisão, glossário '
                    'contextualizado e aula ao vivo. O ideal é estudar com frequência, mesmo que por '
                    'pouco tempo.'},
              {'q': 'Posso aprender iorubá sozinho?',
               'a': 'Você pode iniciar sozinho com materiais confiáveis, mas aulas ao vivo são '
                    'importantes para corrigir pronúncia, entender tons, tirar dúvidas culturais e '
                    'criar uma sequência de aprendizado.'},
              {'q': 'Como estudar iorubá com respeito?',
               'a': 'Ouça antes de repetir, anote contexto junto com tradução, pergunte antes de '
                    'afirmar, evite exotizar a cultura e aceite correção como parte do cuidado com a '
                    'língua.'},
              {'q': 'A Vedium oferece curso de iorubá online ao vivo?',
               'a': 'Sim. A Vedium oferece aulas de iorubá online e ao vivo, com foco em língua, '
                    'cultura, respeito à tradição e evolução real, sem contrato de fidelidade.'}],
     'cta_title': 'Quer aprender iorubá com pronúncia correta desde o início?',
     'cta_text': 'Aulas ao vivo, do zero ao avançado, com foco em tons e conversação real.',
     'cta_label': 'Conhecer o curso de Iorubá',
     'cta_url': '/curso-de-ioruba-online'},
    "como-os-tons-mudam-o-significado-das-palavras-em-ioruba": {'title': 'Como os tons mudam o significado das palavras em iorubá',
     'meta_description': 'Entenda por que os tons no iorubá mudam significados e como praticar '
                         'pronúncia com respeito em aulas ao vivo.',
     'h1': 'Como os tons mudam o significado das palavras em iorubá',
     'date': '2025-01-10',
     'date_display': '10 de janeiro de 2025',
     'hero_image': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Estudo de iorubá na Vedium',
     'tag': 'Iorubá',
     'category': 'ioruba',
     'lead': 'Os tons mudam o significado das palavras em iorubá porque a língua é tonal: a altura da '
             'voz não é apenas “melodia”, mas parte do sentido. Em outras palavras, duas palavras '
             'podem parecer iguais na escrita sem marcação, mas ter significados diferentes quando '
             'pronunciadas com tom alto, médio ou baixo.',
     'sections': [{'heading': '',
                   'body': ['<p>Para quem busca aprender iorubá por ancestralidade, cultura, cantigas, '
                            'rezas ou estudo sério da tradição, esse ponto é essencial. Não basta '
                            'decorar uma lista de palavras. É preciso escutar, repetir, receber '
                            'correção e compreender o contexto de uso. Uma sílaba pronunciada com o '
                            'tom errado pode alterar o que se quer dizer, gerar confusão ou esvaziar o '
                            'sentido cultural de uma expressão.</p>',
                            '<p>Na Vedium, o iorubá é tratado com profundidade e respeito. A proposta '
                            'não é transformar uma língua viva em conteúdo raso, nem reduzir cantigas '
                            'e palavras de tradição a traduções soltas. O objetivo é aprender com '
                            'orientação, em aulas ao vivo, entendendo que pronúncia, cultura e '
                            'significado caminham juntos.</p>',
                            '<p>Essa diferença é ainda mais importante para quem já tentou estudar por '
                            'vídeos curtos, PDFs soltos ou listas encontradas na internet. Esses '
                            'materiais podem até ajudar no primeiro contato, mas raramente conseguem '
                            'corrigir sua pronúncia em tempo real. E, no iorubá, ouvir e ser ouvido '
                            'faz parte do aprendizado.</p>',
                            '<p>A Vedium oferece aulas online ao vivo, com acompanhamento e sem '
                            'fidelidade. Você começa com liberdade, permanece pelo resultado e aprende '
                            'em um ambiente que respeita o idioma e a cultura que vive nele.</p>']},
                  {'heading': 'Contexto cultural do tema',
                   'body': ['<p>Os tons em iorubá são fundamentais porque fazem parte da identidade '
                            'sonora da língua. Eles ajudam a diferenciar palavras, organizar sentidos '
                            'e preservar a forma como o idioma é realmente falado, cantado e '
                            'transmitido.</p>',
                            '<p>Quando uma pessoa busca iorubá para compreender cantigas, rezas, '
                            'saudações ou nomes, a tonalidade deixa de ser apenas um detalhe técnico. '
                            'Ela passa a ser uma ponte entre som, significado e respeito. Em muitas '
                            'tradições, a oralidade tem papel central. Aquilo que se canta ou se '
                            'pronuncia não é neutro: carrega intenção, memória, reverência e '
                            'pertencimento.</p>',
                            '<p>Por isso, aprender iorubá exige uma postura diferente de simplesmente '
                            '“decorar traduções”. A pergunta não deve ser apenas “o que essa palavra '
                            'significa?”. Também é necessário perguntar:</p>',
                            '<ul><li>Como essa palavra é pronunciada?</li><li>O tom muda o '
                            'sentido?</li><li>Em que contexto ela aparece?</li><li>Ela é usada em fala '
                            'cotidiana, estudo cultural, canto, saudação ou prática '
                            'religiosa?</li><li>Há algum cuidado especial ao repeti-la?</li></ul>',
                            '<p>O iorubá costuma ser apresentado, de forma didática, com três níveis '
                            'tonais principais: tom alto, tom médio e tom baixo. Na escrita com '
                            'marcação tonal, o tom alto pode aparecer indicado por acento agudo, o tom '
                            'baixo por acento grave e o tom médio pode ficar sem marca específica. '
                            'Essa estrutura ajuda o estudante a perceber que a voz sobe, se mantém ou '
                            'desce, e que essa diferença interfere diretamente na compreensão.</p>',
                            '<p>Para quem vem do português brasileiro, isso pode parecer estranho no '
                            'começo. Em português, usamos entonação para expressar emoção, pergunta, '
                            'surpresa ou ironia. Já em uma língua tonal, a altura aplicada a certas '
                            'sílabas pode distinguir palavras. Ou seja: o tom não é apenas expressivo; '
                            'ele é linguístico.</p>',
                            '<p>Esse é um dos motivos pelos quais o estudo ao vivo faz tanta '
                            'diferença. O aluno precisa ouvir exemplos, repetir, comparar sons e '
                            'receber retorno. Ler uma palavra sem ouvir a tonalidade pode criar uma '
                            'falsa sensação de aprendizado. A pessoa acha que aprendeu, mas ainda não '
                            'sabe pronunciar com segurança.</p>',
                            '<p>Na Vedium, esse cuidado é parte da experiência. O iorubá é ensinado '
                            'como língua e cultura, não como curiosidade. O aluno aprende a perceber o '
                            'som, fazer perguntas e avançar com consciência.</p>']},
                  {'heading': 'Como praticar com respeito',
                   'body': ['<p>A melhor forma de praticar tons em iorubá é escutar antes de repetir, '
                            'repetir com orientação e evitar usar palavras sensíveis sem entender o '
                            'contexto. Pronúncia correta também é uma forma de respeito.</p>',
                            '<p>O primeiro passo é aceitar que, no início, o ouvido precisa ser '
                            'treinado. Muitos alunos querem falar rápido, mas o caminho mais seguro '
                            'começa pela escuta. Antes de tentar memorizar muitas palavras, vale '
                            'praticar poucas expressões com atenção total à altura da voz. É melhor '
                            'aprender cinco palavras com som, sentido e contexto do que decorar '
                            'cinquenta sem saber pronunciá-las.</p>',
                            '<p>Uma prática simples é dividir o estudo em três camadas:</p>',
                            '<ol><li><strong>Escuta:</strong> ouvir a palavra pronunciada com calma, '
                            'observando se a sílaba sobe, desce ou se '
                            'mantém.</li><li><strong>Repetição:</strong> pronunciar em voz alta, sem '
                            'pressa, tentando reproduzir o padrão '
                            'tonal.</li><li><strong>Correção:</strong> receber retorno de quem domina '
                            'a língua e pode explicar onde ajustar.</li></ol>',
                            '<p>Essa terceira camada é justamente a que falta em muitos estudos '
                            'solitários. Em um vídeo gravado, você ouve, mas o professor não ouve '
                            'você. Em uma aula ao vivo, a pronúncia vira prática real. O professor '
                            'pode pedir para repetir, mostrar a diferença entre tons, corrigir uma '
                            'sílaba e explicar por que aquilo muda o sentido.</p>',
                            '<p>Também é importante praticar com humildade cultural. O iorubá não deve '
                            'ser tratado como enfeite, moda ou “palavra bonita” para usar sem '
                            'critério. Para muitas pessoas, ele está ligado a espiritualidade, '
                            'ancestralidade, casa, comunidade e memória. Por isso, quanto mais '
                            'profundo o tema, maior deve ser o cuidado.</p>',
                            '<p>Uma boa regra é: não repita em público aquilo que você ainda não '
                            'compreende. Estude primeiro. Pergunte. Entenda o contexto. Reconheça que '
                            'há expressões de uso cotidiano, expressões culturais e expressões que '
                            'podem pertencer a contextos religiosos específicos. Um curso de língua '
                            'pode ajudar na base linguística, mas não substitui a orientação de uma '
                            'tradição, liderança ou comunidade quando o assunto é prática '
                            'religiosa.</p>',
                            '<p>Para organizar o estudo, crie um caderno com quatro colunas:</p>',
                            '<ul><li>Palavra ou expressão;</li><li>Marcação tonal ou pronúncia '
                            'aproximada;</li><li>Tradução inicial;</li><li>Contexto cultural ou '
                            'situação de uso.</li></ul>',
                            '<p>Esse tipo de registro evita que a palavra vire uma informação solta. '
                            'Ele ajuda o aluno a lembrar não apenas “o que significa”, mas também '
                            '“como soa” e “quando faz sentido usar”.</p>']},
                  {'heading': 'Exercício para aula ao vivo',
                   'body': ['<p>Um exercício eficaz para aprender tons em iorubá é comparar palavras '
                            'parecidas e observar como pequenas mudanças na altura da voz podem '
                            'alterar o significado. Esse exercício deve ser feito com escuta, '
                            'repetição e correção.</p>',
                            '<p>Durante uma aula ao vivo, o professor pode selecionar uma sequência '
                            'curta de palavras ou sílabas e pedir que o aluno perceba as diferenças. O '
                            'foco não é correr para traduzir tudo. O foco é educar o ouvido.</p>',
                            '<p>Veja um modelo de exercício que pode ser usado em uma aula:</p>',
                            '<ol><li>O professor apresenta três versões sonoras de uma palavra ou '
                            'sequência parecida.</li><li>O aluno apenas escuta na primeira rodada, sem '
                            'repetir.</li><li>Na segunda rodada, o aluno marca se percebeu tom alto, '
                            'médio ou baixo.</li><li>Na terceira rodada, o aluno repete cada '
                            'versão.</li><li>O professor corrige a pronúncia e explica o impacto no '
                            'significado.</li><li>O aluno registra a palavra no caderno com contexto e '
                            'observação cultural.</li><li>Ao final, o aluno cria uma frase de estudo '
                            'ou uma anotação de uso.</li></ol>',
                            '<p>Esse tipo de prática funciona porque aproxima o estudante da lógica '
                            'real da língua. Em vez de estudar iorubá como se fosse apenas texto, o '
                            'aluno entende que a palavra também vive no som.</p>',
                            '<p>Outro exercício útil é a leitura guiada. O professor apresenta '
                            'palavras com marcação tonal e ajuda o aluno a transformar o sinal gráfico '
                            'em movimento vocal. No começo, pode parecer mecânico. Com o tempo, o '
                            'ouvido começa a reconhecer padrões e a pronúncia fica mais natural.</p>',
                            '<p>Também vale praticar com cantigas, quando isso for adequado ao '
                            'objetivo do aluno e ao cuidado cultural do tema. Nesse caso, a aula deve '
                            'ir além da repetição. O professor pode trabalhar trechos curtos, explicar '
                            'sons, destacar palavras, comentar contexto e mostrar por que não se deve '
                            'separar canto, língua e significado.</p>',
                            '<p>Para a persona Adá, que busca entender o que canta e reza, esse '
                            'exercício tem um valor especial. Ele transforma a relação com o '
                            'aprendizado. A pessoa deixa de repetir sons de forma automática e começa '
                            'a perceber o que está pronunciando. Isso gera mais consciência, mais '
                            'segurança e mais respeito.</p>',
                            '<p><strong>Quer praticar tons com correção em tempo real? Acesse <a '
                            'href="/curso-de-ioruba-online">https://vediums.com/</a> e fale com a '
                            'Vedium sobre a próxima turma de Iorubá ao vivo.</strong></p>']},
                  {'heading': 'Por que os tons são difíceis para falantes de português',
                   'body': ['<p>Os tons podem ser difíceis para falantes de português porque nosso '
                            'ouvido não foi treinado, desde a infância, a usar altura vocal como '
                            'diferença de significado lexical. Por isso, o desafio é mais auditivo do '
                            'que intelectual.</p>',
                            '<p>Muitos alunos entendem a explicação rapidamente: tom alto, médio e '
                            'baixo. A dificuldade aparece na prática. A pessoa escuta uma palavra, '
                            'acha que repetiu igual, mas muda a altura de uma sílaba sem perceber. '
                            'Isso é normal. Aprender uma língua tonal exige tempo, repetição e '
                            'feedback.</p>',
                            '<p>O português usa acentos, ritmo e entonação, mas não funciona como o '
                            'iorubá nesse aspecto. Quando fazemos uma pergunta em português, por '
                            'exemplo, podemos mudar a entonação da frase. Quando demonstramos '
                            'surpresa, também mudamos a voz. Mas, em geral, essa mudança não cria '
                            'outra palavra totalmente diferente. No iorubá, a tonalidade pode estar '
                            'ligada ao próprio significado.</p>',
                            '<p>Por isso, o aluno precisa evitar um erro comum: tentar “aportuguesar” '
                            'a pronúncia. Quando isso acontece, ele força a palavra para caber no '
                            'ritmo do português e perde parte da estrutura sonora do iorubá. O estudo '
                            'fica mais seguro quando o aluno aceita ouvir de novo, repetir devagar e '
                            'ajustar a boca e o ouvido sem pressa.</p>',
                            '<p>A aula ao vivo também ajuda porque reduz a insegurança. Em vez de '
                            'estudar sozinho e ficar na dúvida se está fazendo certo, o aluno recebe '
                            'orientação. Essa troca cria confiança e evita que erros se '
                            'cristalizem.</p>']},
                  {'heading': 'Como a Vedium ajuda no aprendizado dos tons',
                   'body': ['<p>A Vedium ajuda no aprendizado dos tons porque oferece aulas ao vivo, '
                            'prática orientada e profundidade cultural. O aluno não fica sozinho '
                            'diante de uma lista de palavras: ele escuta, fala, pergunta e evolui com '
                            'acompanhamento.</p>',
                            '<p>Esse formato é especialmente importante no iorubá. Como a língua '
                            'depende muito da escuta e da pronúncia, a presença de um professor em '
                            'tempo real torna o estudo mais concreto. O aluno consegue perceber a '
                            'diferença entre entender a teoria e realmente produzir o som.</p>',
                            '<p>Nas aulas ao vivo, é possível trabalhar:</p>',
                            '<ul><li>pronúncia de palavras iniciais;</li><li>leitura com marcação '
                            'tonal;</li><li>repetição guiada;</li><li>diferença entre som e '
                            'significado;</li><li>vocabulário ligado ao contexto do '
                            'aluno;</li><li>cuidado cultural no uso de expressões;</li><li>dúvidas '
                            'sobre cantigas, saudações e nomes, sempre com respeito.</li></ul>',
                            '<p>Além disso, a Vedium trabalha com uma proposta sem fidelidade. Isso '
                            'reduz a barreira para começar. Você pode iniciar sua jornada sem medo de '
                            'ficar preso a contratos longos. A escola prefere que o aluno permaneça '
                            'porque percebe evolução, não porque foi amarrado por multa.</p>',
                            '<p>Para quem busca o iorubá por identidade, ancestralidade ou tradição, '
                            'essa postura importa. O aprendizado precisa ser sério, mas também '
                            'acolhedor. Precisa ter profundidade, mas sem elitismo. Precisa respeitar '
                            'a cultura, mas sem tornar o caminho inacessível.</p>']},
                  {'heading': 'Conclusão com CTA forte',
                   'body': ['<p>Os tons mudam o significado das palavras em iorubá porque fazem parte '
                            'da estrutura da língua. Eles não são detalhe estético, nem simples “jeito '
                            'de falar”. São parte do sentido. Para quem deseja compreender cantigas, '
                            'rezas, saudações, nomes e expressões com mais consciência, aprender a '
                            'ouvir e praticar os tons é um passo essencial.</p>',
                            '<p>Esse aprendizado pede orientação. Pede escuta. Pede correção. Pede '
                            'respeito. E é exatamente por isso que aulas ao vivo fazem diferença: você '
                            'não apenas recebe conteúdo, mas pratica com alguém que pode ouvir sua '
                            'pronúncia, responder suas dúvidas e ajudar você a construir uma base mais '
                            'segura.</p>',
                            '<p>Se você quer aprender iorubá com profundidade cultural, sem conteúdo '
                            'raso e sem contrato de fidelidade, fale com a Vedium. A fluência além das '
                            'palavras começa quando você entende não só o que se diz, mas como se diz '
                            'e por que aquilo importa.</p>',
                            '<p><strong>Acesse <a '
                            'href="/blog/alfabeto-ioruba">https://vediums.com/</a> e fale sobre a '
                            'próxima turma de Iorubá ao vivo. Você fica pelo resultado, não por '
                            'amarras.</strong></p>']}],
     'faqs': [{'q': 'O iorubá é uma língua tonal?',
               'a': 'Sim. O iorubá é uma língua tonal, o que significa que a altura da voz ajuda a '
                    'diferenciar significados. Por isso, pronunciar uma sílaba com tom alto, médio ou '
                    'baixo pode mudar a compreensão da palavra.'},
              {'q': 'Quantos tons existem no iorubá?',
               'a': 'De forma didática, o iorubá costuma ser ensinado com três tons principais: alto, '
                    'médio e baixo. A marcação tonal ajuda o aluno a perceber como a voz deve se '
                    'movimentar ao pronunciar a palavra.'},
              {'q': 'Dá para aprender os tons de iorubá sozinho?',
               'a': 'É possível começar sozinho, mas é limitado. Como os tons dependem de escuta e '
                    'correção, aulas ao vivo ajudam muito mais. O professor pode ouvir sua pronúncia, '
                    'corrigir em tempo real e explicar diferenças de sentido.'},
              {'q': 'Por que os tons são importantes em cantigas e rezas?',
               'a': 'Porque cantigas e rezas vivem no som, não apenas no texto. Quando o aluno entende '
                    'os tons, ele se aproxima melhor da pronúncia, do sentido e do contexto cultural '
                    'das palavras que canta ou escuta.'},
              {'q': 'A Vedium tem curso de iorubá online ao vivo?',
               'a': 'Sim. A Vedium oferece aulas de iorubá online ao vivo, com profundidade cultural, '
                    'prática orientada e sem fidelidade. Para saber sobre a próxima turma, acesse '
                    'https://vediums.com/.'}],
     'cta_title': 'Quer aprender iorubá com pronúncia correta desde o início?',
     'cta_text': 'Aulas ao vivo, do zero ao avançado, com foco em tons e conversação real.',
     'cta_label': 'Conhecer o curso de Iorubá',
     'cta_url': '/curso-de-ioruba-online'},
    "como-usar-perguntas-culturais-para-aprofundar-a-aula": {'title': 'Como usar perguntas culturais para aprofundar a aula',
     'meta_description': 'Aprenda a usar perguntas culturais para aprofundar aulas de iorubá com '
                         'respeito, contexto e prática ao vivo.',
     'h1': 'Como usar perguntas culturais para aprofundar a aula',
     'date': '2026-06-12',
     'date_display': '12 de junho de 2026',
     'hero_image': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Estudo de iorubá na Vedium',
     'tag': 'Iorubá',
     'category': 'ioruba',
     'lead': 'Usar perguntas culturais para aprofundar a aula de iorubá significa ir além da tradução '
             'literal e investigar o contexto, o uso, a pronúncia, a tradição e o sentido por trás das '
             'palavras. Em vez de perguntar apenas “o que isso significa?”, o aluno aprende a '
             'perguntar “em que situação essa palavra é usada?”, “qual cuidado devo ter ao repetir?”, '
             '“isso aparece em uma saudação, cantiga, reza ou conversa cotidiana?”, “a pronúncia muda '
             'o sentido?” e “qual história existe por trás desse termo?”.',
     'sections': [{'heading': '',
                   'body': ['<p>Esse tipo de pergunta transforma a aula. O iorubá deixa de ser uma '
                            'lista de vocabulário e passa a ser compreendido como língua viva, com '
                            'memória, oralidade, relações sociais e profundidade cultural. Para quem '
                            'busca aprender por ancestralidade, identidade, religiosidade, pesquisa ou '
                            'interesse cultural, essa mudança é decisiva. A aula fica mais respeitosa, '
                            'mais rica e mais conectada ao que realmente importa: entender não só as '
                            'palavras, mas o mundo que vive nelas.</p>',
                            '<p>Na Vedium, o ensino de iorubá parte dessa visão: aulas ao vivo, com '
                            'profundidade cultural e respeito à tradição. A proposta é evitar o '
                            'aprendizado raso baseado em vídeos soltos ou traduções apressadas. O '
                            'aluno aprende a ouvir, perguntar, praticar, receber correção e construir '
                            'compreensão passo a passo.</p>',
                            '<p>Neste artigo, você vai entender por que perguntas culturais aprofundam '
                            'a aula, quais perguntas levar para o professor, como praticar com '
                            'respeito e como transformar curiosidade em aprendizado responsável.</p>']},
                  {'heading': 'Por que perguntas culturais aprofundam uma aula de iorubá?',
                   'body': ['<p>Perguntas culturais aprofundam uma aula de iorubá porque ajudam o '
                            'aluno a compreender contexto, uso e sentido, não apenas tradução. Em uma '
                            'língua ligada à oralidade, à memória afro-diaspórica e a práticas '
                            'culturais profundas, perguntar melhor é uma forma de aprender com mais '
                            'respeito.</p>',
                            '<p>Muitos alunos começam o estudo do iorubá com uma pergunta legítima: “o '
                            'que essa palavra quer dizer?”. Essa pergunta é importante, mas sozinha é '
                            'limitada. Uma palavra pode ter aproximações em português, mas seu sentido '
                            'real pode depender do tom, da situação, da relação entre as pessoas, do '
                            'ambiente em que aparece e da tradição que a envolve.</p>',
                            '<p>Por exemplo, ao estudar uma saudação, não basta saber a tradução '
                            'aproximada. É preciso entender:</p>',
                            '<ul><li>quando essa saudação é usada;</li><li>para quem ela é '
                            'dirigida;</li><li>se há diferença entre uso cotidiano e uso '
                            'tradicional;</li><li>qual postura acompanha a fala;</li><li>se existe uma '
                            'resposta esperada;</li><li>como a pronúncia deve ser feita;</li><li>se há '
                            'marcas de respeito no uso.</li></ul>',
                            '<p>Perguntas culturais também ajudam a evitar o erro de tratar a cultura '
                            'iorubá como “curiosidade” ou “ornamento”. O aluno não está apenas '
                            'colecionando termos bonitos. Está se aproximando de uma língua com '
                            'história, povo, ancestralidade e presença viva. Essa postura muda '
                            'tudo.</p>',
                            '<p>Em um curso de iorubá online com aula ao vivo, esse aprofundamento se '
                            'torna ainda mais importante porque o professor pode responder, corrigir, '
                            'exemplificar e orientar em tempo real. O aluno aprende a perguntar melhor '
                            'e, com isso, aprende melhor.</p>',
                            '<p>CTA: Se você quer estudar iorubá com contexto cultural e prática ao '
                            'vivo, fale com a Vedium sobre a próxima turma em <a '
                            'href="/curso-de-ioruba-online">https://vediums.com/</a>.</p>']},
                  {'heading': 'Qual é a diferença entre perguntar “o que significa?” e perguntar “como '
                              'se usa?”',
                   'body': ['<p>A diferença é que “o que significa?” busca uma resposta curta, '
                            'enquanto “como se usa?” abre espaço para contexto, cuidado e compreensão '
                            'real. No iorubá, essa diferença é essencial.</p>',
                            '<p>Quando o aluno pergunta apenas “o que significa?”, pode receber uma '
                            'tradução aproximada e acreditar que entendeu tudo. Mas a tradução não '
                            'responde se a palavra é formal, cotidiana, ritual, poética, familiar, '
                            'comunitária ou sensível. Também não explica se há variações de pronúncia, '
                            'se o tom muda o sentido ou se o termo exige cautela.</p>',
                            '<p>A pergunta “como se usa?” é mais completa. Ela leva a outras '
                            'perguntas:</p>',
                            '<ul><li>Essa palavra aparece em conversa comum?</li><li>É usada por '
                            'qualquer pessoa?</li><li>Há uma resposta adequada?</li><li>Existe uma '
                            'situação em que não devo usar?</li><li>A palavra muda de sentido conforme '
                            'o tom?</li><li>O significado é literal ou aproximado?</li><li>Que '
                            'contexto cultural preciso conhecer?</li></ul>',
                            '<p>Essa mudança ajuda muito alunos que chegam ao iorubá motivados por '
                            'cantigas, rezas, nomes, saudações ou vivências culturais. Em vez de '
                            'buscar respostas rápidas, eles aprendem a construir entendimento.</p>',
                            '<p>Um exemplo prático: se o aluno encontra uma expressão em uma cantiga, '
                            'a pergunta mais responsável não é apenas “traduza isso”. Um caminho '
                            'melhor seria:</p>',
                            '<p>“Professor, essa expressão aparece em qual contexto? Ela tem sentido '
                            'literal ou simbólico? Há alguma nuance cultural que eu preciso entender '
                            'antes de repetir ou interpretar?”</p>',
                            '<p>Esse tipo de pergunta demonstra respeito. Mostra que o aluno não quer '
                            'apenas consumir a língua, mas aprender com responsabilidade.</p>']},
                  {'heading': 'Quais perguntas culturais levar para uma aula de iorubá?',
                   'body': ['<p>As melhores perguntas culturais são aquelas que investigam contexto, '
                            'pronúncia, uso, limites e relação com a tradição. Elas ajudam o professor '
                            'a explicar mais do que vocabulário e tornam a aula mais rica.</p>',
                            '<p>Aqui estão perguntas úteis para levar a uma aula de iorubá ao '
                            'vivo:</p>',
                            '<h3>Perguntas sobre contexto</h3>',
                            '<ul><li>Em que situação essa palavra é usada?</li><li>Essa expressão é '
                            'cotidiana, formal, cultural ou religiosa?</li><li>Quem costuma usar essa '
                            'saudação?</li><li>Existe diferença entre falar isso em uma aula e em uma '
                            'comunidade?</li><li>Essa palavra aparece mais na fala, em cantigas, em '
                            'rezas ou em textos?</li></ul>',
                            '<h3>Perguntas sobre pronúncia e tons</h3>',
                            '<ul><li>Qual é o tom correto dessa palavra?</li><li>Se eu mudar o tom, o '
                            'sentido muda?</li><li>Qual erro de pronúncia é mais comum para '
                            'brasileiros?</li><li>Posso repetir devagar para você '
                            'corrigir?</li><li>Existe diferença entre a forma escrita e a forma '
                            'falada?</li></ul>',
                            '<h3>Perguntas sobre tradução</h3>',
                            '<ul><li>A tradução em português é literal ou aproximada?</li><li>Existe '
                            'alguma palavra em português que não alcança bem o sentido?</li><li>Essa '
                            'expressão tem mais de uma interpretação?</li><li>O significado muda '
                            'conforme o contexto?</li><li>Como eu posso explicar essa palavra sem '
                            'simplificar demais?</li></ul>',
                            '<h3>Perguntas sobre respeito cultural</h3>',
                            '<ul><li>Essa expressão exige algum cuidado ao ser usada?</li><li>Há '
                            'situações em que não devo repetir?</li><li>O que seria uma forma '
                            'desrespeitosa de usar esse termo?</li><li>Existe uma postura adequada ao '
                            'estudar esse tema?</li><li>Que contexto histórico ou cultural devo '
                            'conhecer antes de avançar?</li></ul>',
                            '<h3>Perguntas sobre continuidade do estudo</h3>',
                            '<ul><li>O que preciso aprender antes de estudar esse tema com mais '
                            'profundidade?</li><li>Qual vocabulário básico ajuda a entender esse '
                            'assunto?</li><li>Que exercício posso fazer até a próxima '
                            'aula?</li><li>Como posso revisar sem distorcer o sentido?</li><li>Qual é '
                            'o próximo passo para estudar isso com responsabilidade?</li></ul>',
                            '<p>Essas perguntas mostram maturidade de aprendizado. Elas ajudam a aula '
                            'a sair do nível “palavra e tradução” e entrar no nível “língua, cultura e '
                            'uso”.</p>']},
                  {'heading': 'Como perguntas culturais ajudam quem quer entender cantigas e rezas?',
                   'body': ['<p>Perguntas culturais ajudam porque cantigas e rezas não devem ser '
                            'tratadas como textos comuns para tradução rápida. Elas podem carregar '
                            'camadas de som, ritmo, função, contexto, memória e sentido que exigem '
                            'orientação.</p>',
                            '<p>Muitas pessoas chegam ao estudo do iorubá com o desejo de entender o '
                            'que cantam ou rezam. Esse desejo é profundo e legítimo. Mas justamente '
                            'por ser profundo, precisa de cuidado. Apressar a tradução pode gerar '
                            'interpretações rasas. Repetir palavras sem entender o contexto pode levar '
                            'a usos inadequados. Tentar explicar tudo sozinho a partir de listas '
                            'soltas pode criar confusão.</p>',
                            '<p>Em vez de pedir apenas “traduza essa cantiga”, o aluno pode '
                            'perguntar:</p>',
                            '<ul><li>Qual é o contexto dessa cantiga?</li><li>Que palavras aparecem '
                            'com frequência nela?</li><li>Essa expressão tem sentido literal ou '
                            'simbólico?</li><li>Existe relação entre a pronúncia e o ritmo?</li><li>Há '
                            'alguma palavra que exige cuidado especial?</li><li>O que eu preciso '
                            'estudar antes de interpretar esse trecho?</li><li>Essa cantiga pode ter '
                            'variações?</li><li>Como devo registrar minhas dúvidas sem afirmar o que '
                            'ainda não entendi?</li></ul>',
                            '<p>Esse caminho transforma a aula em investigação respeitosa. O aluno '
                            'aprende a ouvir melhor, identificar palavras, reconhecer padrões e '
                            'compreender que algumas respostas dependem de contexto e orientação.</p>',
                            '<p>A aula ao vivo é fundamental aqui. O professor pode ouvir a dúvida, '
                            'explicar os limites, corrigir pronúncia e orientar o estudante sobre como '
                            'avançar sem desrespeitar a tradição.</p>']},
                  {'heading': 'Como praticar com respeito depois da aula?',
                   'body': ['<p>Praticar com respeito depois da aula significa revisar o conteúdo sem '
                            'transformar explicações em certezas apressadas. O aluno deve ouvir, '
                            'anotar contexto, repetir com cuidado e separar o que entendeu do que '
                            'ainda precisa confirmar.</p>',
                            '<p>Um bom método de prática é criar um caderno de perguntas culturais. Em '
                            'vez de anotar apenas traduções, organize assim:</p>',
                            '<table class="vd-table"><thead><tr><th>Palavra ou '
                            'expressão</th><th>Tradução aproximada</th><th>Contexto de '
                            'uso</th><th>Pronúncia / tom</th><th>Dúvidas '
                            'culturais</th></tr></thead><tbody></tbody></table>',
                            '<p>Esse formato ajuda a lembrar que a palavra não está sozinha. Ela tem '
                            'som, uso, contexto e limites.</p>',
                            '<p>Depois da aula, siga estes passos:</p>',
                            '<ol><li>Revise as palavras estudadas.</li><li>Escute a pronúncia '
                            'novamente, se tiver material de apoio.</li><li>Repita devagar, sem '
                            'pressa.</li><li>Anote as dúvidas que surgirem.</li><li>Escreva uma '
                            'pergunta para a próxima aula.</li><li>Evite publicar explicações antes de '
                            'confirmar.</li><li>Não use termos sensíveis como decoração '
                            'estética.</li></ol>',
                            '<p>Esse último ponto é importante. Aprender iorubá com respeito significa '
                            'não transformar a língua em enfeite de legenda, tatuagem, marca pessoal '
                            'ou postagem sem compreensão. A língua carrega memória. O estudo precisa '
                            'acompanhar essa responsabilidade.</p>',
                            '<p>CTA: Quer aprender iorubá com orientação, correção e contexto '
                            'cultural? Fale com a Vedium sobre a próxima turma em <a '
                            'href="/blog/alfabeto-ioruba">https://vediums.com/</a>.</p>']},
                  {'heading': 'Como transformar curiosidade em aprendizado responsável?',
                   'body': ['<p>Transformar curiosidade em aprendizado responsável exige método. A '
                            'curiosidade abre a porta; a responsabilidade mostra como atravessar.</p>',
                            '<p>A curiosidade costuma aparecer assim:</p>',
                            '<ul><li>“Ouvi essa palavra em uma cantiga.”</li><li>“Vi esse termo em uma '
                            'postagem.”</li><li>“Quero entender o significado de um '
                            'nome.”</li><li>“Escutei uma saudação no terreiro.”</li><li>“Li uma '
                            'expressão e fiquei com dúvida.”</li><li>“Quero saber se estou '
                            'pronunciando certo.”</li></ul>',
                            '<p>O próximo passo é organizar essa curiosidade em perguntas melhores. '
                            'Por exemplo:</p>',
                            '<table class="vd-table"><thead><tr><th>Curiosidade '
                            'inicial</th><th>Pergunta mais profunda</th></tr></thead><tbody><tr><td>O '
                            'que significa essa palavra?</td><td>Em que contexto essa palavra é usada '
                            'e qual é sua tradução aproximada?</td></tr><tr><td>Como pronuncia '
                            'isso?</td><td>Qual é a pronúncia correta e como os tons mudam o '
                            'sentido?</td></tr><tr><td>Posso usar essa expressão?</td><td>Em quais '
                            'situações essa expressão é adequada ou inadequada?</td></tr><tr><td>Essa '
                            'cantiga quer dizer o quê?</td><td>Que palavras desse trecho podemos '
                            'estudar com cuidado antes de interpretar o '
                            'conjunto?</td></tr><tr><td>Esse nome significa o quê?</td><td>Qual é o '
                            'contexto linguístico e cultural desse nome?</td></tr></tbody></table>',
                            '<p>Esse processo torna o aluno mais ativo. Ele não espera apenas '
                            'respostas prontas. Ele participa da construção do entendimento.</p>']},
                  {'heading': 'Exercício para aula ao vivo: o roteiro das 7 perguntas culturais',
                   'body': ['<p>Este exercício pode ser usado em qualquer aula de iorubá ao vivo para '
                            'aprofundar um termo, saudação, expressão ou trecho de cantiga.</p>',
                            '<p>Escolha uma palavra ou expressão e responda com o professor:</p>',
                            '<h3>1. Onde essa palavra aparece?</h3>',
                            '<p>Ela aparece em conversa cotidiana, saudação, cantiga, reza, nome, '
                            'texto, contexto familiar, ambiente cultural ou situação específica?</p>',
                            '<h3>2. Como se pronuncia corretamente?</h3>',
                            '<p>Observe sons, vogais, ritmo e tons. Repita devagar e peça '
                            'correção.</p>',
                            '<h3>3. Qual é a tradução aproximada?</h3>',
                            '<p>Anote a tradução, mas marque se ela é literal, aproximada ou '
                            'dependente de contexto.</p>',
                            '<h3>4. Qual é o contexto cultural?</h3>',
                            '<p>Pergunte que cuidado, história, relação social ou tradição ajuda a '
                            'entender melhor a palavra.</p>',
                            '<h3>5. Quem usa e para quem?</h3>',
                            '<p>Algumas expressões podem depender de idade, respeito, posição, relação '
                            'ou situação. Pergunte se há alguma marca social no uso.</p>',
                            '<h3>6. O que devo evitar?</h3>',
                            '<p>Pergunte se existe uso inadequado, pronúncia perigosa, interpretação '
                            'rasa ou contexto em que não convém repetir.</p>',
                            '<h3>7. Como posso praticar até a próxima aula?</h3>',
                            '<p>Peça um exercício seguro: repetir pronúncia, montar glossário, ouvir '
                            'áudio, revisar vocabulário relacionado ou preparar nova pergunta.</p>',
                            '<p>Esse roteiro ajuda a transformar qualquer dúvida em aprendizado '
                            'estruturado. Ele também evita que a aula se perca em curiosidades soltas. '
                            'Cada pergunta aprofunda a anterior.</p>']},
                  {'heading': 'Como perguntas culturais melhoram a relação com o professor?',
                   'body': ['<p>Perguntas culturais melhoram a relação com o professor porque mostram '
                            'que o aluno está comprometido com aprendizado profundo, não apenas com '
                            'respostas rápidas. A aula se torna uma troca mais rica.</p>',
                            '<p>Quando o aluno pergunta com cuidado, o professor percebe que pode ir '
                            'além da explicação básica. Pode falar sobre nuance, contexto, história, '
                            'uso, variação e respeito. Isso cria uma relação de confiança. O aluno '
                            'também se sente mais seguro para dizer: “não entendi”, “posso repetir?”, '
                            '“essa interpretação está correta?”, “qual cuidado devo ter?”.</p>',
                            '<p>Em uma aula de iorubá, essa confiança é muito importante. Muitos '
                            'alunos chegam com vínculo emocional forte: querem honrar a '
                            'ancestralidade, compreender cantigas, se aproximar da cultura ou estudar '
                            'uma língua ligada à sua trajetória espiritual e identitária. A aula '
                            'precisa acolher essa motivação sem perder rigor.</p>',
                            '<p>Boas perguntas ajudam a equilibrar acolhimento e seriedade.</p>']},
                  {'heading': 'Como perguntas culturais fortalecem a memória?',
                   'body': ['<p>Perguntas culturais fortalecem a memória porque criam conexão entre '
                            'palavra, história e uso. O cérebro lembra melhor aquilo que tem '
                            'significado. Quando uma palavra é estudada com contexto, ela deixa de ser '
                            'um item isolado e passa a fazer parte de uma rede de sentidos.</p>',
                            '<p>Compare duas formas de estudo:</p>',
                            '<ul><li>Decorar: “palavra X = significado Y”.</li><li>Compreender: '
                            '“palavra X aparece em tal contexto, é pronunciada assim, tem esse tom, '
                            'pode ser usada nessa situação, mas exige cuidado nessa outra”.</li></ul>',
                            '<p>A segunda forma exige mais atenção, mas gera memória mais profunda. O '
                            'aluno não apenas reconhece a palavra; ele entende onde ela vive.</p>',
                            '<p>Isso é especialmente útil para vocabulário ligado a relações sociais, '
                            'saudações, respeito, comunidade, cantigas e expressões culturais. Quando '
                            'o aluno entende o contexto, a palavra ganha corpo.</p>']},
                  {'heading': 'O que evitar ao fazer perguntas culturais?',
                   'body': ['<p>Ao fazer perguntas culturais, evite pressa, sensacionalismo e '
                            'exigência de respostas definitivas para temas que podem depender de '
                            'contexto. Nem toda questão cultural cabe em uma tradução simples.</p>',
                            '<p>Evite perguntas formuladas assim:</p>',
                            '<ul><li>“Qual é a tradução exata e definitiva?”</li><li>“Como eu uso isso '
                            'para impressionar?”</li><li>“Me ensina só a parte forte.”</li><li>“Dá '
                            'para resumir toda a cantiga?”</li><li>“Posso usar essa palavra em '
                            'qualquer lugar?”</li><li>“Isso é só simbólico, né?”</li></ul>',
                            '<p>Essas perguntas podem reduzir a complexidade do tema. Uma forma melhor '
                            'seria:</p>',
                            '<ul><li>“Qual é a tradução aproximada nesse contexto?”</li><li>“Que '
                            'cuidado devo ter com essa expressão?”</li><li>“O que eu preciso entender '
                            'antes de interpretar esse trecho?”</li><li>“Essa palavra tem uso '
                            'cotidiano ou específico?”</li><li>“Existe algum limite para repetir ou '
                            'explicar isso?”</li></ul>',
                            '<p>A maneira como o aluno pergunta já revela sua postura. Perguntar com '
                            'respeito é parte do aprendizado.</p>']},
                  {'heading': 'Por que aulas ao vivo são melhores para perguntas culturais?',
                   'body': ['<p>Aulas ao vivo são melhores para perguntas culturais porque permitem '
                            'diálogo, correção e aprofundamento imediato. Em conteúdos gravados, o '
                            'aluno recebe uma explicação pronta. Na aula ao vivo, ele pode dizer onde '
                            'está sua dúvida, repetir a palavra, perguntar sobre contexto e ajustar a '
                            'compreensão.</p>',
                            '<p>A aula ao vivo permite:</p>',
                            '<ul><li>corrigir pronúncia;</li><li>explicar tons;</li><li>diferenciar '
                            'tradução literal e sentido cultural;</li><li>responder dúvidas '
                            'específicas;</li><li>adaptar exemplos ao aluno;</li><li>aprofundar com '
                            'cuidado;</li><li>orientar o que não deve ser simplificado;</li><li>criar '
                            'exercícios personalizados.</li></ul>',
                            '<p>Em um curso de iorubá online, isso faz muita diferença. O aluno não '
                            'fica sozinho tentando interpretar materiais soltos. Ele tem um caminho, '
                            'uma pessoa para orientar e um espaço seguro para perguntar.</p>',
                            '<p>Na Vedium, as aulas ao vivo valorizam justamente essa experiência: '
                            'aprender com gente real, em tempo real, com respeito à cultura e sem '
                            'fidelidade. A permanência vem do resultado, da confiança e do valor '
                            'percebido.</p>']},
                  {'heading': 'Como a Vedium entende o ensino de iorubá?',
                   'body': ['<p>A Vedium entende o ensino de iorubá como uma união entre língua, '
                            'cultura e responsabilidade. A proposta não é entregar apenas palavras '
                            'isoladas, mas ajudar o aluno a compreender sentido, uso e contexto.</p>',
                            '<p>Isso aparece em quatro princípios:</p>',
                            '<ul><li><strong>Aula ao vivo de verdade:</strong> interação, pergunta, '
                            'resposta e correção em tempo real.</li><li><strong>Idioma + '
                            'cultura:</strong> aprender a língua junto com o mundo que vive '
                            'nela.</li><li><strong>Evolução real:</strong> avançar com base, nível, '
                            'prática e acompanhamento.</li><li><strong>Sem amarras:</strong> estudar '
                            'sem contrato de fidelidade, ficando pelo resultado.</li></ul>',
                            '<p>Para a persona Adá, isso é essencial. Quem quer entender o que canta, '
                            'reza ou pesquisa precisa de respeito, profundidade e orientação. Não quer '
                            'conteúdo raso. Não quer exotização. Quer aprender com seriedade.</p>']},
                  {'heading': 'Conclusão com CTA forte',
                   'body': ['<p>Usar perguntas culturais para aprofundar a aula de iorubá é uma das '
                            'formas mais responsáveis de aprender. Boas perguntas ajudam a sair da '
                            'tradução literal e entrar no território do contexto, da pronúncia, dos '
                            'tons, do uso, da memória e do respeito. Elas transformam a aula em um '
                            'espaço de investigação viva, onde cada palavra pode ser compreendida com '
                            'mais cuidado.</p>',
                            '<p>Se você busca iorubá por ancestralidade, identidade, fé, pesquisa ou '
                            'amor à cultura, não se contente com respostas rápidas. Pergunte melhor. '
                            'Ouça mais. Pratique com orientação. Leve suas dúvidas para uma aula ao '
                            'vivo e permita que o aprendizado aconteça além das palavras.</p>',
                            '<p>A Vedium oferece aulas de iorubá ao vivo, com profundidade cultural e '
                            'sem contrato de fidelidade. Você aprende no seu ritmo, com correção, '
                            'contexto e respeito à tradição.</p>',
                            '<p>Fale com a Vedium sobre a próxima turma de Iorubá em <a '
                            'href="/curso-de-ioruba-online">https://vediums.com/</a> e comece a '
                            'transformar suas perguntas em caminho de aprendizado.</p>']}],
     'faqs': [{'q': 'Por que fazer perguntas culturais em uma aula de iorubá?',
               'a': 'Porque perguntas culturais ajudam a entender contexto, uso, respeito, pronúncia e '
                    'sentido. Elas evitam traduções rasas e tornam o aprendizado mais profundo e '
                    'responsável.'},
              {'q': 'Que tipo de pergunta devo levar para uma aula de iorubá?',
               'a': 'Leve perguntas sobre contexto de uso, pronúncia, tons, tradução aproximada, '
                    'cuidado cultural, situações adequadas e formas corretas de praticar até a próxima '
                    'aula.'},
              {'q': 'Perguntas culturais ajudam a entender cantigas e rezas?',
               'a': 'Sim. Cantigas e rezas podem ter camadas linguísticas e culturais. Perguntas bem '
                    'formuladas ajudam a estudar trechos com cuidado, sem reduzir tudo a uma tradução '
                    'rápida.'},
              {'q': 'Posso estudar cultura iorubá apenas com conteúdos gravados?',
               'a': 'Conteúdos gravados podem ajudar no primeiro contato, mas aulas ao vivo são '
                    'melhores para tirar dúvidas, corrigir pronúncia, entender contexto e praticar com '
                    'orientação.'},
              {'q': 'A Vedium oferece curso de iorubá online ao vivo?',
               'a': 'Sim. A Vedium oferece aulas de iorubá online e ao vivo, com foco em língua, '
                    'cultura, respeito à tradição e evolução real, sem contrato de fidelidade.'}],
     'cta_title': 'Quer aprender iorubá com pronúncia correta desde o início?',
     'cta_text': 'Aulas ao vivo, do zero ao avançado, com foco em tons e conversação real.',
     'cta_label': 'Conhecer o curso de Iorubá',
     'cta_url': '/curso-de-ioruba-online'},
    "o-que-e-o-idioma-ioruba-e-por-que-ele-carrega-cultura-e-memoria": {'title': 'O que é o idioma iorubá e por que ele carrega cultura e memória',
     'meta_description': 'Entenda o que é o idioma iorubá, sua relação com cultura e memória, e como '
                         'aprender com respeito em aulas ao vivo.',
     'h1': 'O que é o idioma iorubá e por que ele carrega cultura e memória',
     'date': '2025-01-03',
     'date_display': '3 de janeiro de 2025',
     'hero_image': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Estudo de iorubá na Vedium',
     'tag': 'Iorubá',
     'category': 'ioruba',
     'lead': 'O idioma iorubá é uma língua viva, profunda e ligada a uma das tradições culturais mais '
             'influentes da África Ocidental e da diáspora afro-atlântica. Para muitas pessoas no '
             'Brasil, aprender iorubá não é apenas estudar vocabulário: é buscar sentido, '
             'ancestralidade, identidade e compreensão do que se canta, reza, ouve e pratica em '
             'contextos religiosos, culturais e comunitários.',
     'sections': [{'heading': '',
                   'body': ['<p>Na Vedium, olhamos para o iorubá com o respeito que o tema exige. Uma '
                            'língua não é uma lista de palavras soltas. Ela carrega memória, formas de '
                            'pensar, modos de saudar, histórias de povo, espiritualidade, música, '
                            'oralidade e pertencimento. Por isso, quem procura um curso de iorubá '
                            'online normalmente não está buscando apenas “aprender frases”. Está '
                            'buscando entender o que existe por trás das palavras.</p>',
                            '<p>Esse é o ponto central: o iorubá não deve ser tratado como curiosidade '
                            'exótica, ornamento de marketing ou conteúdo raso para decorar expressões. '
                            'Ele precisa ser estudado com contexto, cuidado e orientação. '
                            'Especialmente quando aparece em cantigas, rezas, nomes, saudações e '
                            'práticas de matriz africana no Brasil, cada termo pode carregar camadas '
                            'de significado que não se explicam bem em uma tradução literal.</p>',
                            '<p>Se você já tentou aprender por vídeos soltos, listas de palavras ou '
                            'conteúdos fragmentados, talvez tenha sentido exatamente isso: informação '
                            'existe, mas falta caminho. Falta alguém ao vivo para explicar, corrigir, '
                            'contextualizar e mostrar como aquela palavra vive dentro da cultura. É '
                            'aqui que uma aula ao vivo faz diferença.</p>',
                            '<p>Na Vedium, a proposta é simples e séria: aprender iorubá com '
                            'profundidade cultural, em aulas ao vivo, no seu ritmo e sem contrato de '
                            'fidelidade. Você continua porque percebe resultado, não porque está preso '
                            'a uma multa.</p>']},
                  {'heading': 'Contexto cultural do tema',
                   'body': ['<p>O iorubá importa porque é uma língua de cultura, memória e '
                            'pertencimento. Ela conecta pessoas a histórias, territórios, rituais, '
                            'cantigas, nomes, saudações e formas de compreender o mundo que '
                            'atravessaram gerações.</p>',
                            '<p>Quando falamos em idioma iorubá, falamos de uma língua relacionada ao '
                            'povo iorubá, historicamente presente em regiões da África Ocidental, '
                            'especialmente na Nigéria e em áreas vizinhas. Mas sua importância não se '
                            'limita ao continente africano. Pela história da diáspora, muitos '
                            'elementos linguísticos, religiosos, musicais e simbólicos atravessaram o '
                            'Atlântico e permaneceram vivos em diferentes comunidades '
                            'afrodescendentes, inclusive no Brasil.</p>',
                            '<p>Por isso, para muita gente, aprender iorubá é uma forma de escutar '
                            'melhor a própria história. É compreender que certas palavras não são '
                            'apenas sons repetidos em uma cantiga. Elas podem expressar respeito, '
                            'saudação, pedido, reverência, qualidade, relação, força, origem ou '
                            'memória.</p>',
                            '<p>Na prática, isso muda tudo. Uma pessoa pode cantar algo durante anos '
                            'e, em algum momento, perceber que deseja saber o que está dizendo. Pode '
                            'ouvir uma saudação e querer entender sua estrutura. Pode encontrar um '
                            'nome de origem iorubá e querer compreender seu sentido. Pode participar '
                            'de uma comunidade religiosa ou cultural e sentir que precisa de uma base '
                            'mais séria para não depender apenas de traduções soltas.</p>',
                            '<p>Essa busca é legítima. E também exige responsabilidade.</p>',
                            '<p>Aprender iorubá com respeito significa reconhecer que a língua tem '
                            'vida própria. Ela não existe apenas para ser “usada” em um ritual ou em '
                            'uma postagem. Ela pertence a uma tradição ampla, com história, variações, '
                            'usos e contextos. Por isso, a pergunta “o que essa palavra significa?” '
                            'nem sempre tem uma resposta curta. Às vezes, a resposta correta começa '
                            'com: “depende do contexto”.</p>',
                            '<p>É por isso que cursos apenas gravados ou conteúdos muito resumidos '
                            'podem deixar lacunas. Eles podem até apresentar uma palavra, mas '
                            'dificilmente respondem às dúvidas que aparecem no caminho: como '
                            'pronunciar? Em que contexto se usa? Essa tradução está completa? Esse '
                            'termo tem sentido religioso, cotidiano ou ambos? Essa expressão deve ser '
                            'dita por qualquer pessoa? Existe cuidado cultural envolvido?</p>',
                            '<p>Em uma aula ao vivo, essas perguntas ganham espaço. E, quando o '
                            'assunto é iorubá, espaço para pergunta é parte essencial do '
                            'aprendizado.</p>']},
                  {'heading': 'Como praticar com respeito',
                   'body': ['<p>Praticar iorubá com respeito significa estudar a língua sem separar '
                            'palavra, cultura e contexto. O objetivo não é decorar sons, mas '
                            'compreender sentidos com cuidado.</p>',
                            '<p>Para começar, uma boa prática é abandonar a pressa de “traduzir tudo '
                            'ao pé da letra”. Muitas línguas carregam expressões que não cabem '
                            'perfeitamente em português. No iorubá, isso pode ser ainda mais sensível '
                            'porque várias palavras aparecem ligadas a cantos, nomes, saudações, '
                            'hierarquias, narrativas e práticas tradicionais. Uma tradução literal '
                            'pode ajudar, mas raramente esgota o significado.</p>',
                            '<p>O primeiro passo é criar uma base segura:</p>',
                            '<ul><li>aprender saudações e expressões iniciais;</li><li>compreender '
                            'sons e pronúncia com orientação;</li><li>estudar vocabulário essencial '
                            'com contexto;</li><li>diferenciar uso cotidiano, cultural e '
                            'ritual;</li><li>perguntar antes de repetir expressões '
                            'sensíveis;</li><li>reconhecer que cada casa, comunidade ou tradição pode '
                            'ter modos próprios de ensinar e preservar saberes.</li></ul>',
                            '<p>Esse último ponto é importante. Um curso de iorubá não deve substituir '
                            'a orientação espiritual, religiosa ou comunitária de uma casa, liderança '
                            'ou tradição. O papel do curso é oferecer base linguística, consciência '
                            'cultural e prática orientada. Quando o aluno entende isso, ele aprende '
                            'com mais humildade e mais profundidade.</p>',
                            '<p>Outro cuidado essencial é a pronúncia. Muitas pessoas começam pelo '
                            'texto escrito, mas uma língua também vive no som. Em cantigas e rezas, '
                            'por exemplo, pequenas diferenças de pronúncia podem alterar a percepção '
                            'da palavra. Por isso, estudar sozinho por leitura pode ser limitado. O '
                            'aluno precisa ouvir, repetir, ser corrigido e construir segurança '
                            'gradualmente.</p>',
                            '<p>Aqui entram as aulas ao vivo da Vedium. Em vez de assistir a um vídeo '
                            'e ficar sem saber se pronunciou corretamente, você pratica com professor, '
                            'tira dúvidas em tempo real e aprende dentro de uma sequência. Isso evita '
                            'um problema comum: acumular palavras soltas sem conseguir formar '
                            'entendimento.</p>',
                            '<p>Também é importante praticar com intenção. Uma pessoa que busca o '
                            'iorubá por ancestralidade talvez tenha necessidades diferentes de alguém '
                            'que pesquisa cultura afro-brasileira academicamente. Quem quer '
                            'compreender cantigas e rezas pode precisar de um caminho diferente de '
                            'quem deseja começar por conversação básica. Um bom curso reconhece essas '
                            'diferenças e organiza o aprendizado sem desrespeitar a profundidade do '
                            'tema.</p>',
                            '<p>Na Vedium, a comunicação sobre iorubá parte de um princípio: respeito '
                            'não é detalhe, é fundamento. A língua não é tratada como promessa '
                            'milagrosa nem como fórmula rápida. A evolução acontece aula após aula, '
                            'com escuta, prática e acompanhamento.</p>',
                            '<p>Se você sente que já passou da fase de repetir palavras sem entender, '
                            'talvez este seja o momento de aprender com estrutura.</p>',
                            '<p><strong>Quer começar com orientação real? Acesse <a '
                            'href="/curso-de-ioruba-online">https://vediums.com/</a> e fale com a '
                            'Vedium sobre a próxima turma de Iorubá ao vivo.</strong></p>']},
                  {'heading': 'Exercício para aula ao vivo',
                   'body': ['<p>Um bom exercício inicial é escolher uma palavra, saudação ou trecho '
                            'curto e investigar não apenas “a tradução”, mas o contexto de uso. Esse '
                            'processo ajuda o aluno a sair da memorização mecânica e entrar na '
                            'compreensão cultural.</p>',
                            '<p>Veja um modelo simples de exercício para levar a uma aula ao vivo:</p>',
                            '<ol><li>Escolha uma expressão curta que você já ouviu em uma cantiga, '
                            'saudação, conversa ou estudo.</li><li>Escreva como você ouviu, mesmo que '
                            'não tenha certeza da grafia.</li><li>Anote onde essa expressão apareceu: '
                            'canto, reza, nome, cumprimento, conversa, texto ou aula.</li><li>Diga o '
                            'que você imagina que ela significa.</li><li>Peça ao professor para ajudar '
                            'com pronúncia, grafia, sentido e contexto.</li><li>Depois da explicação, '
                            'crie uma frase de estudo ou uma anotação cultural com suas próprias '
                            'palavras.</li></ol>',
                            '<p>Esse tipo de exercício funciona porque respeita a complexidade da '
                            'língua. Em vez de tratar o iorubá como um dicionário isolado, você começa '
                            'pelo uso real. A aula ao vivo permite que o professor corrija caminhos, '
                            'explique nuances e mostre quando uma tradução está incompleta.</p>',
                            '<p>Por exemplo, ao estudar uma saudação, a pergunta não deve ser apenas '
                            '“qual é a tradução?”. Perguntas melhores seriam:</p>',
                            '<ul><li>Em que situação essa saudação é usada?</li><li>Ela é formal, '
                            'cotidiana, religiosa ou cultural?</li><li>Há diferença entre dizer, '
                            'cantar e escrever?</li><li>Existe cuidado específico para quem está '
                            'aprendendo?</li><li>Como pronunciar de forma mais respeitosa?</li></ul>',
                            '<p>Essas perguntas fazem o aprendizado crescer. Elas transformam a aula '
                            'em uma experiência de escuta e reflexão, não apenas em repetição.</p>',
                            '<p>Outro exercício poderoso é montar um “caderno de memória linguística”. '
                            'Nele, cada nova palavra aprendida deve ter quatro campos: palavra, '
                            'pronúncia aproximada, contexto e observação cultural. Com o tempo, esse '
                            'caderno se torna mais que material de estudo. Ele vira um registro da sua '
                            'caminhada com o idioma.</p>',
                            '<p>Essa prática também ajuda a evitar um erro comum: aprender várias '
                            'palavras em um dia e esquecer quase tudo na semana seguinte. Quando o '
                            'aluno registra contexto, o cérebro cria conexão. E, quando pratica ao '
                            'vivo, a palavra deixa de ser apenas informação e começa a virar '
                            'uso.</p>']},
                  {'heading': 'Por que aprender iorubá online ao vivo',
                   'body': ['<p>Aprender iorubá online ao vivo une acesso, orientação e profundidade. '
                            'Você pode estudar de onde estiver, mas sem abrir mão da presença de um '
                            'professor em tempo real.</p>',
                            '<p>Esse formato é especialmente útil para quem tem rotina cheia, mora '
                            'longe de centros culturais específicos ou não encontra professores '
                            'qualificados perto de casa. O online amplia o acesso. O ao vivo preserva '
                            'a interação. Essa combinação é essencial para uma língua que pede escuta, '
                            'pronúncia, pergunta e correção.</p>',
                            '<p>Além disso, aulas ao vivo criam compromisso. Não é a mesma coisa que '
                            'salvar uma playlist para ver depois e nunca terminar. Quando existe '
                            'horário, turma, professor e acompanhamento, o aprendizado ganha ritmo. E, '
                            'quando esse ritmo vem sem fidelidade, a relação fica mais honesta: o '
                            'aluno permanece porque sente evolução.</p>',
                            '<p>Para a persona que busca ancestralidade, identidade e compreensão '
                            'cultural, isso tem ainda mais valor. Não se trata apenas de completar '
                            'módulos. Trata-se de se aproximar de uma língua com cuidado. Trata-se de '
                            'aprender sem pressa irresponsável, mas também sem ficar perdido em '
                            'conteúdos fragmentados.</p>',
                            '<p>A Vedium oferece esse caminho com aulas ao vivo, proposta cultural e '
                            'liberdade para o aluno começar sem amarras. Essa combinação reduz o medo '
                            'de entrar em “mais um curso” e aumenta a confiança de estudar com '
                            'seriedade.</p>']},
                  {'heading': 'Conclusão com CTA forte',
                   'body': ['<p>O idioma iorubá carrega cultura e memória porque vive em palavras, '
                            'sons, cantigas, nomes, saudações, histórias e práticas que atravessam '
                            'gerações. Aprender iorubá é mais do que traduzir expressões: é construir '
                            'uma relação mais consciente com aquilo que se escuta, canta, reza e '
                            'honra.</p>',
                            '<p>Se você quer entender o que está por trás das palavras, comece por um '
                            'caminho que respeite a língua e a tradição. Na Vedium, você aprende '
                            'iorubá em aulas ao vivo, com profundidade cultural, acompanhamento real e '
                            'sem contrato de fidelidade. A retenção vem do resultado, não de '
                            'amarras.</p>',
                            '<p><strong>Fale agora com a Vedium sobre a próxima turma de Iorubá e dê o '
                            'primeiro passo para aprender com respeito: <a '
                            'href="/blog/alfabeto-ioruba">https://vediums.com/</a></strong></p>']}],
     'faqs': [{'q': 'O que é o idioma iorubá?',
               'a': 'O iorubá é uma língua ligada ao povo iorubá e a uma ampla tradição cultural da '
                    'África Ocidental e da diáspora. No Brasil, também aparece em contextos culturais, '
                    'religiosos, musicais e comunitários de matriz africana.'},
              {'q': 'Por que aprender iorubá ajuda a entender cantigas e rezas?',
               'a': 'Porque muitas cantigas, rezas, saudações e expressões preservam palavras e '
                    'sentidos de origem iorubá. Ao estudar a língua com contexto, o aluno deixa de '
                    'apenas repetir sons e começa a compreender significados e usos.'},
              {'q': 'Dá para aprender iorubá online?',
               'a': 'Sim. O ideal é aprender em aulas online ao vivo, porque o aluno pode praticar '
                    'pronúncia, tirar dúvidas e receber orientação em tempo real, em vez de depender '
                    'apenas de vídeos gravados ou listas de palavras.'},
              {'q': 'Preciso ter conhecimento prévio para começar?',
               'a': 'Não. Um bom curso de iorubá pode começar do básico, apresentando sons, saudações, '
                    'vocabulário inicial e contexto cultural. O mais importante é estudar com '
                    'respeito, constância e orientação adequada.'},
              {'q': 'A Vedium tem curso de iorubá ao vivo?',
               'a': 'Sim. A Vedium trabalha com aulas ao vivo e uma abordagem que une idioma e '
                    'cultura. Para saber sobre a próxima turma de Iorubá, acesse https://vediums.com/ '
                    'e fale com a equipe.'}],
     'cta_title': 'Quer aprender iorubá com pronúncia correta desde o início?',
     'cta_text': 'Aulas ao vivo, do zero ao avançado, com foco em tons e conversação real.',
     'cta_label': 'Conhecer o curso de Iorubá',
     'cta_url': '/curso-de-ioruba-online'},
    "plano-de-30-dias-para-comecar-ioruba-com-base-solida": {'title': 'Plano de 30 dias para começar iorubá com base sólida',
     'meta_description': 'Comece iorubá em 30 dias com base sólida, respeito cultural e prática ao '
                         'vivo. Veja um plano seguro para iniciar do jeito certo.',
     'h1': 'Plano de 30 dias para começar iorubá com base sólida',
     'date': '2026-07-03',
     'date_display': '3 de julho de 2026',
     'hero_image': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Estudo de iorubá na Vedium',
     'tag': 'Iorubá',
     'category': 'ioruba',
     'lead': 'Começar iorubá com base sólida exige três cuidados desde o primeiro dia: aprender a '
             'pronúncia com atenção aos tons, compreender que a língua carrega cultura e praticar com '
             'orientação para não transformar tradição em decoração. Em 30 dias, o objetivo não é '
             '“dominar” o iorubá, mas criar uma fundação respeitosa para reconhecer sons, saudações, '
             'palavras essenciais, estruturas simples e contextos de uso.',
     'sections': [{'heading': '',
                   'body': ['<p>Para muitas pessoas no Brasil e nas comunidades afro-diaspóricas, '
                            'aprender iorubá não é apenas estudar um idioma novo. É se aproximar de '
                            'memórias, cantigas, rezas, nomes, saudações e referências que atravessam '
                            'a história. Por isso, um plano de estudo responsável precisa unir língua '
                            'e cultura. Não basta decorar palavras soltas. É preciso entender o '
                            'sentido, o uso, o tom, o contexto e a forma correta de praticar.</p>',
                            '<p>Este guia apresenta um plano de 30 dias para quem quer começar iorubá '
                            'com seriedade. A proposta é simples: organizar o primeiro mês em etapas '
                            'possíveis, com exercícios práticos e espaço para aula ao vivo. A Vedium '
                            'trabalha justamente com essa visão: aulas de iorubá ao vivo, com '
                            'profundidade cultural, para que o aluno aprenda não só palavras, mas o '
                            'sentido por trás delas.</p>']},
                  {'heading': 'Por que um plano de 30 dias ajuda no começo do iorubá?',
                   'body': ['<p>Um plano de 30 dias ajuda porque evita o estudo solto e cria uma '
                            'sequência segura. No início, o maior risco é consumir vídeos, listas e '
                            'traduções sem saber o que vem antes, o que precisa de correção e o que '
                            'exige contexto cultural.</p>',
                            '<p>O iorubá é uma língua tonal. Isso significa que o tom usado na '
                            'pronúncia pode mudar o significado de uma palavra. Para quem fala '
                            'português, esse ponto costuma ser novo, porque estamos acostumados a '
                            'pensar mais em sílabas fortes, acentos gráficos e entonação de frase. No '
                            'iorubá, a atenção ao tom precisa começar cedo.</p>',
                            '<p>Além disso, muitas pessoas chegam ao iorubá motivadas por '
                            'ancestralidade, religiosidade, pesquisa cultural ou vontade de '
                            'compreender melhor cantigas e rezas. Esse interesse é legítimo, mas exige '
                            'cuidado. Aprender uma palavra sem entender seu uso pode gerar '
                            'interpretações erradas. Repetir expressões sagradas sem orientação pode '
                            'soar desrespeitoso em determinados contextos. Por isso, a base precisa '
                            'ser construída com calma.</p>',
                            '<p>Um bom plano inicial deve responder a quatro perguntas:</p>',
                            '<ul><li>O que devo aprender primeiro?</li><li>Como praticar pronúncia e '
                            'tons sem vícios?</li><li>Como respeitar o contexto cultural da '
                            'língua?</li><li>Quando buscar uma aula ao vivo para corrigir e '
                            'aprofundar?</li></ul>',
                            '<p>O plano de 30 dias funciona como uma porta de entrada. Ele não '
                            'substitui um curso de iorubá online bem estruturado, mas prepara o aluno '
                            'para chegar à aula com mais consciência, melhores perguntas e mais '
                            'segurança para praticar.</p>']},
                  {'heading': 'O que você deve saber antes de começar?',
                   'body': ['<p>Antes de começar, entenda que iorubá não é apenas vocabulário: é '
                            'língua, memória, cultura e forma de ver o mundo. Essa consciência muda a '
                            'postura do aluno desde o primeiro contato.</p>',
                            '<p>Para iniciar com respeito, considere estes princípios:</p>',
                            '<ul><li><strong>Não trate o iorubá como curiosidade exótica.</strong> A '
                            'língua tem história, povo, território, literatura, oralidade e presença '
                            'viva.</li><li><strong>Não reduza o idioma ao uso religioso.</strong> '
                            'Muitas pessoas buscam o iorubá por caminhos espirituais, mas a língua é '
                            'ampla e também está ligada à vida cotidiana, cultura, nomes, saudações, '
                            'músicas, histórias e relações sociais.</li><li><strong>Não confie apenas '
                            'em traduções isoladas.</strong> Uma palavra pode ter nuances que dependem '
                            'de tom, contexto e uso.</li><li><strong>Não tenha pressa para '
                            '“interpretar tudo”.</strong> Compreensão profunda vem com estudo, escuta, '
                            'repetição e orientação.</li><li><strong>Valorize professores e fontes '
                            'qualificadas.</strong> Aprender ao vivo com quem domina a língua e a '
                            'cultura reduz erros e aprofunda a experiência.</li></ul>',
                            '<p>Essa postura é especialmente importante para quem deseja compreender '
                            'cantigas, rezas e saudações com seriedade. O respeito não aparece apenas '
                            'no tema estudado, mas no modo de estudar.</p>',
                            '<p>CTA: Se você quer aprender iorubá com orientação e cuidado cultural, '
                            'conheça as aulas ao vivo da Vedium em <a '
                            'href="/curso-de-ioruba-online">https://vediums.com/</a> e fale sobre a '
                            'próxima turma de Iorubá.</p>']},
                  {'heading': 'Semana 1: sons, tons e postura de aprendizado',
                   'body': ['<p>A primeira semana deve formar o ouvido. O objetivo é reconhecer que o '
                            'iorubá tem sons e tons que precisam ser escutados antes de serem '
                            'repetidos com confiança.</p>',
                            '<p>Nos primeiros sete dias, não tente memorizar muitas palavras. Foque em '
                            'escuta, repetição cuidadosa e consciência fonética. Para um iniciante, '
                            'falar pouco e ouvir bem pode ser mais produtivo do que decorar listas '
                            'longas.</p>',
                            '<h3>Dia 1: defina seu motivo e sua postura</h3>',
                            '<p>Escreva por que você quer aprender iorubá. Pode ser ancestralidade, '
                            'pesquisa, vivência cultural, compreensão de cantigas, conexão com a '
                            'tradição ou interesse linguístico. Depois, escreva também como deseja '
                            'estudar: com respeito, paciência e abertura para correção.</p>',
                            '<p>Esse exercício parece simples, mas cria intenção. Quem aprende iorubá '
                            'por memória e identidade precisa se lembrar de que cada palavra merece '
                            'cuidado.</p>',
                            '<h3>Dia 2: entenda o que é uma língua tonal</h3>',
                            '<p>Pesquise o conceito de língua tonal e observe exemplos guiados por '
                            'professor ou material confiável. O ponto principal é entender que o tom '
                            'não é detalhe decorativo: ele participa do significado.</p>',
                            '<p>Evite sair repetindo palavras sem ouvir várias vezes. No iorubá, a '
                            'repetição sem escuta pode fixar pronúncias erradas.</p>',
                            '<h3>Dia 3: observe vogais e sons diferentes do português</h3>',
                            '<p>Dedique o dia a perceber sons que não aparecem do mesmo modo no '
                            'português brasileiro. Alguns sinais gráficos usados no iorubá indicam '
                            'sons específicos. O iniciante não precisa dominar todos de uma vez, mas '
                            'deve entender que grafia, som e tom caminham juntos.</p>',
                            '<h3>Dia 4: escute saudações básicas</h3>',
                            '<p>Comece por saudações, porque elas conectam idioma e relação social. '
                            'Saudar é mais do que dizer “oi”. Em muitas culturas, saudação carrega '
                            'respeito, reconhecimento e contexto.</p>',
                            '<p>Anote três saudações, escute a pronúncia e repita devagar. Se '
                            'possível, grave sua voz e compare com a referência.</p>',
                            '<h3>Dia 5: pratique repetição consciente</h3>',
                            '<p>Escolha cinco palavras ou expressões da semana. Repita cada uma em voz '
                            'alta, devagar, com atenção ao som. Não acelere. A fluência começa com '
                            'precisão.</p>',
                            '<h3>Dia 6: escreva o que você já percebeu</h3>',
                            '<p>Registre quais sons parecem mais difíceis, quais expressões chamaram '
                            'sua atenção e quais dúvidas apareceram. Essas dúvidas serão valiosas em '
                            'uma aula ao vivo.</p>',
                            '<h3>Dia 7: revisão leve</h3>',
                            '<p>Revise tudo sem buscar quantidade. A meta da primeira semana é '
                            'simples: perceber que o iorubá tem lógica própria e merece escuta '
                            'atenta.</p>']},
                  {'heading': 'Semana 2: saudações, identidade e vocabulário essencial',
                   'body': ['<p>A segunda semana deve transformar escuta em vocabulário inicial. O '
                            'foco é aprender palavras e expressões que criam base para reconhecer '
                            'pessoas, cumprimentar, agradecer e se localizar no idioma.</p>',
                            '<p>Aqui, a ideia não é montar frases complexas. É começar a criar '
                            'familiaridade com expressões que aparecem em interações reais e em '
                            'contextos culturais.</p>',
                            '<h3>Dia 8: saudações do cotidiano</h3>',
                            '<p>Reforce saudações e expressões simples. Em um curso de iorubá online '
                            'com aula ao vivo, esse é um bom momento para praticar pronúncia com '
                            'correção.</p>',
                            '<p>Exercício: escolha três saudações e pratique em três ritmos:</p>',
                            '<ul><li>bem devagar;</li><li>em ritmo natural;</li><li>em resposta a uma '
                            'situação simulada.</li></ul>',
                            '<h3>Dia 9: formas de respeito</h3>',
                            '<p>Aprenda como a língua expressa respeito em interações. Muitas línguas '
                            'marcam formalidade, idade, posição social ou relação entre pessoas. O '
                            'importante aqui é perceber que idioma e comportamento caminham '
                            'juntos.</p>',
                            '<p>Não tente simplificar tudo para uma tradução direta em português. '
                            'Pergunte: “Em que situação isso é usado?” Essa pergunta é mais importante '
                            'do que “O que significa literalmente?”</p>',
                            '<h3>Dia 10: nomes, identidade e pertencimento</h3>',
                            '<p>Estude a relação entre língua e nomes. Muitos alunos se interessam '
                            'pelo iorubá por causa de nomes, termos ancestrais e significados. Esse '
                            'estudo deve ser feito com cautela, porque nomes podem carregar histórias, '
                            'valores e interpretações profundas.</p>',
                            '<p>Exercício: pesquise um nome ou termo com orientação confiável e '
                            'anote:</p>',
                            '<ul><li>pronúncia;</li><li>possível significado;</li><li>contexto de '
                            'uso;</li><li>dúvidas sobre interpretação.</li></ul>',
                            '<h3>Dia 11: vocabulário de pessoas e relações</h3>',
                            '<p>Aprenda palavras ligadas a pessoa, comunidade, família, professor, '
                            'aluno e grupo. Esse tipo de vocabulário ajuda a construir frases simples '
                            'depois.</p>',
                            '<h3>Dia 12: agradecimento e resposta</h3>',
                            '<p>Estude formas de agradecer e responder de maneira adequada. '
                            'Agradecimento é um ótimo tema para iniciantes, porque une comunicação '
                            'prática e sensibilidade cultural.</p>',
                            '<h3>Dia 13: revisão com voz</h3>',
                            '<p>Leia em voz alta tudo que aprendeu na semana. Grave um áudio curto com '
                            'suas saudações e expressões. Não se preocupe em soar perfeito. O objetivo '
                            'é perceber evolução e identificar pontos para corrigir.</p>',
                            '<h3>Dia 14: prepare perguntas para aula</h3>',
                            '<p>Liste cinco dúvidas para levar a uma aula ao vivo. Exemplos:</p>',
                            '<ul><li>Estou pronunciando corretamente?</li><li>Esse termo é usado em '
                            'qual contexto?</li><li>Essa expressão é cotidiana, cultural ou '
                            'ritual?</li><li>Qual erro comum devo evitar?</li><li>O que devo estudar '
                            'antes de avançar?</li></ul>']},
                  {'heading': 'Semana 3: frases simples e contexto cultural',
                   'body': ['<p>A terceira semana deve unir vocabulário a frases curtas. O objetivo é '
                            'começar a usar o idioma, ainda de forma básica, sem perder o cuidado com '
                            'o contexto.</p>',
                            '<p>Frases simples ajudam o aluno a sair da memorização passiva. Mas, no '
                            'iorubá, a construção precisa ser orientada. Não basta traduzir palavra '
                            'por palavra do português.</p>',
                            '<h3>Dia 15: construa frases com orientação</h3>',
                            '<p>Escolha expressões básicas e aprenda como formar frases simples. Evite '
                            'criar frases complexas sozinho se ainda não conhece a estrutura. Comece '
                            'por modelos seguros.</p>',
                            '<p>Exercício: pegue uma frase modelo validada por professor e substitua '
                            'apenas uma parte, mantendo a estrutura.</p>',
                            '<h3>Dia 16: pratique perguntas simples</h3>',
                            '<p>Aprenda perguntas básicas, especialmente aquelas úteis em aula:</p>',
                            '<ul><li>Como se diz isso?</li><li>O que significa?</li><li>Pode '
                            'repetir?</li><li>Qual é o tom?</li><li>Em que contexto se usa?</li></ul>',
                            '<p>Mesmo que você ainda não saiba formular tudo em iorubá, entender essas '
                            'necessidades ajuda a direcionar o estudo.</p>',
                            '<h3>Dia 17: estude uma cantiga com cuidado</h3>',
                            '<p>Se seu interesse envolve cantigas, escolha apenas um pequeno trecho e '
                            'não tente interpretar sozinho. Anote palavras que reconhece, dúvidas de '
                            'pronúncia e possíveis significados. Depois, leve para orientação.</p>',
                            '<p>O objetivo não é “traduzir uma cantiga inteira” em um dia. É aprender '
                            'a respeitar o caminho de interpretação.</p>',
                            '<h3>Dia 18: diferencie uso cotidiano e uso sagrado</h3>',
                            '<p>Nem toda palavra tem o mesmo peso em todos os contextos. Algumas '
                            'expressões podem aparecer em ambientes religiosos, culturais, históricos '
                            'ou cotidianos. O aluno precisa aprender a perguntar antes de usar.</p>',
                            '<p>Perguntas úteis:</p>',
                            '<ul><li>Essa expressão pode ser usada em conversa comum?</li><li>Existe '
                            'contexto em que não devo repetir?</li><li>A pronúncia muda o '
                            'sentido?</li><li>Há uma forma mais respeitosa de falar?</li></ul>',
                            '<h3>Dia 19: escuta ativa</h3>',
                            '<p>Ouça um material curto e tente identificar sons, pausas e repetições. '
                            'Não foque apenas no significado. O ouvido precisa aprender o ritmo da '
                            'língua.</p>',
                            '<h3>Dia 20: miniapresentação</h3>',
                            '<p>Crie uma apresentação simples com o que já sabe, mesmo que parte '
                            'esteja em português. Por exemplo:</p>',
                            '<p>“Estou começando a estudar iorubá. Quero aprender com respeito. Esta '
                            'semana pratiquei saudações, sons e algumas expressões.”</p>',
                            '<p>Depois, marque quais partes você gostaria de aprender em iorubá com um '
                            'professor.</p>',
                            '<h3>Dia 21: revisão da semana</h3>',
                            '<p>Revise frases, perguntas e vocabulário. Identifique o que já está mais '
                            'natural e o que ainda parece confuso.</p>']},
                  {'heading': 'Semana 4: prática ao vivo, correção e continuidade',
                   'body': ['<p>A quarta semana deve consolidar a base e abrir o caminho para '
                            'continuidade. Agora, o mais importante é não deixar o estudo virar uma '
                            'coleção de anotações. É hora de praticar com alguém que corrija, explique '
                            'e contextualize.</p>',
                            '<h3>Dia 22: faça uma revisão geral</h3>',
                            '<p>Volte aos dias 1 a 21 e selecione:</p>',
                            '<ul><li>10 palavras importantes;</li><li>5 expressões úteis;</li><li>3 '
                            'dúvidas de pronúncia;</li><li>2 temas culturais que quer entender '
                            'melhor;</li><li>1 objetivo para os próximos 30 dias.</li></ul>',
                            '<p>Esse resumo mostra que você não está começando do zero. Você já tem '
                            'uma base inicial.</p>',
                            '<h3>Dia 23: organize seu glossário prático</h3>',
                            '<p>Crie um glossário pessoal com quatro colunas:</p>',
                            '<table class="vd-table"><thead><tr><th>Palavra ou '
                            'expressão</th><th>Pronúncia / tom</th><th>Significado '
                            'aproximado</th><th>Contexto de '
                            'uso</th></tr></thead><tbody></tbody></table>',
                            '<p>Esse formato evita o erro comum de anotar apenas “palavra = tradução”. '
                            'No iorubá, o contexto importa muito.</p>',
                            '<h3>Dia 24: pratique com repetição espaçada</h3>',
                            '<p>Revise palavras dos dias anteriores sem olhar as respostas. Tente '
                            'lembrar primeiro, depois confira. Esse método fortalece a memória e '
                            'revela o que ainda precisa de atenção.</p>',
                            '<h3>Dia 25: simule uma aula ao vivo</h3>',
                            '<p>Prepare-se como se fosse participar de uma aula. Tenha caderno, '
                            'dúvidas, áudio gravado e objetivos claros. Em uma aula de iorubá ao vivo, '
                            'você aproveita melhor quando chega com perguntas específicas.</p>',
                            '<h3>Dia 26: peça correção de pronúncia</h3>',
                            '<p>A pronúncia é uma das partes mais importantes no começo. Peça correção '
                            'para tons, sons e ritmo. Não encare correção como crítica. Correção é '
                            'cuidado com a língua.</p>',
                            '<h3>Dia 27: aprenda com uma situação real</h3>',
                            '<p>Escolha uma situação: cumprimentar alguém, agradecer, perguntar o '
                            'significado de uma palavra, apresentar seu motivo de estudo ou comentar '
                            'uma cantiga. Trabalhe essa situação com frases simples.</p>',
                            '<h3>Dia 28: defina seu próximo nível de estudo</h3>',
                            '<p>Depois de 30 dias, você precisa escolher continuidade. Pode ser entrar '
                            'em uma turma, manter aulas semanais, aprofundar pronúncia ou estudar '
                            'temas culturais específicos.</p>',
                            '<h3>Dia 29: revise sua motivação inicial</h3>',
                            '<p>Volte ao texto que escreveu no primeiro dia. O que mudou? Você está '
                            'mais consciente? Tem novas dúvidas? Entendeu que aprender iorubá exige '
                            'paciência e respeito?</p>',
                            '<h3>Dia 30: transforme o começo em compromisso</h3>',
                            '<p>O último dia não é encerramento. É transição. Agora você sabe que o '
                            'iorubá precisa de escuta, prática, contexto e orientação. O próximo passo '
                            'natural é estudar ao vivo, com acompanhamento e profundidade.</p>',
                            '<p>CTA: Fale com a Vedium sobre a próxima turma de Iorubá em <a '
                            'href="/blog/alfabeto-ioruba">https://vediums.com/</a>. Aprenda ao vivo, '
                            'com respeito à cultura e sem depender de vídeos soltos.</p>']},
                  {'heading': 'Exercício para aula ao vivo: seu primeiro mapa de estudo',
                   'body': ['<p>Antes de entrar em uma aula, prepare um mapa simples. Ele ajuda o '
                            'professor a entender sua jornada e torna a aula mais produtiva.</p>',
                            '<p>Preencha:</p>',
                            '<ol><li><strong>Meu motivo para aprender iorubá:</strong>  '
                            '</li><li><strong>O que já tentei estudar:</strong>  </li><li><strong>Três '
                            'palavras ou expressões que quero entender melhor:</strong>  '
                            '</li><li><strong>Minha maior dificuldade até agora:</strong>  '
                            '</li><li><strong>Um tema cultural que quero aprender com '
                            'respeito:</strong>  </li><li><strong>Uma cantiga, saudação ou contexto '
                            'que quero compreender melhor:</strong>  </li><li><strong>Meu objetivo '
                            'para os próximos 30 dias:</strong>  </li></ol>',
                            '<p>Esse exercício é especialmente útil para quem chega com uma relação '
                            'afetiva, ancestral ou religiosa com o idioma. Ele organiza a intenção e '
                            'evita um estudo apressado.</p>']},
                  {'heading': 'Como praticar iorubá com respeito?',
                   'body': ['<p>Praticar com respeito significa reconhecer que a língua tem donos, '
                            'história e contextos. Você pode e deve estudar, mas precisa fazer isso '
                            'com humildade, cuidado e disposição para aprender com quem sabe.</p>',
                            '<p>Algumas atitudes importantes:</p>',
                            '<ul><li>ouvir antes de repetir;</li><li>perguntar antes de usar '
                            'expressões sensíveis;</li><li>evitar “traduções definitivas” sem fonte '
                            'confiável;</li><li>respeitar variações e contextos;</li><li>não usar '
                            'termos culturais como enfeite;</li><li>valorizar professores, '
                            'pesquisadores e comunidades;</li><li>aceitar correção como parte do '
                            'processo.</li></ul>',
                            '<p>A Vedium defende essa abordagem porque “fluência além das palavras” '
                            'significa exatamente isso: aprender a língua junto com a inteligência '
                            'cultural que ela carrega. No caso do iorubá, essa profundidade não é '
                            'detalhe. É o centro do aprendizado.</p>']},
                  {'heading': 'Curso de iorubá online: quando vale começar com aula ao vivo?',
                   'body': ['<p>Vale começar com aula ao vivo quando você quer evitar vícios de '
                            'pronúncia, entender tons, tirar dúvidas culturais e praticar com '
                            'orientação. O autodidatismo pode ajudar na curiosidade inicial, mas o '
                            'acompanhamento é essencial para construir base sólida.</p>',
                            '<p>Um curso de iorubá online ao vivo é especialmente indicado se '
                            'você:</p>',
                            '<ul><li>quer entender cantigas e rezas com seriedade;</li><li>já tentou '
                            'aprender por vídeos soltos e ficou confuso;</li><li>tem medo de '
                            'pronunciar errado;</li><li>quer saber o contexto por trás das '
                            'palavras;</li><li>busca um caminho estruturado;</li><li>deseja aprender '
                            'com respeito à cultura iorubá;</li><li>precisa de constância para '
                            'continuar estudando.</li></ul>',
                            '<p>A grande diferença da aula ao vivo é a interação. Você fala, escuta, '
                            'pergunta, erra, corrige e entende. O professor percebe suas dificuldades '
                            'e ajusta a explicação. Isso não acontece do mesmo jeito em conteúdo '
                            'gravado.</p>',
                            '<p>Na Vedium, não há contrato de fidelidade. A proposta é que você '
                            'continue porque sente que está evoluindo, não porque está preso. Para '
                            'quem está começando iorubá, essa liberdade combina com um aprendizado '
                            'mais consciente: você entra, experimenta, sente a aula e decide continuar '
                            'pelo valor real da experiência.</p>']},
                  {'heading': 'Conclusão com CTA forte',
                   'body': ['<p>Um plano de 30 dias para começar iorubá com base sólida não promete '
                            'fluência imediata. Ele oferece algo mais importante: um início correto, '
                            'respeitoso e consciente. Em um mês, você pode formar o ouvido, entender a '
                            'importância dos tons, aprender saudações, criar um glossário prático, '
                            'reconhecer contextos culturais e chegar mais preparado para uma aula ao '
                            'vivo.</p>',
                            '<p>Aprender iorubá é mais do que acumular palavras. É se aproximar de uma '
                            'língua viva, profunda e carregada de memória. Por isso, o caminho precisa '
                            'unir estudo, escuta, cultura e orientação.</p>',
                            '<p>Se você quer começar com respeito, fale com a Vedium sobre a próxima '
                            'turma de Iorubá. As aulas são ao vivo, com profundidade cultural e sem '
                            'fidelidade. Você aprende no seu ritmo e continua porque percebe o valor '
                            'do caminho.</p>',
                            '<p>Acesse <a href="/curso-de-ioruba-online">https://vediums.com/</a> e dê '
                            'o primeiro passo para aprender iorubá além das palavras.</p>']}],
     'faqs': [{'q': 'É possível aprender iorubá em 30 dias?',
               'a': 'Em 30 dias, você não fica fluente, mas pode construir uma base inicial sólida. O '
                    'ideal é aprender sons, tons, saudações, vocabulário essencial e contexto cultural '
                    'para continuar com mais segurança.'},
              {'q': 'Qual é o maior erro de quem começa a estudar iorubá?',
               'a': 'O maior erro é decorar palavras soltas sem aprender pronúncia, tom e contexto de '
                    'uso. No iorubá, som e sentido caminham juntos, e a orientação correta evita '
                    'interpretações rasas.'},
              {'q': 'Preciso ter vínculo religioso para aprender iorubá?',
               'a': 'Não. Muitas pessoas estudam por ancestralidade, cultura, pesquisa, identidade, '
                    'música, história ou interesse linguístico. O importante é estudar com respeito e '
                    'compreender os contextos da língua.'},
              {'q': 'Curso de iorubá online funciona?',
               'a': 'Funciona quando há aula ao vivo, prática real, correção de pronúncia e explicação '
                    'cultural. Vídeos gravados podem ajudar, mas não substituem a interação com '
                    'professor qualificado.'},
              {'q': 'A Vedium oferece aulas de iorubá ao vivo?',
               'a': 'Sim. A Vedium oferece aulas de iorubá ao vivo, com foco em língua, cultura e '
                    'respeito à tradição. Não há contrato de fidelidade: você continua porque vê valor '
                    'e evolução no aprendizado.'}],
     'cta_title': 'Quer aprender iorubá com pronúncia correta desde o início?',
     'cta_text': 'Aulas ao vivo, do zero ao avançado, com foco em tons e conversação real.',
     'cta_label': 'Conhecer o curso de Iorubá',
     'cta_url': '/curso-de-ioruba-online'},
    "primeiras-saudacoes-em-ioruba-para-aprender-com-respeito": {'title': 'Primeiras saudações em iorubá para aprender com respeito',
     'meta_description': 'Aprenda saudações básicas em iorubá com contexto, pronúncia e respeito '
                         'cultural. Veja como praticar em aulas ao vivo na Vedium.',
     'h1': 'Primeiras saudações em iorubá para aprender com respeito',
     'date': '2025-01-17',
     'date_display': '17 de janeiro de 2025',
     'hero_image': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Estudo de iorubá na Vedium',
     'tag': 'Iorubá',
     'category': 'ioruba',
     'lead': 'Aprender as primeiras saudações em iorubá é um passo simples, mas profundamente '
             'simbólico. Antes de decorar palavras, é importante entender que cada cumprimento carrega '
             'relação, escuta, presença e contexto cultural. Para quem busca o iorubá por '
             'ancestralidade, tradição, pesquisa, religiosidade afro-brasileira ou interesse cultural, '
             'começar pelas saudações é uma forma respeitosa de entrar na língua sem tratá-la como '
             'curiosidade solta.',
     'sections': [{'heading': '',
                   'body': ['<p>Na <a href="/blog/alfabeto-ioruba">Vedium</a>, o iorubá é ensinado ao '
                            'vivo porque a língua não vive apenas no papel. Ela aparece no som, no '
                            'tom, na repetição, na escuta e na correção feita por quem compreende a '
                            'língua e a cultura. Por isso, este artigo não é uma lista “pronta para '
                            'sair falando sem contexto”. É um guia inicial para você entender como '
                            'cumprimentar, o que observar e por que a prática acompanhada faz '
                            'diferença.</p>']},
                  {'heading': 'Por que começar pelas saudações em iorubá?',
                   'body': ['<p>Começar pelas saudações é começar pela relação. Em muitas culturas, '
                            'cumprimentar não é apenas dizer “oi”; é reconhecer a presença da outra '
                            'pessoa, demonstrar consideração e abrir uma conversa com cuidado.</p>',
                            '<p>No aprendizado de iorubá, as saudações ajudam você a praticar três '
                            'pontos essenciais desde o início:</p>',
                            '<ul><li>escuta dos sons;</li><li>atenção aos tons;</li><li>compreensão do '
                            'contexto social e cultural.</li></ul>',
                            '<p>Isso é especialmente importante porque o iorubá é uma língua tonal. Em '
                            'línguas tonais, a maneira como a sílaba é entoada pode alterar o sentido '
                            'da palavra. Ou seja: não basta olhar a palavra escrita e tentar adivinhar '
                            'a pronúncia. O ouvido precisa ser treinado.</p>',
                            '<p>Quando uma pessoa aprende uma saudação sem escutar corretamente, pode '
                            'até memorizar a sequência de letras, mas não necessariamente aprende a '
                            'língua. Por isso, aulas ao vivo fazem diferença: o professor corrige a '
                            'pronúncia, explica a situação de uso e mostra como a palavra se comporta '
                            'na fala real.</p>',
                            '<p>Na Vedium, a proposta é exatamente essa: aprender iorubá com respeito, '
                            'profundidade e prática real, não apenas repetir termos '
                            'desconectados.</p>']},
                  {'heading': 'O que você precisa saber antes de repetir palavras em iorubá?',
                   'body': ['<p>Você precisa saber que uma saudação em iorubá envolve som, tom, '
                            'intenção e contexto. Repetir sem entender pode esvaziar o sentido da '
                            'palavra ou gerar uso inadequado.</p>',
                            '<p>Antes de decorar qualquer cumprimento, observe quatro cuidados:</p>',
                            '<h3>1. O iorubá tem marcas que orientam a pronúncia</h3>',
                            '<p>Na escrita, você pode encontrar acentos e sinais que indicam tons ou '
                            'sons específicos. Eles não são enfeites. Eles ajudam a guiar a leitura e '
                            'a pronúncia. Ignorar essas marcas pode mudar completamente a forma como a '
                            'palavra soa.</p>',
                            '<p>Por isso, ao estudar, procure materiais que preservem a escrita '
                            'correta sempre que possível e, principalmente, escute a pronúncia com '
                            'orientação. Em uma aula ao vivo, esse ponto deixa de ser abstrato: você '
                            'fala, escuta, ajusta e repete.</p>',
                            '<h3>2. Algumas palavras circulam em contextos religiosos e culturais</h3>',
                            '<p>Para muitas pessoas no Brasil, o contato com o iorubá acontece por '
                            'cantigas, rezas, saudações tradicionais, nomes, termos de terreiro ou '
                            'referências afro-diaspóricas. Isso exige responsabilidade.</p>',
                            '<p>Nem toda palavra deve ser tratada como frase de efeito. Algumas '
                            'expressões têm peso cultural, histórico, espiritual ou comunitário. '
                            'Aprender com respeito é perguntar: “em que contexto isso é usado?”, “quem '
                            'usa?”, “quando se usa?” e “o que essa palavra realmente quer dizer?”.</p>',
                            '<h3>3. Traduções literais nem sempre explicam o sentido</h3>',
                            '<p>Uma saudação pode ser traduzida como “bom dia” ou “como vai?”, mas o '
                            'sentido cultural pode ser mais amplo. Em muitos casos, o cumprimento '
                            'expressa cuidado, reconhecimento, desejo de bem-estar ou respeito pela '
                            'pessoa cumprimentada.</p>',
                            '<p>Por isso, o ideal é não estudar apenas equivalências. Estude '
                            'situações.</p>',
                            '<h3>4. Aprender ao vivo evita vícios de pronúncia</h3>',
                            '<p>Vídeos, listas e posts ajudam no primeiro contato, mas não substituem '
                            'a prática com retorno. Quando você aprende sozinho, pode repetir por '
                            'semanas uma pronúncia imprecisa sem perceber. Em uma aula ao vivo, o '
                            'professor identifica o ajuste necessário na hora.</p>',
                            '<p>É por isso que um curso de iorubá online ao vivo pode ser mais seguro '
                            'para quem busca aprendizado sério: você mantém a flexibilidade do online '
                            'sem abrir mão da presença humana.</p>']},
                  {'heading': 'Primeiras saudações em iorubá: um glossário inicial',
                   'body': ['<p>A seguir, você verá saudações e expressões básicas para começar. Elas '
                            'devem ser estudadas com escuta e orientação, especialmente por causa dos '
                            'tons. Use este glossário como porta de entrada, não como substituto de '
                            'uma aula.</p>',
                            '<h3>Ẹ n lẹ́ — saudação geral</h3>',
                            '<p><strong>Sentido aproximado:</strong> olá; cumprimento geral.</p>',
                            '<p>Esta é uma forma de saudação usada para iniciar contato de maneira '
                            'respeitosa. Para quem está começando, ela ajuda a treinar o som de “Ẹ”, '
                            'que não deve ser tratado como uma letra qualquer do português. A '
                            'pronúncia precisa ser escutada e praticada.</p>',
                            '<p><strong>Como praticar:</strong> repita devagar, prestando atenção à '
                            'abertura da vogal e ao ritmo da frase. Depois, treine em uma pequena '
                            'troca:</p>',
                            '<p>Pessoa A: Ẹ n lẹ́.<br>Pessoa B: Ẹ n lẹ́.</p>',
                            '<p>Em aula, o professor pode mostrar variações, uso mais natural e '
                            'diferenças de contexto.</p>',
                            '<h3>Ẹ káàárọ̀ — bom dia</h3>',
                            '<p><strong>Sentido aproximado:</strong> bom dia.</p>',
                            '<p>Essa é uma saudação importante para o início do dia. Ela mostra como '
                            'uma expressão aparentemente simples pode exigir cuidado com tons e vogais '
                            'longas. A escrita com acentos ajuda, mas a escuta é essencial.</p>',
                            '<p><strong>Como praticar:</strong> não transforme a palavra em uma '
                            'pronúncia “aportuguesada”. Escute, repita e peça correção. O objetivo não '
                            'é falar rápido; é falar com consciência.</p>',
                            '<h3>Ẹ káàsán — boa tarde</h3>',
                            '<p><strong>Sentido aproximado:</strong> boa tarde.</p>',
                            '<p>É uma saudação usada no período da tarde. Para quem está começando, '
                            'ela é útil para perceber como as saudações de tempo podem ter estruturas '
                            'semelhantes, mas sons diferentes.</p>',
                            '<p><strong>Como praticar:</strong> compare com “Ẹ káàárọ̀” e observe onde '
                            'a boca muda, onde o som se alonga e onde o tom se altera.</p>',
                            '<h3>Ẹ káalẹ́ — boa noite / boa tarde-noite</h3>',
                            '<p><strong>Sentido aproximado:</strong> boa noite ou cumprimento no fim '
                            'do dia, conforme contexto.</p>',
                            '<p>Essa expressão pode aparecer associada ao período da noite ou ao fim '
                            'do dia. Como ocorre em qualquer língua, o uso exato pode depender de '
                            'contexto, região e orientação de quem ensina. Por isso, vale aprender a '
                            'expressão dentro de situações reais, não isoladamente.</p>',
                            '<p><strong>Como praticar:</strong> imagine uma chegada a uma aula no '
                            'período da noite. Você cumprimenta o professor e a turma com calma, '
                            'ouvindo a resposta e repetindo.</p>',
                            '<h3>Báwo ni? — como vai?</h3>',
                            '<p><strong>Sentido aproximado:</strong> como você está? / como vai?</p>',
                            '<p>Esta é uma expressão prática para iniciar uma conversa simples. Ela '
                            'aproxima o aprendizado da vida real porque permite sair da saudação única '
                            'e entrar em uma pequena interação.</p>',
                            '<p>Uma resposta inicial possível, em contexto básico de aula, é:</p>',
                            '<p><strong>Mo wà dáadáa</strong> — estou bem.</p>',
                            '<p>Aqui também é importante não estudar apenas por equivalência. A frase '
                            'precisa ser repetida com atenção à pronúncia.</p>',
                            '<h3>Ẹ ṣé — obrigado(a)</h3>',
                            '<p><strong>Sentido aproximado:</strong> obrigado(a).</p>',
                            '<p>Expressar agradecimento é parte fundamental de qualquer aprendizado '
                            'linguístico. “Ẹ ṣé” é uma expressão curta, mas exige atenção ao som '
                            'representado por “ṣ”, que não deve ser confundido automaticamente com o '
                            '“s” comum do português.</p>',
                            '<p><strong>Como praticar:</strong> use após uma correção em aula, depois '
                            'de receber uma explicação ou ao encerrar uma interação simples.</p>',
                            '<h3>Ó dáàbọ̀ — adeus / até logo</h3>',
                            '<p><strong>Sentido aproximado:</strong> adeus; até logo.</p>',
                            '<p>Essa expressão pode aparecer em despedidas. Para o iniciante, ela '
                            'ajuda a formar uma sequência mínima de conversação: cumprimentar, '
                            'perguntar como a pessoa está, agradecer e se despedir.</p>',
                            '<p>Um pequeno diálogo didático ficaria assim:</p>',
                            '<p>Pessoa A: Ẹ n lẹ́.<br>Pessoa B: Ẹ n lẹ́.<br>Pessoa A: Báwo '
                            'ni?<br>Pessoa B: Mo wà dáadáa. Ẹ ṣé.<br>Pessoa A: Ó dáàbọ̀.</p>',
                            '<p>Esse tipo de exercício é simples, mas muito útil. Ele transforma '
                            'palavras soltas em prática comunicativa.</p>']},
                  {'heading': 'Como praticar saudações em iorubá sem perder o respeito cultural?',
                   'body': ['<p>Pratique devagar, com escuta, orientação e consciência do contexto. '
                            'Respeito cultural não significa ter medo de aprender; significa aprender '
                            'sem superficialidade.</p>',
                            '<p>Aqui está um caminho prático para começar:</p>',
                            '<h3>Primeiro, escute antes de repetir</h3>',
                            '<p>Antes de sair pronunciando, escute várias vezes. Tente perceber o '
                            'ritmo da frase. Em iorubá, a musicalidade da língua importa. Quando você '
                            'escuta com atenção, começa a notar detalhes que a escrita não revela '
                            'completamente.</p>',
                            '<h3>Depois, repita em voz alta</h3>',
                            '<p>Repetir mentalmente não basta. A língua precisa passar pela boca. Fale '
                            'devagar, grave sua voz se possível e compare com a pronúncia de '
                            'referência. Mas lembre-se: a comparação sozinho tem limite. A correção de '
                            'um professor acelera muito o processo.</p>',
                            '<h3>Em seguida, use em microdiálogos</h3>',
                            '<p>Não memorize apenas listas. Crie pequenas situações:</p>',
                            '<ul><li>cumprimentar ao chegar;</li><li>perguntar como alguém '
                            'está;</li><li>agradecer;</li><li>se despedir.</li></ul>',
                            '<p>Isso gera confiança e evita que o aprendizado fique mecânico.</p>',
                            '<h3>Por fim, pergunte sobre o contexto</h3>',
                            '<p>Sempre que aprender uma saudação, pergunte: essa expressão é formal? É '
                            'cotidiana? É usada com mais velhos? É adequada em contexto religioso? Tem '
                            'variações? Existe uma forma mais respeitosa?</p>',
                            '<p>Esse tipo de pergunta mostra maturidade no aprendizado.</p>']},
                  {'heading': 'Por que aulas ao vivo são melhores para aprender saudações em iorubá?',
                   'body': ['<p>Aulas ao vivo permitem correção imediata, prática oral e explicação '
                            'cultural no momento em que a dúvida aparece. Para uma língua tonal e '
                            'culturalmente profunda como o iorubá, isso faz grande diferença.</p>',
                            '<p>Um curso gravado pode mostrar uma lista de cumprimentos. Uma aula ao '
                            'vivo mostra como você está pronunciando, onde precisa ajustar e por que '
                            'determinada expressão deve ser usada com cuidado.</p>',
                            '<p>Na Vedium, o diferencial está em unir três elementos:</p>',
                            '<ul><li><strong>língua:</strong> vocabulário, pronúncia, estrutura e '
                            'prática;</li><li><strong>cultura:</strong> origem, uso, contexto e '
                            'respeito;</li><li><strong>presença:</strong> aula ao vivo, com professor '
                            'e interação real.</li></ul>',
                            '<p>Isso combina diretamente com quem busca mais do que “aprender '
                            'palavras”. Para a persona Adá, o objetivo não é apenas falar uma '
                            'saudação. É compreender o que se diz e honrar o caminho de onde aquela '
                            'palavra vem.</p>']},
                  {'heading': 'Exercício para sua primeira aula de iorubá ao vivo',
                   'body': ['<p>A melhor forma de começar é transformar as saudações em uma prática '
                            'curta. Veja um exercício simples para levar para sua primeira aula:</p>',
                            '<ol><li>Escolha três saudações deste artigo.</li><li>Copie cada uma com a '
                            'grafia completa.</li><li>Escute a pronúncia com o '
                            'professor.</li><li>Repita três vezes devagar.</li><li>Pergunte em que '
                            'situação cada expressão é usada.</li><li>Monte um diálogo curto com '
                            'saudação, pergunta, agradecimento e despedida.</li><li>Peça correção de '
                            'tom, ritmo e contexto.</li></ol>',
                            '<p>Esse exercício mostra que aprender iorubá não precisa começar de forma '
                            'pesada. Mas precisa começar com responsabilidade.</p>']},
                  {'heading': 'Como a Vedium ensina iorubá com profundidade cultural?',
                   'body': ['<p>A Vedium ensina iorubá em aulas online ao vivo, com foco em prática '
                            'real, escuta, pronúncia e contexto cultural. A proposta é que o aluno '
                            'avance com acompanhamento, sem depender apenas de vídeos soltos ou listas '
                            'desconectadas.</p>',
                            '<p>O aluno aprende no próprio ritmo, com a segurança de poder perguntar, '
                            'errar, repetir e entender. Isso é essencial para quem está começando do '
                            'zero e também para quem já tem contato com cantigas, rezas ou termos '
                            'culturais, mas quer compreender melhor o significado das palavras.</p>',
                            '<p>Outro ponto importante: a Vedium trabalha sem fidelidade. Você não '
                            'fica preso por contrato longo. A ideia é simples: você continua porque '
                            'percebe valor, acolhimento e evolução.</p>',
                            '<p>Para quem busca um curso de iorubá online, esse modelo reduz o medo de '
                            'começar e aumenta a chance de desenvolver constância. Afinal, aprender '
                            'uma língua não é decorar uma vez. É criar relação com ela.</p>']},
                  {'heading': 'Conclusão com CTA forte',
                   'body': ['<p>As primeiras saudações em iorubá são mais do que frases básicas. Elas '
                            'são uma entrada respeitosa em uma língua que carrega história, presença, '
                            'ancestralidade e cultura. Ao aprender expressões como <strong>Ẹ n '
                            'lẹ́</strong>, <strong>Ẹ káàárọ̀</strong>, <strong>Báwo ni?</strong>, '
                            '<strong>Ẹ ṣé</strong> e <strong>Ó dáàbọ̀</strong>, você começa a '
                            'construir uma base de escuta, pronúncia e consciência.</p>',
                            '<p>Mas o passo mais importante é não aprender sozinho de forma rasa. O '
                            'iorubá pede ouvido, prática e contexto. E é exatamente isso que uma aula '
                            'ao vivo oferece.</p>',
                            '<p>Se você quer aprender iorubá com profundidade cultural, respeito à '
                            'tradição e acompanhamento real, conheça a próxima turma da Vedium.</p>',
                            '<p><strong>Acesse <a '
                            'href="/curso-de-ioruba-online">https://vediums.com/</a> e fale com a '
                            'Vedium sobre a próxima turma de Iorubá.</strong><br>Aqui, você aprende ao '
                            'vivo, sem fidelidade, e continua porque sente que está evoluindo de '
                            'verdade.</p>']}],
     'faqs': [{'q': 'Quais são as primeiras saudações em iorubá para aprender?',
               'a': 'Algumas saudações iniciais são <strong>Ẹ n lẹ́</strong> (olá), <strong>Ẹ '
                    'káàárọ̀</strong> (bom dia), <strong>Ẹ káàsán</strong> (boa tarde), <strong>Ẹ '
                    'káalẹ́</strong> (boa noite), <strong>Báwo ni?</strong> (como vai?), <strong>Ẹ '
                    'ṣé</strong> (obrigado/a) e <strong>Ó dáàbọ̀</strong> (adeus/até logo).'},
              {'q': 'Posso aprender saudações em iorubá sozinho?',
               'a': 'Você pode começar sozinho com materiais introdutórios, mas o ideal é praticar com '
                    'orientação. Como o iorubá é tonal, a pronúncia e os tons precisam de escuta e '
                    'correção para evitar vícios.'},
              {'q': 'Por que aprender iorubá exige respeito cultural?',
               'a': 'Porque muitas palavras circulam em contextos culturais, religiosos e '
                    'afro-diaspóricos. Aprender com respeito significa entender o uso, o contexto e o '
                    'sentido por trás das expressões, não apenas repetir sons.'},
              {'q': 'Curso de iorubá online funciona?',
               'a': 'Funciona quando há aula ao vivo, prática oral e acompanhamento. O formato online '
                    'dá flexibilidade, mas a presença do professor é essencial para corrigir '
                    'pronúncia, explicar tons e contextualizar o vocabulário.'},
              {'q': 'A Vedium oferece aula de iorubá ao vivo?',
               'a': 'Sim. A Vedium oferece aulas online ao vivo, com foco em língua, cultura e prática '
                    'real. Não há contrato de fidelidade: o aluno continua porque percebe evolução, '
                    'acolhimento e profundidade no aprendizado.'}],
     'cta_title': 'Quer aprender iorubá com pronúncia correta desde o início?',
     'cta_text': 'Aulas ao vivo, do zero ao avançado, com foco em tons e conversação real.',
     'cta_label': 'Conhecer o curso de Iorubá',
     'cta_url': '/curso-de-ioruba-online'},
    "vocabulario-de-relacoes-sociais-em-ioruba-comunidade-e-respeito": {'title': 'Vocabulário de relações sociais em iorubá: comunidade e respeito',
     'meta_description': 'Aprenda vocabulário inicial de relações sociais em iorubá com foco em '
                         'comunidade, respeito, contexto cultural e prática ao vivo.',
     'h1': 'Vocabulário de relações sociais em iorubá: comunidade e respeito',
     'date': '2026-06-19',
     'date_display': '19 de junho de 2026',
     'hero_image': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Estudo de iorubá na Vedium',
     'tag': 'Iorubá',
     'category': 'ioruba',
     'lead': 'O vocabulário de relações sociais em iorubá importa porque a língua não organiza apenas '
             'palavras: ela expressa vínculos, idade, pertencimento, respeito, acolhimento e posição '
             'dentro da comunidade. Para quem está começando a aprender iorubá, estudar termos ligados '
             'a família, amizade, comunidade e reverência ajuda a compreender melhor como a língua se '
             'conecta à vida social e à cultura.',
     'sections': [{'heading': '',
                   'body': ['<p>Esse tema é especialmente importante para quem busca o iorubá por '
                            'ancestralidade, tradição, pesquisa, religiosidade, memória '
                            'afro-diaspórica ou interesse cultural. Muitas pessoas querem entender '
                            'cantigas, saudações, rezas, nomes e expressões que ouviram em '
                            'comunidades, terreiros, estudos ou vivências culturais. Mas, antes de '
                            'avançar para conteúdos mais complexos, é essencial construir uma base de '
                            'vocabulário social com cuidado.</p>',
                            '<p>No iorubá, não basta perguntar “qual é a tradução?” de uma palavra. É '
                            'preciso perguntar também: “em que contexto essa palavra aparece?”, “a '
                            'pronúncia muda o sentido?”, “há marca de respeito?”, “esse termo é '
                            'familiar, comunitário, religioso ou formal?”, “posso usar essa palavra em '
                            'qualquer situação?”. Essas perguntas protegem o aprendizado contra '
                            'simplificações e ajudam o aluno a se aproximar da língua com '
                            'responsabilidade.</p>',
                            '<p>Neste artigo, você verá vocabulário inicial de relações sociais em '
                            'iorubá, com foco em comunidade e respeito. Também encontrará orientações '
                            'para praticar sem superficialidade, um exercício para aula ao vivo e um '
                            'caminho para continuar aprendendo com profundidade cultural na '
                            'Vedium.</p>']},
                  {'heading': 'Por que relações sociais são um bom começo para aprender iorubá?',
                   'body': ['<p>Relações sociais são um bom começo porque apresentam palavras que '
                            'aparecem em encontros, saudações, família, comunidade, pertencimento e '
                            'convivência. Em vez de começar apenas por listas abstratas, o aluno entra '
                            'no idioma por uma porta humana: quem fala, com quem fala, como se dirige '
                            'ao outro e qual respeito está envolvido.</p>',
                            '<p>Aprender relações sociais também ajuda a evitar um erro comum: tratar '
                            'o iorubá como um vocabulário solto de termos “bonitos” ou “misteriosos”. '
                            'A língua vive nas relações. Ela aparece quando alguém saúda uma pessoa '
                            'mais velha, quando se reconhece um grupo, quando se fala de filhos, pais, '
                            'mães, amigos, comunidade ou responsabilidade.</p>',
                            '<p>Para quem está no início, esse vocabulário ajuda a criar três '
                            'bases:</p>',
                            '<ul><li><strong>Base linguística:</strong> reconhecimento de palavras '
                            'frequentes e estruturas simples.</li><li><strong>Base cultural:</strong> '
                            'percepção de que a língua expressa respeito e '
                            'pertencimento.</li><li><strong>Base prática:</strong> possibilidade de '
                            'usar palavras em exercícios de fala, escuta e memória.</li></ul>',
                            '<p>Também é um tema útil para aulas ao vivo, porque o professor pode '
                            'corrigir pronúncia, explicar tons, mostrar usos e alertar sobre sentidos '
                            'que não cabem em tradução literal. No iorubá, essa orientação é '
                            'decisiva.</p>',
                            '<p>CTA: Se você quer aprender iorubá com profundidade cultural e prática '
                            'ao vivo, fale com a Vedium sobre a próxima turma em <a '
                            'href="/curso-de-ioruba-online">https://vediums.com/</a>.</p>']},
                  {'heading': 'Antes do vocabulário: três cuidados essenciais',
                   'body': ['<p>Antes de decorar palavras, entenda três cuidados. Eles ajudam a '
                            'estudar iorubá com mais respeito e reduzem o risco de erro.</p>',
                            '<h3>1. A pronúncia e os tons importam</h3>',
                            '<p>O iorubá é uma língua tonal. Isso significa que a forma como a palavra '
                            'é pronunciada pode mudar o significado. Por isso, vocabulário escrito é '
                            'apenas uma parte do aprendizado. O aluno precisa ouvir, repetir, comparar '
                            'e ser corrigido.</p>',
                            '<p>Em um artigo, é possível apresentar palavras como ponto de partida, '
                            'mas o ideal é praticá-las em aula ao vivo, com atenção aos sinais '
                            'gráficos, sons e tons. Se você copiar apenas a escrita sem escutar a '
                            'pronúncia, pode criar um hábito difícil de ajustar depois.</p>',
                            '<h3>2. Traduções são aproximações</h3>',
                            '<p>Muitas palavras em iorubá não cabem perfeitamente em uma única palavra '
                            'em português. Em temas sociais e culturais, a tradução pode depender do '
                            'contexto. Uma palavra pode ter uso cotidiano, familiar, comunitário, '
                            'simbólico ou religioso.</p>',
                            '<p>Por isso, neste artigo, os significados devem ser lidos como '
                            'aproximações iniciais, não como definições absolutas. O próximo passo é '
                            'sempre estudar contexto e uso.</p>',
                            '<h3>3. Respeito também é método</h3>',
                            '<p>Estudar com respeito não significa ter medo da língua. Significa '
                            'aprender com humildade. Ouvir antes de repetir. Perguntar antes de '
                            'afirmar. Aceitar correção. Não usar termos culturais como enfeite. E '
                            'reconhecer que a língua iorubá carrega histórias, povos, memórias e '
                            'tradições.</p>',
                            '<p>Esse cuidado está no centro da proposta da Vedium: fluência além das '
                            'palavras.</p>']},
                  {'heading': 'Vocabulário inicial de família e parentesco',
                   'body': ['<p>O vocabulário de família é uma das primeiras portas para entender '
                            'relações sociais. Ele mostra como a língua organiza vínculos afetivos e '
                            'posições dentro do grupo.</p>',
                            '<table class="vd-table"><thead><tr><th>Iorubá</th><th>Significado '
                            'aproximado</th><th>Observação de '
                            'estudo</th></tr></thead><tbody><tr><td>ẹbí</td><td>família / '
                            'parentes</td><td>Termo amplo para relações familiares e grupo de '
                            'parentesco</td></tr><tr><td>bàbá</td><td>pai / homem mais '
                            'velho</td><td>Pode carregar sentido de respeito dependendo do '
                            'contexto</td></tr><tr><td>ìyá</td><td>mãe / mulher mais '
                            'velha</td><td>Também pode aparecer como forma respeitosa em certos '
                            'usos</td></tr><tr><td>ọmọ</td><td>filho, filha, criança</td><td>Palavra '
                            'importante em muitos contextos sociais e '
                            'culturais</td></tr><tr><td>arákùnrin</td><td>irmão / homem</td><td>Pode '
                            'aparecer em referência a homem ou irmão, conforme '
                            'contexto</td></tr><tr><td>arábìnrin</td><td>irmã / mulher</td><td>Pode '
                            'aparecer em referência a mulher ou irmã, conforme '
                            'contexto</td></tr><tr><td>ọkọ</td><td>marido</td><td>Precisa ser estudado '
                            'com contexto de uso</td></tr><tr><td>aya</td><td>esposa</td><td>Também '
                            'exige atenção ao contexto</td></tr></tbody></table>',
                            '<p>O objetivo inicial não é apenas memorizar. É praticar frases e '
                            'perceber como a língua organiza relações.</p>',
                            '<p>Exercícios simples para começar:</p>',
                            '<ul><li>Identifique quais termos indicam família.</li><li>Separe palavras '
                            'que podem envolver respeito.</li><li>Pratique a pronúncia em voz alta '
                            'apenas depois de ouvir um modelo confiável.</li><li>Leve dúvidas para '
                            'aula: “esse termo é usado em qual situação?”, “há diferença entre uso '
                            'familiar e uso respeitoso?”, “qual tom devo observar?”.</li></ul>',
                            '<p>É importante lembrar: termos como “pai” e “mãe” podem ter camadas '
                            'culturais, afetivas e sociais além da tradução direta. Em muitas '
                            'culturas, palavras familiares também funcionam como formas de respeito ou '
                            'reconhecimento. Por isso, o professor precisa explicar o uso, não apenas '
                            'o significado.</p>']},
                  {'heading': 'Vocabulário de comunidade e pertencimento',
                   'body': ['<p>Comunidade é uma ideia central para quem aprende iorubá por '
                            'identidade, ancestralidade ou cultura. As palavras ligadas ao coletivo '
                            'ajudam a entender que o idioma não vive isolado no indivíduo: ele se '
                            'manifesta em grupos, relações e continuidade.</p>',
                            '<table class="vd-table"><thead><tr><th>Iorubá</th><th>Significado '
                            'aproximado</th><th>Observação de '
                            'estudo</th></tr></thead><tbody><tr><td>àwùjọ</td><td>comunidade / '
                            'sociedade</td><td>Termo ligado ao coletivo e à vida '
                            'social</td></tr><tr><td>ìlú</td><td>cidade / povoado / '
                            'comunidade</td><td>Pode variar conforme o '
                            'contexto</td></tr><tr><td>ènìyàn</td><td>pessoa / ser '
                            'humano</td><td>Palavra essencial para falar de '
                            'pessoas</td></tr><tr><td>àwọn ènìyàn</td><td>pessoas</td><td>Forma plural '
                            'aproximada, importante para leitura '
                            'inicial</td></tr><tr><td>ọ̀rẹ́</td><td>amigo / amiga</td><td>Termo útil '
                            'em relações pessoais</td></tr><tr><td>aládùúgbò</td><td>vizinho / pessoa '
                            'da vizinhança</td><td>Relacionado à convivência '
                            'próxima</td></tr><tr><td>olùkọ́</td><td>professor / '
                            'professora</td><td>Termo importante para contexto de '
                            'aprendizagem</td></tr><tr><td>akẹ́kọ̀ọ́</td><td>estudante / '
                            'aluno</td><td>Útil em aulas e apresentações</td></tr></tbody></table>',
                            '<p>Essas palavras permitem montar temas de aula muito práticos. Por '
                            'exemplo: apresentar-se como estudante, falar do professor, reconhecer '
                            'amigos, falar de comunidade ou perguntar sobre pessoas.</p>',
                            '<p>Atenção: a escrita correta, os sinais e a pronúncia são parte do '
                            'aprendizado. Em iorubá, copiar sem orientação pode gerar erros. Por isso, '
                            'use a tabela como mapa inicial e pratique com áudio e professor.</p>']},
                  {'heading': 'Vocabulário de respeito, caráter e convivência',
                   'body': ['<p>Quando falamos de relações sociais em iorubá, respeito é um eixo '
                            'central. Não se trata apenas de “educação” no sentido superficial, mas de '
                            'postura diante de pessoas, mais velhos, comunidade, tradição e '
                            'palavra.</p>',
                            '<table class="vd-table"><thead><tr><th>Iorubá</th><th>Significado '
                            'aproximado</th><th>Observação de '
                            'estudo</th></tr></thead><tbody><tr><td>ìbọ̀wọ̀</td><td>respeito</td><td>Termo '
                            'importante para discutir postura '
                            'respeitosa</td></tr><tr><td>àgbà</td><td>pessoa mais velha / '
                            'ancião</td><td>Pode indicar senioridade e '
                            'respeito</td></tr><tr><td>ìwà</td><td>caráter / '
                            'comportamento</td><td>Palavra importante para discussões '
                            'culturais</td></tr><tr><td>ọmọlúwàbí</td><td>pessoa de bom caráter / '
                            'conduta respeitável</td><td>Conceito cultural profundo, exige explicação '
                            'cuidadosa</td></tr><tr><td>àlàáfíà</td><td>paz / bem-estar</td><td>Muito '
                            'presente em saudações e ideias de '
                            'harmonia</td></tr><tr><td>ìfẹ́</td><td>amor / afeição</td><td>Termo '
                            'amplo, deve ser estudado em contexto</td></tr><tr><td>inú '
                            'rere</td><td>boa intenção / bom coração</td><td>Expressão aproximada, '
                            'útil para discutir postura</td></tr><tr><td>ìfarabalẹ̀</td><td>calma / '
                            'paciência</td><td>Importante para postura de '
                            'aprendizado</td></tr></tbody></table>',
                            '<p>Essas palavras mostram por que estudar iorubá exige mais do que '
                            'tradução. “Ọmọlúwàbí”, por exemplo, não deve ser tratado como uma simples '
                            'palavra equivalente a “educado”. É um conceito cultural ligado a caráter, '
                            'conduta e valores. Para compreender bem, o aluno precisa de explicação, '
                            'exemplos e contexto.</p>',
                            '<p>Esse é o tipo de tema que se beneficia muito de aula ao vivo. O '
                            'professor pode apresentar situações, comparar usos e explicar o que a '
                            'tradução não alcança.</p>']},
                  {'heading': 'Como usar esse vocabulário em frases simples?',
                   'body': ['<p>Para usar o vocabulário de relações sociais em frases simples, comece '
                            'com modelos seguros e validados em aula. Não tente traduzir frases '
                            'complexas do português para o iorubá palavra por palavra. Isso costuma '
                            'gerar erros de estrutura e sentido.</p>',
                            '<p>Um caminho mais seguro é trabalhar assim:</p>',
                            '<ol><li>Escolha uma palavra.</li><li>Escute a pronúncia.</li><li>Entenda '
                            'o contexto.</li><li>Use em uma frase curta apresentada pelo '
                            'professor.</li><li>Repita com pequenas variações.</li><li>Peça '
                            'correção.</li></ol>',
                            '<p>Por exemplo, em uma aula ao vivo, o professor pode trabalhar frases de '
                            'apresentação, identificação e respeito. O aluno pode praticar:</p>',
                            '<ul><li>apresentar-se como estudante;</li><li>reconhecer o '
                            'professor;</li><li>falar de família;</li><li>nomear amigo ou '
                            'comunidade;</li><li>perguntar sobre uso correto de uma '
                            'palavra;</li><li>repetir saudações adequadas ao contexto.</li></ul>',
                            '<p>O importante é não pular etapas. Primeiro, som e sentido. Depois, uso. '
                            'Depois, frases. Depois, pequenos diálogos.</p>']},
                  {'heading': 'Como praticar com respeito?',
                   'body': ['<p>Praticar com respeito significa aprender sem pressa, sem exotizar a '
                            'língua e sem transformar cultura em decoração. O respeito aparece no modo '
                            'como você escuta, anota, pergunta e compartilha o que aprendeu.</p>',
                            '<p>Aqui estão práticas recomendadas:</p>',
                            '<h3>Ouça antes de repetir</h3>',
                            '<p>Antes de falar uma palavra, escute várias vezes. Observe o tom, a '
                            'duração, a abertura das vogais e o ritmo. Se possível, grave sua '
                            'repetição e compare com a orientação do professor.</p>',
                            '<h3>Anote contexto junto com tradução</h3>',
                            '<p>Não escreva apenas “palavra = significado”. Use um glossário com '
                            'quatro colunas:</p>',
                            '<table class="vd-table"><thead><tr><th>Palavra</th><th>Pronúncia / '
                            'tom</th><th>Significado aproximado</th><th>Contexto de '
                            'uso</th></tr></thead><tbody></tbody></table>',
                            '<p>Esse formato ajuda você a lembrar que a palavra não vive sozinha.</p>',
                            '<h3>Pergunte quando tiver dúvida</h3>',
                            '<p>A dúvida é parte do aprendizado responsável. Pergunte:</p>',
                            '<ul><li>Posso usar essa palavra em conversa comum?</li><li>Esse termo '
                            'exige contexto religioso ou cultural?</li><li>Há diferença entre uso '
                            'cotidiano e uso tradicional?</li><li>A pronúncia que fiz muda o '
                            'sentido?</li><li>Existe uma forma mais respeitosa?</li></ul>',
                            '<h3>Evite ensinar antes de aprender com segurança</h3>',
                            '<p>Compartilhar estudo pode ser bonito, mas é preciso cuidado. Antes de '
                            'publicar uma explicação, ensinar uma palavra ou interpretar uma '
                            'expressão, confirme com fontes e professores qualificados. Aprender '
                            'iorubá com respeito também é evitar espalhar erro.</p>',
                            '<h3>Valorize o professor e a tradição oral</h3>',
                            '<p>A língua iorubá tem forte dimensão oral. Por isso, a presença de quem '
                            'fala, escuta e corrige é essencial. A aula ao vivo permite que o aluno '
                            'aprenda com interação, não apenas com leitura.</p>',
                            '<p>CTA: Quer praticar vocabulário de relações sociais em iorubá com '
                            'orientação? Fale com a Vedium sobre a próxima turma em <a '
                            'href="/blog/alfabeto-ioruba">https://vediums.com/</a>.</p>']},
                  {'heading': 'Exercício para aula ao vivo: mapa das relações',
                   'body': ['<p>Este exercício ajuda o aluno iniciante a praticar vocabulário social '
                            'com consciência cultural. Ele pode ser levado para uma aula ao vivo de '
                            'iorubá.</p>',
                            '<h3>Passo 1: organize as palavras por categoria</h3>',
                            '<p>Separe o vocabulário em três grupos:</p>',
                            '<p><strong>Família:</strong><br>- ẹbí<br>- bàbá<br>- ìyá<br>- ọmọ<br>- '
                            'arákùnrin<br>- arábìnrin</p>',
                            '<p><strong>Comunidade:</strong><br>- àwùjọ<br>- ìlú<br>- ènìyàn<br>- '
                            'ọ̀rẹ́<br>- aládùúgbò<br>- olùkọ́<br>- akẹ́kọ̀ọ́</p>',
                            '<p><strong>Respeito e convivência:</strong><br>- ìbọ̀wọ̀<br>- àgbà<br>- '
                            'ìwà<br>- ọmọlúwàbí<br>- àlàáfíà<br>- ìfarabalẹ̀</p>',
                            '<h3>Passo 2: escolha cinco palavras para praticar pronúncia</h3>',
                            '<p>Não escolha muitas. Escolha cinco e trabalhe bem. Para cada uma, '
                            'anote:</p>',
                            '<ul><li>como é escrita;</li><li>como soa;</li><li>quais sinais '
                            'aparecem;</li><li>significado aproximado;</li><li>contexto de '
                            'uso;</li><li>dúvida principal.</li></ul>',
                            '<h3>Passo 3: crie perguntas para o professor</h3>',
                            '<p>Leve perguntas como:</p>',
                            '<ul><li>Essa palavra é usada em conversa cotidiana?</li><li>Qual é o erro '
                            'de pronúncia mais comum?</li><li>Essa palavra muda de sentido com outro '
                            'tom?</li><li>Posso usar essa palavra para falar com qualquer '
                            'pessoa?</li><li>Existe uma saudação relacionada a esse termo?</li></ul>',
                            '<h3>Passo 4: pratique um mini diálogo</h3>',
                            '<p>Com orientação do professor, pratique um diálogo simples de '
                            'apresentação e respeito. O foco não é falar muito. O foco é falar '
                            'corretamente, com atenção ao som e ao contexto.</p>',
                            '<p>Esse exercício transforma vocabulário em experiência de aula. Em vez '
                            'de decorar uma lista, o aluno aprende a perguntar, ouvir e ajustar.</p>']},
                  {'heading': 'Por que aula ao vivo é importante nesse tema?',
                   'body': ['<p>Aula ao vivo é importante porque vocabulário social envolve som, tom, '
                            'contexto e sensibilidade cultural. Um vídeo gravado pode apresentar uma '
                            'lista, mas não corrige sua pronúncia, não responde suas dúvidas e não '
                            'percebe quando você está interpretando uma palavra de modo raso.</p>',
                            '<p>Em uma aula de iorubá ao vivo, você pode:</p>',
                            '<ul><li>ouvir a pronúncia correta;</li><li>repetir com '
                            'correção;</li><li>entender tons;</li><li>perguntar sobre '
                            'contexto;</li><li>aprender diferenças de uso;</li><li>praticar frases '
                            'simples;</li><li>receber orientação cultural;</li><li>evoluir de forma '
                            'mais segura.</li></ul>',
                            '<p>Para quem busca iorubá por ancestralidade, cultura ou tradição, isso '
                            'faz diferença. O aluno não quer apenas “saber palavras”. Ele quer '
                            'compreender o sentido por trás delas. Quer aprender sem desrespeitar. '
                            'Quer ter segurança para continuar.</p>',
                            '<p>Essa é a proposta da Vedium: aulas ao vivo, profundidade cultural e '
                            'liberdade sem contrato de fidelidade. A permanência vem do valor da '
                            'experiência, não de amarras.</p>']},
                  {'heading': 'Como continuar depois do vocabulário inicial?',
                   'body': ['<p>Depois de estudar vocabulário de relações sociais, o próximo passo é '
                            'avançar para saudações, estruturas simples, tons e pequenos diálogos. A '
                            'sequência ideal é crescer com base, sem pressa.</p>',
                            '<p>Um caminho possível:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Etapa</th><th>Foco</th></tr></thead><tbody><tr><td>1</td><td>Sons, '
                            'tons e escuta</td></tr><tr><td>2</td><td>Saudações e '
                            'respeito</td></tr><tr><td>3</td><td>Vocabulário de família e '
                            'comunidade</td></tr><tr><td>4</td><td>Frases '
                            'simples</td></tr><tr><td>5</td><td>Perguntas '
                            'básicas</td></tr><tr><td>6</td><td>Cantigas e expressões com '
                            'orientação</td></tr><tr><td>7</td><td>Leitura e interpretação '
                            'cuidadosa</td></tr></tbody></table>',
                            '<p>Essa sequência evita que o aluno pule direto para materiais complexos '
                            'sem ter base. Quem quer entender cantigas, rezas e termos culturais '
                            'precisa primeiro construir ouvido, vocabulário e postura.</p>']},
                  {'heading': 'Conclusão com CTA forte',
                   'body': ['<p>O vocabulário de relações sociais em iorubá é uma porta de entrada '
                            'poderosa porque mostra a língua em sua dimensão humana: família, '
                            'comunidade, amizade, respeito, caráter e convivência. Para quem busca '
                            'aprender por ancestralidade, identidade, cultura ou tradição, essas '
                            'palavras ajudam a construir uma base mais sensível e responsável.</p>',
                            '<p>Mas esse aprendizado precisa ser feito com cuidado. No iorubá, '
                            'pronúncia, tons e contexto importam. Traduções são aproximações. Algumas '
                            'palavras carregam camadas culturais profundas. Por isso, a melhor forma '
                            'de avançar é unir estudo individual, escuta atenta e aula ao vivo com '
                            'orientação qualificada.</p>',
                            '<p>A Vedium oferece aulas de iorubá ao vivo, com respeito à cultura e '
                            'foco em evolução real. Você aprende o idioma além das palavras: entende '
                            'sentido, contexto e uso. E continua porque percebe valor, não porque está '
                            'preso a contrato de fidelidade.</p>',
                            '<p>Fale com a Vedium sobre a próxima turma de Iorubá em <a '
                            'href="/curso-de-ioruba-online">https://vediums.com/</a> e comece a '
                            'aprender com profundidade, respeito e presença.</p>']}],
     'faqs': [{'q': 'Por que estudar vocabulário de relações sociais em iorubá?',
               'a': 'Porque esse vocabulário ajuda a entender família, comunidade, respeito e '
                    'convivência. Ele cria uma base humana e cultural para o aprendizado, em vez de '
                    'limitar o estudo a palavras soltas.'},
              {'q': 'Posso decorar palavras em iorubá apenas por listas?',
               'a': 'Listas podem ajudar como apoio, mas não bastam. O ideal é estudar pronúncia, '
                    'tons, contexto de uso e exemplos com orientação, especialmente porque o iorubá é '
                    'uma língua tonal.'},
              {'q': 'O que significa aprender iorubá com respeito?',
               'a': 'Significa ouvir antes de repetir, perguntar antes de afirmar, aceitar correção, '
                    'evitar exotização da cultura e estudar a língua junto com seu contexto histórico, '
                    'social e cultural.'},
              {'q': 'Aula ao vivo ajuda no vocabulário de iorubá?',
               'a': 'Sim. A aula ao vivo permite corrigir pronúncia, entender tons, tirar dúvidas '
                    'culturais e praticar o vocabulário em frases e situações reais.'},
              {'q': 'A Vedium oferece curso de iorubá online?',
               'a': 'Sim. A Vedium oferece aulas de iorubá online e ao vivo, com profundidade '
                    'cultural, prática orientada e sem contrato de fidelidade.'}],
     'cta_title': 'Quer aprender iorubá com pronúncia correta desde o início?',
     'cta_text': 'Aulas ao vivo, do zero ao avançado, com foco em tons e conversação real.',
     'cta_label': 'Conhecer o curso de Iorubá',
     'cta_url': '/curso-de-ioruba-online'},
    "brazilian-portuguese-for-relocation-teams-what-employees-need-before-arrival": {'title': 'Brazilian Portuguese for relocation teams: what employees need before arrival',
     'meta_description': 'Help relocation teams prepare employees for Brazil with practical '
                         'Portuguese, culture, documents and live language training.',
     'h1': 'Brazilian Portuguese for relocation teams: what employees need before arrival',
     'date': '2025-01-01',
     'date_display': 'January 1, 2025',
     'hero_image': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aprender português como língua estrangeira',
     'tag': 'Brazilian Portuguese',
     'lang': 'en',
     'category': 'brazilian-portuguese',
     'lead': 'Relocation to Brazil is easier when employees arrive with practical Portuguese, cultural '
             'confidence and a clear language plan. Before the flight, relocation teams should prepare '
             'employees to handle daily interactions, workplace conversations, basic documents, '
             'housing routines and the social codes that shape life in Brazil.',
     'sections': [{'heading': '',
                   'body': ['<p>For global mobility teams, language training is not a “nice-to-have” '
                            'benefit. It is part of risk reduction, employee experience and faster '
                            'integration. A professional who lands in Brazil unable to ask questions, '
                            'understand local processes or express basic needs may depend too much on '
                            'HR, colleagues, partners or family members. That creates friction for '
                            'everyone.</p>',
                            '<p>The solution is not to overload the employee with grammar before '
                            'arrival. The better approach is to teach Brazilian Portuguese for real '
                            'situations: speaking to a building doorman, confirming an address with a '
                            'driver, introducing oneself at work, asking about documents, '
                            'understanding payment methods, scheduling appointments, joining meetings '
                            'and reading essential signs or forms.</p>',
                            '<p>At Vedium, Brazilian Portuguese for foreigners is taught through live '
                            'online classes, with a practical and cultural focus. That matters because '
                            'relocation is not only about moving a person from one country to another. '
                            'It is about helping that person function, work and feel at home.</p>']},
                  {'heading': 'What relocation teams should solve before the employee arrives',
                   'body': ['<p>Relocation teams should solve three problems before arrival: '
                            'communication, confidence and context. Communication helps the employee '
                            'perform basic tasks. Confidence reduces fear of speaking. Context helps '
                            'the employee understand how Brazil works beyond vocabulary.</p>',
                            '<p>A pre-arrival Brazilian Portuguese plan should answer questions such '
                            'as:</p>',
                            '<ul><li>Can the employee introduce themselves in Portuguese?</li><li>Can '
                            'they explain where they live, work and need to go?</li><li>Can they ask '
                            'for help in a respectful and natural way?</li><li>Can they understand '
                            'basic workplace greetings and informal expressions?</li><li>Can they read '
                            'essential words in forms, signs, bills and apps?</li><li>Can they deal '
                            'with common situations without waiting for someone to translate '
                            'everything?</li></ul>',
                            '<p>This is especially important for professionals relocating with family. '
                            'The employee may need Portuguese at work, but their daily life also '
                            'includes schools, housing, supermarkets, pharmacies, banks, '
                            'transportation and healthcare appointments. Even a basic level can make '
                            'the difference between feeling lost and feeling capable.</p>',
                            '<p>For companies, the business case is simple: the faster the employee '
                            'adapts, the faster they can focus on performance. Language support helps '
                            'reduce avoidable stress, improves the onboarding experience and shows '
                            'that the company is investing in the person, not just the position.</p>',
                            '<p><strong>CTA for relocation teams:</strong> Book a free level check '
                            'with Vedium and understand the Portuguese starting point of each employee '
                            'before arrival: <a '
                            'href="/en/learn-portuguese-brazil">https://vediums.com/</a></p>']},
                  {'heading': 'Why Brazilian Portuguese matters before landing in Brazil',
                   'body': ['<p>Brazilian Portuguese matters before arrival because many everyday '
                            'systems depend on spoken interaction. Apps help, but they do not replace '
                            'live communication when the situation is urgent, emotional or '
                            'unclear.</p>',
                            '<p>A relocating employee may need to speak Portuguese when:</p>',
                            '<ul><li>confirming delivery details with a courier;</li><li>talking to a '
                            'landlord, building manager or doorman;</li><li>asking about invoices, '
                            'receipts or payment methods;</li><li>explaining a dietary restriction at '
                            'a restaurant;</li><li>checking appointment times;</li><li>understanding '
                            'workplace small talk;</li><li>asking for directions in a '
                            'neighborhood;</li><li>handling school or childcare '
                            'communication;</li><li>describing a problem with internet, utilities or '
                            'maintenance.</li></ul>',
                            '<p>The point is not immediate fluency. The point is functional '
                            'independence. Employees should arrive able to participate in simple '
                            'conversations and recognize the language patterns they will hear every '
                            'day.</p>',
                            '<p>A common mistake is training only formal Portuguese. In Brazil, '
                            'employees will hear a mix of polite professional language, regional '
                            'accents, casual expressions and fast everyday speech. A practical course '
                            'should prepare them for this range without making them feel '
                            'overwhelmed.</p>',
                            '<p>This is where live classes make a difference. In a live class, the '
                            'teacher can correct pronunciation, simulate real situations, explain '
                            'cultural nuance and adapt the lesson to the employee’s role, city and '
                            'relocation timeline. Recorded lessons can support review, but they cannot '
                            'respond to the exact sentence the employee needs to say tomorrow.</p>']},
                  {'heading': 'The pre-arrival Brazilian Portuguese checklist',
                   'body': ['<p>A strong pre-arrival checklist should organize Portuguese around '
                            'immediate use. Relocation teams do not need to turn employees into '
                            'advanced speakers before arrival. They need to give them the first layer '
                            'of autonomy.</p>',
                            '<h3>1. Survival communication</h3>',
                            '<p>Survival communication means the employee can handle the first days '
                            'without panic. They should learn how to greet people, ask for repetition, '
                            'spell their name, share phone numbers, confirm addresses and say when '
                            'they do not understand.</p>',
                            '<p>Useful phrases include:</p>',
                            '<ul><li>“Você pode repetir, por favor?” — Can you repeat, '
                            'please?</li><li>“Eu estou aprendendo português.” — I am learning '
                            'Portuguese.</li><li>“Pode falar mais devagar?” — Can you speak more '
                            'slowly?</li><li>“Como eu chego nesse endereço?” — How do I get to this '
                            'address?</li><li>“Preciso de ajuda.” — I need help.</li></ul>',
                            '<p>These phrases may look basic, but they are powerful. They give the '
                            'employee permission to participate instead of freezing.</p>',
                            '<h3>2. Workplace basics</h3>',
                            '<p>Workplace Portuguese should cover introductions, meetings, schedules, '
                            'feedback and polite interaction. Even when the company operates in '
                            'English, Portuguese often appears in informal conversations, building '
                            'communication, HR documents, local vendors and team culture.</p>',
                            '<p>Employees should practice how to say:</p>',
                            '<ul><li>their role and department;</li><li>where they worked '
                            'before;</li><li>what they are responsible for;</li><li>when they are '
                            'available;</li><li>what they need clarified;</li><li>whether they agree, '
                            'disagree or need more time.</li></ul>',
                            '<p>This is also a cultural topic. Brazilian workplace communication can '
                            'include warmth, small talk and indirect softening before difficult '
                            'points. Employees do not need to imitate everything, but they should '
                            'understand what is happening.</p>',
                            '<h3>3. Housing and neighborhood language</h3>',
                            '<p>Housing is one of the first stress points in relocation. Employees may '
                            'need to understand words related to rent, condominium rules, maintenance, '
                            'deliveries, parking, bills and building access.</p>',
                            '<p>A practical Brazilian Portuguese course should teach words such '
                            'as:</p>',
                            '<ul><li>aluguel — rent;</li><li>condomínio — building fee or '
                            'condominium;</li><li>portaria — building reception/security '
                            'desk;</li><li>entrega — delivery;</li><li>manutenção — '
                            'maintenance;</li><li>boleto — payment slip;</li><li>comprovante — proof '
                            'or receipt;</li><li>endereço — address;</li><li>bairro — '
                            'neighborhood.</li></ul>',
                            '<p>This vocabulary helps the employee understand local instructions '
                            'faster and reduces dependency on HR for simple issues.</p>',
                            '<h3>4. Documents and appointments</h3>',
                            '<p>Relocation teams should not turn language classes into legal training. '
                            'However, employees need enough Portuguese to recognize the vocabulary '
                            'around documents and appointments.</p>',
                            '<p>Official procedures can vary by nationality, visa type and employment '
                            'situation, so companies should always verify current instructions with '
                            'immigration counsel and official sources. Useful official references '
                            'include the Brazilian Ministry of Foreign Affairs pages on visa '
                            'categories, Gov.br service pages for foreigner registration and CPF '
                            'guidance for non-Brazilian citizens.</p>',
                            '<p>Language training should help employees understand terms such as:</p>',
                            '<ul><li>passaporte — passport;</li><li>visto — visa;</li><li>autorização '
                            'de residência — residence authorization;</li><li>registro — '
                            'registration;</li><li>CPF — individual taxpayer '
                            'registry;</li><li>agendamento — appointment;</li><li>documento — '
                            'document;</li><li>formulário — form;</li><li>assinatura — '
                            'signature.</li></ul>',
                            '<p>The employee does not need to master the system alone. They need to '
                            'understand what is being requested, what questions to ask and when to ask '
                            'for help.</p>',
                            '<h3>5. Daily services and payments</h3>',
                            '<p>Brazilian daily life includes many payment and service interactions. '
                            'Employees may hear words related to Pix, card payments, installments, '
                            'invoices, receipts and service fees. Even when they use apps, they will '
                            'need to understand confirmations, cancellations and support '
                            'conversations.</p>',
                            '<p>Useful vocabulary includes:</p>',
                            '<ul><li>cartão — card;</li><li>dinheiro — cash;</li><li>nota fiscal — '
                            'invoice or fiscal receipt;</li><li>recibo — receipt;</li><li>parcela — '
                            'installment;</li><li>taxa — fee;</li><li>senha — password or '
                            'PIN;</li><li>atendimento — customer service.</li></ul>',
                            '<p>These words help employees navigate supermarkets, pharmacies, taxis, '
                            'restaurants, service providers and online purchases.</p>']},
                  {'heading': 'Real-life situations employees should practice',
                   'body': ['<p>The best pre-arrival Portuguese training uses scenarios, not isolated '
                            'word lists. Employees need to rehearse the moments that will actually '
                            'happen.</p>',
                            '<p>Relocation teams can ask the language provider to include role plays '
                            'such as:</p>',
                            '<ul><li>arriving at the airport and confirming '
                            'transportation;</li><li>checking into temporary housing;</li><li>asking '
                            'the building doorman about deliveries;</li><li>introducing oneself to a '
                            'Brazilian colleague;</li><li>ordering food and explaining '
                            'preferences;</li><li>buying medicine at a pharmacy;</li><li>scheduling a '
                            'medical or service appointment;</li><li>explaining an internet or '
                            'maintenance problem;</li><li>asking for help when an app or payment '
                            'fails;</li><li>joining a simple workplace conversation.</li></ul>',
                            '<p>These simulations build confidence because the employee hears their '
                            'own voice solving problems in Portuguese before the real situation '
                            'happens. This is one of the main advantages of live online classes: the '
                            'teacher can pause, correct, repeat and make the conversation more '
                            'realistic.</p>']},
                  {'heading': 'Essential vocabulary before arrival',
                   'body': ['<p>Employees should learn high-frequency words first. The goal is not to '
                            'memorize a dictionary. The goal is to recognize words that appear '
                            'repeatedly in Brazilian life.</p>',
                            '<p>A practical vocabulary map may include:</p>',
                            '<p><strong>People and relationships:</strong> colega, chefe, gerente, '
                            'vizinho, porteiro, atendente, motorista.</p>',
                            '<p><strong>Places:</strong> empresa, escritório, mercado, farmácia, '
                            'banco, escola, hospital, restaurante, aeroporto.</p>',
                            '<p><strong>Time:</strong> hoje, amanhã, ontem, agora, depois, cedo, '
                            'tarde, semana, mês.</p>',
                            '<p><strong>Action verbs:</strong> precisar, querer, poder, entender, '
                            'falar, chegar, sair, pagar, comprar, marcar.</p>',
                            '<p><strong>Problem words:</strong> problema, erro, atraso, cancelado, '
                            'urgente, perdido, quebrado, indisponível.</p>',
                            '<p>This vocabulary should be practiced in sentences. Employees should not '
                            'only know that “precisar” means “to need.” They should be able to say, '
                            '“Eu preciso marcar um horário” or “Preciso de ajuda com este '
                            'documento.”</p>']},
                  {'heading': 'How live classes improve relocation outcomes',
                   'body': ['<p>Live classes improve relocation outcomes because they train reaction, '
                            'not only knowledge. In real life, employees need to listen, respond, ask '
                            'again and adjust. That is hard to build through passive study.</p>',
                            '<p>For relocation teams, live Brazilian Portuguese classes offer four '
                            'advantages:</p>',
                            '<ol><li><strong>Better diagnosis:</strong> the teacher can identify '
                            'pronunciation, listening and confidence gaps '
                            'quickly.</li><li><strong>Faster relevance:</strong> lessons can be '
                            'adapted to the employee’s city, job and relocation '
                            'stage.</li><li><strong>Cultural explanation:</strong> the employee learns '
                            'what a phrase means and how it may be '
                            'perceived.</li><li><strong>Accountability:</strong> scheduled classes '
                            'create rhythm, which helps busy professionals keep learning.</li></ol>',
                            '<p>At Vedium, classes are live and designed to connect language with '
                            'culture. The objective is not to trap employees in long contracts. It is '
                            'to help them see progress and continue because the learning is '
                            'useful.</p>',
                            '<p><strong>CTA:</strong> Prepare your relocation employees with practical '
                            'Brazilian Portuguese before they land. Book a free level check at <a '
                            'href="/en/portuguese-placement-test">https://vediums.com/</a></p>']},
                  {'heading': 'How relocation teams can structure the program',
                   'body': ['<p>A clear program should combine assessment, practical modules and '
                            'progress visibility. For HR and global mobility teams, structure matters '
                            'because each employee may arrive with a different background.</p>',
                            '<p>A useful model includes:</p>',
                            '<p><strong>Before arrival:</strong> level check, survival Portuguese, '
                            'relocation vocabulary and basic cultural orientation.</p>',
                            '<p><strong>First 30 days in Brazil:</strong> housing, transportation, '
                            'workplace introductions, appointments and daily services.</p>',
                            '<p><strong>After 60 to 90 days:</strong> workplace communication, '
                            'meetings, presentations, feedback, social integration and more complex '
                            'listening practice.</p>',
                            '<p><strong>Ongoing:</strong> level progression, conversation practice and '
                            'targeted lessons based on the employee’s role.</p>',
                            '<p>This format avoids a common problem: teaching too much too soon. '
                            'Relocation is already demanding. The language plan should reduce '
                            'pressure, not add another source of anxiety.</p>']},
                  {'heading': 'Official sources relocation teams should verify',
                   'body': ['<p>Relocation rules and document procedures can change. Before publishing '
                            'internal guidance or advising employees, teams should verify information '
                            'with official sources and qualified immigration support.</p>',
                            '<p>Useful official starting points include:</p>',
                            '<ul><li>Brazilian Ministry of Foreign Affairs — visa information: '
                            'https://www.gov.br/mre/pt-br/consulado-los-angeles/english/visas/types-of-visa</li><li>Gov.br '
                            '— registration as a foreigner in Brazil: '
                            'https://www.gov.br/pt-br/servicos/registrar-se-como-estrangeiro-no-brasil</li><li>Ministry '
                            'of Foreign Affairs — CPF for non-Brazilian citizens: '
                            'https://www.gov.br/mre/pt-br/consulado-hartford/servicos-consulares-e-informacoes-uties/cpf-brasileiros-foreigners/cpf-foreigners</li><li>Brazilian '
                            'Federal Police — migration FAQ: '
                            'https://www.gov.br/pf/pt-br/assuntos/imigracao/en/duvidas</li></ul>',
                            '<p>Language training should support these processes by making employees '
                            'more prepared to understand instructions, ask questions and participate '
                            'in appointments. It should not replace legal or immigration advice.</p>']},
                  {'heading': 'Conclusion: prepare people, not just paperwork',
                   'body': ['<p>A successful relocation to Brazil depends on more than flights, '
                            'housing and documents. Employees also need words, confidence and cultural '
                            'context. When relocation teams invest in Brazilian Portuguese before '
                            'arrival, they help professionals start their new chapter with less stress '
                            'and more autonomy.</p>',
                            '<p>The best preparation is practical: survival phrases, workplace '
                            'introductions, housing vocabulary, document language, daily service '
                            'interactions and real conversation practice. That is exactly where live '
                            'classes create value. Employees can rehearse the conversations they will '
                            'soon face, receive correction and understand the cultural meaning behind '
                            'the words.</p>',
                            '<p>Vedium offers live online Brazilian Portuguese classes for foreigners, '
                            'with a practical and cultural approach designed for real life in Brazil. '
                            'No generic app can fully prepare an employee for the human side of '
                            'relocation. A live teacher can.</p>',
                            '<p><strong>Book a free level check with Vedium and help your relocation '
                            'employees arrive in Brazil ready to speak, work and belong: <a '
                            'href="/en/learn-portuguese-brazil">https://vediums.com/</a></strong></p>']}],
     'faqs': [{'q': 'When should employees start Brazilian Portuguese before relocating to Brazil?',
               'a': 'Ideally, employees should start before arrival, even if they only have a few '
                    'weeks. The first goal is not fluency; it is basic independence for greetings, '
                    'directions, housing, appointments and workplace introductions.'},
              {'q': 'What level of Portuguese does a relocating employee need before arrival?',
               'a': 'Most employees benefit from a survival or beginner level before arrival. They '
                    'should be able to introduce themselves, ask for help, understand common words and '
                    'manage simple daily situations.'},
              {'q': 'Should relocation teams choose Brazilian Portuguese instead of European '
                    'Portuguese?',
               'a': 'Yes, for employees moving to Brazil, Brazilian Portuguese is the right focus. '
                    'Pronunciation, vocabulary, expressions and daily usage differ, so training should '
                    'match the country where the employee will live and work.'},
              {'q': 'Can live Portuguese classes help employees who are very busy?',
               'a': 'Yes. Live classes help busy employees because lessons can focus on the most '
                    'urgent real-life situations. The teacher can adapt practice to the employee’s '
                    'role, schedule, city and immediate relocation needs.'},
              {'q': 'How can Vedium support relocation teams?',
               'a': 'Vedium supports relocation teams with live online Brazilian Portuguese classes, '
                    'practical conversation, cultural context and free level checks. Teams can use '
                    'this to prepare employees before arrival and continue development after they '
                    'settle in Brazil.'}],
     'cta_title': 'Want to know your real Portuguese level?',
     'cta_text': "Take Vedium's free placement test and find out where to start.",
     'cta_label': 'Learn about the Portuguese course',
     'cta_url': '/en/learn-portuguese-brazil'},
    "brazilian-portuguese-for-expats-what-to-learn-before-your-first-month-in-brazil": {'title': 'Brazilian Portuguese for expats: what to learn before your first month in Brazil',
     'meta_description': 'Learn what expats should study before their first month in Brazil: real-life '
                         'Portuguese, culture, vocabulary and live practice.',
     'h1': 'Brazilian Portuguese for expats: what to learn before your first month in Brazil',
     'date': '2025-01-07',
     'date_display': 'January 7, 2025',
     'hero_image': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aprender português como língua estrangeira',
     'tag': 'Brazilian Portuguese',
     'lang': 'en',
     'category': 'brazilian-portuguese',
     'lead': 'Expats moving to Brazil should learn practical Brazilian Portuguese before their first '
             'month: greetings, addresses, housing vocabulary, transportation, food, payments, '
             'workplace introductions, emergency phrases and the cultural habits that shape everyday '
             'conversation. The goal is not to arrive fluent. The goal is to arrive able to '
             'participate in real life with more confidence.',
     'sections': [{'heading': '',
                   'body': ['<p>For many foreigners, Brazil is exciting and challenging at the same '
                            'time. You may be preparing for a job transfer, an international study '
                            'program, a family move, a long-term remote work experience or a personal '
                            'relocation. In all these situations, Portuguese is more than a language '
                            'subject. It becomes the tool you use to solve problems, build '
                            'relationships, understand instructions, read signs, ask for help and feel '
                            'less dependent on translation apps.</p>',
                            '<p>The first month in Brazil usually brings a wave of practical '
                            'situations: checking into temporary housing, talking to a building '
                            'doorman, confirming deliveries, using ride-hailing apps, shopping for '
                            'groceries, ordering food, opening local services, understanding receipts, '
                            'attending workplace meetings and meeting neighbors. Apps can support you, '
                            'but they do not replace the confidence of saying a clear sentence and '
                            'understanding the answer.</p>',
                            '<p>That is why the smartest approach is to study Brazilian Portuguese for '
                            'real-life use. At Vedium, Portuguese for foreigners is taught through '
                            'live online classes, with cultural context and speaking practice from the '
                            'beginning. You learn the language as it is used in Brazil, not only as it '
                            'appears in a grammar table.</p>']},
                  {'heading': 'Why expats should study Brazilian Portuguese before arriving',
                   'body': ['<p>Expats should study before arrival because the first month is full of '
                            'spoken interactions. Even a basic level of Portuguese can reduce stress, '
                            'improve safety and make daily life easier.</p>',
                            '<p>Brazil is a warm and social country, but it also requires '
                            'communication in small everyday moments. A doorman may ask who you are '
                            'visiting. A delivery person may call to confirm an address. A '
                            'receptionist may request a document. A driver may ask which entrance to '
                            'use. A colleague may invite you for coffee. These are simple situations, '
                            'but they become difficult when you do not recognize the words or know how '
                            'to respond.</p>',
                            '<p>Learning before arrival gives you three advantages:</p>',
                            '<ul><li><strong>Autonomy:</strong> you can handle small tasks without '
                            'waiting for someone to translate.</li><li><strong>Confidence:</strong> '
                            'you are more willing to speak, even with '
                            'mistakes.</li><li><strong>Cultural awareness:</strong> you understand how '
                            'Brazilians greet, ask, explain and build trust.</li></ul>',
                            '<p>For expats, the biggest problem is rarely one isolated word. The real '
                            'problem is speed, context and confidence. You may learn that “obrigado” '
                            'means “thank you”, but you also need to understand when people say '
                            '“valeu”, “brigado”, “imagina”, “pois não”, “tudo certo?” or “beleza?”. '
                            'Brazilian Portuguese is alive, informal and highly relational. A good '
                            'course prepares you for that reality.</p>',
                            '<p>This is also why live classes matter. In a live class, you can '
                            'practice pronunciation, ask questions, repeat real phrases and simulate '
                            'the exact situations you will face in Brazil. Recorded lessons are useful '
                            'for review, but they cannot correct how you say an address, guide your '
                            'first conversation with a landlord or help you adapt vocabulary to your '
                            'city, job and lifestyle.</p>',
                            '<p><strong>CTA:</strong> Book a free level check with Vedium and start '
                            'your Brazilian Portuguese plan before your first month in Brazil: <a '
                            'href="/en/learn-portuguese-brazil">https://vediums.com/</a></p>']},
                  {'heading': 'What to learn for housing and neighborhood life',
                   'body': ['<p>For housing and neighborhood life, learn how to identify yourself, '
                            'explain where you live, speak with doormen, ask about maintenance and '
                            'understand basic building vocabulary.</p>',
                            '<p>Many expats in Brazil live in apartment buildings, where daily '
                            'interaction with the entrance desk is common. You may need to say your '
                            'apartment number, confirm a visitor, receive a package, talk about '
                            'parking, ask about water, internet or electricity, and understand '
                            'building rules.</p>',
                            '<p>Useful vocabulary includes:</p>',
                            '<ul><li><strong>prédio</strong> — '
                            'building;</li><li><strong>apartamento</strong> — '
                            'apartment;</li><li><strong>portaria</strong> — front desk or building '
                            'entrance;</li><li><strong>porteiro / porteira</strong> — doorman or front '
                            'desk staff;</li><li><strong>entrega</strong> — '
                            'delivery;</li><li><strong>encomenda</strong> — '
                            'package;</li><li><strong>elevador</strong> — '
                            'elevator;</li><li><strong>garagem</strong> — '
                            'garage;</li><li><strong>chave</strong> — '
                            'key;</li><li><strong>manutenção</strong> — maintenance.</li></ul>',
                            '<p>Useful phrases include:</p>',
                            '<ul><li>“Eu moro no apartamento ___.” — I live in apartment '
                            '___.</li><li>“Chegou alguma encomenda para mim?” — Has any package '
                            'arrived for me?</li><li>“Pode avisar quando a entrega chegar?” — Can you '
                            'let me know when the delivery arrives?</li><li>“O elevador está '
                            'funcionando?” — Is the elevator working?</li><li>“Preciso falar com a '
                            'administração.” — I need to speak with the administration.</li></ul>',
                            '<p>This kind of vocabulary is more urgent than memorizing long verb '
                            'tables. During your first month, the language you use around your home '
                            'directly affects your comfort. A practical Brazilian Portuguese course '
                            'should prepare you to speak calmly in these small, repeated '
                            'situations.</p>']},
                  {'heading': 'What to learn for transportation and getting around',
                   'body': ['<p>For transportation, learn addresses, directions, time expressions, '
                            'landmarks and how to confirm routes. Getting around in Brazil often '
                            'requires quick spoken communication.</p>',
                            '<p>Even when you use navigation apps, people may ask for details. A '
                            'driver might say they are at the wrong gate. A receptionist may explain '
                            'that the entrance is on another street. Someone may tell you to turn left '
                            'after a bakery, cross the avenue or wait near the pharmacy. This is why '
                            'expats should learn location language early.</p>',
                            '<p>Essential words include:</p>',
                            '<ul><li><strong>rua</strong> — street;</li><li><strong>avenida</strong> — '
                            'avenue;</li><li><strong>esquina</strong> — '
                            'corner;</li><li><strong>entrada</strong> — '
                            'entrance;</li><li><strong>saída</strong> — '
                            'exit;</li><li><strong>perto</strong> — '
                            'near;</li><li><strong>longe</strong> — far;</li><li><strong>à '
                            'direita</strong> — to the right;</li><li><strong>à esquerda</strong> — to '
                            'the left;</li><li><strong>em frente</strong> — straight ahead or in '
                            'front.</li></ul>',
                            '<p>Practice phrases such as:</p>',
                            '<ul><li>“Esse é o endereço certo?” — Is this the correct '
                            'address?</li><li>“Pode me deixar na entrada principal?” — Can you drop me '
                            'at the main entrance?</li><li>“Quanto tempo demora?” — How long does it '
                            'take?</li><li>“É perto daqui?” — Is it near here?</li><li>“Eu preciso ir '
                            'para este endereço.” — I need to go to this address.</li></ul>',
                            '<p>The cultural detail is important: Brazilians often give directions '
                            'using landmarks, not only street numbers. They may say something is “next '
                            'to the bakery”, “behind the mall” or “in front of the square”. A live '
                            'teacher can help you understand these patterns and practice listening to '
                            'natural responses.</p>']},
                  {'heading': 'What to learn for food, shopping and payments',
                   'body': ['<p>For daily shopping, learn how to order, ask prices, understand payment '
                            'methods, request receipts and explain preferences or restrictions.</p>',
                            '<p>Food is one of the easiest ways to enjoy Brazil, but it is also one of '
                            'the first areas where language becomes necessary. You may need to order '
                            'lunch, ask if a dish contains meat, explain allergies, buy groceries, '
                            'understand the difference between “débito” and “crédito”, or ask whether '
                            'a store accepts Pix or card.</p>',
                            '<p>Essential words include:</p>',
                            '<ul><li><strong>cardápio</strong> — menu;</li><li><strong>conta</strong> '
                            '— bill;</li><li><strong>nota fiscal</strong> — receipt or '
                            'invoice;</li><li><strong>dinheiro</strong> — '
                            'cash;</li><li><strong>cartão</strong> — '
                            'card;</li><li><strong>débito</strong> — '
                            'debit;</li><li><strong>crédito</strong> — credit;</li><li><strong>sem '
                            'açúcar</strong> — without sugar;</li><li><strong>sem carne</strong> — '
                            'without meat;</li><li><strong>água sem gás / com gás</strong> — still '
                            'water / sparkling water.</li></ul>',
                            '<p>Useful phrases include:</p>',
                            '<ul><li>“Pode trazer o cardápio, por favor?” — Can you bring the menu, '
                            'please?</li><li>“Eu tenho alergia a ___.” — I am allergic to '
                            '___.</li><li>“Aceita cartão?” — Do you accept card?</li><li>“Pode ser no '
                            'crédito?” — Can it be credit?</li><li>“A conta, por favor.” — The bill, '
                            'please.</li></ul>',
                            '<p>This is also a good moment to learn Brazilian politeness. “Por favor”, '
                            '“obrigado/obrigada”, “com licença” and “desculpa” are simple, but they '
                            'help interactions feel warmer and more respectful. In Brazil, tone '
                            'matters. Speaking with kindness often makes communication easier, even '
                            'when your Portuguese is still basic.</p>']},
                  {'heading': 'What to learn for work and professional integration',
                   'body': ['<p>For work, learn introductions, meeting phrases, scheduling language, '
                            'polite questions and vocabulary connected to your role. Even in '
                            'English-speaking companies, Portuguese appears in local routines.</p>',
                            '<p>Many expats assume they will only use English at work. That may be '
                            'true in formal meetings, but Portuguese often appears in office '
                            'greetings, informal chats, HR communication, vendor conversations, '
                            'facility requests, events and team relationships. Understanding these '
                            'interactions helps you feel included.</p>',
                            '<p>Start with phrases such as:</p>',
                            '<ul><li>“Prazer em conhecer.” — Nice to meet you.</li><li>“Eu trabalho na '
                            'área de ___.” — I work in the area of ___.</li><li>“Você pode me '
                            'explicar?” — Can you explain it to me?</li><li>“Ainda estou aprendendo '
                            'português.” — I am still learning Portuguese.</li><li>“Podemos marcar uma '
                            'reunião?” — Can we schedule a meeting?</li><li>“Qual é o prazo?” — What '
                            'is the deadline?</li><li>“Vou confirmar e te aviso.” — I will confirm and '
                            'let you know.</li></ul>',
                            '<p>The goal is not to sound perfect. The goal is to participate. When you '
                            'make the effort to speak Portuguese, many Brazilian colleagues appreciate '
                            'it. It shows respect for the local culture and creates a stronger '
                            'connection.</p>',
                            '<p>A structured Portuguese for foreigners course should adapt practice to '
                            'your professional reality. A software engineer, an executive, a teacher, '
                            'a researcher and a relocation employee do not need exactly the same '
                            'vocabulary. Live classes make this personalization easier because the '
                            'teacher can bring your real situations into class.</p>']},
                  {'heading': 'Essential vocabulary for your first month in Brazil',
                   'body': ['<p>The best first-month vocabulary is practical, repeatable and connected '
                            'to urgent needs. Focus on phrases you will actually say, not isolated '
                            'lists you may never use.</p>',
                            '<p>Start with these categories:</p>',
                            '<h3>Personal information</h3>',
                            '<p>You should be able to say your name, nationality, profession, address, '
                            'phone number and reason for being in Brazil.</p>',
                            '<p>Examples:</p>',
                            '<ul><li>“Meu nome é ___.” — My name is ___.</li><li>“Eu sou de ___.” — I '
                            'am from ___.</li><li>“Eu estou no Brasil a trabalho.” — I am in Brazil '
                            'for work.</li><li>“Meu telefone é ___.” — My phone number is '
                            '___.</li></ul>',
                            '<h3>Help and clarification</h3>',
                            '<p>These phrases are essential because they keep the conversation open '
                            'when you do not understand.</p>',
                            '<ul><li>“Pode repetir?” — Can you repeat?</li><li>“Pode falar mais '
                            'devagar?” — Can you speak more slowly?</li><li>“Como se diz ___ em '
                            'português?” — How do you say ___ in Portuguese?</li><li>“Eu não entendi.” '
                            '— I did not understand.</li></ul>',
                            '<h3>Time and appointments</h3>',
                            '<p>You will need time expressions for meetings, deliveries, classes, '
                            'services and appointments.</p>',
                            '<ul><li><strong>hoje</strong> — today;</li><li><strong>amanhã</strong> — '
                            'tomorrow;</li><li><strong>ontem</strong> — '
                            'yesterday;</li><li><strong>agora</strong> — now;</li><li><strong>mais '
                            'tarde</strong> — later;</li><li><strong>semana que vem</strong> — next '
                            'week.</li></ul>',
                            '<h3>Problems and emergencies</h3>',
                            '<p>You should know how to express basic problems clearly.</p>',
                            '<ul><li>“Preciso de ajuda.” — I need help.</li><li>“Perdi minha chave.” — '
                            'I lost my key.</li><li>“Meu celular não está funcionando.” — My phone is '
                            'not working.</li><li>“É urgente.” — It is urgent.</li></ul>',
                            '<p>This vocabulary creates a foundation. From there, you can expand into '
                            'grammar, conversation, pronunciation and cultural fluency.</p>']},
                  {'heading': 'How live classes help expats learn faster',
                   'body': ['<p>Live classes help expats learn faster because they turn passive study '
                            'into real communication. You do not just recognize words; you practice '
                            'using them with correction, rhythm and context.</p>',
                            '<p>A strong live-class plan for expats should include:</p>',
                            '<ul><li>speaking practice from the first lesson;</li><li>pronunciation '
                            'correction;</li><li>role-play for real situations in '
                            'Brazil;</li><li>vocabulary adapted to housing, work, transport and daily '
                            'life;</li><li>cultural explanations behind common '
                            'expressions;</li><li>progress tracking by level;</li><li>flexibility for '
                            'busy relocation routines.</li></ul>',
                            '<p>This approach is especially useful for adults who need Portuguese for '
                            'life, not for a school exam. Expats often have limited time and high '
                            'pressure. They need classes that respect their routine and focus on what '
                            'will make life easier immediately.</p>',
                            '<p>At Vedium, the promise is practical and human: live online Portuguese '
                            'classes, cultural depth and no long-term lock-in. You continue because '
                            'the classes help you speak with more confidence, not because a contract '
                            'forces you to stay.</p>']},
                  {'heading': 'Conclusion: arrive in Brazil with more confidence, not just more '
                              'vocabulary',
                   'body': ['<p>Your first month in Brazil will be easier if you prepare for real '
                            'conversations before arrival. Learn how to introduce yourself, ask for '
                            'help, handle housing situations, move around the city, order food, make '
                            'payments and participate at work. This is the Portuguese that turns '
                            'relocation into daily life.</p>',
                            '<p>Brazilian Portuguese for expats should be practical, cultural and '
                            'live. You need more than grammar explanations. You need a safe space to '
                            'speak, make mistakes, receive correction and understand how Brazilians '
                            'actually communicate.</p>',
                            '<p><strong>Book a free level check with Vedium at <a '
                            'href="/en/portuguese-placement-test">https://vediums.com/</a> and start '
                            'learning Brazilian Portuguese for the life you are about to live in '
                            'Brazil. Live classes, real situations and no long-term contracts — you '
                            'stay because you feel the progress.</strong></p>']}],
     'faqs': [{'q': 'What Portuguese should expats learn before moving to Brazil?',
               'a': 'Expats should first learn greetings, personal information, addresses, '
                    'transportation, housing vocabulary, food, payments, help phrases and basic '
                    'workplace communication. These areas cover the most common situations in the '
                    'first month.'},
              {'q': 'Do I need to be fluent before arriving in Brazil?',
               'a': 'No. You do not need fluency before arrival. You need functional Portuguese: '
                    'enough to ask questions, understand basic answers, introduce yourself, solve '
                    'small problems and feel more confident in daily life.'},
              {'q': 'Is Brazilian Portuguese different from European Portuguese?',
               'a': 'Yes. Brazilian Portuguese has differences in pronunciation, vocabulary, rhythm, '
                    'common expressions and everyday usage. Expats moving to Brazil should focus on '
                    'Brazilian Portuguese because it matches the language they will hear locally.'},
              {'q': 'Are live Portuguese classes better than apps for expats?',
               'a': 'Live classes are better for speaking confidence because they allow correction, '
                    'conversation, role-play and cultural explanation. Apps can help with review, but '
                    'they do not fully prepare you for unpredictable real conversations in Brazil.'},
              {'q': 'How can Vedium help foreigners learn Portuguese for Brazil?',
               'a': 'Vedium offers live online Brazilian Portuguese classes for foreigners, focused on '
                    'practical situations, cultural understanding and real speaking practice. You can '
                    'book a free level check and start from your current level.'}],
     'cta_title': 'Want to know your real Portuguese level?',
     'cta_text': "Take Vedium's free placement test and find out where to start.",
     'cta_label': 'Learn about the Portuguese course',
     'cta_url': '/en/learn-portuguese-brazil'},
    "brazilian-portuguese-for-cultural-adaptation-in-the-first-90-days": {'title': 'Título SEO: Brazilian Portuguese for Cultural Adaptation: Your First 90 Days in Brazil',
     'meta_description': 'Moving to Brazil? Master the Brazilian Portuguese needed for your first 90 '
                         'days. Practical tips, essential vocabulary, and live classes for smooth '
                         'integration.',
     'h1': 'Título SEO: Brazilian Portuguese for Cultural Adaptation: Your First 90 Days in Brazil',
     'date': '2026-06-09',
     'date_display': 'June 9, 2026',
     'hero_image': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aprender português como língua estrangeira',
     'tag': 'Brazilian Portuguese',
     'lang': 'en',
     'category': 'brazilian-portuguese',
     'lead': '',
     'sections': [{'heading': 'The First 90 Days: Why Language is Your Best Cultural Tool',
                   'body': ['<p>If you are reading this, you are likely preparing for one of the most '
                            'exciting transitions of your life: moving to Brazil. Whether for a new '
                            'job, an academic program, or personal relocation, the first 90 days are '
                            'critical. Beyond the logistics of housing and bureaucracy, your ability '
                            'to communicate in Portuguese will be the single greatest factor in how '
                            'quickly you feel "at home."</p>',
                            '<p>Many expats make the mistake of relying solely on English or Spanish, '
                            'assuming they can "get by." While many Brazilians are welcoming, the '
                            'heart of Brazilian culture—the nuance, the warmth, and the professional '
                            'rapport—is locked behind the Portuguese language.</p>',
                            '<p>At <a href="/en/portuguese-placement-test">Vedium</a>, we believe that '
                            'learning a language is not just about grammar; it is about '
                            '<em>Inteligência Cultural</em> (Cultural Intelligence). In these first 90 '
                            "days, you don't just need textbooks; you need a functional, real-world "
                            'command of the language that allows you to navigate daily life with '
                            'confidence.</p>']},
                  {'heading': 'Essential Vocabulary for Survival and Connection',
                   'body': ["<p>When you arrive, you won't need to discuss complex political theories "
                            'immediately. You need the "survival" vocabulary that builds trust.</p>',
                            '<ul><li><strong>Professional Greetings:</strong> "Bom dia," "Boa tarde," '
                            'and "Boa noite" are fundamental. In Brazil, these are not just polite; '
                            'they are the baseline for every interaction.</li><li><strong>The Power of '
                            '\'Como vai?\':</strong> Unlike the cold "How are you?" in some cultures, '
                            '"Tudo bem?" is an invitation to connect. A genuine answer shows you are '
                            'ready to engage.</li><li><strong>Bureaucratic Basics:</strong> Words like '
                            '<em>documento</em>, <em>CPF</em> (the essential tax ID), and '
                            '<em>agendar</em> will be your constant companions. '
                            '</li><li><strong>Navigating Logistics:</strong> Knowing how to ask "Onde '
                            'fica..." (Where is...) or "Como faço para..." (How do I...) at a bank or '
                            'a government office can save you hours of confusion.</li></ul>',
                            "<p><strong>Pro-tip:</strong> Don't memorize lists. Practice these in live "
                            'scenarios. At Vedium, our approach focuses on conversational immersion, '
                            'meaning you practice these exact scenarios with a teacher before you ever '
                            'step foot in a Brazilian office.</p>']},
                  {'heading': '30-60-90 Days: Your Roadmap to Integration',
                   'body': ['<h3>Days 1-30: The Foundation of Independence</h3>',
                            '<p>In the first month, your goal is functional independence. You need to '
                            'handle the supermarket, the pharmacy, and your commute.<br>*   '
                            '<strong>Focus:</strong> Practical commands and basic questions.<br>*   '
                            "<strong>Strategy:</strong> Don't aim for perfection. Aim for clarity. "
                            'When you struggle to find a word, explain the concept in simpler '
                            'terms.<br>*   <strong>Vedium approach:</strong> We help you simulate '
                            'these "first-week" stressors in a safe environment, so when you face the '
                            'real thing, it feels familiar.</p>',
                            '<h3>Days 31-60: The Professional and Social Bridge</h3>',
                            '<p>By the second month, you should be moving toward small talk. This is '
                            'where cultural intelligence kicks in.<br><em>   <strong>Focus:</strong> '
                            'Understanding </em>Jeitinho Brasileiro*—not as a negative, but as a '
                            'flexible way of solving problems.<br>*   <strong>Strategy:</strong> '
                            'Observe social hierarchies in your office. Learn when to use "você" '
                            '(formal/informal) and how to respond to common Brazilian '
                            'colloquialisms.<br><em>   <strong>Vedium approach:</strong> Our live '
                            'classes provide the cultural context that apps miss, explaining not just '
                            '</em>what<em> is said, but </em>why* it is said.</p>',
                            '<h3>Days 61-90: Building Confidence and Community</h3>',
                            '<p>By the end of the third month, you are no longer a tourist; you are a '
                            'participant.<br>*   <strong>Focus:</strong> Expressing your opinions and '
                            'building long-term relationships.<br>*   <strong>Strategy:</strong> Join '
                            'local groups, attend workshops, or simply spend time at local cafes. Use '
                            'your Portuguese to listen more than you speak.<br>*   <strong>Vedium '
                            'approach:</strong> We help you refine your accent and expand your '
                            'vocabulary so that you feel comfortable in professional meetings and '
                            'social gatherings alike.</p>']},
                  {'heading': 'Overcoming the "Expat Barrier" to Fluency',
                   'body': ['<p>The biggest barrier to fluency in Brazil is the "English Trap." '
                            'Because Brazilians are often eager to practice their English with you, '
                            'they will switch languages the moment they detect a hesitation in your '
                            'Portuguese.</p>',
                            '<p>To overcome this:<br>1.  <strong>Be Persistent:</strong> Politely say, '
                            '<em>"Pode continuar em português, por favor? Estou praticando!"</em> (Can '
                            'you continue in Portuguese, please? I am practicing!).<br>2.  '
                            '<strong>Immerse Yourself:</strong> Avoid only interacting with other '
                            'expats.<br>3.  <strong>Invest in Live Training:</strong> Apps are great '
                            'for vocabulary, but they cannot mimic the pressure of a real '
                            'conversation. Vedium offers live, interactive classes where you can '
                            'practice maintaining your Portuguese even when the other person tries to '
                            'switch to English.</p>']},
                  {'heading': 'Why Live Classes Beat Self-Paced Apps',
                   'body': ['<p>If you rely on apps alone, you will learn <em>information</em> but not '
                            '<em>interaction</em>. Learning a language for relocation requires '
                            'immediate feedback. When you mispronounce a word at a government office, '
                            "a 10-minute app session won't help you fix it. A live session with a "
                            'professional teacher will.</p>',
                            "<p>At Vedium, we don't believe in long-term contracts. We believe in "
                            "results. If you aren't evolving, we aren't doing our job. Our students "
                            'stay because they see real progress in their daily interactions, not '
                            'because they are tied down by fine print.</p>']},
                  {'heading': 'Conclusão: Start Your Journey with Vedium',
                   'body': ["<p>Your first 90 days in Brazil will define your long-term success. Don't "
                            "leave your integration to chance or automated apps that don't understand "
                            'the Brazilian context. Equip yourself with the language and cultural '
                            'intelligence to thrive.</p>',
                            '<p><strong>Ready to start?</strong> Ensure your transition is smooth by '
                            'speaking with a professional today. <a '
                            'href="/en/learn-portuguese-brazil">Book a free level check at Vedium</a> '
                            'and see how our live classes can help you master Portuguese for your new '
                            'life in Brazil.</p>']}],
     'faqs': [{'q': 'How long does it take to become functional in Portuguese?',
               'a': 'With consistent, live classes, most students reach a functional level for daily '
                    'life within 3 to 6 months. Our focus is on prioritizing high-frequency vocabulary '
                    'to get you talking faster.'},
              {'q': 'Is it hard to learn Portuguese if I already speak Spanish?',
               'a': 'They are related, but different. While Spanish helps with vocabulary, the '
                    'pronunciation and grammar structures in Portuguese are distinct. Our teachers '
                    'help you bridge that gap without confusing the two languages.'},
              {'q': 'Do I need to know grammar rules to live in Brazil?',
               'a': 'Not immediately. You need communication skills. We prioritize the "language of '
                    'action"—giving you the phrases you need to get things done—and layer in the '
                    'grammar as you advance.'},
              {'q': 'Why choose live classes over self-paced apps?',
               'a': 'Apps lack the feedback loop necessary for social and professional integration. In '
                    'a live class, you practice the <em>real</em> conversations you will have in '
                    'Brazil, including local slang and cultural nuances.'},
              {'q': 'Does Vedium offer classes for professional or corporate use?',
               'a': 'Yes. Whether you need Portuguese for work or personal life, our classes are '
                    'personalized to your goals. We focus on the "Cultural Intelligence" required to '
                    'succeed in the Brazilian business environment.'}],
     'cta_title': 'Want to know your real Portuguese level?',
     'cta_text': "Take Vedium's free placement test and find out where to start.",
     'cta_label': 'Learn about the Portuguese course',
     'cta_url': '/en/learn-portuguese-brazil'},
    "portuguese-for-everyday-bureaucracy-in-brazil": {'title': 'Portuguese for everyday bureaucracy in Brazil: Your survival guide',
     'meta_description': 'Navigating Brazilian bureaucracy as an expat? Master the essential '
                         'Portuguese phrases to handle daily tasks and live in Brazil with confidence.',
     'h1': 'Portuguese for everyday bureaucracy in Brazil: Your survival guide',
     'date': '2026-05-26',
     'date_display': 'May 26, 2026',
     'hero_image': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aprender português como língua estrangeira',
     'tag': 'Brazilian Portuguese',
     'lang': 'en',
     'category': 'brazilian-portuguese',
     'lead': '',
     'sections': [{'heading': 'Mastering Brazilian Bureaucracy: Why Language is Your Primary Tool',
                   'body': ['<p>Moving to a new country is an exhilarating experience, but for anyone '
                            'relocating to Brazil, the word "bureaucracy" (<em>burocracia</em>) often '
                            'triggers a sense of unease. Whether you are dealing with opening a bank '
                            'account, setting up utilities, or navigating tax requirements at the '
                            '<em>Receita Federal</em>, the administrative hurdles can be daunting.</p>',
                            '<p>For the expat, the challenge is twofold: understanding the complex '
                            'requirements and communicating them in a language that is not your own. '
                            'At <a href="/en/portuguese-placement-test">Vedium</a>, we view this not '
                            'just as a hurdle, but as a critical component of your cultural '
                            'integration. Understanding how to handle your own affairs is the fastest '
                            'route to true autonomy in your new home. Our approach to <em>Português '
                            'para Estrangeiros</em> focuses on <strong>Inteligência '
                            'Cultural</strong>—giving you the functional language you need to resolve '
                            'real-life problems efficiently, without relying on intermediaries or '
                            'costly translation services.</p>']},
                  {'heading': 'Why "Burocracia" Traps the Expats',
                   'body': ["<p>The main reason expats struggle with Brazilian bureaucracy isn't just "
                            'the paperwork; it\'s the lack of "functional fluency." Many learners '
                            'spend months on apps mastering abstract vocabulary like "the apple is '
                            'red" or "the boy plays soccer." While valid, this does not prepare you '
                            'for a tense moment at a utility office or a confusing conversation at a '
                            'bank.</p>',
                            "<p>When you don't understand the specific social and professional scripts "
                            'used in Brazilian administrative offices, you lose confidence. You '
                            'hesitate, you ask for English speakers—who may not be available—and you '
                            'become dependent. We believe that your autonomy starts with your ability '
                            'to articulate your needs clearly in Portuguese. This is where live, '
                            'interactive classes make the difference: we simulate these high-pressure '
                            'bureaucratic scenarios so that when you arrive at a desk, you already '
                            'know the flow of the conversation and the vocabulary required to get '
                            'things done.</p>']},
                  {'heading': 'Essential Vocabulary for Administrative Independence',
                   'body': ['<p>You do not need to be a lawyer to handle your daily affairs, but you '
                            'do need the "language of action." Here are the pillars of the vocabulary '
                            'you will need:</p>',
                            '<ul><li><strong>Documents and Identification:</strong> Understanding '
                            '<em>CPF</em> (your tax ID, the most important document in Brazil), '
                            '<em>RG</em> (general identity), and <em>comprovante de residência</em> '
                            '(proof of residence) is fundamental. You will be asked for these '
                            'constantly.</li><li><strong>The Power of Asking:</strong> Knowing how to '
                            'ask "Quais documentos são necessários?" (Which documents are necessary?) '
                            'or "Onde posso protocolar este pedido?" (Where can I file this request?) '
                            'transforms you from a confused observer into an active manager of your '
                            'own life.</li><li><strong>Navigation Terms:</strong> Phrases like '
                            '<em>agendar</em> (to schedule), <em>atendimento</em> '
                            '(service/assistance), and <em>prazo</em> (deadline) are vital. Knowing '
                            'when a deadline is strict or when there is flexibility is part of '
                            'understanding the Brazilian context.</li></ul>',
                            "<p><strong>Pro-tip:</strong> Don't memorize lists; memorize interactions. "
                            'At Vedium, we focus on conversational immersion, helping you practice '
                            'these interactions with a teacher who provides immediate feedback on your '
                            'tone and clarity.</p>']},
                  {'heading': 'Your Roadmap to Mastering Bureaucratic Interactions',
                   'body': ['<h3>Step 1: Preparation (Pre-meeting)</h3>',
                            '<p>Before you even step into an office, you must know what you need. '
                            'Brazilians are helpful, but you must be prepared to be helped.<br>*   '
                            '<strong>The Strategy:</strong> Always have a checklist in Portuguese. If '
                            'you are going to a phone company to change your plan, have your contract '
                            'number and document copies ready and listed in your language '
                            'notes.<br>*   <strong>Vedium approach:</strong> We help you prepare these '
                            '"checklists of communication," teaching you how to phrase your requests '
                            'so you are taken seriously from the moment you speak.</p>',
                            '<h3>Step 2: The Interaction (During the meeting)</h3>',
                            '<p>This is where cultural intelligence is key. Politeness '
                            '(<em>educação</em>) is the lubricant of Brazilian interactions.<br>*   '
                            '<strong>The Strategy:</strong> Start with a polite greeting. "Bom dia, '
                            'tudo bem?" is more than a greeting; it’s a necessary social entry point. '
                            'Use polite requests: "Poderia me informar..." instead of '
                            '"Quero...".<br>*   <strong>Vedium approach:</strong> We teach you how to '
                            'manage the tone of your conversation, ensuring you remain polite yet '
                            'assertive enough to ensure your problem is resolved.</p>',
                            '<h3>Step 3: Resolution (Closing the loop)</h3>',
                            '<p>Never leave an office without confirming the next steps.<br>*   '
                            '<strong>The Strategy:</strong> Always ask "Qual é o próximo passo?" (What '
                            'is the next step?) and "Quanto tempo demora?" (How long does it '
                            'take?).<br>*   <strong>Vedium approach:</strong> Our live sessions '
                            'simulate the closing of these interactions, ensuring you leave with the '
                            'clarity you need to avoid repeat visits.</p>']},
                  {'heading': 'Why Live Classes Beat Self-Paced Apps',
                   'body': ['<p>Apps are excellent for passive learning, but they are disastrous for '
                            'active administrative survival. When you are in a line at a government '
                            "office and the clerk uses an idiom you don't understand, an app cannot "
                            'help you. A live teacher, however, can explain the nuance, suggest an '
                            'alternative way to ask the question, and help you regain your '
                            'footing.</p>',
                            "<p>At Vedium, we don't believe in long-term contracts. We believe in "
                            "results. If you aren't evolving, we aren't doing our job. Our students "
                            'stay because they see real progress in their daily interactions, not '
                            'because they are tied down by fine print. You want to live your life in '
                            'Brazil, not struggle through it—and we are here to ensure that '
                            'happens.</p>']},
                  {'heading': 'Overcoming the "Expat Barrier" to Fluency',
                   'body': ['<p>The biggest barrier to fluency in Brazil is the "English Trap." '
                            'Because Brazilians are often eager to practice their English, they will '
                            'switch languages the moment they detect a hesitation in your '
                            'Portuguese.</p>',
                            '<p>To overcome this:<br>1.  <strong>Be Persistent:</strong> Politely say, '
                            '<em>"Pode continuar em português, por favor? Estou praticando!"</em> (Can '
                            'you continue in Portuguese, please? I am practicing!).<br>2.  '
                            '<strong>Immerse Yourself:</strong> The more you use Portuguese for the '
                            '"hard" things, the faster your brain will adapt.<br>3.  <strong>Invest in '
                            'Live Training:</strong> Vedium offers live, interactive classes where you '
                            'can practice maintaining your Portuguese even when the other person tries '
                            'to switch to English. This is the ultimate "gym" for your language '
                            'skills.</p>']},
                  {'heading': 'Conclusion: Take Control of Your Life in Brazil',
                   'body': ["<p>Bureaucracy doesn't have to be the most stressful part of your life in "
                            'Brazil. By treating it as a language-learning opportunity and equipping '
                            'yourself with the right functional vocabulary and cultural intelligence, '
                            'you can turn these obstacles into stepping stones for your '
                            'independence.</p>',
                            "<p>Don't leave your integration to chance or automated apps that don't "
                            'understand the Brazilian context. Equip yourself with the language and '
                            'cultural intelligence to thrive.</p>',
                            '<p><strong>Ready to start?</strong> Gain the autonomy you deserve. <a '
                            'href="/en/learn-portuguese-brazil">Book a free level check at Vedium</a> '
                            'and see how our live classes can help you master the Portuguese you need '
                            'to handle your life in Brazil with ease.</p>']}],
     'faqs': [{'q': 'How long does it take to become functional in Portuguese for daily tasks?',
               'a': 'With consistent, live classes, most students reach a functional level for daily '
                    'administrative tasks within 3 to 6 months. Our focus is on prioritizing '
                    'high-frequency vocabulary to get you talking and resolving issues faster.'},
              {'q': 'Is it hard to learn Portuguese if I already speak another Latin language?',
               'a': 'While your previous language helps with vocabulary, the pronunciation and grammar '
                    'structures in Portuguese are distinct. Our teachers help you bridge that gap, '
                    'focusing on the specific "Brazilian" way of saying things to ensure you don\'t '
                    'develop bad habits.'},
              {'q': 'Do I need to know formal grammar rules to handle bureaucracy?',
               'a': 'Not immediately. You need functional communication skills. We prioritize the '
                    '"language of action"—giving you the phrases you need to get things done—and layer '
                    'in the formal grammar as you advance.'},
              {'q': 'Why choose live classes over self-paced apps?',
               'a': 'Apps lack the feedback loop necessary for navigating real-world social and '
                    'professional stressors. In a live class, you practice the <em>real</em> '
                    'conversations you will have in Brazil, including the cultural nuances that '
                    'determine whether you get a "yes" or a "no" at the counter.'},
              {'q': 'Does Vedium offer classes for professional or corporate use?',
               'a': 'Yes. Whether you need Portuguese for work, managing your personal life, or '
                    'handling complex administrative tasks, our classes are personalized to your '
                    'goals. We focus on the "Cultural Intelligence" required to succeed in the '
                    'Brazilian environment.'}],
     'cta_title': 'Want to know your real Portuguese level?',
     'cta_text': "Take Vedium's free placement test and find out where to start.",
     'cta_label': 'Learn about the Portuguese course',
     'cta_url': '/en/learn-portuguese-brazil'},
    "how-to-sound-natural-when-saying-yes-no-and-maybe-in-portuguese": {'title': 'How to sound natural when saying yes, no and maybe in Portuguese',
     'meta_description': 'Moving to Brazil? Learn how to sound natural when saying yes, no, and maybe '
                         'in Portuguese. Master cultural nuance and build confidence with Vedium.',
     'h1': 'How to sound natural when saying yes, no and maybe in Portuguese',
     'date': '2026-06-02',
     'date_display': 'June 2, 2026',
     'hero_image': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aprender português como língua estrangeira',
     'tag': 'Brazilian Portuguese',
     'lang': 'en',
     'category': 'brazilian-portuguese',
     'lead': '',
     'sections': [{'heading': 'Mastering the Nuance: Beyond Literal Translations in Portuguese',
                   'body': ['<p>When you are an expat in Brazil, learning "yes," "no," and "maybe" '
                            'seems like the easiest part of the journey. After all, "sim," "não," and '
                            '"talvez" are among the first words any beginner learns. However, the true '
                            'challenge arises when you realize that in Brazilian Portuguese, these '
                            'words are rarely used in isolation. To sound natural—and more '
                            'importantly, to avoid misunderstandings—you must master the cultural '
                            'nuance behind how Brazilians use these simple affirmations and '
                            'negations.</p>',
                            '<p>At <a href="/en/portuguese-placement-test">Vedium</a>, we know that '
                            'language is not just about vocabulary; it is about <em>Inteligência '
                            'Cultural</em> (Cultural Intelligence). When you navigate the professional '
                            'or social world in Brazil, saying "no" too directly can seem abrasive, '
                            'while saying "yes" without qualification can lead to unrealistic '
                            'expectations. This guide will help you understand the context so you can '
                            'integrate smoothly and speak with the confidence of a local.</p>']},
                  {'heading': 'Why Saying "Yes", "No" and "Maybe" is Difficult for Expats',
                   'body': ["<p>The difficulty isn't the words themselves; it’s the cultural context. "
                            'In many Western cultures, a "no" is seen as a clear, definitive boundary. '
                            'In Brazil, the way a "no" is delivered is often softened to preserve '
                            'social harmony. If you are a foreigner, you might find yourself confused '
                            'when someone says "talvez" (maybe) to a request, when in reality, they '
                            'might mean "no."</p>',
                            '<p>Conversely, when you want to say "yes," a simple "sim" might sound '
                            'robotic. Brazilians frequently use repetition, idiomatic expressions, and '
                            "even body language to convey their intent. If you don't grasp these "
                            'subtleties, you risk appearing distant or misunderstood. This is where '
                            "live, interactive language classes become essential. At Vedium, we don't "
                            'just teach you the dictionary definition; we teach you the <em>real</em> '
                            'usage, ensuring you have the confidence to navigate these social and '
                            'professional interactions without fear.</p>']},
                  {'heading': 'The Art of "Yes": More Than Just Affirmation',
                   'body': ['<p>In Portuguese, "sim" is the baseline, but to sound natural, you should '
                            'adapt your response based on the context.</p>',
                            '<ul><li><strong>Confirming Understanding:</strong> Instead of just saying '
                            '"sim," Brazilians often use phrases like "Com certeza" (For sure) or '
                            '"Claro" (Of course) to emphasize agreement.</li><li><strong>Professional '
                            'Contexts:</strong> In a business setting, using "Pois não" (which '
                            'actually means "how can I help you?" or "certainly," rather than "of '
                            'course not") is a crucial skill to '
                            'distinguish.</li><li><strong>Enthusiasm:</strong> Brazilians value '
                            'warmth. Adding a positive spin to your "yes"—like "Com certeza, vamos '
                            'fazer isso!" (For sure, let\'s do this!)—builds a much stronger '
                            'connection than a curt "sim."</li></ul>',
                            '<p><strong>Practical Exercise:</strong> Next time you are in a situation '
                            'where you agree with someone, try using "Claro que sim" or "Pois não." '
                            'Pay attention to the reaction you get; you will likely notice a warmer, '
                            'more engaged response from your interlocutor.</p>']},
                  {'heading': 'Navigating the "No": Maintaining Harmony',
                   'body': ['<p>"Não" is a powerful word, but in Brazil, it is often wrapped in layers '
                            'of polite cushioning. Using a blunt "não" can sometimes be perceived as '
                            'rude, especially in professional environments or when dealing with '
                            'clients.</p>',
                            '<ul><li><strong>Softening the Blow:</strong> Brazilians often say '
                            '"olha..." (look...) before stating a negative, or they might explain the '
                            '<em>reason</em> for the "no" before actually saying the '
                            'word.</li><li><strong>The "Talvez" (Maybe) Trap:</strong> Often, "talvez" '
                            'is used as a polite way to avoid a direct confrontation. Recognizing this '
                            'is part of your cultural intelligence journey.</li><li><strong>Polite '
                            'Alternatives:</strong> Instead of just saying "não," you might hear '
                            '"infelizmente, não posso" (unfortunately, I cannot) or "quem sabe em '
                            'outra oportunidade" (maybe another time).</li></ul>',
                            '<p>At Vedium, our teachers specialize in helping you practice these '
                            'social scripts. You will practice the scenarios in a live class '
                            'environment, allowing you to fine-tune your tone so that your "no" is '
                            'firm but respectful, maintaining the professional relationships you need '
                            'to succeed.</p>']},
                  {'heading': 'When "Maybe" Means Everything',
                   'body': ['<p>"Talvez" is perhaps the most nuanced word in the Brazilian vocabulary. '
                            'It can range from a genuine uncertainty to a polite decline. Learning to '
                            'read the context is key.</p>',
                            '<ul><li><strong>Reading the Context:</strong> If you ask a colleague for '
                            'a report and they say "talvez," observe their tone. Are they smiling? Are '
                            'they rushing? The tone often tells you more than the word '
                            'itself.</li><li><strong>Mastering the Ambiguity:</strong> As a foreigner, '
                            'you can use "talvez" to buy yourself time or to soften a request. '
                            'Learning the right moment to use it will make you sound infinitely more '
                            'native.</li></ul>']},
                  {'heading': 'Why Live Classes are the Best Path to Fluency',
                   'body': ['<p>If you rely on self-paced apps, you will never get feedback on your '
                            'tone, body language, or the "vibe" of your speech. You might learn that '
                            '"sim" means "yes," but you won\'t learn <em>when</em> to use "pois não" '
                            'or how to soften a "não" to keep your boss happy.</p>',
                            '<p>Vedium is designed for people who want results, not just hours of '
                            'screen time. Our live classes focus on the conversational immersion that '
                            "is strictly required to master cultural nuances. Because we don't hold "
                            'you to long-term contracts, we rely on the quality of our teaching to '
                            'keep you motivated. Our students stay because they see their real-world '
                            'interactions improve, week after week.</p>']},
                  {'heading': 'Overcoming the "Expat Barrier"',
                   'body': ['<p>The most significant barrier to sounding natural is the "English '
                            'Trap." Because Brazilians are friendly, they will often switch to English '
                            'as soon as they hear your accent. To truly sound natural, you have to be '
                            'persistent.</p>',
                            '<ol><li><strong>Be Assertive:</strong> Politely insist in Portuguese: '
                            '<em>"Desculpa, eu prefiro praticar em português."</em> (Sorry, I prefer '
                            'to practice in Portuguese).</li><li><strong>Practice Scenarios:</strong> '
                            'Use your Vedium classes to simulate these exact moments where you must '
                            "maintain your Portuguese despite the other person's urge to switch "
                            'languages.</li><li><strong>Cultural Intelligence:</strong> Understand '
                            'that the switch to English is a gesture of kindness, not an insult to '
                            'your Portuguese. Acknowledging this and responding kindly in Portuguese '
                            'will earn you immense respect.</li></ol>']},
                  {'heading': 'Conclusion: Start Your Journey with Vedium',
                   'body': ['<p>Sounding natural when saying "yes," "no," and "maybe" is just the '
                            'beginning of your integration into Brazil. Whether you are living, '
                            'working, or studying here, the ability to navigate these cultural '
                            "subtleties will define your success. Don't leave your integration to "
                            'automated apps that lack the human element.</p>',
                            '<p><strong>Ready to start?</strong> Gain the cultural intelligence and '
                            'the language skills you need to thrive in Brazil. <a '
                            'href="/en/learn-portuguese-brazil">Book a free level check at Vedium</a> '
                            'and discover how our live, personalized methodology can help you move '
                            'beyond the dictionary and into real, natural fluency.</p>']}],
     'faqs': [{'q': 'How long does it take to learn the cultural nuances of Portuguese?',
               'a': 'While it varies, most students start feeling comfortable with these nuances '
                    'within 3 to 6 months of consistent, live practice. Our methodology focuses on '
                    'high-frequency scenarios to accelerate this process.'},
              {'q': 'Is it rude to say "não" directly in Brazil?',
               'a': 'It is not necessarily rude, but it can be perceived as overly blunt depending on '
                    'the relationship. Brazilians value maintaining social harmony, so learning to '
                    'soften your "no" is a valuable skill for professional success.'},
              {'q': 'Why do Brazilians switch to English when I speak Portuguese?',
               'a': 'It is usually a sign of hospitality and an attempt to make you comfortable. They '
                    'are trying to be helpful, so maintain a positive attitude, thank them, and '
                    'politely ask to continue in Portuguese.'},
              {'q': 'How does Vedium help me sound more natural?',
               'a': 'By focusing on live interaction, our teachers provide real-time feedback on your '
                    'intonation, the context of your word choices, and the cultural appropriateness of '
                    'your sentences, which apps cannot replicate.'},
              {'q': 'Do I need to learn complex grammar to sound natural?',
               'a': 'Not necessarily. You need to focus on functional phrases and cultural context. We '
                    'prioritize the language you actually use in daily life, integrating grammar rules '
                    'as your confidence grows.'}],
     'cta_title': 'Want to know your real Portuguese level?',
     'cta_text': "Take Vedium's free placement test and find out where to start.",
     'cta_label': 'Learn about the Portuguese course',
     'cta_url': '/en/learn-portuguese-brazil'},
    "how-to-ask-better-questions-in-brazilian-portuguese": {'title': 'How to ask better questions in Brazilian Portuguese',
     'meta_description': 'Learn how to ask better questions in Brazilian Portuguese for work, study '
                         'and daily life in Brazil, with practical examples.',
     'h1': 'How to ask better questions in Brazilian Portuguese',
     'date': '2026-06-30',
     'date_display': 'June 30, 2026',
     'hero_image': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aprender português como língua estrangeira',
     'tag': 'Brazilian Portuguese',
     'lang': 'en',
     'category': 'brazilian-portuguese',
     'lead': 'Asking better questions in Brazilian Portuguese means learning more than question words. '
             'You need to understand real Brazilian phrasing, polite tone, informal shortcuts, '
             'workplace expectations and how people actually respond in daily life. For foreigners '
             'living, working or studying in Brazil, questions are survival tools: they help you solve '
             'problems, make friends, understand instructions and participate with confidence.',
     'sections': [{'heading': '',
                   'body': ['<p>Many learners start with “what”, “where”, “when” and “how much.” That '
                            'is a good beginning, but it is not enough for real life in Brazil. You '
                            'also need to ask follow-up questions, confirm information, ask for '
                            'repetition, sound polite without being too formal, and understand short '
                            'answers like “pode ser”, “pois não”, “fica tranquilo”, “combinado” and '
                            '“já já.”</p>',
                            '<p>This guide shows how to ask better questions in Brazilian Portuguese, '
                            'with practical examples for expats, international students and '
                            'professionals. You will learn essential question words, common '
                            'structures, real-life phrases and when live Portuguese classes can help '
                            'you sound more natural.</p>']},
                  {'heading': 'Why asking questions is one of the most important skills in Brazilian '
                              'Portuguese',
                   'body': ['<p>Asking questions is essential because it turns passive vocabulary into '
                            'real interaction. When you can ask clear questions, you are no longer '
                            'waiting for perfect fluency before participating. You can start solving '
                            'daily situations immediately.</p>',
                            '<p>For foreigners in Brazil, questions appear everywhere:</p>',
                            '<ul><li>at the airport;</li><li>in an apartment building;</li><li>with an '
                            'Uber or taxi driver;</li><li>at restaurants and cafés;</li><li>at '
                            'pharmacies and clinics;</li><li>in banks and service desks;</li><li>at '
                            'universities;</li><li>in meetings;</li><li>with coworkers;</li><li>with '
                            'neighbors;</li><li>in WhatsApp conversations.</li></ul>',
                            '<p>The problem is that many learners know isolated vocabulary but freeze '
                            'when they need to ask something spontaneously. They may know the word '
                            '“address”, but not how to ask “Could you confirm the address?” They may '
                            'know “meeting”, but not how to ask “What time does the meeting start?” '
                            'They may know “repeat”, but not how to say “Could you say that more '
                            'slowly?”</p>',
                            '<p>Better questions give you independence. They also show respect. In '
                            'Brazil, communication is often relational. People may appreciate when you '
                            'try to speak Portuguese, even if your sentence is not perfect. A '
                            'well-formed, polite question can open doors and reduce anxiety.</p>',
                            '<p>At Vedium, Brazilian Portuguese for foreigners is taught through live '
                            'classes because asking questions requires real-time practice. You need to '
                            'hear answers, react, clarify and receive correction. That is difficult to '
                            'master only with apps or recorded lessons.</p>',
                            '<p>CTA: If you want to speak Portuguese with more confidence in Brazil, '
                            'book a free level check at <a '
                            'href="/en/learn-portuguese-brazil">https://vediums.com/</a> and discover '
                            'your starting point.</p>']},
                  {'heading': 'The basic question words in Brazilian Portuguese',
                   'body': ['<p>The first step is to learn the main question words. These words help '
                            'you ask for information quickly and clearly.</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portuguese</th><th>English</th><th>Example</th></tr></thead><tbody><tr><td>O '
                            'que?</td><td>What?</td><td>O que significa '
                            'isso?</td></tr><tr><td>Quem?</td><td>Who?</td><td>Quem é o '
                            'responsável?</td></tr><tr><td>Onde?</td><td>Where?</td><td>Onde fica a '
                            'entrada?</td></tr><tr><td>Quando?</td><td>When?</td><td>Quando começa a '
                            'aula?</td></tr><tr><td>Como?</td><td>How?</td><td>Como eu faço '
                            'isso?</td></tr><tr><td>Quanto? / Quantos?</td><td>How much? / How '
                            'many?</td><td>Quanto custa?</td></tr><tr><td>Qual? / '
                            'Quais?</td><td>Which? / What?</td><td>Qual é o seu '
                            'nome?</td></tr><tr><td>Por quê?</td><td>Why?</td><td>Por que '
                            'mudou?</td></tr></tbody></table>',
                            '<p>These words are simple, but they become powerful when you use them in '
                            'real situations. Notice that Brazilian Portuguese questions often sound '
                            'natural with small supporting words like “é que”, “mesmo”, “aqui”, “por '
                            'favor” and “você sabe”.</p>',
                            '<p>For example:</p>',
                            '<ul><li>“Onde fica o banheiro?” — Where is the bathroom?</li><li>“Quanto '
                            'custa?” — How much is it?</li><li>“Como eu faço para chegar lá?” — How do '
                            'I get there?</li><li>“Qual é o melhor horário?” — What is the best '
                            'time?</li><li>“Você sabe onde fica a recepção?” — Do you know where the '
                            'reception is?</li></ul>',
                            '<p>The phrase “Você sabe...” is especially useful. It softens the '
                            'question and makes it sound natural: “Você sabe onde fica...?” means “Do '
                            'you know where... is?”</p>']},
                  {'heading': 'How to ask polite questions without sounding too formal',
                   'body': ['<p>To ask polite questions in Brazilian Portuguese, use “por favor”, '
                            '“você pode”, “poderia” and a friendly tone. Brazilian politeness often '
                            'depends not only on words, but also on warmth, facial expression and '
                            'context.</p>',
                            '<p>A question can be grammatically correct and still sound abrupt if it '
                            'is too direct. For example, “Onde é?” may work in some informal moments, '
                            'but “Você sabe onde fica, por favor?” sounds more polite and '
                            'complete.</p>',
                            '<p>Here are useful polite structures:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Structure</th><th>Meaning</th><th>Example</th></tr></thead><tbody><tr><td>Você '
                            'pode...?</td><td>Can you...?</td><td>Você pode repetir, por '
                            'favor?</td></tr><tr><td>Você sabe...?</td><td>Do you '
                            'know...?</td><td>Você sabe onde fica o '
                            'metrô?</td></tr><tr><td>Poderia...?</td><td>Could you...?</td><td>Poderia '
                            'me ajudar?</td></tr><tr><td>Eu gostaria de saber...</td><td>I would like '
                            'to know...</td><td>Eu gostaria de saber o horário.</td></tr><tr><td>Será '
                            'que...?</td><td>Would it be possible...?</td><td>Será que você pode me '
                            'explicar?</td></tr></tbody></table>',
                            '<p>“Será que...” is very common in Brazil. It does not translate '
                            'perfectly into English, but it softens a request. It can make a question '
                            'sound less demanding.</p>',
                            '<p>Examples:</p>',
                            '<ul><li>“Será que você pode repetir?” — Could you maybe repeat '
                            'that?</li><li>“Será que dá para pagar com cartão?” — Is it possible to '
                            'pay by card?</li><li>“Será que você sabe onde fica a sala?” — Do you '
                            'happen to know where the room is?</li></ul>',
                            '<p>For expats, this is important because direct translations from English '
                            'can sound too blunt. In English, “Can you help me?” is normal. In '
                            'Brazilian Portuguese, “Você pode me ajudar, por favor?” or “Será que você '
                            'pode me ajudar?” often sounds warmer.</p>']},
                  {'heading': 'Real-life questions for daily life in Brazil',
                   'body': ['<p>For daily life in Brazil, you need questions that help you move, buy, '
                            'schedule, confirm and solve small problems. These are the questions that '
                            'give you independence in your first weeks.</p>',
                            '<h3>At a restaurant or café</h3>',
                            '<p>Use these questions to order and clarify:</p>',
                            '<ul><li>“Tem mesa para duas pessoas?” — Do you have a table for '
                            'two?</li><li>“Qual é o prato do dia?” — What is the dish of the '
                            'day?</li><li>“Esse prato tem carne?” — Does this dish have '
                            'meat?</li><li>“Posso pedir sem cebola?” — Can I order it without '
                            'onion?</li><li>“A conta, por favor?” — The bill, please?</li><li>“Aceita '
                            'cartão?” — Do you accept cards?</li></ul>',
                            '<p>In Brazil, “aceita cartão?” is extremely practical. You may also hear '
                            '“débito ou crédito?” when paying.</p>',
                            '<h3>In an apartment building</h3>',
                            '<p>Many expats interact with building staff, landlords, maintenance teams '
                            'and neighbors. Useful questions include:</p>',
                            '<ul><li>“Você sabe se chegou uma entrega para mim?” — Do you know if a '
                            'delivery arrived for me?</li><li>“Com quem eu falo sobre manutenção?” — '
                            'Who do I talk to about maintenance?</li><li>“Pode me avisar quando o '
                            'técnico chegar?” — Can you let me know when the technician '
                            'arrives?</li><li>“Onde fica a lixeira?” — Where is the trash '
                            'area?</li><li>“Qual é o horário permitido para mudança?” — What is the '
                            'allowed time for moving?</li></ul>',
                            '<p>These questions are not only linguistic. They help you understand '
                            'Brazilian apartment culture, building rules and daily logistics.</p>',
                            '<h3>In transport</h3>',
                            '<p>For taxis, buses, metro and ride apps, learn:</p>',
                            '<ul><li>“Esse ônibus vai para o centro?” — Does this bus go '
                            'downtown?</li><li>“Quanto tempo demora?” — How long does it '
                            'take?</li><li>“Pode me deixar aqui, por favor?” — Can you drop me off '
                            'here, please?</li><li>“Este é o melhor caminho?” — Is this the best '
                            'route?</li><li>“Onde eu pego o metrô?” — Where do I take the '
                            'metro?</li></ul>',
                            '<p>Brazilian cities can be busy and unpredictable. Clear questions reduce '
                            'stress.</p>',
                            '<h3>At a pharmacy or clinic</h3>',
                            '<p>Health-related questions are essential:</p>',
                            '<ul><li>“Preciso de receita?” — Do I need a prescription?</li><li>“Como '
                            'eu tomo esse remédio?” — How do I take this medicine?</li><li>“Tem algum '
                            'genérico?” — Is there a generic version?</li><li>“Vocês aceitam meu '
                            'seguro?” — Do you accept my insurance?</li><li>“Qual é o horário de '
                            'atendimento?” — What are the opening hours?</li></ul>',
                            '<p>If you are not confident, you can add:</p>',
                            '<ul><li>“Meu português ainda é básico.” — My Portuguese is still '
                            'basic.</li><li>“Pode falar mais devagar, por favor?” — Can you speak more '
                            'slowly, please?</li></ul>',
                            '<p>These phrases help people adjust their speech without making you feel '
                            'embarrassed.</p>']},
                  {'heading': 'Questions for work and study in Brazil',
                   'body': ['<p>At work or university, better questions help you participate, clarify '
                            'expectations and avoid misunderstandings. You do not need perfect '
                            'Portuguese to communicate professionally. You need clear, respectful and '
                            'useful questions.</p>',
                            '<h3>In meetings</h3>',
                            '<p>Use questions like:</p>',
                            '<ul><li>“Você pode explicar esse ponto de novo?” — Can you explain this '
                            'point again?</li><li>“Qual é o prazo?” — What is the '
                            'deadline?</li><li>“Quem vai ficar responsável por isso?” — Who will be '
                            'responsible for this?</li><li>“O que eu preciso entregar?” — What do I '
                            'need to deliver?</li><li>“Podemos alinhar os próximos passos?” — Can we '
                            'align the next steps?</li><li>“Só para confirmar, a reunião é às três?” — '
                            'Just to confirm, is the meeting at three?</li></ul>',
                            '<p>“Só para confirmar...” is one of the most useful phrases in '
                            'professional Brazilian Portuguese. It is polite, natural and helps '
                            'prevent mistakes.</p>',
                            '<h3>At university or in class</h3>',
                            '<p>International students can use:</p>',
                            '<ul><li>“Quando é a entrega do trabalho?” — When is the assignment '
                            'due?</li><li>“Pode repetir a explicação?” — Can you repeat the '
                            'explanation?</li><li>“Esse conteúdo vai cair na prova?” — Will this '
                            'content be on the test?</li><li>“Posso entregar por e-mail?” — Can I '
                            'submit it by email?</li><li>“Onde encontro o material da aula?” — Where '
                            'can I find the class material?</li></ul>',
                            '<h3>With coworkers</h3>',
                            '<p>Workplace small talk is also part of communication:</p>',
                            '<ul><li>“Como foi o fim de semana?” — How was your weekend?</li><li>“Você '
                            'trabalha em qual área?” — Which area do you work in?</li><li>“Você sabe '
                            'quem pode me ajudar com isso?” — Do you know who can help me with '
                            'this?</li><li>“Vamos marcar um café?” — Shall we schedule a '
                            'coffee?</li><li>“Você prefere falar por e-mail ou WhatsApp?” — Do you '
                            'prefer email or WhatsApp?</li></ul>',
                            '<p>In Brazil, relationship-building often matters. Asking friendly '
                            'questions can help you integrate into teams.</p>']},
                  {'heading': 'How to ask follow-up questions naturally',
                   'body': ['<p>Follow-up questions are what make conversations feel real. Without '
                            'them, you may ask one question, receive an answer and stop. With '
                            'follow-up questions, you show interest and keep the interaction '
                            'going.</p>',
                            '<p>Useful follow-up phrases include:</p>',
                            '<ul><li>“Como assim?” — What do you mean?</li><li>“Pode me dar um '
                            'exemplo?” — Can you give me an example?</li><li>“E depois?” — And after '
                            'that?</li><li>“O que você recomenda?” — What do you '
                            'recommend?</li><li>“Por quê?” — Why?</li><li>“Tem outra opção?” — Is '
                            'there another option?</li><li>“Isso é comum no Brasil?” — Is this common '
                            'in Brazil?</li></ul>',
                            '<p>“Como assim?” is very common, but tone matters. It can sound curious, '
                            'surprised or confused depending on how you say it. In live Portuguese '
                            'classes, you can practice these differences with a teacher.</p>',
                            '<p>Follow-up questions are especially useful when you are learning '
                            'culture, not only vocabulary. For example, if someone tells you that a '
                            'certain document is necessary, you can ask:</p>',
                            '<ul><li>“Onde eu faço isso?”</li><li>“Precisa agendar?”</li><li>“Quanto '
                            'tempo demora?”</li><li>“Tem que levar algum documento?”</li><li>“Isso '
                            'pode ser feito online?”</li></ul>',
                            '<p>These questions help you solve real tasks in Brazil.</p>']},
                  {'heading': 'How to ask someone to repeat or slow down',
                   'body': ['<p>To ask someone to repeat or slow down, use direct but polite phrases. '
                            'This is one of the most important survival skills for foreigners in '
                            'Brazil.</p>',
                            '<p>Learn these phrases early:</p>',
                            '<ul><li>“Pode repetir, por favor?” — Can you repeat, '
                            'please?</li><li>“Pode falar mais devagar?” — Can you speak more '
                            'slowly?</li><li>“Desculpa, não entendi.” — Sorry, I did not '
                            'understand.</li><li>“Como se escreve?” — How do you spell it?</li><li>“O '
                            'que significa essa palavra?” — What does this word mean?</li><li>“Você '
                            'pode explicar de outro jeito?” — Can you explain it another '
                            'way?</li></ul>',
                            '<p>Do not be afraid to say you are learning. Many Brazilians will adjust '
                            'when they understand your level.</p>',
                            '<p>You can say:</p>',
                            '<ul><li>“Estou aprendendo português.”</li><li>“Meu português ainda é '
                            'básico.”</li><li>“Pode falar um pouco mais devagar?”</li><li>“Eu entendo '
                            'melhor quando você fala devagar.”</li></ul>',
                            '<p>These phrases reduce pressure and make the conversation more '
                            'collaborative.</p>']},
                  {'heading': 'Common mistakes foreigners make when asking questions',
                   'body': ['<p>Foreigners often make questions too direct, translate word-for-word '
                            'from English or forget that Brazilian Portuguese has flexible word order '
                            'and natural conversational markers.</p>',
                            '<p>Common mistakes include:</p>',
                            '<h3>1. Using “fazer uma pergunta” too literally all the time</h3>',
                            '<p>“Can I ask a question?” can be translated as “Posso fazer uma '
                            'pergunta?”, and that is correct. But in many situations, you can simply '
                            'ask directly with a polite opening:</p>',
                            '<ul><li>“Desculpa, você sabe onde fica a recepção?”</li><li>“Por favor, '
                            'qual é o horário?”</li><li>“Só uma dúvida: precisa agendar?”</li></ul>',
                            '<p>“Só uma dúvida...” is very useful and natural.</p>',
                            '<h3>2. Forgetting “por favor” and tone</h3>',
                            '<p>Portuguese learners sometimes focus on grammar and forget social '
                            'warmth. Adding “por favor”, “desculpa” or “com licença” can make a big '
                            'difference.</p>',
                            '<ul><li>“Com licença, onde fica o banheiro?”</li><li>“Desculpa, você pode '
                            'me ajudar?”</li><li>“Por favor, qual é o seu nome?”</li></ul>',
                            '<h3>3. Using English structure too rigidly</h3>',
                            '<p>English questions often depend on auxiliaries like “do” and “does.” '
                            'Portuguese does not work the same way. In Brazilian Portuguese, '
                            'intonation and question words often carry the question.</p>',
                            '<p>Instead of thinking “Do you accept card?”, learn the natural '
                            'phrase:</p>',
                            '<ul><li>“Aceita cartão?”</li></ul>',
                            '<p>Instead of “Do you have coffee?”, say:</p>',
                            '<ul><li>“Tem café?”</li></ul>',
                            '<p>These short questions are common and natural.</p>',
                            '<h3>4. Not practicing answers</h3>',
                            '<p>A question is only half of the interaction. You also need to '
                            'understand the answer. This is why live classes matter. A teacher can '
                            'simulate realistic responses, including fast speech, informal expressions '
                            'and follow-up questions.</p>']},
                  {'heading': 'Live-class practice: question drills that work',
                   'body': ['<p>In live Portuguese classes, question practice should be interactive. '
                            'The teacher asks, the student answers, the student asks back, and the '
                            'situation changes. This builds flexibility.</p>',
                            '<p>Here are useful drills:</p>',
                            '<h3>Drill 1: Ask for location</h3>',
                            '<p>Teacher gives a place. Student asks how to get there.</p>',
                            '<ul><li>“Onde fica a farmácia?”</li><li>“Como eu chego ao '
                            'metrô?”</li><li>“É longe daqui?”</li></ul>',
                            '<h3>Drill 2: Confirm information</h3>',
                            '<p>Student practices confirmation phrases.</p>',
                            '<ul><li>“Só para confirmar, a aula é amanhã?”</li><li>“Então, o endereço '
                            'é esse?”</li><li>“O pagamento é no cartão?”</li></ul>',
                            '<h3>Drill 3: Ask for help</h3>',
                            '<p>Student practices polite requests.</p>',
                            '<ul><li>“Você pode me ajudar, por favor?”</li><li>“Será que você pode '
                            'explicar de novo?”</li><li>“Poderia falar mais devagar?”</li></ul>',
                            '<h3>Drill 4: Workplace clarification</h3>',
                            '<p>Student practices professional questions.</p>',
                            '<ul><li>“Qual é o prazo?”</li><li>“Quem vai participar da '
                            'reunião?”</li><li>“O que eu preciso preparar?”</li></ul>',
                            '<h3>Drill 5: Real Brazil role-play</h3>',
                            '<p>The teacher creates situations such as pharmacy, restaurant, building '
                            'reception, university office or meeting. The student must ask questions, '
                            'understand answers and react.</p>',
                            '<p>This is where recorded content is limited. Real conversation is '
                            'unpredictable. Live classes help you learn not only the correct question, '
                            'but also how to continue after the answer.</p>',
                            '<p>CTA: Want to practice Brazilian Portuguese questions in real time? '
                            'Book a free level check at <a '
                            'href="/en/portuguese-placement-test">https://vediums.com/</a> and '
                            'experience live Portuguese classes with practical, Brazil-focused '
                            'communication.</p>']},
                  {'heading': 'A simple weekly plan to improve your questions',
                   'body': ['<p>A weekly plan helps you turn question practice into a habit. You do '
                            'not need long study sessions. You need frequent, useful practice.</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Day</th><th>Focus</th><th>Practice</th></tr></thead><tbody><tr><td>Monday</td><td>Question '
                            'words</td><td>Write 10 questions with “onde”, “quando”, '
                            '“como”</td></tr><tr><td>Tuesday</td><td>Daily life</td><td>Practice '
                            'restaurant, transport and apartment '
                            'questions</td></tr><tr><td>Wednesday</td><td>Listening</td><td>Listen for '
                            'questions in Brazilian videos or '
                            'dialogues</td></tr><tr><td>Thursday</td><td>Speaking</td><td>Record '
                            'yourself asking 10 '
                            'questions</td></tr><tr><td>Friday</td><td>Work/study</td><td>Practice '
                            'meeting or class questions</td></tr><tr><td>Weekend</td><td>Live '
                            'practice</td><td>Role-play with a teacher or conversation '
                            'partner</td></tr></tbody></table>',
                            '<p>The key is to connect questions to your real life. If you are moving '
                            'to Brazil, practice questions about housing, transport and services. If '
                            'you are studying, practice questions about classes, assignments and '
                            'schedules. If you are working, practice questions about meetings, '
                            'deadlines and responsibilities.</p>']},
                  {'heading': 'Essential vocabulary for better questions',
                   'body': ['<p>Here is a practical list to start using immediately:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portuguese</th><th>English</th></tr></thead><tbody><tr><td>dúvida</td><td>question '
                            '/ '
                            'doubt</td></tr><tr><td>pergunta</td><td>question</td></tr><tr><td>resposta</td><td>answer</td></tr><tr><td>horário</td><td>time '
                            '/ '
                            'schedule</td></tr><tr><td>endereço</td><td>address</td></tr><tr><td>prazo</td><td>deadline</td></tr><tr><td>reunião</td><td>meeting</td></tr><tr><td>consulta</td><td>appointment</td></tr><tr><td>entrega</td><td>delivery</td></tr><tr><td>documento</td><td>document</td></tr><tr><td>pagamento</td><td>payment</td></tr><tr><td>cartão</td><td>card</td></tr><tr><td>dinheiro</td><td>cash</td></tr><tr><td>responsável</td><td>person '
                            'responsible</td></tr><tr><td>entrada</td><td>entrance</td></tr><tr><td>saída</td><td>exit</td></tr><tr><td>ajuda</td><td>help</td></tr><tr><td>devagar</td><td>slowly</td></tr><tr><td>de '
                            'novo</td><td>again</td></tr><tr><td>agora</td><td>now</td></tr><tr><td>depois</td><td>later '
                            '/ after</td></tr></tbody></table>',
                            '<p>Now turn vocabulary into questions:</p>',
                            '<ul><li>“Qual é o endereço?”</li><li>“Quem é o '
                            'responsável?”</li><li>“Qual é o prazo?”</li><li>“Pode falar '
                            'devagar?”</li><li>“Tem pagamento no cartão?”</li><li>“Onde fica a '
                            'entrada?”</li><li>“Quando é a consulta?”</li></ul>',
                            '<p>Vocabulary becomes useful when it becomes a question you can actually '
                            'ask.</p>']},
                  {'heading': 'Conclusion with strong CTA',
                   'body': ['<p>Asking better questions in Brazilian Portuguese is one of the fastest '
                            'ways to become more independent in Brazil. You do not need to wait for '
                            'advanced fluency. You can start with practical question words, polite '
                            'structures, real-life situations and follow-up phrases that help you '
                            'understand what people say next.</p>',
                            '<p>For expats, international students and professionals, this skill '
                            'matters every day. It helps you talk to building staff, coworkers, '
                            'classmates, doctors, drivers, attendants and new friends. It also helps '
                            'you understand Brazilian culture through conversation, not only '
                            'grammar.</p>',
                            '<p>Vedium offers live Brazilian Portuguese classes for foreigners, with '
                            'practical language, cultural context and real speaking practice. There '
                            'are no long-term loyalty contracts. You continue because you feel '
                            'progress.</p>',
                            '<p>Book your free level check at <a '
                            'href="/en/learn-portuguese-brazil">https://vediums.com/</a> and start '
                            'asking better questions in Portuguese with confidence.</p>']}],
     'faqs': [{'q': 'What are the most important question words in Brazilian Portuguese?',
               'a': 'The most important question words are “o que” (what), “quem” (who), “onde” '
                    '(where), “quando” (when), “como” (how), “quanto” (how much), “qual” (which/what) '
                    'and “por quê” (why).'},
              {'q': 'How do I politely ask someone to repeat in Portuguese?',
               'a': 'You can say “Pode repetir, por favor?” or “Desculpa, não entendi. Pode falar mais '
                    'devagar?” These phrases are polite, natural and useful in daily life in Brazil.'},
              {'q': 'Why do Brazilians use “será que” in questions?',
               'a': '“Será que” softens a question or request. It can make the sentence sound less '
                    'direct and more polite, similar to “Would it be possible...” or “Do you happen to '
                    'know...” in English.'},
              {'q': 'Can I learn Brazilian Portuguese questions with apps?',
               'a': 'Apps can help with vocabulary, but live practice is better for pronunciation, '
                    'natural answers, follow-up questions and cultural context. Real conversation '
                    'requires interaction and correction.'},
              {'q': 'Does Vedium teach Brazilian Portuguese for foreigners?',
               'a': 'Yes. Vedium offers live online Brazilian Portuguese classes for foreigners, '
                    'expats and international professionals, with practical communication, cultural '
                    'context and no long-term loyalty contracts.'}],
     'cta_title': 'Want to know your real Portuguese level?',
     'cta_text': "Take Vedium's free placement test and find out where to start.",
     'cta_label': 'Learn about the Portuguese course',
     'cta_url': '/en/learn-portuguese-brazil'},
    "how-to-greet-people-in-brazil-without-sounding-too-formal": {'title': 'How to greet people in Brazil without sounding too formal',
     'meta_description': 'Learn how to greet people in Brazil naturally, from casual hello to '
                         'workplace introductions, with practical Brazilian Portuguese phrases.',
     'h1': 'How to greet people in Brazil without sounding too formal',
     'date': '2025-01-14',
     'date_display': 'January 14, 2025',
     'hero_image': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aprender português como língua estrangeira',
     'tag': 'Brazilian Portuguese',
     'lang': 'en',
     'category': 'brazilian-portuguese',
     'lead': 'To greet people in Brazil naturally, start with simple Brazilian Portuguese phrases like '
             '“Oi, tudo bem?”, “Bom dia”, “Boa tarde”, “Boa noite” and “Prazer”. The key is not to '
             'sound perfectly native on day one. The key is to understand when Brazilians expect '
             'warmth, when formality is useful, and how to adjust your greeting to real-life '
             'situations.',
     'sections': [{'heading': '',
                   'body': ['<p>For foreigners living, working or studying in Brazil, greetings are '
                            'one of the first cultural bridges. They happen everywhere: at the '
                            'building entrance, in the elevator, at work, in a shop, in a café, on a '
                            'video call, before a meeting and when meeting friends of friends. A '
                            'greeting may seem small, but in Brazil it often sets the tone for the '
                            'whole interaction.</p>',
                            '<p>Many learners translate directly from English and become too formal. '
                            'They say only “Good morning” or “How do you do?” in situations where '
                            'Brazilians would use something warmer and simpler. Others go too casual '
                            'too quickly and use slang with people they do not know yet. The best path '
                            'is balance: friendly, clear and appropriate to the context.</p>',
                            '<p>That is why Brazilian Portuguese for foreigners should not be taught '
                            'only through grammar. You need culture, listening practice and speaking '
                            'correction. At Vedium, Portuguese for foreigners is taught in live online '
                            'classes so you can practice real interactions, ask questions and build '
                            'confidence before using the language in Brazil.</p>']},
                  {'heading': 'Why greetings matter so much in Brazil',
                   'body': ['<p>Greetings matter in Brazil because they show attention, openness and '
                            'respect. A short “Oi, tudo bem?” can make an interaction feel more human '
                            'and less transactional.</p>',
                            '<p>In many Brazilian contexts, people do not jump straight into the '
                            'request. Before asking for information, ordering food or beginning a work '
                            'conversation, it is common to start with a greeting. This does not mean '
                            'every interaction is long. It simply means that a small human opening is '
                            'expected.</p>',
                            '<p>For example, instead of saying only “I need this document,” a more '
                            'natural Brazilian-style interaction would begin with:</p>',
                            '<ul><li>“Oi, tudo bem? Eu preciso deste documento, por '
                            'favor.”</li><li>“Bom dia, tudo bem? Você pode me ajudar?”</li><li>“Boa '
                            'tarde. Eu tenho uma dúvida.”</li></ul>',
                            '<p>These phrases soften the conversation. They also make you sound less '
                            'robotic. If you are an expat or relocation employee, this is especially '
                            'important because many daily situations involve people you will see '
                            'repeatedly, such as doormen, receptionists, colleagues, building staff, '
                            'neighbors and service providers.</p>',
                            '<p>The good news is that you do not need advanced Portuguese to greet '
                            'people well. A small set of phrases, used with the right tone, can help '
                            'you sound more natural immediately.</p>',
                            '<p><strong>CTA:</strong> Book a free level check with Vedium and practice '
                            'Brazilian Portuguese greetings in live classes: <a '
                            'href="/en/learn-portuguese-brazil">https://vediums.com/</a></p>']},
                  {'heading': 'The safest greeting for most situations: “Oi, tudo bem?”',
                   'body': ['<p>The safest everyday greeting in Brazil is “Oi, tudo bem?”. It means '
                            '“Hi, how are you?” and works in many casual and semi-formal '
                            'situations.</p>',
                            '<p>You can use “Oi, tudo bem?” with neighbors, colleagues, classmates, '
                            'store staff, receptionists, delivery people, friends of friends and '
                            'people your age or close to your environment. It is warm without being '
                            'too intimate.</p>',
                            '<p>Pronunciation guide:</p>',
                            '<ul><li><strong>Oi</strong> sounds like “oy”.</li><li><strong>Tudo '
                            'bem?</strong> sounds approximately like “TOO-doo beng?”</li></ul>',
                            '<p>Common variations include:</p>',
                            '<ul><li><strong>Oi, tudo bem?</strong> — Hi, how are '
                            'you?</li><li><strong>Olá, tudo bem?</strong> — Hello, how are '
                            'you?</li><li><strong>Tudo bom?</strong> — All good?</li><li><strong>Tudo '
                            'certo?</strong> — Everything okay?</li><li><strong>Como vai?</strong> — '
                            'How are you? / How is it going?</li></ul>',
                            '<p>If someone asks you “Tudo bem?”, you can answer simply:</p>',
                            '<ul><li><strong>Tudo bem, e você?</strong> — I’m good, and '
                            'you?</li><li><strong>Tudo, obrigado/obrigada. E você?</strong> — All '
                            'good, thank you. And you?</li><li><strong>Tudo certo.</strong> — '
                            'Everything’s fine.</li></ul>',
                            '<p>A common mistake is to give a long answer every time someone asks '
                            '“Tudo bem?”. In Brazil, this phrase often works as a social greeting, not '
                            'always as a deep question. A short answer is enough unless the person is '
                            'a close friend and clearly wants a real update.</p>']},
                  {'heading': 'When to use “Bom dia”, “Boa tarde” and “Boa noite”',
                   'body': ['<p>Use “Bom dia”, “Boa tarde” and “Boa noite” when you want to be polite, '
                            'especially in service, work, building and first-contact situations.</p>',
                            '<p>These expressions are very useful because they sound respectful '
                            'without being stiff. They are also easy to remember because they follow '
                            'the time of day:</p>',
                            '<ul><li><strong>Bom dia</strong> — Good morning.</li><li><strong>Boa '
                            'tarde</strong> — Good afternoon.</li><li><strong>Boa noite</strong> — '
                            'Good evening / Good night.</li></ul>',
                            '<p>In Brazil, “Boa noite” can be used when arriving at night and also '
                            'when saying goodbye at night. Context makes the meaning clear.</p>',
                            '<p>You can combine them with “tudo bem?” for a more natural tone:</p>',
                            '<ul><li>“Bom dia, tudo bem?”</li><li>“Boa tarde, tudo bem?”</li><li>“Boa '
                            'noite, tudo bem?”</li></ul>',
                            '<p>This is a strong formula for foreigners because it works almost '
                            'everywhere. Use it when speaking to:</p>',
                            '<ul><li>a building doorman;</li><li>a receptionist;</li><li>a '
                            'teacher;</li><li>a work contact;</li><li>a doctor’s office;</li><li>a '
                            'bank or service desk;</li><li>an older person you do not '
                            'know;</li><li>someone in a professional setting.</li></ul>',
                            '<p>For example:</p>',
                            '<ul><li>“Bom dia, tudo bem? Eu tenho uma reunião às dez.”</li><li>“Boa '
                            'tarde. Eu gostaria de confirmar meu cadastro.”</li><li>“Boa noite, tudo '
                            'bem? A entrega chegou?”</li></ul>',
                            '<p>These greetings help you sound polite and comfortable. They also give '
                            'you a few seconds to organize the rest of your sentence.</p>']},
                  {'heading': 'How to introduce yourself without sounding too formal',
                   'body': ['<p>To introduce yourself naturally in Brazil, use “Meu nome é...” or “Eu '
                            'sou...” followed by “Prazer”. These phrases are clear, friendly and '
                            'appropriate in most situations.</p>',
                            '<p>Useful phrases include:</p>',
                            '<ul><li><strong>Meu nome é Anna.</strong> — My name is '
                            'Anna.</li><li><strong>Eu sou o Michael.</strong> — I am '
                            'Michael.</li><li><strong>Eu sou a Laura.</strong> — I am '
                            'Laura.</li><li><strong>Prazer.</strong> — Nice to meet '
                            'you.</li><li><strong>Prazer em conhecer.</strong> — Nice to meet '
                            'you.</li><li><strong>Muito prazer.</strong> — Very nice to meet '
                            'you.</li></ul>',
                            '<p>In spoken Brazilian Portuguese, people often use “Eu sou o...” for a '
                            'man and “Eu sou a...” for a woman before a first name. This may feel '
                            'unusual for English speakers because Portuguese uses the article before '
                            'names in many informal contexts. You do not need to master every regional '
                            'detail immediately, but hearing this pattern will help you understand '
                            'Brazilians better.</p>',
                            '<p>A simple first introduction might be:</p>',
                            '<p>“Oi, tudo bem? Eu sou a Emma. Prazer.”</p>',
                            '<p>Or, in a work context:</p>',
                            '<p>“Bom dia, tudo bem? Meu nome é David. Eu sou novo na equipe.”</p>',
                            '<p>If you are still learning Portuguese, say it clearly:</p>',
                            '<p>“Eu ainda estou aprendendo português.”</p>',
                            '<p>This phrase is extremely useful. It tells people to slow down, but it '
                            'also shows effort and respect. Many Brazilians respond positively when '
                            'foreigners try to speak Portuguese, even with mistakes.</p>']},
                  {'heading': 'Casual greetings you will hear in Brazil',
                   'body': ['<p>You will hear casual greetings like “E aí?”, “Beleza?”, “Fala!” and '
                            '“Tudo certo?” in Brazil, but you should use them carefully until you '
                            'understand the context.</p>',
                            '<p>These expressions are common among friends, younger people, colleagues '
                            'with informal relationships and relaxed environments. They are not wrong, '
                            'but they may sound too casual in a bank, formal meeting, interview or '
                            'first interaction with an older person.</p>',
                            '<p>Here are useful casual greetings:</p>',
                            '<ul><li><strong>E aí?</strong> — What’s '
                            'up?</li><li><strong>Beleza?</strong> — All good?</li><li><strong>Tudo '
                            'certo?</strong> — Everything okay?</li><li><strong>Fala!</strong> — Hey! '
                            '/ What’s up?</li><li><strong>Oi, gente!</strong> — Hi, '
                            'everyone!</li></ul>',
                            '<p>A safe strategy is to understand these expressions before using them '
                            'heavily. When someone says “E aí?”, you can answer:</p>',
                            '<ul><li>“Tudo bem!”</li><li>“Tudo certo!”</li><li>“Beleza!”</li></ul>',
                            '<p>In live classes, this is exactly the kind of difference that matters. '
                            'A teacher can help you decide which phrase fits your personality, your '
                            'workplace and the city where you live. Brazilian Portuguese is not only '
                            'about correct words; it is also about social rhythm.</p>']},
                  {'heading': 'Greetings at work and in professional settings',
                   'body': ['<p>In professional settings, use greetings that are warm and respectful: '
                            '“Bom dia, tudo bem?”, “Olá, pessoal” and “Prazer em conhecer” are strong '
                            'choices.</p>',
                            '<p>Brazilian workplaces vary. Some are formal, some are very relaxed, and '
                            'many mix both depending on the person and situation. A safe approach is '
                            'to begin slightly more polite and adapt as you observe how others '
                            'speak.</p>',
                            '<p>For a meeting, you can say:</p>',
                            '<ul><li>“Bom dia, pessoal. Tudo bem?” — Good morning, everyone. How are '
                            'you?</li><li>“Boa tarde. Prazer em conhecer vocês.” — Good afternoon. '
                            'Nice to meet you all.</li><li>“Olá, eu sou o Daniel, da equipe de '
                            'produto.” — Hello, I’m Daniel, from the product team.</li></ul>',
                            '<p>For email or chat, you can write:</p>',
                            '<ul><li>“Olá, tudo bem?”</li><li>“Bom dia, Ana. Tudo bem?”</li><li>“Boa '
                            'tarde, equipe.”</li></ul>',
                            '<p>Avoid starting every professional interaction with a very cold phrase '
                            'if you want to sound natural in Brazil. A direct message with no greeting '
                            'can feel abrupt, especially when writing to someone for the first '
                            'time.</p>',
                            '<p>Also learn how to close conversations politely:</p>',
                            '<ul><li><strong>Obrigado/obrigada.</strong> — Thank '
                            'you.</li><li><strong>Até mais.</strong> — See you '
                            'later.</li><li><strong>Até amanhã.</strong> — See you '
                            'tomorrow.</li><li><strong>Bom trabalho.</strong> — Have a good '
                            'workday.</li></ul>',
                            '<p>For relocation teams and international professionals, this type of '
                            'language improves integration. Employees who can greet colleagues '
                            'naturally often feel more included and more confident in daily '
                            'communication.</p>']},
                  {'heading': 'Greetings in shops, restaurants and service situations',
                   'body': ['<p>In shops and restaurants, combine a greeting with a polite request. '
                            '“Oi, tudo bem?” plus “por favor” is usually enough to sound friendly and '
                            'respectful.</p>',
                            '<p>Examples:</p>',
                            '<ul><li>“Oi, tudo bem? Você pode me ajudar?” — Hi, how are you? Can you '
                            'help me?</li><li>“Bom dia. Eu gostaria de um café, por favor.” — Good '
                            'morning. I would like a coffee, please.</li><li>“Boa tarde. Vocês aceitam '
                            'cartão?” — Good afternoon. Do you accept card?</li><li>“Oi. Pode trazer o '
                            'cardápio, por favor?” — Hi. Can you bring the menu, please?</li></ul>',
                            '<p>In Brazil, service conversations often include small polite markers. '
                            'You do not need to overdo it, but using “por favor”, “obrigado/obrigada” '
                            'and “com licença” makes a difference.</p>',
                            '<p>Important words:</p>',
                            '<ul><li><strong>por favor</strong> — '
                            'please;</li><li><strong>obrigado</strong> — thank you, said by a '
                            'man;</li><li><strong>obrigada</strong> — thank you, said by a '
                            'woman;</li><li><strong>com licença</strong> — excuse '
                            'me;</li><li><strong>desculpa</strong> — sorry / excuse me.</li></ul>',
                            '<p>A practical class should help you say these phrases aloud. '
                            'Pronunciation matters because you will use them many times in real '
                            'life.</p>']},
                  {'heading': 'What to avoid when greeting people in Brazil',
                   'body': ['<p>Avoid sounding too cold, too translated or too formal for the '
                            'situation. The safest tone is friendly, simple and respectful.</p>',
                            '<p>Common mistakes include:</p>',
                            '<ol><li><strong>Skipping the greeting completely.</strong> In many '
                            'situations, going straight to the request may sound '
                            'abrupt.</li><li><strong>Using only formal textbook phrases.</strong> '
                            'Expressions like “Como vai o senhor?” may be correct, but they can sound '
                            'distant if used everywhere.</li><li><strong>Using slang too '
                            'soon.</strong> “E aí?” and “Fala!” are useful, but not ideal for every '
                            'context.</li><li><strong>Giving long answers to “Tudo bem?” every '
                            'time.</strong> Often, a short answer is '
                            'enough.</li><li><strong>Translating English greetings word for '
                            'word.</strong> Natural Portuguese has its own rhythm.</li></ol>',
                            '<p>The goal is not to become someone else. The goal is to communicate in '
                            'a way that Brazilians recognize as warm and appropriate.</p>']},
                  {'heading': 'How live classes help you sound natural faster',
                   'body': ['<p>Live classes help you sound natural because you practice greeting real '
                            'people, receive correction and learn the cultural context behind each '
                            'phrase.</p>',
                            '<p>Recorded lessons can show vocabulary, but they cannot tell you whether '
                            'your tone sounds too formal, whether your pronunciation is clear or '
                            'whether a phrase fits your situation. In a live class, you can practice '
                            'introductions, workplace greetings, restaurant interactions and everyday '
                            'conversations with feedback.</p>',
                            '<p>At Vedium, Brazilian Portuguese for foreigners is built around '
                            'real-life use. You learn vocabulary, but you also practice how to speak. '
                            'You bring your actual needs into class: relocation, work, housing, '
                            'transportation, social life or study in Brazil.</p>',
                            '<p>And because Vedium offers live online classes with no long-term '
                            'contracts, you can begin with a clear goal: speak with more confidence in '
                            'the situations you will actually face. You stay because the classes help '
                            'you progress, not because you are locked into a long commitment.</p>']},
                  {'heading': 'Conclusion with CTA: start greeting people in Brazil with confidence',
                   'body': ['<p>If you want to greet people in Brazil without sounding too formal, '
                            'start with a simple toolkit: “Oi, tudo bem?”, “Bom dia”, “Boa tarde”, '
                            '“Boa noite”, “Prazer”, “Por favor” and “Obrigado/obrigada”. Then learn '
                            'when each phrase fits: casual conversations, work, service situations, '
                            'first introductions and daily life.</p>',
                            '<p>This is more than vocabulary. It is cultural fluency. A natural '
                            'greeting can make your first month in Brazil smoother, warmer and less '
                            'intimidating. It helps you speak to colleagues, neighbors, doormen, '
                            'teachers, drivers, restaurant staff and new friends with more '
                            'confidence.</p>',
                            '<p><strong>Book a free level check with Vedium at <a '
                            'href="/en/portuguese-placement-test">https://vediums.com/</a> and start '
                            'practicing Brazilian Portuguese in live classes. Learn the language, the '
                            'culture and the real conversations you need to feel at home in '
                            'Brazil.</strong></p>']}],
     'faqs': [{'q': 'What is the most common greeting in Brazil?',
               'a': 'The most common everyday greeting is “Oi, tudo bem?”. It means “Hi, how are you?” '
                    'and works in many casual and semi-formal situations.'},
              {'q': 'Is “Bom dia” too formal in Brazil?',
               'a': 'No. “Bom dia” is polite, natural and widely used. You can make it warmer by '
                    'saying “Bom dia, tudo bem?” before asking a question or starting a conversation.'},
              {'q': 'Can foreigners use “E aí?” in Brazil?',
               'a': 'Yes, but it is casual. Use “E aí?” with friends, informal colleagues or relaxed '
                    'situations. For first contacts, “Oi, tudo bem?” is safer.'},
              {'q': 'How do I introduce myself in Brazilian Portuguese?',
               'a': 'You can say “Meu nome é...” or “Eu sou...” followed by your name. Add “Prazer” or '
                    '“Prazer em conhecer” to sound polite and natural.'},
              {'q': 'What is the best way to practice Brazilian Portuguese greetings?',
               'a': 'The best way is to practice aloud in realistic conversations. Live classes help '
                    'because a teacher can correct pronunciation, explain cultural context and '
                    'simulate daily situations in Brazil.'}],
     'cta_title': 'Want to know your real Portuguese level?',
     'cta_text': "Take Vedium's free placement test and find out where to start.",
     'cta_label': 'Learn about the Portuguese course',
     'cta_url': '/en/learn-portuguese-brazil'},
    "how-to-use-live-classes-to-gain-speaking-confidence": {'title': 'How to use live classes to gain speaking confidence',
     'meta_description': 'Learn how live Portuguese classes help foreigners gain speaking confidence '
                         'for real life, work and study in Brazil.',
     'h1': 'How to use live classes to gain speaking confidence',
     'date': '2026-06-16',
     'date_display': 'June 16, 2026',
     'hero_image': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aprender português como língua estrangeira',
     'tag': 'Brazilian Portuguese',
     'lang': 'en',
     'category': 'brazilian-portuguese',
     'lead': 'Live classes help you gain speaking confidence because they turn Brazilian Portuguese '
             'from something you “study” into something you actually use with real people. For '
             'foreigners, expats and international professionals in Brazil, speaking confidence does '
             'not come from memorizing vocabulary alone. It comes from asking questions, making '
             'mistakes safely, receiving correction, hearing natural answers and practicing situations '
             'that happen in real life.',
     'sections': [{'heading': '',
                   'body': ['<p>Many learners know more Portuguese than they can speak. They may '
                            'understand greetings, recognize words in apps and read simple sentences, '
                            'but when a Brazilian asks “Tudo bem?”, “Você precisa de ajuda?” or “Pode '
                            'repetir o endereço?”, they freeze. This is not a lack of intelligence. It '
                            'is usually a lack of live practice. Speaking is a skill, and skills need '
                            'interaction.</p>',
                            '<p>This guide explains how to use live Portuguese classes to gain '
                            'speaking confidence step by step. You will learn why speaking feels '
                            'difficult, what to practice in class, which real-life situations matter '
                            'most in Brazil, how to prepare before each lesson and how Vedium’s live '
                            'online classes help foreigners move from passive knowledge to practical '
                            'communication.</p>']},
                  {'heading': 'Why do many learners understand Portuguese but freeze when speaking?',
                   'body': ['<p>Many learners freeze because understanding and speaking are different '
                            'skills. You can recognize a word when you read it, but still struggle to '
                            'say it quickly in conversation. Speaking requires memory, pronunciation, '
                            'listening, confidence, word order and emotional control at the same '
                            'time.</p>',
                            '<p>This is especially common in Brazilian Portuguese for foreigners. A '
                            'learner may know phrases such as:</p>',
                            '<ul><li>“Eu sou...” — I am...</li><li>“Eu moro em...” — I live '
                            'in...</li><li>“Eu trabalho com...” — I work with...</li><li>“Pode '
                            'repetir?” — Can you repeat?</li><li>“Quanto custa?” — How much is '
                            'it?</li></ul>',
                            '<p>But in a real interaction, the other person may speak fast, use '
                            'informal expressions, ask an unexpected question or answer with words the '
                            'learner did not study. That moment creates pressure. The student starts '
                            'translating mentally, worries about mistakes and loses confidence.</p>',
                            '<p>Live classes solve this by creating a safe version of real life. You '
                            'practice with a teacher who can slow down, repeat, correct, explain and '
                            'help you try again. Over time, your brain learns that speaking Portuguese '
                            'is not a test. It is a conversation.</p>',
                            '<p>For expats in Brazil, this shift matters. You need Portuguese not only '
                            'for grammar exercises, but for daily tasks: ordering food, taking '
                            'transportation, talking to building staff, explaining a problem, making '
                            'small talk, asking for help and participating at work or school.</p>']},
                  {'heading': 'What makes live Portuguese classes different from apps or recorded '
                              'lessons?',
                   'body': ['<p>Live Portuguese classes are different because they include real-time '
                            'interaction. Apps and recorded lessons can help with vocabulary and '
                            'repetition, but they cannot fully train your ability to react, ask '
                            'follow-up questions and adjust your speech when communication becomes '
                            'unpredictable.</p>',
                            '<p>A recorded lesson can teach you:</p>',
                            '<ul><li>a list of verbs;</li><li>a pronunciation rule;</li><li>a grammar '
                            'explanation;</li><li>a set of travel phrases;</li><li>a listening '
                            'exercise.</li></ul>',
                            '<p>But a live class can ask you:</p>',
                            '<ul><li>“Where do you live in Brazil?”</li><li>“What did you do '
                            'yesterday?”</li><li>“How would you explain this problem to a '
                            'receptionist?”</li><li>“Can you ask the same question more '
                            'politely?”</li><li>“Can you repeat that with better '
                            'pronunciation?”</li></ul>',
                            '<p>That difference is powerful. Speaking confidence grows when you are '
                            'invited to produce language, not only consume it.</p>',
                            '<p>In live classes, you also receive feedback. If your sentence is '
                            'understandable but unnatural, the teacher can suggest a better version. '
                            'If your pronunciation changes the meaning, the teacher can correct it. If '
                            'you are using a phrase that sounds too formal or too direct for Brazilian '
                            'daily life, the teacher can explain the cultural nuance.</p>',
                            '<p>This is why Vedium emphasizes live online classes. The goal is not '
                            'just to teach Portuguese as a subject. The goal is to help you feel at '
                            'home in Portuguese, with practical language and cultural intelligence for '
                            'Brazil.</p>',
                            '<p>CTA: If you want to speak Brazilian Portuguese with more confidence, '
                            'book a free level check at <a '
                            'href="/en/learn-portuguese-brazil">https://vediums.com/</a> and see which '
                            'live class path fits your current level.</p>']},
                  {'heading': 'How live classes build confidence step by step',
                   'body': ['<p>Live classes build confidence through repeated exposure, guided '
                            'speaking and correction. The process is gradual. You do not become '
                            'confident by waiting until you are perfect. You become confident by '
                            'practicing before you are perfect and discovering that communication '
                            'still works.</p>',
                            '<h3>Step 1: You learn to speak before you feel ready</h3>',
                            '<p>Most learners wait too long to speak. They think, “I need more '
                            'vocabulary first” or “I need to understand grammar better.” But speaking '
                            'confidence grows by speaking. Live classes give you controlled '
                            'opportunities to start small.</p>',
                            '<p>At the beginning, this may mean answering simple questions:</p>',
                            '<ul><li>“Qual é o seu nome?” — What is your name?</li><li>“De onde você '
                            'é?” — Where are you from?</li><li>“Onde você mora?” — Where do you '
                            'live?</li><li>“Você trabalha ou estuda?” — Do you work or '
                            'study?</li><li>“Por que você está aprendendo português?” — Why are you '
                            'learning Portuguese?</li></ul>',
                            '<p>These questions are simple, but they create a foundation. The student '
                            'learns to introduce themselves without panic.</p>',
                            '<h3>Step 2: You repeat useful phrases until they become automatic</h3>',
                            '<p>Confidence increases when common phrases stop requiring translation. '
                            'Live classes help you repeat high-value phrases in different '
                            'situations.</p>',
                            '<p>Examples:</p>',
                            '<ul><li>“Pode repetir, por favor?” — Can you repeat, '
                            'please?</li><li>“Pode falar mais devagar?” — Can you speak more '
                            'slowly?</li><li>“Não entendi essa parte.” — I did not understand that '
                            'part.</li><li>“Como se diz isso em português?” — How do you say this in '
                            'Portuguese?</li><li>“Você pode me ajudar?” — Can you help me?</li></ul>',
                            '<p>These phrases are not “extra.” They are survival tools. They help you '
                            'stay inside the conversation even when you do not understand '
                            'everything.</p>',
                            '<h3>Step 3: You practice real situations before facing them</h3>',
                            '<p>A good live class should simulate Brazilian life. This is especially '
                            'important for expats and relocation learners. Instead of studying random '
                            'sentences, you practice what you will actually need.</p>',
                            '<p>Situations include:</p>',
                            '<ul><li>checking in at a hotel;</li><li>asking for '
                            'directions;</li><li>ordering in a restaurant;</li><li>speaking to '
                            'building reception;</li><li>reporting a delivery problem;</li><li>booking '
                            'an appointment;</li><li>asking about payment;</li><li>introducing '
                            'yourself at work;</li><li>joining a class or meeting;</li><li>making '
                            'small talk with colleagues.</li></ul>',
                            '<p>Each role-play reduces fear. When the real situation happens, your '
                            'brain recognizes the pattern.</p>',
                            '<h3>Step 4: You receive correction without shame</h3>',
                            '<p>Correction is one of the most valuable parts of live learning. Many '
                            'adults fear mistakes because they associate errors with embarrassment. A '
                            'good teacher changes that experience. Correction becomes support, not '
                            'judgment.</p>',
                            '<p>In live classes, correction can focus on:</p>',
                            '<ul><li>pronunciation;</li><li>word choice;</li><li>verb '
                            'form;</li><li>sentence order;</li><li>natural '
                            'phrasing;</li><li>politeness;</li><li>cultural context;</li><li>listening '
                            'comprehension.</li></ul>',
                            '<p>The goal is not to make you feel wrong. The goal is to help you be '
                            'understood more clearly and naturally.</p>',
                            '<h3>Step 5: You measure progress through real communication</h3>',
                            '<p>Speaking confidence grows when you notice progress. Maybe you can now '
                            'introduce yourself faster. Maybe you can ask for repetition without '
                            'freezing. Maybe you can speak to a receptionist or understand a simple '
                            'WhatsApp message.</p>',
                            '<p>Small wins matter. In language learning, confidence is built through '
                            'evidence: “I did this once. I can do it again.”</p>']},
                  {'heading': 'Real-life situations to practice in live Portuguese classes',
                   'body': ['<p>The best live classes for Brazilian Portuguese should be connected to '
                            'real life in Brazil. If your goal is to live, work or study in Brazil, '
                            'your speaking practice should reflect that.</p>',
                            '<h3>Airport and arrival</h3>',
                            '<p>Practice:</p>',
                            '<ul><li>“Onde fica a retirada de bagagem?” — Where is baggage '
                            'claim?</li><li>“Onde eu pego o Uber?” — Where do I take the '
                            'Uber?</li><li>“Pode me ajudar?” — Can you help me?</li><li>“Meu destino é '
                            'este endereço.” — My destination is this address.</li></ul>',
                            '<p>This gives confidence for your first hours in the country.</p>',
                            '<h3>Apartment and building communication</h3>',
                            '<p>Practice:</p>',
                            '<ul><li>“Chegou uma entrega para mim?” — Did a delivery arrive for '
                            'me?</li><li>“A internet não está funcionando.” — The internet is not '
                            'working.</li><li>“Preciso falar com a manutenção.” — I need to speak with '
                            'maintenance.</li><li>“Onde fica a lixeira?” — Where is the trash '
                            'area?</li></ul>',
                            '<p>These phrases are highly relevant for expats living in Brazilian '
                            'apartment buildings.</p>',
                            '<h3>Restaurants and cafés</h3>',
                            '<p>Practice:</p>',
                            '<ul><li>“Tem mesa para duas pessoas?” — Do you have a table for '
                            'two?</li><li>“Qual é o prato do dia?” — What is the dish of the '
                            'day?</li><li>“A conta, por favor.” — The bill, please.</li><li>“Aceita '
                            'cartão?” — Do you accept cards?</li></ul>',
                            '<p>Food situations are excellent for building early confidence because '
                            'they repeat often.</p>',
                            '<h3>Work and study</h3>',
                            '<p>Practice:</p>',
                            '<ul><li>“Qual é o prazo?” — What is the deadline?</li><li>“Podemos marcar '
                            'uma reunião?” — Can we schedule a meeting?</li><li>“Só para confirmar...” '
                            '— Just to confirm...</li><li>“Você pode explicar de novo?” — Can you '
                            'explain again?</li><li>“Onde encontro o material da aula?” — Where can I '
                            'find the class material?</li></ul>',
                            '<p>For professionals and students, these phrases help you participate '
                            'rather than stay silent.</p>',
                            '<h3>Health and pharmacy</h3>',
                            '<p>Practice:</p>',
                            '<ul><li>“Estou com dor de cabeça.” — I have a headache.</li><li>“Precisa '
                            'de receita?” — Do I need a prescription?</li><li>“Como eu tomo esse '
                            'remédio?” — How do I take this medicine?</li><li>“Tenho alergia a...” — I '
                            'am allergic to...</li></ul>',
                            '<p>Health vocabulary is not optional. It gives peace of mind.</p>']},
                  {'heading': 'Essential vocabulary for speaking confidence',
                   'body': ['<p>Speaking confidence grows when you have essential vocabulary ready for '
                            'common situations. Do not try to learn every word at once. Start with '
                            'high-frequency words that unlock many conversations.</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portuguese</th><th>English</th></tr></thead><tbody><tr><td>ajuda</td><td>help</td></tr><tr><td>dúvida</td><td>question '
                            '/ '
                            'doubt</td></tr><tr><td>endereço</td><td>address</td></tr><tr><td>horário</td><td>time '
                            '/ '
                            'schedule</td></tr><tr><td>reunião</td><td>meeting</td></tr><tr><td>trabalho</td><td>work</td></tr><tr><td>aula</td><td>class</td></tr><tr><td>entrega</td><td>delivery</td></tr><tr><td>documento</td><td>document</td></tr><tr><td>pagamento</td><td>payment</td></tr><tr><td>cartão</td><td>card</td></tr><tr><td>dinheiro</td><td>cash</td></tr><tr><td>banheiro</td><td>bathroom</td></tr><tr><td>farmácia</td><td>pharmacy</td></tr><tr><td>mercado</td><td>market</td></tr><tr><td>restaurante</td><td>restaurant</td></tr><tr><td>problema</td><td>problem</td></tr><tr><td>devagar</td><td>slowly</td></tr><tr><td>de '
                            'novo</td><td>again</td></tr><tr><td>agora</td><td>now</td></tr><tr><td>amanhã</td><td>tomorrow</td></tr><tr><td>hoje</td><td>today</td></tr></tbody></table>',
                            '<p>Turn vocabulary into useful phrases:</p>',
                            '<ul><li>“Preciso de ajuda.” — I need help.</li><li>“Tenho uma dúvida.” — '
                            'I have a question.</li><li>“Qual é o endereço?” — What is the '
                            'address?</li><li>“Qual é o horário?” — What is the time?</li><li>“Tenho '
                            'uma reunião amanhã.” — I have a meeting tomorrow.</li><li>“Pode falar '
                            'devagar?” — Can you speak slowly?</li><li>“Pode repetir de novo?” — Can '
                            'you repeat again?</li></ul>',
                            '<p>This is how vocabulary becomes speaking ability.</p>']},
                  {'heading': 'How to prepare before a live Portuguese class',
                   'body': ['<p>To get the most from live Portuguese classes, prepare with a clear '
                            'goal. You do not need to study for hours before class. You need to arrive '
                            'with useful material and questions.</p>',
                            '<p>Use this simple preparation plan:</p>',
                            '<h3>1. Choose one real situation</h3>',
                            '<p>Examples:</p>',
                            '<ul><li>talking to a taxi driver;</li><li>checking in at a '
                            'hotel;</li><li>asking a coworker for help;</li><li>speaking with building '
                            'staff;</li><li>ordering lunch;</li><li>making an '
                            'appointment;</li><li>explaining a problem.</li></ul>',
                            '<h3>2. Write five sentences you want to say</h3>',
                            '<p>Do not worry if they are imperfect. Bring them to class. The teacher '
                            'can correct and improve them.</p>',
                            '<p>Example:</p>',
                            '<ul><li>“I need to speak with maintenance.”</li><li>“My internet is not '
                            'working.”</li><li>“Can you help me?”</li><li>“What time will the '
                            'technician arrive?”</li><li>“Can you send me a message?”</li></ul>',
                            '<h3>3. Prepare three questions</h3>',
                            '<p>Ask about pronunciation, word choice or cultural context.</p>',
                            '<p>Examples:</p>',
                            '<ul><li>“Is this phrase polite?”</li><li>“How do Brazilians usually say '
                            'this?”</li><li>“Can I use this in a formal situation?”</li></ul>',
                            '<h3>4. Practice aloud before class</h3>',
                            '<p>Reading silently is not enough. Speaking confidence requires voice. '
                            'Say the sentences out loud, even if slowly.</p>',
                            '<h3>5. Ask for role-play</h3>',
                            '<p>Tell your teacher: “Can we practice this situation?” Role-play is one '
                            'of the fastest ways to turn knowledge into confidence.</p>']},
                  {'heading': 'What to do during the live class',
                   'body': ['<p>During the live class, your main goal is to speak, not to be perfect. '
                            'Many learners use class time only to listen, but confidence grows when '
                            'you produce language.</p>',
                            '<p>Do these five things:</p>',
                            '<ul><li>answer in full phrases when possible;</li><li>ask the teacher to '
                            'repeat naturally;</li><li>request correction;</li><li>repeat corrected '
                            'sentences aloud;</li><li>ask for a second attempt after '
                            'feedback.</li></ul>',
                            '<p>For example, if you say:</p>',
                            '<p>“Eu precisa ajuda.”</p>',
                            '<p>The teacher may correct:</p>',
                            '<p>“Eu preciso de ajuda.”</p>',
                            '<p>Do not just say “okay.” Repeat the corrected version three times. Then '
                            'use it in another sentence:</p>',
                            '<ul><li>“Eu preciso de ajuda com o endereço.”</li><li>“Eu preciso de '
                            'ajuda no hotel.”</li><li>“Eu preciso de ajuda com a internet.”</li></ul>',
                            '<p>This turns correction into learning.</p>']},
                  {'heading': 'What to do after class to keep improving',
                   'body': ['<p>After class, review and reuse what you practiced. Speaking confidence '
                            'fades if class is the only moment you touch Portuguese. You need short '
                            'follow-up practice.</p>',
                            '<p>After each live class:</p>',
                            '<ol><li>Write down five corrected phrases.</li><li>Record yourself saying '
                            'them.</li><li>Repeat the role-play alone once.</li><li>Use one phrase in '
                            'real life if possible.</li><li>Bring one new question to the next '
                            'class.</li></ol>',
                            '<p>This creates a learning loop: prepare, speak, receive correction, '
                            'review, use, repeat.</p>',
                            '<p>A weekly rhythm could be:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Day</th><th>Practice</th></tr></thead><tbody><tr><td>Monday</td><td>Review '
                            'class phrases</td></tr><tr><td>Tuesday</td><td>Listen to a short '
                            'Brazilian dialogue</td></tr><tr><td>Wednesday</td><td>Live '
                            'class</td></tr><tr><td>Thursday</td><td>Record corrected '
                            'phrases</td></tr><tr><td>Friday</td><td>Practice one real '
                            'situation</td></tr><tr><td>Weekend</td><td>Review and prepare next '
                            'class</td></tr></tbody></table>',
                            '<p>Consistency matters more than long study sessions. Ten focused minutes '
                            'after class can make the next class much stronger.</p>']},
                  {'heading': 'How live classes help with Brazilian culture',
                   'body': ['<p>Live classes help with culture because language is not only grammar. '
                            'In Brazil, tone, friendliness, politeness and small talk often shape '
                            'communication. A phrase may be correct but sound too cold, too formal or '
                            'too direct depending on the situation.</p>',
                            '<p>For example, in Brazilian Portuguese, you may hear and use expressions '
                            'like:</p>',
                            '<ul><li>“Tudo bem?” — How are you?</li><li>“Com licença.” — Excuse '
                            'me.</li><li>“Por favor.” — Please.</li><li>“Desculpa.” — Sorry / excuse '
                            'me.</li><li>“Será que você pode...?” — Would it be possible for you '
                            'to...?</li><li>“Só para confirmar...” — Just to '
                            'confirm...</li><li>“Combinado.” — Agreed / deal.</li><li>“Pode deixar.” — '
                            'Sure, leave it to me.</li></ul>',
                            '<p>These expressions carry cultural meaning. “Será que” softens a '
                            'request. “Só para confirmar” avoids misunderstanding politely. '
                            '“Combinado” closes an agreement in a natural Brazilian way.</p>',
                            '<p>A live teacher can explain these nuances and help you choose the right '
                            'expression for the context. This is especially useful for foreigners '
                            'working or studying in Brazil, where communication is both practical and '
                            'relational.</p>']},
                  {'heading': 'Common mistakes learners make with speaking practice',
                   'body': ['<p>Many learners slow their progress by practicing in ways that feel '
                            'comfortable but do not build speaking confidence.</p>',
                            '<h3>Mistake 1: Waiting to speak until grammar is perfect</h3>',
                            '<p>You do not need perfect grammar to start speaking. You need guided '
                            'practice. Grammar improves faster when it is connected to real '
                            'communication.</p>',
                            '<h3>Mistake 2: Memorizing lists without using them</h3>',
                            '<p>Vocabulary lists are useful only if you turn words into phrases and '
                            'phrases into dialogue.</p>',
                            '<h3>Mistake 3: Avoiding correction</h3>',
                            '<p>Correction is not a sign of failure. It is the fastest way to improve. '
                            'A live class gives you correction in a supportive environment.</p>',
                            '<h3>Mistake 4: Practicing only formal Portuguese</h3>',
                            '<p>In Brazil, you need both polite and natural language. Live classes '
                            'help you understand when to use a formal phrase and when a simpler, '
                            'warmer expression sounds better.</p>',
                            '<h3>Mistake 5: Not repeating after feedback</h3>',
                            '<p>The moment after correction is extremely important. Repeat '
                            'immediately. That is how your mouth and memory learn the better '
                            'version.</p>']},
                  {'heading': 'Why Vedium is a practical choice for expats in Brazil',
                   'body': ['<p>Vedium is a practical choice because it combines live online classes, '
                            'Brazilian real-life situations and cultural depth. The goal is not to '
                            'make foreigners memorize Portuguese from a distance. The goal is to help '
                            'them speak with confidence in Brazil.</p>',
                            '<p>For expats, international professionals and students, Vedium’s '
                            'approach is useful because it focuses on:</p>',
                            '<ul><li>live interaction, not only recorded content;</li><li>practical '
                            'Brazilian Portuguese;</li><li>real-life communication;</li><li>cultural '
                            'intelligence;</li><li>speaking confidence;</li><li>flexible online '
                            'learning;</li><li>no long-term loyalty contracts.</li></ul>',
                            '<p>The absence of long-term contracts matters. It means learners stay '
                            'because they feel progress. The relationship is based on value, not '
                            'pressure.</p>',
                            '<p>CTA: Book a free level check at <a '
                            'href="/en/portuguese-placement-test">https://vediums.com/</a> and '
                            'discover how live Portuguese classes can help you speak with more '
                            'confidence in Brazil.</p>']},
                  {'heading': 'Conclusion with strong CTA',
                   'body': ['<p>Speaking confidence in Brazilian Portuguese is not built by waiting '
                            'until you know everything. It is built through real interaction: '
                            'speaking, listening, asking, making mistakes, receiving correction and '
                            'trying again. Live classes create the safest and most effective '
                            'environment for that process.</p>',
                            '<p>If you are a foreigner, expat, international student or professional '
                            'preparing for life in Brazil, live Portuguese classes can help you move '
                            'from passive knowledge to practical communication. You can practice '
                            'airport arrival, hotel check-in, apartment problems, work conversations, '
                            'study situations, restaurants, transport, pharmacy visits and everyday '
                            'small talk before facing them alone.</p>',
                            '<p>Vedium offers live online Brazilian Portuguese classes for foreigners, '
                            'with practical language, cultural context and no long-term loyalty '
                            'contracts. You continue because you gain confidence and see progress.</p>',
                            '<p>Book your free level check at <a '
                            'href="/en/learn-portuguese-brazil">https://vediums.com/</a> and start '
                            'speaking Brazilian Portuguese with more confidence, one live class at a '
                            'time.</p>']}],
     'faqs': [{'q': 'Can live classes really improve speaking confidence?',
               'a': 'Yes. Live classes improve speaking confidence because they give you real-time '
                    'practice, correction, listening exposure and safe opportunities to make mistakes '
                    'and try again.'},
              {'q': 'Are live Portuguese classes better than apps?',
               'a': 'Apps can help with vocabulary and repetition, but live classes are better for '
                    'speaking, pronunciation, natural conversation, cultural context and real-time '
                    'feedback.'},
              {'q': 'What should I practice in a live Brazilian Portuguese class?',
               'a': 'Practice real situations such as introductions, airport arrival, hotel check-in, '
                    'restaurants, transport, apartment issues, work meetings, study questions and '
                    'asking for help.'},
              {'q': 'How often should I take live Portuguese classes?',
               'a': 'One or two live classes per week, combined with short independent practice, can '
                    'create steady progress. More frequent classes may help if you need faster '
                    'preparation for relocation or work.'},
              {'q': 'Does Vedium offer live Portuguese classes for foreigners?',
               'a': 'Yes. Vedium offers live online Brazilian Portuguese classes for foreigners, '
                    'expats and international professionals, focused on practical communication, '
                    'cultural understanding and speaking confidence.'}],
     'cta_title': 'Want to know your real Portuguese level?',
     'cta_text': "Take Vedium's free placement test and find out where to start.",
     'cta_label': 'Learn about the Portuguese course',
     'cta_url': '/en/learn-portuguese-brazil'},
    "portuguese-for-airport-arrival-and-first-hotel-check-in": {'title': 'Portuguese for airport arrival and first hotel check-in',
     'meta_description': 'Learn essential Brazilian Portuguese for airport arrival and hotel check-in, '
                         'with practical phrases for your first hours in Brazil.',
     'h1': 'Portuguese for airport arrival and first hotel check-in',
     'date': '2026-06-23',
     'date_display': 'June 23, 2026',
     'hero_image': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aprender português como língua estrangeira',
     'tag': 'Brazilian Portuguese',
     'lang': 'en',
     'category': 'brazilian-portuguese',
     'lead': 'Brazilian Portuguese for airport arrival and first hotel check-in is about handling your '
             'first practical interactions in Brazil with confidence: immigration, baggage, transport, '
             'hotel reception, documents, payment, Wi-Fi, breakfast, check-out time and asking for '
             'help. You do not need advanced Portuguese to arrive safely, but you do need a small set '
             'of real phrases that work in Brazilian contexts.',
     'sections': [{'heading': '',
                   'body': ['<p>For foreigners, expats, relocation employees and international '
                            'students, the first hours in Brazil can feel intense. You may be tired '
                            'from a long flight, surrounded by fast speech, unfamiliar signs and new '
                            'procedures. Even if some airport and hotel staff speak English, you '
                            'cannot assume every interaction will happen in English. A few Brazilian '
                            'Portuguese phrases can reduce stress, help you confirm important '
                            'information and make you feel more in control.</p>',
                            '<p>This guide gives you practical Portuguese for airport arrival and '
                            'hotel check-in in Brazil. It includes real-life situations, essential '
                            'vocabulary, useful sentence patterns and live-class practice ideas. It is '
                            'designed for learners who want Brazilian Portuguese for foreigners in a '
                            'practical way, not just grammar in isolation.</p>']},
                  {'heading': 'Why learn Portuguese before your first airport arrival in Brazil?',
                   'body': ['<p>You should learn basic Portuguese before arriving in Brazil because '
                            'your first interactions often involve urgent, practical decisions. You '
                            'may need to ask where to go, confirm baggage information, speak to a '
                            'driver, explain a reservation problem or ask hotel reception for '
                            'help.</p>',
                            '<p>Airport arrival and hotel check-in are decision-heavy moments. You '
                            'need to understand signs, people, documents, payment options and '
                            'directions. When you are tired or nervous, even simple tasks can feel '
                            'harder. Knowing a few phrases in Portuguese gives you a safety net.</p>',
                            '<p>For example, you may need to ask:</p>',
                            '<ul><li>Where is baggage claim?</li><li>Where can I take an Uber or '
                            'taxi?</li><li>Can you repeat that, please?</li><li>Do I need to show my '
                            'passport?</li><li>Is breakfast included?</li><li>What time is '
                            'check-out?</li><li>Can I leave my luggage here?</li><li>What is the Wi-Fi '
                            'password?</li></ul>',
                            '<p>These questions are not advanced, but they matter. They help you move '
                            'from the airport to your hotel, complete check-in and solve immediate '
                            'needs.</p>',
                            '<p>At Vedium, Brazilian Portuguese is taught through live classes because '
                            'travel and relocation language must be practiced as real interaction. It '
                            'is not enough to memorize a phrase. You need to hear a response, ask '
                            'again, clarify and pronounce the sentence clearly enough to be '
                            'understood.</p>',
                            '<p>CTA: If you are preparing to arrive in Brazil, book a free level check '
                            'at <a href="/en/learn-portuguese-brazil">https://vediums.com/</a> and '
                            'start learning practical Brazilian Portuguese with live classes.</p>']},
                  {'heading': 'Step 1: Essential phrases when you land in Brazil',
                   'body': ['<p>When you land in Brazil, your first useful phrases are about '
                            'orientation, repetition and help. These phrases work in many contexts: '
                            'airport, immigration, baggage area, transport and hotel reception.</p>',
                            '<p>Start with these:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portuguese</th><th>English</th></tr></thead><tbody><tr><td>Com '
                            'licença.</td><td>Excuse me.</td></tr><tr><td>Você pode me '
                            'ajudar?</td><td>Can you help me?</td></tr><tr><td>Eu não '
                            'entendi.</td><td>I did not understand.</td></tr><tr><td>Pode repetir, por '
                            'favor?</td><td>Can you repeat, please?</td></tr><tr><td>Pode falar mais '
                            'devagar?</td><td>Can you speak more slowly?</td></tr><tr><td>Estou '
                            'aprendendo português.</td><td>I am learning '
                            'Portuguese.</td></tr><tr><td>Eu falo pouco português.</td><td>I speak a '
                            'little Portuguese.</td></tr><tr><td>Onde fica...?</td><td>Where '
                            'is...?</td></tr><tr><td>Como eu chego a...?</td><td>How do I get '
                            'to...?</td></tr><tr><td>Obrigado / Obrigada.</td><td>Thank '
                            'you.</td></tr></tbody></table>',
                            '<p>A very useful sentence is:</p>',
                            '<p><strong>“Desculpa, eu falo pouco português. Pode falar mais devagar, '
                            'por favor?”</strong><br>Sorry, I speak a little Portuguese. Can you speak '
                            'more slowly, please?</p>',
                            '<p>This sentence does two things at once. It explains your level and '
                            'politely asks the person to adjust. Many Brazilians appreciate the effort '
                            'and will try to help.</p>']},
                  {'heading': 'Step 2: Portuguese for immigration and passport control',
                   'body': ['<p>At immigration, keep your answers simple, clear and calm. In many '
                            'cases, officers may use basic questions or gestures, and some may speak '
                            'English. Still, knowing key words helps you understand the process.</p>',
                            '<p>Common vocabulary:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portuguese</th><th>English</th></tr></thead><tbody><tr><td>passaporte</td><td>passport</td></tr><tr><td>visto</td><td>visa</td></tr><tr><td>motivo '
                            'da viagem</td><td>purpose of the '
                            'trip</td></tr><tr><td>turismo</td><td>tourism</td></tr><tr><td>trabalho</td><td>work</td></tr><tr><td>estudo</td><td>study</td></tr><tr><td>endereço</td><td>address</td></tr><tr><td>hotel</td><td>hotel</td></tr><tr><td>empresa</td><td>company</td></tr><tr><td>quanto '
                            'tempo</td><td>how long</td></tr><tr><td>passagem de volta</td><td>return '
                            'ticket</td></tr></tbody></table>',
                            '<p>Possible questions you may hear:</p>',
                            '<ul><li>“Qual é o motivo da viagem?” — What is the purpose of the '
                            'trip?</li><li>“Quanto tempo você vai ficar no Brasil?” — How long will '
                            'you stay in Brazil?</li><li>“Onde você vai ficar?” — Where will you '
                            'stay?</li><li>“Você tem passagem de volta?” — Do you have a return '
                            'ticket?</li><li>“Você vem a trabalho?” — Are you coming for '
                            'work?</li><li>“Você vem a turismo?” — Are you coming for '
                            'tourism?</li></ul>',
                            '<p>Simple answers:</p>',
                            '<ul><li>“Turismo.” — Tourism.</li><li>“Trabalho.” — '
                            'Work.</li><li>“Estudo.” — Study.</li><li>“Vou ficar duas semanas.” — I '
                            'will stay for two weeks.</li><li>“Vou ficar neste hotel.” — I will stay '
                            'at this hotel.</li><li>“Aqui está o endereço.” — Here is the '
                            'address.</li><li>“Aqui está a reserva.” — Here is the '
                            'reservation.</li></ul>',
                            '<p>If you are relocating for work, you can say:</p>',
                            '<p><strong>“Eu venho a trabalho. Minha empresa fica em São '
                            'Paulo.”</strong><br>I am coming for work. My company is in São Paulo.</p>',
                            '<p>If you are studying:</p>',
                            '<p><strong>“Eu venho para estudar.”</strong><br>I am coming to study.</p>',
                            '<p>The goal is not to give long explanations. The goal is to answer '
                            'clearly.</p>']},
                  {'heading': 'Step 3: Portuguese for baggage claim and airport problems',
                   'body': ['<p>After immigration, you may need to find baggage claim, ask about a '
                            'suitcase or report a problem. This is where practical Portuguese becomes '
                            'extremely useful.</p>',
                            '<p>Useful vocabulary:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portuguese</th><th>English</th></tr></thead><tbody><tr><td>bagagem</td><td>baggage</td></tr><tr><td>mala</td><td>suitcase</td></tr><tr><td>esteira</td><td>baggage '
                            'carousel</td></tr><tr><td>carrinho</td><td>luggage '
                            'cart</td></tr><tr><td>perdida</td><td>lost</td></tr><tr><td>danificada</td><td>damaged</td></tr><tr><td>comprovante</td><td>receipt '
                            '/ '
                            'proof</td></tr><tr><td>etiqueta</td><td>tag</td></tr><tr><td>atendimento</td><td>service '
                            'desk</td></tr></tbody></table>',
                            '<p>Useful phrases:</p>',
                            '<ul><li>“Onde fica a retirada de bagagem?” — Where is baggage '
                            'claim?</li><li>“Onde fica a esteira do voo de Miami?” — Where is the '
                            'carousel for the flight from Miami?</li><li>“Minha mala não chegou.” — My '
                            'suitcase did not arrive.</li><li>“Minha mala está danificada.” — My '
                            'suitcase is damaged.</li><li>“Com quem eu posso falar?” — Who can I speak '
                            'to?</li><li>“Aqui está a etiqueta da bagagem.” — Here is the baggage '
                            'tag.</li><li>“Preciso registrar uma ocorrência.” — I need to file a '
                            'report.</li></ul>',
                            '<p>If you are nervous, keep the sentence simple:</p>',
                            '<p><strong>“Minha mala não chegou. Você pode me ajudar?”</strong><br>My '
                            'suitcase did not arrive. Can you help me?</p>',
                            '<p>This is enough to start the interaction.</p>']},
                  {'heading': 'Step 4: Portuguese for airport transport',
                   'body': ['<p>Airport transport in Brazil may involve taxi, Uber, private transfer, '
                            'bus or metro, depending on the city. Your main goal is to confirm the '
                            'location, price, address and safety of the ride.</p>',
                            '<p>Useful vocabulary:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portuguese</th><th>English</th></tr></thead><tbody><tr><td>táxi</td><td>taxi</td></tr><tr><td>aplicativo</td><td>app</td></tr><tr><td>Uber</td><td>Uber</td></tr><tr><td>motorista</td><td>driver</td></tr><tr><td>endereço</td><td>address</td></tr><tr><td>destino</td><td>destination</td></tr><tr><td>saída</td><td>exit</td></tr><tr><td>embarque</td><td>boarding '
                            '/ pickup</td></tr><tr><td>desembarque</td><td>arrivals / '
                            'drop-off</td></tr><tr><td>preço</td><td>price</td></tr><tr><td>cartão</td><td>card</td></tr><tr><td>dinheiro</td><td>cash</td></tr></tbody></table>',
                            '<p>Useful questions:</p>',
                            '<ul><li>“Onde eu pego o Uber?” — Where do I take the Uber?</li><li>“Onde '
                            'fica o ponto de táxi?” — Where is the taxi stand?</li><li>“Esse é o '
                            'endereço?” — Is this the address?</li><li>“Quanto custa até o hotel?” — '
                            'How much does it cost to the hotel?</li><li>“Aceita cartão?” — Do you '
                            'accept cards?</li><li>“Pode me deixar na entrada do hotel?” — Can you '
                            'drop me off at the hotel entrance?</li><li>“Quanto tempo demora?” — How '
                            'long does it take?</li></ul>',
                            '<p>A practical phrase for drivers:</p>',
                            '<p><strong>“Meu destino é este endereço.”</strong><br>My destination is '
                            'this address.</p>',
                            '<p>Then show the address on your phone.</p>',
                            '<p>Another useful phrase:</p>',
                            '<p><strong>“Pode confirmar o nome do hotel?”</strong><br>Can you confirm '
                            'the name of the hotel?</p>',
                            '<p>This helps avoid confusion, especially in large cities with hotels '
                            'that have similar names.</p>']},
                  {'heading': 'Step 5: Portuguese for your first hotel check-in',
                   'body': ['<p>Hotel check-in is one of the most important first interactions in '
                            'Brazil. You may need to show your passport, confirm your reservation, ask '
                            'about payment, breakfast, Wi-Fi and check-out.</p>',
                            '<p>Useful vocabulary:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portuguese</th><th>English</th></tr></thead><tbody><tr><td>reserva</td><td>reservation</td></tr><tr><td>check-in</td><td>check-in</td></tr><tr><td>check-out</td><td>check-out</td></tr><tr><td>passaporte</td><td>passport</td></tr><tr><td>documento</td><td>ID '
                            '/ '
                            'document</td></tr><tr><td>quarto</td><td>room</td></tr><tr><td>diária</td><td>daily '
                            'rate</td></tr><tr><td>café da '
                            'manhã</td><td>breakfast</td></tr><tr><td>senha do Wi-Fi</td><td>Wi-Fi '
                            'password</td></tr><tr><td>elevador</td><td>elevator</td></tr><tr><td>recepção</td><td>reception</td></tr><tr><td>pagamento</td><td>payment</td></tr><tr><td>cartão '
                            'de crédito</td><td>credit card</td></tr></tbody></table>',
                            '<p>Useful phrases:</p>',
                            '<ul><li>“Tenho uma reserva.” — I have a reservation.</li><li>“A reserva '
                            'está no nome de...” — The reservation is under the name...</li><li>“Aqui '
                            'está meu passaporte.” — Here is my passport.</li><li>“O café da manhã '
                            'está incluído?” — Is breakfast included?</li><li>“Qual é a senha do '
                            'Wi-Fi?” — What is the Wi-Fi password?</li><li>“Qual é o horário do '
                            'check-out?” — What time is check-out?</li><li>“Onde fica o elevador?” — '
                            'Where is the elevator?</li><li>“Posso pagar com cartão?” — Can I pay by '
                            'card?</li><li>“Vocês aceitam cartão internacional?” — Do you accept '
                            'international cards?</li><li>“Posso deixar minha mala aqui?” — Can I '
                            'leave my suitcase here?</li></ul>',
                            '<p>A complete check-in phrase:</p>',
                            '<p><strong>“Boa noite. Tenho uma reserva no nome de Anna '
                            'Smith.”</strong><br>Good evening. I have a reservation under the name '
                            'Anna Smith.</p>',
                            '<p>If there is a problem:</p>',
                            '<p><strong>“Acho que houve um problema com a reserva.”</strong><br>I '
                            'think there was a problem with the reservation.</p>',
                            '<p>Then show the confirmation email.</p>']},
                  {'heading': 'Step 6: Questions to ask at reception',
                   'body': ['<p>Reception is not only for check-in. It is also where you can solve '
                            'many first-day questions. In Brazil, hotel reception can help with '
                            'transport, food, safety, directions and local recommendations.</p>',
                            '<p>Useful questions:</p>',
                            '<ul><li>“Tem restaurante perto daqui?” — Is there a restaurant near '
                            'here?</li><li>“É seguro andar a pé aqui à noite?” — Is it safe to walk '
                            'here at night?</li><li>“Vocês chamam táxi?” — Can you call a '
                            'taxi?</li><li>“Tem mercado por perto?” — Is there a market '
                            'nearby?</li><li>“Como eu chego ao metrô?” — How do I get to the '
                            'metro?</li><li>“Qual é o melhor jeito de ir para o aeroporto?” — What is '
                            'the best way to go to the airport?</li><li>“Tem adaptador de tomada?” — '
                            'Do you have a power adapter?</li><li>“Posso pedir comida por aplicativo?” '
                            '— Can I order food through an app?</li><li>“Vocês têm serviço de '
                            'lavanderia?” — Do you have laundry service?</li></ul>',
                            '<p>A very useful polite structure is:</p>',
                            '<p><strong>“Você pode me recomendar...?”</strong><br>Can you '
                            'recommend...?</p>',
                            '<p>Examples:</p>',
                            '<ul><li>“Você pode me recomendar um restaurante?”</li><li>“Você pode me '
                            'recomendar uma farmácia?”</li><li>“Você pode me recomendar um transporte '
                            'seguro?”</li></ul>',
                            '<p>This sounds natural and respectful.</p>']},
                  {'heading': 'Step 7: Essential vocabulary for your first 24 hours in Brazil',
                   'body': ['<p>Your first 24 hours require vocabulary that helps you move, rest, eat, '
                            'connect and ask for support.</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portuguese</th><th>English</th></tr></thead><tbody><tr><td>água</td><td>water</td></tr><tr><td>comida</td><td>food</td></tr><tr><td>banheiro</td><td>bathroom</td></tr><tr><td>quarto</td><td>room</td></tr><tr><td>chave</td><td>key</td></tr><tr><td>cartão</td><td>card</td></tr><tr><td>dinheiro</td><td>cash</td></tr><tr><td>internet</td><td>internet</td></tr><tr><td>tomada</td><td>power '
                            'outlet</td></tr><tr><td>adaptador</td><td>adapter</td></tr><tr><td>farmácia</td><td>pharmacy</td></tr><tr><td>mercado</td><td>market</td></tr><tr><td>restaurante</td><td>restaurant</td></tr><tr><td>rua</td><td>street</td></tr><tr><td>entrada</td><td>entrance</td></tr><tr><td>saída</td><td>exit</td></tr><tr><td>ajuda</td><td>help</td></tr><tr><td>emergência</td><td>emergency</td></tr><tr><td>agora</td><td>now</td></tr><tr><td>amanhã</td><td>tomorrow</td></tr><tr><td>hoje</td><td>today</td></tr></tbody></table>',
                            '<p>Turn vocabulary into phrases:</p>',
                            '<ul><li>“Preciso de água.” — I need water.</li><li>“Onde fica a '
                            'farmácia?” — Where is the pharmacy?</li><li>“A chave não está '
                            'funcionando.” — The key is not working.</li><li>“A internet não está '
                            'funcionando.” — The internet is not working.</li><li>“Preciso de um '
                            'adaptador.” — I need an adapter.</li><li>“Tem restaurante no hotel?” — Is '
                            'there a restaurant in the hotel?</li></ul>',
                            '<p>Vocabulary is useful only when you can use it in sentences. That is '
                            'why live-class practice matters.</p>']},
                  {'heading': 'Live-class practice: airport and hotel role-play',
                   'body': ['<p>The best way to prepare for airport arrival and hotel check-in is to '
                            'practice role-plays before traveling. In live Portuguese classes, the '
                            'teacher can simulate the exact situations you will face and correct your '
                            'pronunciation, structure and tone.</p>',
                            '<p>Here are useful role-plays:</p>',
                            '<h3>Role-play 1: Asking for baggage claim</h3>',
                            '<p>Student asks:</p>',
                            '<ul><li>“Onde fica a retirada de bagagem?”</li><li>“Minha mala não '
                            'chegou.”</li><li>“Você pode me ajudar?”</li></ul>',
                            '<p>Teacher responds with realistic airport language.</p>',
                            '<h3>Role-play 2: Finding transport</h3>',
                            '<p>Student practices:</p>',
                            '<ul><li>“Onde eu pego o Uber?”</li><li>“Quanto custa até o '
                            'hotel?”</li><li>“Esse é o endereço?”</li></ul>',
                            '<p>Teacher gives different answers so the student learns to react.</p>',
                            '<h3>Role-play 3: Hotel check-in</h3>',
                            '<p>Student says:</p>',
                            '<ul><li>“Tenho uma reserva no nome de...”</li><li>“Aqui está meu '
                            'passaporte.”</li><li>“Qual é o horário do check-out?”</li></ul>',
                            '<p>Teacher acts as receptionist and asks follow-up questions.</p>',
                            '<h3>Role-play 4: Solving a hotel problem</h3>',
                            '<p>Student explains:</p>',
                            '<ul><li>“A internet não está funcionando.”</li><li>“A chave do quarto não '
                            'funciona.”</li><li>“Preciso de uma toalha, por favor.”</li></ul>',
                            '<p>Teacher corrects grammar and helps make the request sound natural.</p>',
                            '<p>This is where live Portuguese classes are much stronger than '
                            'memorizing a list. Real interaction requires listening, responding and '
                            'adjusting.</p>',
                            '<p>CTA: Want to practice your first airport and hotel conversations '
                            'before arriving in Brazil? Book a free level check at <a '
                            'href="/en/portuguese-placement-test">https://vediums.com/</a> and start '
                            'with live Brazilian Portuguese classes.</p>']},
                  {'heading': 'How to sound polite in Brazilian Portuguese',
                   'body': ['<p>To sound polite in Brazilian Portuguese, combine simple phrases with '
                            'warmth. Use “por favor”, “com licença”, “desculpa” and '
                            '“obrigado/obrigada.” You do not need complex grammar to sound '
                            'respectful.</p>',
                            '<p>Useful polite expressions:</p>',
                            '<ul><li>“Com licença.” — Excuse me.</li><li>“Por favor.” — '
                            'Please.</li><li>“Desculpa.” — Sorry / excuse me.</li><li>“Muito '
                            'obrigado.” — Thank you very much. (said by men)</li><li>“Muito obrigada.” '
                            '— Thank you very much. (said by women)</li><li>“Você pode me ajudar?” — '
                            'Can you help me?</li><li>“Eu gostaria de...” — I would '
                            'like...</li><li>“Será que você pode...?” — Would it be possible for you '
                            'to...?</li></ul>',
                            '<p>“Será que” is very common in Brazil and softens a request. For '
                            'example:</p>',
                            '<p><strong>“Será que você pode falar mais devagar?”</strong><br>Would it '
                            'be possible for you to speak more slowly?</p>',
                            '<p>This sounds polite and natural.</p>']},
                  {'heading': 'What if you do not understand the answer?',
                   'body': ['<p>If you do not understand the answer, do not panic. Use repair phrases. '
                            'These are phrases that help fix communication when something breaks '
                            'down.</p>',
                            '<p>Memorize these:</p>',
                            '<ul><li>“Desculpa, não entendi.” — Sorry, I did not '
                            'understand.</li><li>“Pode repetir?” — Can you repeat?</li><li>“Pode falar '
                            'mais devagar?” — Can you speak more slowly?</li><li>“Pode escrever?” — '
                            'Can you write it down?</li><li>“Como se escreve?” — How do you spell '
                            'it?</li><li>“Você pode mostrar no mapa?” — Can you show me on the '
                            'map?</li><li>“Você pode mandar por WhatsApp?” — Can you send it by '
                            'WhatsApp?</li></ul>',
                            '<p>These phrases are extremely useful because they keep the conversation '
                            'alive. You do not need to understand everything the first time.</p>']},
                  {'heading': 'Why live Portuguese classes are the best next step before traveling',
                   'body': ['<p>Live Portuguese classes are the best next step because your first days '
                            'in Brazil involve real people, not textbook dialogues. You need to '
                            'practice listening to different speeds, asking for clarification, '
                            'pronouncing key phrases and solving practical situations.</p>',
                            '<p>Recorded lessons and apps can help with vocabulary, but they do not '
                            'fully prepare you for unpredictable conversation. At an airport or hotel, '
                            'you may hear a different accent, background noise, fast speech or '
                            'unexpected questions.</p>',
                            '<p>With live classes, you can:</p>',
                            '<ul><li>practice your exact travel scenario;</li><li>learn Brazilian '
                            'pronunciation;</li><li>receive correction in real time;</li><li>role-play '
                            'airport and hotel situations;</li><li>ask questions about Brazilian '
                            'culture;</li><li>build confidence before arrival;</li><li>learn what to '
                            'say when you do not understand.</li></ul>',
                            '<p>Vedium offers live online Brazilian Portuguese classes for foreigners, '
                            'expats and international professionals. The focus is practical '
                            'communication with cultural intelligence. There are no long-term loyalty '
                            'contracts. You stay because you see progress.</p>']},
                  {'heading': 'How to prepare in one week before your trip',
                   'body': ['<p>If your trip is close, focus on high-impact phrases. You do not need '
                            'to learn everything. You need to prepare for the first interactions.</p>',
                            '<p>A one-week plan:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Day</th><th>Focus</th></tr></thead><tbody><tr><td>Day '
                            '1</td><td>Greetings and “I speak a little '
                            'Portuguese”</td></tr><tr><td>Day 2</td><td>Airport directions and '
                            'baggage</td></tr><tr><td>Day 3</td><td>Transport to '
                            'hotel</td></tr><tr><td>Day 4</td><td>Hotel check-in</td></tr><tr><td>Day '
                            '5</td><td>Wi-Fi, breakfast and check-out questions</td></tr><tr><td>Day '
                            '6</td><td>Problem-solving phrases</td></tr><tr><td>Day 7</td><td>Live '
                            'role-play or full review</td></tr></tbody></table>',
                            '<p>Practice aloud every day. Speaking is not only mental. Your mouth '
                            'needs to get used to the sounds.</p>']},
                  {'heading': 'Conclusion with strong CTA',
                   'body': ['<p>Your first airport arrival and hotel check-in in Brazil do not require '
                            'perfect Portuguese. They require practical, clear and polite '
                            'communication. If you can ask where to go, request repetition, confirm '
                            'transport, show your reservation, ask about breakfast and solve small '
                            'problems, your first hours in Brazil become much easier.</p>',
                            '<p>Brazilian Portuguese for foreigners should start with real life: '
                            'airports, hotels, transport, food, housing, work and daily confidence. '
                            'Grammar matters, but communication comes first when you are arriving in a '
                            'new country.</p>',
                            '<p>Vedium helps foreigners and expats learn Brazilian Portuguese through '
                            'live online classes, practical situations and cultural context. You '
                            'practice with real interaction, receive correction and prepare for Brazil '
                            'as it is actually lived. There are no long-term contracts. You continue '
                            'because the classes help you feel more confident.</p>',
                            '<p>Book your free level check at <a '
                            'href="/en/learn-portuguese-brazil">https://vediums.com/</a> and start '
                            'preparing your Portuguese for arrival in Brazil.</p>']}],
     'faqs': [{'q': 'Do I need Portuguese at Brazilian airports?',
               'a': 'You can often manage with English in major airports, but basic Portuguese is very '
                    'helpful for baggage, transport, directions, delays, hotel transfers and asking '
                    'for help when English is not available.'},
              {'q': 'What should I say when I do not understand Portuguese?',
               'a': 'Say “Desculpa, não entendi. Pode repetir, por favor?” You can also say “Pode '
                    'falar mais devagar?” to ask the person to speak more slowly.'},
              {'q': 'How do I say I have a hotel reservation in Portuguese?',
               'a': 'Say “Tenho uma reserva” or “Tenho uma reserva no nome de...” followed by your '
                    'name. This is the most useful phrase for hotel check-in.'},
              {'q': 'Are live Portuguese classes useful before traveling to Brazil?',
               'a': 'Yes. Live classes help you practice real airport, hotel and transport situations, '
                    'improve pronunciation and learn how to react when the answer is different from '
                    'what you expected.'},
              {'q': 'Does Vedium teach Brazilian Portuguese for foreigners?',
               'a': 'Yes. Vedium offers live online Brazilian Portuguese classes for foreigners, '
                    'expats and international professionals, focused on practical communication, '
                    'cultural context and real-life confidence.'}],
     'cta_title': 'Want to know your real Portuguese level?',
     'cta_text': "Take Vedium's free placement test and find out where to start.",
     'cta_label': 'Learn about the Portuguese course',
     'cta_url': '/en/learn-portuguese-brazil'},
    "portuguese-for-brazil-a-realistic-study-path-from-a1-to-b1": {'title': 'Portuguese for Brazil: a realistic study path from A1 to B1',
     'meta_description': 'Learn a realistic A1 to B1 study path for Brazilian Portuguese, with '
                         'practical steps for living, working and speaking confidently in Brazil.',
     'h1': 'Portuguese for Brazil: a realistic study path from A1 to B1',
     'date': '2026-07-01',
     'date_display': 'July 1, 2026',
     'hero_image': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aprender português como língua estrangeira',
     'tag': 'Brazilian Portuguese',
     'lang': 'en',
     'category': 'brazilian-portuguese',
     'lead': 'A realistic path from A1 to B1 in Portuguese for Brazil should focus on real-life '
             'communication first: greetings, survival phrases, daily routines, work situations, '
             'services, housing, transport, healthcare and social confidence. Grammar matters, but for '
             'expats, relocation teams and international professionals, the goal is not to “study '
             'Portuguese in theory.” The goal is to live, work and interact in Brazil with more '
             'independence.',
     'sections': [{'heading': '',
                   'body': ['<p>Brazilian Portuguese is the version of Portuguese you need if you are '
                            'moving to Brazil, working with Brazilian teams, managing daily life in '
                            'São Paulo, Rio de Janeiro, Brasília, Curitiba, Recife or any other '
                            'Brazilian city, or preparing employees before arrival. It has its own '
                            'pronunciation, rhythm, informal expressions, cultural expectations and '
                            'workplace communication style. A course designed for Portugal will not '
                            'fully prepare you for Brazilian daily life.</p>',
                            '<p>This guide explains how to move from A1 to B1 with a practical, '
                            'Brazil-specific study path. It is made for learners who want clarity: '
                            'what to learn first, what to practice at each level, how long progress '
                            'may take, and why live classes can make the difference between “knowing '
                            'words” and actually speaking.</p>']},
                  {'heading': 'What does A1 to B1 mean in Brazilian Portuguese?',
                   'body': ['<p>A1 to B1 means moving from basic survival communication to independent '
                            'everyday communication. At A1, you can introduce yourself and handle very '
                            'simple interactions. At B1, you can manage common situations in Brazil, '
                            'explain needs, talk about work and daily life, and participate in '
                            'conversations with more confidence.</p>',
                            '<p>The levels are useful because they give structure. But the real '
                            'question is: what should each level allow you to do in Brazil?</p>',
                            '<p>At <strong>A1</strong>, you should be able to:</p>',
                            '<ul><li>greet people and introduce yourself;</li><li>say where you are '
                            'from and what you do;</li><li>ask simple questions;</li><li>understand '
                            'very basic signs and instructions;</li><li>order food and drinks with '
                            'support;</li><li>use numbers, dates, times and basic '
                            'directions;</li><li>talk about your routine using simple '
                            'sentences.</li></ul>',
                            '<p>At <strong>A2</strong>, you should be able to:</p>',
                            '<ul><li>handle common daily interactions;</li><li>speak with building '
                            'staff, drivers, receptionists and store attendants;</li><li>explain '
                            'simple needs;</li><li>schedule appointments;</li><li>describe your home, '
                            'job and plans;</li><li>understand slow, clear '
                            'conversations;</li><li>participate in predictable social '
                            'situations.</li></ul>',
                            '<p>At <strong>B1</strong>, you should be able to:</p>',
                            '<ul><li>solve everyday problems with more autonomy;</li><li>explain '
                            'situations at work;</li><li>talk about past experiences and future '
                            'plans;</li><li>participate in informal conversations;</li><li>understand '
                            'the main idea of conversations around you;</li><li>write simple messages '
                            'and emails;</li><li>express opinions with basic '
                            'structure;</li><li>navigate Brazil with more confidence.</li></ul>',
                            '<p>For someone relocating to Brazil, B1 is a powerful milestone. It does '
                            'not mean native fluency. It means you can function. You can ask for help, '
                            'explain what happened, understand context, join conversations and reduce '
                            'the stress of daily life.</p>']},
                  {'heading': 'Why should Portuguese for Brazil be practical from day one?',
                   'body': ['<p>Portuguese for Brazil should be practical from day one because real '
                            'life starts before grammar feels complete. Expats and international '
                            'professionals need to speak with people in apartments, schools, offices, '
                            'banks, restaurants, transportation apps, gyms, clinics and '
                            'government-related situations.</p>',
                            '<p>Many learners make the mistake of waiting too long before speaking. '
                            'They study verb charts, memorize lists and use apps, but when they arrive '
                            'in Brazil, they still freeze when someone says “Pois não?”, “Tudo '
                            'certo?”, “CPF na nota?” or “Pode deixar.”</p>',
                            '<p>A Brazil-focused learning path should include:</p>',
                            '<ul><li>real pronunciation and listening practice;</li><li>informal and '
                            'polite expressions used in Brazil;</li><li>essential vocabulary for daily '
                            'life;</li><li>workplace communication;</li><li>cultural '
                            'expectations;</li><li>confidence-building speaking '
                            'practice;</li><li>correction from a teacher in live classes.</li></ul>',
                            '<p>Brazilian Portuguese is not only a language system. It is also a '
                            'social experience. Brazilians often use warm greetings, indirect '
                            'phrasing, small talk and flexible conversational patterns. Understanding '
                            'this helps you sound more natural and feel less lost.</p>',
                            '<p>At Vedium, the approach to Portuguese for foreigners is built around '
                            'live classes, real-life situations and cultural intelligence. The idea is '
                            'not only to teach grammar, but to help learners feel at home in '
                            'Portuguese.</p>',
                            '<p>CTA: If you are preparing to live or work in Brazil, book a free level '
                            'check at <a href="/en/learn-portuguese-brazil">https://vediums.com/</a> '
                            'and understand where your Portuguese should start.</p>']},
                  {'heading': 'Stage 1: A1 Portuguese for Brazil — building survival confidence',
                   'body': ['<p>A1 should give you your first layer of independence. The goal is not '
                            'complex conversation. The goal is to stop feeling completely dependent in '
                            'simple interactions.</p>',
                            '<p>At this level, you should focus on pronunciation, greetings, personal '
                            'information, numbers, basic verbs and practical phrases. You should also '
                            'learn how Brazilian Portuguese sounds in real speech, because the written '
                            'word can look easier than the spoken version.</p>',
                            '<h3>Essential A1 situations</h3>',
                            '<p>Start with situations you will face immediately in Brazil:</p>',
                            '<ul><li>saying hello and goodbye;</li><li>introducing '
                            'yourself;</li><li>spelling your name;</li><li>saying your '
                            'nationality;</li><li>giving your phone number;</li><li>asking for the '
                            'price;</li><li>ordering coffee or food;</li><li>taking an Uber or '
                            'taxi;</li><li>asking where something is;</li><li>understanding “yes”, '
                            '“no”, “maybe”, “now”, “later”;</li><li>saying you do not '
                            'understand;</li><li>asking someone to repeat.</li></ul>',
                            '<p>Useful phrases include:</p>',
                            '<ul><li>“Oi, tudo bem?” — Hi, how are you?</li><li>“Eu sou dos Estados '
                            'Unidos.” — I am from the United States.</li><li>“Eu não entendi.” — I did '
                            'not understand.</li><li>“Pode repetir, por favor?” — Can you repeat, '
                            'please?</li><li>“Quanto custa?” — How much is it?</li><li>“Onde fica o '
                            'banheiro?” — Where is the bathroom?</li><li>“Eu estou aprendendo '
                            'português.” — I am learning Portuguese.</li></ul>',
                            '<p>At A1, pronunciation matters. Learners should practice nasal sounds, '
                            'open and closed vowels, the Brazilian “r” in different positions and the '
                            'rhythm of common phrases. This is one reason live classes help: a teacher '
                            'can correct small habits before they become difficult to change.</p>',
                            '<h3>A1 grammar that matters</h3>',
                            '<p>Grammar should support communication. At A1, prioritize:</p>',
                            '<ul><li>personal pronouns;</li><li>present tense of common '
                            'verbs;</li><li>gender and plural basics;</li><li>articles;</li><li>simple '
                            'questions;</li><li>negation;</li><li>basic prepositions;</li><li>numbers '
                            'and time expressions.</li></ul>',
                            '<p>Do not try to learn everything at once. A1 works best when grammar '
                            'appears inside real sentences. For example, instead of studying “ser” and '
                            '“estar” only as a rule, practice:</p>',
                            '<ul><li>“Eu sou professor.”</li><li>“Eu estou no Brasil.”</li><li>“Ela é '
                            'brasileira.”</li><li>“Nós estamos em São Paulo.”</li></ul>',
                            '<p>This builds function, not just theory.</p>']},
                  {'heading': 'Stage 2: A2 Portuguese for Brazil — handling daily life',
                   'body': ['<p>A2 is where learners start feeling more capable. You can survive '
                            'simple situations at A1, but at A2 you begin to manage daily life with '
                            'less panic and more flexibility.</p>',
                            '<p>The focus should move from isolated phrases to short conversations. '
                            'You need to understand questions, respond with context and explain basic '
                            'needs.</p>',
                            '<h3>Essential A2 situations</h3>',
                            '<p>A2 learners should practice:</p>',
                            '<ul><li>renting an apartment or talking to building staff;</li><li>asking '
                            'about maintenance problems;</li><li>going to the '
                            'pharmacy;</li><li>booking appointments;</li><li>speaking at reception '
                            'desks;</li><li>talking about work routines;</li><li>describing '
                            'symptoms;</li><li>making small talk;</li><li>buying clothes or household '
                            'items;</li><li>asking for recommendations;</li><li>understanding delivery '
                            'instructions;</li><li>communicating with service providers.</li></ul>',
                            '<p>This level is especially important for expats because Brazil has many '
                            'daily interactions that require spoken communication. Even if many '
                            'professionals speak English in global companies, daily life outside work '
                            'often happens in Portuguese.</p>',
                            '<p>Useful A2 phrases include:</p>',
                            '<ul><li>“Eu preciso marcar uma consulta.” — I need to schedule an '
                            'appointment.</li><li>“Meu apartamento está com um problema.” — My '
                            'apartment has a problem.</li><li>“Você pode me ajudar?” — Can you help '
                            'me?</li><li>“Eu gostaria de pagar com cartão.” — I would like to pay by '
                            'card.</li><li>“Qual é o melhor horário?” — What is the best '
                            'time?</li><li>“Eu trabalho em uma empresa internacional.” — I work at an '
                            'international company.</li><li>“Eu cheguei ao Brasil há pouco tempo.” — I '
                            'arrived in Brazil recently.</li></ul>',
                            '<p>At this stage, you should also learn common Brazilian conversational '
                            'markers such as “então”, “tipo”, “né”, “tá bom”, “beleza”, “combinado” '
                            'and “pois é.” These words may look small, but they appear constantly in '
                            'real conversations.</p>',
                            '<h3>A2 grammar that matters</h3>',
                            '<p>At A2, focus on:</p>',
                            '<ul><li>past tense for common events;</li><li>future expressions with “ir '
                            '+ verb”;</li><li>reflexive verbs used in routine;</li><li>modal verbs '
                            'such as “poder”, “querer”, “precisar”;</li><li>comparison;</li><li>object '
                            'pronouns in common use;</li><li>more question '
                            'structures;</li><li>connectors like “porque”, “mas”, “então”, '
                            '“também”.</li></ul>',
                            '<p>The goal is to tell simple stories and explain practical needs. For '
                            'example:</p>',
                            '<ul><li>“Ontem eu fui ao mercado.”</li><li>“Amanhã eu vou trabalhar de '
                            'casa.”</li><li>“Eu preciso falar com o porteiro.”</li><li>“Eu queria '
                            'saber se tem vaga.”</li><li>“Eu não consegui entender a '
                            'mensagem.”</li></ul>',
                            '<p>These sentences are the bridge between beginner Portuguese and '
                            'real-life autonomy.</p>']},
                  {'heading': 'Stage 3: B1 Portuguese for Brazil — becoming independent',
                   'body': ['<p>B1 is the level where Portuguese begins to feel usable in a wider '
                            'range of situations. You still make mistakes, but you can keep going. You '
                            'can explain, ask, clarify and participate.</p>',
                            '<p>For relocation, B1 is often the most practical target because it gives '
                            'employees and families enough confidence to interact beyond scripted '
                            'situations.</p>',
                            '<h3>Essential B1 situations</h3>',
                            '<p>At B1, you should practice:</p>',
                            '<ul><li>explaining a problem in detail;</li><li>telling stories about '
                            'past experiences;</li><li>discussing work tasks;</li><li>joining social '
                            'conversations;</li><li>giving opinions;</li><li>understanding the main '
                            'point of meetings;</li><li>writing simple professional '
                            'messages;</li><li>managing travel inside Brazil;</li><li>talking to '
                            'schools, doctors or service providers;</li><li>handling misunderstandings '
                            'politely;</li><li>asking follow-up questions.</li></ul>',
                            '<p>Useful B1 phrases include:</p>',
                            '<ul><li>“Na minha opinião...” — In my opinion...</li><li>“O principal '
                            'problema é...” — The main problem is...</li><li>“Eu gostaria de entender '
                            'melhor...” — I would like to understand better...</li><li>“Aconteceu um '
                            'imprevisto.” — Something unexpected happened.</li><li>“Você pode me '
                            'explicar como funciona?” — Can you explain how it works?</li><li>“Eu '
                            'ainda estou aprendendo, mas consigo acompanhar.” — I am still learning, '
                            'but I can follow.</li></ul>',
                            '<p>At B1, learners need guided conversation. This is where live classes '
                            'become even more valuable. You need correction, role-play, feedback and '
                            'exposure to natural Brazilian speech. You also need confidence to keep '
                            'speaking even when your sentence is not perfect.</p>',
                            '<h3>B1 grammar that matters</h3>',
                            '<p>At B1, prioritize:</p>',
                            '<ul><li>past tense contrast;</li><li>future and conditional '
                            'expressions;</li><li>opinions and justification;</li><li>connectors for '
                            'longer speech;</li><li>indirect requests;</li><li>relative '
                            'clauses;</li><li>common uses of subjunctive in fixed '
                            'expressions;</li><li>formal and informal register.</li></ul>',
                            '<p>The goal is not to sound academic. The goal is to be understandable, '
                            'polite and capable of navigating Brazil.</p>']},
                  {'heading': 'A realistic timeline from A1 to B1',
                   'body': ['<p>A realistic timeline depends on your native language, study frequency, '
                            'exposure to Portuguese and speaking practice. However, many motivated '
                            'learners can move from A1 foundations toward B1 communication with '
                            'consistent weekly study, especially when they combine live classes with '
                            'independent practice.</p>',
                            '<p>A practical rhythm could be:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Stage</th><th>Focus</th><th>Suggested '
                            'duration</th></tr></thead><tbody><tr><td>A1 foundation</td><td>Survival '
                            'phrases, pronunciation, basic grammar</td><td>8 to 12 '
                            'weeks</td></tr><tr><td>A2 development</td><td>Daily-life conversations '
                            'and practical tasks</td><td>12 to 16 weeks</td></tr><tr><td>B1 '
                            'transition</td><td>Independent communication and work/social '
                            'situations</td><td>16 to 24 weeks</td></tr></tbody></table>',
                            '<p>This is not a promise of guaranteed fluency. It is a realistic study '
                            'path. Some learners move faster because they live in Brazil and practice '
                            'daily. Others need more time because they study from abroad or have '
                            'limited contact with the language.</p>',
                            '<p>The key is consistency. One live class per week plus short practice '
                            'sessions can already create progress. Two or three live sessions per week '
                            'can accelerate confidence, especially for employees preparing for '
                            'relocation.</p>']},
                  {'heading': 'How live classes help you progress faster',
                   'body': ['<p>Live classes help because they turn passive knowledge into active '
                            'communication. Apps and recorded lessons can introduce vocabulary, but '
                            'they cannot fully simulate the pressure and rhythm of a real '
                            'conversation.</p>',
                            '<p>In live Brazilian Portuguese classes, you can:</p>',
                            '<ul><li>practice pronunciation with correction;</li><li>ask questions in '
                            'real time;</li><li>role-play situations you will face in '
                            'Brazil;</li><li>receive feedback on grammar and word '
                            'choice;</li><li>learn cultural context;</li><li>build speaking '
                            'confidence;</li><li>stay accountable.</li></ul>',
                            '<p>This is especially important for relocation teams. Employees do not '
                            'only need to “know Portuguese.” They need to interact with colleagues, '
                            'landlords, schools, doctors, drivers and neighbors. They need practical '
                            'language and cultural confidence before and after arrival.</p>',
                            '<p>Vedium offers live online classes with no long-term loyalty contracts. '
                            'That matters because the relationship is based on results, not pressure. '
                            'Learners stay because they feel progress, not because they are '
                            'trapped.</p>',
                            '<p>CTA: Book a free level check at <a '
                            'href="/en/portuguese-placement-test">https://vediums.com/</a> and see '
                            'which Brazilian Portuguese level fits your relocation or work '
                            'goals.</p>']},
                  {'heading': 'Weekly study plan for A1 to B1 learners',
                   'body': ['<p>A realistic weekly plan should be simple enough to repeat. The best '
                            'plan combines live instruction, short independent practice and real-life '
                            'vocabulary.</p>',
                            '<p>For A1:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Day</th><th>Activity</th></tr></thead><tbody><tr><td>Monday</td><td>Review '
                            'greetings and pronunciation</td></tr><tr><td>Tuesday</td><td>Practice '
                            'numbers, time and basic questions</td></tr><tr><td>Wednesday</td><td>Live '
                            'class or guided speaking</td></tr><tr><td>Thursday</td><td>Listen to '
                            'short dialogues</td></tr><tr><td>Friday</td><td>Write five simple '
                            'sentences</td></tr><tr><td>Weekend</td><td>Practice one real-life '
                            'situation</td></tr></tbody></table>',
                            '<p>For A2:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Day</th><th>Activity</th></tr></thead><tbody><tr><td>Monday</td><td>Review '
                            'past tense in daily situations</td></tr><tr><td>Tuesday</td><td>Practice '
                            'service and apartment vocabulary</td></tr><tr><td>Wednesday</td><td>Live '
                            'conversation class</td></tr><tr><td>Thursday</td><td>Listen to Brazilian '
                            'audio or video</td></tr><tr><td>Friday</td><td>Write a short message in '
                            'Portuguese</td></tr><tr><td>Weekend</td><td>Role-play a practical '
                            'situation</td></tr></tbody></table>',
                            '<p>For B1:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Day</th><th>Activity</th></tr></thead><tbody><tr><td>Monday</td><td>Prepare '
                            'a short opinion</td></tr><tr><td>Tuesday</td><td>Practice work-related '
                            'vocabulary</td></tr><tr><td>Wednesday</td><td>Live class with '
                            'discussion</td></tr><tr><td>Thursday</td><td>Listen to natural Brazilian '
                            'speech</td></tr><tr><td>Friday</td><td>Write a professional '
                            'message</td></tr><tr><td>Weekend</td><td>Speak with a Brazilian or '
                            'simulate a real task</td></tr></tbody></table>',
                            '<p>The point is not perfection. The point is repetition and relevance. '
                            'Every week should include speaking, listening, vocabulary and a situation '
                            'connected to life in Brazil.</p>']},
                  {'heading': 'What relocation teams need before arrival',
                   'body': ['<p>Before arriving in Brazil, relocation teams need more than basic '
                            'vocabulary. They need a practical communication plan. This includes '
                            'survival Portuguese, cultural orientation and confidence to ask for '
                            'help.</p>',
                            '<p>A strong pre-arrival program should include:</p>',
                            '<ul><li>greetings and polite interaction;</li><li>pronunciation '
                            'basics;</li><li>transport and address vocabulary;</li><li>housing and '
                            'building communication;</li><li>food and restaurant '
                            'language;</li><li>health and pharmacy situations;</li><li>workplace '
                            'introductions;</li><li>emergency phrases;</li><li>Brazilian small '
                            'talk;</li><li>messaging etiquette;</li><li>common '
                            'misunderstandings.</li></ul>',
                            '<p>For companies, this is not just a language benefit. It supports '
                            'employee adaptation, reduces stress and improves integration. A '
                            'professional who can communicate basic needs in Portuguese often feels '
                            'more confident, more connected and more prepared to work in Brazil.</p>']},
                  {'heading': 'Conclusion with strong CTA',
                   'body': ['<p>Learning Portuguese for Brazil from A1 to B1 is not about memorizing '
                            'every grammar rule before you speak. It is about building practical '
                            'confidence step by step: first survival communication, then daily-life '
                            'interactions, then independent conversations for work, services and '
                            'social life.</p>',
                            '<p>A realistic path focuses on Brazil-specific situations, essential '
                            'vocabulary, pronunciation, cultural intelligence and live speaking '
                            'practice. This is the difference between studying Portuguese as a subject '
                            'and using Portuguese as a life skill.</p>',
                            '<p>Vedium helps foreigners, expats and relocation teams learn Brazilian '
                            'Portuguese through live online classes, practical content and cultural '
                            'depth. There are no long-term loyalty contracts. You continue because you '
                            'see progress.</p>',
                            '<p>Book your free level check at <a '
                            'href="/en/learn-portuguese-brazil">https://vediums.com/</a> and start '
                            'your Brazilian Portuguese path with clarity, confidence and real '
                            'conversation.</p>']}],
     'faqs': [{'q': 'How long does it take to go from A1 to B1 in Brazilian Portuguese?',
               'a': 'It depends on your study frequency, exposure and speaking practice. A realistic '
                    'path may take several months of consistent study, especially if you combine live '
                    'classes with weekly independent practice.'},
              {'q': 'Is Brazilian Portuguese different from European Portuguese?',
               'a': 'Yes. Brazilian Portuguese has different pronunciation, vocabulary, expressions '
                    'and communication habits. If you are moving to Brazil, you should study '
                    'Portuguese specifically for Brazil.'},
              {'q': 'What should I learn first before relocating to Brazil?',
               'a': 'Start with greetings, numbers, directions, transport, food, housing, healthcare, '
                    'basic work introductions and phrases to ask for repetition or help. These are the '
                    'most useful in your first weeks.'},
              {'q': 'Are live classes better than apps for Portuguese for foreigners?',
               'a': 'Apps can support vocabulary and repetition, but live classes are better for '
                    'speaking, correction, pronunciation and cultural context. For relocation, live '
                    'practice is especially important.'},
              {'q': 'Does Vedium offer Brazilian Portuguese classes for foreigners?',
               'a': 'Yes. Vedium offers live online Brazilian Portuguese classes for foreigners, '
                    'expats and relocation teams, with practical language, cultural context and no '
                    'long-term loyalty contracts.'}],
     'cta_title': 'Want to know your real Portuguese level?',
     'cta_text': "Take Vedium's free placement test and find out where to start.",
     'cta_label': 'Learn about the Portuguese course',
     'cta_url': '/en/learn-portuguese-brazil'},
    "portugues-brasileno-para-llegar-a-brasil-preparado": {'title': 'Portugués brasileño para llegar a Brasil preparado',
     'meta_description': 'Aprende portugués brasileño para llegar a Brasil preparado: situaciones '
                         'reales, vocabulario clave y práctica en clases en vivo.',
     'h1': 'Portugués brasileño para llegar a Brasil preparado',
     'date': '2026-06-10',
     'date_display': '10 de junio de 2026',
     'hero_image': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aula de português para estrangeiros na Vedium',
     'tag': 'Portugués brasileño',
     'lang': 'es',
     'category': 'portugues-brasileno',
     'lead': 'Llegar a Brasil preparado significa conocer el portugués brasileño que realmente se usa '
             'en la vida diaria: saludos, transporte, hotel, vivienda, trabajo, estudios, farmacia, '
             'restaurantes, pagos, WhatsApp y conversaciones básicas con brasileños. No necesitas '
             'hablar perfecto desde el primer día, pero sí necesitas entender y decir frases '
             'esenciales para moverte con más seguridad y menos dependencia del inglés o del español.',
     'sections': [{'heading': '',
                   'body': ['<p>Para hispanohablantes, Brasil puede parecer lingüísticamente cercano. '
                            'El portugués y el español comparten raíces, muchas palabras se parecen y '
                            'algunas frases se intuyen. Pero esa cercanía también puede engañar. '
                            'Entender un texto simple no es lo mismo que comprender a una persona '
                            'brasileña hablando rápido en una recepción, una reunión, una farmacia o '
                            'un edificio residencial. La pronunciación, los falsos amigos, el ritmo, '
                            'las expresiones informales y la cultura de comunicación son '
                            'diferentes.</p>',
                            '<p>Por eso, si vas a vivir, trabajar, estudiar o pasar una temporada '
                            'larga en Brasil, conviene estudiar específicamente Portuguese for Brazil: '
                            'portugués brasileño para situaciones reales. Un Brazilian Portuguese '
                            'course bien diseñado no debe limitarse a gramática aislada. Debe ayudarte '
                            'a hablar, escuchar, preguntar, confirmar información y entender la '
                            'cultura local.</p>',
                            '<p>En esta guía encontrarás un camino práctico para llegar a Brasil '
                            'preparado, con vocabulario clave, situaciones reales y ejercicios para '
                            'practicar en clases en vivo. La propuesta de Vedium es justamente esa: '
                            'enseñar portugués brasileño para extranjeros con clases online en vivo, '
                            'profundidad cultural y aprendizaje útil para la vida real.</p>']},
                  {'heading': '¿Por qué aprender portugués brasileño antes de llegar a Brasil?',
                   'body': ['<p>Aprender portugués brasileño antes de llegar a Brasil reduce la '
                            'ansiedad de los primeros días y te permite resolver situaciones prácticas '
                            'con más autonomía. Aunque algunas personas hablen inglés o entiendan '
                            'español, no puedes depender de eso en todos los contextos.</p>',
                            '<p>En Brasil, necesitarás comunicarte en situaciones como:</p>',
                            '<ul><li>llegada al aeropuerto;</li><li>transporte hasta tu '
                            'alojamiento;</li><li>check-in en hotel o '
                            'apartamento;</li><li>conversación con porteros y administradores de '
                            'edificio;</li><li>compras en supermercado;</li><li>pedidos en '
                            'restaurantes;</li><li>pagos con tarjeta;</li><li>consultas en '
                            'farmacia;</li><li>citas médicas;</li><li>reuniones de '
                            'trabajo;</li><li>clases, cursos o universidad;</li><li>mensajes por '
                            'WhatsApp;</li><li>conversaciones sociales.</li></ul>',
                            '<p>Muchas de estas interacciones son simples, pero ocurren cuando estás '
                            'cansado, con prisa o bajo presión. Por ejemplo, si tu maleta no llega, si '
                            'tu tarjeta no funciona o si necesitas explicar un problema con internet '
                            'en el apartamento, unas pocas frases correctas pueden hacer una gran '
                            'diferencia.</p>',
                            '<p>Aprender antes de llegar también te ayuda a evitar la dependencia del '
                            '“portuñol”. El portuñol puede servir para una emergencia, pero no siempre '
                            'es claro ni profesional. Para integrarte mejor, necesitas entender cómo '
                            'suena el portugués brasileño y cómo se expresan los brasileños en '
                            'situaciones cotidianas.</p>',
                            '<p>CTA: Si quieres llegar a Brasil con más seguridad lingüística, reserva '
                            'una prueba de nivel gratuita en <a '
                            'href="/es/portugues-para-extranjeros">https://vediums.com/</a> y descubre '
                            'por dónde empezar.</p>']},
                  {'heading': 'Situación real 1: llegada al aeropuerto',
                   'body': ['<p>La llegada al aeropuerto es uno de los primeros momentos en los que el '
                            'portugués brasileño puede ayudarte. Puede que necesites preguntar por '
                            'equipaje, transporte, dirección o ayuda.</p>',
                            '<p>Vocabulario clave:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portugués</th><th>Español</th></tr></thead><tbody><tr><td>aeroporto</td><td>aeropuerto</td></tr><tr><td>passaporte</td><td>pasaporte</td></tr><tr><td>visto</td><td>visa</td></tr><tr><td>bagagem</td><td>equipaje</td></tr><tr><td>mala</td><td>maleta</td></tr><tr><td>saída</td><td>salida</td></tr><tr><td>entrada</td><td>entrada</td></tr><tr><td>táxi</td><td>taxi</td></tr><tr><td>Uber</td><td>Uber</td></tr><tr><td>endereço</td><td>dirección</td></tr><tr><td>ajuda</td><td>ayuda</td></tr><tr><td>dinheiro</td><td>efectivo</td></tr><tr><td>cartão</td><td>tarjeta</td></tr></tbody></table>',
                            '<p>Frases útiles:</p>',
                            '<ul><li>“Com licença.” — Disculpe.</li><li>“Você pode me ajudar?” — '
                            '¿Puede ayudarme?</li><li>“Onde fica a retirada de bagagem?” — ¿Dónde está '
                            'la recogida de equipaje?</li><li>“Minha mala não chegou.” — Mi maleta no '
                            'llegó.</li><li>“Onde eu pego o Uber?” — ¿Dónde tomo el Uber?</li><li>“Meu '
                            'destino é este endereço.” — Mi destino es esta dirección.</li><li>“Pode '
                            'repetir, por favor?” — ¿Puede repetir, por favor?</li><li>“Eu falo pouco '
                            'português.” — Hablo poco portugués.</li></ul>',
                            '<p>Una frase especialmente útil es:</p>',
                            '<p><strong>“Desculpa, eu falo pouco português. Pode falar mais '
                            'devagar?”</strong><br>Disculpa, hablo poco portugués. ¿Puede hablar más '
                            'despacio?</p>',
                            '<p>Esta frase te permite explicar tu nivel y pedir apoyo sin sentir '
                            'vergüenza. En clases en vivo, puedes practicarla con diferentes '
                            'entonaciones y respuestas posibles.</p>']},
                  {'heading': 'Situación real 2: hotel, alojamiento y edificio',
                   'body': ['<p>Después del aeropuerto, el alojamiento es una prioridad. Puedes llegar '
                            'a un hotel, Airbnb, residencia universitaria o apartamento alquilado. En '
                            'todos los casos, necesitarás confirmar datos, documentos, horarios y '
                            'servicios.</p>',
                            '<p>Vocabulario clave:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portugués</th><th>Español</th></tr></thead><tbody><tr><td>reserva</td><td>reserva</td></tr><tr><td>quarto</td><td>habitación</td></tr><tr><td>check-in</td><td>check-in</td></tr><tr><td>check-out</td><td>check-out</td></tr><tr><td>documento</td><td>documento</td></tr><tr><td>passaporte</td><td>pasaporte</td></tr><tr><td>chave</td><td>llave</td></tr><tr><td>Wi-Fi</td><td>Wi-Fi</td></tr><tr><td>senha</td><td>contraseña</td></tr><tr><td>café '
                            'da '
                            'manhã</td><td>desayuno</td></tr><tr><td>recepção</td><td>recepción</td></tr><tr><td>portaria</td><td>portería</td></tr><tr><td>porteiro</td><td>portero</td></tr><tr><td>entrega</td><td>entrega '
                            '/ '
                            'paquete</td></tr><tr><td>manutenção</td><td>mantenimiento</td></tr></tbody></table>',
                            '<p>Frases útiles:</p>',
                            '<ul><li>“Tenho uma reserva.” — Tengo una reserva.</li><li>“A reserva está '
                            'no nome de...” — La reserva está a nombre de...</li><li>“Aqui está meu '
                            'passaporte.” — Aquí está mi pasaporte.</li><li>“Qual é a senha do Wi-Fi?” '
                            '— ¿Cuál es la contraseña del Wi-Fi?</li><li>“O café da manhã está '
                            'incluído?” — ¿El desayuno está incluido?</li><li>“Qual é o horário do '
                            'check-out?” — ¿Cuál es el horario del check-out?</li><li>“A chave não '
                            'está funcionando.” — La llave no está funcionando.</li><li>“A internet '
                            'não está funcionando.” — Internet no funciona.</li><li>“Chegou uma '
                            'entrega para mim?” — ¿Llegó una entrega para mí?</li></ul>',
                            '<p>Para quienes van a vivir en un edificio en Brasil, la palabra '
                            '<strong>portaria</strong> es muy importante. Se refiere a la recepción o '
                            'entrada del edificio, normalmente con un portero o equipo de control de '
                            'acceso. Esta interacción es muy común en la vida diaria brasileña.</p>']},
                  {'heading': 'Situación real 3: transporte y direcciones',
                   'body': ['<p>Moverse en Brasil puede exigir preguntas simples pero importantes. '
                            'Incluso si usas aplicaciones, puedes necesitar confirmar el punto de '
                            'encuentro, el destino o el tiempo de viaje.</p>',
                            '<p>Vocabulario clave:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portugués</th><th>Español</th></tr></thead><tbody><tr><td>rua</td><td>calle</td></tr><tr><td>avenida</td><td>avenida</td></tr><tr><td>metrô</td><td>metro</td></tr><tr><td>ônibus</td><td>autobús</td></tr><tr><td>estação</td><td>estación</td></tr><tr><td>motorista</td><td>conductor</td></tr><tr><td>destino</td><td>destino</td></tr><tr><td>caminho</td><td>camino</td></tr><tr><td>perto</td><td>cerca</td></tr><tr><td>longe</td><td>lejos</td></tr><tr><td>direita</td><td>derecha</td></tr><tr><td>esquerda</td><td>izquierda</td></tr><tr><td>aqui</td><td>aquí</td></tr><tr><td>ali</td><td>allí</td></tr></tbody></table>',
                            '<p>Frases útiles:</p>',
                            '<ul><li>“Como eu chego lá?” — ¿Cómo llego allí?</li><li>“É perto daqui?” '
                            '— ¿Está cerca de aquí?</li><li>“É longe?” — ¿Está lejos?</li><li>“Esse '
                            'ônibus vai para o centro?” — ¿Este autobús va al centro?</li><li>“Onde '
                            'fica o metrô?” — ¿Dónde está el metro?</li><li>“Pode me deixar aqui, por '
                            'favor?” — ¿Puede dejarme aquí, por favor?</li><li>“Quanto tempo demora?” '
                            '— ¿Cuánto tarda?</li><li>“Este é o melhor caminho?” — ¿Este es el mejor '
                            'camino?</li></ul>',
                            '<p>Los hispanohablantes suelen entender algunas palabras escritas, pero '
                            'la pronunciación brasileña puede ser muy diferente. Por eso, practicar '
                            'listening y speaking antes de llegar es esencial.</p>']},
                  {'heading': 'Situación real 4: restaurantes, cafeterías y pagos',
                   'body': ['<p>Comer fuera es una de las mejores formas de practicar portugués '
                            'brasileño. Las interacciones se repiten mucho y permiten ganar confianza '
                            'rápidamente.</p>',
                            '<p>Vocabulario clave:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portugués</th><th>Español</th></tr></thead><tbody><tr><td>restaurante</td><td>restaurante</td></tr><tr><td>padaria</td><td>panadería '
                            '/ '
                            'cafetería</td></tr><tr><td>café</td><td>café</td></tr><tr><td>água</td><td>agua</td></tr><tr><td>almoço</td><td>almuerzo</td></tr><tr><td>jantar</td><td>cena</td></tr><tr><td>cardápio</td><td>menú</td></tr><tr><td>conta</td><td>cuenta</td></tr><tr><td>cartão</td><td>tarjeta</td></tr><tr><td>dinheiro</td><td>efectivo</td></tr><tr><td>débito</td><td>débito</td></tr><tr><td>crédito</td><td>crédito</td></tr></tbody></table>',
                            '<p>Frases útiles:</p>',
                            '<ul><li>“Tem mesa para duas pessoas?” — ¿Hay mesa para dos '
                            'personas?</li><li>“Posso ver o cardápio?” — ¿Puedo ver el '
                            'menú?</li><li>“Quero um café, por favor.” — Quiero un café, por '
                            'favor.</li><li>“Esse prato tem carne?” — ¿Este plato tiene '
                            'carne?</li><li>“A conta, por favor.” — La cuenta, por '
                            'favor.</li><li>“Aceita cartão?” — ¿Aceptan tarjeta?</li><li>“É débito ou '
                            'crédito?” — ¿Es débito o crédito?</li></ul>',
                            '<p>En Brasil, al pagar con tarjeta, es muy común escuchar: '
                            '<strong>“débito ou crédito?”</strong>. Conviene reconocer esta pregunta '
                            'desde el principio.</p>']},
                  {'heading': 'Situación real 5: trabajo, estudios y vida profesional',
                   'body': ['<p>Si llegas a Brasil para trabajar o estudiar, necesitas portugués para '
                            'integrarte mejor. Aunque tu empresa o universidad use inglés o español en '
                            'algunos contextos, la vida cotidiana alrededor del trabajo y del estudio '
                            'suele ocurrir en portugués.</p>',
                            '<p>Vocabulario clave:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portugués</th><th>Español</th></tr></thead><tbody><tr><td>trabalho</td><td>trabajo</td></tr><tr><td>reunião</td><td>reunión</td></tr><tr><td>equipe</td><td>equipo</td></tr><tr><td>prazo</td><td>plazo</td></tr><tr><td>projeto</td><td>proyecto</td></tr><tr><td>responsável</td><td>responsable</td></tr><tr><td>aula</td><td>clase</td></tr><tr><td>professor</td><td>profesor</td></tr><tr><td>material</td><td>material</td></tr><tr><td>inscrição</td><td>inscripción</td></tr><tr><td>prova</td><td>examen</td></tr><tr><td>mensagem</td><td>mensaje</td></tr></tbody></table>',
                            '<p>Frases útiles:</p>',
                            '<ul><li>“Qual é o prazo?” — ¿Cuál es el plazo?</li><li>“Quem é o '
                            'responsável?” — ¿Quién es el responsable?</li><li>“Podemos marcar uma '
                            'reunião?” — ¿Podemos programar una reunión?</li><li>“Só para '
                            'confirmar...” — Solo para confirmar...</li><li>“Você pode explicar de '
                            'novo?” — ¿Puedes explicar de nuevo?</li><li>“Onde encontro o material da '
                            'aula?” — ¿Dónde encuentro el material de la clase?</li><li>“Como faço a '
                            'inscrição?” — ¿Cómo hago la inscripción?</li></ul>',
                            '<p>La frase <strong>“Só para confirmar...”</strong> es muy útil en '
                            'ambientes profesionales. Suena educada, clara y ayuda a evitar '
                            'malentendidos.</p>']},
                  {'heading': '¿Qué diferencia al portugués brasileño del español?',
                   'body': ['<p>El portugués brasileño y el español se parecen, pero no son iguales. '
                            'La similitud ayuda al inicio, pero puede convertirse en una trampa si el '
                            'alumno confía demasiado en la intuición.</p>',
                            '<p>Diferencias importantes:</p>',
                            '<ul><li><strong>Pronunciación:</strong> el portugués brasileño tiene '
                            'sonidos nasales y vocales que no siempre existen en '
                            'español.</li><li><strong>Ritmo:</strong> la entonación brasileña puede '
                            'sonar más musical y con reducciones naturales.</li><li><strong>Falsos '
                            'amigos:</strong> algunas palabras se parecen, pero significan cosas '
                            'distintas.</li><li><strong>Uso informal:</strong> los brasileños usan '
                            'muchas expresiones cortas como “beleza”, “tá bom”, “pois é” y “pode '
                            'deixar”.</li><li><strong>Cultura de comunicación:</strong> hay mucho uso '
                            'de cordialidad, pequeñas conversaciones y fórmulas suaves para pedir '
                            'algo.</li></ul>',
                            '<p>Ejemplos de expresiones brasileñas:</p>',
                            '<table class="vd-table"><thead><tr><th>Portugués</th><th>Sentido '
                            'aproximado</th></tr></thead><tbody><tr><td>Tudo bem?</td><td>¿Todo bien? '
                            '/ ¿Cómo estás?</td></tr><tr><td>Beleza.</td><td>Perfecto / bien / '
                            'ok</td></tr><tr><td>Tá bom.</td><td>Está '
                            'bien</td></tr><tr><td>Combinado.</td><td>De acuerdo</td></tr><tr><td>Pode '
                            'deixar.</td><td>Déjalo conmigo / no te preocupes</td></tr><tr><td>Pois '
                            'é.</td><td>Sí, así es / pues sí</td></tr><tr><td>Fica '
                            'tranquilo.</td><td>Quédate tranquilo / no te '
                            'preocupes</td></tr></tbody></table>',
                            '<p>Estas expresiones son difíciles de dominar solo con listas. En clases '
                            'en vivo, puedes escuchar cómo se usan, repetirlas y entender su '
                            'tono.</p>']},
                  {'heading': 'Cómo practicar antes de llegar a Brasil',
                   'body': ['<p>Para practicar antes de llegar a Brasil, organiza tu estudio por '
                            'situaciones, no solo por capítulos gramaticales. La gramática importa, '
                            'pero debe servir a la comunicación.</p>',
                            '<p>Un plan simple de cuatro semanas:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Semana</th><th>Enfoque</th><th>Objetivo</th></tr></thead><tbody><tr><td>1</td><td>Saludos, '
                            'presentación y frases de ayuda</td><td>Explicar quién eres y pedir '
                            'repetición</td></tr><tr><td>2</td><td>Aeropuerto, hotel y '
                            'transporte</td><td>Llegar y moverte con '
                            'seguridad</td></tr><tr><td>3</td><td>Restaurante, pagos y '
                            'compras</td><td>Resolver necesidades '
                            'diarias</td></tr><tr><td>4</td><td>Trabajo, estudio y '
                            'vivienda</td><td>Integrarte mejor en la rutina</td></tr></tbody></table>',
                            '<p>Cada semana, haz cuatro acciones:</p>',
                            '<ol><li>Aprende 10 palabras clave.</li><li>Crea 10 frases '
                            'útiles.</li><li>Practica en voz alta.</li><li>Haz una simulación en clase '
                            'en vivo.</li></ol>',
                            '<p>La simulación es fundamental. No basta con leer la frase “Tenho uma '
                            'reserva”. Debes decirla, escuchar una respuesta y reaccionar. Eso es lo '
                            'que construye confianza.</p>']},
                  {'heading': 'Vocabulario clave para tus primeros días en Brasil',
                   'body': ['<p>Aquí tienes un glosario inicial para llegar mejor preparado:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Portugués</th><th>Español</th></tr></thead><tbody><tr><td>ajuda</td><td>ayuda</td></tr><tr><td>banheiro</td><td>baño</td></tr><tr><td>endereço</td><td>dirección</td></tr><tr><td>horário</td><td>horario</td></tr><tr><td>dinheiro</td><td>efectivo</td></tr><tr><td>cartão</td><td>tarjeta</td></tr><tr><td>farmácia</td><td>farmacia</td></tr><tr><td>mercado</td><td>mercado '
                            '/ '
                            'supermercado</td></tr><tr><td>restaurante</td><td>restaurante</td></tr><tr><td>hotel</td><td>hotel</td></tr><tr><td>reserva</td><td>reserva</td></tr><tr><td>mala</td><td>maleta</td></tr><tr><td>documento</td><td>documento</td></tr><tr><td>passaporte</td><td>pasaporte</td></tr><tr><td>trabalho</td><td>trabajo</td></tr><tr><td>reunião</td><td>reunión</td></tr><tr><td>aula</td><td>clase</td></tr><tr><td>entrega</td><td>entrega '
                            '/ '
                            'paquete</td></tr><tr><td>problema</td><td>problema</td></tr><tr><td>agora</td><td>ahora</td></tr><tr><td>hoje</td><td>hoy</td></tr><tr><td>amanhã</td><td>mañana</td></tr><tr><td>devagar</td><td>despacio</td></tr><tr><td>de '
                            'novo</td><td>de nuevo</td></tr></tbody></table>',
                            '<p>Convierte cada palabra en frase:</p>',
                            '<ul><li>“Preciso de ajuda.” — Necesito ayuda.</li><li>“Onde fica o '
                            'banheiro?” — ¿Dónde está el baño?</li><li>“Qual é o endereço?” — ¿Cuál es '
                            'la dirección?</li><li>“Aceita cartão?” — ¿Aceptan tarjeta?</li><li>“Tenho '
                            'uma reunião amanhã.” — Tengo una reunión mañana.</li><li>“Pode falar '
                            'devagar?” — ¿Puede hablar despacio?</li><li>“Pode repetir de novo?” — '
                            '¿Puede repetir de nuevo?</li></ul>',
                            '<p>El vocabulario funciona mejor cuando se convierte en acción.</p>']},
                  {'heading': 'Práctica en clase en vivo: escenarios recomendados',
                   'body': ['<p>Las clases en vivo son especialmente útiles porque te obligan a usar '
                            'el idioma en tiempo real. Un profesor puede corregir pronunciación, '
                            'naturalidad y estructura, además de explicar diferencias culturales.</p>',
                            '<p>Escenarios para practicar:</p>',
                            '<h3>1. Check-in en hotel</h3>',
                            '<p>Practica:</p>',
                            '<ul><li>“Tenho uma reserva.”</li><li>“A reserva está no nome '
                            'de...”</li><li>“Qual é a senha do Wi-Fi?”</li><li>“O café da manhã está '
                            'incluído?”</li></ul>',
                            '<h3>2. Pedido en restaurante</h3>',
                            '<p>Practica:</p>',
                            '<ul><li>“Quero um café, por favor.”</li><li>“Esse prato tem '
                            'carne?”</li><li>“A conta, por favor.”</li><li>“Aceita cartão?”</li></ul>',
                            '<h3>3. Problema en apartamento</h3>',
                            '<p>Practica:</p>',
                            '<ul><li>“A internet não está funcionando.”</li><li>“Preciso falar com a '
                            'manutenção.”</li><li>“A chave não funciona.”</li><li>“Chegou uma entrega '
                            'para mim?”</li></ul>',
                            '<h3>4. Reunión de trabajo</h3>',
                            '<p>Practica:</p>',
                            '<ul><li>“Qual é o prazo?”</li><li>“Só para confirmar...”</li><li>“Você '
                            'pode explicar de novo?”</li><li>“Quem é o responsável?”</li></ul>',
                            '<h3>5. Primer día de clase</h3>',
                            '<p>Practica:</p>',
                            '<ul><li>“Onde encontro o material?”</li><li>“Quando é a '
                            'aula?”</li><li>“Como faço a inscrição?”</li><li>“Pode repetir, por '
                            'favor?”</li></ul>',
                            '<p>Este tipo de práctica crea una memoria comunicativa. Cuando la '
                            'situación real ocurre, tu cerebro reconoce el patrón.</p>',
                            '<p>CTA: Reserva una prueba de nivel gratuita en <a '
                            'href="/es/prueba-de-nivel-de-portugues">https://vediums.com/</a> y '
                            'empieza a practicar portugués brasileño con clases en vivo antes de '
                            'llegar a Brasil.</p>']},
                  {'heading': '¿Por qué las clases en vivo son mejores que estudiar solo?',
                   'body': ['<p>Las clases en vivo son mejores para ganar confianza al hablar porque '
                            'el idioma se practica con interacción real. Las aplicaciones y los videos '
                            'pueden ayudar con vocabulario, pero no corrigen tu pronunciación, no '
                            'responden a tus dudas y no simulan conversaciones imprevisibles.</p>',
                            '<p>En una clase en vivo puedes:</p>',
                            '<ul><li>practicar situaciones reales de Brasil;</li><li>recibir '
                            'corrección inmediata;</li><li>aprender pronunciación '
                            'brasileña;</li><li>entender expresiones culturales;</li><li>hacer '
                            'preguntas;</li><li>repetir frases hasta ganar fluidez;</li><li>practicar '
                            'con seguridad antes de la vida real.</li></ul>',
                            '<p>Vedium ofrece clases online en vivo de portugués brasileño para '
                            'extranjeros. La propuesta combina idioma, cultura y práctica real. '
                            'Además, no hay contratos largos de fidelidad: el alumno continúa porque '
                            'siente progreso, no porque está atado a una obligación.</p>']},
                  {'heading': 'Conclusión con CTA fuerte',
                   'body': ['<p>Llegar a Brasil preparado no significa hablar portugués perfecto. '
                            'Significa tener herramientas para comunicarte desde el primer día: '
                            'saludar, pedir ayuda, confirmar información, moverte por la ciudad, hacer '
                            'check-in, pagar, pedir comida, hablar con la portería, participar en el '
                            'trabajo o en los estudios y entender expresiones brasileñas '
                            'frecuentes.</p>',
                            '<p>Para hispanohablantes, el portugués brasileño puede parecer cercano, '
                            'pero requiere práctica real. La pronunciación, el ritmo, las expresiones '
                            'y la cultura de comunicación son diferentes del español. Por eso, el '
                            'mejor camino es estudiar con situaciones reales y clases en vivo.</p>',
                            '<p>Vedium ayuda a extranjeros, expatriados y profesionales '
                            'internacionales a aprender portugués brasileño con clases online en vivo, '
                            'enfoque práctico y profundidad cultural. Sin contratos largos: sigues '
                            'porque avanzas.</p>',
                            '<p>Reserva una prueba de nivel gratuita en <a '
                            'href="/es/portugues-para-extranjeros">https://vediums.com/</a> y empieza '
                            'a prepararte para Brasil con más confianza.</p>']}],
     'faqs': [{'q': '¿Necesito aprender portugués antes de llegar a Brasil?',
               'a': 'Sí. Aunque puedas encontrar personas que hablen inglés o entiendan español, el '
                    'portugués brasileño te dará más autonomía en aeropuerto, hotel, transporte, '
                    'vivienda, trabajo, estudios y vida diaria.'},
              {'q': '¿El español es suficiente para comunicarme en Brasil?',
               'a': 'Puede ayudar en algunas situaciones, pero no es suficiente para integrarte bien. '
                    'El portugués brasileño tiene pronunciación, expresiones y usos culturales propios '
                    'que conviene practicar.'},
              {'q': '¿Qué debo aprender primero en portugués brasileño?',
               'a': 'Empieza por saludos, presentación personal, frases para pedir ayuda, aeropuerto, '
                    'hotel, transporte, restaurante, pagos, vivienda, farmacia y preguntas básicas.'},
              {'q': '¿Las clases en vivo ayudan más que las aplicaciones?',
               'a': 'Sí. Las aplicaciones ayudan con repetición y vocabulario, pero las clases en vivo '
                    'permiten practicar conversación real, recibir corrección, mejorar pronunciación y '
                    'entender el contexto cultural brasileño.'},
              {'q': '¿Vedium ofrece portugués brasileño para extranjeros?',
               'a': 'Sí. Vedium ofrece clases online en vivo de portugués brasileño para extranjeros, '
                    'expatriados y profesionales, con foco en situaciones reales, cultura y confianza '
                    'para hablar.'}],
     'cta_title': '¿Quieres saber tu nivel real de portugués?',
     'cta_text': 'Haz la prueba de nivel gratuita de Vedium y descubre por dónde empezar.',
     'cta_label': 'Conocer el curso de portugués',
     'cta_url': '/es/portugues-para-extranjeros'},
    "brasilianisches-portugiesisch-fur-auswanderer-die-wichtigsten-grundlagen": {'title': 'Brasilianisches Portugiesisch für Auswanderer: die wichtigsten Grundlagen',
     'meta_description': 'Lernen Sie die wichtigsten Grundlagen des brasilianischen Portugiesisch für '
                         'Alltag, Arbeit und Ankunft in Brasilien.',
     'h1': 'Brasilianisches Portugiesisch für Auswanderer: die wichtigsten Grundlagen',
     'date': '2025-01-15',
     'date_display': '15. Januar 2025',
     'hero_image': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aprender português como língua estrangeira',
     'tag': 'Deutsch',
     'lang': 'de',
     'lead': 'Brasilianisches Portugiesisch für Auswanderer sollte zuerst auf reale Situationen '
             'vorbereiten: Ankunft, Wohnen, Einkaufen, Arbeit, Transport, Gesundheit, Behördengänge '
             'und soziale Kontakte. Wer nach Brasilien zieht, braucht nicht am ersten Tag perfekte '
             'Grammatik. Viel wichtiger ist ein praktischer Grundwortschatz, klare Aussprache, '
             'kulturelles Verständnis und die Fähigkeit, in alltäglichen Momenten selbstbewusst zu '
             'reagieren.',
     'sections': [{'heading': '',
                   'body': ['<p>Für deutschsprachige Auswanderer, Expatriates, internationale '
                            'Fachkräfte und Familien ist Brasilien oft ein Land voller Chancen, aber '
                            'auch voller sprachlicher Details. In São Paulo, Rio de Janeiro, '
                            'Florianópolis, Curitiba, Belo Horizonte oder Salvador kann Englisch in '
                            'bestimmten Arbeitsumfeldern helfen. Der Alltag läuft jedoch überwiegend '
                            'auf Portugiesisch: im Gebäude, im Supermarkt, in der Apotheke, beim Arzt, '
                            'in der Schule, im Taxi, im Fitnessstudio, mit Nachbarn, bei '
                            'Lieferdiensten und in vielen beruflichen Gesprächen.</p>',
                            '<p>Genau hier entsteht der Unterschied zwischen „ich kenne ein paar '
                            'Wörter“ und „ich kann mich im Alltag bewegen“. Brasilianisches '
                            'Portugiesisch ist nicht nur eine Sprache mit Vokabeln und Verben. Es ist '
                            'auch eine soziale Brücke. Begrüßungen, Höflichkeitsformeln, indirekte '
                            'Fragen, kleine Gesprächseinstiege und die freundliche Art, um Hilfe zu '
                            'bitten, gehören zur Kommunikation dazu.</p>',
                            '<p>Deshalb sollte ein Kurs für Portugiesisch für Brasilien nicht nur aus '
                            'aufgezeichneten Lektionen bestehen. Auswanderer brauchen Live-Unterricht, '
                            'echte Gesprächspraxis und Korrektur. Bei Vedium lernen Sie '
                            'brasilianisches Portugiesisch online im Live-Unterricht, mit kulturellem '
                            'Kontext und ohne langfristige Vertragsbindung. Sie bleiben, weil Sie '
                            'Fortschritt spüren, nicht weil ein Vertrag Sie festhält.</p>']},
                  {'heading': 'Warum brasilianisches Portugiesisch vor der Auswanderung wichtig ist',
                   'body': ['<p>Brasilianisches Portugiesisch vor der Auswanderung zu lernen reduziert '
                            'Stress, beschleunigt Integration und macht die ersten Wochen in Brasilien '
                            'deutlich leichter. Schon ein gut aufgebautes A1-Niveau kann im Alltag '
                            'einen großen Unterschied machen.</p>',
                            '<p>Die ersten Wochen in einem neuen Land sind intensiv. Sie müssen eine '
                            'Adresse erklären, Dokumente zeigen, einen Termin bestätigen, eine '
                            'Lieferung empfangen, eine Frage stellen, einen Weg verstehen, ein Problem '
                            'beschreiben und sich Menschen vorstellen. Wenn jede kleine Situation zur '
                            'Sprachprüfung wird, wirkt der Umzug anstrengender als nötig.</p>',
                            '<p>Viele Auswanderer verlassen sich am Anfang auf Übersetzungs-Apps. '
                            'Diese können helfen, aber sie ersetzen keine echte Gesprächsfähigkeit. '
                            'Eine App übersetzt Wörter. Sie erklärt aber nicht immer den Ton, die '
                            'Höflichkeit, regionale Gewohnheiten oder die Frage, ob ein Satz natürlich '
                            'klingt. Genau diese Nuancen sind in Brasilien wichtig, weil Kommunikation '
                            'oft warm, persönlich und situationsabhängig ist.</p>',
                            '<p>Ein Beispiel: Sie könnten theoretisch sagen: „Eu quero informação.“ '
                            'Das ist verständlich, klingt aber sehr direkt. Natürlicher wäre: „Oi, '
                            'tudo bem? Você pode me ajudar, por favor?“ Das bedeutet: „Hallo, alles '
                            'gut? Können Sie mir bitte helfen?“ Der zweite Satz öffnet die Situation '
                            'freundlicher und passt besser zum brasilianischen Alltag.</p>',
                            '<p>Vor der Ankunft sollten Sie deshalb drei Ziele verfolgen:</p>',
                            '<ul><li><strong>alltägliche Sätze verstehen</strong>, auch wenn sie '
                            'schnell gesprochen werden;</li><li><strong>einfache Antworten sicher '
                            'formulieren</strong>, ohne lange nachdenken zu '
                            'müssen;</li><li><strong>kulturelle Signale erkennen</strong>, zum '
                            'Beispiel Begrüßungen, Höflichkeit und informelle Ausdrücke.</li></ul>',
                            '<p>Live-Unterricht ist dafür besonders wertvoll. Sie hören echte Sprache, '
                            'sprechen laut, bekommen Korrektur und üben Situationen, die tatsächlich '
                            'auf Sie zukommen.</p>',
                            '<p><strong>CTA:</strong> Buchen Sie einen kostenlosen Einstufungstest bei '
                            'Vedium und starten Sie mit einem klaren Plan für Ihr Portugiesisch in '
                            'Brasilien: <a '
                            'href="/de/portugiesisch-fuer-auslaender">https://vediums.com/</a></p>']},
                  {'heading': 'Reale Alltagssituation: die Ankunft in Brasilien meistern',
                   'body': ['<p>Die Ankunft in Brasilien gelingt leichter, wenn Sie einfache Sätze für '
                            'Flughafen, Transport, Unterkunft und erste Kontakte beherrschen. Diese '
                            'Situationen kommen sofort vor und sollten daher früh geübt werden.</p>',
                            '<p>Direkt nach der Landung brauchen Sie Sprache für praktische Fragen. Wo '
                            'ist der Ausgang? Wo ist der Fahrer? Welche Adresse müssen Sie nennen? Wie '
                            'sagen Sie, dass Sie gerade angekommen sind? Wie erklären Sie, dass Sie '
                            'Hilfe brauchen? Selbst wenn jemand Englisch spricht, wirkt ein einfacher '
                            'portugiesischer Satz oft freundlich und respektvoll.</p>',
                            '<p>Nützliche Wörter und Sätze für die Ankunft:</p>',
                            '<ul><li><strong>aeroporto</strong> — '
                            'Flughafen;</li><li><strong>bagagem</strong> — '
                            'Gepäck;</li><li><strong>saída</strong> — '
                            'Ausgang;</li><li><strong>endereço</strong> — '
                            'Adresse;</li><li><strong>motorista</strong> — Fahrer oder '
                            'Fahrerin;</li><li><strong>cheguei agora</strong> — ich bin gerade '
                            'angekommen;</li><li><strong>preciso de ajuda</strong> — ich brauche '
                            'Hilfe;</li><li><strong>onde fica...?</strong> — wo befindet '
                            'sich...?</li><li><strong>pode me ajudar, por favor?</strong> — können Sie '
                            'mir bitte helfen?</li></ul>',
                            '<p>Ein praktischer Dialog könnte so aussehen:</p>',
                            '<p><strong>Você:</strong> Oi, tudo bem? Onde fica a saída '
                            'principal?<br><strong>Pessoa:</strong> Fica ali, à '
                            'direita.<br><strong>Você:</strong> Obrigado. Meu motorista está esperando '
                            'lá.</p>',
                            '<p>Auf Deutsch: „Hallo, alles gut? Wo ist der Hauptausgang?“ — „Dort '
                            'rechts.“ — „Danke. Mein Fahrer wartet dort.“</p>',
                            '<p>Das ist kein komplexes Portugiesisch. Aber es gibt Ihnen Kontrolle. '
                            'Sie müssen nicht schweigen, zeigen oder nervös auf eine App tippen. Sie '
                            'können die erste Situation aktiv bewältigen.</p>',
                            '<p>Auswanderer sollten außerdem lernen, ihre Adresse langsam zu sagen. '
                            'Brasilianische Adressen enthalten oft Straße, Hausnummer, Apartment, '
                            'Gebäude, Block, Stadtteil und Referenzpunkt. Wenn Sie zum Beispiel in '
                            'einem großen Wohnkomplex leben, kann die genaue Beschreibung wichtig '
                            'sein.</p>',
                            '<p>Praktische Sätze:</p>',
                            '<ul><li><strong>Meu endereço é...</strong> — meine Adresse '
                            'ist...;</li><li><strong>Moro no apartamento...</strong> — ich wohne in '
                            'Apartment...;</li><li><strong>É perto de...</strong> — es ist in der Nähe '
                            'von...;</li><li><strong>Pode me deixar na entrada?</strong> — können Sie '
                            'mich am Eingang absetzen?</li></ul>',
                            '<p>Diese Grundlagen geben Ihnen Sicherheit vom ersten Tag an.</p>']},
                  {'heading': 'Wichtiger Wortschatz für Wohnen, Einkaufen und tägliche Erledigungen',
                   'body': ['<p>Der wichtigste Wortschatz für Auswanderer ist der Wortschatz des '
                            'Alltags: Wohnung, Supermarkt, Apotheke, Lieferung, Zahlung und einfache '
                            'Probleme. Diese Wörter werden viel häufiger gebraucht als abstrakte '
                            'Grammatikthemen.</p>',
                            '<p>Beim Wohnen geht es nicht nur um „casa“ oder „apartamento“. Sie müssen '
                            'mit Portiers, Vermietern, Maklern, Reinigungskräften, Technikern, '
                            'Internetanbietern und Nachbarn sprechen. In vielen brasilianischen '
                            'Gebäuden gibt es eine <strong>portaria</strong>, also einen Empfang oder '
                            'Pförtnerbereich. Diese Funktion ist für viele deutschsprachige '
                            'Auswanderer ungewohnt, aber im Alltag sehr wichtig.</p>',
                            '<p>Nützliche Wörter rund ums Wohnen:</p>',
                            '<ul><li><strong>apartamento</strong> — '
                            'Wohnung;</li><li><strong>casa</strong> — '
                            'Haus;</li><li><strong>aluguel</strong> — '
                            'Miete;</li><li><strong>contrato</strong> — '
                            'Vertrag;</li><li><strong>portaria</strong> — Empfang oder '
                            'Pförtnerbereich;</li><li><strong>porteiro / porteira</strong> — Pförtner '
                            'oder Pförtnerin;</li><li><strong>chave</strong> — '
                            'Schlüssel;</li><li><strong>entrega</strong> — '
                            'Lieferung;</li><li><strong>manutenção</strong> — Wartung oder '
                            'Reparatur;</li><li><strong>vazamento</strong> — Leck oder '
                            'Wasseraustritt.</li></ul>',
                            '<p>Praktische Sätze:</p>',
                            '<ul><li><strong>Tem uma entrega para mim?</strong> — Gibt es eine '
                            'Lieferung für mich?</li><li><strong>A internet não está '
                            'funcionando.</strong> — Das Internet funktioniert '
                            'nicht.</li><li><strong>Preciso falar com a manutenção.</strong> — Ich '
                            'muss mit der Wartung sprechen.</li><li><strong>Perdi minha '
                            'chave.</strong> — Ich habe meinen Schlüssel verloren.</li></ul>',
                            '<p>Für Einkäufe und tägliche Erledigungen brauchen Sie einfache, '
                            'wiederholbare Strukturen:</p>',
                            '<ul><li><strong>Quanto custa?</strong> — Wie viel kostet '
                            'das?</li><li><strong>Vocês aceitam cartão?</strong> — Akzeptieren Sie '
                            'Karte?</li><li><strong>Preciso de uma sacola, por favor.</strong> — Ich '
                            'brauche bitte eine Tasche.</li><li><strong>Onde fica a farmácia?</strong> '
                            '— Wo ist die Apotheke?</li><li><strong>Estou procurando...</strong> — Ich '
                            'suche...</li></ul>',
                            '<p>In der Apotheke ist Kommunikation besonders wichtig. Sie müssen '
                            'Symptome beschreiben, nach einem Produkt fragen oder erklären, dass Sie '
                            'ein bestimmtes Medikament suchen. Natürlich ersetzt Sprachunterricht '
                            'keine medizinische Beratung. Aber einfache Sätze helfen Ihnen, die '
                            'Situation besser zu organisieren.</p>',
                            '<p>Beispiele:</p>',
                            '<ul><li><strong>Estou com dor de cabeça.</strong> — Ich habe '
                            'Kopfschmerzen.</li><li><strong>Estou com febre.</strong> — Ich habe '
                            'Fieber.</li><li><strong>Você tem algo para...?</strong> — Haben Sie etwas '
                            'gegen...?</li><li><strong>Preciso de orientação.</strong> — Ich brauche '
                            'Beratung.</li></ul>',
                            '<p>Ein guter Kurs für brasilianisches Portugiesisch sollte diese '
                            'Alltagsszenarien aktiv trainieren. Nicht als Vokabelliste, sondern als '
                            'Gespräch: Sie stellen eine Frage, hören eine Antwort, reagieren und '
                            'verbessern Ihre Aussprache.</p>']},
                  {'heading': 'Portugiesisch für Arbeit und professionelle Integration',
                   'body': ['<p>Portugiesisch für die Arbeit in Brasilien sollte Sie darauf '
                            'vorbereiten, sich vorzustellen, Fragen zu stellen, Informationen zu '
                            'bestätigen und höflich um Klärung zu bitten. Fachvokabular kommt danach; '
                            'zuerst brauchen Sie kommunikative Sicherheit.</p>',
                            '<p>Viele Auswanderer ziehen aus beruflichen Gründen nach Brasilien: '
                            'Entsendung, internationale Rolle, Remote-Arbeit, lokales Team, Projekt, '
                            'Forschung oder Unternehmensgründung. Selbst wenn die Unternehmenssprache '
                            'Englisch ist, findet ein Teil der Beziehungspflege oft auf Portugiesisch '
                            'statt. Ein kurzes „Bom dia, tudo bem?“ vor einem Meeting oder ein '
                            'freundliches „obrigado“ im Büro kann Ihre Integration verbessern.</p>',
                            '<p>Nützliche Sätze für den Beruf:</p>',
                            '<ul><li><strong>Eu trabalho na área de...</strong> — Ich arbeite im '
                            'Bereich...;</li><li><strong>Sou responsável por...</strong> — Ich bin '
                            'verantwortlich für...;</li><li><strong>Podemos marcar uma '
                            'reunião?</strong> — Können wir ein Meeting planen?</li><li><strong>Qual é '
                            'o prazo?</strong> — Was ist die Frist?</li><li><strong>Pode repetir, por '
                            'favor?</strong> — Können Sie das bitte wiederholen?</li><li><strong>Pode '
                            'falar mais devagar?</strong> — Können Sie langsamer '
                            'sprechen?</li><li><strong>Vou verificar e te retorno.</strong> — Ich '
                            'prüfe das und melde mich zurück.</li></ul>',
                            '<p>Besonders wichtig ist der Satz: <strong>Pode repetir, por '
                            'favor?</strong> Viele Lernende haben Angst, um Wiederholung zu bitten. '
                            'Dabei ist das eine normale und sehr nützliche Kommunikationsstrategie. '
                            'Wer höflich um Wiederholung bittet, bleibt im Gespräch und zeigt '
                            'Interesse.</p>',
                            '<p>Auch kulturell unterscheidet sich der berufliche Austausch in '
                            'Brasilien häufig von deutschsprachigen Umfeldern. Die Kommunikation kann '
                            'wärmer, beziehungsorientierter und weniger abrupt wirken. Das bedeutet '
                            'nicht, dass sie weniger professionell ist. Es bedeutet, dass Beziehung '
                            'und Vertrauen oft Teil der professionellen Sprache sind.</p>',
                            '<p>Ein Live-Kurs kann diese Unterschiede simulieren: Begrüßung im '
                            'Meeting, kurze Vorstellung, Nachfragen, höfliches Unterbrechen, E-Mails, '
                            'Chat-Nachrichten und Feedbackgespräche. Genau darin liegt der Vorteil '
                            'gegenüber reinem Selbststudium.</p>']},
                  {'heading': 'Häufige Fehler deutschsprachiger Lernender',
                   'body': ['<p>Deutschsprachige Lernende machen oft dieselben Fehler: Sie übersetzen '
                            'zu wörtlich, sprechen zu formell, vermeiden das Sprechen zu lange oder '
                            'unterschätzen die Aussprache. Diese Fehler sind normal, lassen sich aber '
                            'durch gezieltes Training früh korrigieren.</p>',
                            '<p>Der erste Fehler ist die direkte Übersetzung aus dem Deutschen. '
                            'Portugiesisch folgt anderen Mustern. „Ich habe kalt“ wird nicht wörtlich '
                            'übertragen. Man sagt <strong>Estou com frio</strong>. „Ich bin mit '
                            'Hunger“ klingt auf Deutsch seltsam, ist aber im Portugiesischen die '
                            'Struktur: <strong>Estou com fome</strong>. Wer solche Muster als ganze '
                            'Ausdrücke lernt, spricht schneller natürlicher.</p>',
                            '<p>Der zweite Fehler ist zu viel Formalität. Viele Anfänger lernen sehr '
                            'korrekte Sätze, die im Alltag jedoch steif wirken. In Brasilien sind '
                            'einfache und freundliche Formulierungen oft besser. „Oi, tudo bem?“ ist '
                            'in vielen Situationen natürlicher als eine sehr distanzierte '
                            'Begrüßung.</p>',
                            '<p>Der dritte Fehler ist passives Lernen. Apps, Videos und Bücher können '
                            'unterstützen, aber Auswanderer müssen sprechen. Wenn Sie erst in '
                            'Brasilien anfangen, laut zu üben, wird jede Alltagssituation zur ersten '
                            'Übung. Besser ist es, vorher im geschützten Raum zu sprechen, Fehler zu '
                            'machen und Feedback zu bekommen.</p>',
                            '<p>Der vierte Fehler ist die Aussprache. Brasilianisches Portugiesisch '
                            'hat Laute, die für deutschsprachige Personen ungewohnt sein können: '
                            'Nasallaute, offene Vokale, das „lh“, das „ão“ und regionale Varianten des '
                            '„r“. Diese Dinge lernt man nicht sicher durch Lesen. Man muss hören, '
                            'nachsprechen und korrigiert werden.</p>',
                            '<p>Der fünfte Fehler ist fehlender kultureller Kontext. Ein Wort kann '
                            'grammatisch korrekt sein und trotzdem in einer Situation unpassend '
                            'klingen. Deshalb verbindet Vedium Sprache mit Kultur: Sie lernen nicht '
                            'nur, was ein Satz bedeutet, sondern wann Sie ihn benutzen können.</p>']},
                  {'heading': 'Übung im Live-Unterricht: wie Sie schneller sicher werden',
                   'body': ['<p>Live-Unterricht macht Sie schneller sicher, weil Sie aktiv sprechen, '
                            'direkte Korrektur erhalten und echte Brasilien-Situationen üben. Genau '
                            'diese Kombination brauchen Auswanderer vor und nach der Ankunft.</p>',
                            '<p>Ein sinnvoller Lernplan für brasilianisches Portugiesisch sollte nicht '
                            'mit abstrakten Kapiteln beginnen, sondern mit Ihren realen Bedürfnissen. '
                            'Ziehen Sie allein um? Kommen Sie mit Familie? Arbeiten Sie in einem '
                            'brasilianischen Team? Müssen Sie eine Wohnung mieten? Werden Sie viel '
                            'reisen? Haben Sie Kinder in einer Schule? Jede Antwort verändert den '
                            'Lernplan.</p>',
                            '<p>Im Live-Unterricht kann eine Lehrkraft die Szenarien anpassen. Sie '
                            'üben zum Beispiel:</p>',
                            '<ul><li>die erste Vorstellung in der Hausverwaltung;</li><li>ein Gespräch '
                            'mit dem Portier;</li><li>eine Frage im Supermarkt;</li><li>einen Termin '
                            'in der Apotheke;</li><li>eine kurze berufliche Vorstellung;</li><li>eine '
                            'Nachricht an einen Kollegen;</li><li>eine Bitte um '
                            'Wiederholung;</li><li>eine Wegbeschreibung für einen Fahrer.</li></ul>',
                            '<p>Diese Übungen verbinden Wortschatz, Aussprache, Hörverstehen und '
                            'Kultur. Sie lernen nicht isoliert. Sie lernen so, wie Sprache im echten '
                            'Leben funktioniert.</p>',
                            '<p>Bei Vedium findet dieser Lernprozess online und live statt. Das '
                            'bedeutet: Unterricht mit realer Person, echte Interaktion, Möglichkeit '
                            'zum Fragen, kleine Schritte und Fokus auf Fortschritt. Es gibt keine '
                            'Notwendigkeit, sich durch einen langen Vertrag unter Druck zu setzen. Die '
                            'Idee ist einfach: Sie bleiben, weil der Unterricht Ihnen hilft, in '
                            'Brasilien besser zu leben, zu arbeiten und sich sicherer zu fühlen.</p>']},
                  {'heading': 'Fazit mit starkem CTA',
                   'body': ['<p>Brasilianisches Portugiesisch für Auswanderer muss praktisch, '
                            'kulturell und lebendig sein. Die wichtigsten Grundlagen sind nicht nur '
                            'Verben und Vokabeln, sondern konkrete Fähigkeiten: sich vorstellen, Hilfe '
                            'erbitten, eine Adresse erklären, einkaufen, mit der Portaria sprechen, '
                            'einfache berufliche Gespräche führen und kulturelle Signale '
                            'verstehen.</p>',
                            '<p>Wenn Sie nach Brasilien ziehen, sollten Sie vor der Ankunft mit den '
                            'häufigsten Situationen beginnen. Lernen Sie ganze Sätze, sprechen Sie '
                            'laut, üben Sie Dialoge und bauen Sie eine Routine auf, die zu Ihrem Leben '
                            'passt. Perfektion ist nicht das Ziel der ersten Phase. Handlungsfähigkeit '
                            'ist das Ziel.</p>',
                            '<p>Vedium hilft Ihnen dabei mit Live-Unterricht, kulturellem Kontext und '
                            'einem Lernplan für reale Kommunikation in Brasilien. Buchen Sie jetzt '
                            'Ihren kostenlosen Einstufungstest und starten Sie mit brasilianischem '
                            'Portugiesisch, das Sie wirklich im Alltag brauchen: <a '
                            'href="/de/portugiesisch-einstufungstest">https://vediums.com/</a></p>']}],
     'faqs': [{'q': 'Welches Portugiesisch sollte ich für Brasilien lernen?',
               'a': 'Sie sollten brasilianisches Portugiesisch lernen, nicht europäisches '
                    'Portugiesisch. Aussprache, Wortschatz, Alltagssprache und kulturelle Gewohnheiten '
                    'unterscheiden sich deutlich.'},
              {'q': 'Reicht Englisch für den Alltag in Brasilien?',
               'a': 'Englisch kann in internationalen Unternehmen oder touristischen Bereichen helfen. '
                    'Für Wohnen, Einkaufen, Gesundheit, Transport, Nachbarschaft und viele '
                    'Dienstleistungen ist Portugiesisch jedoch sehr wichtig.'},
              {'q': 'Was sollte ich vor der Auswanderung zuerst lernen?',
               'a': 'Beginnen Sie mit Begrüßungen, Zahlen, Adressen, Fragen nach Hilfe, Einkäufen, '
                    'Transport, Wohnen, Gesundheit und einfachen beruflichen Sätzen. Diese Themen '
                    'brauchen Sie direkt in den ersten Wochen.'},
              {'q': 'Sind Live-Kurse besser als Sprach-Apps?',
               'a': 'Sprach-Apps können beim Wiederholen helfen. Live-Kurse sind jedoch stärker für '
                    'Aussprache, echte Gespräche, Korrektur, spontane Antworten und kulturelle '
                    'Nuancen.'},
              {'q': 'Bietet Vedium Portugiesisch für Auswanderer an?',
               'a': 'Ja. Vedium bietet brasilianisches Portugiesisch für Ausländer im '
                    'Live-Online-Unterricht an, mit Fokus auf Alltag, Arbeit, Kultur und realen '
                    'Situationen in Brasilien.'}],
     'cta_title': 'Bereit für Ihr brasilianisches Portugiesisch?',
     'cta_text': 'Buchen Sie einen kostenlosen Einstufungstest und starten Sie mit einem klaren '
                 'Lernplan.',
     'cta_label': 'Kostenlosen Einstufungstest buchen',
     'cta_url': '/de/portugiesisch-fuer-auslaender'},
    "brasilianisches-portugiesisch-fur-fuhrungskrafte-und-manager": {'title': 'Brasilianisches Portugiesisch für Führungskräfte und Manager',
     'meta_description': 'Sie sind Führungskraft in Brasilien? Lernen Sie mit Vedium effizient '
                         'brasilianisches Portugiesisch für den beruflichen Erfolg und kulturelle '
                         'Integration.',
     'h1': 'Brasilianisches Portugiesisch für Führungskräfte und Manager',
     'date': '2026-06-03',
     'date_display': '3. Juni 2026',
     'hero_image': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aula de português para estrangeiros na Vedium',
     'tag': 'Deutsch',
     'lang': 'de',
     'lead': '',
     'sections': [{'heading': 'Warum brasilianisches Portugiesisch für Führungskräfte so wichtig ist',
                   'body': ['<p>Wenn Sie als Führungskraft oder Manager in Brasilien arbeiten, ist die '
                            'Sprache weit mehr als nur ein Kommunikationsmittel; sie ist Ihr '
                            'wichtigstes Werkzeug für den Aufbau von Vertrauen und Respekt. Viele '
                            'internationale Manager machen den Fehler, sich allein auf Englisch zu '
                            'verlassen. Doch wer die lokale Sprache beherrscht, erschließt sich nicht '
                            'nur die geschäftlichen Nuancen, sondern auch die Unternehmenskultur und '
                            'die informellen Beziehungsgeflechte, die in der brasilianischen '
                            'Arbeitswelt entscheidend sind.</p>',
                            '<p>Bei <a href="/de/portugiesisch-einstufungstest">Vedium</a> verstehen '
                            'wir, dass Führungskräfte keine Zeit für theoretische Grammatikübungen '
                            'haben, die keinen Praxisbezug bieten. Unser Ansatz basiert auf '
                            '<strong>Intelligenz durch kulturelle Tiefe</strong>. Wir bereiten Sie auf '
                            'reale Situationen vor – von der Leitung eines Meetings über das Führen '
                            'von Verhandlungen bis hin zum Aufbau von Verbindungen zu Ihren '
                            'Mitarbeitern. Für Sie als Manager bedeutet dies: Sie lernen nicht nur '
                            '"Portugiesisch", sondern Sie lernen, wie Sie in Brasilien erfolgreich '
                            'führen.</p>']},
                  {'heading': 'Die geschäftliche Relevanz: Kommunikation als Führungsinstrument',
                   'body': ['<p>In Brasilien wird viel Wert auf persönliche Beziehungen und Empathie '
                            'gelegt. Eine Führungskraft, die sich die Mühe macht, Portugiesisch zu '
                            'sprechen, signalisiert damit Wertschätzung für das Land und seine Kultur. '
                            'Das verbessert die Mitarbeiterbindung und erleichtert die tägliche '
                            'Zusammenarbeit ungemein.</p>',
                            '<ul><li><strong>Vertrauensaufbau:</strong> Durch das Sprechen der '
                            'Landessprache zeigen Sie Ihren Mitarbeitern, dass Sie Teil des Teams sind '
                            'und nicht nur ein kurzzeitiger Gast.</li><li><strong>Kulturelle '
                            'Intelligenz:</strong> Sie lernen das <em>Jeitinho Brasileiro</em> – die '
                            'brasilianische Art, Probleme kreativ und flexibel zu lösen – zu verstehen '
                            'und konstruktiv zu nutzen, statt sich daran zu '
                            'reiben.</li><li><strong>Präzision in der Führung:</strong> '
                            'Missverständnisse entstehen oft durch Nuancen, die in einer Übersetzung '
                            'verloren gehen. Wenn Sie direkt auf Portugiesisch kommunizieren, haben '
                            'Sie die volle Kontrolle über Ihre Botschaft.</li></ul>']},
                  {'heading': 'Brasilianische Geschäftskultur: Was Sie in den ersten Monaten brauchen',
                   'body': ['<p>Als Manager in einem neuen Land ist Ihre Lernkurve steil. Wir bei '
                            'Vedium konzentrieren uns darauf, diese Kurve durch hochgradig '
                            'individualisierte Live-Unterrichtseinheiten zu optimieren. Was Sie in den '
                            'ersten Monaten benötigen, sind keine komplizierten Satzstrukturen, '
                            'sondern funktionale Sprache für den Führungsalltag:</p>',
                            '<h3>1. Die Sprache der Verhandlung und des Konsens</h3>',
                            '<p>In brasilianischen Meetings wird oft viel diskutiert, bevor eine '
                            'Entscheidung fällt. Es ist wichtig, nicht nur zu verstehen, was gesagt '
                            'wird, sondern auch, was zwischen den Zeilen kommuniziert wird. Unser '
                            'Live-Unterricht simuliert diese Meetings, sodass Sie lernen, wie man '
                            'aktiv zuhört und moderiert.</p>',
                            '<h3>2. Feedback-Kultur und soziale Kompetenz</h3>',
                            '<p>Die Art und Weise, wie in Brasilien Feedback gegeben wird, '
                            'unterscheidet sich von deutschen oder europäischen Standards. Direkte '
                            'Kritik wird oft als unhöflich empfunden. Wir helfen Ihnen, ein '
                            'diplomatisches, aber klares Vokabular zu entwickeln, das Ihre Autorität '
                            'unterstreicht, ohne die Beziehungen zu belasten.</p>',
                            '<h3>3. Networking und informelle Kommunikation</h3>',
                            '<p>Ein großer Teil der geschäftlichen Entscheidungen wird in Brasilien '
                            'beim Mittagessen oder bei informellen Treffen getroffen. Wir bereiten Sie '
                            'darauf vor, auch in diesen lockeren Situationen sicher und souverän auf '
                            'Portugiesisch zu agieren.</p>']},
                  {'heading': 'Warum Vedium für Manager die richtige Wahl ist',
                   'body': ['<p>Manager brauchen Flexibilität und Ergebnisse. Vedium bietet genau '
                            'das:</p>',
                            '<ul><li><strong>100% Live-Unterricht:</strong> Kein Vergleich zu Apps '
                            'oder starren Videokursen. Sie sprechen mit einem menschlichen Lehrer, der '
                            'Ihre spezifischen beruflichen Herausforderungen '
                            'kennt.</li><li><strong>Keine Bindungsfrist:</strong> Wir vertrauen '
                            'darauf, dass unsere Ergebnisse Sie überzeugen. Sie bleiben bei uns, weil '
                            'Sie Ihren Fortschritt im Berufsalltag merken, nicht weil Sie einen '
                            'Vertrag unterschrieben haben.</li><li><strong>Maßgeschneiderte '
                            'Inhalte:</strong> Ob IT, Finanzen oder Personalwesen – wir integrieren '
                            'Ihren Arbeitskontext direkt in den Unterricht, sodass Sie das Gelernte '
                            'sofort am nächsten Tag anwenden können.</li></ul>']},
                  {'heading': 'Wie Sie als Manager effizienter lernen',
                   'body': ['<p>Erfolg beim Sprachenlernen bedeutet für eine Führungskraft, den Fokus '
                            'auf die 20% der Inhalte zu legen, die 80% des Ergebnisses liefern. Unser '
                            'didaktischer Ansatz bei Vedium unterstützt Sie dabei, diese Prioritäten '
                            'zu setzen.</p>',
                            '<ul><li><strong>Fokussiertes Vokabular:</strong> Wir eliminieren '
                            'unnötigen Ballast und konzentrieren uns auf das spezifische Vokabular '
                            'Ihrer Branche.</li><li><strong>Simulationen:</strong> Wir spielen Ihre '
                            'nächste Gehaltsverhandlung, Ihr nächstes wichtiges Meeting oder Ihre '
                            'nächste Präsentation durch. Sie erhalten unmittelbares Feedback zur '
                            'Sprache, zur Tonalität und zur kulturellen '
                            'Angemessenheit.</li><li><strong>Monitoring und messbarer '
                            'Fortschritt:</strong> Wir begleiten Sie auf Ihrem Weg vom A1- bis zum '
                            'C1-Niveau mit regelmäßigen Zertifizierungen, sodass Sie Ihren Fortschritt '
                            'schwarz auf weiß sehen können.</li></ul>',
                            '<p>Die Herausforderung für Manager ist oft der Zeitmangel. Unsere '
                            'Live-Plattform ist so gestaltet, dass Sie Ihre Lerneinheiten nahtlos in '
                            'Ihren Kalender integrieren können, ohne an festen, starren Zeiten zu '
                            'scheitern, die nicht zu Ihrem Business-Alltag passen.</p>']},
                  {'heading': 'Conclusão: Investieren Sie in Ihre Sprachkompetenz',
                   'body': ['<p>Die Beherrschung des brasilianischen Portugiesisch ist eine '
                            'Investition, die sich in jedem Meeting, bei jeder Verhandlung und in der '
                            'täglichen Zusammenarbeit mit Ihrem brasilianischen Team bezahlt machen '
                            'wird. Werden Sie zu einer Führungskraft, die nicht nur verwaltet, sondern '
                            'inspiriert und verbindet.</p>',
                            '<p><strong>Bereit für den nächsten Schritt?</strong> Überlassen Sie Ihre '
                            'kulturelle und sprachliche Vorbereitung nicht dem Zufall. Vedium bietet '
                            'Ihnen die Expertise, die Sie für den Erfolg in Brasilien benötigen. <a '
                            'href="/de/portugiesisch-fuer-fuehrungskraefte">Buchen Sie noch heute '
                            'Ihren kostenlosen Einstufungstest bei Vedium</a> und erfahren Sie, wie '
                            'unsere Live-Methodik Ihre berufliche Performance in Brasilien '
                            'transformieren kann.</p>']}],
     'faqs': [{'q': 'Wie viel Zeit muss ich wöchentlich investieren, um Fortschritte zu machen?',
               'a': 'Das hängt von Ihrem Ziel ab, aber bereits 2 bis 3 gezielte '
                    'Live-Unterrichtseinheiten pro Woche führen bei Führungskräften zu spürbaren '
                    'Ergebnissen, da wir uns konsequent auf Ihren Berufsalltag konzentrieren.'},
              {'q': 'Ist brasilianisches Portugiesisch sehr anders als das europäische Portugiesisch?',
               'a': 'Ja, es gibt signifikante Unterschiede in der Aussprache, im Wortschatz und in der '
                    'Grammatik. Da Sie in Brasilien führen, ist es essenziell, das brasilianische '
                    'Portugiesisch zu erlernen, um authentisch und verständlich zu bleiben.'},
              {'q': 'Muss ich als Manager von Anfang an perfekte Grammatik beherrschen?',
               'a': 'Überhaupt nicht. Unsere Priorität liegt auf Ihrer Handlungsfähigkeit. Wir '
                    'vermitteln Grammatik funktional, damit Sie vom ersten Tag an professionell '
                    'kommunizieren können.'},
              {'q': 'Warum ist Vedium für B2B-Kunden und Führungskräfte besser als eine Sprach-App?',
               'a': 'Apps vermitteln Wissen, aber keine Interaktion. Als Führungskraft brauchen Sie '
                    'das Feedback zu Ihrer Tonalität und kulturellen Angemessenheit, das nur ein '
                    'erfahrener Live-Lehrer geben kann.'},
              {'q': 'Wie kann ich eine Probestunde buchen?',
               'a': 'Besuchen Sie einfach unsere Webseite https://vediums.com/, machen Sie den '
                    'Einstufungstest und kontaktieren Sie unser Team. Wir vereinbaren gerne eine erste '
                    'Live-Einheit, um Ihren individuellen Bedarf zu besprechen.'}],
     'cta_title': 'Bereit für Ihr brasilianisches Portugiesisch?',
     'cta_text': 'Buchen Sie einen kostenlosen Einstufungstest und starten Sie mit einem klaren '
                 'Lernplan.',
     'cta_label': 'Kostenlosen Einstufungstest buchen',
     'cta_url': '/de/portugiesisch-fuer-fuehrungskraefte'},
    "portugais-bresilien-pour-expatries-les-bases-avant-de-vivre-au-bresil": {'title': 'Portugais brésilien pour expatriés : les bases avant de vivre au Brésil',
     'meta_description': 'Apprenez les bases du portugais brésilien avant de vivre au Brésil : '
                         'vocabulaire utile, situations réelles et cours en direct.',
     'h1': 'Portugais brésilien pour expatriés : les bases avant de vivre au Brésil',
     'date': '2025-01-08',
     'date_display': '8 janvier 2025',
     'hero_image': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aprender português como língua estrangeira',
     'tag': 'Français',
     'lang': 'fr',
     'lead': 'Les expatriés qui préparent une installation au Brésil doivent apprendre en priorité un '
             'portugais brésilien pratique : se présenter, demander de l’aide, comprendre les '
             'salutations, parler de logement, se déplacer, gérer les courses, communiquer au travail '
             'et décoder les habitudes culturelles du quotidien. L’objectif n’est pas d’arriver '
             'parfaitement bilingue. L’objectif est d’arriver capable d’agir, de répondre et de créer '
             'du lien dès les premières semaines.',
     'sections': [{'heading': '',
                   'body': ['<p>Vivre au Brésil est une expérience riche, chaleureuse et parfois '
                            'déroutante pour une personne francophone. Même dans les grandes villes où '
                            'l’on peut trouver des anglophones, la vie réelle se passe majoritairement '
                            'en portugais : à la réception d’un immeuble, avec un chauffeur, au '
                            'supermarché, dans une pharmacie, dans une réunion, avec un voisin, dans '
                            'une salle de sport ou au téléphone avec un service local. Les '
                            'applications de traduction peuvent aider ponctuellement, mais elles ne '
                            'remplacent pas la confiance de comprendre une phrase spontanée et de '
                            'répondre naturellement.</p>',
                            '<p>C’est pour cette raison qu’un cours de portugais brésilien pour '
                            'expatriés doit aller au-delà de la grammaire. Il doit préparer aux vraies '
                            'situations : écouter des accents, prononcer clairement, poser des '
                            'questions simples, comprendre les formules sociales et éviter les '
                            'malentendus culturels. Chez Vedium, le portugais pour étrangers est '
                            'enseigné en cours en direct, avec un professeur, de la conversation '
                            'réelle et une approche culturelle. Vous apprenez la langue du Brésil '
                            'vivant, pas seulement une liste de règles.</p>']},
                  {'heading': 'Pourquoi apprendre le portugais brésilien avant d’arriver au Brésil',
                   'body': ['<p>Apprendre avant d’arriver réduit le stress, accélère l’adaptation et '
                            'donne plus d’autonomie dans les premières démarches. Même un niveau '
                            'débutant bien orienté peut changer votre première expérience au '
                            'Brésil.</p>',
                            '<p>Les premières semaines dans un nouveau pays demandent beaucoup '
                            'd’énergie. Vous devez comprendre comment fonctionne votre logement, '
                            'reconnaître les documents demandés, confirmer une adresse, acheter des '
                            'produits du quotidien, expliquer un problème, répondre à des messages et '
                            'vous présenter à de nouvelles personnes. Si chaque interaction devient '
                            'une épreuve linguistique, l’installation peut vite devenir fatigante.</p>',
                            '<p>Le portugais brésilien est aussi très relationnel. Les Brésiliens '
                            'utilisent beaucoup de petites formules pour créer de la proximité : « '
                            'tudo bem? », « beleza? », « pois não », « tranquilo », « imagina », « '
                            'valeu ». Ces expressions ne sont pas toujours faciles à traduire mot à '
                            'mot, mais elles sont essentielles pour comprendre le ton de la '
                            'conversation. Un expatrié qui apprend seulement du vocabulaire isolé peut '
                            'connaître des mots et rester bloqué dans la conversation réelle.</p>',
                            '<p>Avant le départ, il est donc utile de travailler trois compétences '
                            ':</p>',
                            '<ul><li><strong>comprendre les phrases fréquentes du quotidien '
                            ';</strong></li><li><strong>répondre avec des structures simples et '
                            'correctes ;</strong></li><li><strong>savoir quand une expression est '
                            'formelle, informelle ou culturelle.</strong></li></ul>',
                            '<p>Les cours en direct sont particulièrement efficaces pour cela, car ils '
                            'permettent de parler, d’être corrigé et de simuler les situations qui '
                            'vous attendent. Une vidéo enregistrée peut expliquer une règle, mais elle '
                            'ne peut pas vous entraîner à répondre à un concierge, à un collègue ou à '
                            'un livreur.</p>',
                            '<p><strong>CTA :</strong> réservez un test de niveau gratuit avec Vedium '
                            'et construisez votre plan de portugais brésilien avant votre arrivée : <a '
                            'href="/fr/portugais-pour-etrangers">https://vediums.com/</a></p>']},
                  {'heading': 'Situation réelle : se présenter et créer un premier contact',
                   'body': ['<p>La première base à maîtriser est la présentation personnelle. Vous '
                            'devez pouvoir dire qui vous êtes, d’où vous venez, pourquoi vous êtes au '
                            'Brésil et ce dont vous avez besoin.</p>',
                            '<p>Pour un expatrié francophone, les premières conversations peuvent être '
                            'simples mais très importantes. Dans un immeuble, on peut vous demander '
                            'votre nom et votre appartement. Au travail, on peut vous demander votre '
                            'poste. Dans une école ou une université, on peut vous demander depuis '
                            'combien de temps vous êtes au Brésil. Dans un commerce, on peut vous '
                            'demander si vous avez besoin d’aide.</p>',
                            '<p>Voici des phrases utiles à connaître dès le début :</p>',
                            '<ul><li><strong>Meu nome é...</strong> — Je '
                            'm’appelle...</li><li><strong>Eu sou da França / da Bélgica / da Suíça / '
                            'do Canadá.</strong> — Je viens de France / de Belgique / de Suisse / du '
                            'Canada.</li><li><strong>Eu vou morar no Brasil.</strong> — Je vais vivre '
                            'au Brésil.</li><li><strong>Eu trabalho com...</strong> — Je travaille '
                            'dans...</li><li><strong>Estou aprendendo português.</strong> — J’apprends '
                            'le portugais.</li><li><strong>Você pode falar mais devagar, por '
                            'favor?</strong> — Pouvez-vous parler plus lentement, s’il vous plaît '
                            '?</li><li><strong>Não entendi. Pode repetir?</strong> — Je n’ai pas '
                            'compris. Pouvez-vous répéter ?</li></ul>',
                            '<p>Ces phrases donnent immédiatement plus de sécurité. Elles montrent '
                            'aussi que vous faites l’effort de parler la langue locale, ce qui est '
                            'souvent très apprécié. Au Brésil, la façon de communiquer compte autant '
                            'que l’information. Un ton ouvert, un sourire et une phrase simple peuvent '
                            'faciliter beaucoup de situations.</p>',
                            '<p>En cours en direct, ces présentations doivent être pratiquées à voix '
                            'haute. Il ne suffit pas de les lire. Il faut apprendre le rythme de la '
                            'phrase, la prononciation des sons nasaux, l’intonation des questions et '
                            'la différence entre une réponse très courte et une réponse plus '
                            'naturelle.</p>']},
                  {'heading': 'Vocabulaire essentiel pour le logement et la vie quotidienne',
                   'body': ['<p>Pour vivre au Brésil, le vocabulaire du logement est prioritaire. Il '
                            'vous aide à gérer l’immeuble, les livraisons, les réparations, les '
                            'voisins et les services de base.</p>',
                            '<p>Beaucoup d’expatriés vivent dans des appartements, parfois avec une '
                            'réception ou une portaria. Ce mot, très courant au Brésil, désigne '
                            'l’entrée ou le poste d’accueil de l’immeuble. Vous pouvez y recevoir des '
                            'colis, laisser une information, confirmer l’arrivée d’un visiteur ou '
                            'demander de l’aide.</p>',
                            '<p>Mots essentiels :</p>',
                            '<ul><li><strong>prédio</strong> — immeuble '
                            ';</li><li><strong>apartamento</strong> — appartement '
                            ';</li><li><strong>portaria</strong> — accueil / entrée de l’immeuble '
                            ';</li><li><strong>porteiro / porteira</strong> — concierge / personne à '
                            'l’accueil ;</li><li><strong>entrega</strong> — livraison '
                            ';</li><li><strong>encomenda</strong> — colis '
                            ';</li><li><strong>elevador</strong> — ascenseur '
                            ';</li><li><strong>chave</strong> — clé ;</li><li><strong>garagem</strong> '
                            '— garage ;</li><li><strong>manutenção</strong> — maintenance / '
                            'réparation.</li></ul>',
                            '<p>Phrases utiles :</p>',
                            '<ul><li><strong>Eu moro no apartamento...</strong> — J’habite dans '
                            'l’appartement...</li><li><strong>Chegou alguma encomenda para '
                            'mim?</strong> — Un colis est-il arrivé pour moi ?</li><li><strong>O '
                            'elevador está funcionando?</strong> — L’ascenseur fonctionne-t-il '
                            '?</li><li><strong>Preciso de ajuda com a internet.</strong> — J’ai besoin '
                            'd’aide avec Internet.</li><li><strong>Pode avisar quando a entrega '
                            'chegar?</strong> — Pouvez-vous me prévenir quand la livraison arrive '
                            '?</li></ul>',
                            '<p>Ce vocabulaire peut sembler très pratique, presque banal. Pourtant, il '
                            'est essentiel. La maîtrise de ces mots permet d’éviter des blocages dans '
                            'des moments où vous êtes fatigué, pressé ou déjà stressé par '
                            'l’installation. Un bon programme de portugais pour étrangers doit donc '
                            'relier le vocabulaire à des scénarios concrets, pas seulement à des '
                            'listes de mots.</p>']},
                  {'heading': 'Se déplacer au Brésil : directions, adresses et transports',
                   'body': ['<p>Pour se déplacer avec confiance, il faut apprendre les adresses, les '
                            'directions, les repères urbains et les phrases de confirmation. Même avec '
                            'une application, vous aurez besoin de parler.</p>',
                            '<p>Au Brésil, il est fréquent de donner des indications avec des repères '
                            ': près de la pharmacie, en face de la banque, au coin de la rue, après le '
                            'marché, à côté de l’immeuble. Un chauffeur peut vous appeler pour '
                            'confirmer le point d’entrée. Un collègue peut vous expliquer comment '
                            'arriver à un bureau. Un voisin peut vous indiquer un commerce à '
                            'proximité.</p>',
                            '<p>Vocabulaire utile :</p>',
                            '<ul><li><strong>rua</strong> — rue ;</li><li><strong>avenida</strong> — '
                            'avenue ;</li><li><strong>esquina</strong> — coin de rue '
                            ';</li><li><strong>entrada</strong> — entrée '
                            ';</li><li><strong>saída</strong> — sortie '
                            ';</li><li><strong>perto</strong> — près ;</li><li><strong>longe</strong> '
                            '— loin ;</li><li><strong>à direita</strong> — à droite '
                            ';</li><li><strong>à esquerda</strong> — à gauche ;</li><li><strong>em '
                            'frente</strong> — en face ;</li><li><strong>ao lado</strong> — à '
                            'côté.</li></ul>',
                            '<p>Phrases à pratiquer :</p>',
                            '<ul><li><strong>Onde fica...?</strong> — Où se trouve... '
                            '?</li><li><strong>É perto daqui?</strong> — Est-ce près d’ici '
                            '?</li><li><strong>Pode me deixar na entrada principal?</strong> — '
                            'Pouvez-vous me déposer à l’entrée principale ?</li><li><strong>Estou '
                            'chegando em cinco minutos.</strong> — J’arrive dans cinq '
                            'minutes.</li><li><strong>Qual é o melhor caminho?</strong> — Quel est le '
                            'meilleur chemin ?</li></ul>',
                            '<p>La difficulté n’est pas seulement de connaître ces mots. Il faut aussi '
                            'les entendre rapidement dans une phrase naturelle. C’est ici que la '
                            'pratique orale fait la différence. En cours en direct, le professeur peut '
                            'jouer le rôle d’un chauffeur, d’un collègue ou d’un passant, puis adapter '
                            'la difficulté à votre niveau.</p>']},
                  {'heading': 'Portugais pour le travail : ce qu’un expatrié doit savoir',
                   'body': ['<p>Pour travailler au Brésil, il faut apprendre à se présenter '
                            'professionnellement, demander une clarification, participer à une réunion '
                            'et comprendre le ton relationnel du milieu professionnel.</p>',
                            '<p>Le portugais du travail n’est pas uniquement technique. Bien sûr, vous '
                            'devrez apprendre le vocabulaire de votre secteur. Mais avant cela, vous '
                            'devez être capable de dire ce que vous faites, de comprendre une '
                            'consigne, de demander un délai, de confirmer une information et '
                            'd’interagir avec politesse.</p>',
                            '<p>Phrases utiles :</p>',
                            '<ul><li><strong>Eu trabalho na área de...</strong> — Je travaille dans le '
                            'domaine de...</li><li><strong>Sou responsável por...</strong> — Je suis '
                            'responsable de...</li><li><strong>Pode me explicar de novo?</strong> — '
                            'Pouvez-vous me réexpliquer ?</li><li><strong>Vou verificar e te '
                            'retorno.</strong> — Je vais vérifier et je vous '
                            'reviens.</li><li><strong>Podemos marcar uma reunião?</strong> — '
                            'Pouvons-nous planifier une réunion ?</li><li><strong>Qual é o '
                            'prazo?</strong> — Quel est le délai ?</li></ul>',
                            '<p>Un point culturel important : dans de nombreuses situations '
                            'professionnelles au Brésil, la relation précède l’exécution. Les échanges '
                            'peuvent commencer par « tudo bem? », quelques mots personnels ou un ton '
                            'plus chaleureux que dans certains contextes européens. Cela ne veut pas '
                            'dire manque de professionnalisme. C’est souvent une manière de créer de '
                            'la confiance.</p>',
                            '<p>Un cours de portugais brésilien pour expatriés doit donc inclure '
                            'l’intelligence culturelle : comment saluer, quand utiliser un ton plus '
                            'direct, comment demander sans paraître brusque, comment remercier, '
                            'comment relancer et comment participer à une conversation de '
                            'groupe.</p>']},
                  {'heading': 'Comment pratiquer avant le départ en 4 étapes',
                   'body': ['<p>La meilleure méthode est de pratiquer par situations, pas par '
                            'chapitres abstraits. Avant de vivre au Brésil, organisez votre '
                            'apprentissage autour de ce que vous devrez vraiment faire.</p>',
                            '<p><strong>Étape 1 : identifiez vos scénarios prioritaires.</strong> '
                            'Faites une liste de vos situations probables : logement, travail, '
                            'transports, courses, santé, école, banque, sport ou vie sociale. Un '
                            'expatrié avec enfants n’a pas les mêmes besoins qu’un étudiant ou qu’un '
                            'cadre transféré.</p>',
                            '<p><strong>Étape 2 : apprenez des phrases complètes.</strong> Ne '
                            'mémorisez pas uniquement des mots isolés. Une phrase complète vous donne '
                            'une structure réutilisable. Par exemple, « Preciso de ajuda com... » peut '
                            'servir pour Internet, un document, une adresse ou un service.</p>',
                            '<p><strong>Étape 3 : parlez à voix haute dès le début.</strong> Le '
                            'portugais brésilien a des sons, des liaisons et une musicalité qui '
                            'demandent de l’entraînement. Lire silencieusement ne suffit pas. Vous '
                            'devez entendre votre propre voix et recevoir des corrections.</p>',
                            '<p><strong>Étape 4 : simulez les conversations réelles.</strong> '
                            'Demandez, répondez, répétez, reformulez. Plus vous pratiquez avant '
                            'l’arrivée, moins vous serez surpris quand quelqu’un parlera vite ou '
                            'utilisera une expression informelle.</p>',
                            '<p>Chez Vedium, cette logique est au cœur des cours : le professeur '
                            'travaille avec vous en direct, corrige votre expression, contextualise '
                            'les phrases et vous aide à construire une confiance progressive. Vous '
                            'restez parce que vous voyez le résultat, pas parce qu’un contrat long '
                            'vous retient.</p>']},
                  {'heading': 'Conclusion avec CTA fort',
                   'body': ['<p>Le portugais brésilien pour expatriés doit être pratique, vivant et '
                            'culturel. Avant de vivre au Brésil, concentrez-vous sur ce qui vous '
                            'donnera de l’autonomie : vous présenter, parler de logement, comprendre '
                            'les directions, gérer les interactions du quotidien, participer au '
                            'travail et demander de l’aide avec naturel.</p>',
                            '<p>La grammaire reste importante, mais elle doit servir la vie réelle. '
                            'Vous n’avez pas besoin de tout savoir avant d’arriver. Vous avez besoin '
                            'd’un plan clair, de phrases utiles, d’une pratique orale régulière et '
                            'd’un professeur capable de vous guider dans les nuances du Brésil.</p>',
                            '<p>Avec Vedium, vous apprenez le portugais brésilien en cours en direct, '
                            'avec conversation, culture et accompagnement. Réservez votre test de '
                            'niveau gratuit et commencez à préparer votre arrivée au Brésil avec plus '
                            'de confiance : <a '
                            'href="/fr/test-de-niveau-de-portugais">https://vediums.com/</a></p>']}],
     'faqs': [{'q': 'Quel portugais dois-je apprendre avant de vivre au Brésil ?',
               'a': 'Vous devez apprendre le portugais brésilien, avec priorité aux situations de la '
                    'vie réelle : salutations, logement, transports, courses, travail, santé et '
                    'demandes d’aide.'},
              {'q': 'Puis-je vivre au Brésil en parlant seulement anglais ?',
               'a': 'Dans certaines grandes villes et entreprises internationales, l’anglais peut '
                    'aider. Mais pour la vie quotidienne, le portugais reste essentiel pour gagner en '
                    'autonomie et créer de meilleures relations.'},
              {'q': 'Combien de temps faut-il pour apprendre les bases utiles ?',
               'a': 'Avec des cours en direct et une pratique régulière, quelques semaines peuvent '
                    'suffire pour construire des bases fonctionnelles. Le temps exact dépend de votre '
                    'rythme, de votre objectif et de votre exposition à la langue.'},
              {'q': 'Les cours en direct sont-ils meilleurs que les applications ?',
               'a': 'Les applications peuvent aider à réviser du vocabulaire, mais les cours en direct '
                    'sont plus efficaces pour parler, corriger la prononciation, poser des questions '
                    'et simuler de vraies conversations au Brésil.'},
              {'q': 'Vedium propose-t-il un test de niveau pour les expatriés ?',
               'a': 'Oui. Vedium propose un test de niveau gratuit pour comprendre votre point de '
                    'départ et vous orienter vers un apprentissage adapté à votre vie au Brésil.'}],
     'cta_title': 'Prêt à commencer votre portugais brésilien ?',
     'cta_text': 'Réservez un test de niveau gratuit et démarrez avec un plan clair.',
     'cta_label': 'Réserver un test de niveau gratuit',
     'cta_url': '/fr/portugais-pour-etrangers'},
    "portugais-du-bresil-pour-familles-qui-s-installent-au-bresil": {'title': "Portugais du Brésil pour familles qui s'installent au Brésil.md",
     'meta_description': '',
     'h1': "Portugais du Brésil pour familles qui s'installent au Brésil.md",
     'date': '2026-05-27',
     'date_display': '27 mai 2026',
     'hero_image': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aprender português como língua estrangeira',
     'tag': 'Français',
     'lang': 'fr',
     'lead': "<strong>Titre SEO :</strong> Portugais du Brésil pour familles : guide d'installation et "
             'intégration réussie',
     'sections': [{'heading': "Pourquoi l'apprentissage du portugais est la clé de votre réussite "
                              'familiale au Brésil',
                   'body': ['<p>Déménager au Brésil en famille est une aventure humaine '
                            "extraordinaire, mais c'est aussi un défi logistique et culturel majeur. "
                            "L'une des erreurs les plus fréquentes que commettent les familles "
                            "expatriées est de penser qu'elles pourront se reposer uniquement sur "
                            "l'anglais ou sur une connaissance scolaire du portugais pour gérer leur "
                            "vie quotidienne. La réalité est tout autre : pour vraiment s'installer, "
                            'scolariser ses enfants, interagir avec le voisinage et naviguer dans les '
                            'services administratifs brésiliens, la maîtrise du portugais du Brésil '
                            'est indispensable.</p>',
                            '<p>Chez <a href="/fr/test-de-niveau-de-portugais">Vedium</a>, nous '
                            "concevons l'apprentissage de la langue non pas comme un exercice "
                            "académique, mais comme une porte d'entrée vers l'<strong>Intelligenz "
                            "Cultural</strong> (Intelligence Culturelle). S'installer au Brésil en "
                            "famille demande de comprendre les codes locaux, d'être capable d'exprimer "
                            'ses besoins avec assurance et de tisser des liens sociaux solides. '
                            'Apprendre en direct avec des professeurs dédiés, plutôt que via des '
                            'applications impersonnelles, est le moyen le plus rapide pour que chaque '
                            'membre de la famille se sente enfin "à la maison" dans sa nouvelle '
                            'réalité.</p>']},
                  {'heading': 'Le vocabulaire essentiel pour la vie quotidienne en famille',
                   'body': ["<p>Quand vous arrivez au Brésil, vous n'avez pas besoin de maîtriser "
                            "immédiatement la littérature classique. Vous avez besoin d'un vocabulaire "
                            'de survie et de connexion qui transforme votre quotidien de stressant en '
                            'gratifiant.</p>',
                            '<ul><li><strong>Gestion de la maison et services :</strong> Savoir '
                            'décrire un problème technique au plombier (<em>encanador</em>) ou '
                            'expliquer vos besoins spécifiques en produits ménagers dans un '
                            'supermarché local (<em>mercado</em>) est la base de votre '
                            'autonomie.</li><li><strong>La vie scolaire :</strong> Communiquer avec '
                            'les enseignants de vos enfants (<em>escola</em>) est primordial. '
                            'Comprendre les circulaires, demander des rendez-vous et suivre les '
                            'progrès scolaires nécessite un portugais clair et '
                            'direct.</li><li><strong>Santé et bien-être :</strong> Savoir expliquer '
                            'des symptômes simples chez un médecin (<em>médico</em>) ou à la pharmacie '
                            "(<em>farmácia</em>) apporte une tranquillité d'esprit inestimable pour "
                            'les parents.</li><li><strong>Les petits échanges qui comptent :</strong> '
                            'Saluer vos voisins ou échanger quelques mots avec le gardien de votre '
                            "immeuble (<em>porteiro</em>) construit le sentiment d'appartenance à une "
                            'communauté.</li></ul>',
                            '<p><strong>Conseil Vedium :</strong> Ne mémorisez pas de listes de mots '
                            'déconnectées. Pratiquez ces situations dans le cadre de nos cours de '
                            'portugais en direct. Nous simulons ces scénarios avec vous pour que, le '
                            "jour J, vous ayez déjà l'habitude des structures de phrases "
                            'nécessaires.</p>']},
                  {'heading': '3 mois pour transformer votre intégration familiale',
                   'body': ["<p>L'intégration d'une famille expatriée se fait souvent par étapes. "
                            'Voici comment structurer votre apprentissage pour maximiser votre impact '
                            ':</p>',
                            "<h3>Mois 1 : La fondation de l'autonomie</h3>",
                            "<p>Votre objectif est de gérer les besoins de base sans dépendre d'un "
                            'interprète.<br>*   <strong>Focus :</strong> Commandes simples, questions '
                            'de localisation, vocabulaire des courses et des services.<br>*   '
                            '<strong>Stratégie :</strong> Soyez patient. Le but est de se faire '
                            "comprendre, pas d'être parfait.<br>*   <strong>Approche Vedium :</strong> "
                            'Nos professeurs vous aident à simuler ces interactions pour réduire '
                            "l'anxiété liée à la nouveauté.</p>",
                            '<h3>Mois 2 : Le pont vers le lien social</h3>',
                            '<p>Une fois l\'autonomie acquise, il est temps de passer au "Petit Talk" '
                            'et à la compréhension des coutumes.<br><em>   <strong>Focus :</strong> '
                            'Comprendre le </em>Jeitinho Brasileiro* (cette manière flexible et '
                            'créative de résoudre les problèmes).<br>*   <strong>Stratégie :</strong> '
                            'Apprenez les nuances du vouvoiement et de la politesse brésilienne pour '
                            'mieux interagir avec le personnel de maison, les enseignants ou les '
                            'autres parents.<br>*   <strong>Approche Vedium :</strong> Nos cours en '
                            'direct vous donnent le contexte culturel que les applications ne peuvent '
                            'pas offrir : le "pourquoi" derrière chaque coutume.</p>',
                            '<h3>Mois 3 : Construire votre communauté</h3>',
                            '<p>Le troisième mois est celui où vous commencez à vous sentir membre à '
                            'part entière de la société brésilienne.<br>*   <strong>Focus :</strong> '
                            'Exprimer vos opinions, participer à des activités de groupe et construire '
                            'des amitiés durables.<br>*   <strong>Stratégie :</strong> Sortez des '
                            "cercles d'expatriés. Utilisez votre portugais pour vous investir dans des "
                            'activités locales ou des centres culturels.<br>*   <strong>Approche '
                            'Vedium :</strong> Nous affinons votre prononciation et élargissons votre '
                            "vocabulaire pour que vous soyez à l'aise dans n'importe quel contexte "
                            'social, professionnel ou privé.</p>']},
                  {'heading': 'Surmonter la barrière de "l\'expatrié" pour atteindre la fluidité',
                   'body': ["<p>L'un des plus grands obstacles pour les familles au Brésil est la "
                            "tentation des Brésiliens de parler anglais avec vous. Parce qu'ils sont "
                            "extrêmement accueillants et curieux, dès qu'ils détectent une hésitation, "
                            "ils passeront à l'anglais.</p>",
                            '<p>Pour contrer cela :<br>1.  <strong>Restez poli mais ferme :</strong> '
                            'Dites simplement : <em>"Pode continuar em português, por favor? Estou '
                            'praticando!"</em> (Pouvez-vous continuer en portugais, s\'il vous plaît ? '
                            "Je m'exerce !).<br>2.  <strong>Immergez-vous :</strong> Évitez de limiter "
                            "vos interactions sociales aux autres familles d'expatriés.<br>3.  "
                            '<strong>Investissez dans un suivi pédagogique :</strong> Les applications '
                            "sont utiles, mais elles ne peuvent pas corriger vos erreurs d'intonation "
                            'ou de contexte culturel en temps réel. Vedium vous propose des cours en '
                            'direct où vous apprenez à maintenir votre portugais dans des conditions '
                            'réelles.</p>']},
                  {'heading': 'Pourquoi choisir le direct plutôt que des cours enregistrés ?',
                   'body': ['<p>Si vous vous reposez uniquement sur des cours enregistrés ou des '
                            "applications, vous accumulerez de l'information théorique, mais vous ne "
                            'développerez pas la confiance nécessaire pour interagir. Pour une '
                            "famille, l'enjeu est la rapidité d'adaptation. Lorsqu'une urgence "
                            "survient, vous avez besoin de réponses immédiates, pas d'un chapitre de "
                            'manuel.</p>',
                            '<p>Chez Vedium, nous ne croyons pas aux contrats de longue durée qui vous '
                            "enferment. Nous croyons en votre résultat. Si vous n'évoluez pas, nous ne "
                            'faisons pas notre travail. Nos étudiants restent avec nous car ils '
                            'constatent des progrès concrets dans leur vie quotidienne au Brésil, '
                            "grâce à des professeurs qui s'adaptent à leurs besoins spécifiques.</p>"]},
                  {'heading': 'Conclusion : Démarrez votre nouvelle vie au Brésil avec Vedium',
                   'body': ['<p>Votre installation réussie au Brésil dépend en grande partie de votre '
                            'capacité à communiquer avec votre environnement. Ne laissez pas cette '
                            'étape au hasard. Équipez votre famille des outils linguistiques et de '
                            "l'intelligence culturelle nécessaires pour transformer ce défi en une "
                            'opportunité de croissance personnelle et familiale.</p>',
                            '<p><strong>Prêts à franchir le pas ?</strong> Assurez-vous une '
                            'intégration en douceur. <a href="/fr/portugais-pour-etrangers">Réservez '
                            "dès aujourd'hui votre test de niveau gratuit chez Vedium</a> et découvrez "
                            'comment nos cours en direct peuvent aider votre famille à maîtriser le '
                            'portugais du Brésil.</p>']}],
     'faqs': [{'q': 'Combien de temps faut-il pour devenir fonctionnel en portugais ?',
               'a': 'Avec une pratique régulière dans nos cours en direct, la plupart des familles '
                    'atteignent un niveau fonctionnel pour la vie quotidienne en 3 à 6 mois. Nous '
                    'privilégions le vocabulaire à haute fréquence pour vous rendre opérationnel '
                    'rapidement.'},
              {'q': "Est-il difficile d'apprendre le portugais si l'on parle déjà une autre langue "
                    'latine ?',
               'a': 'Bien que les langues latines partagent des racines communes, le portugais possède '
                    'ses propres pièges grammaticaux et une phonétique particulière. Nos professeurs '
                    'vous aident à faire la transition sans confusion, en se concentrant sur les '
                    'spécificités du portugais du Brésil.'},
              {'q': 'La grammaire est-elle une priorité absolue pour commencer ?',
               'a': 'Pas au début. La priorité est la communication fonctionnelle. Nous intégrons la '
                    'grammaire progressivement, à mesure que votre aisance augmente, pour que vous '
                    'puissiez vous exprimer sans blocage dès le premier jour.'},
              {'q': 'Pourquoi les cours en direct de Vedium sont-ils plus efficaces que les '
                    'applications ?',
               'a': 'Les applications ne peuvent pas corriger votre ton, votre approche culturelle ou '
                    "vous aider à surmonter l'anxiété de la parole. Dans un cours en direct, vous "
                    'pratiquez de vraies conversations que vous aurez réellement au Brésil, avec un '
                    'feedback personnalisé.'},
              {'q': 'Vedium propose-t-il des cours adaptés aux besoins professionnels et familiaux ?',
               'a': 'Absolument. Nos cours sont entièrement personnalisés. Que vous ayez besoin de '
                    'portugais pour le travail ou pour gérer la logistique familiale, nous adaptons le '
                    "contenu pour qu'il soit utile et pertinent pour vous dès maintenant."}],
     'cta_title': 'Prêt à commencer votre portugais brésilien ?',
     'cta_text': 'Réservez un test de niveau gratuit et démarrez avec un plan clair.',
     'cta_label': 'Réserver un test de niveau gratuit',
     'cta_url': '/fr/portugais-pour-etrangers'},
    "ple-zh-078": {'title': '90天建立巴西葡萄牙语基础的计划',
     'meta_description': '用90天建立巴西葡萄牙语基础：真实巴西生活、工作与学习场景，搭配真人直播课练习。',
     'h1': '90天建立巴西葡萄牙语基础的计划',
     'date': '2026-06-24',
     'date_display': '2026年6月24日',
     'hero_image': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aula de português para estrangeiros na Vedium',
     'tag': '中文',
     'lang': 'zh-CN',
     'lead': '90天可以建立巴西葡萄牙语的基础，但前提是学习目标要现实：不是在三个月内“精通葡萄牙语”，而是能够在巴西的真实生活中开始听懂、敢开口、能提问、能处理常见场景。对准备搬到巴西、在巴西工作、读书或陪同家人长期生活的人来说，巴西葡萄牙语不是一门抽象学科，而是一种每天都会用到的生存能力。',
     'sections': [{'heading': '',
                   'body': ['<p>很多中文母语者一开始会搜索 Portuguese for Brazil、Brazilian Portuguese course 或 '
                            'Portuguese for '
                            'foreigners，因为他们真正需要的不是欧洲葡萄牙语，也不是只会背单词的课程，而是能在巴西使用的语言：在公寓门口和门卫沟通，在餐厅点餐，在药店说明症状，在公司介绍自己，在学校询问作业，在 '
                            'WhatsApp 上回复消息，在日常寒暄中不显得太生硬。</p>',
                            '<p>这篇文章给你一个清晰的90天计划。它把学习拆成三个阶段：第1个月建立声音、句子和生活基础；第2个月进入工作、学习和城市生活场景；第3个月训练真实对话、应急表达和文化理解。每个阶段都强调真人直播课的价值，因为巴西葡萄牙语不仅要“看懂”，更要在真实互动中说出来。</p>']},
                  {'heading': '为什么学习巴西葡萄牙语要以真实场景为核心？',
                   'body': ['<p>学习巴西葡萄牙语要以真实场景为核心，因为你在巴西遇到的问题通常不是“这条语法规则叫什么”，而是“我现在怎么说才不会卡住”。真正影响生活质量的，是你能不能听懂对方的问题，能不能表达自己的需求，能不能确认信息，能不能礼貌地请求帮助。</p>',
                            '<p>在巴西，语言和文化关系很紧密。巴西人常用比较自然、热情、带有寒暄感的表达方式。比如，日常见面时常听到：</p>',
                            '<ul><li>“Oi, tudo bem?” —— 嗨，你好吗？</li><li>“Tudo certo?” —— '
                            '一切都好吗？</li><li>“Pois não?” —— 有什么可以帮您？</li><li>“Pode deixar.” —— '
                            '放心，交给我。</li><li>“Combinado.” —— 说定了。</li><li>“Já já.” —— '
                            '一会儿，很快。</li></ul>',
                            '<p>这些表达不能只靠字面翻译理解。你需要在对话中听、模仿、回应，才能知道它们在什么语气和场景下使用。对初学者来说，最好的路径不是先背完一本语法书，而是从高频场景出发，让语法服务于沟通。</p>',
                            '<p>Vedium '
                            '的巴西葡萄牙语课程强调真人直播课、真实生活情境和文化理解。目标不是让学生孤独地看录播，而是在实时课堂中开口、被纠正、被鼓励，并逐步建立在巴西生活的语言信心。</p>',
                            '<p>CTA：准备来巴西生活、工作或学习？访问 <a '
                            'href="/en/learn-portuguese-brazil">https://vediums.com/</a> '
                            '预约免费水平测试，找到适合你的巴西葡萄牙语起点。</p>']},
                  {'heading': '第1个月：建立发音、问候和基础生存表达',
                   'body': ['<p>第1个月的目标是建立最基本的语言安全感。你不需要说复杂句子，但要能打招呼、介绍自己、说明自己还在学习葡萄牙语、询问价格、地点、时间，并在听不懂时请求对方重复。</p>',
                            '<h3>第1周：先熟悉巴西葡萄牙语的声音</h3>',
                            '<p>中文母语者学习巴西葡萄牙语时，第一关通常是发音和听力节奏。巴西葡萄牙语有鼻音、开闭元音、不同位置的 r '
                            '音，还有非常自然的连读节奏。如果一开始只看文字，很容易以为自己会读，但真正听到巴西人说话时却反应不过来。</p>',
                            '<p>这一周要做三件事：</p>',
                            '<ol><li>每天听5到10分钟巴西葡萄牙语短音频。</li><li>模仿问候语和简单句，不追求速度。</li><li>记录最难听清的声音。</li></ol>',
                            '<p>重点表达：</p>',
                            '<ul><li>“Oi, tudo bem?” —— 你好，最近好吗？</li><li>“Bom dia.” —— '
                            '早上好。</li><li>“Boa tarde.” —— 下午好。</li><li>“Boa noite.” —— '
                            '晚上好。</li><li>“Meu nome é...” —— 我的名字是……</li><li>“Eu sou da China.” —— '
                            '我来自中国。</li><li>“Estou aprendendo português.” —— 我正在学习葡萄牙语。</li></ul>',
                            '<h3>第2周：学会介绍自己和询问基本信息</h3>',
                            '<p>第二周的目标是能够完成最基础的自我介绍和信息确认。你可以练习说自己来自哪里、做什么工作、住在哪里、为什么来巴西，以及自己的葡萄牙语水平。</p>',
                            '<p>核心句型：</p>',
                            '<ul><li>“Eu trabalho com...” —— 我从事……</li><li>“Eu moro em...” —— '
                            '我住在……</li><li>“Eu cheguei ao Brasil recentemente.” —— '
                            '我最近来到巴西。</li><li>“Eu estudo português porque...” —— '
                            '我学习葡萄牙语是因为……</li><li>“Você fala inglês?” —— 你会说英语吗？</li><li>“Pode '
                            'repetir, por favor?” —— 可以请你重复一遍吗？</li><li>“Pode falar mais devagar?” —— '
                            '可以说慢一点吗？</li></ul>',
                            '<p>这类表达非常重要。它们可以帮助你在还不流利时保护自己，让对方知道你正在学习，并愿意调整语速。</p>',
                            '<h3>第3周：掌握数字、时间、价格和地点</h3>',
                            '<p>在巴西生活，数字和时间非常实用。你会在点餐、购物、预约、打车、办手续、看房、上课时反复用到。</p>',
                            '<p>练习主题：</p>',
                            '<ul><li>数字 1 到 '
                            '100；</li><li>日期和星期；</li><li>时间表达；</li><li>价格；</li><li>地址和方向；</li><li>“哪里”“什么时候”“多少钱”。</li></ul>',
                            '<p>常用问题：</p>',
                            '<ul><li>“Quanto custa?” —— 多少钱？</li><li>“Que horas são?” —— '
                            '现在几点？</li><li>“Quando começa?” —— 什么时候开始？</li><li>“Onde fica o banheiro?” '
                            '—— 洗手间在哪里？</li><li>“Como eu chego lá?” —— 我怎么到那里？</li><li>“Qual é o '
                            'endereço?” —— 地址是什么？</li></ul>',
                            '<h3>第4周：模拟真实生活小场景</h3>',
                            '<p>第4周要把前面学到的内容放进场景中，而不是继续孤立背单词。你可以模拟三类情况：咖啡馆点餐、打车、在公寓楼和门卫沟通。</p>',
                            '<p>场景练习示例：</p>',
                            '<ul><li>在咖啡馆点一杯咖啡；</li><li>问 Uber '
                            '司机是否到达正确地址；</li><li>向门卫询问是否有包裹；</li><li>在超市询问是否可以刷卡；</li><li>在药店询问是否需要处方。</li></ul>',
                            '<p>真人直播课在这个阶段很有价值，因为老师可以马上纠正你的发音、语序和用词，让你知道自己说得是否自然。</p>']},
                  {'heading': '第2个月：进入工作、学习和城市生活场景',
                   'body': ['<p>第2个月的目标是从“我能说一些句子”进步到“我能处理常见任务”。这时要开始练习更长一点的表达，比如说明问题、提出请求、确认安排和描述过去发生的事。</p>',
                            '<h3>第5周：住房与公寓生活</h3>',
                            '<p>很多外国人在巴西会住在公寓。你可能需要和 '
                            'porteiro（门卫）、síndico（物业/公寓管理负责人）、proprietário（房东）或 '
                            'manutenção（维修人员）沟通。</p>',
                            '<p>核心词汇：</p>',
                            '<ul><li>apartamento —— 公寓；</li><li>portaria —— 门卫处；</li><li>entrega —— '
                            '包裹/配送；</li><li>manutenção —— 维修；</li><li>elevador —— 电梯；</li><li>água —— '
                            '水；</li><li>luz —— 电/灯；</li><li>internet —— 网络；</li><li>problema —— '
                            '问题。</li></ul>',
                            '<p>实用句子：</p>',
                            '<ul><li>“Chegou uma entrega para mim?” —— 有我的包裹吗？</li><li>“Estou com um '
                            'problema no apartamento.” —— 我的公寓有个问题。</li><li>“O elevador não está '
                            'funcionando.” —— 电梯不能用了。</li><li>“Preciso falar com a manutenção.” —— '
                            '我需要联系维修人员。</li></ul>',
                            '<h3>第6周：工作和会议表达</h3>',
                            '<p>如果你来巴西工作，葡萄牙语会帮助你更好地融入团队。即使公司内部使用英语，日常寒暄、办公室沟通和本地流程仍然经常需要葡萄牙语。</p>',
                            '<p>重点表达：</p>',
                            '<ul><li>“Qual é o prazo?” —— 截止日期是什么时候？</li><li>“Quem é o responsável?” '
                            '—— 谁负责？</li><li>“Podemos marcar uma reunião?” —— 我们可以安排一个会议吗？</li><li>“Só '
                            'para confirmar...” —— 我只是确认一下……</li><li>“Eu não entendi essa parte.” —— '
                            '这一部分我没听懂。</li><li>“Você pode me explicar de novo?” —— '
                            '你可以再解释一遍吗？</li></ul>',
                            '<p>“Só para confirmar” 是非常实用的职场表达。它礼貌、自然，可以减少误会。</p>',
                            '<h3>第7周：学习和学校场景</h3>',
                            '<p>对国际学生或带孩子来巴西的家庭来说，学校和大学场景很重要。你需要理解课程安排、作业、考试、材料、报名和通知。</p>',
                            '<p>常用句子：</p>',
                            '<ul><li>“Onde encontro o material da aula?” —— '
                            '我在哪里找到课堂材料？</li><li>“Quando é a entrega do trabalho?” —— '
                            '作业什么时候交？</li><li>“Esse conteúdo vai cair na prova?” —— '
                            '这个内容会考吗？</li><li>“Como faço a inscrição?” —— 我如何报名？</li><li>“Pode enviar '
                            'por e-mail?” —— 可以通过邮件发送吗？</li></ul>',
                            '<h3>第8周：药店、诊所和基本健康表达</h3>',
                            '<p>健康场景必须提前准备。即使你还不流利，也应该能说出自己哪里不舒服、是否有过敏、是否需要处方、如何服药。</p>',
                            '<p>核心词汇：</p>',
                            '<ul><li>farmácia —— 药店；</li><li>consulta —— 就诊/预约；</li><li>dor —— '
                            '疼痛；</li><li>febre —— 发烧；</li><li>alergia —— 过敏；</li><li>remédio —— '
                            '药；</li><li>receita —— 处方；</li><li>seguro saúde —— 健康保险。</li></ul>',
                            '<p>实用句子：</p>',
                            '<ul><li>“Estou com dor de cabeça.” —— 我头疼。</li><li>“Tenho alergia a...” '
                            '—— 我对……过敏。</li><li>“Precisa de receita?” —— 需要处方吗？</li><li>“Como eu tomo '
                            'esse remédio?” —— 这个药怎么吃？</li><li>“Vocês aceitam meu seguro?” —— '
                            '你们接受我的保险吗？</li></ul>']},
                  {'heading': '第3个月：建立对话能力、文化理解和持续学习节奏',
                   'body': ['<p>第3个月的目标是提升独立沟通能力。你开始练习更完整地说明情况、表达观点、讲过去经历、谈未来计划，并理解巴西人更自然的回答方式。</p>',
                            '<h3>第9周：从短句进入小对话</h3>',
                            '<p>你要开始练习“问一句、听一句、再追问一句”。这比背很多单词更接近真实沟通。</p>',
                            '<p>常用追问：</p>',
                            '<ul><li>“Como assim?” —— 什么意思？</li><li>“Pode me dar um exemplo?” —— '
                            '可以给我一个例子吗？</li><li>“E depois?” —— 然后呢？</li><li>“O que você recomenda?” —— '
                            '你推荐什么？</li><li>“Tem outra opção?” —— 有其他选择吗？</li></ul>',
                            '<p>这些句子能让你把对话继续下去。</p>',
                            '<h3>第10周：学习巴西人的自然表达</h3>',
                            '<p>巴西葡萄牙语中有很多高频口语词。它们不一定是教科书最先讲的内容，但在真实生活中非常常见。</p>',
                            '<p>例如：</p>',
                            '<ul><li>“tá bom” —— 好的；</li><li>“beleza” —— 好/没问题；</li><li>“pois é” —— '
                            '是啊/可不是；</li><li>“né” —— 对吧；</li><li>“então” —— 那么/所以；</li><li>“fica '
                            'tranquilo” —— 放心；</li><li>“deixa comigo” —— 交给我。</li></ul>',
                            '<p>学习这些表达能让你更快听懂日常对话，也能减少“我每个词都学过，但整句听不懂”的挫败感。</p>',
                            '<h3>第11周：职场、学习和社交综合练习</h3>',
                            '<p>这一周要把不同场景混合起来。你可以用一个主题做综合练习，例如“我在巴西第一周遇到的问题”“我如何介绍自己的工作”“我如何预约服务”。</p>',
                            '<p>练习方式：</p>',
                            '<ol><li>写出5个关键词。</li><li>用葡萄牙语说出5个短句。</li><li>录音1分钟。</li><li>在直播课上请老师纠正。</li><li>再说一遍，比较前后差异。</li></ol>',
                            '<p>这比单纯看课程更有效，因为你真的在输出语言。</p>',
                            '<h3>第12周：复盘90天并制定下一阶段目标</h3>',
                            '<p>最后一周要复盘，而不是盲目继续。你需要知道自己已经能做什么，还不能做什么，下一阶段应该往 A2、B1 还是某个具体目标前进。</p>',
                            '<p>可以问自己：</p>',
                            '<ul><li>我能介绍自己吗？</li><li>我能点餐和购物吗？</li><li>我能问路和确认地址吗？</li><li>我能在工作中问简单问题吗？</li><li>我能说明一个基本问题吗？</li><li>我能听懂常见问候和回答吗？</li><li>我最需要提高的是听力、口语、词汇还是语法？</li></ul>',
                            '<p>这个复盘也适合在真人直播课中完成。老师可以帮你判断真实水平，而不是只凭感觉。</p>',
                            '<p>CTA：90天之后，最重要的是继续向可使用的葡萄牙语前进。访问 <a '
                            'href="/en/portuguese-placement-test">https://vediums.com/</a> '
                            '预约免费水平测试，了解下一阶段应该如何学习。</p>']},
                  {'heading': '90天学习计划总表',
                   'body': ['<p>下面是一个可执行的90天框架：</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>阶段</th><th>时间</th><th>学习重点</th><th>目标</th></tr></thead><tbody><tr><td>第1阶段</td><td>第1—30天</td><td>发音、问候、数字、地点、价格、基础句</td><td>建立生存表达</td></tr><tr><td>第2阶段</td><td>第31—60天</td><td>住房、工作、学习、健康、服务场景</td><td>处理常见任务</td></tr><tr><td>第3阶段</td><td>第61—90天</td><td>小对话、追问、自然表达、复盘</td><td>提升独立沟通</td></tr></tbody></table>',
                            '<p>每周建议安排：</p>',
                            '<ul><li>1到2次真人直播课；</li><li>3次短时间自学，每次15到30分钟；</li><li>1次真实场景练习；</li><li>1次复习和录音；</li><li>每周积累10到20个高频词。</li></ul>',
                            '<p>对忙碌的成年人来说，这样的节奏比每天硬背两小时更现实。语言学习靠持续接触，而不是一次性冲刺。</p>']},
                  {'heading': '为什么真人直播课比只看录播更适合初学者？',
                   'body': ['<p>真人直播课更适合初学者，因为你需要即时反馈。巴西葡萄牙语的发音、语气、礼貌表达和真实回答，都需要在互动中练习。录播可以介绍知识，但不能判断你是否说得自然，也不能根据你的错误调整练习。</p>',
                            '<p>在直播课中，你可以：</p>',
                            '<ul><li>练习发音并被纠正；</li><li>模拟真实巴西场景；</li><li>学会如何提问和追问；</li><li>理解表达背后的文化；</li><li>建立开口信心；</li><li>按水平逐步学习；</li><li>避免长期孤立学习后仍然不敢说。</li></ul>',
                            '<p>Vedium '
                            '的课程是100%在线真人直播课，没有长期合约束缚。学生继续学习，是因为感受到进步，而不是因为被合同锁住。这对外国学习者尤其重要：你可以先了解自己的水平，再选择适合生活、工作或学习目标的路径。</p>']},
                  {'heading': '结论：90天的目标不是完美，而是能开始使用',
                   'body': ['<p>90天建立巴西葡萄牙语基础，最重要的不是追求完美，而是建立可以继续成长的语言能力。你需要会问候、会说明自己、会请求重复、会处理餐厅、交通、住房、健康、工作和学习中的基本场景。你也需要开始理解巴西人的真实表达方式，而不只是背书面句子。</p>',
                            '<p>如果你准备来巴西，或者已经在巴西生活，越早建立实用基础，日常压力就越小。语言会帮助你更独立，也会帮助你更接近巴西文化和当地人。</p>',
                            '<p>Vedium '
                            '提供面向外国人的巴西葡萄牙语真人直播课，结合真实场景、核心词汇、文化理解和口语练习。没有长期合约，学习关系建立在真实进步之上。</p>',
                            '<p>现在访问 <a href="/en/learn-portuguese-brazil">https://vediums.com/</a> '
                            '预约免费水平测试，开始你的90天巴西葡萄牙语基础计划。</p>']}],
     'faqs': [{'q': '90天可以学会巴西葡萄牙语吗？',
               'a': '90天不能保证流利，但可以建立非常重要的基础。你可以学会问候、自我介绍、常见生活表达、工作和学习中的基本问题，并开始用葡萄牙语处理简单场景。'},
              {'q': '巴西葡萄牙语和欧洲葡萄牙语一样吗？',
               'a': '不完全一样。两者在发音、词汇、日常表达和语气上都有差异。准备在巴西生活、工作或学习的人，应该优先学习巴西葡萄牙语。'},
              {'q': '初学者应该先学语法还是先学实用表达？',
               'a': '初学者应该把实用表达放在前面，让语法服务于沟通。先学会打招呼、提问、说明需求和请求重复，再逐步系统学习语法会更有效。'},
              {'q': '只用应用程序可以学好巴西葡萄牙语吗？',
               'a': '应用程序可以帮助记单词和做重复练习，但不够完整。发音、口语反应、真实对话和文化理解更适合通过真人直播课练习。'},
              {'q': 'Vedium 有面向外国人的巴西葡萄牙语课程吗？',
               'a': '有。Vedium 提供面向外国人、外派员工、留学生和在巴西生活者的巴西葡萄牙语真人直播课，强调真实场景、文化理解和口语信心。'}],
     'cta_title': '准备好开始学习巴西葡萄牙语了吗？',
     'cta_text': '预约免费水平测试，找到适合你的起点。',
     'cta_label': 'Learn about the Portuguese course',
     'cta_url': '/en/learn-portuguese-brazil'},
    "ple-ru-077": {'title': 'Реалистичный план изучения бразильского португальского на 90 дней',
     'meta_description': 'Реалистичный план на 90 дней для изучения бразильского португальского: '
                         'жизнь, работа, учеба и практика на живых уроках.',
     'h1': 'Реалистичный план изучения бразильского португальского на 90 дней',
     'date': '2026-06-17',
     'date_display': '17 июня 2026 г.',
     'hero_image': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1100&h=560&fit=crop&q=80',
     'hero_alt': 'Aprender português como língua estrangeira',
     'tag': 'Русский',
     'lang': 'ru-RU',
     'lead': 'Реалистичный план изучения бразильского португальского на 90 дней должен быть построен '
             'вокруг реальных ситуаций в Бразилии: прилет, жилье, транспорт, работа, учеба, общение с '
             'соседями, поход в аптеку, прием у врача, разговоры в офисе, сообщения в WhatsApp и '
             'базовая социальная интеграция. За три месяца не стоит обещать себе идеальную беглость, '
             'но можно создать прочный фундамент: начать понимать частые фразы, говорить в простых '
             'ситуациях, задавать вопросы и чувствовать себя увереннее в повседневной жизни.',
     'sections': [{'heading': '',
                   'body': ['<p>Для русскоговорящих студентов, специалистов, релокационных команд и '
                            'экспатов бразильский португальский — это не просто “еще один иностранный '
                            'язык”. Это инструмент адаптации. В Бразилии он помогает решать бытовые '
                            'задачи, строить рабочие отношения, понимать культуру общения и '
                            'чувствовать себя не гостем, который постоянно зависит от перевода, а '
                            'человеком, который постепенно входит в местную жизнь.</p>',
                            '<p>Важно изучать именно бразильский вариант португальского. Если ваша '
                            'цель — жить, работать или учиться в Бразилии, вам нужны бразильское '
                            'произношение, местные выражения, реальные диалоги и культурные '
                            'особенности общения. Запросы вроде Portuguese for Brazil, Brazilian '
                            'Portuguese course и Portuguese for foreigners часто появляются именно '
                            'потому, что людям нужен практический язык для Бразилии, а не абстрактный '
                            'курс грамматики.</p>',
                            '<p>Этот план на 90 дней показывает, что учить сначала, как распределить '
                            'темы по неделям и почему живые онлайн-уроки помогают быстрее перейти от '
                            '“я понимаю отдельные слова” к “я могу участвовать в разговоре”.</p>']},
                  {'heading': 'Почему 90 дней — хороший срок для старта?',
                   'body': ['<p>90 дней — хороший срок, потому что он достаточно длинный для '
                            'формирования привычки и достаточно короткий, чтобы сохранять фокус. За '
                            'этот период можно пройти путь от первых приветствий до простых разговоров '
                            'о жизни, работе, учебе и бытовых задачах.</p>',
                            '<p>Главная ошибка новичков — пытаться выучить все сразу. Человек '
                            'скачивает приложения, открывает видео, читает правила, выписывает сотни '
                            'слов, но не понимает, что именно ему нужно для первых месяцев в Бразилии. '
                            'В результате знания остаются разрозненными: слова есть, а говорить '
                            'трудно.</p>',
                            '<p>Реалистичный план должен отвечать на три вопроса:</p>',
                            '<ul><li>Что мне понадобится в Бразилии в первую очередь?</li><li>Какие '
                            'фразы помогут мне не растеряться?</li><li>Где мне нужна практика с '
                            'преподавателем, а не только самостоятельное чтение?</li></ul>',
                            '<p>Бразильский португальский нужно учить как язык действия. Не просто '
                            '“знать слово”, а уметь заказать еду, спросить дорогу, уточнить адрес, '
                            'записаться на прием, объяснить проблему с квартирой, задать вопрос на '
                            'работе и попросить человека говорить медленнее.</p>',
                            '<p>Vedium обучает бразильскому португальскому через живые онлайн-уроки, '
                            'потому что реальная коммуникация требует реакции, обратной связи и '
                            'практики. Записанный урок может объяснить тему, но он не исправит ваше '
                            'произношение, не задаст уточняющий вопрос и не поможет перестроить фразу '
                            'в реальном времени.</p>',
                            '<p>CTA: Если вы готовитесь к жизни, работе или учебе в Бразилии, '
                            'запишитесь на бесплатную проверку уровня на <a '
                            'href="/ru/portugalskiy-dlya-inostrantsev">https://vediums.com/</a> и '
                            'начните с понятного маршрута обучения.</p>']},
                  {'heading': 'Месяц 1: выживание, произношение и первые диалоги',
                   'body': ['<p>Первый месяц нужен для базовой языковой безопасности. Ваша цель — не '
                            'говорить сложно, а перестать чувствовать полную беспомощность в простых '
                            'ситуациях.</p>',
                            '<p>Фокус первого месяца:</p>',
                            '<ul><li>приветствия;</li><li>представление себя;</li><li>просьба '
                            'повторить;</li><li>цифры и время;</li><li>цены;</li><li>базовые '
                            'вопросы;</li><li>транспорт;</li><li>кафе и рестораны;</li><li>отель или '
                            'квартира;</li><li>понимание частых ответов.</li></ul>',
                            '<h3>Неделя 1: звуки и первые фразы</h3>',
                            '<p>Начните с бразильского произношения. Русскоговорящим ученикам важно '
                            'привыкнуть к носовым звукам, открытым и закрытым гласным, мягкому ритму '
                            'фразы и разным вариантам звука “r”. Не нужно сразу говорить быстро. Нужно '
                            'говорить понятно.</p>',
                            '<p>Выучите и отработайте:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Португальский</th><th>Русский</th></tr></thead><tbody><tr><td>Oi, '
                            'tudo bem?</td><td>Привет, как дела?</td></tr><tr><td>Bom '
                            'dia.</td><td>Доброе утро.</td></tr><tr><td>Boa tarde.</td><td>Добрый '
                            'день.</td></tr><tr><td>Boa noite.</td><td>Добрый вечер / спокойной '
                            'ночи.</td></tr><tr><td>Meu nome é...</td><td>Меня '
                            'зовут...</td></tr><tr><td>Eu sou da Rússia.</td><td>Я из '
                            'России.</td></tr><tr><td>Estou aprendendo português.</td><td>Я учу '
                            'португальский.</td></tr><tr><td>Eu falo pouco português.</td><td>Я '
                            'немного говорю по-португальски.</td></tr></tbody></table>',
                            '<p>Самая полезная фраза первой недели:</p>',
                            '<p><strong>“Desculpa, eu falo pouco português. Pode falar mais '
                            'devagar?”</strong><br>Извините, я немного говорю по-португальски. Можете '
                            'говорить медленнее?</p>',
                            '<p>Эта фраза сразу снижает стресс. Вы объясняете свой уровень и просите '
                            'собеседника адаптировать речь.</p>',
                            '<h3>Неделя 2: вопросы и базовая ориентация</h3>',
                            '<p>На второй неделе учите вопросы. Вопросы важнее идеальных ответов, '
                            'потому что они помогают получать помощь.</p>',
                            '<p>Основные вопросительные слова:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Португальский</th><th>Русский</th></tr></thead><tbody><tr><td>O '
                            'que?</td><td>Что?</td></tr><tr><td>Quem?</td><td>Кто?</td></tr><tr><td>Onde?</td><td>Где?</td></tr><tr><td>Quando?</td><td>Когда?</td></tr><tr><td>Como?</td><td>Как?</td></tr><tr><td>Quanto?</td><td>Сколько?</td></tr><tr><td>Qual?</td><td>Какой '
                            '/ который?</td></tr><tr><td>Por '
                            'quê?</td><td>Почему?</td></tr></tbody></table>',
                            '<p>Практические фразы:</p>',
                            '<ul><li>“Onde fica o banheiro?” — Где находится туалет?</li><li>“Quanto '
                            'custa?” — Сколько стоит?</li><li>“Como eu chego lá?” — Как мне туда '
                            'добраться?</li><li>“Qual é o endereço?” — Какой адрес?</li><li>“Quando '
                            'começa?” — Когда начинается?</li><li>“Pode repetir, por favor?” — Можете '
                            'повторить, пожалуйста?</li></ul>',
                            '<p>На живом уроке важно тренировать не только сами вопросы, но и ответы. '
                            'В реальности человек может ответить быстро, с акцентом, с жестами или с '
                            'местными словами. Преподаватель может смоделировать это безопасно и '
                            'постепенно.</p>',
                            '<h3>Неделя 3: кафе, магазин, транспорт</h3>',
                            '<p>Третья неделя должна быть максимально бытовой. В Бразилии вы быстро '
                            'столкнетесь с ресторанами, пекарнями, супермаркетами, доставкой, Uber, '
                            'метро, автобусами и оплатой картой.</p>',
                            '<p>Ключевая лексика:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Португальский</th><th>Русский</th></tr></thead><tbody><tr><td>café</td><td>кофе</td></tr><tr><td>água</td><td>вода</td></tr><tr><td>comida</td><td>еда</td></tr><tr><td>restaurante</td><td>ресторан</td></tr><tr><td>mercado</td><td>магазин '
                            '/ '
                            'рынок</td></tr><tr><td>cartão</td><td>карта</td></tr><tr><td>dinheiro</td><td>наличные</td></tr><tr><td>endereço</td><td>адрес</td></tr><tr><td>motorista</td><td>водитель</td></tr><tr><td>entrada</td><td>вход</td></tr><tr><td>saída</td><td>выход</td></tr></tbody></table>',
                            '<p>Фразы:</p>',
                            '<ul><li>“Aceita cartão?” — Вы принимаете карту?</li><li>“Quero um café, '
                            'por favor.” — Я хочу кофе, пожалуйста.</li><li>“A conta, por favor.” — '
                            'Счет, пожалуйста.</li><li>“Onde eu pego o Uber?” — Где мне сесть в '
                            'Uber?</li><li>“Pode me deixar aqui?” — Можете высадить меня '
                            'здесь?</li><li>“Esse é o endereço?” — Это адрес?</li></ul>',
                            '<p>Цель недели — научиться решать маленькие задачи. Даже если вы '
                            'ошибаетесь, вы уже начинаете взаимодействовать.</p>',
                            '<h3>Неделя 4: первая мини-разговорная практика</h3>',
                            '<p>На четвертой неделе соедините темы в простые сценарии. Например:</p>',
                            '<ul><li>вы прилетели в аэропорт;</li><li>вы заселяетесь в '
                            'отель;</li><li>вы покупаете воду и еду;</li><li>вы едете на '
                            'такси;</li><li>вы спрашиваете дорогу;</li><li>вы говорите, что учите '
                            'португальский.</li></ul>',
                            '<p>Пример мини-диалога:</p>',
                            '<p><strong>Você:</strong> Boa tarde. Eu tenho uma reserva.<br>Добрый '
                            'день. У меня есть бронь.</p>',
                            '<p><strong>Recepcionista:</strong> Qual é o seu nome?<br>Как вас '
                            'зовут?</p>',
                            '<p><strong>Você:</strong> Meu nome é Anna Petrova.<br>Меня зовут Анна '
                            'Петрова.</p>',
                            '<p><strong>Recepcionista:</strong> Seu passaporte, por favor.<br>Ваш '
                            'паспорт, пожалуйста.</p>',
                            '<p><strong>Você:</strong> Claro. Aqui está.<br>Конечно. Вот он.</p>',
                            '<p>Такие диалоги нужно проговаривать вслух. Португальский должен стать не '
                            'только текстом в тетради, но и движением речи.</p>']},
                  {'heading': 'Месяц 2: жизнь в Бразилии, работа и учеба',
                   'body': ['<p>Второй месяц переводит вас от выживания к более самостоятельному '
                            'общению. Вы начинаете описывать проблемы, договариваться о времени, '
                            'говорить о работе, учебе и жилье.</p>',
                            '<p>Фокус второго месяца:</p>',
                            '<ul><li>квартира и дом;</li><li>общение с консьержем или администрацией '
                            'здания;</li><li>аптека и здоровье;</li><li>работа и '
                            'встречи;</li><li>учеба;</li><li>сообщения;</li><li>прошедшее и будущее '
                            'время в простых фразах.</li></ul>',
                            '<h3>Неделя 5: жилье и бытовые проблемы</h3>',
                            '<p>Если вы живете в Бразилии, вам часто придется говорить с porteiro — '
                            'сотрудником на входе в здание, с владельцем квартиры, управляющим или '
                            'мастером.</p>',
                            '<p>Лексика:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Португальский</th><th>Русский</th></tr></thead><tbody><tr><td>apartamento</td><td>квартира</td></tr><tr><td>portaria</td><td>вход '
                            '/ пост охраны</td></tr><tr><td>porteiro</td><td>консьерж / сотрудник на '
                            'входе</td></tr><tr><td>entrega</td><td>доставка / '
                            'посылка</td></tr><tr><td>manutenção</td><td>ремонт / '
                            'обслуживание</td></tr><tr><td>problema</td><td>проблема</td></tr><tr><td>água</td><td>вода</td></tr><tr><td>luz</td><td>свет '
                            '/ '
                            'электричество</td></tr><tr><td>internet</td><td>интернет</td></tr><tr><td>chave</td><td>ключ</td></tr></tbody></table>',
                            '<p>Фразы:</p>',
                            '<ul><li>“Chegou uma entrega para mim?” — Мне пришла '
                            'посылка?</li><li>“Estou com um problema no apartamento.” — У меня '
                            'проблема в квартире.</li><li>“A internet não está funcionando.” — '
                            'Интернет не работает.</li><li>“A chave não funciona.” — Ключ не '
                            'работает.</li><li>“Preciso falar com a manutenção.” — Мне нужно '
                            'поговорить с сервисной службой.</li></ul>',
                            '<p>Эти фразы дают реальную автономию. Вы можете не говорить идеально, но '
                            'вас поймут.</p>',
                            '<h3>Неделя 6: работа и профессиональное общение</h3>',
                            '<p>Даже если ваша компания международная, в Бразилии португальский '
                            'помогает в неформальном общении, локальных процессах и интеграции в '
                            'команду.</p>',
                            '<p>Лексика:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Португальский</th><th>Русский</th></tr></thead><tbody><tr><td>trabalho</td><td>работа</td></tr><tr><td>reunião</td><td>встреча '
                            '/ '
                            'совещание</td></tr><tr><td>prazo</td><td>срок</td></tr><tr><td>equipe</td><td>команда</td></tr><tr><td>projeto</td><td>проект</td></tr><tr><td>responsável</td><td>ответственный</td></tr><tr><td>relatório</td><td>отчет</td></tr><tr><td>mensagem</td><td>сообщение</td></tr><tr><td>e-mail</td><td>электронная '
                            'почта</td></tr><tr><td>chamada</td><td>звонок / '
                            'видеозвонок</td></tr></tbody></table>',
                            '<p>Фразы:</p>',
                            '<ul><li>“Qual é o prazo?” — Какой срок?</li><li>“Quem é o responsável?” — '
                            'Кто ответственный?</li><li>“Podemos marcar uma reunião?” — Мы можем '
                            'назначить встречу?</li><li>“Só para confirmar...” — Просто чтобы '
                            'подтвердить...</li><li>“Eu não entendi essa parte.” — Я не понял эту '
                            'часть.</li><li>“Você pode explicar de novo?” — Можете объяснить еще '
                            'раз?</li></ul>',
                            '<p>Фраза “Só para confirmar...” очень полезна. Она звучит вежливо и '
                            'помогает избежать недопонимания.</p>',
                            '<h3>Неделя 7: учеба и образовательная среда</h3>',
                            '<p>Если вы студент или проходите курс в Бразилии, вам понадобится лексика '
                            'для расписания, заданий, преподавателей и материалов.</p>',
                            '<p>Лексика:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Португальский</th><th>Русский</th></tr></thead><tbody><tr><td>aula</td><td>урок '
                            '/ занятие</td></tr><tr><td>professor / '
                            'professora</td><td>преподаватель</td></tr><tr><td>aluno / '
                            'aluna</td><td>студент / '
                            'ученица</td></tr><tr><td>material</td><td>материал</td></tr><tr><td>prova</td><td>тест '
                            '/ экзамен</td></tr><tr><td>trabalho</td><td>работа / '
                            'задание</td></tr><tr><td>prazo</td><td>срок</td></tr><tr><td>nota</td><td>оценка</td></tr><tr><td>inscrição</td><td>регистрация</td></tr><tr><td>curso</td><td>курс</td></tr></tbody></table>',
                            '<p>Фразы:</p>',
                            '<ul><li>“Quando é a aula?” — Когда занятие?</li><li>“Onde encontro o '
                            'material?” — Где найти материал?</li><li>“Quando é a entrega do '
                            'trabalho?” — Когда сдавать работу?</li><li>“Esse conteúdo vai cair na '
                            'prova?” — Это будет на тесте?</li><li>“Como faço a inscrição?” — Как '
                            'зарегистрироваться?</li></ul>',
                            '<h3>Неделя 8: здоровье и аптека</h3>',
                            '<p>Медицинские ситуации нельзя откладывать до “когда-нибудь потом”. Даже '
                            'базовые фразы могут быть очень важны.</p>',
                            '<p>Лексика:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Португальский</th><th>Русский</th></tr></thead><tbody><tr><td>farmácia</td><td>аптека</td></tr><tr><td>consulta</td><td>прием '
                            'у врача</td></tr><tr><td>médico / '
                            'médica</td><td>врач</td></tr><tr><td>dor</td><td>боль</td></tr><tr><td>febre</td><td>температура</td></tr><tr><td>alergia</td><td>аллергия</td></tr><tr><td>remédio</td><td>лекарство</td></tr><tr><td>receita</td><td>рецепт</td></tr><tr><td>seguro '
                            'saúde</td><td>медицинская '
                            'страховка</td></tr><tr><td>emergência</td><td>экстренная '
                            'ситуация</td></tr></tbody></table>',
                            '<p>Фразы:</p>',
                            '<ul><li>“Estou com dor de cabeça.” — У меня болит голова.</li><li>“Estou '
                            'com febre.” — У меня температура.</li><li>“Tenho alergia a...” — У меня '
                            'аллергия на...</li><li>“Precisa de receita?” — Нужен '
                            'рецепт?</li><li>“Como eu tomo esse remédio?” — Как принимать это '
                            'лекарство?</li><li>“Vocês aceitam meu seguro?” — Вы принимаете мою '
                            'страховку?</li></ul>',
                            '<p>Живой урок здесь особенно полезен, потому что преподаватель может '
                            'проиграть ситуацию “аптека”, “регистратура”, “врач” и научить вас не '
                            'теряться.</p>']},
                  {'heading': 'Месяц 3: уверенность, диалоги и культурная адаптация',
                   'body': ['<p>Третий месяц нужен для перехода от отдельных фраз к более живому '
                            'общению. Вы начинаете задавать уточняющие вопросы, рассказывать о '
                            'прошлом, планировать будущее и понимать естественные выражения '
                            'бразильцев.</p>',
                            '<p>Фокус третьего месяца:</p>',
                            '<ul><li>маленькие диалоги;</li><li>уточняющие '
                            'вопросы;</li><li>естественные разговорные выражения;</li><li>прошедшее '
                            'время;</li><li>планы на будущее;</li><li>рабочие и учебные '
                            'сценарии;</li><li>культурная адаптация;</li><li>итоговая проверка '
                            'уровня.</li></ul>',
                            '<h3>Неделя 9: уточняющие вопросы</h3>',
                            '<p>Уточняющие вопросы помогают поддерживать разговор и решать задачи.</p>',
                            '<p>Полезные фразы:</p>',
                            '<ul><li>“Como assim?” — В каком смысле?</li><li>“Pode me dar um exemplo?” '
                            '— Можете дать пример?</li><li>“E depois?” — А потом?</li><li>“Tem outra '
                            'opção?” — Есть другой вариант?</li><li>“O que você recomenda?” — Что вы '
                            'рекомендуете?</li><li>“Isso é comum no Brasil?” — Это обычно для '
                            'Бразилии?</li><li>“Pode escrever?” — Можете написать?</li></ul>',
                            '<p>Эти фразы делают вас активным участником разговора. Вы не просто '
                            'слушаете, а уточняете и продвигаете диалог.</p>',
                            '<h3>Неделя 10: естественная речь бразильцев</h3>',
                            '<p>Бразильцы часто используют короткие разговорные выражения. Они не '
                            'всегда понятны по прямому переводу, но очень важны для жизни.</p>',
                            '<p>Примеры:</p>',
                            '<table class="vd-table"><thead><tr><th>Выражение</th><th>Приблизительный '
                            'смысл</th></tr></thead><tbody><tr><td>Tá '
                            'bom.</td><td>Хорошо.</td></tr><tr><td>Beleza.</td><td>Отлично / '
                            'окей.</td></tr><tr><td>Combinado.</td><td>Договорились.</td></tr><tr><td>Pois '
                            'é.</td><td>Да, вот так / действительно.</td></tr><tr><td>Fica '
                            'tranquilo.</td><td>Не волнуйтесь.</td></tr><tr><td>Pode '
                            'deixar.</td><td>Хорошо, я займусь / оставьте это мне.</td></tr><tr><td>Já '
                            'já.</td><td>Скоро / вот-вот.</td></tr><tr><td>Né?</td><td>Да? / правда? / '
                            'не так ли?</td></tr></tbody></table>',
                            '<p>Их нужно не только перевести, но и услышать в контексте. На живом '
                            'уроке можно тренировать интонацию, потому что одно и то же выражение '
                            'может звучать по-разному в зависимости от ситуации.</p>',
                            '<h3>Неделя 11: рассказы о прошлом и планах</h3>',
                            '<p>Чтобы общаться свободнее, вам нужно говорить не только “сейчас”, но и '
                            'о прошлом и будущем.</p>',
                            '<p>Практические фразы:</p>',
                            '<ul><li>“Ontem eu fui ao mercado.” — Вчера я ходил(а) в '
                            'магазин.</li><li>“Semana passada eu tive uma reunião.” — На прошлой '
                            'неделе у меня была встреча.</li><li>“Amanhã eu vou trabalhar de casa.” — '
                            'Завтра я буду работать из дома.</li><li>“No fim de semana eu vou viajar.” '
                            '— На выходных я поеду в поездку.</li><li>“Eu cheguei ao Brasil há dois '
                            'meses.” — Я приехал(а) в Бразилию два месяца назад.</li></ul>',
                            '<p>Не нужно сразу изучать всю систему времен идеально. Сначала выучите '
                            'самые полезные модели и используйте их в реальных историях.</p>',
                            '<h3>Неделя 12: итоговая практика и план следующего этапа</h3>',
                            '<p>Последняя неделя — это не конец, а переход. Нужно понять, что уже '
                            'получается, а что требует дальнейшей работы.</p>',
                            '<p>Проверьте себя:</p>',
                            '<ul><li>Могу ли я представиться?</li><li>Могу ли я объяснить, что учу '
                            'португальский?</li><li>Могу ли я заказать еду?</li><li>Могу ли я спросить '
                            'дорогу?</li><li>Могу ли я решить проблему в отеле или '
                            'квартире?</li><li>Могу ли я задать вопрос на работе?</li><li>Могу ли я '
                            'попросить повторить или говорить медленнее?</li><li>Могу ли я рассказать '
                            'простую историю о прошлом?</li></ul>',
                            '<p>Если большая часть ответов “да, но с ошибками”, это хороший результат. '
                            'Ошибки — часть процесса. Главное, что у вас появилась языковая база для '
                            'продолжения.</p>',
                            '<p>CTA: После 90 дней важно не останавливаться. Запишитесь на бесплатную '
                            'проверку уровня на <a '
                            'href="/ru/portugalskiy-dlya-rukovoditeley">https://vediums.com/</a> и '
                            'узнайте, какой следующий шаг поможет вам говорить увереннее.</p>']},
                  {'heading': 'Как выглядит недельный ритм обучения?',
                   'body': ['<p>Реалистичный ритм обучения не должен разрушать вашу жизнь. Для '
                            'занятого взрослого человека лучше регулярные короткие сессии, чем редкие '
                            'марафоны.</p>',
                            '<p>Оптимальный вариант:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Активность</th><th>Частота</th></tr></thead><tbody><tr><td>Живой '
                            'онлайн-урок</td><td>1–2 раза в неделю</td></tr><tr><td>Самостоятельная '
                            'практика</td><td>3 раза в неделю по 15–30 '
                            'минут</td></tr><tr><td>Повторение слов</td><td>5–10 минут в '
                            'день</td></tr><tr><td>Практика вслух</td><td>3–4 раза в '
                            'неделю</td></tr><tr><td>Ролевая ситуация</td><td>1 раз в '
                            'неделю</td></tr><tr><td>Повторение и мини-тест</td><td>1 раз в '
                            'неделю</td></tr></tbody></table>',
                            '<p>Главное — не просто “учить”, а использовать. Если вы выучили 10 слов, '
                            'превратите их в 10 фраз. Если вы выучили 5 вопросов, задайте их вслух. '
                            'Если вы прошли тему “отель”, разыграйте регистрацию на ресепшене.</p>']},
                  {'heading': 'Почему живые уроки важны для бразильского португальского?',
                   'body': ['<p>Живые уроки важны, потому что язык — это не только знание, но и '
                            'реакция. В Бразилии вам нужно будет слушать, отвечать, уточнять, просить '
                            'повторить, менять фразу и понимать культурный тон.</p>',
                            '<p>Приложения и видео могут помочь с лексикой, но у них есть ограничения. '
                            'Они не исправляют вашу интонацию в реальном разговоре. Они не слышат, где '
                            'вы произносите звук неестественно. Они не моделируют живую ситуацию с '
                            'неожиданным ответом.</p>',
                            '<p>На живом уроке вы можете:</p>',
                            '<ul><li>тренировать произношение;</li><li>разыгрывать аэропорт, отель, '
                            'аптеку, работу и учебу;</li><li>получать исправления '
                            'сразу;</li><li>задавать вопросы о культуре;</li><li>учиться звучать '
                            'естественнее;</li><li>укреплять уверенность;</li><li>отслеживать '
                            'прогресс.</li></ul>',
                            '<p>Vedium предлагает живые онлайн-уроки бразильского португальского для '
                            'иностранцев. Это формат для тех, кому нужен практический язык, культурная '
                            'адаптация и понятный путь обучения без долгих контрактных обязательств. '
                            'Вы продолжаете не потому, что привязаны договором, а потому, что '
                            'чувствуете результат.</p>']},
                  {'heading': 'Ключевая лексика на первые 90 дней',
                   'body': ['<p>Вот базовый список слов, который стоит освоить за первые три '
                            'месяца:</p>',
                            '<table '
                            'class="vd-table"><thead><tr><th>Португальский</th><th>Русский</th></tr></thead><tbody><tr><td>ajuda</td><td>помощь</td></tr><tr><td>banheiro</td><td>туалет</td></tr><tr><td>endereço</td><td>адрес</td></tr><tr><td>dinheiro</td><td>наличные</td></tr><tr><td>cartão</td><td>карта</td></tr><tr><td>mercado</td><td>магазин</td></tr><tr><td>farmácia</td><td>аптека</td></tr><tr><td>restaurante</td><td>ресторан</td></tr><tr><td>trabalho</td><td>работа</td></tr><tr><td>reunião</td><td>встреча</td></tr><tr><td>prazo</td><td>срок</td></tr><tr><td>aula</td><td>урок</td></tr><tr><td>professor</td><td>преподаватель</td></tr><tr><td>consulta</td><td>прием '
                            'у '
                            'врача</td></tr><tr><td>remédio</td><td>лекарство</td></tr><tr><td>entrega</td><td>доставка '
                            '/ '
                            'посылка</td></tr><tr><td>apartamento</td><td>квартира</td></tr><tr><td>internet</td><td>интернет</td></tr><tr><td>chave</td><td>ключ</td></tr><tr><td>problema</td><td>проблема</td></tr><tr><td>hoje</td><td>сегодня</td></tr><tr><td>amanhã</td><td>завтра</td></tr><tr><td>ontem</td><td>вчера</td></tr><tr><td>agora</td><td>сейчас</td></tr><tr><td>depois</td><td>потом</td></tr></tbody></table>',
                            '<p>Но список сам по себе не решает задачу. Для каждого слова создайте '
                            'фразу:</p>',
                            '<ul><li>“Preciso de ajuda.”</li><li>“Onde fica o banheiro?”</li><li>“Qual '
                            'é o endereço?”</li><li>“Aceita cartão?”</li><li>“Tenho uma reunião '
                            'amanhã.”</li><li>“A internet não está funcionando.”</li><li>“Preciso '
                            'marcar uma consulta.”</li></ul>',
                            '<p>Так словарь превращается в реальное общение.</p>']},
                  {'heading': 'Как понять, что план работает?',
                   'body': ['<p>План работает, если через 90 дней вы не просто “знаете больше слов”, а '
                            'можете выполнять конкретные действия на португальском.</p>',
                            '<p>Признаки прогресса:</p>',
                            '<ul><li>вы быстрее понимаете приветствия;</li><li>вы можете попросить '
                            'повторить без паники;</li><li>вы задаете базовые вопросы;</li><li>вы '
                            'знаете фразы для кафе, транспорта, аптеки и жилья;</li><li>вы можете '
                            'представиться;</li><li>вы можете объяснить простую проблему;</li><li>вы '
                            'понимаете часть естественных бразильских выражений;</li><li>вы готовы '
                            'говорить, даже если ошибаетесь.</li></ul>',
                            '<p>Именно это нужно на начальном этапе. Не идеальная грамматика, а '
                            'способность действовать.</p>']},
                  {'heading': 'Заключение с сильным CTA',
                   'body': ['<p>Реалистичный план изучения бразильского португальского на 90 дней не '
                            'обещает мгновенную беглость. Он дает более ценное: понятный старт, '
                            'практическую базу и уверенность для первых реальных ситуаций в Бразилии. '
                            'За три месяца можно научиться приветствовать, представляться, задавать '
                            'вопросы, решать бытовые задачи, говорить о работе и учебе, объяснять '
                            'простые проблемы и понимать культурный контекст общения.</p>',
                            '<p>Если вы собираетесь жить, работать или учиться в Бразилии, не ждите '
                            '“идеального момента”. Начните с реальных ситуаций и живой практики. '
                            'Бразильский португальский становится полезным тогда, когда вы используете '
                            'его с людьми.</p>',
                            '<p>Vedium предлагает живые онлайн-уроки бразильского португальского для '
                            'иностранцев, экспатов, студентов и специалистов. Занятия строятся вокруг '
                            'реальной жизни, ключевой лексики, культуры и разговорной практики. Без '
                            'долгой привязки контрактом: вы продолжаете, потому что видите '
                            'прогресс.</p>',
                            '<p>Запишитесь на бесплатную проверку уровня на <a '
                            'href="/ru/portugalskiy-dlya-inostrantsev">https://vediums.com/</a> и '
                            'начните свой 90-дневный путь к уверенному португальскому для '
                            'Бразилии.</p>']}],
     'faqs': [{'q': 'Можно ли выучить бразильский португальский за 90 дней?',
               'a': 'За 90 дней нельзя гарантировать свободное владение, но можно создать сильную '
                    'базу: приветствия, простые вопросы, бытовые ситуации, работа, учеба, аптека, '
                    'жилье и первые диалоги.'},
              {'q': 'Чем бразильский португальский отличается от европейского?',
               'a': 'Бразильский португальский отличается произношением, лексикой, интонацией, '
                    'разговорными выражениями и культурой общения. Если вы едете в Бразилию, лучше '
                    'учить именно вариант Portuguese for Brazil.'},
              {'q': 'С чего начать изучение португальского для жизни в Бразилии?',
               'a': 'Начните с приветствий, просьбы повторить, базовых вопросов, чисел, времени, '
                    'адресов, транспорта, еды, жилья, аптеки и рабочих или учебных ситуаций.'},
              {'q': 'Нужны ли живые уроки, если я занимаюсь по приложению?',
               'a': 'Приложения полезны для повторения слов, но живые уроки нужны для произношения, '
                    'разговорной реакции, исправления ошибок и практики реальных ситуаций в Бразилии.'},
              {'q': 'Есть ли у Vedium курс бразильского португальского для иностранцев?',
               'a': 'Да. Vedium предлагает живые онлайн-уроки бразильского португальского для '
                    'иностранцев, экспатов, студентов и специалистов, с фокусом на практическую '
                    'коммуникацию и культурную адаптацию.'}],
     'cta_title': 'Готовы начать изучать бразильский португальский?',
     'cta_text': 'Запишитесь на бесплатную проверку уровня и начните с понятного плана.',
     'cta_label': 'Записаться на бесплатную проверку уровня',
     'cta_url': '/ru/portugalskiy-dlya-inostrantsev'},
}



def _post_url(slug, post):
    """URL do post: nova estrutura por categoria (/blog/<cat>/<slug> ou
    /<lang>/blog/<cat>/<slug>) se o post declarar "category"; senão, a URL
    plana antiga (/blog/<slug>) — usada pelos 8 posts publicados antes da
    reestruturação de URL de 2026-07-14, que NÃO mudam de endereço."""
    category = post.get("category")
    if not category:
        return f"/blog/{slug}"
    lang = post.get("lang") or "pt-BR"
    prefix = "" if lang in ("pt-BR", "pt") else f"/{lang}"
    return f"{prefix}/blog/{category}/{slug}"


def _post_card(slug, post):
    return {
        "slug": slug,
        "url": _post_url(slug, post),
        "title": post["title"],
        "meta_description": post["meta_description"],
        "date": str(post.get("date", "")),
        "date_display": post.get("date_display", ""),
        "tag": post.get("tag", "Vedium"),
        "hero_image": post.get("hero_image", ""),
        "category": post.get("category"),
        "lang": post.get("lang", "pt-BR"),
    }


def _db_post_card(row):
    return {
        "slug": row.slug,
        "url": f"/blog/{row.slug}",
        "title": row.title,
        "meta_description": row.meta_description or "",
        "date": str(row.date or ""),
        "date_display": "",
        "tag": row.tag or "Vedium",
        "hero_image": row.hero_image or "",
        "lang": row.lang or "pt-BR",
    }


def list_db_blog_posts():
    """Posts publicados via painel (doctype Vedium Blog Post, sem código/deploy)."""
    import frappe

    rows = frappe.get_all(
        "Vedium Blog Post",
        filters={"published": 1},
        fields=["name as slug", "title", "meta_description", "tag", "date", "hero_image", "lang"],
        ignore_permissions=True,
    )
    return [_db_post_card(row) for row in rows]


def list_blog_posts():
    """Lista combinada (posts do painel + posts de código), mais recente primeiro."""
    cards = [_post_card(slug, post) for slug, post in BLOG_POSTS.items()]
    cards += list_db_blog_posts()
    cards.sort(key=lambda c: c["date"], reverse=True)
    return cards


def get_blog_post(slug):
    post = dict(BLOG_POSTS[slug])
    post["slug"] = slug
    post["url"] = f"{BASE_URL}/blog/{slug}"
    return post


def get_blog_post_from_db(slug):
    """Post publicado via painel do Frappe (/app/vedium-blog-post). None se não existir/publicado."""
    import frappe

    doc = frappe.db.get_value(
        "Vedium Blog Post",
        {"slug": slug, "published": 1},
        [
            "title", "meta_description", "tag", "date", "hero_image", "hero_alt",
            "lead", "content", "cta_title", "cta_text", "cta_label", "cta_url", "lang",
        ],
        as_dict=True,
    )
    if not doc:
        return None
    faqs = frappe.get_all(
        "Vedium Blog FAQ",
        filters={"parenttype": "Vedium Blog Post", "parent": slug},
        fields=["question as q", "answer as a"],
        order_by="idx asc",
        ignore_permissions=True,
    )
    return {
        "slug": slug,
        "url": f"{BASE_URL}/blog/{slug}",
        "title": doc.title,
        "h1": doc.title,
        "meta_description": doc.meta_description or "",
        "tag": doc.tag or "Vedium",
        "date": str(doc.date or ""),
        "date_display": str(doc.date or ""),
        "hero_image": doc.hero_image or "",
        "hero_alt": doc.hero_alt or "",
        "lead": doc.lead or "",
        "lang": doc.lang or "pt-BR",
        # content é HTML de um Text Editor (rich text) — uma seção única sem
        # heading (o template pula o <h2> quando heading está vazio).
        "sections": [{"heading": "", "body": [doc.content or ""]}],
        "faqs": faqs,
        "cta_title": doc.cta_title or "",
        "cta_text": doc.cta_text or "",
        "cta_label": doc.cta_label or "",
        "cta_url": doc.cta_url or "",
    }


def get_blog_post_any(slug):
    """Procura o post primeiro no painel (banco), depois no dict de código."""
    post = get_blog_post_from_db(slug)
    if post:
        return post
    if slug in BLOG_POSTS:
        return get_blog_post(slug)
    return None


def apply_blog_context(context, slug):
    post = get_blog_post(slug)
    context.title = post["title"]
    context.description = post["meta_description"]
    context.post = post


POSTS_PER_PAGE = 12


def get_blog_categories(lang=None):
    """Categorias (tag) distintas entre os posts, para o filtro do /blog
    (ou /<lang>/blog, quando lang é passado)."""
    posts = list_blog_posts()
    if lang:
        posts = [p for p in posts if p.get("lang") == lang]
    return sorted({c["tag"] for c in posts if c.get("tag")})


def get_adjacent_posts(slug):
    """(anterior, próximo) na lista combinada ordenada por data (mais recente
    primeiro) — "anterior" é o post mais recente que este, "próximo" o mais
    antigo, espelhando a ordem em que aparecem no índice /blog."""
    posts = list_blog_posts()
    idx = next((i for i, p in enumerate(posts) if p["slug"] == slug), None)
    if idx is None:
        return None, None
    newer = posts[idx - 1] if idx > 0 else None
    older = posts[idx + 1] if idx + 1 < len(posts) else None
    return newer, older


# =============================================================================
# Páginas de categoria do blog (2026-07-14) — cada frente do calendário
# editorial (Cliente/Vedium/Artigos/vedium_calendario_editorial_seo_geo_318_posts.xlsx)
# ganha uma página própria, ao mesmo tempo categoria (lista os posts daquele
# tema) e página editorial (H1, introdução, blocos temáticos, FAQ e CTA) —
# não uma lista automática pura. Chave = (lang, slug da categoria); lang "pt"
# pras 4 frentes brasileiras (URL sem prefixo: /blog/<slug>), "en"/"es" pro
# PLE internacional (URL com prefixo: /<lang>/blog/<slug>).
#
# "legacy_tag" é o valor de "tag" usado pelos posts publicados ANTES desta
# reestruturação (ver BLOG_POSTS acima) — permite listar esses posts na
# categoria certa sem mexer na URL deles (só ganham "category"/nested URL
# os posts NOVOS, publicados depois de 2026-07-14).
RESERVED_CATEGORY_SLUGS = {"ingles", "ioruba", "hebraico", "espanhol"}

PLE_CATEGORY_BY_LANG = {
    "en": "brazilian-portuguese",
    "es": "portugues-brasileno",
}

CATEGORY_PAGES = {
    ("pt", "ingles"): {
        "h1": "Inglês para carreira, viagens e conversas reais",
        "meta_description": "Conteúdos para quem deseja aprender inglês com clareza, entender como o idioma funciona e evoluir nível a nível.",
        "intro": "Conteúdos para quem deseja aprender inglês com clareza, entender como o idioma funciona e evoluir nível a nível — carreira, entrevistas, viagens e conversação real, sem enrolação.",
        "blocks": [
            {"title": "Comece por aqui", "text": "Descubra seu nível real e o caminho recomendado antes de escolher um curso."},
            {"title": "Inglês para carreira", "text": "Entrevistas, e-mails corporativos, reuniões e vocabulário para o mercado de trabalho."},
            {"title": "Conversação", "text": "Como treinar speaking de verdade, sem depender só de aplicativo ou gramática decorada."},
            {"title": "Pronúncia", "text": "Sons que não existem em português, ritmo da fala e os erros mais comuns de brasileiros."},
            {"title": "Gramática", "text": "Os pontos que mais confundem — tempos verbais, preposições e uso natural do idioma."},
            {"title": "Viagens", "text": "Frases e situações práticas para se virar bem em qualquer país de língua inglesa."},
        ],
        "faqs": [
            {"q": "Preciso saber gramática antes de começar a falar inglês?", "a": "Não. Na Vedium, o foco é começar a falar desde a primeira aula, com a gramática entrando naturalmente como suporte — não como pré-requisito."},
            {"q": "Quanto tempo leva para ficar fluente em inglês?", "a": "Depende do nível inicial e da frequência de prática, mas aulas ao vivo regulares costumam mostrar evolução perceptível em poucos meses."},
        ],
        "cta_title": "Quer saber seu nível real de inglês?",
        "cta_text": "Faça o teste de nível gratuito da Vedium e descubra por onde começar.",
        "cta_label": "Fazer teste de nível",
        "cta_url": "/teste-de-nivel-ingles",
        "course_url": "/curso-de-ingles-online",
        "course_label": "Conhecer o curso de Inglês",
        "legacy_tag": None,
    },
    ("pt", "ioruba"): {
        "h1": "Iorubá: idioma, cultura e ancestralidade com respeito",
        "meta_description": "Guias sobre o idioma iorubá — alfabeto, tons, saudações, números e cultura — pensados para quem está começando do zero.",
        "intro": "O iorubá é uma língua tonal riquíssima, com forte presença na cultura e na história brasileiras. Aqui você encontra guias práticos sobre pronúncia, vocabulário e cultura, sempre com respeito à ancestralidade do idioma.",
        "blocks": [
            {"title": "Comece por aqui", "text": "O que é o idioma iorubá e por que ele carrega cultura e memória."},
            {"title": "Alfabeto e pronúncia", "text": "As 25 letras, as vogais e os três tons que mudam o significado das palavras."},
            {"title": "Saudações e vocabulário", "text": "Como cumprimentar com respeito e o vocabulário do dia a dia."},
            {"title": "Cultura e ancestralidade", "text": "A relação do iorubá com a diáspora e as tradições afro-brasileiras."},
            {"title": "Números e estrutura", "text": "Como contar em iorubá e a lógica vigesimal (base 20) do idioma."},
        ],
        "faqs": [
            {"q": "Preciso ter alguma religião para aprender iorubá?", "a": "Não. O curso da Vedium ensina o idioma e a cultura de forma aberta e respeitosa, sem exigir nenhuma prática religiosa."},
            {"q": "O iorubá é difícil para quem fala português?", "a": "O maior desafio é o sistema de tons, mas com aulas ao vivo e correção em tempo real a pronúncia é totalmente aprendível desde o início."},
        ],
        "cta_title": "Quer aprender iorubá com pronúncia correta desde o início?",
        "cta_text": "Aulas ao vivo, do zero ao avançado, com foco em tons e conversação real.",
        "cta_label": "Conhecer o curso de Iorubá",
        "cta_url": "/curso-de-ioruba-online",
        "course_url": "/curso-de-ioruba-online",
        "course_label": "Conhecer o curso de Iorubá",
        "legacy_tag": "Iorubá",
    },
    ("pt", "hebraico"): {
        "h1": "Hebraico bíblico e moderno: como aprender com clareza",
        "meta_description": "Guias sobre o alfabeto, a leitura e as diferenças entre o hebraico bíblico e o moderno, para quem está começando.",
        "intro": "Para quem quer ler a Bíblia no original ou se comunicar em hebraico moderno, o primeiro passo é entender o alfabeto e as diferenças entre os dois registros do idioma. Os conteúdos aqui organizam esse caminho.",
        "blocks": [
            {"title": "Comece por aqui", "text": "Como começar a ler hebraico e por onde seguir depois do alfabeto."},
            {"title": "Alfabeto hebraico", "text": "As letras, os sinais de vogal (nikkud) e a leitura da direita para a esquerda."},
            {"title": "Hebraico bíblico", "text": "Vocabulário e estrutura para ler o Antigo Testamento no original."},
            {"title": "Hebraico moderno", "text": "O idioma falado hoje em Israel, no dia a dia e na conversação."},
            {"title": "Pronúncia e leitura", "text": "Sons próprios do hebraico e como treinar a leitura com confiança."},
        ],
        "faqs": [
            {"q": "Hebraico bíblico e hebraico moderno são o mesmo idioma?", "a": "Compartilham o alfabeto e boa parte da raiz, mas têm diferenças de vocabulário, gramática e uso — vale entender qual dos dois você quer aprender antes de começar."},
            {"q": "Preciso já saber ler hebraico para começar o curso?", "a": "Não. O curso da Vedium começa pelo alfabeto e pela leitura, do zero."},
        ],
        "cta_title": "Quer aprender a ler e entender hebraico desde o início?",
        "cta_text": "Aulas ao vivo com professor especializado, do alfabeto à leitura fluente.",
        "cta_label": "Conhecer o curso de Hebraico",
        "cta_url": "/curso-de-hebraico-online",
        "course_url": "/curso-de-hebraico-online",
        "course_label": "Conhecer o curso de Hebraico",
        "legacy_tag": None,
    },
    ("pt", "espanhol"): {
        "h1": "Espanhol para viagens, trabalho e o dia a dia",
        "meta_description": "Guias práticos de espanhol — falsos cognatos, gramática essencial e espanhol para viagem — para brasileiros aprendendo o idioma.",
        "intro": "O espanhol parece fácil pra quem fala português, mas é justamente essa proximidade que esconde as maiores armadilhas — os falsos cognatos, a pronúncia e as diferenças regionais. Os conteúdos aqui ajudam a aprender com precisão, não só por semelhança.",
        "blocks": [
            {"title": "Comece por aqui", "text": "Os primeiros passos e as armadilhas mais comuns de quem já fala português."},
            {"title": "Falsos cognatos", "text": "Palavras parecidas com o português que têm significados bem diferentes."},
            {"title": "Espanhol para viagem", "text": "Frases e vocabulário essenciais para se comunicar em qualquer país hispanofalante."},
            {"title": "Gramática essencial", "text": "Ser x estar, os tempos verbais e outros pontos que mais confundem brasileiros."},
            {"title": "Diferenças regionais", "text": "Como o espanhol muda entre Espanha e a América Latina."},
        ],
        "faqs": [
            {"q": "Falar português ajuda a aprender espanhol mais rápido?", "a": "Ajuda na compreensão, mas também cria vícios — os falsos cognatos e a pronúncia exigem atenção específica, que o curso trabalha desde o início."},
            {"q": "O curso ensina o espanhol da Espanha ou da América Latina?", "a": "O professor mostra as principais diferenças regionais, para você reconhecer variações e se comunicar bem em qualquer país hispanofalante."},
        ],
        "cta_title": "Quer aprender espanhol sem cair nas armadilhas do português?",
        "cta_text": "Aulas ao vivo com foco em pronúncia, gramática essencial e conversação real.",
        "cta_label": "Conhecer o curso de Espanhol",
        "cta_url": "/curso-de-espanhol-online",
        "course_url": "/curso-de-espanhol-online",
        "course_label": "Conhecer o curso de Espanhol",
        "legacy_tag": None,
    },
    ("en", "brazilian-portuguese"): {
        "h1": "Brazilian Portuguese for people who actually need it",
        "meta_description": "Practical guides to Brazilian Portuguese for expats, relocation and everyday life in Brazil — real situations, not just grammar.",
        "intro": "Whether you're relocating to Brazil, working with a Brazilian team, or just visiting, these guides focus on the Portuguese you'll actually use — real-life situations, essential vocabulary and honest advice from Vedium's teachers.",
        "blocks": [
            {"title": "Start here", "text": "What to learn before your first month in Brazil."},
            {"title": "Living in Brazil", "text": "Everyday bureaucracy, housing and getting around."},
            {"title": "Portuguese for work", "text": "Vocabulary and etiquette for relocation teams and professionals."},
            {"title": "Everyday conversations", "text": "How to greet people, ask questions and sound natural, not textbook-formal."},
            {"title": "Pronunciation", "text": "The sounds that trip up English speakers and how to train them."},
        ],
        "faqs": [
            {"q": "Do I need to already speak Spanish or another Romance language to learn Portuguese?", "a": "No. Vedium's live classes start from zero, with a teacher guiding pronunciation and structure from day one."},
            {"q": "Is Brazilian Portuguese very different from European Portuguese?", "a": "Yes — pronunciation, some vocabulary and everyday expressions differ. These guides focus specifically on the Brazilian variant."},
        ],
        "cta_title": "Want to know your real Portuguese level?",
        "cta_text": "Take Vedium's free placement test and find out where to start.",
        "cta_label": "Take the placement test",
        "cta_url": "/en/portuguese-placement-test",
        "course_url": "/en/learn-portuguese-brazil",
        "course_label": "Learn about the Portuguese course",
        "legacy_tag": None,
    },
    ("es", "portugues-brasileno"): {
        "h1": "Português brasileño para quienes lo necesitan de verdad",
        "meta_description": "Guías prácticas de portugués brasileño para expatriados y vida diaria en Brasil — situaciones reales, no solo gramática.",
        "intro": "Si te mudas a Brasil, trabajas con un equipo brasileño o simplemente estás de viaje, estas guías se enfocan en el portugués que realmente vas a usar — situaciones reales, vocabulario esencial y consejos honestos de los profesores de Vedium.",
        "blocks": [
            {"title": "Empieza por aquí", "text": "Qué aprender antes de tu primer mes en Brasil."},
            {"title": "Vivir en Brasil", "text": "Trámites del día a día, vivienda y cómo moverte por la ciudad."},
            {"title": "Portugués para el trabajo", "text": "Vocabulario y etiqueta para equipos de reubicación y profesionales."},
            {"title": "Conversaciones cotidianas", "text": "Cómo saludar, preguntar y sonar natural, no como en un libro de texto."},
            {"title": "Pronunciación", "text": "Los sonidos que más confunden a hispanohablantes y cómo entrenarlos."},
        ],
        "faqs": [
            {"q": "¿El portugués brasileño es muy diferente del español?", "a": "Se parecen en varias estructuras, pero la pronunciación y muchos falsos cognatos exigen atención específica desde el principio."},
            {"q": "¿Necesito conocimientos previos de portugués para empezar?", "a": "No. Las clases en vivo de Vedium empiezan desde cero, con un profesor guiando la pronunciación y la estructura desde el primer día."},
        ],
        "cta_title": "¿Quieres saber tu nivel real de portugués?",
        "cta_text": "Haz la prueba de nivel gratuita de Vedium y descubre por dónde empezar.",
        "cta_label": "Hacer la prueba de nivel",
        "cta_url": "/es/prueba-de-nivel-de-portugues",
        "course_url": "/es/portugues-para-extranjeros",
        "course_label": "Conocer el curso de portugués",
        "legacy_tag": None,
    },
}


def _post_matches_category(card, lang, category, legacy_tag):
    want_lang = lang or "pt-BR"
    if card.get("category") == category and (card.get("lang") or "pt-BR") == want_lang:
        return True
    if legacy_tag and want_lang == "pt-BR" and card.get("tag") == legacy_tag:
        return True
    return False


def get_category_context(context, category, lang=None):
    """Contexto da página de categoria/pilar (ver CATEGORY_PAGES acima).
    `lang` é None para as 4 categorias PT (URL sem prefixo) ou "en"/"es"
    para as categorias PLE (URL com prefixo /<lang>/blog/<category>)."""
    import frappe

    key = (lang or "pt", category)
    page = CATEGORY_PAGES.get(key)
    if not page:
        frappe.local.flags.redirect_location = f"/{lang}/blog" if lang else "/blog"
        raise frappe.Redirect

    posts = [
        card for card in list_blog_posts()
        if _post_matches_category(card, lang, category, page.get("legacy_tag"))
    ]

    context.is_category = True
    context.category = page
    context.category_posts = posts
    context.category_lang = lang or "pt-BR"
    context.category_slug = category
    context.title = f"{page['h1']} | Vedium"
    context.description = page["meta_description"]
    return context


BLOG_INDEX_COPY = {
    None: {
        "title": "Blog da Vedium — idiomas, cultura e aprendizado",
        "description": (
            "Conteúdos gratuitos sobre inglês, iorubá e português para estrangeiros: "
            "guias práticos, níveis, pronúncia e cultura, escritos pela equipe da Vedium."
        ),
        "search_placeholder": "Pesquisar artigos...",
    },
    "en": {
        "title": "Vedium Blog — Brazilian Portuguese for expats and relocation",
        "description": (
            "Free guides on Brazilian Portuguese for expats, relocation and everyday life "
            "in Brazil, written by Vedium's teaching team."
        ),
        "search_placeholder": "Search articles...",
    },
    "es": {
        "title": "Blog de Vedium — Portugués brasileño para expatriados",
        "description": (
            "Guías gratuitas de portugués brasileño para expatriados y vida diaria en "
            "Brasil, escritas por el equipo de profesores de Vedium."
        ),
        "search_placeholder": "Buscar artículos...",
    },
}


def get_blog_index_context(context, lang=None):
    import frappe

    page = frappe.utils.cint(frappe.form_dict.get("page") or 1) or 1
    category = (frappe.form_dict.get("category") or "").strip()
    query = (frappe.form_dict.get("q") or "").strip()

    posts = list_blog_posts()
    if lang:
        posts = [p for p in posts if p.get("lang") == lang]
    if category:
        posts = [p for p in posts if p.get("tag") == category]
    if query:
        needle = query.lower()
        posts = [
            p for p in posts
            if needle in p["title"].lower() or needle in p["meta_description"].lower()
        ]

    total = len(posts)
    total_pages = max(1, (total + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE)
    page = min(max(page, 1), total_pages)
    start = (page - 1) * POSTS_PER_PAGE
    page_posts = posts[start:start + POSTS_PER_PAGE]

    copy = BLOG_INDEX_COPY.get(lang, BLOG_INDEX_COPY[None])
    context.title = copy["title"]
    context.description = copy["description"]
    context.search_placeholder = copy["search_placeholder"]
    context.blog_lang = lang
    context.posts = page_posts
    context.categories = get_blog_categories(lang)
    context.selected_category = category
    context.search_query = query
    context.page = page
    context.total_pages = total_pages
    context.total_posts = total
    context.has_prev = page > 1
    context.has_next = page < total_pages
    context.is_filtered = bool(category or query)
