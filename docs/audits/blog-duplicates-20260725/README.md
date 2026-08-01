# Auditoria de duplicidade do blog Vedium

Data: 25/07/2026  
Modo: dry run, somente leitura

## Resultado

- 97 artigos no catálogo versionado.
- 130 cards coletados em 11 páginas da listagem ao vivo.
- 124 URLs únicas e 100 títulos normalizados únicos.
- 31 componentes duplicados, equivalentes a 31 cards excedentes.
- 56 URLs duplicadas verificadas; todas responderam HTTP 200.
- Nenhum dos 31 grupos apresentou divergência de hash entre as URLs renderizadas.
- 50 das 56 URLs usam canonical diferente da arquitetura do catálogo.
- 25 aliases são candidatos provisórios a 301.
- 6 grupos repetem exatamente o mesmo `href` na listagem.
- 3 títulos contêm metadado de importação ou extensão de arquivo.
- 4 pares de possível canibalização permanecem como `REVISÃO HUMANA`.

## Causa técnica confirmada

O controlador Frappe do artigo consulta o conteúdo apenas pelo `slug`. Ele não
valida se a categoria e o idioma presentes na URL correspondem à rota canônica
do artigo. Uma rota com categoria inexistente retornou HTTP 200 e o mesmo
conteúdo, comprovando que aliases arbitrários podem ser renderizados.

A branch atual já contém uma proteção para priorizar artigos versionados sobre
cópias do banco na listagem. Essa mudança ainda não aparece no site ao vivo
auditado.

## Bloqueios

Nenhuma exclusão, alteração de banco ou regra 301 foi aplicada.

O prompt exige backup completo do banco antes dessas ações. Este checkout não
possui `bench`, configuração de site ou cliente MariaDB, e o daemon Docker não
está disponível. Também faltam dados do Google Search Console e backlinks,
necessários para preservar a URL de maior valor de SEO.

Foram produzidos e verificados:

- bundle completo do histórico Git;
- ZIP completo dos arquivos do projeto;
- inventário do catálogo versionado;
- listagem e sitemap ao vivo;
- hashes e verificações HTTP/canonical;
- plano de redirecionamento bloqueado;
- relatório de links internos;
- matriz de revisão humana.

Os backups ficam em:

`C:\Users\ivonm\Downloads\vedium_blog_dedup_backup_20260725_174037`

## Evidências

- [Resumo da auditoria](summary.json)
- [Inventário de artigos](article_inventory.csv)
- [Cards da listagem ao vivo](live_blog_cards.csv)
- [Grupos duplicados](duplicate_groups.csv)
- [Verificações HTTP e canonical](duplicate_url_checks.csv)
- [Plano provisório de redirecionamentos](redirect_dry_run.csv)
- [Sitemap ao vivo](live_sitemap_blog_urls.csv)
- [Anomalias de título](title_anomalies.csv)
- [Duplicados exatos no catálogo](exact_content_duplicates.csv)
- [Duplicados próximos no catálogo](near_content_duplicates.csv)
- [Canibalização para revisão humana](cannibalization_review.csv)
- [Links internos para aliases](internal_links_to_duplicate_urls.csv)
- [Artefato validado do relatório](artifact.json)

## Próxima etapa

1. Gerar e testar um backup restaurável do banco de produção.
2. Exportar os registros de artigos com IDs internos, idioma, categoria,
   publicação e slug.
3. Exportar Search Console e backlinks por URL.
4. Aprovar a matriz de URL principal e os quatro pares de canibalização.
5. Só então implementar 301, validação de rota, correção dos títulos,
   despublicação das cópias confirmadas, sitemap/cache e testes finais.
