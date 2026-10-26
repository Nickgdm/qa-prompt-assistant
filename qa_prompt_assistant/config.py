import os
from pathlib import Path

APP_VERSION = '2.2.0'
DEFAULT_PROVIDER = 'gemini'
DEFAULT_MODELS = {
    'gemini': 'gemini-3.5-flash-lite',
    'openai_compatible': 'gpt-4o-mini',
    'ollama': 'llama3.2',
}
HISTORY_DIR = Path('historico')
EXPORT_DIR = Path('prompts_gerados')
STATE_FILE = HISTORY_DIR / 'uso_local.json'


def load_local_env():
    """Carrega variáveis do .env no diretório atual ou na raiz do projeto."""
    candidates = [Path.cwd() / '.env', Path(__file__).resolve().parent.parent / '.env']
    seen = set()
    for path in candidates:
        if not path.is_file() or path.resolve() in seen:
            continue
        seen.add(path.resolve())
        for raw in path.read_text(encoding='utf-8-sig').splitlines():
            line = raw.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key.startswith('export '):
                key = key[7:].strip()
            if key:
                os.environ.setdefault(key, value)


def get_provider():
    load_local_env()
    provider = os.getenv('AI_PROVIDER', DEFAULT_PROVIDER).strip().lower()
    aliases = {'openai': 'openai_compatible', 'compatible': 'openai_compatible', 'local': 'ollama', 'llama': 'ollama'}
    provider = aliases.get(provider, provider)
    return provider if provider in ('gemini', 'openai_compatible', 'ollama') else DEFAULT_PROVIDER


def get_model():
    load_local_env()
    provider = get_provider()
    env_model = os.getenv('AI_MODEL', '').strip()
    if not env_model and provider == 'gemini':
        env_model = os.getenv('GEMINI_MODEL', '').strip()  # compatibilidade com .env antigo
    return env_model or DEFAULT_MODELS[provider]


def get_api_key():
    load_local_env()
    provider = get_provider()
    if provider == 'gemini':
        value = os.getenv('GEMINI_API_KEY', '').strip() or os.getenv('AI_API_KEY', '').strip()
        return '' if value == 'COLOQUE_SUA_CHAVE_AQUI' else value
    value = os.getenv('AI_API_KEY', '').strip()
    return '' if value in ('COLOQUE_SUA_CHAVE_AQUI', 'SUA_CHAVE_AQUI') else value


def get_base_url():
    load_local_env()
    provider = get_provider()
    if provider == 'ollama':
        return os.getenv('AI_BASE_URL', '').strip() or 'http://localhost:11434/v1'
    return os.getenv('AI_BASE_URL', '').strip()
