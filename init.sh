#!/bin/bash

# =============================================================================
# Vedium - Frappe v15 Initialization Script
# =============================================================================

set -e

echo "=============================================="
echo "  VEDIUM - Frappe v15 Initialization"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Initialize Frappe Bench
echo -e "${YELLOW}[1/3] Initializing Frappe Bench...${NC}"
bench init --skip-redis-config-generation --frappe-branch version-15 vedium-bench

# Step 2: Navigate to bench directory
echo -e "${YELLOW}[2/3] Entering vedium-bench directory...${NC}"
cd vedium-bench

# Step 3: Create vedium_core app
echo -e "${YELLOW}[3/3] Creating vedium_core app...${NC}"
bench new-app vedium_core

echo ""
echo -e "${GREEN}=============================================="
echo "  Initialization Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "  1. cd vedium-bench/apps/vedium_core"
echo "  2. Follow GIT_WORKFLOW.md to connect to GitHub"
echo "  3. bench new-site vedium.localhost"
echo "  4. bench --site vedium.localhost install-app vedium_core"
echo "===============================================${NC}"
