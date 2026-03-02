# 🔒 Analisador de Ameaças STRIDE com IA

Sistema de análise automática de diagramas de arquitetura de software usando a metodologia STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) com GPT-4o Vision.

> **🎯 TL;DR**: Upload de um diagrama de arquitetura → IA analisa com metodologia STRIDE → Relatório PDF com ameaças e contramedidas

**Status**: ✅ MVP Completo e Funcional | **Fase**: 6/7 | **Stack**: Python + FastAPI + Streamlit + GPT-4o Vision

## 📋 Índice

- [Projeto](#-projeto)
- [Funcionalidades](#-funcionalidades)
- [Requisitos do Sistema](#-requisitos-do-sistema)
- [Instalação](#-instalação)
- [Uso](#-uso)
  - [Interface Web](#opção-1-interface-web-recomendado-)
  - [API REST](#opção-2-api-rest-)
  - [Script Python](#opção-3-script-python-direto-)
- [Metodologia STRIDE](#-o-que-é-stride)
- [Formato da Análise](#-formato-da-análise)
- [Documentação](#-documentação)
- [Dependências](#-dependências-principais)
- [Próximos Passos](#-próximos-passos)
- [Troubleshooting](#-troubleshooting)
- [Autor](#-autor)
- [Licença](#-licença)

## 📋 Projeto

Este projeto foi desenvolvido para o **Hackathon FIAP Fase 5** e utiliza Inteligência Artificial para identificar ameaças de segurança em arquiteturas de software.

## 🎯 Funcionalidades

- ✅ **FASE 1**: Setup do projeto e configuração de ambiente
- ✅ **FASE 2**: Base de conhecimento STRIDE implementada
- ✅ **FASE 3**: Análise de arquitetura com GPT-4o Vision
- ✅ **FASE 4**: API REST com FastAPI
- ✅ **FASE 5**: Interface Web com Streamlit
- ✅ **FASE 6**: Geração de Relatórios PDF
- 🔄 **FASE 7**: Testes e documentação completa

## 📋 Requisitos do Sistema

### Software Necessário

- **Python**: 3.8 ou superior
- **pip**: Gerenciador de pacotes Python
- **Conta OpenAI**: Com acesso a GPT-4o
- **Sistema Operacional**: macOS, Linux ou Windows

### Dependências Python

Todas as dependências estão listadas em `requirements.txt`:
- openai (>=1.0.0)
- fastapi (>=0.100.0)
- uvicorn (>=0.23.0)
- streamlit (>=1.28.0)
- pillow (>=10.0.0)
- reportlab (>=4.0.0)
- python-dotenv (>=1.0.0)
- requests (>=2.31.0)

### Recursos Estimados

- **Espaço em disco**: ~500 MB (com dependências)
- **RAM**: Mínimo 2 GB, recomendado 4 GB
- **Internet**: Necessária para API OpenAI
- **Custo estimado**: ~$0.02-0.05 por análise (GPT-4o)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/Mavsousa30/Hackathon_fase5.git
cd Hackathon_fase5
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # No macOS/Linux
# ou
venv\Scripts\activate  # No Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a chave da API OpenAI

Copie o arquivo de exemplo e configure sua chave:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da API OpenAI:

```
OPENAI_API_KEY=sk-sua-chave-aqui
```

> 🔑 Obtenha sua chave em: https://platform.openai.com/api-keys

## 💻 Uso

### Opção 1: Interface Web (Recomendado) 🌐

A maneira mais fácil de usar o sistema é através da interface web com Streamlit:

#### 1. Inicie a API (Terminal 1)

```bash
uvicorn main:app --reload
```

A API estará disponível em: http://localhost:8000
- Documentação interativa: http://localhost:8000/docs
- Health check: http://localhost:8000/health

#### 2. Inicie a Interface Web (Terminal 2)

```bash
streamlit run app.py
```

A interface estará disponível em: http://localhost:8501

#### 3. Use a Interface

1. Faça upload de um diagrama de arquitetura (PNG, JPG ou JPEG)
2. Clique em "🚀 Analisar Ameaças"
3. Aguarde a análise da IA (10-20 segundos)
4. Revise as ameaças identificadas por componente
5. **Opções de download:**
   - Clique em "💾 Baixar Relatório (JSON)" para dados estruturados
   - Clique em "📄 Gerar Relatório PDF" para relatório profissional
   - Após gerar, clique em "⬇️ Baixar PDF Gerado"
6. Use "🔄 Nova Análise" para analisar outro diagrama

### Opção 2: API REST 🚀

Para integrar com outros sistemas, use a API REST:

#### Verificar saúde da API

```bash
curl http://localhost:8000/health
```

#### Analisar uma imagem (retorna JSON)

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@examples/arquitetura.png"
```

#### Analisar e gerar PDF diretamente

```bash
curl -X POST "http://localhost:8000/analyze-pdf" \
  -H "accept: application/pdf" \
  -F "image=@examples/arquitetura.png" \
  -o "relatorio_stride.pdf"
```

#### Obter informações sobre STRIDE

```bash
curl http://localhost:8000/stride-info
```

### Opção 3: Script Python Direto 🐍

Para analisar uma imagem de arquitetura diretamente:

```bash
python analyzer.py caminho/para/imagem.png
```

Exemplo:

```bash
python analyzer.py examples/arquitetura_exemplo.png
```

### Análise Programática

```python
from analyzer import analyze_architecture

# Analisar arquitetura
result = analyze_architecture("examples/arquitetura.png")

if result["success"]:
    print("Análise concluída!")
    print(result["analysis"])
else:
    print(f"Erro: {result['error']}")
```

## 📁 Estrutura do Projeto

```
hackathon-stride/
├── main.py                 # API REST FastAPI
├── app.py                  # Interface Web Streamlit
├── analyzer.py             # Análise com GPT-4o Vision
├── stride_knowledge.py     # Base de conhecimento STRIDE
├── test_analyzer.py        # Testes do analisador
├── requirements.txt        # Dependências Python
├── .env.example           # Exemplo de configuração
├── .gitignore             # Arquivos ignorados pelo git
├── README.md              # Esta documentação
├── QUICKSTART.md          # Guia rápido de início
├── PLANO_IMPLEMENTACAO_SIMPLIFICADO.md  # Plano de implementação
└── examples/              # Imagens de exemplo
    └── README.md          # Documentação dos exemplos
```

## 🛡️ Metodologia STRIDE

O sistema analisa diagramas de arquitetura aplicando as 6 categorias da metodologia STRIDE:

| Categoria | Descrição |
|-----------|-----------|
| **S** poofing | Falsificação de identidade |
| **T** ampering | Adulteração de dados |
| **R** epudiation | Negação de ações realizadas |
| **I** nformation Disclosure | Vazamento de informações |
| **D** enial of Service | Negação de serviço |
| **E** levation of Privilege | Elevação de privilégios |

## 🔍 O que o Sistema Faz

1. **Identifica Componentes**: Reconhece automaticamente componentes no diagrama (APIs, bancos de dados, usuários, servidores, etc)
2. **Aplica STRIDE**: Para cada componente, identifica ameaças nas 6 categorias
3. **Analisa Fluxos**: Identifica riscos nas comunicações entre componentes
4. **Sugere Contramedidas**: Propõe soluções práticas para cada ameaça
5. **Prioriza Riscos**: Classifica ameaças por criticidade (Alta, Média, Baixa)

## 📊 Formato da Análise

A análise retorna um JSON estruturado com:

```json
{
  "componentes": [...],
  "fluxos_dados": [...],
  "resumo": {
    "total_componentes": 5,
    "total_ameacas": 15,
    "ameacas_alta": 3,
    "ameacas_media": 8,
    "ameacas_baixa": 4
  },
  "recomendacoes_gerais": [...]
}
```

## 📚 Documentação

Este projeto possui documentação organizada no diretório [`docs/`](docs/):

- **[Quick Start](docs/QUICKSTART.md)** - Guia rápido para começar a usar
- **[Documento do Hackathon](docs/IADT%20-%20Fase%205%20-%20Hackaton.pdf)** - Documento oficial FIAP
- **[Relatórios de Exemplo](docs/reports/)** - PDFs de exemplo gerados pelo sistema

## �🔧 Dependências Principais

- **OpenAI** (>=1.0.0): Para GPT-4o Vision
- **FastAPI** (>=0.100.0): Framework para API REST
- **Uvicorn** (>=0.23.0): Servidor ASGI para FastAPI
- **Streamlit** (>=1.28.0): Interface web interativa
- **Pillow** (>=10.0.0): Processamento de imagens
- **python-dotenv** (>=1.0.0): Gerenciamento de variáveis de ambiente
- **requests** (>=2.31.0): Requisições HTTP

## 📝 Próximos Passos

- [x] Implementar API REST com FastAPI
- [x] Criar interface web com Streamlit
- [x] Gerar relatórios em PDF
- [ ] Adicionar testes automatizados completos
- [ ] Implementar cache de análises
- [ ] Adicionar suporte a múltiplos modelos de IA
- [ ] Deploy em produção (Docker/Cloud)

---

## 👥 Autor

Desenvolvido para o Hackathon FIAP Fase 5 - Modelagem de Ameaças com IA

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais no contexto do Hackathon FIAP.

---

## 🐛 Troubleshooting

#### Erro: "API não está respondendo"
- Verifique se a API está rodando: `curl http://localhost:8000/health`
- Inicie a API: `uvicorn main:app --reload`

#### Erro: "OPENAI_API_KEY não configurada"
- Verifique o arquivo `.env`
- Certifique-se de que a chave está correta

#### Erro: "Arquivo muito grande"
- Reduza o tamanho da imagem (máx. 10MB)
- Use ferramentas de compressão de imagem
