#!/usr/bin/env sh
set -eu

IMAGE="ghcr.io/pycodebr/scsi_v1:latest"
SKIP_BUILD=0

if [ "${1:-}" = "--skip-build" ]; then
    SKIP_BUILD=1
fi

load_env() {
    while IFS= read -r line || [ -n "$line" ]; do
        case "$line" in ''|'#'*) continue ;; esac
        key=${line%%=*}
        value=${line#*=}
        case "$key" in *[!A-Za-z0-9_]*|'') continue ;; esac
        export "$key=$value"
    done < .env
}

[ -f .env ] && load_env
docker info --format '{{.Swarm.LocalNodeState}}' | grep -q active
docker secret inspect CLOUDFLARE_DNS_API_TOKEN >/dev/null
docker network inspect traefik_public >/dev/null
docker network inspect scsi_v1_egress >/dev/null || docker network create --driver overlay --attachable scsi_v1_egress
test "${DEBUG:-False}" = "False"
printf '%s' "${ALLOWED_HOSTS:-}" | grep -q 'localhost'

git pull --ff-only
if [ "$SKIP_BUILD" -eq 0 ]; then
    docker build -t "$IMAGE" .
    docker push "$IMAGE"
fi
docker stack deploy --with-registry-auth -c docker-stack.yml scsi_v1
docker service update --force scsi_v1_app
docker service update --force scsi_v1_celery_worker
docker service update --force scsi_v1_celery_beat
