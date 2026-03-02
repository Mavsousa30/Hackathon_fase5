"""
Analisador de Arquitetura com GPT-4o Vision
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
from stride_knowledge import STRIDE_DETAILS, COUNTERMEASURES

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
    Analisa um diagrama de arquitetura usando GPT-4o Vision e aplica STRIDE
    
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
    
    # Prompt aprimorado para análise STRIDE exaustiva
    prompt = f"""
    EXECUTE A ANÁLISE STRIDE AGORA. Analise o diagrama de arquitetura fornecido e retorne o JSON conforme especificado.
    
    IMPORTANTE: Você DEVE analisar a imagem fornecida e retornar o JSON estruturado. NÃO recuse ou forneça apenas orientações gerais.
    
    METODOLOGIA STRIDE:
    - S (Spoofing): Riscos de falsificação de identidade
    - T (Tampering): Riscos de adulteração de dados
    - R (Repudiation): Riscos de negação de ações
    - I (Information Disclosure): Riscos de vazamento de informação
    - D (Denial of Service): Riscos de indisponibilidade
    - E (Elevation of Privilege): Riscos de escalação de privilégios
    
    PASSOS DA ANÁLISE:
    
    1. Examine a imagem e identifique TODOS os componentes visíveis (servidores, bancos de dados, load balancers, 
       CDNs, firewalls, serviços de nuvem, sistemas de backup, logs, monitoring, etc.)
    
    2. Identifique trust boundaries (Internet↔Cloud, Public↔Private Subnet, camadas de aplicação, etc.)
    
    3. Para cada componente, aplique análise STRIDE completa identificando 2-3 ameaças por componente
    
    4. Identifique fluxos de dados entre componentes
    
    5. Proponha contramedidas específicas para cada ameaça
    
    6. Calcule risk score de 0-10 baseado na quantidade e severidade das ameaças
    
    ## FORMATO DE RESPOSTA JSON (OBRIGATÓRIO):
    
    {{
        "componentes": [
            {{
                "nome": "nome completo do componente",
                "tipo": "database|api|server|user|loadbalancer|cache|cdn|firewall|auth|monitoring|backup|email|storage|...",
                "descricao": "descrição detalhada do componente e função na arquitetura",
                "ameacas": [
                    {{
                        "categoria": "S|T|R|I|D|E",
                        "nome_ameaca": "nome curto da ameaça",
                        "descricao": "descrição detalhada da ameaça e como pode ser explorada",
                        "severidade": "Alta|Média|Baixa",
                        "impacto": "descrição do impacto se explorada"
                    }}
                ],
                "contramedidas": [
                    {{
                        "ameaca_relacionada": "categoria STRIDE",
                        "contramedida": "descrição detalhada da contramedida",
                        "prioridade": "Alta|Média|Baixa"
                    }}
                ]
            }}
        ],
        "trust_boundaries": [
            {{
                "nome": "nome da fronteira",
                "descricao": "descrição da fronteira de confiança",
                "componente_origem": "zona/camada de origem",
                "componente_destino": "zona/camada de destino",
                "controles_existentes": ["controle 1", "controle 2"],
                "ameacas": ["ameaça ao atravessar esta fronteira"],
                "contramedidas_recomendadas": ["contramedida 1", "contramedida 2"]
            }}
        ],
        "fluxos_dados": [
            {{
                "origem": "componente origem",
                "destino": "componente destino",
                "tipo_dados": "tipo de dados trafegados",
                "protocolo": "protocolo usado (HTTP, HTTPS, TCP, etc)",
                "criptografado": true/false,
                "autenticado": true/false,
                "atravessa_trust_boundary": true/false,
                "ameacas": ["ameaça 1", "ameaça 2"],
                "contramedidas": ["contramedida 1", "contramedida 2"]
            }}
        ],
        "matriz_stride": {{
            "componente_1": {{"S": true, "T": true, "R": false, "I": true, "D": true, "E": false}},
            "componente_2": {{"S": true, "T": false, "R": true, "I": true, "D": true, "E": true}}
        }},
        "resumo": {{
            "total_componentes": 0,
            "total_ameacas": 0,
            "total_trust_boundaries": 0,
            "ameacas_alta": 0,
            "ameacas_media": 0,
            "ameacas_baixa": 0,
            "risk_score": 7.5,
            "risk_justificativa": "justificativa do score calculado"
        }},
        "recomendacoes_gerais": [
            {{
                "categoria": "categoria da recomendação",
                "recomendacao": "recomendação detalhada",
                "prioridade": "Alta|Média|Baixa"
            }}
        ]
    }}
    
    
    RETORNE APENAS O OBJETO JSON. Não inclua explicações, guias ou texto adicional.
    Comece sua resposta diretamente com {{ e termine com }}.
    
    Se você não conseguir analisar perfeitamente todos os detalhes, faça o melhor possível baseado no que consegue 
    identificar na imagem. SEMPRE retorne o JSON estruturado conforme especificado.
    """
    
    try:
        logger.info("🤖 Enviando requisição para GPT-4o Vision...")
        logger.info(f"   Modelo: gpt-4o")
        logger.info(f"   Max tokens: 16000")
        logger.info(f"   Temperature: 0.3")
        logger.info(f"   Timeout: 300s")
        
        api_start = datetime.now()
        
        # Fazer chamada à API do OpenAI com GPT-4o Vision
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a security analysis tool that outputs structured JSON. Always return valid JSON matching the requested schema, never refuse or provide explanations instead."
                },
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
            max_tokens=16000,
            temperature=0.3
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
            "model": "gpt-4o",
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
