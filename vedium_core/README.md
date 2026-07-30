# Vedium Core

Core application for Vedium platform.

## Integração com o Brevo

A sincronização de uma matrícula com o Brevo é opcional e usa estas chaves do
`site_config.json`:

```json
{
  "BREVO_API_KEY": "xkeysib-...",
  "BREVO_LIST_IDS": [12, 34]
}
```

`BREVO_API_KEY` habilita a integração. `BREVO_LIST_IDS` é opcional e associa o
contato às listas informadas, que podem disparar as automações configuradas no
Brevo. A sincronização ocorre quando um formulário público registra interesse
e quando uma matrícula é criada. A chave deve permanecer apenas na configuração
do site e nunca ser versionada.

O atributo de interesse ou matrícula enviado no payload é `COURSE`. Esse
atributo deve existir previamente no Brevo; `COURSE_INTEREST` não faz parte do
contrato da integração.
