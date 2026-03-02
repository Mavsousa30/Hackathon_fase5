"""
Base de Conhecimento STRIDE - Metodologia de Modelagem de Ameaças
Utilizada para enriquecer e validar análises geradas por IA (GPT-4o Vision)
"""

# Definição da metodologia STRIDE
STRIDE = {
    "S - Spoofing": "Falsificação de identidade",
    "T - Tampering": "Adulteração de dados",
    "R - Repudiation": "Negação de ações realizadas",
    "I - Information Disclosure": "Vazamento de informações",
    "D - Denial of Service": "Negação de serviço",
    "E - Elevation of Privilege": "Elevação de privilégios"
}

# Mapeamento de categorias STRIDE por tipo de componente
# Para cada tipo, indica quais categorias STRIDE são mais relevantes
STRIDE_PER_COMPONENT_TYPE = {
    "database": {
        "S": {"ameaca": "Acesso com credenciais falsificadas", "severidade": "Alta"},
        "T": {"ameaca": "Adulteração ou corrupção de dados armazenados", "severidade": "Alta"},
        "R": {"ameaca": "Alterações sem trilha de auditoria", "severidade": "Média"},
        "I": {"ameaca": "Vazamento de dados sensíveis por consultas não autorizadas", "severidade": "Alta"},
        "D": {"ameaca": "Exaustão de conexões ou queries pesadas", "severidade": "Média"},
        "E": {"ameaca": "Escalação de privilégios via SQL Injection", "severidade": "Alta"},
    },
    "api": {
        "S": {"ameaca": "Falsificação de tokens de autenticação", "severidade": "Alta"},
        "T": {"ameaca": "Manipulação de payloads de requisição", "severidade": "Alta"},
        "R": {"ameaca": "Requisições sem logging adequado", "severidade": "Média"},
        "I": {"ameaca": "Exposição de dados sensíveis em respostas da API", "severidade": "Alta"},
        "D": {"ameaca": "Ataques de flooding/rate limiting insuficiente", "severidade": "Média"},
        "E": {"ameaca": "Bypass de autorização em endpoints", "severidade": "Alta"},
    },
    "server": {
        "S": {"ameaca": "Impersonação de servidor via DNS spoofing", "severidade": "Alta"},
        "T": {"ameaca": "Modificação de binários ou configurações", "severidade": "Alta"},
        "R": {"ameaca": "Ações administrativas sem registro", "severidade": "Média"},
        "I": {"ameaca": "Exposição de informações via erros ou debug", "severidade": "Média"},
        "D": {"ameaca": "Ataques DDoS ou esgotamento de recursos", "severidade": "Alta"},
        "E": {"ameaca": "Exploração de vulnerabilidades para acesso root", "severidade": "Alta"},
    },
    "loadbalancer": {
        "S": {"ameaca": "Redirecionamento de tráfego para servidor malicioso", "severidade": "Alta"},
        "T": {"ameaca": "Adulteração de tráfego em trânsito (MITM)", "severidade": "Alta"},
        "R": {"ameaca": "Falta de logging de requisições distribuídas", "severidade": "Média"},
        "I": {"ameaca": "Exposição de headers internos ou IPs de backend", "severidade": "Média"},
        "D": {"ameaca": "Sobrecarga por pico de tráfego ou ataque volumétrico", "severidade": "Alta"},
        "E": {"ameaca": "Acesso não autorizado ao painel de gerenciamento", "severidade": "Alta"},
    },
    "cdn": {
        "S": {"ameaca": "Cache poisoning com conteúdo malicioso", "severidade": "Alta"},
        "T": {"ameaca": "Adulteração de conteúdo cacheado", "severidade": "Média"},
        "I": {"ameaca": "Vazamento de dados sensíveis via cache público", "severidade": "Alta"},
        "D": {"ameaca": "Bypass de CDN para atingir servidor de origem", "severidade": "Média"},
    },
    "firewall": {
        "S": {"ameaca": "Bypass de regras via IP spoofing", "severidade": "Alta"},
        "T": {"ameaca": "Modificação de regras por acesso não autorizado", "severidade": "Alta"},
        "D": {"ameaca": "Exaustão de capacidade de inspeção de pacotes", "severidade": "Média"},
        "E": {"ameaca": "Escalação de privilégios no sistema do firewall", "severidade": "Alta"},
    },
    "waf": {
        "S": {"ameaca": "Evasão de regras WAF com payloads ofuscados", "severidade": "Alta"},
        "T": {"ameaca": "Bypass de WAF para injeção de código", "severidade": "Alta"},
        "D": {"ameaca": "Regras excessivas causando latência/indisponibilidade", "severidade": "Média"},
        "I": {"ameaca": "Vazamento de informações sobre regras e configuração", "severidade": "Média"},
    },
    "cache": {
        "S": {"ameaca": "Acesso a cache com credenciais falsificadas", "severidade": "Média"},
        "T": {"ameaca": "Envenenamento de cache (cache poisoning)", "severidade": "Alta"},
        "I": {"ameaca": "Dados sensíveis armazenados sem criptografia em cache", "severidade": "Alta"},
        "D": {"ameaca": "Exaustão de memória do cache", "severidade": "Média"},
    },
    "queue": {
        "S": {"ameaca": "Injeção de mensagens falsas na fila", "severidade": "Alta"},
        "T": {"ameaca": "Adulteração de mensagens em trânsito", "severidade": "Alta"},
        "R": {"ameaca": "Processamento de mensagens sem confirmação auditável", "severidade": "Média"},
        "I": {"ameaca": "Mensagens sensíveis em texto plano na fila", "severidade": "Alta"},
        "D": {"ameaca": "Flooding de fila com mensagens maliciosas", "severidade": "Média"},
    },
    "storage": {
        "S": {"ameaca": "Acesso não autenticado a buckets/volumes", "severidade": "Alta"},
        "T": {"ameaca": "Adulteração de arquivos armazenados", "severidade": "Alta"},
        "I": {"ameaca": "Bucket/storage público expondo dados sensíveis", "severidade": "Alta"},
        "D": {"ameaca": "Exclusão massiva de arquivos", "severidade": "Alta"},
        "E": {"ameaca": "Escalação via políticas de acesso mal configuradas", "severidade": "Alta"},
    },
    "auth": {
        "S": {"ameaca": "Bypass de autenticação ou falsificação de identidade", "severidade": "Alta"},
        "T": {"ameaca": "Adulteração de tokens ou sessões", "severidade": "Alta"},
        "R": {"ameaca": "Ações de autenticação sem auditoria", "severidade": "Média"},
        "I": {"ameaca": "Exposição de credenciais ou tokens em logs", "severidade": "Alta"},
        "E": {"ameaca": "Escalação de privilégios via manipulação de roles", "severidade": "Alta"},
    },
    "monitoring": {
        "T": {"ameaca": "Adulteração ou exclusão de logs de monitoramento", "severidade": "Alta"},
        "R": {"ameaca": "Gaps de monitoramento permitem ações sem registro", "severidade": "Média"},
        "I": {"ameaca": "Logs expondo informações sensíveis", "severidade": "Média"},
        "D": {"ameaca": "Desativação do sistema de monitoramento", "severidade": "Alta"},
    },
    "email": {
        "S": {"ameaca": "Envio de emails falsificados (spoofing)", "severidade": "Alta"},
        "T": {"ameaca": "Adulteração de conteúdo de emails em trânsito", "severidade": "Média"},
        "I": {"ameaca": "Vazamento de dados sensíveis por email", "severidade": "Alta"},
        "D": {"ameaca": "Abuso do serviço para spam/flooding", "severidade": "Média"},
    },
    "backup": {
        "S": {"ameaca": "Acesso não autorizado a backups", "severidade": "Alta"},
        "T": {"ameaca": "Corrupção de dados de backup", "severidade": "Alta"},
        "I": {"ameaca": "Backups sem criptografia expondo dados sensíveis", "severidade": "Alta"},
        "D": {"ameaca": "Exclusão de backups comprometendo recuperação", "severidade": "Alta"},
    },
    "encryption": {
        "S": {"ameaca": "Uso de chaves comprometidas para falsificar identidade", "severidade": "Alta"},
        "T": {"ameaca": "Comprometimento de chaves de criptografia", "severidade": "Alta"},
        "I": {"ameaca": "Exposição de chaves ou material criptográfico", "severidade": "Alta"},
        "E": {"ameaca": "Acesso não autorizado ao gerenciamento de chaves", "severidade": "Alta"},
    },
    "user": {
        "S": {"ameaca": "Roubo de identidade ou phishing", "severidade": "Alta"},
        "T": {"ameaca": "Manipulação de dados do lado do cliente", "severidade": "Média"},
        "R": {"ameaca": "Usuário nega ter realizado ações no sistema", "severidade": "Média"},
        "I": {"ameaca": "Exposição de dados pessoais", "severidade": "Alta"},
        "E": {"ameaca": "Usuário obtém privilégios administrativos", "severidade": "Alta"},
    },
    "gateway": {
        "S": {"ameaca": "Falsificação de requisições ao API Gateway", "severidade": "Alta"},
        "T": {"ameaca": "Manipulação de headers e payloads no gateway", "severidade": "Alta"},
        "R": {"ameaca": "Requisições sem logging no gateway", "severidade": "Média"},
        "I": {"ameaca": "Exposição de APIs internas pelo gateway", "severidade": "Alta"},
        "D": {"ameaca": "Sobrecarga do gateway com requisições maliciosas", "severidade": "Alta"},
        "E": {"ameaca": "Bypass de políticas de autorização no gateway", "severidade": "Alta"},
    },
    "security": {
        "T": {"ameaca": "Modificação de configurações de segurança", "severidade": "Alta"},
        "D": {"ameaca": "Desativação ou bypass de controles de segurança", "severidade": "Alta"},
        "E": {"ameaca": "Exploração de falhas no serviço de segurança", "severidade": "Alta"},
    },
}

