"""Conteúdo do blog da Vedium — posts ricos (SEO/GEO) renderizados pelo
template compartilhado templates/includes/blog_post.html.

Cada post fica em www/blog/<slug>.html (2 linhas, chama get_blog_post) +
www/blog/<slug>.py (apply_blog_context). O índice em www/blog.html lista
BLOG_INDEX (posts deste dict + posts legados standalone).

Convenção de conteúdo: corpo em HTML controlado por nós (parágrafos,
listas e tabelas), com no mínimo ~900 palavras por post, headings H2 e
um bloco de FAQs para rich snippet.
"""

BASE_URL = "https://vediums.com"
WHATSAPP_PHONE = "5511911293075"


BLOG_POSTS = {
    "alfabeto-ioruba": {
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
}


# Posts legados (HTML standalone) que ainda não migraram para o dict, mas
# devem aparecer no índice /blog.
LEGACY_POSTS = [
    {
        "slug": "niveis-de-ingles-a1-c1",
        "title": "Níveis de inglês: do A1 ao C1, por onde começar",
        "meta_description": "Entenda o que significam os níveis A1, A2, B1, B2 e C1 e descubra em qual deles você está antes de começar.",
        "date": "2026-06-02",
        "tag": "Inglês",
    },
    {
        "slug": "como-funcionam-as-aulas-ao-vivo",
        "title": "Como funcionam as aulas ao vivo na Vedium",
        "meta_description": "Aulas em tempo real, turmas pequenas e professor de verdade: veja como é estudar Inglês e Iorubá online na Vedium.",
        "date": "2026-06-02",
        "tag": "Vedium",
    },
    {
        "slug": "aprender-ioruba-lingua-e-cultura",
        "title": "Iorubá: conheça o idioma e por que aprendê-lo",
        "meta_description": "O iorubá é falado por milhões na África Ocidental e tem forte presença na cultura brasileira. Conheça o idioma.",
        "date": "2026-06-02",
        "tag": "Iorubá",
    },
]


def _post_card(slug, post):
    return {
        "slug": slug,
        "url": f"/blog/{slug}",
        "title": post["title"],
        "meta_description": post["meta_description"],
        "date": post.get("date", ""),
        "date_display": post.get("date_display", ""),
        "tag": post.get("tag", "Vedium"),
        "hero_image": post.get("hero_image", ""),
    }


def list_blog_posts():
    """Lista combinada (dict + legados), mais recente primeiro, para o índice."""
    cards = [_post_card(slug, post) for slug, post in BLOG_POSTS.items()]
    cards += [
        {
            "slug": p["slug"],
            "url": f"/blog/{p['slug']}",
            "title": p["title"],
            "meta_description": p["meta_description"],
            "date": p.get("date", ""),
            "date_display": "",
            "tag": p.get("tag", "Vedium"),
            "hero_image": "",
        }
        for p in LEGACY_POSTS
    ]
    cards.sort(key=lambda c: c["date"], reverse=True)
    return cards


def get_blog_post(slug):
    post = dict(BLOG_POSTS[slug])
    post["slug"] = slug
    post["url"] = f"{BASE_URL}/blog/{slug}"
    return post


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
