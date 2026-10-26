# QA Prompt Assistant 2.3.0

Ferramenta de terminal em Python para criar, revisar e enviar prompts para modelos de IA úteis em atividades de Quality Assurance (QA). O projeto é configurável: não depende exclusivamente da Gemini e pode usar serviços por API (gratuitos ou pagos) e modelos locais via Ollama.

## Funcionalidades
- Tela inicial, menus, tutorial e exemplos práticos em português.
- Prompts guiados para casos de teste, requisitos, bugs, APIs e automação.
- Respostas formatadas e separadas das mensagens/opções do próprio programa.
- Suporte a Gemini, APIs compatíveis com o SDK da OpenAI e modelos locais pelo Ollama.
- Opção para abrir um prompt no GitHub Copilot Chat do VS Code usando a CLI `code chat -`, além de copiar para a área de transferência.
- Verificação heurística de prompts, exportação TXT/Markdown e histórico local opcional.
- Registro local de chamadas; não representa a cota oficial do provedor.

## Provedores compatíveis

### 1. Google Gemini API
- Provedor: `AI_PROVIDER=gemini`
- Chave: `GEMINI_API_KEY`
- Modelo: `AI_MODEL` (ou `GEMINI_MODEL` para compatibilidade com configurações antigas)
- Obtenha a chave no [Google AI Studio](https://aistudio.google.com/).

### 2. APIs compatíveis com OpenAI Chat Completions
O programa usa o SDK Python `openai` e o endpoint Chat Completions. Pode funcionar com OpenAI e serviços como OpenRouter, Groq, Together AI, ou outros provedores **desde que ofereçam endpoint compatível com OpenAI Chat Completions**. Cada serviço pode ter diferenças de URL, nome de modelo, cabeçalhos, limites e cobrança; consulte a documentação do serviço. Nem todo serviço compatível oferece todos os parâmetros ou todos os modelos.
- Provedor: `AI_PROVIDER=openai_compatible`
- Chave: `AI_API_KEY`
- Modelo: `AI_MODEL`
- URL base: `AI_BASE_URL` (ex.: `https://api.openai.com/v1` para OpenAI; substitua pela URL oficial do serviço escolhido).
- Para serviços que não exigem URL personalizada, pode-se deixar `AI_BASE_URL` vazia se o endpoint padrão for o correto.

### 3. Modelos locais com Ollama (incluindo Llama)
Ollama permite executar modelos baixados localmente, como famílias Llama, no computador do usuário. O desempenho depende do modelo, da memória RAM/VRAM e do hardware. É necessário instalar e iniciar o Ollama e baixar um modelo; o programa não baixa modelos automaticamente.
1. Instale o [Ollama](https://ollama.com/).
2. No terminal, baixe um modelo, por exemplo: `ollama pull llama3.2`.
3. Configure no `.env`:
   ```dotenv
   AI_PROVIDER=ollama
   AI_MODEL=llama3.2
   AI_BASE_URL=http://localhost:11434/v1
   ```
4. Deixe `AI_API_KEY` vazia; a integração local usa uma credencial fictícia somente para compatibilidade com o cliente, e não envia uma chave real.

Consulte a documentação da [API do Ollama](https://docs.ollama.com/api) para detalhes e modelos disponíveis.

## Usar com GitHub Copilot Chat no VS Code

A opção **Abrir no GitHub Copilot Chat (VS Code)** utiliza o comando oficial `code chat -` do VS Code para abrir uma conversa e passar o prompt pela entrada padrão. É necessário ter uma versão compatível do VS Code instalada, o comando `code` disponível no PATH e acesso ao GitHub Copilot autenticado no VS Code. Consulte a [documentação da CLI do VS Code](https://code.visualstudio.com/docs/configure/command-line#_start-chat-from-the-command-line).

Essa integração **não usa uma API do Copilot nem requer uma chave de API no QA Prompt Assistant**. A disponibilidade e o comportamento de abertura do chat dependem da versão instalada do VS Code. Se o comando não estiver disponível ou falhar, use a opção de copiar o prompt e cole-o manualmente no Copilot Chat. O usuário continua responsável por revisar e enviar o conteúdo no VS Code.

## Instalação (Windows)
1. Instale Python 3.10 ou superior.
2. Extraia o ZIP e abra o terminal na pasta do projeto.
3. Instale as dependências: `py -m pip install -r requirements.txt`.
4. Copie `.env.example` para `.env` e edite as variáveis conforme o provedor desejado.
5. Execute: `py main.py`.

Para Linux/macOS, use `python3 -m pip install -r requirements.txt` e `python3 main.py`.

## Exemplos de configuração

**Gemini:**
```dotenv
AI_PROVIDER=gemini
GEMINI_API_KEY=sua_chave_real
AI_MODEL=gemini-3.5-flash-lite
```

**OpenAI (API paga conforme plano e preços vigentes):**
```dotenv
AI_PROVIDER=openai_compatible
AI_API_KEY=sua_chave_real
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
```
Confirme o identificador de modelo atualmente disponível na sua conta e os preços diretamente no site oficial.

**Ollama local:**
```dotenv
AI_PROVIDER=ollama
AI_MODEL=llama3.2
AI_BASE_URL=http://localhost:11434/v1
```

## Segurança e privacidade
- Nunca publique o `.env` preenchido, nem envie chaves ao GitHub. O `.env` está no `.gitignore`; cada pessoa deve usar sua própria chave.
- Em provedores hospedados, o prompt é enviado ao serviço escolhido e fica sujeito aos termos, políticas de retenção, privacidade e preços desse provedor.
- Ollama local normalmente processa os prompts na máquina, mas a instalação e as configurações de rede do usuário importam.
- Não envie senhas, tokens, dados pessoais ou informações confidenciais. Use dados fictícios em demonstrações.

## Limites e custos
O programa não consegue exibir uma contagem universal de cota restante, custo exato ou tempo de redefinição para todos os provedores. Os limites podem variar por conta, modelo, região, plano e tipo de endpoint. APIs pagas podem cobrar por uso; confira preços e limites oficiais antes de utilizar. Os contadores locais do aplicativo servem apenas como referência de quantas chamadas bem-sucedidas foram registradas pelo próprio programa.

## Testes
```powershell
py -m pip install -r requirements-dev.txt
py -m pytest
```

## Estrutura
```text
qa-prompt-assistant-v2.3.0/
├── main.py
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── qa_prompt_assistant/
│   ├── config.py
│   ├── ai_client.py
│   ├── cli.py
│   ├── prompts.py
│   ├── usage.py
│   └── utils.py
└── tests/
```

## Limitações
- Compatibilidade com terceiros depende de eles oferecerem uma API de chat compatível com OpenAI; endpoints e modelos proprietários não compatíveis podem exigir adaptação.
- O nome `Llama` se refere à família de modelos; para uso local neste projeto, a forma mais simples é executá-los pelo Ollama.
- Respostas de IA podem conter erros; valide-as com requisitos e evidências reais.
- A avaliação de qualidade de prompt é heurística e não constitui garantia de qualidade.
