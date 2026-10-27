╔══════════════════════════════════════════════════════╗
║                  QA PROMPT ASSISTANT                  ║
╚══════════════════════════════════════════════════════╝

Ferramenta de terminal em Python para criar, revisar e organizar prompts que podem apoiar atividades de Quality Assurance (QA). O projeto explora o uso de modelos de IA como auxílio à preparação de artefatos de teste, mantendo a necessidade de revisão humana.

══════════════════════════════════════════════════════

## Sobre o projeto

O QA Prompt Assistant oferece uma interface de terminal em português para orientar a criação de prompts e encaminhá-los a provedores de IA compatíveis ou modelos locais.

══════════════════════════════════════════════════════

## Funcionalidades

- Menus, tutorial e exemplos práticos em português.
- Prompts guiados para casos de teste, análise de requisitos, relatos de bugs, testes de API e automação.
- Respostas formatadas e separadas das mensagens do próprio programa.
- Integração com Google Gemini API, APIs compatíveis com OpenAI Chat Completions e modelos locais pelo Ollama.
- Opção para abrir prompts no GitHub Copilot Chat do VS Code por meio da CLI `code chat -`.
- Opções para copiar e exportar prompts em TXT/Markdown.
- Histórico local opcional.
- Verificação heurística de prompts e registro local de chamadas. Os contadores não representam a cota oficial de um provedor.

══════════════════════════════════════════════════════

## Provedores compatíveis

### Google Gemini API

- Provedor: `AI_PROVIDER=gemini`
- Chave: `GEMINI_API_KEY`
- Modelo: `AI_MODEL` ou `GEMINI_MODEL` para compatibilidade com configurações antigas.

Consulte o [Google AI Studio](https://aistudio.google.com/) para criar e gerenciar uma chave.

### APIs compatíveis com OpenAI Chat Completions

O programa utiliza o SDK Python `openai` e o endpoint Chat Completions. Pode funcionar com a API da OpenAI e serviços como OpenRouter, Groq e Together AI, desde que ofereçam um endpoint compatível. URLs, modelos, cabeçalhos, limites e cobranças variam entre provedores.

- Provedor: `AI_PROVIDER=openai_compatible`
- Chave: `AI_API_KEY`
- Modelo: `AI_MODEL`
- URL base: `AI_BASE_URL`

Para a API da OpenAI, por exemplo, a URL base é `https://api.openai.com/v1`. Consulte a documentação oficial do provedor escolhido.

### Modelos locais com Ollama

O [Ollama](https://ollama.com/) permite executar modelos baixados localmente, incluindo modelos da família Llama. O desempenho depende do modelo e do hardware disponível. O programa não baixa modelos automaticamente.

1. Instale o Ollama.
2. Baixe um modelo, por exemplo:

```bash
ollama pull llama3.2
```

3. Configure o arquivo `.env`:

```dotenv
AI_PROVIDER=ollama
AI_MODEL=llama3.2
AI_BASE_URL=http://localhost:11434/v1
```

4. Deixe `AI_API_KEY` vazia. A integração local utiliza uma credencial fictícia apenas para compatibilidade com o cliente; não é necessária uma chave real para esse fluxo.

Consulte a [documentação da API do Ollama](https://docs.ollama.com/api) para detalhes.

══════════════════════════════════════════════════════

## Usar com GitHub Copilot Chat no VS Code

A opção para abrir um prompt no GitHub Copilot Chat utiliza o comando `code chat -` do VS Code. É necessário ter uma versão compatível do VS Code, o comando `code` disponível no PATH e o acesso ao Copilot configurado.

Consulte a [documentação da CLI do VS Code](https://code.visualstudio.com/docs/configure/command-line#_start-chat-from-the-command-line).

Essa integração não utiliza uma API do Copilot nem requer uma chave de API no QA Prompt Assistant. A disponibilidade depende da versão instalada do VS Code. Se o comando falhar, copie o prompt e cole-o manualmente no Copilot Chat. O usuário continua responsável por revisar e enviar o conteúdo no VS Code.

══════════════════════════════════════════════════════

## Instalação

### Windows

1. Instale Python 3.10 ou superior.
2. Clone ou baixe o repositório e abra o terminal na pasta do projeto.
3. Instale as dependências:

```powershell
py -m pip install -r requirements.txt
```

4. Copie `.env.example` para `.env` e configure o provedor desejado.
5. Execute:

```powershell
py main.py
```

### Linux/macOS

Instale as dependências e execute o programa:

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

══════════════════════════════════════════════════════

## Exemplos de configuração

### Gemini

```dotenv
AI_PROVIDER=gemini
GEMINI_API_KEY=sua_chave_real
AI_MODEL=nome_do_modelo_disponivel
```

### API compatível com OpenAI Chat Completions

```dotenv
AI_PROVIDER=openai_compatible
AI_API_KEY=sua_chave_real
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=nome_do_modelo_disponivel
```

O uso de APIs hospedadas pode gerar cobranças. Confirme o modelo, os preços e os limites atuais na documentação oficial do provedor.

### Ollama local

```dotenv
AI_PROVIDER=ollama
AI_MODEL=llama3.2
AI_BASE_URL=http://localhost:11434/v1
```

══════════════════════════════════════════════════════

## Segurança e privacidade

- Nunca publique o arquivo `.env` preenchido nem envie chaves de API ao GitHub. Mantenha o arquivo no `.gitignore` e publique apenas o `.env.example` sem segredos.
- Em provedores hospedados, os prompts são enviados ao serviço selecionado e ficam sujeitos aos termos, às políticas de privacidade e retenção e aos preços desse provedor.
- Com o Ollama, os prompts são processados localmente por padrão, mas a instalação e a configuração de rede também importam.
- Não envie senhas, tokens, dados pessoais ou informações confidenciais. Utilize dados fictícios em demonstrações.

══════════════════════════════════════════════════════

## Limites e custos

O programa não consegue apresentar uma contagem universal de cota restante, custo exato ou tempo de redefinição para todos os provedores. Limites e disponibilidade variam conforme conta, modelo, região, plano e endpoint. Os contadores locais servem apenas como referência das chamadas registradas pelo aplicativo.

══════════════════════════════════════════════════════

## Testes

Instale as dependências de desenvolvimento e execute os testes:

```powershell
py -m pip install -r requirements-dev.txt
py -m pytest
```

══════════════════════════════════════════════════════

## Estrutura do projeto

```text
qa-prompt-assistant/
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

══════════════════════════════════════════════════════

## Limitações conhecidas

- Provedores de terceiros precisam oferecer API compatível com OpenAI Chat Completions; serviços não compatíveis podem exigir adaptações.
- Para modelos Llama locais, o fluxo documentado utiliza Ollama.
- Respostas de IA podem conter erros e devem ser validadas com requisitos e evidências reais.
- A avaliação da qualidade de prompts é heurística e não garante a correção das respostas.

══════════════════════════════════════════════════════

## Considerações finais

O QA Prompt Assistant é uma ferramenta de apoio ao estudo e à organização de prompts. Ele não substitui análise de requisitos, execução de testes ou validação humana. Confirme sempre as respostas geradas antes de utilizá-las em atividades de QA.

══════════════════════════════════════════════════════

## Natureza do projeto

Este projeto foi desenvolvido como parte do portfólio de estudos em Quality Assurance (QA), explorando o uso de IA como apoio a atividades de teste. Seu desenvolvimento tem caráter educacional e de experimentação; os recursos disponíveis dependem das configurações e dos provedores escolhidos pelo usuário.

══════════════════════════════════════════════════════