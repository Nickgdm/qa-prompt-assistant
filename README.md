# QA Prompt Assistant

Ferramenta de terminal em Python para criar, revisar e encaminhar prompts para modelos de IA úteis em atividades de Quality Assurance (QA). O projeto foi desenvolvido como parte do meu portfólio de QA, incluindo um projeto de IA para apoiar atividades comuns de testes de software.

> **Projeto relacionado à formação EBAC:** [QA Prompt Assistant](https://github.com/Nickgdm/qa-prompt-assistant) é o projeto de IA; este repositório contém o código e a documentação da ferramenta.

## Funcionalidades

- Tela inicial, menus, tutorial e exemplos práticos em português.
- Prompts guiados para casos de teste, análise de requisitos, relatos de bugs, testes de API e automação.
- Respostas formatadas e separadas das mensagens e opções do próprio programa.
- Suporte à Google Gemini API, APIs compatíveis com OpenAI Chat Completions e modelos locais pelo Ollama.
- Opção para abrir um prompt no GitHub Copilot Chat do VS Code usando a CLI `code chat -`, além de copiar para a área de transferência.
- Verificação heurística de prompts, exportação para TXT/Markdown e histórico local opcional.
- Registro local de chamadas; os contadores não representam a cota oficial do provedor.

## Provedores compatíveis

### 1. Google Gemini API

- Provedor: `AI_PROVIDER=gemini`
- Chave: `GEMINI_API_KEY`
- Modelo: `AI_MODEL` (ou `GEMINI_MODEL` para compatibilidade com configurações antigas)
- Crie e gerencie sua chave no [Google AI Studio](https://aistudio.google.com/).

### 2. APIs compatíveis com OpenAI Chat Completions

O programa usa o SDK Python `openai` e o endpoint Chat Completions. Pode funcionar com a API da OpenAI e serviços como OpenRouter, Groq e Together AI, desde que ofereçam um endpoint compatível. Cada serviço pode ter diferenças de URL, nome de modelo, cabeçalhos, limites e cobrança. Consulte sempre a documentação oficial do serviço escolhido; nem todos os endpoints ou parâmetros são intercambiáveis.

- Provedor: `AI_PROVIDER=openai_compatible`
- Chave: `AI_API_KEY`
- Modelo: `AI_MODEL`
- URL base: `AI_BASE_URL` (por exemplo, `https://api.openai.com/v1` para a API da OpenAI).

### 3. Modelos locais com Ollama (incluindo Llama)

O [Ollama](https://ollama.com/) permite executar modelos baixados localmente, incluindo modelos da família Llama. O desempenho depende do modelo e do hardware disponível. O programa não instala nem baixa modelos automaticamente.

1. Instale o Ollama.
2. Baixe um modelo, por exemplo: `ollama pull llama3.2`.
3. Configure o arquivo `.env`:

   ```dotenv
   AI_PROVIDER=ollama
   AI_MODEL=llama3.2
   AI_BASE_URL=http://localhost:11434/v1
   ```

4. Deixe `AI_API_KEY` vazia. A integração local usa uma credencial fictícia apenas para compatibilidade com o cliente; nenhuma chave real é necessária para esse fluxo.

Consulte a [documentação da API do Ollama](https://docs.ollama.com/api) para detalhes.

## Usar com GitHub Copilot Chat no VS Code

A opção **Abrir no GitHub Copilot Chat (VS Code)** utiliza o comando `code chat -` do VS Code para abrir uma conversa e passar o prompt pela entrada padrão. É necessário ter uma versão compatível do VS Code, o comando `code` disponível no PATH e acesso ao GitHub Copilot configurado no VS Code. Consulte a [documentação da CLI do VS Code](https://code.visualstudio.com/docs/configure/command-line#_start-chat-from-the-command-line).

Essa integração não usa uma API do Copilot nem requer uma chave de API no QA Prompt Assistant. A disponibilidade e o comportamento dependem da versão instalada do VS Code. Se o comando falhar, use a opção de copiar o prompt e cole-o manualmente no Copilot Chat. O usuário continua responsável por revisar e enviar o conteúdo no VS Code.

## Instalação

### Windows

1. Instale Python 3.10 ou superior.
2. Baixe ou clone este repositório e abra o terminal na pasta do projeto.
3. Instale as dependências:

   ```powershell
   py -m pip install -r requirements.txt
   ```

4. Copie `.env.example` para `.env` e configure o provedor que deseja utilizar.
5. Execute:

   ```powershell
   py main.py
   ```

### Linux/macOS

Use `python3 -m pip install -r requirements.txt` e depois `python3 main.py`.

## Exemplos de configuração

### Gemini

```dotenv
AI_PROVIDER=gemini
GEMINI_API_KEY=sua_chave_real
AI_MODEL=gemini-3.5-flash-lite
```

### OpenAI (API cobrada conforme preços e condições vigentes)

```dotenv
AI_PROVIDER=openai_compatible
AI_API_KEY=sua_chave_real
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
```

Confirme o nome do modelo e os preços atuais diretamente na documentação oficial do provedor.

### Ollama local

```dotenv
AI_PROVIDER=ollama
AI_MODEL=llama3.2
AI_BASE_URL=http://localhost:11434/v1
```

## Segurança e privacidade

- Nunca publique o arquivo `.env` preenchido nem envie chaves de API ao GitHub. O `.env` deve estar no `.gitignore`; publique apenas o `.env.example` sem segredos.
- Em provedores hospedados, os prompts são enviados ao serviço selecionado e ficam sujeitos aos termos, às políticas de privacidade e retenção, e aos preços desse provedor.
- Com o Ollama, os prompts são processados localmente por padrão; a instalação e a configuração de rede do usuário também importam.
- Não envie senhas, tokens, dados pessoais ou informações confidenciais. Use dados fictícios em demonstrações.

## Limites e custos

O programa não consegue exibir uma contagem universal de cota restante, custo exato ou tempo de redefinição para todos os provedores. Limites e disponibilidade podem variar conforme conta, modelo, região, plano e endpoint. APIs pagas podem gerar cobranças; confira preços e limites oficiais antes de usar. Os contadores locais servem apenas como referência das chamadas registradas pelo aplicativo.

## Testes

Instale as dependências de desenvolvimento e execute os testes:

```powershell
py -m pip install -r requirements-dev.txt
py -m pytest
```

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

## Limitações conhecidas

- Provedores de terceiros precisam oferecer uma API compatível com OpenAI Chat Completions; serviços proprietários não compatíveis podem exigir adaptações.
- Para usar modelos Llama localmente, o caminho documentado neste projeto é o Ollama.
- Respostas geradas por IA podem conter erros e devem ser validadas com requisitos e evidências reais.
- A avaliação da qualidade de prompts é heurística e não garante a qualidade nem a correção da resposta.

## Formação

Projeto desenvolvido como parte do meu percurso de estudos em **Quality Assurance (QA) pela EBAC — Escola Britânica de Artes Criativas e Tecnologia**.

## Projeto relacionado

- [Repositório de atividades EBAC](https://github.com/Nickgdm/Ebac) — exercícios e cenários de testes relacionados à formação.
