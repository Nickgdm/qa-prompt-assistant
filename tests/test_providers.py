from qa_prompt_assistant.config import get_base_url, get_model, get_provider


def test_provider_aliases(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "llama")
    assert get_provider() == "ollama"


def test_ollama_defaults(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "ollama")
    monkeypatch.delenv("AI_MODEL", raising=False)
    monkeypatch.delenv("AI_BASE_URL", raising=False)
    assert get_model() == "llama3.2"
    assert get_base_url() == "http://localhost:11434/v1"


def test_openai_compatible_configuration(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "openai_compatible")
    monkeypatch.setenv("AI_MODEL", "custom-model")
    monkeypatch.setenv("AI_BASE_URL", "https://example.invalid/v1")
    assert get_provider() == "openai_compatible"
    assert get_model() == "custom-model"
    assert get_base_url() == "https://example.invalid/v1"
