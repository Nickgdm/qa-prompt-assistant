import os
import shutil
import subprocess
import textwrap

from . import __version__
from .ai_client import AIConfigurationError, AIRequestError, ask_ai
from .config import get_model, get_provider, load_local_env
from .prompts import (
    build_test_cases_prompt, build_requirements_prompt, build_bug_prompt,
    build_api_prompt, build_automation_prompt, build_freeform_prompt,
    build_ai_question_prompt,
)
from .usage import format_usage
from .utils import ask_choice, evaluate_prompt, list_history, save_history, save_prompt


def clear_screen():
    """Limpa a tela em terminais convencionais do Windows, macOS e Linux."""
    os.system('cls' if os.name == 'nt' else 'clear')


def terminal_width():
    """Retorna uma largura confortável, mesmo em terminais estreitos."""
    return max(50, min(shutil.get_terminal_size((88, 24)).columns, 100))


def line(char='─'):
    print(char * terminal_width())


def banner():
    clear_screen()
    width = min(terminal_width(), 76)
    print('╔' + '═' * (width - 2) + '╗')
    for text in ['🧪 QA PROMPT ASSISTANT', f'Versão {__version__}  •  Seu apoio prático para atividades de QA']:
        inner = text[:width - 4]
        print('║ ' + inner.center(width - 4) + ' ║')
    print('╠' + '═' * (width - 2) + '╣')
    for text in [
        'Crie prompts melhores, organize suas ideias e consulte a IA',
        'com orientações guiadas, exemplos e linguagem simples.',
    ]:
        print('║ ' + text[:width - 4].ljust(width - 4) + ' ║')
    print('╚' + '═' * (width - 2) + '╝')
    print(f'  Provedor: {get_provider()}  •  Modelo: {get_model()}')
    print('  Dica: você pode preparar e exportar prompts mesmo sem chamar a IA.')


MENU = {
    '1': ('Criar casos de teste', build_test_cases_prompt),
    '2': ('Analisar requisito', build_requirements_prompt),
    '3': ('Revisar relato de bug', build_bug_prompt),
    '4': ('Criar cenários de teste de API', build_api_prompt),
    '5': ('Planejar automação de testes', build_automation_prompt),
    '6': ('Aprimorar ideia ou prompt livre', build_freeform_prompt),
    '7': ('Perguntar diretamente à IA sobre QA', build_ai_question_prompt),
}


def print_wrapped(text, indent='  '):
    """Imprime texto longo com quebra de linha sem destruir blocos de código/tabelas."""
    width = max(40, terminal_width() - len(indent) - 1)
    in_code = False
    for raw_line in str(text).replace('\r\n', '\n').replace('\r', '\n').split('\n'):
        stripped = raw_line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            print(indent + raw_line)
            continue
        if not stripped:
            print()
        elif in_code or stripped.startswith('|') or len(stripped) <= width and stripped.startswith(('http://', 'https://')):
            print(indent + raw_line)
        else:
            # Mantém listas e títulos visualmente alinhados quando a linha quebra.
            prefix = ''
            body = raw_line.lstrip()
            for marker in ('### ', '## ', '# ', '- ', '* ', '• '):
                if body.startswith(marker):
                    prefix, body = marker, body[len(marker):]
                    break
            wrapped = textwrap.fill(
                body, width=width, initial_indent=prefix,
                subsequent_indent=' ' * len(prefix), break_long_words=True,
                break_on_hyphens=False,
            )
            for wrapped_line in wrapped.splitlines() or ['']:
                print(indent + wrapped_line)



def send_to_vscode_copilot(prompt):
    """Abre o GitHub Copilot Chat no VS Code com o prompt via stdin.

    O comando `code chat -` é suportado por versões compatíveis do VS Code.
    Não envia credenciais nem usa uma API própria do Copilot.
    """
    executable = shutil.which('code')
    if not executable:
        print_wrapped(
            'Não encontrei o comando `code` no PATH. Instale/ative a CLI do VS Code. '
            'Como alternativa, use [3] para copiar o prompt e cole-o no Copilot Chat.'
        )
        return False
    try:
        result = subprocess.run(
            [executable, 'chat', '-'],
            input=prompt, text=True, encoding='utf-8', check=False,
        )
        if result.returncode == 0:
            print_wrapped('O comando do VS Code foi iniciado. Confira o Copilot Chat e envie a mensagem se necessário.')
            return True
        print_wrapped(f'O VS Code retornou o código {result.returncode}. Tente copiar o prompt manualmente.')
        return False
    except (OSError, subprocess.SubprocessError) as exc:
        print_wrapped(f'Não foi possível abrir o Copilot Chat: {exc}')
        return False


