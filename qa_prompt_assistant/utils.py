from datetime import datetime
from pathlib import Path
import re
from .config import EXPORT_DIR, HISTORY_DIR

def ask_non_empty(question):
    while True:
        value = input(question).strip()
        if value: return value
        print("A resposta não pode ficar vazia. Se não souber, digite 'Não sei'.")

def ask_optional(question, default='Não informado'):
    return input(question).strip() or default

def ask_choice(question, options):
    while True:
        value = input(question).strip()
        if value in options: return value
        print('Opção inválida. Escolha: ' + ', '.join(options))

def evaluate_prompt(prompt):
    checks = {
        'contexto': r'\b(contexto|sistema|funcionalidade|requisito|aplica[cç][aã]o)\b',
        'objetivo': r'\b(objetivo|preciso|quero|crie|analise|elabore|ajude)\b',
        'formato de resposta': r'\b(tabela|lista|formato|estrutura|markdown|json)\b',
        'restrições': r'\b(n[aã]o invente|restri[cç][oõ]es|limita[cç][oõ]es|n[aã]o assuma)\b',
        'critérios/validação': r'\b(resultado esperado|crit[eé]rios|valid[eá]|verific[aá]vel|casos de borda)\b',
        'lacunas/perguntas': r'\b(ambigu|informa[cç][oõ]es ausentes|perguntas|esclarecer|faltantes)\b',
    }
    lower = prompt.lower(); missing = [name for name, pattern in checks.items() if not re.search(pattern, lower)]
    return round((len(checks)-len(missing))*100/len(checks)), [f'Considere incluir: {x}.' for x in missing]

def save_prompt(title, prompt, extension='txt'):
    EXPORT_DIR.mkdir(parents=True, exist_ok=True); safe = ''.join(c.lower() if c.isalnum() else '_' for c in title).strip('_') or 'prompt'; stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = EXPORT_DIR / f'{safe}_{stamp}.{extension}'
    content = f'# {title}\n\n```text\n{prompt}\n```\n' if extension == 'md' else prompt.rstrip()+'\n'
    path.write_text(content, encoding='utf-8'); return path

def save_history(title, prompt, answer=''):
    HISTORY_DIR.mkdir(parents=True, exist_ok=True); stamp = datetime.now().strftime('%Y%m%d_%H%M%S'); path = HISTORY_DIR / f'{stamp}_{title.lower().replace(" ", "_")}.md'
    content = f'# {title}\n\n**Data local:** {datetime.now().isoformat(timespec="seconds")}\n\n## Prompt\n\n{prompt}\n\n'
    if answer: content += f'## Resposta da IA\n\n{answer}\n'
    path.write_text(content, encoding='utf-8'); return path

def list_history(): return sorted(HISTORY_DIR.glob('*.md'), reverse=True) if HISTORY_DIR.exists() else []
