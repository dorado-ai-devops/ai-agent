#!/bin/bash

set -e

# Usa siempre el home root para SSH en contenedores, es lo que espera git/ssh por defecto
SSH_DIR="/root/.ssh"
KEY_FILE="$SSH_DIR/id_ed25519"

mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

# Si GH_SECRET viene como variable (por ejemplo, como envFrom) la escribimos
if [[ -n "$GH_SECRET" ]]; then
    echo "$GH_SECRET" > "$KEY_FILE"
    chmod 600 "$KEY_FILE"
fi

# Si ya viene montada por volumen, asegura permisos (por seguridad, siempre)
if [ -f "$KEY_FILE" ]; then
    chmod 600 "$KEY_FILE"
fi

# Añade github.com a known_hosts si no existe
if [ ! -f "$SSH_DIR/known_hosts" ] || ! grep -q "github.com" "$SSH_DIR/known_hosts"; then
    ssh-keyscan github.com >> "$SSH_DIR/known_hosts" 2>/dev/null
    chmod 644 "$SSH_DIR/known_hosts"
fi

# (Opcional) Arranca ssh-agent solo si vas a hacer múltiples git/ssh en background (no necesario para subprocess git)
# eval "$(ssh-agent -s)"
# ssh-add "$KEY_FILE"

# Lanza la aplicación principal
exec python server.py
