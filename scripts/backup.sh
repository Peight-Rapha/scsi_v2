#!/usr/bin/env sh
set -eu

BACKUP_DIR=${BACKUP_DIR:-/opt/scsi_v1/backups}
RETENTION_DAYS=${RETENTION_DAYS:-14}
STAMP=$(date +%Y%m%d-%H%M%S)

mkdir -p "$BACKUP_DIR"
docker exec "$(docker ps --filter name=scsi_v1_postgresql -q | head -n 1)" pg_dump -U scsi scsi > "$BACKUP_DIR/postgresql-$STAMP.sql"
docker run --rm -v scsi_v1_media:/media:ro -v "$BACKUP_DIR:/backup" alpine tar czf "/backup/media-$STAMP.tar.gz" /media
find "$BACKUP_DIR" -type f -mtime +"$RETENTION_DAYS" -delete
