# Multi-tenant

O SCSI usa banco compartilhado com isolamento lógico por corretora.

Regras obrigatórias:

- Toda entidade de negócio herda de `BrokerageModel` ou mantém vínculo equivalente com `Brokerage`.
- Toda listagem usa `queryset.for_brokerage(request.brokerage)`.
- Toda CBV interna deve receber o tenant por `CurrentBrokerageMiddleware`.
- Forms filtram FKs com `BrokerageScopedFormMixin`.
- Admin operacional filtra querysets e FKs por corretora com `TenantAdminMixin`.
- IDs vindos de URL ou formulário são revalidados contra `request.brokerage`.
- Cache de dados de negócio deve incluir `brokerage_id` na chave.
