# Segurança

- Rotas internas exigem autenticação.
- Views, forms, admin, relatórios, anexos e IA filtram por corretora.
- Arquivos privados são baixados apenas por view autenticada.
- `.env` é gitignored e produção usa Docker Secrets.
- `/health/` não acessa banco e é isento de redirect HTTPS.
- Markdown da IA é sanitizado com `bleach` quando instalado.
