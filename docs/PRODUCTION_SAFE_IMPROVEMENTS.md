# Melhorias seguras para produção — Vedium

Este pacote foi preparado considerando que `vediums.com` já está em produção, com Stripe ativo, alunos e professores cadastrados.

## O que este pacote faz

- Adiciona landing pages de SEO por objetivo/nicho, sem alterar banco de dados, DocTypes, permissões, checkout ou LMS.
- Atualiza `llms.txt` para refletir as novas páginas e corrigir o nível Upper Intermediário para B2.
- Inclui dados cadastrais da empresa no rodapé, Termos de Uso e Política de Privacidade.
- Mantém Stripe como processador de pagamentos descrito nos documentos públicos.

## O que este pacote não faz

- Não altera Nginx, deploy, Docker, CI/CD, `hooks.py`, `api.py` ou endpoints de pagamento.
- Não redireciona `app.vediums.com`.
- Não altera tabelas, fixtures, cadastros de alunos, professores, matrículas, assinaturas ou cursos.
- Não muda lógica de cobrança, webhook, checkout ou assinatura Stripe.

## Checklist antes de publicar

1. Aplicar em branch separada.
2. Rodar os testes puros de marketing.
3. Abrir PR e revisar arquivos alterados.
4. Publicar em janela segura, sem migration de banco.
5. Validar no site: novas landing pages, rodapé, Termos, Privacidade e CTAs de WhatsApp.
