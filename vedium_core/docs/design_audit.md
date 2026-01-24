# Auditoria do Design System: "Raízes de Luxo"

**Objetivo**: Garantir que todos os templates sigam o sistema de design "Raízes de Luxo".

## Referência de Tokens

- **Cores**:
  - Primária: `var(--primary)` (#FECF03)
  - Ação: `var(--action)` (#FF2712)
  - Rodapé: `var(--footer)` (#2A3290)
- **Tipografia**: `Kanit` (Sans-serif)

## Checklist

### Elementos Globais

- [ ] **Favicon**: O logo correto está sendo usado?
- [ ] **Tipografia**: A fonte `Kanit` está aplicada globalmente?
- [ ] **Botões**: Os botões usam o gradiente ou cor de ação sólida com efeitos de hover?

### Componentes

- [ ] **Navbar**: Verifique o alinhamento do logo e a visibilidade dos links de navegação.
- [ ] **Seção Hero**:
  - [ ] Qualidade da imagem de fundo.
  - [ ] Presença do gradiente de sobreposição (`hero-overlay`).
  - [ ] Contraste do texto (Texto hero rosado).
- [ ] **Cards (Cursos)**:
  - [ ] Profundidade da sombra.
  - [ ] Cantos arredondados (border-radius consistente).
  - [ ] Proporção da imagem.

### Templates para Revisar

- `vedium_core/templates/base.html`
- `vedium_core/www/home.html`
- `vedium_core/www/courses/index.html`

## Descobertas

*(Registre discrepâncias aqui durante a revisão manual)*

- Nenhuma incompatibilidade encontrada ainda.
