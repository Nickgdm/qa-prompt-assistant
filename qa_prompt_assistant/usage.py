import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from .config import STATE_FILE
try:
    from zoneinfo import ZoneInfo
    PACIFIC = ZoneInfo('America/Los_Angeles')
except Exception:
    PACIFIC = timezone(timedelta(hours=-8), name='PST estimado')

def _read(path=STATE_FILE):
    try: return json.loads(path.read_text(encoding='utf-8'))
    except (FileNotFoundError, json.JSONDecodeError, OSError): return {}

def record_call(path=STATE_FILE, provider="gemini"):
    now = datetime.now(PACIFIC); today = now.date().isoformat(); s = _read(path)
    if s.get('date_pacific') != today: s = {'date_pacific': today, 'calls_today_local': 0, 'calls_session': 0}
    s['calls_today_local'] = int(s.get('calls_today_local', 0)) + 1
    s['calls_session'] = int(s.get('calls_session', 0)) + 1
    s['providers'] = s.get('providers', {})
    s['providers'][provider] = int(s['providers'].get(provider, 0)) + 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding='utf-8')
    return s

def usage_snapshot(path=STATE_FILE):
    now = datetime.now(PACIFIC); s = _read(path)
    if s.get('date_pacific') != now.date().isoformat(): s = {'calls_today_local': 0, 'calls_session': 0}
    tomorrow = now.date() + timedelta(days=1)
    reset = datetime(tomorrow.year, tomorrow.month, tomorrow.day, tzinfo=PACIFIC)
    seconds = max(0, int((reset-now).total_seconds())); h, r = divmod(seconds, 3600); m, sec = divmod(r, 60)
    return {'calls_today_local': int(s.get('calls_today_local', 0)), 'calls_session': int(s.get('calls_session', 0)), 'reset_at': reset.strftime('%Y-%m-%d %H:%M %Z'), 'countdown': f'{h:02d}h {m:02d}m {sec:02d}s'}

def format_usage(model, provider='gemini'):
    s = usage_snapshot()
    return (f'Provedor configurado: {provider}\nModelo configurado: {model}\nChamadas registradas localmente hoje: {s["calls_today_local"]}\n'
            f'Chamadas registradas nesta sessão (contagem local persistida): {s["calls_session"]}\n'
            f'Redefinição diária de referência (horário do Pacífico): {s["reset_at"]}\nTempo até a redefinição de referência: {s["countdown"]}\n'
            'A contagem regressiva é apenas uma referência até a meia-noite do Pacífico; não indica quando o provedor libera a cota.\n'
            'Cota oficial restante e redefinição real: consulte o painel do provedor configurado.\n'
            'Os contadores locais não representam a cota oficial da API.')
