# Deploy

Produção usa Docker Swarm com imagem `ghcr.io/pycodebr/scsi_v1:latest`, Traefik, Cloudflare DNS-01 e redes separadas.

Comandos principais:

```bash
docker network create --driver overlay --attachable traefik_public
docker network create --driver overlay --attachable --internal scsi_v1_internal
docker network create --driver overlay --attachable scsi_v1_egress
./scripts/deploy.sh
./scripts/deploy.sh --skip-build
```

O app roda migrations com advisory lock e `collectstatic --clear`. Celery usa entrypoint separado e não roda migrations nem collectstatic.
