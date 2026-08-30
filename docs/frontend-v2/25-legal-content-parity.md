# 25 — Paridade do conteúdo legal

Verificação textual V1 (produção/Frappe) × Next executada em 29/08/2026 com `frontend/scripts/legal-audit.mjs`.

## Método

1. Abrir a rota pública em `https://vediums.com` e capturar `.vd-legal .container`.
2. Abrir a rota no build local Next e capturar `[data-legal-source-content]`.
3. Remover somente elementos adicionais marcados `data-parity-ignore` (eyebrow, índice e navegação entre documentos).
4. Normalizar Unicode NFC e whitespace.
5. Comparar o texto integral e calcular SHA-256.

Markup, anchors e espaços não alteram o resultado. Texto, pontuação, números, datas, células de tabela e labels de links alteram o hash e fazem o teste falhar.

Reprodução:

```powershell
cd frontend
npm run build
npm start -- -p 3104
node scripts/legal-audit.mjs
```

## Resultado

| Documento | V1 words | Next words | V1 SHA-256 | Next SHA-256 | Paridade |
|---|---:|---:|---|---|---|
| Privacidade | 932 | 932 | `7a129ca04a1e3168fb48f7edc0c6a7eb5bdeea9ceb282c3234847902f20bfa0c` | `7a129ca04a1e3168fb48f7edc0c6a7eb5bdeea9ceb282c3234847902f20bfa0c` | **PASS** |
| Termos | 854 | 854 | `b9b8b468a833ad8326c32e418e5730884a387da009196d83ea36c1115a8d9b42` | `b9b8b468a833ad8326c32e418e5730884a387da009196d83ea36c1115a8d9b42` | **PASS** |
| Cancelamento/Reembolso | 544 | 544 | `9a53c90783c1e896f284cc3f95eadfca0e294d14f2c4601722c2c4e9aef9cfe4` | `9a53c90783c1e896f284cc3f95eadfca0e294d14f2c4601722c2c4e9aef9cfe4` | **PASS** |

Resumo exigido:

- `PRIVACY CONTENT PARITY: PASS`
- `TERMS CONTENT PARITY: PASS`
- `CANCELLATION CONTENT PARITY: PASS`

## Hash dos arquivos-fonte brutos

Esses hashes preservam também markup, CSS/Jinja e whitespace dos templates Frappe; são registro técnico, não a regra de paridade semântica:

| Template | SHA-256 bruto |
|---|---|
| `privacidade.html` | `c16a64b2c4d96ca59f9a2408c2eecefc12a3720b831353228ac48e17dd7ef23e` |
| `termos.html` | `4cbad1411f33fce6c8c104bd7500a2bbb0e6c2b201315fac3ab3bf86242f4800` |
| `cancelamento-reembolso.html` | `673c326d2d32212f98a93df4af7f155974f7ccd243276ada95855a0672169e98` |

## Preservação por categoria

| Categoria | Privacidade | Termos | Cancelamento |
|---|---|---|---|
| Título e data | Preservados | Preservados | Preservados |
| Headings | 13/13 | 14/14 | 10/10 |
| Parágrafos/listas | Preservados | Preservados | Preservados |
| Tabelas | 3/3 | n/a | n/a |
| Prazos e números | Preservados | Preservados | Preservados |
| Entidade/contato | Preservados | Preservados | Preservados |
| Links/PDFs | Preservados | Preservados | Preservados |
| Carimbo/base legal | Preservado | Preservado | Preservado |

## Alterações técnicas excluídas do hash

- Eyebrow “DOCUMENTOS LEGAIS”.
- Índice navegável construído com os títulos reais.
- IDs de anchor nos H2.
- Navegação simples Privacidade / Termos / Cancelamento e Reembolso.
- Header/Footer Next e estilos responsivos.

Nenhum desses elementos substitui, resume ou altera cláusula.

## Gate

Qualquer diferença futura no texto normalizado gera `parity: FAIL` e inclui o primeiro trecho divergente no JSON do audit. Não promover a rota enquanto houver FAIL não justificado por revisão jurídica versionada.