# Ameaças por componente (formato legado mantido para compatibilidade)
COMPONENT_THREATS = {
    "database": ["SQL Injection", "Data Leakage", "Unauthorized Access", "Privilege Escalation"],
    "api": ["Broken Authentication", "Injection Attacks", "Rate Limiting", "Data Exposure"],
    "server": ["DDoS", "Privilege Escalation", "Malware", "Remote Code Execution"],
    "user": ["Phishing", "Session Hijacking", "Credential Theft", "Social Engineering"],
    "cloud": ["Misconfiguration", "Data Breach", "Account Hijacking", "Insecure APIs"],
    "loadbalancer": ["Traffic Manipulation", "DDoS Amplification", "SSL Stripping", "Health Check Abuse"],
    "cdn": ["Cache Poisoning", "Content Injection", "Origin Exposure", "SSL/TLS Issues"],
    "firewall": ["Rule Bypass", "IP Spoofing", "Configuration Tampering", "Capacity Exhaustion"],
    "waf": ["Payload Obfuscation", "Rule Evasion", "False Positive Abuse", "Bypass Techniques"],
    "cache": ["Cache Poisoning", "Data Leakage", "Memory Exhaustion", "Stale Data Attacks"],
    "queue": ["Message Injection", "Queue Flooding", "Message Tampering", "Unauthorized Consumption"],
    "storage": ["Unauthorized Access", "Data Exfiltration", "Ransomware", "Misconfigured Permissions"],
    "auth": ["Credential Stuffing", "Token Theft", "Session Fixation", "MFA Bypass"],
    "monitoring": ["Log Tampering", "Alert Suppression", "Monitoring Gaps", "Data Exfiltration via Logs"],
    "email": ["Email Spoofing", "Phishing", "Data Leakage", "Spam Abuse"],
    "backup": ["Backup Theft", "Backup Corruption", "Unencrypted Backups", "Backup Deletion"],
    "encryption": ["Key Compromise", "Weak Algorithms", "Key Exposure", "Side Channel Attacks"],
    "gateway": ["API Abuse", "Authentication Bypass", "Rate Limit Bypass", "Injection via Gateway"],
    "security": ["Security Control Bypass", "Config Tampering", "Privilege Escalation"],
}

