"""
Analisador de Arquitetura com GPT-5-mini Vision
Aplica a metodologia STRIDE em diagramas de arquitetura
"""

import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
import json
from openai import APITimeoutError, APIError
import logging
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('analyzer.log')
    ]
)
logger = logging.getLogger(__name__)

# Inicializar cliente OpenAI com timeout aumentado
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=300.0,  # 5 minutos de timeout
    max_retries=2
)


def analyze_architecture(image_path: str) -> dict:
    """
    Analisa um diagrama de arquitetura usando GPT-5-mini Vision e aplica STRIDE
    
    Args:
        image_path: Caminho para o arquivo de imagem da arquitetura
        
    Returns:
        dict: Resultado da análise com ameaças identificadas e contramedidas
    """
    
    start_time = datetime.now()
    logger.info(f"🚀 Iniciando análise do arquivo: {image_path}")
    
    # Ler e codificar a imagem
    try:
        logger.info("📂 Lendo arquivo de imagem...")
        with open(image_path, "rb") as f:
            image_data = f.read()
            image_size_mb = len(image_data) / (1024 * 1024)
            logger.info(f"✅ Imagem carregada: {image_size_mb:.2f} MB")
            image_base64 = base64.b64encode(image_data).decode()
            logger.info(f"✅ Imagem codificada em base64: {len(image_base64)} caracteres")
    except FileNotFoundError:
        logger.error(f"❌ Arquivo não encontrado: {image_path}")
        return {"error": f"Arquivo não encontrado: {image_path}"}
    except Exception as e:
        logger.error(f"❌ Erro ao ler arquivo: {str(e)}")
        return {"error": f"Erro ao ler arquivo: {str(e)}"}
    
    # Prompt para análise STRIDE
    prompt = """
    Analise este diagrama de arquitetura de software e aplique a metodologia STRIDE de modelagem de ameaças.
    
    Siga estas instruções:
    
    1. **Identificação de Componentes**: Liste todos os componentes visíveis no diagrama (usuários, servidores, bancos de dados, APIs, serviços externos, redes, etc)
    
    2. **Análise STRIDE por Componente**: Para cada componente identificado, analise as seguintes categorias:
       - **S (Spoofing)**: Ameaças de falsificação de identidade
       - **T (Tampering)**: Ameaças de adulteração de dados
       - **R (Repudiation)**: Ameaças de repúdio/negação de ações
       - **I (Information Disclosure)**: Ameaças de vazamento de informações
       - **D (Denial of Service)**: Ameaças de negação de serviço
       - **E (Elevation of Privilege)**: Ameaças de elevação de privilégio
    
    3. **Análise de Fluxos de Dados**: Identifique os fluxos de dados entre componentes e possíveis ameaças nessas comunicações
    
    4. **Contramedidas**: Para cada ameaça identificada, sugira contramedidas específicas e práticas
    
    5. **Priorização**: Classifique as ameaças por criticidade (Alta, Média, Baixa)
    
    Estruture a resposta em formato JSON com a seguinte estrutura:
    {
        "componentes": [
            {
                "nome": "nome do componente",
                "tipo": "tipo do componente (ex: database, api, user, server)",
                "descricao": "breve descrição do componente e sua função na arquitetura",
                "ameacas": [
                    {
                        "categoria": "S/T/R/I/D/E",
                        "descricao": "descrição detalhada da ameaça",
                        "severidade": "Alta/Média/Baixa"
                    }
                ],
                "contramedidas": ["contramedida 1", "contramedida 2", "contramedida 3"]
            }
        ],
        "fluxos_dados": [
            {
                "origem": "componente origem",
                "destino": "componente destino",
                "ameacas": ["ameaça 1", "ameaça 2"],
                "contramedidas": ["contramedida 1", "contramedida 2"]
            }
        ],
        "resumo": {
            "total_componentes": 0,
            "total_ameacas": 0,
            "ameacas_alta": 0,
            "ameacas_media": 0,
            "ameacas_baixa": 0
        },
        "recomendacoes_gerais": ["recomendação 1", "recomendação 2"]
    }
    
    Seja específico e detalhado nas análises. Considere as melhores práticas de segurança atuais.
    """
    
    try:
        logger.info("🤖 Enviando requisição para GPT-4o-mini Vision...")
        logger.info(f"   Modelo: gpt-4o-mini")
        logger.info(f"   Max tokens: 8192")
        logger.info(f"   Temperature: 1")
        logger.info(f"   Timeout: 300s")
        
        api_start = datetime.now()
        
        # Fazer chamada à API do OpenAI com GPT-4o-mini Vision
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=8192,
            temperature=0.5
        )
        
        api_duration = (datetime.now() - api_start).total_seconds()
        logger.info(f"✅ Resposta recebida da API em {api_duration:.2f}s")
        
        # Extrair resposta
        analysis_text = response.choices[0].message.content
        logger.info(f"📝 Resposta recebida: {len(analysis_text)} caracteres")
        logger.info(f"   Primeiros 100 caracteres: {analysis_text[:100]}...")
        
        # Tentar parsear como JSON
        logger.info("🔍 Tentando parsear resposta como JSON...")
        try:
            # Procurar por JSON na resposta
            if "```json" in analysis_text:
                logger.info("   Detectado bloco de código JSON com markdown")
                json_start = analysis_text.find("```json") + 7
                json_end = analysis_text.find("```", json_start)
                json_str = analysis_text[json_start:json_end].strip()
                analysis_json = json.loads(json_str)
                logger.info("✅ JSON parseado com sucesso (de bloco markdown)")
            elif analysis_text.strip().startswith("{"):
                logger.info("   Detectado JSON direto")
                analysis_json = json.loads(analysis_text)
                logger.info("✅ JSON parseado com sucesso (direto)")
            else:
                logger.warning("⚠️  Resposta não é JSON, retornando como texto")
                # Se não for JSON, retornar como texto
                analysis_json = {
                    "analysis_text": analysis_text,
                    "note": "Análise retornada em formato texto"
                }
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erro ao parsear JSON: {str(e)}")
            # Se falhar o parse, retornar como texto
            analysis_json = {
                "analysis_text": analysis_text,
                "note": "Não foi possível parsear como JSON"
            }
        
        total_duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Análise completa em {total_duration:.2f}s")
        logger.info(f"   Componentes encontrados: {len(analysis_json.get('componentes', []))}")
        
        return {
            "success": True,
            "analysis": analysis_json,
            "model": "gpt-4o-mini",
            "image_path": image_path
        }
    
    except APITimeoutError:
        logger.error(f"⏱️  TIMEOUT após {(datetime.now() - start_time).total_seconds():.2f}s")
        return {
            "success": False,
            "error": "Timeout na análise. A imagem pode ser muito complexa ou o serviço está sobrecarregado. Tente novamente ou use uma imagem mais simples."
        }
    except APIError as e:
        logger.error(f"❌ Erro da API: {str(e)}")
        return {
            "success": False,
            "error": f"Erro da API OpenAI: {str(e)}"
        }    
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": f"Erro na análise: {str(e)}"
        }


