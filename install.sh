#!/bin/bash

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MVR_PATH="$SCRIPT_DIR/mvr.py"

# Ensure ~/.local/bin exists
mkdir -p ~/.local/bin

# Create symlink
ln -sf "$MVR_PATH" ~/.local/bin/mvr

echo "✅ mvr installed to ~/.local/bin"
echo "Make sure ~/.local/bin is in your PATH to use 'mvr' from anywhere"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "⚠️  ~/.local/bin is not in your PATH"
    echo "Add this to your ~/.zshrc or ~/.bashrc:"
    echo 'export PATH="$HOME/.local/bin:$PATH"'
fi
