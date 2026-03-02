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
    
    # Importar conhecimento STRIDE para enriquecer o prompt e a análise
    from stride_knowledge import STRIDE_DETAILS, COUNTERMEASURES, STRIDE_PER_COMPONENT_TYPE, enrich_analysis

    # Listar tipos de componentes conhecidos para guiar a detecção
    tipos_conhecidos = list(STRIDE_PER_COMPONENT_TYPE.keys())

    # Prompt aprimorado para análise STRIDE exaustiva
    prompt = f"""
    EXECUTE A ANÁLISE STRIDE COMPLETA E EXAUSTIVA. Analise o diagrama de arquitetura fornecido e retorne o JSON.

    IMPORTANTE: Você DEVE analisar a imagem e identificar ABSOLUTAMENTE TODOS os componentes visíveis.
    NÃO OMITA nenhum componente. Em arquiteturas cloud típicas existem 10-20+ componentes.

    REGRAS OBRIGATÓRIAS:
    - Identifique no MÍNIMO 10 componentes (arquiteturas cloud possuem tipicamente 12-20+)
    - Cada componente DEVE ter ameaças de pelo menos 2-3 categorias STRIDE DIFERENTES
    - Identifique pelo menos 3 trust boundaries
    - Identifique pelo menos 5 fluxos de dados
    - Forneça pelo menos 5 recomendações gerais

    TIPOS DE COMPONENTES QUE VOCÊ DEVE PROCURAR (identifique TODOS que estiverem presentes):
    - Usuários/Clientes/Browsers/Mobile Apps (user)
    - Load Balancers - ALB, NLB, ELB, Azure LB (loadbalancer)
    - Servidores de Aplicação - EC2, App Service, ECS, Lambda (server)
    - Bancos de Dados Primários - RDS Primary, Aurora, SQL Server (database)
    - Bancos de Dados Réplica/Secondary - RDS Read Replica, Standby, Secondary (database)
    - APIs e API Gateways - API Gateway, APIM, Kong (api, gateway)
    - CDNs - CloudFront, Akamai, Azure CDN (cdn)
    - Firewalls e WAFs - AWS WAF, Azure WAF, Firewall (firewall, waf)
    - Serviços de Cache - ElastiCache, Redis, Memcached (cache)
    - Filas de Mensagem - SQS, SNS, RabbitMQ, Kafka, Service Bus (queue)
    - Armazenamento de Objetos - S3, Blob Storage (storage)
    - Armazenamento de Arquivos - EFS, FSx, Azure Files (storage)
    - Serviços de Autenticação - IAM, Entra ID, Cognito, Active Directory (auth)
    - Monitoramento - CloudWatch, CloudTrail, App Insights, X-Ray (monitoring)
    - Email - SES, SendGrid, Exchange (email)
    - Backup - AWS Backup, Azure Backup, Snapshots (backup)
    - Criptografia/KMS - AWS KMS, Key Vault, HSM, Certificate Manager (encryption)
    - Proteção DDoS - AWS Shield, Azure DDoS Protection (security)
    - Orquestração - Logic Apps, Step Functions, EventBridge (server)
    - Developer Portal, Swagger/OpenAPI endpoints (api)
    - DNS - Route 53, Azure DNS, CloudFlare (server)
    - VPC/VNet, Subnets, Security Groups, NSGs (firewall)

    IMPORTANTE: Se existirem réplicas, instâncias secondary ou standby de bancos de dados,
    liste-as como componentes SEPARADOS (ex: "Amazon RDS Primary" e "Amazon RDS Read Replica").

    METODOLOGIA STRIDE:
    - S (Spoofing): Falsificação de identidade → Foco: Autenticação
    - T (Tampering): Adulteração de dados → Foco: Integridade
    - R (Repudiation): Negação de ações → Foco: Não-repúdio/Auditoria
    - I (Information Disclosure): Vazamento de informação → Foco: Confidencialidade
    - D (Denial of Service): Indisponibilidade → Foco: Disponibilidade
    - E (Elevation of Privilege): Escalação de privilégios → Foco: Autorização

    TRUST BOUNDARIES COMUNS A IDENTIFICAR:
    - Internet ↔ Rede Cloud (Edge/Perímetro)
    - Zona Pública (Public Subnet) ↔ Zona Privada (Private Subnet)
    - Camada de Aplicação ↔ Camada de Dados
    - VPC/VNet ↔ Serviços Gerenciados Externos
    - Diferentes Availability Zones ou Regiões
    - Rede Interna ↔ Serviços de Terceiros (SaaS)

    FORMATO DE RESPOSTA JSON (OBRIGATÓRIO):

    {{
        "componentes": [
            {{
                "nome": "nome completo do componente (ex: Amazon RDS Primary)",
                "tipo": "{"|".join(tipos_conhecidos)}",
                "descricao": "descrição detalhada da função na arquitetura",
                "ameacas": [
                    {{
                        "categoria": "S|T|R|I|D|E",
                        "nome_ameaca": "nome curto e específico da ameaça",
                        "descricao": "como a ameaça pode ser explorada neste componente específico",
                        "severidade": "Alta|Média|Baixa",
                        "impacto": "impacto concreto se explorada"
                    }}
                ],
                "contramedidas": [
                    {{
                        "ameaca_relacionada": "S|T|R|I|D|E",
                        "contramedida": "contramedida técnica específica",
                        "prioridade": "Alta|Média|Baixa"
                    }}
                ]
            }}
        ],
        "trust_boundaries": [
            {{
                "nome": "nome descritivo (ex: Internet↔AWS Cloud)",
                "descricao": "descrição da fronteira e por que é crítica",
                "componente_origem": "zona/camada de origem",
                "componente_destino": "zona/camada de destino",
                "controles_existentes": ["controle 1", "controle 2"],
                "ameacas": ["ameaça específica nesta fronteira"],
                "contramedidas_recomendadas": ["contramedida 1", "contramedida 2"]
            }}
        ],
        "fluxos_dados": [
            {{
                "origem": "componente origem",
                "destino": "componente destino",
                "tipo_dados": "tipo de dados (ex: credenciais, dados de negócio, logs)",
                "protocolo": "HTTPS|HTTP|TCP|TLS|gRPC|AMQP|etc",
                "criptografado": true,
                "autenticado": true,
                "atravessa_trust_boundary": true,
                "ameacas": ["ameaça específica neste fluxo"],
                "contramedidas": ["contramedida para este fluxo"]
            }}
        ],
        "matriz_stride": {{
            "Nome Componente": {{"S": true, "T": true, "R": false, "I": true, "D": true, "E": false}}
        }},
        "resumo": {{
            "total_componentes": 0,
            "total_ameacas": 0,
            "total_trust_boundaries": 0,
            "ameacas_alta": 0,
            "ameacas_media": 0,
            "ameacas_baixa": 0,
            "risk_score": 7.5,
            "risk_justificativa": "justificativa detalhada do score baseada na análise"
        }},
        "recomendacoes_gerais": [
            {{
                "categoria": "Autenticação|Criptografia|Monitoramento|Rede|Dados|Acesso|Resiliência|Compliance",
                "recomendacao": "recomendação técnica detalhada e acionável",
                "prioridade": "Alta|Média|Baixa"
            }}
        ]
    }}


    RETORNE APENAS O OBJETO JSON. Não inclua explicações, guias ou texto adicional.
    Comece sua resposta diretamente com {{ e termine com }}.

    LEMBRE-SE: Identifique TODOS os componentes (mínimo 10), com MÚLTIPLAS ameaças STRIDE cada (mínimo 2-3 categorias diferentes por componente).
    Inclua réplicas, instâncias secondary e serviços auxiliares como componentes separados.
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
        
        # Enriquecer análise com knowledge base STRIDE
        if isinstance(analysis_json, dict) and 'componentes' in analysis_json:
            logger.info("🔧 Enriquecendo análise com knowledge base STRIDE...")
            componentes_antes = len(analysis_json.get('componentes', []))
            ameacas_antes = sum(len(c.get('ameacas', [])) for c in analysis_json.get('componentes', []))

            analysis_json = enrich_analysis(analysis_json)

            ameacas_depois = sum(len(c.get('ameacas', [])) for c in analysis_json.get('componentes', []))
            logger.info(f"   Componentes: {componentes_antes}")
            logger.info(f"   Ameaças antes do enriquecimento: {ameacas_antes}")
            logger.info(f"   Ameaças após enriquecimento: {ameacas_depois}")
            logger.info(f"   Ameaças adicionadas pelo knowledge base: {ameacas_depois - ameacas_antes}")

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
