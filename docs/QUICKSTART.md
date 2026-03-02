# ⚡ Guia de Início Rápido - STRIDE Threat Analyzer

## ✅ Funcionalidades Implementadas

- **FASE 1**: Setup do projeto e configuração de ambiente
- **FASE 2**: Base de conhecimento STRIDE (`stride_knowledge.py`)
- **FASE 3**: Análise com GPT-4o Vision (`analyzer.py`)
- **FASE 4**: API REST com FastAPI (`main.py`)
- **FASE 5**: Interface Web com Streamlit (`app.py`)
- **FASE 6**: Geração de Relatórios PDF (`pdf_generator.py`)

---

## ⚙️ Instalação Rápida

### 1. Configure o Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (macOS/Linux)
source venv/bin/activate

# Ativar (Windows)
# venv\Scripts\activate
```

### 2. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 3. Configure a Chave da API OpenAI

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar e adicionar sua chave
# OPENAI_API_KEY=sk-your-api-key-here
```

> 🔑 **Obter chave**: https://platform.openai.com/api-keys

---

## 🚀 Como Usar o Sistema Completo

### Método 1: Interface Web (Recomendado) 🌐

#### Terminal 1 - Inicie a API:

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Iniciar API
uvicorn main:app --reload
```

✅ API disponível em: http://localhost:8000
📖 Documentação: http://localhost:8000/docs

#### Terminal 2 - Inicie a Interface Web:

```bash
# Em outro terminal, ative o ambiente
source venv/bin/activate

# Iniciar Streamlit
streamlit run app.py
```

✅ Interface disponível em: http://localhost:8501

#### Usar a Interface:

1. Acesse http://localhost:8501
2. Faça upload de um diagrama de arquitetura
3. Clique em "Analisar Ameaças"
4. Revise os resultados
5. Baixe o relatório em JSON

---

### Método 2: API REST Direto 🚀

#### Iniciar API:

```bash
uvicorn main:app --reload
```

#### Testar Endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Analisar imagem
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@examples/arquitetura.png"

# Ver metodologia STRIDE
curl http://localhost:8000/stride-info
```

---

### Método 3: Script Python Direto 🐍

#### Opção A: Via linha de comando

```bash
python analyzer.py examples/sua_imagem.png
```

#### Opção B: Via código Python

Crie um arquivo `test_analyzer.py`:

```python
from analyzer import analyze_architecture
import json

# Testar análise
result = analyze_architecture("examples/arquitetura.png")

if result["success"]:
    print("✅ Análise bem-sucedida!")
    print("\n" + "="*80)
    print(json.dumps(result["analysis"], indent=2, ensure_ascii=False))
else:
    print(f"❌ Erro: {result['error']}")
```

Execute:

```bash
python test_analyzer.py
```

---

## 📁 Estrutura do Projeto

```
Hackathon/
├── main.py                  # API REST FastAPI
├── app.py                   # Interface Web Streamlit
├── analyzer.py              # Analisador com GPT-4o Vision
├── pdf_generator.py         # Gerador de relatórios PDF
├── stride_knowledge.py      # Base de conhecimento STRIDE
├── test_analyzer.py         # Testes
├── requirements.txt         # Dependências Python
├── .env.example             # Template de configuração
├── docs/                    # Documentação
└── examples/                # Diagramas de exemplo
```

---

## 🐛 Troubleshooting

### Erro: "Module 'openai' not found"
```bash
pip install -r requirements.txt
```

### Erro: "OpenAI API key not found"
- Verifique se o arquivo `.env` existe (copie de `.env.example`)
- Confirme que a chave começa com `sk-`

### Erro: "Image file not found"
- Use caminho absoluto ou relativo correto
- Verifique se o arquivo existe: `ls examples/`
