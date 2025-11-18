#!/bin/bash

# === Configuración ===
USER="mcantu"               # Usuario en el servidor Debian
HOST="dev.tech-reok.lan"            # IP o dominio del servidor
PORT="22"                       # Puerto SSH (por defecto 22)
REMOTE_DIR="/home/mcantu/devs/firmatika-api"   # Carpeta destino en el servidor

# === Uso ===
# ./sync_folder.sh carpeta_local
# Copiará la carpeta completa al servidor en REMOTE_DIR

if [ $# -eq 0 ]; then
  echo "Uso: $0 carpeta_local"
  exit 1
fi

LOCAL_DIR="$1"

# remover los archivos actuales en el servidor
echo "🗑️ Limpiando carpeta remota $USER@$HOST:$REMOTE_DIR"
ssh -p $PORT "$USER@$HOST" "rm -rf $REMOTE_DIR/* && rm -rf  $REMOTE_DIR/firmatika-blockchain/*"

echo "Copy blockchain files to server"
rsync -avz -e "ssh -p $PORT" "../firmatika-blockchain/artifacts" "$USER@$HOST:$REMOTE_DIR/firmatika-blockchain/"

echo "📂 Sincronizando $LOCAL_DIR → $USER@$HOST:$REMOTE_DIR ..."
rsync -avz -e "ssh -p $PORT" "$LOCAL_DIR" "$USER@$HOST:$REMOTE_DIR"

echo "✅ Transferencia completada."

cd "$REMOTE_DIR"
echo "🚀 Desplegando la aplicación en el servidor.."
ssh -p $PORT "$USER@$HOST" "cd $REMOTE_DIR && docker compose down && docker compose up -d --build"
echo "✅ Despliegue completado."