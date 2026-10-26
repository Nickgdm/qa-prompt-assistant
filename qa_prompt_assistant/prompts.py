from .utils import ask_choice, ask_non_empty, ask_optional

def _context():
    return (ask_non_empty('Qual funcionalidade/sistema será avaliado? '), ask_non_empty('O que deveria acontecer? '), ask_optional('Regras/contexto adicional (Enter para pular): '))

def build_test_cases_prompt():
    print('\n--- Casos de teste ---'); feature, behavior, context = _context()
    p = ask_choice('Plataforma [1] Web [2] Mobile [3] API [4] Outra/não sei: ', ['1','2','3','4'])
    p = {'1':'Web','2':'Mobile','3':'API','4':'Outra/não informada'}[p]
    k = ask_choice('Cenários [1] Positivos [2] Negativos [3] Borda [4] Todos: ', ['1','2','3','4'])
    k = {'1':'positivos','2':'negativos','3':'casos de borda','4':'positivos, negativos e casos de borda'}[k]
    f = ask_choice('Formato [1] Lista [2] Tabela detalhada: ', ['1','2'])
    f = 'lista organizada' if f == '1' else 'tabela com ID, título, pré-condições, dados, passos e resultado esperado'
    return f'Crie casos de teste de QA para: {feature}\nComportamento esperado: {behavior}\nContexto/regras: {context}\nPlataforma: {p}\nCenários: {k}\nFormato: {f}.\nNão invente regras. Sinalize ambiguidades, lacunas e perguntas de esclarecimento. Inclua resultados esperados verificáveis.'

def build_requirements_prompt():
    req = ask_non_empty('Cole/descreva o requisito: '); goal = ask_optional('Objetivo de negócio (Enter para pular): ')
    return f'Analise este requisito como QA.\nRequisito: {req}\nObjetivo: {goal}\nResuma, identifique ambiguidades e lacunas, sugira critérios de aceitação verificáveis (separando sugestões de requisitos explícitos), liste perguntas e proponha cenários. Não invente regras.'

def build_bug_prompt():
    a = ask_non_empty('Título/resumo do problema: '); b = ask_non_empty('Resultado atual: '); c = ask_non_empty('Resultado esperado: '); d = ask_non_empty('Passos para reproduzir: '); e = ask_optional('Ambiente/versão (Enter para pular): ')
    return f'Revise este relato de bug.\nResumo: {a}\nResultado atual: {b}\nResultado esperado: {c}\nPassos: {d}\nAmbiente: {e}\nOrganize o relato, sugira título claro, identifique informações faltantes e evidências úteis. Não afirme causa-raiz sem evidências.'

def build_api_prompt():
    endpoint = ask_non_empty('Endpoint/descrição da API: '); m = ask_choice('Método [1] GET [2] POST [3] PUT [4] PATCH [5] DELETE [6] Não sei: ', ['1','2','3','4','5','6']); m = {'1':'GET','2':'POST','3':'PUT','4':'PATCH','5':'DELETE','6':'não informado'}[m]; behavior = ask_non_empty('Comportamento esperado: ')
    return f'Proponha cenários de teste de API.\nEndpoint: {endpoint}\nMétodo: {m}\nComportamento esperado: {behavior}\nInclua cenários positivos, negativos, validações, limites e status HTTP quando aplicável. Para cada cenário, informe objetivo, entrada e resultado esperado. Não invente o contrato da API. Não inclua segredos nem dados pessoais.'

def build_automation_prompt():
    feature, behavior, context = _context(); t = ask_choice('Ferramenta [1] Cypress [2] Playwright [3] Selenium [4] Não decidi: ', ['1','2','3','4']); t = {'1':'Cypress','2':'Playwright','3':'Selenium','4':'não definida'}[t]; d = ask_choice('Ajuda [1] Estratégia [2] Código comentado [3] Ambos: ', ['1','2','3']); d = {'1':'estratégia','2':'código comentado','3':'estratégia e código comentado'}[d]
    return f'Ajude a planejar automação de QA para {feature}. Comportamento: {behavior}. Contexto: {context}. Ferramenta: {t}. Ajuda: {d}. Explique verificações e riscos de instabilidade. Não invente URLs, seletores ou regras.'

def build_freeform_prompt():
    initial = ask_non_empty('Descreva o que quer pedir à IA: '); context = ask_optional('Contexto/tecnologia (Enter para pular): '); d = ask_choice('Detalhamento [1] Básico [2] Intermediário [3] Avançado: ', ['1','2','3']); d = {'1':'curto e direto','2':'com contexto, objetivo e formato','3':'com critérios, restrições, casos de borda e perguntas sobre lacunas'}[d]
    return f'Transforme em um prompt claro para QA. Solicitação: {initial}\nContexto: {context}\nDetalhamento: {d}. Preserve a intenção, não invente fatos e faça perguntas quando faltarem informações essenciais. Entregue o prompt final e explique brevemente as melhorias.'

def build_ai_question_prompt(): return ask_non_empty('Digite sua pergunta para o assistente de QA: ')
