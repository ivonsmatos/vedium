"use client";

import { useState } from "react";
import { Icon } from "@/components/ui/Icon";
import { Button } from "@/components/ui/Button";
import { TextLink } from "@/components/ui/TextLink";
import { CONTACT_FORM_COPY, FORM_LANGUAGE_OPTIONS, FORM_SUBJECT_OPTIONS } from "@/content/contact";

type Status = "idle" | "loading" | "success" | "error";

interface FormState {
  name: string;
  email: string;
  phone: string;
  subject: string;
  language: string;
  message: string;
  // Honeypot -- humano nunca vê nem preenche este campo (fora da tab
  // order, aria-hidden). Se vier preenchido, é bot.
  companyWebsite: string;
}

const INITIAL_STATE: FormState = {
  name: "",
  email: "",
  phone: "",
  subject: FORM_SUBJECT_OPTIONS[0].label,
  language: FORM_LANGUAGE_OPTIONS[0],
  message: "",
  companyWebsite: "",
};

export function ContactForm() {
  const [form, setForm] = useState<FormState>(INITIAL_STATE);
  const [status, setStatus] = useState<Status>("idle");
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [serverMessage, setServerMessage] = useState<string | null>(null);

  function update<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  function validate(): Record<string, string> {
    const errors: Record<string, string> = {};
    if (!form.name.trim()) errors.name = "Informe seu nome.";
    if (!form.email.trim()) {
      errors.email = "Informe seu e-mail.";
    } else if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email.trim())) {
      errors.email = "Informe um e-mail válido.";
    }
    return errors;
  }

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (status === "loading") return; // evita duplo envio em duplo clique
    const errors = validate();
    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      setStatus("error");
      setServerMessage(null);
      return;
    }

    setStatus("loading");
    setFieldErrors({});
    setServerMessage(null);

    const subjectOption = FORM_SUBJECT_OPTIONS.find((option) => option.label === form.subject) ?? FORM_SUBJECT_OPTIONS[0];

    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: form.name.trim(),
          email: form.email.trim(),
          phone: form.phone.trim(),
          intent: subjectOption.intent,
          goal: subjectOption.goal,
          language: form.language,
          message: form.message.trim(),
          companyWebsite: form.companyWebsite,
        }),
      });
      const data = await response.json();

      if (!response.ok || !data.ok) {
        if (data.field) {
          setFieldErrors({ [data.field]: data.message });
        } else {
          setServerMessage(data.message || CONTACT_FORM_COPY.serverErrorText);
        }
        setStatus("error");
        return; // não apaga os dados digitados (missão seção 16)
      }

      setStatus("success");
      setForm(INITIAL_STATE);
    } catch {
      setServerMessage(CONTACT_FORM_COPY.serverErrorText);
      setStatus("error");
    }
  }

  return (
    <form className="v2-contact-form" onSubmit={onSubmit} noValidate>
      {status === "success" ? (
        <div className="v2-alert v2-alert--success" role="status" aria-live="polite">
          <Icon name="check" decorative={false} label="Sucesso" className="v2-alert__icon" />
          <div className="v2-alert__body">
            <p className="v2-alert__title">{CONTACT_FORM_COPY.successTitle}</p>
            <p>{CONTACT_FORM_COPY.successText}</p>
          </div>
        </div>
      ) : null}

      {status === "error" && serverMessage ? (
        <div className="v2-alert v2-alert--danger" role="alert" aria-live="assertive" style={{ marginBlockEnd: "var(--v2-space-4)" }}>
          <Icon name="close" decorative={false} label="Erro" className="v2-alert__icon" />
          <div className="v2-alert__body">
            <p>{serverMessage}</p>
          </div>
        </div>
      ) : null}

      <div className={`v2-field${fieldErrors.name ? " v2-field--error" : ""}`}>
        <label className="v2-field__label" htmlFor="contact-name">
          {CONTACT_FORM_COPY.fields.name} <span className="v2-field__required">*</span>
        </label>
        <input
          id="contact-name"
          className="v2-input"
          type="text"
          autoComplete="name"
          value={form.name}
          onChange={(event) => update("name", event.target.value)}
          aria-invalid={Boolean(fieldErrors.name)}
          aria-describedby={fieldErrors.name ? "contact-name-error" : undefined}
        />
        {fieldErrors.name ? (
          <p className="v2-field__error" id="contact-name-error">
            {fieldErrors.name}
          </p>
        ) : null}
      </div>

      <div className={`v2-field${fieldErrors.email ? " v2-field--error" : ""}`}>
        <label className="v2-field__label" htmlFor="contact-email">
          {CONTACT_FORM_COPY.fields.email} <span className="v2-field__required">*</span>
        </label>
        <input
          id="contact-email"
          className="v2-input"
          type="email"
          autoComplete="email"
          value={form.email}
          onChange={(event) => update("email", event.target.value)}
          aria-invalid={Boolean(fieldErrors.email)}
          aria-describedby={fieldErrors.email ? "contact-email-error" : undefined}
        />
        {fieldErrors.email ? (
          <p className="v2-field__error" id="contact-email-error">
            {fieldErrors.email}
          </p>
        ) : null}
      </div>

      <div className="v2-field">
        <label className="v2-field__label" htmlFor="contact-phone">
          {CONTACT_FORM_COPY.fields.phone}
        </label>
        <input id="contact-phone" className="v2-input" type="tel" autoComplete="tel" value={form.phone} onChange={(event) => update("phone", event.target.value)} />
      </div>

      <div className="v2-field">
        <label className="v2-field__label" htmlFor="contact-subject">
          {CONTACT_FORM_COPY.fields.subject}
        </label>
        <div className="v2-select-wrap">
          <select id="contact-subject" className="v2-select" value={form.subject} onChange={(event) => update("subject", event.target.value)}>
            {FORM_SUBJECT_OPTIONS.map((option) => (
              <option key={option.label} value={option.label}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="v2-field">
        <label className="v2-field__label" htmlFor="contact-language">
          {CONTACT_FORM_COPY.fields.language}
        </label>
        <div className="v2-select-wrap">
          <select id="contact-language" className="v2-select" value={form.language} onChange={(event) => update("language", event.target.value)}>
            {FORM_LANGUAGE_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="v2-field">
        <label className="v2-field__label" htmlFor="contact-message">
          {CONTACT_FORM_COPY.fields.message}
        </label>
        <textarea id="contact-message" className="v2-input" rows={4} value={form.message} onChange={(event) => update("message", event.target.value)} />
      </div>

      {/* Honeypot -- invisível e fora da tab order para humanos; bots que
          preenchem tudo automaticamente costumam preencher isto também. */}
      <div aria-hidden="true" style={{ position: "absolute", left: "-9999px", width: 1, height: 1, overflow: "hidden" }}>
        <label htmlFor="contact-company-website">Não preencha este campo</label>
        <input id="contact-company-website" type="text" tabIndex={-1} autoComplete="off" value={form.companyWebsite} onChange={(event) => update("companyWebsite", event.target.value)} />
      </div>

      <p className="v2-body-sm v2-text-subtle">
        {CONTACT_FORM_COPY.privacyNoticeText}{" "}
        <TextLink href={CONTACT_FORM_COPY.privacyNoticeHref} size="default">
          {CONTACT_FORM_COPY.privacyNoticeLinkText}
        </TextLink>
        .
      </p>

      <Button type="submit" variant="primary">
        {status === "loading" ? CONTACT_FORM_COPY.submitLabelLoading : CONTACT_FORM_COPY.submitLabel}
      </Button>
    </form>
  );
}
