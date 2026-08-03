(function () {
    "use strict";

    const CHECKOUT_OPTIONS_ENDPOINT =
        "/api/method/vedium_core.checkout_options.get_course_purchase_options";
    const CREATE_CHECKOUT_ENDPOINT =
        "/api/method/vedium_core.frequency_checkout.create_checkout_session";
    const HIGHLIGHT_COLOR = "#2E6DA4";

    let activeCourse = null;
    let purchaseOptions = null;
    let selectedClassesPerWeek = 1;
    let isFetching = false;
    let mutationTimeout = null;

    function isCoursePage() {
        return window.location.pathname.includes("/lms/courses/");
    }

    function getCourseName() {
        const parts = window.location.pathname.split("/").filter(Boolean);
        return decodeURIComponent(parts[parts.length - 1] || "");
    }

    function resetForRouteChange() {
        const courseName = isCoursePage() ? getCourseName() : null;
        if (courseName !== activeCourse) {
            activeCourse = courseName;
            purchaseOptions = null;
            selectedClassesPerWeek = 1;
            isFetching = false;
        }
    }

    function escapeHtml(value) {
        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

    function formatCurrency(amount, currency) {
        const locale = currency === "USD" ? "en-US" : "pt-BR";
        return new Intl.NumberFormat(locale, {
            style: "currency",
            currency,
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        }).format(Number(amount || 0));
    }

    function getCourseCardBody() {
        return document.querySelector(
            ".border-2.rounded-md.min-w-80.max-w-sm .p-5"
        );
    }

    function findLegacyPurchaseControl(cardBody) {
        if (!cardBody) return null;

        const links = cardBody.querySelectorAll("a");
        for (const link of links) {
            const href = link.getAttribute("href") || "";
            if (
                href.includes("/billing/") ||
                href.includes("buy-this-course") ||
                href.includes("/stripe_checkout")
            ) {
                return link;
            }
        }

        const controls = cardBody.querySelectorAll("button, a");
        for (const control of controls) {
            const text = (control.innerText || "").trim().toLowerCase();
            if (
                text.includes("buy this course") ||
                text === "comprar" ||
                text.includes("comprar este curso")
            ) {
                return control.closest("a") || control;
            }
        }
        return null;
    }

    function removeExistingOverride(cardBody) {
        cardBody
            ?.querySelectorAll('[data-vedium-checkout="true"]')
            .forEach((element) => element.remove());
    }

    function hideLegacyCheckout(cardBody) {
        const legacyControl = findLegacyPurchaseControl(cardBody);
        if (legacyControl) {
            legacyControl.style.display = "none";
            legacyControl.setAttribute("aria-hidden", "true");
            legacyControl.setAttribute("tabindex", "-1");
        }

        const oldPrice = cardBody?.querySelector(
            ".text-2xl.font-semibold.mb-3"
        );
        if (oldPrice) oldPrice.style.display = "none";
    }

    function planTerms(plan) {
        if (plan.billing_period === "annual") {
            return (
                plan.terms ||
                "12 cobranças mensais. Permanência mínima de 12 meses."
            );
        }
        return plan.terms || "Cobrança mensal. Sem permanência mínima.";
    }

    function frequencyOption(plan) {
        const options = Array.isArray(plan.frequency_options)
            ? plan.frequency_options
            : [];
        return (
            options.find(
                (option) =>
                    Number(option.classes_per_week) ===
                    Number(selectedClassesPerWeek)
            ) || {
                classes_per_week: 1,
                subtotal: Number(plan.amount || 0),
                discount_percent: 0,
                discount_amount: 0,
                amount: Number(plan.amount || 0),
                savings: Number(plan.savings || 0),
            }
        );
    }

    function createFrequencySelector(container) {
        const wrapper = document.createElement("div");
        wrapper.style.marginBottom = "1rem";
        wrapper.innerHTML = `
            <div style="font-weight:700;font-size:.95rem;color:#1e293b;margin-bottom:.45rem;">
                Quantas aulas por semana?
            </div>
            <div style="color:#64748b;font-size:.78rem;line-height:1.35;margin-bottom:.65rem;">
                Escolha de 1 a 5 aulas. A partir de 2 aulas, o desconto recorrente de 10% é aplicado automaticamente.
            </div>
        `;

        const grid = document.createElement("div");
        grid.style.display = "grid";
        grid.style.gridTemplateColumns = "repeat(5, minmax(0, 1fr))";
        grid.style.gap = ".4rem";

        for (let classes = 1; classes <= 5; classes += 1) {
            const button = document.createElement("button");
            button.type = "button";
            button.textContent = String(classes);
            button.setAttribute(
                "aria-label",
                `${classes} ${classes === 1 ? "aula" : "aulas"} por semana`
            );
            button.style.padding = ".55rem .25rem";
            button.style.borderRadius = ".4rem";
            button.style.fontWeight = "700";
            button.style.cursor = "pointer";
            button.style.border = `1px solid ${
                classes === selectedClassesPerWeek
                    ? HIGHLIGHT_COLOR
                    : "#cbd5e1"
            }`;
            button.style.background =
                classes === selectedClassesPerWeek ? "#eff6ff" : "#ffffff";
            button.style.color =
                classes === selectedClassesPerWeek
                    ? HIGHLIGHT_COLOR
                    : "#334155";
            button.addEventListener("click", () => {
                selectedClassesPerWeek = classes;
                renderPurchaseOptions(getCourseCardBody());
            });
            grid.appendChild(button);
        }

        wrapper.appendChild(grid);
        container.appendChild(wrapper);
    }

    function createPlanButton(plan) {
        const quote = frequencyOption(plan);
        const button = document.createElement("button");
        button.type = "button";
        button.className =
            "w-full mb-3 text-left border rounded-md p-4 transition-all duration-200 hover:shadow-md";
        button.style.borderColor = "#e2e8f0";
        button.style.backgroundColor = "#ffffff";
        button.style.cursor = "pointer";
        button.setAttribute(
            "aria-label",
            `${plan.title}: ${formatCurrency(
                quote.amount,
                plan.currency
            )} por mês, ${selectedClassesPerWeek} aulas por semana`
        );

        button.onmouseover = () => {
            button.style.borderColor = HIGHLIGHT_COLOR;
        };
        button.onmouseout = () => {
            button.style.borderColor = "#e2e8f0";
        };

        const amount = formatCurrency(quote.amount, plan.currency);
        const hasFrequencyDiscount = Number(quote.discount_percent || 0) > 0;
        const subtotalHtml = hasFrequencyDiscount
            ? `<div style="color:#64748b;font-size:.78rem;margin-top:5px;">
                   De <span style="text-decoration:line-through;">${escapeHtml(
                       formatCurrency(quote.subtotal, plan.currency)
                   )}</span> · 10% de desconto
               </div>`
            : "";
        const savings = Number(quote.savings || 0);
        const savingsHtml =
            plan.billing_period === "annual" && savings > 0
                ? `<div style="color:#047857;font-size:.82rem;font-weight:600;margin-top:6px;">Economia de ${escapeHtml(
                      formatCurrency(savings, plan.currency)
                  )} em 12 meses</div>`
                : "";

        button.innerHTML = `
            <div style="display:flex;justify-content:space-between;gap:16px;align-items:flex-start;">
                <div style="min-width:0;">
                    <div style="font-weight:700;font-size:1.05rem;color:#1e293b;">
                        ${escapeHtml(plan.title)}
                    </div>
                    <div style="color:#475569;font-size:.82rem;line-height:1.35;margin-top:5px;">
                        ${escapeHtml(planTerms(plan))}
                    </div>
                    <div style="color:#475569;font-size:.82rem;line-height:1.35;margin-top:5px;">
                        ${escapeHtml(
                            `${selectedClassesPerWeek} ${
                                selectedClassesPerWeek === 1 ? "aula" : "aulas"
                            } por semana`
                        )}
                    </div>
                    ${subtotalHtml}
                    ${savingsHtml}
                </div>
                <div style="font-weight:700;font-size:1.05rem;color:${HIGHLIGHT_COLOR};white-space:nowrap;text-align:right;">
                    ${escapeHtml(amount)}
                    <div style="font-size:.75rem;font-weight:500;color:#64748b;margin-top:2px;">por mês</div>
                </div>
            </div>
        `;

        button.addEventListener("click", () => startCheckout(button, plan));
        return button;
    }

    function setButtonLoading(button) {
        button.disabled = true;
        button.style.pointerEvents = "none";
        button.style.opacity = "0.7";
        button.innerHTML =
            '<div style="text-align:center;font-size:.9rem;font-weight:600;padding:.5rem 0;color:#64748b;">Abrindo o pagamento seguro...</div>';
    }

    function isGuest() {
        return (
            !window.frappe ||
            !window.frappe.session ||
            window.frappe.session.user === "Guest"
        );
    }

    async function startCheckout(button, plan) {
        setButtonLoading(button);

        if (isGuest()) {
            localStorage.setItem("vedium_intent_course", getCourseName());
            localStorage.setItem(
                "vedium_intent_plan",
                plan.billing_period
            );
            localStorage.setItem(
                "vedium_intent_frequency",
                String(selectedClassesPerWeek)
            );
            window.location.href = `/login?redirect-to=${encodeURIComponent(
                window.location.pathname
            )}`;
            return;
        }

        try {
            const response = await fetch(CREATE_CHECKOUT_ENDPOINT, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-Frappe-CSRF-Token":
                        window.frappe?.csrf_token || "",
                },
                body: JSON.stringify({
                    course_name: getCourseName(),
                    billing_period: plan.billing_period,
                    classes_per_week: selectedClassesPerWeek,
                }),
            });

            const data = await response.json();
            if (
                response.ok &&
                data.message &&
                data.message.checkout_url &&
                data.message.checkout_url.startsWith("https://checkout.stripe.com/")
            ) {
                window.location.assign(data.message.checkout_url);
                return;
            }

            throw new Error(extractServerMessage(data));
        } catch (error) {
            console.error("Vedium checkout error:", error);
            alert(
                error.message ||
                    "Não foi possível abrir o pagamento. Tente novamente ou fale com a Vedium no WhatsApp."
            );
            window.location.reload();
        }
    }

    function extractServerMessage(data) {
        try {
            if (data?._server_messages) {
                const messages = JSON.parse(data._server_messages);
                const parsed = JSON.parse(messages[0]);
                if (parsed.message) return parsed.message;
            }
        } catch (error) {
            console.warn("Não foi possível interpretar a mensagem do servidor", error);
        }
        return "Não foi possível abrir o pagamento. Tente novamente ou fale com a Vedium no WhatsApp.";
    }

    function renderLoading(cardBody) {
        removeExistingOverride(cardBody);
        hideLegacyCheckout(cardBody);

        const container = document.createElement("div");
        container.dataset.vediumCheckout = "true";
        container.className = "mb-6 mt-4";
        container.innerHTML = `
            <div style="font-weight:700;font-size:1.125rem;margin-bottom:.75rem;color:#0f172a;">
                Escolha seu plano
            </div>
            <div style="color:#64748b;font-size:.9rem;">Carregando condições...</div>
        `;
        insertBeforeFeatures(cardBody, container);
    }

    function renderError(cardBody) {
        removeExistingOverride(cardBody);
        hideLegacyCheckout(cardBody);

        const container = document.createElement("div");
        container.dataset.vediumCheckout = "true";
        container.className = "mb-6 mt-4";
        container.innerHTML = `
            <div style="font-weight:700;font-size:1.05rem;color:#0f172a;margin-bottom:.5rem;">
                Pagamento temporariamente indisponível
            </div>
            <div style="color:#64748b;font-size:.85rem;line-height:1.4;">
                Fale com a Vedium no WhatsApp para receber orientação.
            </div>
        `;
        insertBeforeFeatures(cardBody, container);
    }

    function insertBeforeFeatures(cardBody, container) {
        if (!cardBody) return;
        const features = cardBody.querySelector(".space-y-3");
        if (features) {
            cardBody.insertBefore(container, features);
        } else {
            cardBody.appendChild(container);
        }
    }

    function renderPurchaseOptions(cardBody) {
        if (!cardBody || !purchaseOptions) return;
        removeExistingOverride(cardBody);
        hideLegacyCheckout(cardBody);

        const container = document.createElement("div");
        container.dataset.vediumCheckout = "true";
        container.className = "mb-6 mt-4";
        container.innerHTML = `
            <div style="font-weight:700;font-size:1.125rem;margin-bottom:.35rem;color:#0f172a;">
                Escolha seu plano
            </div>
            <div style="color:#64748b;font-size:.82rem;line-height:1.4;margin-bottom:1rem;">
                O pagamento é concluído no ambiente seguro da Stripe.
            </div>
        `;

        createFrequencySelector(container);

        const monthlyPlan = purchaseOptions.find(
            (plan) => plan.billing_period === "monthly"
        );
        const annualPlan = purchaseOptions.find(
            (plan) => plan.billing_period === "annual"
        );

        if (monthlyPlan) container.appendChild(createPlanButton(monthlyPlan));
        if (annualPlan) container.appendChild(createPlanButton(annualPlan));

        insertBeforeFeatures(cardBody, container);
    }

    async function fetchPurchaseOptions(cardBody) {
        if (isFetching || purchaseOptions || !activeCourse) return;
        isFetching = true;
        renderLoading(cardBody);

        try {
            const url = `${CHECKOUT_OPTIONS_ENDPOINT}?course_name=${encodeURIComponent(
                activeCourse
            )}`;
            const response = await fetch(url, {
                method: "GET",
                credentials: "same-origin",
                headers: { Accept: "application/json" },
            });
            const data = await response.json();

            if (
                !response.ok ||
                !data.message?.is_paid ||
                !Array.isArray(data.message.plans) ||
                data.message.plans.length === 0
            ) {
                throw new Error("Planos indisponíveis");
            }

            purchaseOptions = data.message.plans;
            renderPurchaseOptions(cardBody);
        } catch (error) {
            console.error("Erro ao buscar opções de compra:", error);
            renderError(cardBody);
        } finally {
            isFetching = false;
        }
    }

    function translateStaticTexts(root) {
        if (!root) return;
        const walker = document.createTreeWalker(
            root,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );
        let node;
        while ((node = walker.nextNode())) {
            let text = node.nodeValue || "";
            const replacements = [
                ["This course has:", "Este curso inclui:"],
                ["enrolled students", "alunos matriculados"],
                ["enrolled student", "aluno matriculado"],
                ["lessons", "aulas"],
                ["lesson", "aula"],
                ["average rating", "avaliação média"],
                ["Certificate of Completion", "Certificado de Conclusão"],
                ["Buy this course", "Escolher plano"],
            ];
            for (const [source, target] of replacements) {
                text = text.replace(source, target);
            }
            node.nodeValue = text;
        }
    }

    function handlePage() {
        resetForRouteChange();
        if (!isCoursePage() || !activeCourse) return;

        const cardBody = getCourseCardBody();
        if (!cardBody) return;

        translateStaticTexts(cardBody);
        hideLegacyCheckout(cardBody);

        if (purchaseOptions) {
            if (!cardBody.querySelector('[data-vedium-checkout="true"]')) {
                renderPurchaseOptions(cardBody);
            }
            return;
        }

        if (!isFetching) fetchPurchaseOptions(cardBody);
    }

    if (window.location.pathname.includes("/lms/billing/course/")) {
        const courseName = window.location.pathname.split("/").pop();
        window.location.replace(`/lms/courses/${courseName}`);
        return;
    }

    const observer = new MutationObserver(() => {
        if (mutationTimeout) window.clearTimeout(mutationTimeout);
        mutationTimeout = window.setTimeout(handlePage, 150);
    });
    observer.observe(document.body, { childList: true, subtree: true });

    window.addEventListener("load", () => {
        const storedFrequency = Number(
            localStorage.getItem("vedium_intent_frequency") || 1
        );
        if (storedFrequency >= 1 && storedFrequency <= 5) {
            selectedClassesPerWeek = storedFrequency;
        }
        handlePage();

        const intentCourse = localStorage.getItem("vedium_intent_course");
        const intentPlan = localStorage.getItem("vedium_intent_plan");
        if (intentCourse && intentPlan && !isGuest()) {
            localStorage.removeItem("vedium_intent_course");
            localStorage.removeItem("vedium_intent_plan");
            localStorage.removeItem("vedium_intent_frequency");
            if (!window.location.pathname.includes(`/lms/courses/${intentCourse}`)) {
                window.location.replace(`/lms/courses/${intentCourse}`);
            }
        }
    });
})();
