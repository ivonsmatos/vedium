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
    "niveis-de-ingles-a1-c1": {
        "title": "Níveis de inglês: do A1 ao C1, por onde começar",
        "meta_description": "O que significam os níveis A1, A2, B1, B2 e C1 do inglês (CEFR) e como descobrir em qual deles você está antes de começar as aulas na Vedium.",
        "h1": "Níveis de inglês: do A1 ao C1, por onde começar",
        "date": "2026-06-02",
        "date_display": "2 de junho de 2026",
        "hero_image": "https://images.unsplash.com/photo-1527689368864-3a821dbccc34?w=1100&h=560&fit=crop&q=80",
        "hero_alt": "Estudante avançando nos níveis de inglês na Vedium",
        "tag": "Inglês",
        "lead": "Os níveis de inglês seguem o Quadro Europeu Comum de Referência (CEFR), um padrão internacional que vai do A1 (iniciante) ao C1/C2 (avançado). Conhecer esses níveis ajuda você a entender onde está e até onde quer chegar.",
        "sections": [
            {
                "heading": "O que significa cada nível",
                "body": [
                    "<ul>"
                    "<li><strong>A1 — Iniciante:</strong> entende e usa frases simples do dia a dia.</li>"
                    "<li><strong>A2 — Básico:</strong> conversas curtas sobre assuntos familiares.</li>"
                    "<li><strong>B1 — Intermediário:</strong> se vira em viagens e situações comuns.</li>"
                    "<li><strong>B2 — Intermediário superior:</strong> conversa com fluência sobre vários temas.</li>"
                    "<li><strong>C1 — Avançado:</strong> usa o inglês com naturalidade no trabalho e nos estudos.</li>"
                    "</ul>",
                ],
            },
            {
                "heading": "Como saber o meu nível",
                "body": [
                    "<p>Não é preciso adivinhar. Na Vedium, antes de começar, ajudamos você a identificar o seu nível para entrar na turma certa — nem fácil demais, nem difícil demais. Assim o seu tempo rende e a evolução é mais rápida.</p>",
                ],
            },
            {
                "heading": "Por onde começar",
                "body": [
                    "<p>Se você nunca estudou inglês, começa no A1. Se já tem alguma base, pode entrar em um nível mais adiantado. O programa da Vedium cobre toda a jornada, do A1 ao C1, com aulas ao vivo e professor dedicado.</p>",
                ],
            },
        ],
        "faqs": [],
        "cta_title": "Pronto para descobrir seu nível?",
        "cta_text": "Faça o teste gratuito e comece no nível certo, sem perder tempo.",
        "cta_label": "Ver os níveis de inglês",
        "cta_url": "/catalogo",
    },
    "como-funcionam-as-aulas-ao-vivo": {
        "title": "Como funcionam as aulas ao vivo na Vedium",
        "meta_description": "Aulas em tempo real, turmas pequenas e professor de verdade: veja como é estudar Inglês e Iorubá online na Vedium.",
        "h1": "Como funcionam as aulas ao vivo na Vedium",
        "date": "2026-06-02",
        "date_display": "2 de junho de 2026",
        "hero_image": "https://images.unsplash.com/photo-1491438590914-bc09fcaaf77a?w=1100&h=560&fit=crop&q=80",
        "hero_alt": "Aluno em aula ao vivo de idiomas na Vedium",
        "tag": "Vedium",
        "lead": "Na Vedium, você não assiste a vídeos gravados: estuda em aulas ao vivo, em tempo real, com um professor que conduz a aula, tira dúvidas na hora e adapta o ritmo à turma. É o jeito mais próximo de uma sala de aula presencial — só que de onde você estiver.",
        "sections": [
            {
                "heading": "Como é uma aula",
                "body": [
                    "<p>Cada aula tem 1 hora de duração e acontece em uma chamada de vídeo. As turmas são pequenas, o que garante que todos falem, pratiquem e recebam correção. O foco é a <strong>conversação</strong>: você usa o idioma desde o primeiro dia, com apoio de materiais e exercícios.</p>",
                ],
            },
            {
                "heading": "O que você precisa",
                "body": [
                    "<ul>"
                    "<li>Um computador ou celular com câmera e microfone;</li>"
                    "<li>Conexão estável com a internet;</li>"
                    "<li>Vontade de praticar — o resto a gente conduz.</li>"
                    "</ul>",
                ],
            },
            {
                "heading": "Quais idiomas e níveis",
                "body": [
                    "<p>Você pode estudar <strong>Inglês</strong>, do básico (A1) ao avançado (C1), ou <strong>Iorubá</strong>, do básico ao avançado. Escolhe a frequência (de 1 a 4 aulas por semana) de acordo com a sua rotina e o seu objetivo. Ao concluir, você recebe um <strong>certificado</strong>.</p>",
                ],
            },
        ],
        "faqs": [],
        "cta_title": "Quer experimentar uma aula ao vivo?",
        "cta_text": "Veja os cursos disponíveis e escolha o idioma e o nível certos para você.",
        "cta_label": "Ver os cursos",
        "cta_url": "/catalogo",
    },
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
}


def _post_card(slug, post):
    return {
        "slug": slug,
        "url": f"/blog/{slug}",
        "title": post["title"],
        "meta_description": post["meta_description"],
        "date": str(post.get("date", "")),
        "date_display": post.get("date_display", ""),
        "tag": post.get("tag", "Vedium"),
        "hero_image": post.get("hero_image", ""),
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
    }


def list_db_blog_posts():
    """Posts publicados via painel (doctype Vedium Blog Post, sem código/deploy)."""
    import frappe

    rows = frappe.get_all(
        "Vedium Blog Post",
        filters={"published": 1},
        fields=["name as slug", "title", "meta_description", "tag", "date", "hero_image"],
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
            "lead", "content", "cta_title", "cta_text", "cta_label", "cta_url",
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


def get_blog_index_context(context):
    context.title = "Blog da Vedium — idiomas, cultura e aprendizado"
    context.description = (
        "Conteúdos gratuitos sobre inglês, iorubá e português para estrangeiros: "
        "guias práticos, níveis, pronúncia e cultura, escritos pela equipe da Vedium."
    )
    context.posts = list_blog_posts()
