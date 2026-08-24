from django.conf import settings

from .tools import build_entity_context, tenant_snapshot


def build_summary(entity_type, entity):
    context = build_entity_context(entity_type, entity)
    if not settings.OPENAI_API_KEY:
        return f'## Resumo automático\n\n{context}\n\n## Observação\n\nOPENAI_API_KEY não configurada. Este resumo foi gerado localmente com os dados autorizados da corretora.'
    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        return f'## Resumo automático\n\n{context}\n\n## Observação\n\nLangChain/OpenAI ainda não estão instalados neste ambiente.'
    llm = ChatOpenAI(model=settings.OPENAI_MODEL, api_key=settings.OPENAI_API_KEY, timeout=30)
    response = llm.invoke(f'Responda em português brasileiro, em Markdown, resumindo apenas estes dados autorizados:\n{context}')
    return response.content


def answer_chat(brokerage, question):
    snapshot = tenant_snapshot(brokerage)
    if not settings.OPENAI_API_KEY:
        return '## Resposta\n\nRecebi sua pergunta. Configure `OPENAI_API_KEY` para respostas completas.\n\n### Dados autorizados disponíveis\n\n' + '\n'.join(f'- {key}: {value}' for key, value in snapshot.items())
    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        return '## Resposta\n\nLangChain/OpenAI ainda não estão instalados neste ambiente.'
    llm = ChatOpenAI(model=settings.OPENAI_MODEL, api_key=settings.OPENAI_API_KEY, timeout=30)
    response = llm.invoke(f'Use apenas este resumo tenant-aware: {snapshot}. Pergunta: {question}')
    return response.content
