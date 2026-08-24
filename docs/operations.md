# Operações

- `python manage.py seed_demo` cria dados fake identificáveis como demonstração.
- `scripts/backup.sh` gera backup PostgreSQL e media com rotação.
- Verifique `/health/`, logs de `app`, `celery_worker`, `celery_beat` e emissão TLS após deploy.
- Restaurar backup exige pausar app, restaurar banco/media, validar permissões e reativar serviços.
