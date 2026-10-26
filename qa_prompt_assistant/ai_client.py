from .config import get_api_key, get_base_url, get_model, get_provider
from .usage import record_call


class AIConfigurationError(RuntimeError):
    pass


class AIRequestError(RuntimeError):
    pass


def _qa_instructions(prompt):
    return (
        'Você é um assistente de Quality Assurance. Responda em português brasileiro, com clareza e estrutura. '
        'Não invente requisitos ou regras de negócio; diferencie fatos, hipóteses e recomendações. '
        'Use títulos, listas e exemplos quando ajudarem. Oriente o usuário a validar criticamente a resposta.\n\n'
        'Solicitação:\n' + prompt
    )


def ask_ai(prompt):
    provider = get_provider()
    model = get_model()
    key = get_api_key()
    base_url = get_base_url()
    request = _qa_instructions(prompt)
    try:
        if provider == 'gemini':
            if not key:
                raise AIConfigurationError('Chave ausente. Configure GEMINI_API_KEY no .env, ou escolha outro provedor em AI_PROVIDER.')
            from google import genai
            client = genai.Client(api_key=key)
            response = client.models.generate_content(model=model, contents=request)
            answer = (getattr(response, 'text', None) or '').strip()
        else:
            try:
                from openai import OpenAI
            except ImportError as exc:
                raise AIConfigurationError('SDK OpenAI-compatible ausente. Execute: py -m pip install -r requirements.txt') from exc
            if provider == 'openai_compatible' and not key:
                raise AIConfigurationError('Falta AI_API_KEY no .env para o provedor de API escolhido. Use a chave fornecida por esse serviço.')
            # Ollama local normalmente não exige chave; esse valor fictício não é enviado como segredo real.
            client_args = {'api_key': key or 'ollama'}
            if base_url:
                client_args['base_url'] = base_url
            client = OpenAI(**client_args)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {'role': 'system', 'content': 'Você é um assistente de Quality Assurance que responde em português brasileiro.'},
                    {'role': 'user', 'content': request},
                ],
            )
            answer = (response.choices[0].message.content or '').strip()
        if not answer:
            answer = 'A IA não retornou texto. Tente reformular a solicitação.'
        record_call(provider=provider)
        return answer, model
    except AIConfigurationError:
        raise
    except Exception as exc:
        msg = str(exc)
        lower = msg.lower()
        if '429' in msg or 'resource_exhausted' in lower or 'rate limit' in lower:
            raise AIRequestError(f'Limite de uso do provedor atingido (429). Consulte o painel e os limites do serviço configurado.\n{msg}') from exc
        if '401' in msg or '403' in msg or 'unauthorized' in lower or 'permission_denied' in lower or 'api key' in lower:
            raise AIRequestError(f'Falha de autenticação/permissão. Confira a chave, o modelo e o acesso do provedor configurado.\n{msg}') from exc
        if provider == 'ollama' and ('connection' in lower or 'connect' in lower or 'refused' in lower):
            raise AIRequestError('Não foi possível conectar ao Ollama local. Confirme que o Ollama está instalado e em execução, e que o modelo foi baixado com `ollama pull NOME_DO_MODELO`.\n' + msg) from exc
        raise AIRequestError(f'Falha ao consultar o provedor {provider} ({type(exc).__name__}): {msg}') from exc


def ask_gemini(prompt):
    """Alias legado mantido para compatibilidade com versões anteriores."""
    return ask_ai(prompt)
