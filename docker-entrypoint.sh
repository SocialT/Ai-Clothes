#!/usr/bin/env sh
set -e

echo "[entrypoint] Ensuring Prisma client is generated..."
prisma generate

MIGRATIONS_DIR="/app/prisma/migrations"

if [ -d "$MIGRATIONS_DIR" ] && [ "$(ls -A $MIGRATIONS_DIR 2>/dev/null)" ]; then
  echo "[entrypoint] Running prisma migrate deploy..."
  prisma migrate deploy
else
  echo "[entrypoint] No migrations found. Running prisma db push to sync schema..."
  prisma db push --accept-data-loss
fi

echo "[entrypoint] Starting application: $@"
exec "$@"


