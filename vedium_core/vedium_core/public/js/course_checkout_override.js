(function() {
    // 1. Redirecionamento forçado do billing interno (legado)
    if (window.location.pathname.includes('/lms/billing/course/')) {
        const courseName = window.location.pathname.split('/').pop();
        window.location.href = `/lms/courses/${courseName}`;
        return;
    }

    // Variáveis de controle
    let purchaseOptions = null;
    let cardModified = false;
    let isFetching = false;

    // A cor de destaque do site
    const highlightColor = "#2E6DA4";

    function getCourseName() {
        return window.location.pathname.split('/').pop();
    }

    async function fetchPurchaseOptions() {
        if (isFetching || purchaseOptions) return;
        isFetching = true;
        
        try {
            const courseName = getCourseName();
            const res = await fetch(`/api/method/vedium_core.api.get_course_purchase_options?course_name=${courseName}`);
            const data = await res.json();
            
            if (data.message && data.message.is_paid && data.message.plans && data.message.plans.length > 0) {
                purchaseOptions = data.message.plans;
                modifyCourseCard();
            }
        } catch (e) {
            console.error("Erro ao buscar opções de compra:", e);
        } finally {
            isFetching = false;
        }
    }

    function createPlanButton(plan) {
        const btn = document.createElement('button');
        // Estilo limpo e moderno, usando flex e cores suaves, com hover
        btn.className = 'w-full mb-3 text-left border rounded-md p-4 transition-all duration-200 hover:shadow-md';
        btn.style.borderColor = "#e2e8f0"; // slate-200
        btn.style.backgroundColor = "#ffffff";
        btn.style.cursor = 'pointer';
        
        btn.onmouseover = () => btn.style.borderColor = highlightColor;
        btn.onmouseout = () => btn.style.borderColor = "#e2e8f0";

        let savingsHtml = '';
        if (plan.savings > 0) {
            savingsHtml = `<div style="color: #10b981; font-size: 0.85rem; font-weight: 600; margin-top: 4px;">Economia de ${plan.currency} ${plan.savings.toFixed(2)} ao ano</div>`;
        }

        btn.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 600; font-size: 1.1rem; color: #1e293b;">${plan.title}</div>
                    ${savingsHtml}
                </div>
                <div style="font-weight: 700; font-size: 1.2rem; color: ${highlightColor};">
                    ${plan.currency} ${plan.amount.toFixed(2)}
                </div>
            </div>
        `;

        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            btn.innerHTML = `<div style="text-align: center; font-size: 0.9rem; font-weight: 600; padding: 0.5rem 0; color: #64748b;">Processando...</div>`;
            btn.style.pointerEvents = "none";
            btn.style.opacity = "0.7";
            
            // Verifica se está logado (Frappe expõe window.frappe.session.user)
            const isGuest = !window.frappe || !window.frappe.session || window.frappe.session.user === "Guest";
            
            if (isGuest) {
                // Salva intenção e vai pro login
                localStorage.setItem("vedium_intent_course", getCourseName());
                localStorage.setItem("vedium_intent_plan", plan.billing_period);
                window.location.href = `/login?redirect-to=${encodeURIComponent(window.location.pathname)}`;
                return;
            }

            try {
                // Post pro checkout
                const resp = await fetch("/api/method/vedium_core.api.create_checkout_session", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-Frappe-CSRF-Token": window.frappe ? window.frappe.csrf_token : ""
                    },
                    body: JSON.stringify({
                        course_name: getCourseName(),
                        billing_period: plan.billing_period
                    })
                });
                
                const data = await resp.json();
                if (data.message && data.message.checkout_url) {
                    window.location.href = data.message.checkout_url;
                } else if (data._server_messages) {
                    const msg = JSON.parse(JSON.parse(data._server_messages)[0]).message;
                    alert(msg);
                    window.location.reload();
                } else {
                    alert("Erro ao gerar checkout");
                    window.location.reload();
                }
            } catch (err) {
                console.error(err);
                alert("Ocorreu um erro de conexão.");
                window.location.reload();
            }
        });

        return btn;
    }

    function modifyCourseCard() {
        if (cardModified || !purchaseOptions) return;
        
        // No DOM do LMS, o card do curso tem essa estrutura principal
        const cardContainer = document.querySelector('.border-2.rounded-md.min-w-80.max-w-sm .p-5');
        if (!cardContainer) return;

        // Procura o botão original que leva para o billing
        const actionLinks = cardContainer.querySelectorAll('a');
        let legacyButtonLink = null;
        for (let link of actionLinks) {
            if (link.getAttribute('href') && (link.getAttribute('href').includes('/billing/') || link.getAttribute('href').includes('buy-this-course'))) {
                legacyButtonLink = link;
                break;
            }
        }
        
        // Outra heurística: procurar texto "Buy this course" no botão
        if (!legacyButtonLink) {
            const buttons = cardContainer.querySelectorAll('button');
            for (let b of buttons) {
                const text = (b.innerText || "").toLowerCase();
                if (text.includes('buy this course') || text.includes('comprar')) {
                    legacyButtonLink = b.closest('a') || b;
                    break;
                }
            }
        }

        if (legacyButtonLink) {
            // Esconde o botão original
            legacyButtonLink.style.display = 'none';
            
            // Oculta também o preço solto antigo que ficava no topo do p-5 (se existir)
            const priceDiv = cardContainer.querySelector('.text-2xl.font-semibold.mb-3');
            if (priceDiv) priceDiv.style.display = 'none';

            // Cria o nosso container de opções
            const optionsContainer = document.createElement('div');
            optionsContainer.className = "mb-6 mt-4";
            optionsContainer.innerHTML = `<div style="font-weight: 600; font-size: 1.125rem; margin-bottom: 1rem; color: #0f172a;">Escolha seu plano</div>`;

            // Garante que o mensal apareça primeiro, depois o anual
            const monthlyPlan = purchaseOptions.find(p => p.billing_period === 'monthly');
            const annualPlan = purchaseOptions.find(p => p.billing_period === 'annual');

            if (monthlyPlan) optionsContainer.appendChild(createPlanButton(monthlyPlan));
            if (annualPlan) optionsContainer.appendChild(createPlanButton(annualPlan));

            // Insere antes das informações "This course has..." (espaçamento .space-y-3)
            const featuresDiv = cardContainer.querySelector('.space-y-3');
            if (featuresDiv) {
                cardContainer.insertBefore(optionsContainer, featuresDiv);
            } else {
                cardContainer.appendChild(optionsContainer);
            }

            cardModified = true;
        }

        // Substituição dos textos estáticos em inglês que ficaram no LMS
        translateStaticTexts(cardContainer);
    }

    function translateStaticTexts(cardContainer) {
        // Usa TreeWalker para varrer apenas os nós de texto (mais seguro que innerHTML)
        const walk = document.createTreeWalker(cardContainer, NodeFilter.SHOW_TEXT, null, false);
        let node;
        while (node = walk.nextNode()) {
            let text = node.nodeValue;
            let changed = false;
            
            if (text.includes("This course has:")) { text = text.replace("This course has:", "Este curso inclui:"); changed = true; }
            if (text.includes("enrolled students")) { text = text.replace("enrolled students", "alunos matriculados"); changed = true; }
            if (text.includes("enrolled student")) { text = text.replace("enrolled student", "aluno matriculado"); changed = true; }
            if (text.includes("lessons")) { text = text.replace("lessons", "aulas"); changed = true; }
            else if (text.includes("lesson")) { text = text.replace("lesson", "aula"); changed = true; }
            if (text.includes("average rating")) { text = text.replace("average rating", "avaliação média"); changed = true; }
            if (text.includes("Certificate of Completion")) { text = text.replace("Certificate of Completion", "Certificado de Conclusão"); changed = true; }
            if (text.includes("Paid Certificate after Evaluation")) { text = text.replace("Paid Certificate after Evaluation", "Certificado com Validação (MEC)"); changed = true; }
            
            if (changed) {
                node.nodeValue = text;
            }
        }
    }

    // Função debounced para não trigar muito no MutationObserver
    let mutationTimeout = null;
    function handleMutations() {
        if (!window.location.pathname.includes('/lms/courses/')) {
            cardModified = false;
            return;
        }
        
        const card = document.querySelector('.border-2.rounded-md.min-w-80.max-w-sm');
        if (card && !cardModified && !isFetching) {
            // Se já tem as opções prontas, aplica logo
            if (purchaseOptions) {
                modifyCourseCard();
            } else {
                fetchPurchaseOptions();
            }
        }
    }

    // Observa mudanças no DOM porque o Vue.js monta e atualiza o DOM client-side
    const observer = new MutationObserver(() => {
        if (mutationTimeout) clearTimeout(mutationTimeout);
        mutationTimeout = setTimeout(handleMutations, 150);
    });

    observer.observe(document.body, { childList: true, subtree: true });

    // Restaura intenção pós-login (verifica se acabou de logar)
    window.addEventListener('load', () => {
        // Frappe LMS pode mudar URL via History API, então chamamos a heurística no boot também
        handleMutations();

        const intentCourse = localStorage.getItem("vedium_intent_course");
        const intentPlan = localStorage.getItem("vedium_intent_plan");
        
        if (intentCourse && intentPlan && window.frappe && window.frappe.session && window.frappe.session.user !== "Guest") {
            // Limpa intenção (ele já está logado e vai ver a página do curso de novo para clicar)
            localStorage.removeItem("vedium_intent_course");
            localStorage.removeItem("vedium_intent_plan");
            
            if (!window.location.pathname.includes(`/lms/courses/${intentCourse}`)) {
                window.location.href = `/lms/courses/${intentCourse}`;
            }
        }
    });

})();
