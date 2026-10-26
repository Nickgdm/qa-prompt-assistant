from qa_prompt_assistant.utils import evaluate_prompt, save_history, save_prompt
from qa_prompt_assistant.usage import record_call, usage_snapshot

def test_evaluate_prompt_detects_missing_elements():
    score, suggestions = evaluate_prompt('Crie testes para um sistema de login.')
    assert 0 <= score <= 100
    assert any('formato de resposta' in item for item in suggestions)

def test_evaluate_prompt_complete():
    prompt = 'Contexto do sistema: login. Objetivo: crie casos de teste. Formato: tabela. Não invente regras. Valide o resultado esperado. Liste perguntas para esclarecer informações ausentes.'
    score, suggestions = evaluate_prompt(prompt)
    assert score == 100 and suggestions == []

def test_export_txt_and_markdown(tmp_path, monkeypatch):
    monkeypatch.setattr('qa_prompt_assistant.utils.EXPORT_DIR', tmp_path)
    txt = save_prompt('Casos de teste', 'Texto', 'txt')
    md = save_prompt('Casos de teste', 'Texto', 'md')
    assert txt.read_text(encoding='utf-8') == 'Texto\n'
    assert '# Casos de teste' in md.read_text(encoding='utf-8')

def test_history(tmp_path, monkeypatch):
    monkeypatch.setattr('qa_prompt_assistant.utils.HISTORY_DIR', tmp_path)
    path = save_history('QA', 'Prompt', 'Resposta')
    assert '## Resposta da IA' in path.read_text(encoding='utf-8')

def test_local_usage_count(tmp_path):
    state_file = tmp_path / 'usage.json'
    assert record_call(state_file)['calls_today_local'] == 1
    assert usage_snapshot(state_file)['calls_today_local'] == 1
