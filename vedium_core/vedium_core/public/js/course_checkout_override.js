(function () {
    "use strict";

    const OPTIONS_ENDPOINT =
        "/api/method/vedium_core.checkout_options.get_course_purchase_options";
    const LMS_CHECKOUT_ENDPOINT =
        "/api/method/vedium_core.frequency_checkout.create_checkout_session";
    const PUBLIC_CHECKOUT_ENDPOINT =
        "https://app.vediums.com/api/method/vedium_core.public_frequency_checkout.start";
    const HIGHLIGHT_COLOR = "#2E6DA4";

    if (!document.getElementById("vedium-frequency-selector-style")) {
        const style = document.createElement("style");
        style.id = "vedium-frequency-selector-style";
        style.textContent = `
            .vedium-frequency-selector {
                width: 100%;
                margin: 0 0 16px;
            }
            .vedium-frequency-selector label {
                display: block;
                margin-bottom: 7px;
                color: #172033;
                font-size: 14px;
                font-weight: 700;
            }
            .vedium-frequency-selector select {
                display: block;
                width: 100%;
                min-height: 48px;
                padding: 0 42px 0 14px;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                background: #fff;
                color: #172033;
                font-size: 15px;
                font-weight: 600;
                cursor: pointer;
            }
            .vedium-frequency-selector select:focus {
                border-color: #315cff;
                outline: 3px solid rgba(49, 92, 255, 0.15);
            }
        `;
        document.head.appendChild(style);
    }

    let activeCourse = null;
    let purchaseOptions = null;
    let selectedClassesPerWeek = 1;
    let isFetching = false;
    let mutationTimeout = null;

    function isLmsCoursePage() {
        return window.location.pathname.includes("/lms/courses/");
    }

    function isPublicCoursePage() {
        return /\/(?:[a-z]{2}(?:-[a-z]{2})?\/)?curso\//i.test(
            window.location.pathname
        );
    }

    function getCourseFromPublicButton() {
        const priceCard = document.querySelector(".course-details__price");
        if (priceCard && priceCard.dataset.courseName) {
            return priceCard.dataset.courseName;
        }

        const link = document.querySelector(
            '.course-details__price-btn a[href*="course_name="]'
        );
        if (!link) return null;
        try {
            return new URL(link.href, window.location.origin).searchParams.get(
                "course_name"
            );
        } catch (error) {
            return null;
        }
    }

    function getCourseName() {
        if (isPublicCoursePage()) {
            return getCourseFromPublicButton();
        }
        const parts = window.location.pathname.split("/").filter(Boolean);
        return decodeURIComponent(parts[parts.length - 1] || "");
    }

    function initialFrequency() {
        const queryValue = new URLSearchParams(window.location.search).get(
            "classes_per_week"
        );
        const storedValue = localStorage.getItem("vedium_intent_frequency");
        const candidate = Number(queryValue || storedValue || 1);
        return Number.isInteger(candidate) && candidate >= 1 && candidate <= 5
            ? candidate
            : 1;
    }

    function resetForRouteChange() {
        const courseName =
            isLmsCoursePage() || isPublicCoursePage() ? getCourseName() : null;
        if (courseName !== activeCourse) {
            activeCourse = courseName;
            purchaseOptions = null;
            selectedClassesPerWeek = initialFrequency();
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

    function planFor(period) {
        return (purchaseOptions || []).find(
            (plan) => plan.billing_period === period
        );
    }

    function quoteFor(plan) {
        const options = Array.isArray(plan?.frequency_options)
            ? plan.frequency_options
            : [];
        return (
            options.find(
                (option) =>
                    Number(option.classes_per_week) ===
                    selectedClassesPerWeek
            ) || {
                classes_per_week: 1,
                subtotal: Number(plan?.amount || 0),
                discount_percent: 0,
                discount_amount: 0,
                amount: Number(plan?.amount || 0),
                savings: Number(plan?.savings || 0),
            }
        );
    }

    function buildFrequencySelector(onChange) {
        const wrapper = document.createElement("div");
        wrapper.dataset.vediumFrequencySelector = "true";
        wrapper.className = "vedium-frequency-selector";

        const label = document.createElement("label");
        label.setAttribute("for", "vedium-classes-per-week");
        label.textContent = "Quantidade de aulas por semana";

        const select = document.createElement("select");
        select.id = "vedium-classes-per-week";
        select.name = "classes_per_week";
        select.setAttribute("aria-label", "Quantidade de aulas por semana");
        select.style.width = "60%";
        select.style.minWidth = "220px";

        for (let classes = 1; classes <= 5; classes += 1) {
            const option = document.createElement("option");
            option.value = String(classes);
            option.textContent =
                classes === 1
                    ? "1 aula por semana"
                    : `${classes} aulas por semana — 10% de desconto`;
            option.selected = classes === selectedClassesPerWeek;
            select.appendChild(option);
        }

        select.addEventListener("change", function () {
            const classes = Number(select.value);

            if (!Number.isInteger(classes) || classes < 1 || classes > 5) {
                return;
            }

            selectedClassesPerWeek = classes;
            localStorage.setItem("vedium_intent_frequency", String(classes));
            onChange();
        });

        wrapper.appendChild(label);
        wrapper.appendChild(select);
        return wrapper;
    }

    function publicCheckoutUrl(plan) {
        const params = new URLSearchParams({
            course_name: activeCourse,
            billing_period: plan.billing_period,
            classes_per_week: String(selectedClassesPerWeek),
        });
        return `${PUBLIC_CHECKOUT_ENDPOINT}?${params.toString()}`;
    }

    function renderPublicCourse() {
        if (!purchaseOptions || !isPublicCoursePage()) return;

        const priceCard = document.querySelector(".course-details__price");
        const amountElement = priceCard?.querySelector(
            ".course-details__price-amount"
        );
        const buttonArea = priceCard?.querySelector(
            ".course-details__price-btn"
        );
        if (!priceCard || !amountElement || !buttonArea) return;

        if (priceCard.dataset.vediumRenderedCourse === activeCourse && 
            priceCard.dataset.vediumRenderedFrequency === String(selectedClassesPerWeek)) {
            return; // State hasn't changed, avoid re-rendering and losing focus
        }
        priceCard.dataset.vediumRenderedCourse = activeCourse;
        priceCard.dataset.vediumRenderedFrequency = String(selectedClassesPerWeek);

        priceCard
            .querySelectorAll('[data-vedium-frequency-selector="true"]')
            .forEach((element) => element.remove());
        priceCard
            .querySelectorAll('[data-vedium-frequency-summary="true"]')
            .forEach((element) => element.remove());

        const monthlyPlan = planFor("monthly") || purchaseOptions[0];
        const annualPlan = planFor("annual");
        const monthlyQuote = quoteFor(monthlyPlan);

        amountElement.setAttribute("aria-live", "polite");
        amountElement.innerHTML = `${escapeHtml(
            formatCurrency(monthlyQuote.amount, monthlyPlan.currency)
        )}<span>/mês</span>`;

        const selector = buildFrequencySelector(renderPublicCourse);
        buttonArea.parentNode.insertBefore(selector, buttonArea);

        const summary = document.createElement("div");
        summary.dataset.vediumFrequencySummary = "true";
        summary.style.margin = "-5px 0 15px";
        summary.style.fontSize = "12px";
        summary.style.lineHeight = "1.45";
        summary.style.color = "#64748b";
        summary.innerHTML =
            Number(monthlyQuote.discount_percent || 0) > 0
                ? `Valor normal: <span style="text-decoration:line-through;">${escapeHtml(
                      formatCurrency(
                          monthlyQuote.subtotal,
                          monthlyPlan.currency
                      )
                  )}</span> · <strong style="color:#047857;">10% de desconto</strong>`
                : "Plano de 1 aula por semana, sem desconto de frequência.";
        buttonArea.parentNode.insertBefore(summary, buttonArea);

        const monthlyButton = buttonArea.querySelector("a.thm-btn");
        if (monthlyButton) {
            monthlyButton.href = publicCheckoutUrl(monthlyPlan);
            monthlyButton.textContent = "MATRICULAR AGORA";
            monthlyButton.onclick = function () {
                window.dataLayer = window.dataLayer || [];
                window.dataLayer.push({
                    event: "course_enrollment_intent_click",
                    course: activeCourse,
                    billing_period: "monthly",
                    classes_per_week: selectedClassesPerWeek,
                    location: "course_detail",
                });
            };
        }

        const annualNote = buttonArea.querySelector(
            ".course-details__annual-note"
        );
        const annualLink = buttonArea.querySelector(
            ".course-details__annual-link"
        );
        if (annualPlan && annualLink) {
            const annualQuote = quoteFor(annualPlan);
            annualLink.href = publicCheckoutUrl(annualPlan);
            annualLink.textContent = "Escolher plano anual";
            if (annualNote) {
                const savings = Number(annualQuote.savings || 0);
                annualNote.textContent = `Plano anual: ${formatCurrency(
                    annualQuote.amount,
                    annualPlan.currency
                )}/mês · 12 cobranças${
                    savings > 0
                        ? ` · economia de ${formatCurrency(
                              savings,
                              annualPlan.currency
                          )}`
                        : ""
                }`;
            }
            annualLink.onclick = function () {
                window.dataLayer = window.dataLayer || [];
                window.dataLayer.push({
                    event: "course_enrollment_intent_click",
                    course: activeCourse,
                    billing_period: "annual",
                    classes_per_week: selectedClassesPerWeek,
                    location: "course_detail",
                });
            };
        }
    }

    function getLmsCardBody() {
        return document.querySelector(
            ".border-2.rounded-md.min-w-80.max-w-sm .p-5"
        );
    }

    function findLegacyPurchaseControl(cardBody) {
        if (!cardBody) return null;
        const controls = cardBody.querySelectorAll("button, a");
        for (const control of controls) {
            const href = control.getAttribute("href") || "";
            const text = (control.innerText || "").trim().toLowerCase();
            if (
                href.includes("/billing/") ||
                href.includes("buy-this-course") ||
                href.includes("/stripe_checkout") ||
                text.includes("buy this course") ||
                text.includes("comprar este curso") ||
                text === "comprar"
            ) {
                return control.closest("a") || control;
            }
        }
        return null;
    }

    function hideLegacyLmsCheckout(cardBody) {
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

    function removeLmsOverride(cardBody) {
        cardBody
            ?.querySelectorAll('[data-vedium-checkout="true"]')
            .forEach((element) => element.remove());
    }

    function planTerms(plan) {
        return plan.billing_period === "annual"
            ? plan.terms ||
                  "12 cobranças mensais. Permanência mínima de 12 meses."
            : plan.terms || "Cobrança mensal. Sem permanência mínima.";
    }

    function createLmsPlanButton(plan) {
        const quote = quoteFor(plan);
        const button = document.createElement("button");
        button.type = "button";
        button.className =
            "w-full mb-3 text-left border rounded-md p-4 transition-all duration-200 hover:shadow-md";
        button.style.borderColor = "#e2e8f0";
        button.style.backgroundColor = "#ffffff";
        button.style.cursor = "pointer";

        const discounted = Number(quote.discount_percent || 0) > 0;
        const savings = Number(quote.savings || 0);
        button.innerHTML = `
            <div style="display:flex;justify-content:space-between;gap:14px;align-items:flex-start;">
                <div style="min-width:0;">
                    <div style="font-weight:700;font-size:1.02rem;color:#1e293b;">${escapeHtml(
                        plan.title
                    )}</div>
                    <div style="color:#475569;font-size:.8rem;line-height:1.35;margin-top:5px;">${escapeHtml(
                        planTerms(plan)
                    )}</div>
                    <div style="color:#475569;font-size:.8rem;margin-top:5px;">${selectedClassesPerWeek} ${
            selectedClassesPerWeek === 1 ? "aula" : "aulas"
        } por semana</div>
                    ${
                        discounted
                            ? `<div style="color:#047857;font-size:.78rem;font-weight:600;margin-top:5px;">10% de desconto · de <span style="text-decoration:line-through;">${escapeHtml(
                                  formatCurrency(
                                      quote.subtotal,
                                      plan.currency
                                  )
                              )}</span></div>`
                            : ""
                    }
                    ${
                        plan.billing_period === "annual" && savings > 0
                            ? `<div style="color:#047857;font-size:.78rem;font-weight:600;margin-top:5px;">Economia de ${escapeHtml(
                                  formatCurrency(savings, plan.currency)
                              )} em 12 meses</div>`
                            : ""
                    }
                </div>
                <div style="font-weight:700;font-size:1.02rem;color:${HIGHLIGHT_COLOR};white-space:nowrap;text-align:right;">${escapeHtml(
            formatCurrency(quote.amount, plan.currency)
        )}<div style="font-size:.72rem;font-weight:500;color:#64748b;margin-top:2px;">por mês</div></div>
            </div>
        `;
        button.addEventListener("click", function () {
            startLmsCheckout(button, plan);
        });
        return button;
    }

    async function startLmsCheckout(button, plan) {
        button.disabled = true;
        button.style.opacity = "0.7";

        if (
            !window.frappe ||
            !window.frappe.session ||
            window.frappe.session.user === "Guest"
        ) {
            localStorage.setItem("vedium_intent_course", activeCourse);
            localStorage.setItem("vedium_intent_plan", plan.billing_period);
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
            const response = await fetch(LMS_CHECKOUT_ENDPOINT, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-Frappe-CSRF-Token": window.frappe?.csrf_token || "",
                },
                body: JSON.stringify({
                    course_name: activeCourse,
                    billing_period: plan.billing_period,
                    classes_per_week: selectedClassesPerWeek,
                }),
            });
            const data = await response.json();
            const checkoutUrl = data.message?.checkout_url || "";
            if (response.ok && checkoutUrl.startsWith("https://checkout.stripe.com/")) {
                window.location.assign(checkoutUrl);
                return;
            }
            throw new Error("Não foi possível abrir o pagamento.");
        } catch (error) {
            console.error("Vedium checkout error:", error);
            alert(
                "Não foi possível abrir o pagamento. Tente novamente ou fale com a Vedium."
            );
            window.location.reload();
        }
    }

    function renderLmsCourse() {
        if (!purchaseOptions || !isLmsCoursePage()) return;

        const cardBody = getLmsCardBody();
        if (!cardBody) return;

        if (cardBody.dataset.vediumRenderedCourse === activeCourse && 
            cardBody.dataset.vediumRenderedFrequency === String(selectedClassesPerWeek)) {
            return; // State hasn't changed
        }
        cardBody.dataset.vediumRenderedCourse = activeCourse;
        cardBody.dataset.vediumRenderedFrequency = String(selectedClassesPerWeek);

        removeLmsOverride(cardBody);
        hideLegacyLmsCheckout(cardBody);

        const container = document.createElement("div");
        container.dataset.vediumCheckout = "true";
        container.className = "mb-6 mt-4";
        container.innerHTML = `
            <div style="font-weight:700;font-size:1.125rem;margin-bottom:.35rem;color:#0f172a;">Escolha seu plano</div>
            <div style="color:#64748b;font-size:.82rem;line-height:1.4;margin-bottom:1rem;">Pagamento seguro processado pela Stripe.</div>
        `;
        container.appendChild(buildFrequencySelector(renderLmsCourse));

        const monthlyPlan = planFor("monthly");
        const annualPlan = planFor("annual");
        if (monthlyPlan) container.appendChild(createLmsPlanButton(monthlyPlan));
        if (annualPlan) container.appendChild(createLmsPlanButton(annualPlan));

        const features = cardBody.querySelector(".space-y-3");
        if (features) cardBody.insertBefore(container, features);
        else cardBody.appendChild(container);
    }

    function renderCurrentPage() {
        if (isPublicCoursePage()) renderPublicCourse();
        if (isLmsCoursePage()) renderLmsCourse();
    }

    async function fetchPurchaseOptions() {
        if (isFetching || purchaseOptions || !activeCourse) return;
        isFetching = true;
        try {
            const response = await fetch(
                `${OPTIONS_ENDPOINT}?course_name=${encodeURIComponent(
                    activeCourse
                )}`,
                {
                    method: "GET",
                    credentials: "same-origin",
                    headers: { Accept: "application/json" },
                }
            );
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
            renderCurrentPage();
        } catch (error) {
            console.error("Erro ao buscar opções de compra:", error);
        } finally {
            isFetching = false;
        }
    }

    function handlePage() {
        resetForRouteChange();
        if (!activeCourse) return;
        if (purchaseOptions) {
            renderCurrentPage();
            return;
        }
        fetchPurchaseOptions();
    }

    if (window.location.pathname.includes("/lms/billing/course/")) {
        const courseName = window.location.pathname.split("/").pop();
        window.location.replace(`/lms/courses/${courseName}`);
        return;
    }

    const observer = new MutationObserver(function () {
        if (mutationTimeout) window.clearTimeout(mutationTimeout);
        mutationTimeout = window.setTimeout(handlePage, 150);
    });
    observer.observe(document.body, { childList: true, subtree: true });

    window.addEventListener("load", handlePage);
    handlePage();
})();
