#!/bin/bash

set -e


SSH_DIR="/root/.ssh"
KEY_FILE="$SSH_DIR/id_ed25519"

mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"


if [[ -n "$GH_SECRET" ]]; then
    echo "$GH_SECRET" > "$KEY_FILE"
    chmod 600 "$KEY_FILE"
fi


if [ -f "$KEY_FILE" ]; then
    chmod 600 "$KEY_FILE"
fi


if [ ! -f "$SSH_DIR/known_hosts" ] || ! grep -q "github.com" "$SSH_DIR/known_hosts"; then
    ssh-keyscan github.com >> "$SSH_DIR/known_hosts" 2>/dev/null
    chmod 644 "$SSH_DIR/known_hosts"
fi


eval "$(ssh-agent -s)"
ssh-add "$KEY_FILE"


exec python server.py