def copy_to_clipboard(text):
    """Copia texto usando ferramentas comuns dos sistemas operacionais."""
    try:
        if os.name == 'nt':
            subprocess.run(['clip'], input=text, text=True, encoding='utf-8', check=True)
        elif shutil.which('pbcopy'):
            subprocess.run(['pbcopy'], input=text, text=True, encoding='utf-8', check=True)
        elif shutil.which('xclip'):
            subprocess.run(['xclip', '-selection', 'clipboard'], input=text, text=True, encoding='utf-8', check=True)
        elif shutil.which('wl-copy'):
            subprocess.run(['wl-copy'], input=text, text=True, encoding='utf-8', check=True)
        else:
            return False
        return True
    except (OSError, subprocess.SubprocessError):
        return False


def pause(message='Pressione Enter para voltar ao menu...'):
    input(f'\n{message}')


def show_usage():
    line()
    print('INDICADORES DE USO')
    line()
    print_wrapped(format_usage(get_model(), get_provider()))
    print_wrapped('Observação: os registros locais não representam a cota oficial restante da API.')
    print('Consulte os limites e o painel oficial do provedor configurado.')


def show_tutorial():
    line('═')
    print('COMO USAR — GUIA RÁPIDO')
    line('═')
    steps = [
        ('1. Escolha uma atividade', 'No menu, selecione casos de teste, análise de requisito, relato de bug, API, automação ou uma pergunta livre.'),
        ('2. Responda às perguntas', 'O programa fará perguntas curtas para entender seu contexto. Use informações fictícias se estiver aprendendo.'),
        ('3. Confira o prompt', 'Antes de enviar, você verá o texto preparado pelo programa e algumas sugestões locais de melhoria.'),
        ('4. Escolha onde usar o prompt', 'Você pode consultar a IA configurada por API, abrir o GitHub Copilot Chat no VS Code ou copiar o prompt para colar em outra ferramenta.'),
        ('5. Leia a resposta', 'A resposta da IA aparecerá em uma seção própria. As perguntas de salvar/exportar exibidas depois são opções do programa, não da IA.'),
        ('6. Salve o que for útil', 'Você pode guardar o prompt e a resposta no histórico local ou exportar o prompt para usar depois.'),
        ('7. Proteja seus dados', 'Nunca compartilhe sua chave API nem envie senhas, tokens, dados pessoais ou informações confidenciais.'),
    ]
    for title, body in steps:
        print(f'\n{title}')
        print_wrapped(body, indent='    ')
    print('\nPRIMEIRO USO')
    print_wrapped('Configure AI_PROVIDER e as variáveis necessárias no arquivo .env; depois instale as dependências com: py -m pip install -r requirements.txt')
    print_wrapped('Depois execute: py main.py')


def show_examples():
    line('═')
    print('EXEMPLOS PRÁTICOS')
    line('═')
    examples = [
        ('Casos de teste — formulário de login', 'Funcionalidade: login por e-mail e senha.\nComportamento esperado: credenciais válidas permitem acesso; credenciais inválidas mostram mensagem de erro.\nIdeias para testar: campos vazios, senha incorreta, e-mail inválido e botão de entrar.'),
        ('Análise de requisito — cadastro', 'Requisito de exemplo: “O usuário pode criar uma conta usando e-mail e senha”.\nPerguntas úteis: quais são as regras de senha? O e-mail precisa ser confirmado? O que acontece se já estiver cadastrado?'),
        ('Relato de bug — botão não funciona', 'Título: “Botão Salvar não conclui o cadastro”.\nResultado atual: ao clicar em Salvar, nada acontece.\nResultado esperado: o cadastro é salvo e uma confirmação é exibida.\nPassos: abrir cadastro, preencher os campos obrigatórios e clicar em Salvar.'),
        ('Teste de API — consulta de usuário', 'Endpoint de exemplo: GET /usuarios/123.\nComportamento esperado: retornar os dados do usuário quando existir.\nVerificações: usuário existente, usuário inexistente, identificador inválido e formato da resposta.'),
        ('Automação — busca de produtos', 'Funcionalidade: busca de produtos em uma loja de demonstração.\nComportamento esperado: exibir resultados relacionados ao termo digitado.\nVerificações: termo válido, busca sem resultados, campo vazio e mensagem de erro.'),
    ]
    for title, body in examples:
        print(f'\n┌─ {title}')
        print_wrapped(body, indent='│  ')
        print('└' + '─' * max(20, terminal_width() - 1))
    print('\nUse os exemplos como ponto de partida e adapte-os ao seu contexto real.')