# Descrições detalhadas das categorias STRIDE
STRIDE_DETAILS = {
    "Spoofing": {
        "description": "Ameaças relacionadas à falsificação de identidade ou credenciais",
        "examples": [
            "Falsificação de autenticação",
            "Roubo de credenciais",
            "Impersonação de usuário",
            "Falsificação de tokens"
        ]
    },
    "Tampering": {
        "description": "Ameaças relacionadas à modificação maliciosa de dados",
        "examples": [
            "Modificação de dados em trânsito",
            "Alteração de logs",
            "Modificação de código",
            "Corrupção de banco de dados"
        ]
    },
    "Repudiation": {
        "description": "Ameaças relacionadas à negação de ações realizadas",
        "examples": [
            "Falta de auditoria",
            "Logs insuficientes",
            "Ausência de assinatura digital",
            "Não rastreabilidade de ações"
        ]
    },
    "Information Disclosure": {
        "description": "Ameaças relacionadas ao vazamento ou exposição de informações sensíveis",
        "examples": [
            "Exposição de dados sensíveis",
            "Vazamento de credenciais",
            "Informações em logs",
            "Mensagens de erro verbosas"
        ]
    },
    "Denial of Service": {
        "description": "Ameaças que visam tornar o sistema indisponível",
        "examples": [
            "Ataques DDoS",
            "Esgotamento de recursos",
            "Flooding de requisições",
            "Crash de aplicação"
        ]
    },
    "Elevation of Privilege": {
        "description": "Ameaças relacionadas à obtenção de privilégios não autorizados",
        "examples": [
            "Exploração de vulnerabilidades",
            "Bypass de controles de acesso",
            "Escalação de privilégios",
            "Execução de código arbitrário"
        ]
    }
}

# Contramedidas comuns por categoria STRIDE
COUNTERMEASURES = {
    "Spoofing": [
        "Implementar autenticação forte (MFA)",
        "Usar certificados digitais",
        "Validar tokens e sessões",
        "Implementar OAuth/OpenID Connect"
    ],
    "Tampering": [
        "Usar HTTPS/TLS para comunicação",
        "Implementar assinaturas digitais",
        "Validar integridade de dados",
        "Proteger logs contra modificação"
    ],
    "Repudiation": [
        "Implementar logging abrangente",
        "Usar assinaturas digitais",
        "Implementar auditoria de ações",
        "Garantir não repúdio em transações críticas"
    ],
    "Information Disclosure": [
        "Criptografar dados sensíveis",
        "Implementar controles de acesso rigorosos",
        "Sanitizar mensagens de erro",
        "Usar HTTPS para todas as comunicações"
    ],
    "Denial of Service": [
        "Implementar rate limiting",
        "Usar CDN e cache",
        "Configurar timeouts adequados",
        "Implementar circuit breakers"
    ],
    "Elevation of Privilege": [
        "Implementar princípio do menor privilégio",
        "Validar todas as entradas",
        "Usar controles de acesso baseados em função (RBAC)",
        "Manter sistema atualizado"
    ]
}

def get_stride_info():
    """Retorna informações completas sobre a metodologia STRIDE"""
    return {
        "methodology": STRIDE,
        "details": STRIDE_DETAILS,
        "countermeasures": COUNTERMEASURES,
        "component_threats": COMPONENT_THREATS,
        "stride_per_component_type": STRIDE_PER_COMPONENT_TYPE
    }


