#!/bin/bash

set -e

# Ruta para almacenar la clave privada temporalmente
SSH_DIR="/app/.ssh"
KEY_FILE="$SSH_DIR/id_ed25519"

# Asegura el directorio
mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

# Escribe la clave si existe la variable GH_SECRET
if [[ -n "$GH_SECRET" ]]; then
    echo "$GH_SECRET" > "$KEY_FILE"
    chmod 600 "$KEY_FILE"
    eval "$(ssh-agent -s)"
    ssh-add "$KEY_FILE"
else
    echo "⚠️  No se encontró GH_SECRET en el entorno. El acceso SSH a GitHub fallará si se usa."
fi

# Añade github.com a known_hosts para evitar problemas de autenticidad
ssh-keyscan github.com >> "$SSH_DIR/known_hosts" 2>/dev/null

# Lanza la aplicación principal
exec python server.py
