#!/bin/bash

# =============================================================================
# Vedium - Apps Installation Script
# =============================================================================
# Este script baixa e instala todos os apps necessários para o Vedium.
# Execute dentro da pasta vedium-bench após rodar init.sh
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SITE_NAME="vedium.localhost"
ADMIN_PASSWORD="admin"

echo -e "${BLUE}=============================================="
echo "  VEDIUM - Apps Installation"
echo "==============================================${NC}"
echo ""

# =============================================================================
# Step 1: Download Apps
# =============================================================================
echo -e "${YELLOW}[1/8] Downloading payments app...${NC}"
bench get-app payments

echo -e "${YELLOW}[2/8] Downloading ERPNext (version-15)...${NC}"
bench get-app erpnext --branch version-15

echo -e "${YELLOW}[3/8] Downloading LMS (version-15)...${NC}"
bench get-app lms --branch version-15

echo -e "${YELLOW}[4/8] Downloading Frappe Builder...${NC}"
bench get-app builder

# =============================================================================
# Step 2: Create Site
# =============================================================================
echo ""
echo -e "${YELLOW}[5/8] Creating site ${SITE_NAME}...${NC}"
bench new-site ${SITE_NAME} --admin-password ${ADMIN_PASSWORD} --force

# =============================================================================
# Step 3: Install Apps (Order matters for dependencies!)
# =============================================================================
echo ""
echo -e "${YELLOW}[6/8] Installing apps on ${SITE_NAME}...${NC}"

echo -e "  ${BLUE}→ Installing payments...${NC}"
bench --site ${SITE_NAME} install-app payments

echo -e "  ${BLUE}→ Installing erpnext...${NC}"
bench --site ${SITE_NAME} install-app erpnext

echo -e "  ${BLUE}→ Installing lms...${NC}"
bench --site ${SITE_NAME} install-app lms

echo -e "  ${BLUE}→ Installing builder...${NC}"
bench --site ${SITE_NAME} install-app builder

echo -e "  ${BLUE}→ Installing vedium_core...${NC}"
bench --site ${SITE_NAME} install-app vedium_core

# =============================================================================
# Step 4: Enable Developer Mode
# =============================================================================
echo ""
echo -e "${YELLOW}[7/8] Enabling developer mode...${NC}"
bench --site ${SITE_NAME} set-config developer_mode 1

# =============================================================================
# Step 5: Final Setup
# =============================================================================
echo ""
echo -e "${YELLOW}[8/8] Running migrations and building assets...${NC}"
bench --site ${SITE_NAME} migrate
bench build

# =============================================================================
# Done!
# =============================================================================
echo ""
echo -e "${GREEN}=============================================="
echo "  Installation Complete!"
echo "=============================================="
echo ""
echo "  Site: http://${SITE_NAME}:8000"
echo "  User: Administrator"
echo "  Password: ${ADMIN_PASSWORD}"
echo ""
echo "  Installed Apps:"
echo "    ✓ payments"
echo "    ✓ erpnext (v15)"
echo "    ✓ lms (v15)"
echo "    ✓ builder"
echo "    ✓ vedium_core"
echo ""
echo "  To start the development server, run:"
echo "    bench start"
echo "===============================================${NC}"