def enrich_analysis(analysis_data: dict) -> dict:
    """
    Enriquece a análise gerada pelo LLM com dados do knowledge base.

    Garante que cada componente tenha ameaças de múltiplas categorias STRIDE
    e contramedidas adequadas. Também valida e complementa trust boundaries
    e fluxos de dados.

    Args:
        analysis_data: Dados da análise gerada pelo LLM

    Returns:
        dict: Análise enriquecida com ameaças e contramedidas adicionais
    """
    if not isinstance(analysis_data, dict):
        return analysis_data

    componentes = analysis_data.get('componentes', [])

    for componente in componentes:
        tipo = componente.get('tipo', '').lower()
        ameacas_existentes = componente.get('ameacas', [])
        contramedidas_existentes = componente.get('contramedidas', [])

        # Categorias STRIDE já cobertas
        categorias_cobertas = set()
        for ameaca in ameacas_existentes:
            categorias_cobertas.add(ameaca.get('categoria', ''))

        # Buscar ameaças adicionais do knowledge base
        stride_map = STRIDE_PER_COMPONENT_TYPE.get(tipo, {})

        for categoria, info in stride_map.items():
            if categoria not in categorias_cobertas:
                nome_comp = componente.get('nome', tipo)
                descricao = _build_enriched_description(categoria, tipo, nome_comp)
                impacto = _build_enriched_impact(categoria, tipo, nome_comp)
                # Adicionar ameaça que faltava
                nova_ameaca = {
                    "categoria": categoria,
                    "nome_ameaca": info["ameaca"],
                    "descricao": descricao,
                    "severidade": info["severidade"],
                    "impacto": impacto
                }
                ameacas_existentes.append(nova_ameaca)

                # Adicionar contramedida correspondente
                stride_name = _get_stride_name(categoria)
                countermeasure_list = COUNTERMEASURES.get(stride_name, [])
                if countermeasure_list:
                    nova_contramedida = {
                        "ameaca_relacionada": categoria,
                        "contramedida": countermeasure_list[0],
                        "prioridade": info["severidade"]
                    }
                    contramedidas_existentes.append(nova_contramedida)

        componente['ameacas'] = ameacas_existentes
        componente['contramedidas'] = contramedidas_existentes

    # Recalcular resumo
    if 'resumo' in analysis_data:
        total_ameacas = 0
        ameacas_alta = 0
        ameacas_media = 0
        ameacas_baixa = 0

        for comp in componentes:
            for ameaca in comp.get('ameacas', []):
                total_ameacas += 1
                sev = ameaca.get('severidade', 'Média')
                if sev == 'Alta':
                    ameacas_alta += 1
                elif sev == 'Média':
                    ameacas_media += 1
                else:
                    ameacas_baixa += 1

        analysis_data['resumo']['total_ameacas'] = total_ameacas
        analysis_data['resumo']['ameacas_alta'] = ameacas_alta
        analysis_data['resumo']['ameacas_media'] = ameacas_media
        analysis_data['resumo']['ameacas_baixa'] = ameacas_baixa

    # Atualizar matriz STRIDE (reutilizar chaves existentes para evitar duplicatas)
    if 'matriz_stride' in analysis_data:
        for comp in componentes:
            nome = comp.get('nome', '')
            # Procurar chave existente na matriz que corresponda a este componente
            existing_key = _find_matrix_key(analysis_data['matriz_stride'], nome)
            key = existing_key if existing_key else nome

            categorias = {}
            for ameaca in comp.get('ameacas', []):
                cat = ameaca.get('categoria', '')
                if cat in ['S', 'T', 'R', 'I', 'D', 'E']:
                    categorias[cat] = True
            for cat in ['S', 'T', 'R', 'I', 'D', 'E']:
                if cat not in categorias:
                    categorias[cat] = False
            analysis_data['matriz_stride'][key] = categorias

    return analysis_data


def _find_matrix_key(matriz: dict, nome: str) -> str:
    """
    Procura uma chave existente na matriz STRIDE que corresponda ao nome do componente.
    Evita duplicatas como 'Amazon ElastiCache' e 'Amazon ElastiCache (memcached)'.

    Compara por substring: se o nome do componente contém a chave existente (ou vice-versa),
    reutiliza a chave existente.

    Returns:
        A chave existente encontrada ou string vazia se não houver match.
    """
    nome_lower = nome.lower().strip()
    for key in matriz:
        key_lower = key.lower().strip()
        if nome_lower == key_lower:
            return key
        # Se um contém o outro, são o mesmo componente
        if nome_lower in key_lower or key_lower in nome_lower:
            return key
        # Comparar palavras principais (ignorar sufixos entre parênteses)
        nome_base = nome_lower.split('(')[0].strip()
        key_base = key_lower.split('(')[0].strip()
        if nome_base and key_base and (nome_base == key_base):
            return key
    return ''


def _get_stride_name(category: str) -> str:
    """Retorna o nome completo da categoria STRIDE"""
    mapping = {
        'S': 'Spoofing',
        'T': 'Tampering',
        'R': 'Repudiation',
        'I': 'Information Disclosure',
        'D': 'Denial of Service',
        'E': 'Elevation of Privilege'
    }
    return mapping.get(category, category)


def _get_stride_focus(category: str) -> str:
    """Retorna o foco de segurança da categoria STRIDE"""
    mapping = {
        'S': 'autenticação',
        'T': 'integridade',
        'R': 'rastreabilidade',
        'I': 'confidencialidade',
        'D': 'disponibilidade',
        'E': 'autorização'
    }
    return mapping.get(category, 'segurança')


