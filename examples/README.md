# Diagramas de Exemplo

Coloque diagramas de arquitetura de software nesta pasta para analise com o STRIDE Threat Analyzer.

## Formatos aceitos
- PNG, JPG, JPEG
- Tamanho maximo: 10MB
- Resolucao recomendada: minimo 800x600 pixels

## Dicas para melhores resultados
- Componentes claramente identificados (APIs, servidores, bancos de dados)
- Conexoes/fluxos visiveis com setas
- Rotulos legiveis nos componentes
- Trust boundaries demarcadas (se possivel)

## Como analisar

```bash
# Via interface web (recomendado)
streamlit run app.py

# Via linha de comando
python analyzer.py examples/test_diagram.png
```

## Arquivo incluido
- `test_diagram.png` - Diagrama de teste para validacao do sistema
