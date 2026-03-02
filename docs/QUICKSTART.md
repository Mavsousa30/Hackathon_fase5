# Guia de Inicio Rapido - STRIDE Threat Analyzer

## Pre-requisitos

- Python 3.8+
- Conta OpenAI com acesso a GPT-4o Vision
- ~500 MB de espaco em disco

## Instalacao

### 1. Configure o Ambiente Virtual

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
# venv\Scripts\activate
```

### 2. Instale as Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configure a Chave da API OpenAI

```bash
cp .env.example .env
```

Edite o `.env` e adicione sua chave:

```
OPENAI_API_KEY=sk-sua-chave-aqui
```

> Obter chave: https://platform.openai.com/api-keys

## Como Usar

### Interface Web (Recomendado)

Abra dois terminais na pasta do projeto:

**Terminal 1 - API:**
```bash
source venv/bin/activate
uvicorn main:app --reload
```
API disponivel em http://localhost:8000 (docs: http://localhost:8000/docs)

**Terminal 2 - Interface Web:**
```bash
source venv/bin/activate
streamlit run app.py
```
Interface disponivel em http://localhost:8501

**Usando a interface:**
1. Faca upload de um diagrama de arquitetura (PNG, JPG ou JPEG)
2. Clique em "Analisar Ameacas"
3. Aguarde a analise (pode levar ate 2 minutos)
4. Baixe o relatorio em JSON ou PDF

### API REST

```bash
# Health check
curl http://localhost:8000/health

# Analisar imagem (retorna JSON)
curl -X POST "http://localhost:8000/analyze" \
  -F "image=@examples/test_diagram.png"

# Analisar e gerar PDF
curl -X POST "http://localhost:8000/analyze-pdf" \
  -F "image=@examples/test_diagram.png" \
  -o relatorio_stride.pdf
```

### Script Python Direto

```bash
python analyzer.py examples/test_diagram.png
```

Ou programaticamente:

```python
from analyzer import analyze_architecture
import json

result = analyze_architecture("examples/test_diagram.png")

if result["success"]:
    print(json.dumps(result["analysis"], indent=2, ensure_ascii=False))
else:
    print(f"Erro: {result['error']}")
```

## Troubleshooting

| Erro | Solucao |
|------|---------|
| "Module not found" | `pip install -r requirements.txt` |
| "API key not found" | Verifique o arquivo `.env` |
| "API nao respondendo" | Inicie a API: `uvicorn main:app --reload` |
| "Timeout na analise" | A imagem pode ser muito complexa, tente uma menor |

## Custos Estimados

- ~$0.02-0.05 por analise (tokens GPT-4o Vision)
- Monitore em: https://platform.openai.com/usage
