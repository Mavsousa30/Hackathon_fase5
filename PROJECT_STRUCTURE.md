# Estrutura do Projeto STRIDE Threat Analyzer

Este documento descreve a organização dos arquivos e o fluxo de processamento do projeto.

## Estrutura de Diretorios

```
Hackathon_fase5/
├── README.md                  # Documentacao principal do projeto
├── PROJECT_STRUCTURE.md       # Este arquivo
├── requirements.txt           # Dependencias Python
├── .env.example               # Exemplo de configuracao
├── .gitignore                 # Arquivos ignorados pelo Git
├── .python-version            # Versao do Python
│
├── main.py                    # API REST (FastAPI)
├── app.py                     # Interface Web (Streamlit)
├── analyzer.py                # Motor de analise com GPT-4o Vision
├── stride_knowledge.py        # Base de conhecimento STRIDE + enriquecimento
├── pdf_generator.py           # Gerador de relatorios PDF (ReportLab)
├── test_analyzer.py           # Script de testes e demonstracao
│
├── docs/                      # Documentacao
│   ├── README.md              # Indice da documentacao
│   ├── QUICKSTART.md          # Guia de inicio rapido
│   ├── IADT - Fase 5 - Hackaton.pdf  # Especificacao do hackathon
│   └── reports/               # Relatorios PDF de exemplo
│       └── README.md
│
└── examples/                  # Diagramas de exemplo para testes
    ├── README.md
    └── test_diagram.png
```

## Fluxo de Processamento

O pipeline completo de analise segue este fluxo:

```
┌──────────────────┐
│  Usuario faz     │
│  upload do       │
│  diagrama (.png) │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   app.py         │  Interface Streamlit (porta 8501)
│   (Streamlit)    │  Recebe imagem, exibe resultados
└────────┬─────────┘
         │ POST /analyze
         ▼
┌──────────────────┐
│   main.py        │  API REST FastAPI (porta 8000)
│   (FastAPI)      │  Valida arquivo, salva temporario
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  analyzer.py     │  Motor de Analise
│  (GPT-4o Vision) │  1. Codifica imagem em base64
│                  │  2. Envia para GPT-4o com prompt STRIDE
│                  │  3. Parseia resposta JSON
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│stride_knowledge  │  Enriquecimento com Knowledge Base
│      .py         │  1. Complementa categorias STRIDE faltantes
│                  │  2. Adiciona descricoes e impactos detalhados
│                  │  3. Recalcula metricas do resumo
│                  │  4. Atualiza matriz STRIDE
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│pdf_generator.py  │  Geracao de Relatorio PDF
│  (ReportLab)     │  Capa, sumario, graficos, analise
│                  │  detalhada, matriz, trust boundaries
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Relatorio PDF   │  17+ paginas com analise completa
│  + JSON          │  Download via interface web
└──────────────────┘
```

## Descricao dos Modulos

### `analyzer.py` - Motor de Analise com IA

- Recebe caminho da imagem do diagrama de arquitetura
- Codifica em base64 e envia para GPT-4o Vision
- Prompt exaustivo solicita minimo 10 componentes, 3 trust boundaries, 5 fluxos
- Identifica componentes, ameacas STRIDE, contramedidas, fluxos de dados
- Apos receber resposta do LLM, chama `enrich_analysis()` para complementar
- Retorna JSON estruturado com analise completa

### `stride_knowledge.py` - Base de Conhecimento e Enriquecimento

- `STRIDE_PER_COMPONENT_TYPE`: mapeamento de 18 tipos de componente para ameacas STRIDE
- `_ENRICHED_DESCRIPTIONS`: descricoes detalhadas por categoria+tipo (108 combinacoes)
- `_ENRICHED_IMPACTS`: impactos contextualizados por categoria+tipo
- `enrich_analysis()`: complementa categorias STRIDE faltantes na analise do LLM
- `_find_matrix_key()`: evita duplicatas na matriz STRIDE por correspondencia de nomes
- `COUNTERMEASURES`: contramedidas padrao por categoria STRIDE

### `pdf_generator.py` - Gerador de Relatorios

- Classe `STRIDEReportGenerator` baseada em ReportLab
- Gera capa profissional, sumario executivo com grafico de pizza
- Analise detalhada por componente com ameacas e contramedidas
- Secoes: fluxos de dados, recomendacoes, matriz STRIDE, trust boundaries
- Numeracao de paginas automatica

### `main.py` - API REST

- `POST /analyze`: recebe imagem, retorna analise JSON
- `POST /analyze-pdf`: recebe imagem, retorna relatorio PDF
- `GET /health`: health check
- `GET /stride-info`: informacoes sobre a metodologia STRIDE
- Validacao de tipo e tamanho de arquivo (max 10MB)

### `app.py` - Interface Web

- Upload de imagem com preview
- Botao de analise com spinner de progresso
- Exibicao de resultados JSON
- Download de relatorio JSON e PDF
- Sidebar com status da API e dicas de uso

## Pontos de Entrada

| Comando | Componente | Porta | Descricao |
|---------|-----------|-------|-----------|
| `uvicorn main:app --reload` | API | 8000 | Inicia servidor FastAPI |
| `streamlit run app.py` | Web UI | 8501 | Inicia interface Streamlit |
| `python analyzer.py <imagem>` | CLI | - | Analise direta via terminal |
| `python test_analyzer.py` | Testes | - | Executa testes do sistema |

## Dependencias Principais

Definidas em `requirements.txt`:

| Pacote | Uso |
|--------|-----|
| `openai` | Integracao com GPT-4o Vision |
| `fastapi` | Framework para API REST |
| `uvicorn` | Servidor ASGI |
| `streamlit` | Interface web interativa |
| `pillow` | Processamento de imagens |
| `reportlab` | Geracao de PDFs |
| `python-dotenv` | Variaveis de ambiente |
| `requests` | Requisicoes HTTP |

## Arquivos Nao Versionados

- `.env` - Contem API keys (nunca commitar)
- `venv/` - Ambiente virtual Python
- `__pycache__/` - Cache de bytecode
- `*.log` - Logs de execucao
- `*.pdf` - Relatorios gerados (exceto especificacao do hackathon)

---

**Versao do projeto**: MVP Completo
**Status**: Producao
