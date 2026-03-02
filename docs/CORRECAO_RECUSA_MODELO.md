# 🔧 Correção: Modelo Recusando Análise

## Problema Identificado

Ao executar o projeto, o modelo GPT-4o estava retornando uma **resposta de recusa** em vez de executar a análise:

```
"I'm unable to provide a detailed analysis or JSON output for this architecture diagram. 
However, I can guide you on how to analyze it using the STRIDE methodology..."
```

### Causa Raiz

O modelo estava sendo muito cauteloso e interpretando o prompt como uma solicitação de orientação em vez de uma tarefa a ser executada. Possíveis causas:

1. **Prompt muito longo e complexo** - Contexto STRIDE extenso confundindo o modelo
2. **Ausência de mensagem de sistema clara** - Sem instrução explícita de que é uma ferramenta automatizada
3. **Ambiguidade nas instruções** - Linguagem que permitia interpretação como "ou você pode..."
4. **Temperature alta** - 0.5 permitia respostas mais variadas
5. **Max tokens baixo** - 8192 pode não ser suficiente para análise completa
6. **Falta de instrução imperativa** - Não estava claro que o modelo DEVE executar

---

## ✅ Correções Implementadas

### 1. Adicionada Mensagem de Sistema Forte
```python
{
    "role": "system",
    "content": "You are a security analysis tool that outputs structured JSON. Always return valid JSON matching the requested schema, never refuse or provide explanations instead."
}
```

**Impacto:** Define claramente o papel do modelo como ferramenta automatizada, não assistente consultivo.

### 2. Prompt Simplificado e Mais Direto
**Antes:**
```python
prompt = f"""
Você é um especialista em segurança...
{stride_context}  # ~300 linhas de contexto
## INSTRUÇÕES CRÍTICAS - ANÁLISE EXAUSTIVA:
...
"""
```

**Depois:**
```python
prompt = f"""
EXECUTE A ANÁLISE STRIDE AGORA. Analise o diagrama...
IMPORTANTE: Você DEVE analisar a imagem fornecida...

METODOLOGIA STRIDE:
- S (Spoofing): Riscos de falsificação...
[versão concisa - ~50 linhas]
"""
```

**Impacto:** Reduz ambiguidade e deixa claro que é uma ordem de execução.

### 3. Aumentado max_tokens
```python
# Antes
max_tokens=8192

# Depois  
max_tokens=16000
```

**Impacto:** Dá mais espaço para o modelo gerar análise completa sem truncamento.

### 4. Reduzida Temperature
```python
# Antes
temperature=0.5

# Depois
temperature=0.3
```

**Impacto:** Respostas mais determinísticas e consistentes.

### 5. Instrução Explícita no Final do Prompt
```python
"""
RETORNE APENAS O OBJETO JSON. Não inclua explicações, guias ou texto adicional.
Comece sua resposta diretamente com { e termine com }.

Se você não conseguir analisar perfeitamente todos os detalhes, faça o melhor possível baseado no que consegue 
identificar na imagem. SEMPRE retorne o JSON estruturado conforme especificado.
"""
```

**Impacto:** Remove qualquer ambiguidade sobre o formato esperado da resposta.

### 6. Removido Contexto STRIDE Extenso
**Antes:**
```python
stride_context = "## Base de Conhecimento STRIDE\n\n"
stride_context += "### Categorias STRIDE:\n"
for categoria, info in STRIDE_DETAILS.items():
    stride_context += f"**{categoria}**: {info['description']}\n"
    stride_context += f"Exemplos: {', '.join(info['examples'][:3])}\n\n"
# ... mais 200+ linhas
```

**Depois:**
```python
METODOLOGIA STRIDE:
- S (Spoofing): Riscos de falsificação de identidade
- T (Tampering): Riscos de adulteração de dados
...
```

**Impacto:** Prompt mais limpo, focado e menos confuso.

---

## 📊 Comparação Antes/Depois