def show_prompt(title, prompt):
    line('═')
    print('PROMPT PREPARADO PELO PROGRAMA')
    print('Este texto foi montado pelo QA Prompt Assistant; ainda não é uma resposta da IA.')
    line('─')
    print_wrapped(prompt)
    line('═')


def program_options_after_answer(title, prompt, answer):
    print('\n')
    line('═')
    print('PRÓXIMAS AÇÕES — OPÇÕES DO PROGRAMA')
    print('Estas opções são exibidas pelo QA Prompt Assistant, não foram geradas pela IA.')
    line('─')
    if ask_choice('Salvar prompt e resposta no histórico local?\n  [1] Sim\n  [2] Não\nEscolha: ', ['1', '2']) == '1':
        print_wrapped('Histórico salvo em: ' + str(save_history(title, prompt, answer).resolve()))
    act = ask_choice('Exportar o prompt?\n  [1] TXT\n  [2] Markdown\n  [3] Não\nEscolha: ', ['1', '2', '3'])
    if act in ('1', '2'):
        print_wrapped('Prompt exportado em: ' + str(save_prompt(title, prompt, 'txt' if act == '1' else 'md').resolve()))


def run_ai(title, prompt):
    score, suggestions = evaluate_prompt(prompt)
    print(f'\nCompletude estimada do prompt: {score}% (avaliação heurística local; não é garantia de qualidade)')
    if suggestions:
        print('\nSUGESTÕES DO PROGRAMA')
        for suggestion in suggestions:
            print_wrapped('• ' + suggestion)
    print('\n')
    line('═')
    print('COMO DESEJA UTILIZAR ESTE PROMPT?')
    print('Escolha API, GitHub Copilot Chat no VS Code ou cópia para outra ferramenta.')
    line('─')
    destination = ask_choice(
        '[1] Consultar a IA configurada por API\n'
        '[2] Abrir no GitHub Copilot Chat (VS Code)\n'
        '[3] Copiar prompt para a área de transferência\n'
        '[4] Apenas salvar/voltar\nEscolha: ', ['1', '2', '3', '4']
    )
    if destination == '2':
        send_to_vscode_copilot(prompt)
        print_wrapped('Nota: a integração abre o chat com o prompt; o envio efetivo e a resposta dependem do comportamento da versão instalada do VS Code/Copilot.')
        act = ask_choice('Salvar também uma cópia do prompt?\n  [1] TXT\n  [2] Markdown\n  [3] Não\nEscolha: ', ['1', '2', '3'])
        if act in ('1', '2'):
            print_wrapped('Prompt salvo em: ' + str(save_prompt(title, prompt, 'txt' if act == '1' else 'md').resolve()))
        return
    if destination == '3':
        if copy_to_clipboard(prompt):
            print_wrapped('Prompt copiado para a área de transferência. Agora cole-o no chat da IA desejada.')
        else:
            print_wrapped('Não consegui acessar a área de transferência. Você pode exportar o prompt em TXT ou Markdown.')
        act = ask_choice('Salvar também uma cópia?\n  [1] TXT\n  [2] Markdown\n  [3] Não\nEscolha: ', ['1', '2', '3'])
        if act in ('1', '2'):
            print_wrapped('Prompt salvo em: ' + str(save_prompt(title, prompt, 'txt' if act == '1' else 'md').resolve()))
        return
    if destination == '4':
        act = ask_choice('Salvar o prompt?\n  [1] TXT\n  [2] Markdown\n  [3] Não\nEscolha: ', ['1', '2', '3'])
        if act in ('1', '2'):
            print_wrapped('Prompt salvo em: ' + str(save_prompt(title, prompt, 'txt' if act == '1' else 'md').resolve()))
        return
    try:
        print(f'\nConectando ao provedor {get_provider()} • modelo {get_model()}...')
        print('Aguarde; respostas longas podem levar alguns segundos.\n')
        answer, model = ask_ai(prompt)
        line('═')
        print(f'RESPOSTA DA IA • MODELO: {model}')
        print('O conteúdo abaixo foi retornado pela IA. Revise antes de usar.')
        line('─')
        print_wrapped(answer)
        line('═')
        print('\n')
        show_usage()
        program_options_after_answer(title, prompt, answer)
    except (AIConfigurationError, AIRequestError) as exc:
        line('═')
        print('ERRO AO CONSULTAR A IA')
        line('─')
        print_wrapped(str(exc))
        print('\nAs opções abaixo são do programa; seu prompt não foi descartado.')
        act = ask_choice('Salvar o prompt mesmo assim?\n  [1] TXT\n  [2] Markdown\n  [3] Não\nEscolha: ', ['1', '2', '3'])
        if act in ('1', '2'):
            print_wrapped('Prompt salvo em: ' + str(save_prompt(title, prompt, 'txt' if act == '1' else 'md').resolve()))


