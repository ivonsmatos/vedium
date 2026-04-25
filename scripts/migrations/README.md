# Scripts de migração e diagnóstico (one-off)

Scripts utilitários usados para popular dados, inspecionar estado ou debugar
o ambiente de desenvolvimento. **Não rodam automaticamente** — são executados
manualmente via `bench --site SITE console < script.py` ou similar.

Mantenha este diretório para o histórico, mas não acrescente lógica
recorrente aqui — para isso, use `scheduler_events` em `hooks.py` ou comandos
do bench.

## Categorias

- `check_*.py`   — diagnósticos (rotas, metadados, configuração)
- `list_*.py`    — listagens de cursos/categorias
- `create_*.py`  — popular cursos/programas/termos
- `cleanup_*.py` — remoção de dados de teste
- `verify_*.py`  — validações pós-migração
- `setup_erp_requirements.py` — preparação inicial de DocTypes ERP
- `debug_site.py`, `test_query.py` — exploração ad-hoc