# Descrições detalhadas para ameaças enriquecidas (por categoria + tipo de componente)
_ENRICHED_DESCRIPTIONS = {
    "S": {
        "database": "Um atacante pode utilizar credenciais roubadas ou forjadas para se autenticar no banco de dados, obtendo acesso não autorizado a dados sensíveis sem ser detectado.",
        "api": "Tokens de autenticação JWT ou OAuth podem ser forjados ou reutilizados por atacantes para se passar por usuários legítimos e acessar endpoints protegidos.",
        "server": "Atacante pode realizar DNS spoofing ou ARP poisoning para redirecionar tráfego destinado ao servidor legítimo para um servidor malicioso.",
        "loadbalancer": "Configurações DNS ou BGP podem ser manipuladas para redirecionar o tráfego do load balancer para servidores controlados pelo atacante.",
        "cdn": "Atacante pode envenenar o cache da CDN com conteúdo malicioso que será servido a todos os usuários subsequentes.",
        "cache": "Sem autenticação adequada, atacantes podem acessar diretamente o serviço de cache e ler ou manipular dados armazenados.",
        "queue": "Mensagens falsas podem ser injetadas na fila por atacantes que obtêm acesso ao broker, comprometendo o processamento downstream.",
        "storage": "Buckets ou volumes de armazenamento sem autenticação adequada podem ser acessados publicamente, expondo dados corporativos.",
        "auth": "O próprio serviço de autenticação pode ser alvo de ataques de bypass, permitindo que atacantes contornem verificações de identidade.",
        "gateway": "Requisições falsificadas podem passar pelo API Gateway se a validação de tokens e certificados não for rigorosa.",
        "user": "Ataques de phishing ou engenharia social podem levar ao roubo de credenciais dos usuários, comprometendo suas contas.",
        "firewall": "Técnicas de IP spoofing podem ser usadas para contornar regras de firewall baseadas em endereço de origem.",
        "waf": "Payloads ofuscados ou codificados podem evadir as regras do WAF, permitindo que ataques cheguem à aplicação.",
        "monitoring": "Logs de monitoramento podem ser falsificados para ocultar atividades maliciosas e dificultar investigações forenses.",
        "email": "Atacantes podem enviar emails falsificados se passando pelo domínio da organização, sem SPF/DKIM/DMARC adequados.",
        "backup": "Acesso não autorizado aos backups pode expor dados históricos sensíveis que já foram removidos dos sistemas em produção.",
        "encryption": "Chaves criptográficas comprometidas podem ser usadas para falsificar assinaturas digitais e certificados.",
        "security": "Controles de segurança podem ter suas configurações modificadas por atacantes com acesso ao painel de gerenciamento.",
    },
    "T": {
        "database": "Ataques de SQL Injection ou acesso direto podem permitir a modificação não autorizada de registros, corrompendo a integridade dos dados de negócio.",
        "api": "Payloads de requisições podem ser interceptados e modificados em trânsito (MITM) se TLS não estiver corretamente configurado.",
        "server": "Binários, configurações ou dependências do servidor podem ser modificados por atacantes com acesso ao sistema de arquivos.",
        "loadbalancer": "Tráfego em trânsito entre clientes e backend pode ser interceptado e adulterado se a terminação TLS não for adequada.",
        "cache": "Dados no cache podem ser envenenados com valores maliciosos que serão servidos a usuários legítimos.",
        "queue": "Mensagens em trânsito na fila podem ser interceptadas e alteradas antes de serem consumidas pelo processador.",
        "storage": "Arquivos armazenados podem ser modificados ou substituídos por versões maliciosas sem controles de integridade.",
        "auth": "Tokens de sessão ou JWT podem ser adulterados para modificar claims de autorização e escopo de acesso.",
        "gateway": "Headers HTTP e payloads podem ser manipulados no trânsito pelo API Gateway, alterando o comportamento da aplicação.",
        "firewall": "Regras de firewall podem ser modificadas por acesso não autorizado ao painel de gerenciamento.",
        "waf": "Atacantes podem explorar bypass do WAF para injetar código malicioso (XSS, SQLi) na aplicação protegida.",
        "monitoring": "Logs de auditoria podem ser adulterados ou excluídos para ocultar evidências de atividades maliciosas.",
        "email": "Conteúdo de emails pode ser adulterado em trânsito se TLS não for usado entre os servidores de email.",
        "backup": "Dados de backup podem ser corrompidos silenciosamente, tornando a recuperação de desastres inviável.",
        "encryption": "Chaves de criptografia podem ser comprometidas, permitindo a descriptografia e modificação de dados protegidos.",
        "security": "Configurações de segurança podem ser modificadas por atacantes, desativando controles de proteção.",
    },
    "R": {
        "database": "Alterações em registros do banco podem não ter trilha de auditoria, impossibilitando rastrear quem fez modificações.",
        "api": "Requisições à API podem não ter logging adequado, permitindo que ações maliciosas não sejam rastreáveis.",
        "server": "Ações administrativas no servidor podem não ser registradas, dificultando a investigação de incidentes.",
        "queue": "Mensagens processadas pela fila podem não ter confirmação auditável, impedindo a rastreabilidade de transações.",
        "auth": "Tentativas de autenticação e mudanças de permissão podem não ser registradas adequadamente para auditoria.",
        "gateway": "Requisições que passam pelo gateway podem não ter logging centralizado, criando pontos cegos de auditoria.",
        "monitoring": "Gaps no monitoramento podem permitir que ações maliciosas ocorram sem nenhum registro.",
        "user": "Usuários podem negar ter realizado ações no sistema se não houver mecanismos de não-repúdio como assinatura digital.",
        "loadbalancer": "Requisições distribuídas entre múltiplos servidores podem perder a rastreabilidade sem logging centralizado.",
    },
    "I": {
        "database": "Consultas não autorizadas ou mal configuradas podem expor dados sensíveis como informações pessoais, financeiras ou credenciais.",
        "api": "Respostas da API podem incluir dados sensíveis desnecessários (over-fetching), expondo informações que não deveriam ser visíveis.",
        "server": "Mensagens de erro detalhadas, stack traces ou modo debug ativo podem expor detalhes internos da arquitetura.",
        "loadbalancer": "Headers de resposta podem vazar informações sobre a infraestrutura interna, como IPs de backend e versões de software.",
        "cdn": "Dados sensíveis podem ser inadvertidamente cacheados em camadas públicas da CDN, ficando acessíveis a qualquer pessoa.",
        "cache": "Dados sensíveis armazenados no cache sem criptografia podem ser lidos por qualquer processo com acesso à memória.",
        "queue": "Mensagens na fila podem conter dados sensíveis em texto plano, expostos a qualquer consumidor com acesso.",
        "storage": "Buckets de armazenamento com permissões públicas podem expor documentos e dados corporativos sensíveis.",
        "auth": "Credenciais, tokens ou secrets podem aparecer em logs, traces ou respostas de erro do serviço de autenticação.",
        "gateway": "O API Gateway pode inadvertidamente expor rotas internas ou documentação de APIs privadas.",
        "firewall": "Informações sobre as regras configuradas e portas permitidas podem vazar, facilitando o planejamento de ataques.",
        "waf": "Mensagens de bloqueio do WAF podem revelar detalhes sobre regras e padrões de detecção configurados.",
        "monitoring": "Logs de monitoramento podem capturar e armazenar dados sensíveis como senhas, tokens ou dados pessoais.",
        "email": "Dados sensíveis incluídos em emails podem ser interceptados ou armazenados em servidores de email sem criptografia.",
        "backup": "Backups sem criptografia podem expor dados sensíveis de períodos anteriores, incluindo dados já excluídos.",
        "encryption": "Material criptográfico como chaves privadas pode ser exposto se o gerenciamento de chaves não for adequado.",
        "user": "Dados pessoais dos usuários podem ser expostos por falhas de controle de acesso ou vulnerabilidades na interface.",
    },
    "D": {
        "database": "Queries pesadas, conexões excessivas ou ataques de exaustão podem tornar o banco de dados indisponível para a aplicação.",
        "api": "Ataques de flooding ou ausência de rate limiting podem sobrecarregar a API, causando indisponibilidade para usuários legítimos.",
        "server": "Ataques DDoS ou esgotamento de CPU/memória/disco podem tornar o servidor completamente indisponível.",
        "loadbalancer": "Picos de tráfego legítimo ou ataques volumétricos podem exceder a capacidade do load balancer.",
        "cdn": "Atacantes podem forçar cache misses massivos, sobrecarregando o servidor de origem por trás da CDN.",
        "cache": "Exaustão de memória do cache pode causar cache misses em cascata, sobrecarregando os sistemas downstream.",
        "queue": "Flooding da fila com mensagens maliciosas pode causar atrasos no processamento ou estouro de recursos.",
        "storage": "Exclusão massiva de arquivos ou preenchimento do espaço disponível pode comprometer o armazenamento.",
        "monitoring": "Desativação do sistema de monitoramento pode criar pontos cegos durante ataques ativos.",
        "firewall": "Exaustão da capacidade de inspeção de pacotes pode fazer o firewall falhar aberto ou causar latência.",
        "waf": "Regras excessivamente complexas podem causar latência significativa ou indisponibilidade do WAF.",
        "email": "Abuso do serviço de email para spam pode causar bloqueio do domínio e indisponibilidade de envio legítimo.",
        "backup": "Exclusão de backups compromete a capacidade de recuperação de desastres e continuidade de negócios.",
        "gateway": "Sobrecarga do API Gateway com requisições maliciosas pode bloquear o acesso a todos os serviços downstream.",
        "security": "Desativação ou bypass de controles de segurança pode deixar toda a infraestrutura desprotegida.",
    },
    "E": {
        "database": "Vulnerabilidades de SQL Injection podem permitir que atacantes executem comandos com privilégios de DBA.",
        "api": "Falhas de autorização podem permitir que usuários comuns acessem endpoints administrativos ou dados de outros usuários.",
        "server": "Exploração de vulnerabilidades no sistema operacional pode permitir escalação de privilégios para acesso root.",
        "loadbalancer": "Acesso não autorizado ao painel de gerenciamento do load balancer pode permitir controle total do tráfego.",
        "storage": "Políticas IAM mal configuradas podem permitir que usuários obtenham acesso a buckets ou recursos restritos.",
        "auth": "Manipulação de roles ou claims pode permitir que usuários comuns obtenham privilégios administrativos.",
        "gateway": "Bypass das políticas de autorização no gateway pode conceder acesso irrestrito a APIs internas.",
        "firewall": "Escalação de privilégios no sistema do firewall pode permitir a desativação completa das regras.",
        "encryption": "Acesso não autorizado ao gerenciamento de chaves pode comprometer toda a criptografia da infraestrutura.",
        "security": "Exploração de falhas no serviço de segurança pode permitir controle sobre todos os controles de proteção.",
        "user": "Um usuário comum pode explorar falhas para obter privilégios administrativos no sistema.",
    },
}

