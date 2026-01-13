#!/bin/bash

# =============================================================================
# Vedium - Tailwind CSS Installation Script
# =============================================================================
# Execute dentro de: vedium-bench/apps/vedium_core
# =============================================================================

set -e

echo "=============================================="
echo "  Installing Tailwind CSS for Vedium"
echo "=============================================="

# Initialize npm project if not exists
if [ ! -f "package.json" ]; then
    echo "Initializing npm project..."
    npm init -y
fi

# Install Tailwind CSS and dependencies
echo "Installing Tailwind CSS..."
npm install -D tailwindcss postcss autoprefixer

# Initialize Tailwind config
echo "Initializing Tailwind config..."
npx tailwindcss init -p

echo ""
echo "=============================================="
echo "  Tailwind CSS Installed!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "  1. Update tailwind.config.js with Vedium theme"
echo "  2. Create input.css with @tailwind directives"
echo "  3. Run: npx tailwindcss -i ./input.css -o ./vedium_core/public/css/vedium.css --watch"
echo "=============================================="
