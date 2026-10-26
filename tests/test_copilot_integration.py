from unittest.mock import Mock, patch
from qa_prompt_assistant import cli


def test_send_to_vscode_copilot_uses_chat_stdin():
    completed = Mock(returncode=0)
    with patch.object(cli.shutil, 'which', return_value='/usr/bin/code'), \
         patch.object(cli.subprocess, 'run', return_value=completed) as run:
        assert cli.send_to_vscode_copilot('prompt de teste') is True
    args, kwargs = run.call_args
    assert args[0] == ['/usr/bin/code', 'chat', '-']
    assert kwargs['input'] == 'prompt de teste'
    assert kwargs['text'] is True


def test_send_to_vscode_copilot_handles_missing_cli():
    with patch.object(cli.shutil, 'which', return_value=None):
        assert cli.send_to_vscode_copilot('prompt') is False
