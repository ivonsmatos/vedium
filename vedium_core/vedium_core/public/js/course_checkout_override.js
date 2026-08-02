(function () {
    "use strict";

    const CHECKOUT_OPTIONS_ENDPOINT =
        "/api/method/vedium_core.checkout_options.get_course_purchase_options";
    const CREATE_CHECKOUT_ENDPOINT =
        "/api/method/vedium_core.api.create_checkout_session";
    const HIGHLIGHT_COLOR = "#2E6DA4";

    let activeCourse = null;
    let purchaseOptions = null;
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

    function createPlanButton(plan) {
        const button = document.createElement("button");
        button.type = "button";
        button.className =
            "w-full mb-3 text-left border rounded-md p-4 transition-all duration-200 hover:shadow-md";
        button.style.borderColor = "#e2e8f0";
        button.style.backgroundColor = "#ffffff";
        button.style.cursor = "pointer";
        button.setAttribute(
            "aria-label",
            `${plan.title}: ${formatCurrency(plan.amount, plan.currency)} por mês`
        );

        button.onmouseover = () => {
            button.style.borderColor = HIGHLIGHT_COLOR;
        };
        button.onmouseout = () => {
            button.style.borderColor = "#e2e8f0";
        };

        const amount = formatCurrency(plan.amount, plan.currency);
        const savings = Number(plan.savings || 0);
        const savingsHtml =
            plan.billing_period === "annual" && savings > 0
                ? `<div style="color:#047857;font-size:.85rem;font-weight:600;margin-top:6px;">Economia de ${escapeHtml(
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
        const features = cardBody.querySelector(".space-y-3");
        if (features) {
            cardBody.insertBefore(container, features);
        } else {
            cardBody.appendChild(container);
        }
    }

    function renderPurchaseOptions(cardBody) {
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
        handlePage();

        const intentCourse = localStorage.getItem("vedium_intent_course");
        const intentPlan = localStorage.getItem("vedium_intent_plan");
        if (intentCourse && intentPlan && !isGuest()) {
            localStorage.removeItem("vedium_intent_course");
            localStorage.removeItem("vedium_intent_plan");
            if (!window.location.pathname.includes(`/lms/courses/${intentCourse}`)) {
                window.location.replace(`/lms/courses/${intentCourse}`);
            }
        }
    });
})();
