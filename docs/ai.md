# Inteligência Artificial

Resumos são processados por Celery recebendo `brokerage_id`, `user_id`, `entity_type` e `entity_id`. Tools carregam entidades apenas via `for_brokerage`.

O chat salva sessões e mensagens por usuário e corretora. Respostas são Markdown e renderizadas de forma sanitizada quando as dependências estão instaladas.

O modelo padrão é `GPT-5.5-mini` via `OPENAI_MODEL`.
