# Relatorios de Exemplo

Diretorio para relatorios PDF gerados pelo STRIDE Threat Analyzer.

## Como Gerar

### Via Interface Web
1. Acesse http://localhost:8501
2. Faca upload de um diagrama de arquitetura
3. Clique em "Analisar Ameacas"
4. Clique em "Gerar Relatorio PDF"
5. Baixe o PDF

### Via API REST
```bash
curl -X POST "http://localhost:8000/analyze-pdf" \
  -F "image=@examples/test_diagram.png" \
  -o relatorio_stride.pdf
```

## Estrutura do Relatorio

1. Capa com informacoes do relatorio
2. Sumario executivo com metricas e grafico de severidade
3. Diagrama de arquitetura analisado
4. Analise detalhada por componente (ameacas + contramedidas)
5. Fluxos de dados e comunicacao
6. Recomendacoes gerais de seguranca
7. Matriz STRIDE panoramica
8. Trust boundaries (fronteiras de confianca)
9. Sobre a metodologia STRIDE

> Nota: PDFs gerados sao ignorados pelo `.gitignore` para manter o repositorio limpo.