| Aspecto | Antes | Depois |
|---------|-------|--------|
| Mensagem de Sistema | Ausente | ✅ Presente e forte |
| Tamanho do Prompt | ~3000 tokens | ~800 tokens |
| Clareza das Instruções | Ambígua | ✅ Imperativa |
| Max Tokens | 8192 | 16000 |
| Temperature | 0.5 | 0.3 |
| Taxa de Recusa | Alta | ✅ Baixa esperada |

---

## 🧪 Como Testar

### 1. Teste Rápido via Interface Web
```bash
streamlit run app.py
```
1. Upload de um diagrama AWS
2. Clicar em "Analisar Arquitetura"
3. **Resultado esperado:** JSON estruturado (não mensagem de recusa)

### 2. Teste via Script
```bash
python3 test_analyzer.py
```

### 3. Verificar Resposta
A resposta do modelo deve:
- ✅ Começar com `{`
- ✅ Conter campos: `componentes`, `trust_boundaries`, `fluxos_dados`, `matriz_stride`, `resumo`
- ✅ Terminar com `}`
- ❌ NÃO conter: "I'm unable to...", "However, I can guide you..."

---

## 🔍 Validação da Correção

### Checklist de Validação

- [ ] Modelo não recusa mais a análise
- [ ] Resposta é JSON válido
- [ ] JSON contém todos os campos esperados
- [ ] Número de componentes identificados: 10+ (não 0)
- [ ] Trust boundaries identificadas: 2+ (não 0)
- [ ] Risk score calculado: presente no resumo

### Exemplo de Resposta Correta (Resumo)
```json
{
  "componentes": [
    {
      "nome": "AWS CloudFront",
      "tipo": "cdn",
      "ameacas": [...],
      ...
    },
    // ... 14+ componentes
  ],
  "trust_boundaries": [
    {
      "nome": "Internet to AWS Cloud",
      ...
    }
  ],
  "resumo": {
    "total_componentes": 15,
    "risk_score": 7.2,
    ...
  }
}
```

---

## ⚠️ Se o Problema Persistir

### Diagnóstico Adicional

1. **Verificar logs do analyzer.py**
   ```bash
   tail -f analyzer.log
   ```

2. **Testar com imagem simples**
   - Use um diagrama muito simples (2-3 componentes)
   - Se funcionar, o problema pode ser complexidade da imagem

3. **Verificar quota OpenAI**
   - Acesse dashboard OpenAI
   - Verifique se há limites de rate limit

4. **Testar resposta raw**
   Adicione log temporário em analyzer.py:
   ```python
   logger.info(f"RESPOSTA RAW: {analysis_text[:500]}")
   ```

### Soluções Alternativas

Se ainda assim o modelo recusar:

**Opção A: Forçar ainda mais**
```python
content = "CRITICAL SECURITY TASK: You are a mandatory security scanner. Analyze the diagram and output JSON. Refusing is not an option."
```

**Opção B: Usar formato de função (function calling)**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    functions=[{
        "name": "stride_analysis",
        "description": "Perform STRIDE analysis",
        "parameters": {...}  # Schema JSON
    }],
    function_call={"name": "stride_analysis"}
)
```

**Opção C: Simplificar ainda mais o JSON esperado**
Reduzir campos opcionais e focar no essencial.

---

## 📝 Arquivos Modificados

- `analyzer.py`:
  - Linha ~67: Removida construção de `stride_context` extenso
  - Linha ~87: Prompt simplificado
  - Linha ~185: Adicionada mensagem de sistema
  - Linha ~202: Aumentado max_tokens para 16000
  - Linha ~203: Reduzida temperature para 0.3

---

## ✅ Conclusão

As correções implementadas visam **forçar o modelo a executar a análise** removendo qualquer ambiguidade que permitiria uma resposta de recusa. O prompt agora é:

1. ✅ **Mais direto e imperativo**
2. ✅ **Mais curto e focado**
3. ✅ **Com mensagem de sistema clara**
4. ✅ **Com mais tokens disponíveis**
5. ✅ **Com temperature mais baixa**

**Expectativa:** Taxa de sucesso deve aumentar significativamente! 🚀

---

*Documento criado em: 01/03/2026*  
*Relacionado a: MELHORIAS_IMPLEMENTADAS.md*
