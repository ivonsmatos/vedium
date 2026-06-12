# =============================================================
# Vedium — Makefile
# =============================================================
# Uso: make <target>
#   make up          → Sobe todos os containers de produção
#   make down        → Para e remove containers
#   make logs        → Tail de todos os logs
#   make shell       → Shell dentro do container frappe
#   make migrate     → Executa migrações pendentes (bench migrate)
#   make backup      → Dispara backup manual via restic
#   make restore     → Restaura último snapshot (interativo)
#   make status      → Status resumido dos containers + health
#   make workers     → Ver status dos workers/scheduler
#   make ps          → docker compose ps
# =============================================================

COMPOSE      := docker compose -f deploy/docker-compose.yml
COMPOSE_OBS  := $(COMPOSE) --profile observability
FRAPPE_CTR   := vedium-frappe
SITE         := $(shell grep FRAPPE_SITE_NAME deploy/.env 2>/dev/null | cut -d= -f2 | tr -d '"' | head -1)
SITE         := $(if $(SITE),$(SITE),app.vediums.com)

.DEFAULT_GOAL := help

.PHONY: help up down restart logs logs-frappe logs-workers shell migrate backup restore \
        status workers ps clean uptime-up uptime-down health lint test

# ------------------------------------------------------------------
help:
	@echo ""
	@echo "  Vedium — comandos disponíveis"
	@echo "  ─────────────────────────────"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	    awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ------------------------------------------------------------------
up: ## Sobe todos os containers em background
	$(COMPOSE) up -d
	@echo "Aguardando healthchecks..."
	@sleep 5
	@$(MAKE) status

down: ## Para e remove containers (volumes são preservados)
	$(COMPOSE) down

restart: ## Reinicia todos os containers
	$(COMPOSE) restart
	@$(MAKE) status

# ------------------------------------------------------------------
logs: ## Tail de todos os logs (Ctrl+C para sair)
	$(COMPOSE) logs -f --tail=100

logs-frappe: ## Logs apenas do container frappe
	$(COMPOSE) logs -f --tail=100 vedium-frappe

logs-workers: ## Logs dos workers e scheduler
	$(COMPOSE) logs -f --tail=50 \
	    vedium-worker-default vedium-worker-short vedium-worker-long vedium-scheduler

# ------------------------------------------------------------------
shell: ## Shell bash dentro do container frappe
	$(COMPOSE) exec $(FRAPPE_CTR) bash

bench: ## bench console interativo (frappe shell)
	$(COMPOSE) exec $(FRAPPE_CTR) \
	    /home/frappe/frappe-bench/env/bin/bench --site $(SITE) console

# ------------------------------------------------------------------
migrate: ## Executa bench migrate no site configurado
	@echo "Executando migrações para site: $(SITE)"
	$(COMPOSE) exec $(FRAPPE_CTR) \
	    /home/frappe/frappe-bench/env/bin/bench --site $(SITE) migrate

build-assets: ## Rebuild assets Frappe (CSS/JS)
	$(COMPOSE) exec $(FRAPPE_CTR) \
	    /home/frappe/frappe-bench/env/bin/bench build --app vedium_core

clear-cache: ## Limpa cache Frappe
	$(COMPOSE) exec $(FRAPPE_CTR) \
	    /home/frappe/frappe-bench/env/bin/bench --site $(SITE) clear-cache

# ------------------------------------------------------------------
backup: ## Dispara backup manual via restic
	@echo "Iniciando backup manual..."
	@bash deploy/scripts/backup.sh

restore: ## Restaura último snapshot (interativo)
	@bash deploy/scripts/restore.sh

restore-list: ## Lista snapshots restic disponíveis
	@bash deploy/scripts/restore.sh --list

# ------------------------------------------------------------------
status: ## Status e health de todos os containers
	@echo ""
	@echo "  Container                       Status      Health"
	@echo "  ─────────────────────────────────────────────────"
	@docker ps --filter name=vedium --format \
	    "  {{.Names}}\t{{.Status}}" | column -t
	@echo ""

workers: ## Status dos workers Frappe via Redis queue
	@echo "=== Filas Redis (vedium-redis-queue) ==="
	@docker exec vedium-redis-queue redis-cli llen frappe:default || true
	@docker exec vedium-redis-queue redis-cli llen frappe:short    || true
	@docker exec vedium-redis-queue redis-cli llen frappe:long     || true
	@echo ""
	@$(COMPOSE) ps vedium-worker-default vedium-worker-short vedium-worker-long vedium-scheduler

ps: ## docker compose ps completo
	$(COMPOSE) ps

health: ## Testa /api/method/ping do Frappe
	@echo "Testando https://app.vediums.com/api/method/ping..."
	@curl -sf https://app.vediums.com/api/method/ping | python3 -m json.tool || \
	    echo "FALHOU — servidor pode estar reiniciando"
	@echo "Testando localhost (porta 8005)..."
	@curl -sf http://localhost:8005/api/method/ping | python3 -m json.tool || \
	    echo "FALHOU — container pode não estar rodando"

# ------------------------------------------------------------------
uptime-up: ## Sobe Uptime Kuma (monitoramento simples — localhost:3004)
	$(COMPOSE_OBS) up -d vedium-uptime-kuma

uptime-down: ## Para Uptime Kuma
	$(COMPOSE_OBS) stop vedium-uptime-kuma

# ------------------------------------------------------------------
clean: ## Remove volumes não utilizados (CUIDADO: irreversível)
	@echo "⚠️  Isso vai remover volumes Docker não utilizados."
	@read -p "Confirmar? (s/N): " c; [ "$$c" = "s" ] || exit 1
	docker volume prune -f

# ------------------------------------------------------------------
lint: ## Lint Python (flake8 + black --check)
	@cd vedium_core && \
	    python -m flake8 vedium_core/ --max-line-length=120 && \
	    python -m black --check vedium_core/

test: ## Roda suite de testes Python
	@cd vedium_core && \
	    python -m pytest vedium_core/tests/ -v

# ------------------------------------------------------------------
# Setup inicial do servidor (executar uma vez)
# ------------------------------------------------------------------
server-init: ## Configuração inicial do servidor (idempotente)
	@echo "Configurando servidor..."
	@bash deploy/scripts/deploy.sh

ssl: ## Ativar/renovar certificado TLS
	@bash deploy/scripts/ativar-ssl.sh