def main():
    load_local_env()
    banner()
    pause('Pressione Enter para abrir o menu...')
    while True:
        clear_screen()
        print('╭' + '─' * (terminal_width() - 2) + '╮')
        print('│ MENU PRINCIPAL'.ljust(terminal_width() - 1) + '│')
        print('╰' + '─' * (terminal_width() - 2) + '╯')
        print('\n  [1] Gerar prompt guiado e consultar IA')
        print('  [2] Verificar a qualidade de um prompt')
        print('  [3] Ver modelo, chamadas locais e redefinição de referência')
        print('  [4] Consultar histórico local')
        print('  [5] Tutorial / Como usar')
        print('  [6] Ver exemplos práticos')
        print('  [0] Sair')
        choice = ask_choice('\nEscolha uma opção: ', ['0', '1', '2', '3', '4', '5', '6'])
        clear_screen()
        if choice == '0':
            print('Até mais! Bons testes.'); return
        if choice == '1':
            line('═'); print('ESCOLHA UMA ATIVIDADE DE QA'); line('─')
            for key, (label, _) in MENU.items():
                print(f'  [{key}] {label}')
            print('  [0] Voltar ao menu principal')
            sub = ask_choice('\nEscolha uma atividade: ', [*MENU.keys(), '0'])
            clear_screen()
            if sub != '0':
                title, builder = MENU[sub]
                print(f'ATIVIDADE: {title}\n')
                prompt = builder()
                show_prompt(title, prompt)
                run_ai(title, prompt)
            pause()
        elif choice == '2':
            line('═'); print('VERIFICAR A QUALIDADE DE UM PROMPT'); line('─')
            prompt = build_ai_question_prompt()
            score, suggestions = evaluate_prompt(prompt)
            print(f'\nCompletude estimada: {score}% (heurística local)')
            if suggestions:
                print('\nSUGESTÕES DO PROGRAMA:')
                for suggestion in suggestions: print_wrapped('• ' + suggestion)
            else:
                print('Os elementos avaliados foram encontrados.')
            if ask_choice('\nPedir à IA para aprimorar este prompt?\n[1] Sim\n[2] Não\nEscolha: ', ['1', '2']) == '1':
                run_ai('Aprimoramento de prompt', 'Aprimore este prompt para QA, preserve a intenção, não invente requisitos e explique melhorias:\n\n' + prompt)
            pause()
        elif choice == '3':
            show_usage(); pause()
        elif choice == '4':
            line('═'); print('HISTÓRICO LOCAL'); line('─')
            items = list_history()
            if not items:
                print('Ainda não há histórico local.')
            else:
                print('\nArquivos mais recentes primeiro:')
                for item in items[:30]: print_wrapped('• ' + item.name)
                print_wrapped('Os arquivos ficam em historico/ e podem conter conteúdo enviado à IA. Revise-os e apague-os se necessário.')
            pause()
        elif choice == '5':
            show_tutorial(); pause()
        elif choice == '6':
            show_examples(); pause()


if __name__ == '__main__':
    main()
