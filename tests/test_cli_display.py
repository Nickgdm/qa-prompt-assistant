from qa_prompt_assistant.cli import terminal_width, MENU

def test_menu_has_seven_qa_activities():
    assert len(MENU) == 7
    assert "Criar casos de teste" in [item[0] for item in MENU.values()]

def test_terminal_width_is_reasonable():
    assert 50 <= terminal_width() <= 100