def analyze_architecture_simple(image_path: str) -> str:
    """
    Versão simplificada que retorna apenas o texto da análise
    
    Args:
        image_path: Caminho para o arquivo de imagem
        
    Returns:
        str: Texto da análise
    """
    logger.info(f"📋 analyze_architecture_simple chamado para: {image_path}")
    result = analyze_architecture(image_path)
    
    if not result.get("success", False):
        return f"Erro: {result.get('error', 'Erro desconhecido')}"
    
    analysis = result.get("analysis", {})
    
    if "analysis_text" in analysis:
        return analysis["analysis_text"]
    
    # Se for JSON, formatar de forma legível
    return json.dumps(analysis, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # Teste do analisador
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python analyzer.py <caminho_imagem>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    logger.info("="*80)
    logger.info(f"MODO DE TESTE - Analisando: {image_path}")
    logger.info("="*80)
    
    result = analyze_architecture(image_path)
    
    if result.get("success"):
        logger.info("="*80)
        logger.info("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
        logger.info("="*80)
        print("\nResultado:")
        print(json.dumps(result["analysis"], indent=2, ensure_ascii=False))
    else:
        logger.error("="*80)
        logger.error(f"❌ ERRO NA ANÁLISE: {result.get('error')}")
        logger.error("="*80)