# Impactos detalhados para ameaças enriquecidas (por categoria + tipo de componente)
_ENRICHED_IMPACTS = {
    "S": {
        "database": "Acesso não autorizado ao banco pode resultar em roubo de dados, violação de compliance (LGPD/GDPR) e danos reputacionais",
        "api": "Atacantes podem executar operações em nome de usuários legítimos, causando fraudes e perda de confiança",
        "server": "Redirecionamento de tráfego pode expor credenciais e dados sensíveis para servidores maliciosos",
        "loadbalancer": "Todo o tráfego da aplicação pode ser interceptado, comprometendo dados de todos os usuários",
        "cdn": "Conteúdo malicioso distribuído pela CDN afeta todos os usuários globalmente",
        "cache": "Dados sensíveis em cache podem ser lidos, incluindo sessões e tokens de autenticação",
        "queue": "Processamento de mensagens falsas pode corromper dados de negócio e gerar transações fraudulentas",
        "storage": "Exposição de documentos corporativos, dados de clientes e propriedade intelectual",
        "auth": "Comprometimento do serviço central de autenticação afeta todos os sistemas dependentes",
        "gateway": "Acesso não autorizado a todas as APIs protegidas pelo gateway",
        "user": "Contas de usuários comprometidas podem ser usadas para fraudes e acesso a dados sensíveis",
        "firewall": "Tráfego malicioso pode contornar as regras de segurança e alcançar sistemas internos",
        "waf": "Ataques web (XSS, SQLi, RCE) podem alcançar a aplicação sem detecção",
        "email": "Emails falsificados podem ser usados para phishing direcionado contra funcionários e clientes",
        "backup": "Dados históricos sensíveis podem ser exfiltrados dos backups",
        "encryption": "Certificados e assinaturas falsificadas comprometem toda a cadeia de confiança",
        "security": "Modificação dos controles de segurança pode abrir brechas em toda a infraestrutura",
        "monitoring": "Evidências de ataques podem ser ocultadas através de logs falsificados",
    },
    "T": {
        "database": "Dados de negócio corrompidos podem levar a decisões erradas, perdas financeiras e violações regulatórias",
        "api": "Dados adulterados em trânsito podem causar transações incorretas e inconsistências no sistema",
        "server": "Servidor comprometido pode servir como ponto de pivô para ataques laterais na rede",
        "loadbalancer": "Adulteração de tráfego pode afetar a integridade de todas as comunicações da aplicação",
        "cache": "Cache envenenado distribui dados incorretos para todos os consumidores, causando erros em cascata",
        "queue": "Mensagens adulteradas podem causar processamento incorreto e inconsistências de dados",
        "storage": "Arquivos modificados podem conter malware ou dados incorretos, afetando sistemas dependentes",
        "auth": "Tokens adulterados podem conceder acesso indevido a recursos protegidos",
        "gateway": "Requisições manipuladas podem explorar vulnerabilidades nos serviços backend",
        "firewall": "Regras alteradas podem abrir portas para tráfego malicioso",
        "waf": "Bypass de WAF expõe a aplicação a ataques de injeção e exploits web",
        "monitoring": "Logs adulterados comprometem investigações forenses e resposta a incidentes",
        "email": "Emails adulterados podem conter links maliciosos ou instruções fraudulentas",
        "backup": "Backups corrompidos tornam a recuperação de desastres inviável",
        "encryption": "Comprometimento de chaves invalida toda a proteção criptográfica da infraestrutura",
        "security": "Controles desativados deixam sistemas expostos a todo tipo de ataque",
    },
    "R": {
        "database": "Sem auditoria, é impossível identificar a origem de alterações maliciosas ou vazamentos de dados",
        "api": "Ações maliciosas via API não podem ser rastreadas, dificultando resposta a incidentes e compliance",
        "server": "Sem logs de ações administrativas, comprometimentos podem passar despercebidos por longos períodos",
        "queue": "Transações processadas sem confirmação auditável impedem a resolução de disputas",
        "auth": "Falhas de auditoria no serviço de autenticação comprometem requisitos de compliance e investigações",
        "gateway": "Pontos cegos no logging do gateway dificultam a detecção de ataques e abusos de API",
        "monitoring": "Gaps de monitoramento permitem ações maliciosas sem qualquer registro detectável",
        "user": "Sem mecanismos de não-repúdio, disputas sobre ações realizadas não podem ser resolvidas",
        "loadbalancer": "Requisições distribuídas sem rastreabilidade dificultam a correlação de eventos de segurança",
    },
    "I": {
        "database": "Exposição de dados pessoais, financeiros ou de saúde pode resultar em multas LGPD/GDPR e processos judiciais",
        "api": "Dados sensíveis expostos em respostas podem ser capturados por atacantes ou armazenados em logs de terceiros",
        "server": "Informações de infraestrutura expostas facilitam o planejamento de ataques direcionados",
        "loadbalancer": "IPs internos e versões de software expostos permitem reconhecimento da infraestrutura",
        "cdn": "Dados sensíveis em cache público ficam acessíveis globalmente e podem ser indexados por buscadores",
        "cache": "Sessões, tokens e dados pessoais em cache sem criptografia ficam expostos a acesso não autorizado",
        "queue": "Dados sensíveis em texto plano na fila podem ser lidos por qualquer consumidor com acesso ao broker",
        "storage": "Buckets públicos podem resultar em vazamento massivo de dados e violações de compliance",
        "auth": "Credenciais expostas em logs podem ser usadas para acessar múltiplos sistemas",
        "gateway": "APIs internas expostas podem revelar funcionalidades não destinadas a uso público",
        "firewall": "Conhecimento das regras de firewall facilita a criação de ataques que evitam detecção",
        "waf": "Regras do WAF expostas permitem que atacantes criem payloads específicos para evasão",
        "monitoring": "Dados sensíveis capturados em logs podem ser acessados por equipes sem autorização",
        "email": "Dados sensíveis em emails podem ser interceptados e usados para chantagem ou fraude",
        "backup": "Backups antigos podem conter dados que já deveriam ter sido eliminados por requisitos de retenção",
        "encryption": "Exposição de chaves compromete todos os dados protegidos por aquela chave",
        "user": "Vazamento de dados pessoais resulta em danos reputacionais e violações de privacidade",
    },
    "D": {
        "database": "Banco de dados indisponível paralisa todas as operações de negócio que dependem dos dados",
        "api": "API indisponível impede que clientes e parceiros acessem os serviços, causando perda de receita",
        "server": "Servidor fora do ar causa interrupção completa do serviço para todos os usuários",
        "loadbalancer": "Falha no load balancer pode causar indisponibilidade total da aplicação",
        "cdn": "Sobrecarga no servidor de origem pode causar indisponibilidade global do conteúdo",
        "cache": "Cache indisponível causa degradação severa de performance em toda a aplicação",
        "queue": "Fila sobrecarregada causa atrasos no processamento e pode perder mensagens críticas",
        "storage": "Perda de armazenamento resulta em perda de dados e interrupção de serviços dependentes",
        "monitoring": "Sem monitoramento, ataques ativos não são detectados e a resposta é atrasada",
        "firewall": "Firewall sobrecarregado pode falhar aberto, removendo a proteção de rede",
        "waf": "WAF indisponível expõe a aplicação diretamente a ataques web",
        "email": "Bloqueio do domínio por spam impede comunicações legítimas com clientes",
        "backup": "Sem backups válidos, a recuperação após incidentes graves torna-se impossível",
        "gateway": "Gateway indisponível bloqueia o acesso a todos os microserviços downstream",
        "security": "Controles de segurança desativados deixam a infraestrutura completamente exposta",
    },
    "E": {
        "database": "Acesso DBA permite leitura e modificação de todos os dados, incluindo dados de outros clientes",
        "api": "Acesso administrativo permite manipulação de dados, configurações e contas de outros usuários",
        "server": "Acesso root permite controle total do servidor, instalação de backdoors e movimento lateral",
        "loadbalancer": "Controle do load balancer permite redirecionamento e interceptação de todo o tráfego",
        "storage": "Acesso irrestrito ao armazenamento permite exfiltração massiva de dados",
        "auth": "Controle do serviço de autenticação permite criar e modificar contas com qualquer nível de privilégio",
        "gateway": "Acesso irrestrito via gateway permite chamar qualquer API interna sem restrições",
        "firewall": "Controle do firewall permite abrir portas e criar regras para facilitar ataques",
        "encryption": "Controle das chaves permite descriptografar dados e forjar assinaturas",
        "security": "Controle dos serviços de segurança permite desativar todas as proteções",
        "user": "Usuário com privilégios administrativos pode acessar e modificar dados de outros usuários",
    },
}


def _build_enriched_description(categoria: str, tipo: str, nome_comp: str) -> str:
    """Gera uma descrição detalhada e contextualizada para ameaças adicionadas pelo enriquecimento."""
    desc_map = _ENRICHED_DESCRIPTIONS.get(categoria, {})
    desc = desc_map.get(tipo, '')
    if desc:
        return desc
    # Fallback genérico se não houver descrição específica
    focus = _get_stride_focus(categoria)
    stride_name = _get_stride_name(categoria)
    return f"Ameaça de {stride_name} identificada no componente {nome_comp}, podendo comprometer a {focus} do sistema."


def _build_enriched_impact(categoria: str, tipo: str, nome_comp: str) -> str:
    """Gera uma descrição de impacto detalhada e contextualizada para ameaças enriquecidas."""
    impact_map = _ENRICHED_IMPACTS.get(categoria, {})
    impact = impact_map.get(tipo, '')
    if impact:
        return impact
    # Fallback genérico
    focus = _get_stride_focus(categoria)
    return f"Comprometimento de {focus} do componente {nome_comp}, podendo afetar a segurança geral da arquitetura"
