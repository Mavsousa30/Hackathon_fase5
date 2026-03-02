"""
Gerador de Relatórios PDF para Análise STRIDE
Cria relatórios profissionais de modelagem de ameaças
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.platypus.flowables import HRFlowable
from datetime import datetime
import json
import os


class STRIDEReportGenerator:
    """Gerador de relatórios PDF para análises STRIDE"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Cria estilos personalizados para o relatório"""
        
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Seção
        self.styles.add(ParagraphStyle(
            name='CustomSection',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#0066cc'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
        
        # Categoria STRIDE
        self.styles.add(ParagraphStyle(
            name='STRIDECategory',
            parent=self.styles['Heading4'],
            fontSize=12,
            textColor=colors.HexColor('#cc0000'),
            spaceAfter=8,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=6
        ))
        
        # Texto de destaque
        self.styles.add(ParagraphStyle(
            name='Highlight',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#0066cc'),
            fontName='Helvetica-Bold'
        ))
    
    def generate_report(self, analysis_data: dict, output_path: str, image_path: str = None):
        """
        Gera o relatório PDF completo
        
        Args:
            analysis_data: Dados da análise (pode ser dict ou string JSON)
            output_path: Caminho para salvar o PDF
            image_path: Caminho da imagem do diagrama (opcional)
        """
        
        # Parsear dados se for string
        if isinstance(analysis_data, str):
            try:
                analysis_data = json.loads(analysis_data)
            except json.JSONDecodeError:
                # Se não for JSON válido, mantém como um dict com o texto
                analysis_data = {"analysis_text": analysis_data}
        
        # Criar documento
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Container para elementos do documento
        story = []
        
        # Adicionar capa
        story.extend(self._create_cover_page(analysis_data))
        story.append(PageBreak())
        
        # Adicionar sumário executivo
        story.extend(self._create_executive_summary(analysis_data))
        story.append(Spacer(1, 0.3*inch))
        
        # Adicionar imagem do diagrama se disponível
        if image_path and os.path.exists(image_path):
            story.extend(self._add_diagram_image(image_path))
            story.append(PageBreak())
        
        # Adicionar análise detalhada
        story.extend(self._create_detailed_analysis(analysis_data))
        
        # Adicionar Matriz STRIDE se disponível
        if isinstance(analysis_data, dict):
            actual_data = analysis_data.get('analysis', analysis_data)
            if 'matriz_stride' in actual_data and actual_data['matriz_stride']:
                story.append(PageBreak())
                story.extend(self._create_stride_matrix(actual_data))
        
        # Adicionar Trust Boundaries se disponível
        if isinstance(analysis_data, dict):
            actual_data = analysis_data.get('analysis', analysis_data)
            if 'trust_boundaries' in actual_data and actual_data['trust_boundaries']:
                story.append(PageBreak())
                story.extend(self._create_trust_boundaries_section(actual_data))
        
        # Adicionar metodologia STRIDE
        story.append(PageBreak())
        story.extend(self._create_stride_methodology())
        
        # Gerar PDF
        doc.build(story)
        
        return output_path
    
    def _create_cover_page(self, data: dict):
        """Cria a página de capa do relatório"""
        elements = []
        
        # Espaço inicial
        elements.append(Spacer(1, 2*inch))
        
        # Título
        elements.append(Paragraph(
            "Relatório de Modelagem de Ameaças",
            self.styles['CustomTitle']
        ))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Subtítulo
        elements.append(Paragraph(
            "Análise STRIDE de Segurança em Arquitetura de Software",
            self.styles['CustomSubtitle']
        ))
        
        elements.append(Spacer(1, 1*inch))
        
        # Informações do relatório
        info_data = [
            ['Data de Geração:', datetime.now().strftime("%d/%m/%Y às %H:%M")],
            ['Metodologia:', 'STRIDE (Microsoft)'],
            ['Ferramenta:', 'STRIDE Threat Analyzer - AI Powered'],
            ['Status:', 'Análise Concluída']
        ]
        
        info_table = Table(info_data, colWidths=[2.5*inch, 3.5*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#0066cc')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.grey),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(info_table)
        
        elements.append(Spacer(1, 1*inch))
        
        # Rodapé da capa
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0066cc')))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph(
            "<i>Projeto Hackathon FIAP - Fase 5<br/>Desenvolvido com IA e OpenAI GPT-4 Vision</i>",
            self.styles['Normal']
        ))
        
        return elements
    
    def _create_executive_summary(self, data: dict):
        """Cria o sumário executivo"""
        elements = []
        
        elements.append(Paragraph("Sumário Executivo", self.styles['CustomTitle']))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0066cc')))
        elements.append(Spacer(1, 0.2*inch))
        
        # Extrair informações resumidas
        total_componentes = 0
        total_ameacas = 0
        ameacas_criticas = 0
        risk_score = 0.0
        risk_justificativa = "Não calculado"
        
        if isinstance(data, dict):
            # Tentar extrair do resumo se existir
            if 'resumo' in data:
                resumo = data['resumo']
                total_componentes = resumo.get('total_componentes', 0)
                total_ameacas = resumo.get('total_ameacas', 0)
                ameacas_criticas = resumo.get('ameacas_alta', 0)
                risk_score = resumo.get('risk_score', 0.0)
                risk_justificativa = resumo.get('risk_justificativa', 'Não calculado')
            # Ou contar dos componentes
            elif 'componentes' in data:
                total_componentes = len(data['componentes'])
                for comp in data['componentes']:
                    if 'ameacas' in comp:
                        total_ameacas += len(comp['ameacas'])
                        for ameaca in comp['ameacas']:
                            if ameaca.get('severidade') == 'Alta':
                                ameacas_criticas += 1
        
        # Determinar status do risk score
        if risk_score >= 8.0:
            risk_status = "CRITICO"
            risk_color = colors.red
        elif risk_score >= 6.0:
            risk_status = "ALTO"
            risk_color = colors.orange
        elif risk_score >= 4.0:
            risk_status = "MEDIO"
            risk_color = colors.HexColor('#FFD700')
        else:
            risk_status = "BAIXO"
            risk_color = colors.green
        
        # Tabela de métricas com Risk Score
        metrics_data = [
            ['Metrica', 'Valor', 'Status'],
            ['Componentes Analisados', str(total_componentes), 'Completo'],
            ['Ameacas Identificadas', str(total_ameacas), 'Alta Prioridade' if total_ameacas > 10 else 'Atencao'],
            ['Ameacas Criticas', str(ameacas_criticas), 'Critico' if ameacas_criticas > 0 else 'OK'],
            ['Risk Score Geral', f'{risk_score:.1f}/10', risk_status]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Adicionar justificativa do Risk Score se disponível
        if risk_justificativa and risk_justificativa != "Não calculado":
            elements.append(Paragraph(
                "<b>Justificativa do Risk Score:</b>",
                self.styles['CustomSection']
            ))
            elements.append(Paragraph(
                risk_justificativa,
                self.styles['CustomBody']
            ))
            elements.append(Spacer(1, 0.2*inch))
        
        # Descrição do sumário
        elements.append(Paragraph(
            "<b>Visão Geral da Análise</b>",
            self.styles['CustomSection']
        ))
        
        summary_text = """
        Este relatório apresenta uma análise completa de segurança baseada na metodologia STRIDE 
        (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).
        A análise foi realizada utilizando Inteligência Artificial para identificar potenciais ameaças 
        de segurança na arquitetura do sistema e fornecer recomendações práticas para mitigação.
        """
        
        elements.append(Paragraph(summary_text, self.styles['CustomBody']))
        
        return elements
    
    def _add_diagram_image(self, image_path: str):
        """Adiciona a imagem do diagrama ao relatório"""
        elements = []
        
        elements.append(Paragraph("Diagrama de Arquitetura Analisado", self.styles['CustomSection']))
        elements.append(Spacer(1, 0.15*inch))
        
        try:
            # Adicionar imagem com tamanho ajustado
            img = Image(image_path, width=6*inch, height=4*inch, kind='proportional')
            elements.append(img)
        except:
            elements.append(Paragraph(
                "<i>Imagem do diagrama não disponível</i>",
                self.styles['Normal']
            ))
        
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_detailed_analysis(self, data: dict):
        """Cria a análise detalhada das ameaças"""
        elements = []
        
        elements.append(Paragraph("Análise Detalhada de Ameaças", self.styles['CustomTitle']))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0066cc')))
        elements.append(Spacer(1, 0.2*inch))
        
        # Extrair dados aninhados se necessário
        actual_data = data
        if isinstance(data, dict):
            # Se tiver 'analysis' aninhado, extrair
            if 'analysis' in data and isinstance(data['analysis'], dict):
                actual_data = data['analysis']
            # Se tiver 'success' e 'analysis', é resposta do analyzer
            elif 'success' in data and 'analysis' in data:
                actual_data = data['analysis']
        
        # Se tiver estrutura de componentes
        if isinstance(actual_data, dict) and 'componentes' in actual_data:
            for idx, componente in enumerate(actual_data['componentes'], 1):
                elements.extend(self._format_component_analysis(componente, idx))
            
            # Adicionar fluxos de dados se existir
            if 'fluxos_dados' in actual_data and actual_data['fluxos_dados']:
                elements.append(Spacer(1, 0.3*inch))
                elements.append(Paragraph("Fluxos de Dados e Comunicação", self.styles['CustomSection']))
                elements.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
                elements.append(Spacer(1, 0.1*inch))
                
                for idx, fluxo in enumerate(actual_data['fluxos_dados'], 1):
                    elements.append(Paragraph(
                        f"<b>{idx}. {fluxo.get('origem', 'N/A')} → {fluxo.get('destino', 'N/A')}</b>",
                        self.styles['CustomBody']
                    ))
                    
                    # Informações do fluxo
                    info_parts = []
                    if 'protocolo' in fluxo:
                        info_parts.append(f"Protocolo: <b>{fluxo['protocolo']}</b>")
                    if 'tipo_dados' in fluxo:
                        info_parts.append(f"Dados: {fluxo['tipo_dados']}")
                    if 'criptografado' in fluxo:
                        if fluxo['criptografado']:
                            cripto = '<font color="#009900"><b>[CRIPTOGRAFADO]</b></font>'
                        else:
                            cripto = '<font color="#cc0000"><b>[NÃO CRIPTOGRAFADO]</b></font>'
                        info_parts.append(cripto)
                    if 'autenticado' in fluxo:
                        if fluxo['autenticado']:
                            auth = '<font color="#009900">[AUTENTICADO]</font>'
                        else:
                            auth = '<font color="#cc0000">[NÃO AUTENTICADO]</font>'
                        info_parts.append(auth)
                    if 'atravessa_trust_boundary' in fluxo and fluxo['atravessa_trust_boundary']:
                        info_parts.append('<font color="#ff9900"><b>[ATRAVESSA TRUST BOUNDARY]</b></font>')
                    
                    if info_parts:
                        elements.append(Paragraph(
                            f"<i>{' | '.join(info_parts)}</i>",
                            self.styles['CustomBody']
                        ))
                    
                    # Ameaças
                    if 'ameacas' in fluxo and fluxo['ameacas']:
                        elements.append(Paragraph("Ameaças:", self.styles['Highlight']))
                        for ameaca in fluxo['ameacas']:
                            elements.append(Paragraph(f"<font color='#cc0000'><b>!</b></font> {ameaca}", self.styles['CustomBody']))
                    
                    # Contramedidas
                    if 'contramedidas' in fluxo and fluxo['contramedidas']:
                        elements.append(Paragraph("Contramedidas:", self.styles['Highlight']))
                        for contra in fluxo['contramedidas']:
                            elements.append(Paragraph(f"<font face='ZapfDingbats'>4</font> {contra}", self.styles['CustomBody']))
                    
                    elements.append(Spacer(1, 0.15*inch))
            
            # Adicionar recomendações gerais
            if 'recomendacoes_gerais' in actual_data and actual_data['recomendacoes_gerais']:
                elements.append(Spacer(1, 0.3*inch))
                elements.append(Paragraph("Recomendações Gerais de Segurança", self.styles['CustomSection']))
                elements.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
                elements.append(Spacer(1, 0.1*inch))
                
                for rec in actual_data['recomendacoes_gerais']:
                    # Verificar se é dicionário (novo formato) ou string (formato antigo)
                    if isinstance(rec, dict):
                        categoria = rec.get('categoria', 'Geral')
                        recomendacao = rec.get('recomendacao', 'N/A')
                        prioridade = rec.get('prioridade', 'Média')
                        
                        # Definir cor por prioridade
                        if prioridade == 'Alta':
                            cor_prioridade = '#cc0000'  # Vermelho
                        elif prioridade == 'Média':
                            cor_prioridade = '#ff9900'  # Laranja
                        else:
                            cor_prioridade = '#009900'  # Verde
                        
                        elements.append(Paragraph(
                            f"<font face='ZapfDingbats'>4</font> <b>[{categoria}]</b> {recomendacao} <font color='{cor_prioridade}'><b>[{prioridade.upper()}]</b></font>",
                            self.styles['CustomBody']
                        ))
                    else:
                        # Formato antigo (string simples)
                        elements.append(Paragraph(f"<font face='ZapfDingbats'>4</font> {rec}", self.styles['CustomBody']))
        
        # Se tiver texto de análise (string)
        elif isinstance(actual_data, dict) and 'analysis_text' in actual_data:
            text = actual_data['analysis_text'].replace('\n', '<br/>')
            elements.append(Paragraph(text, self.styles['CustomBody']))
        
        # Se for string diretamente
        elif isinstance(actual_data, str):
            # Tentar parsear como JSON
            try:
                analysis_json = json.loads(actual_data)
                elements.extend(self._format_json_analysis(analysis_json))
            except:
                # Se não for JSON, adicionar como texto formatado
                elements.append(Paragraph(actual_data.replace('\n', '<br/>'), self.styles['CustomBody']))
        
        # Fallback: mostrar estrutura JSON
        else:
            elements.append(Paragraph(
                "<i>Formato de análise não reconhecido. Dados brutos:</i>",
                self.styles['Normal']
            ))
            elements.append(Spacer(1, 0.1*inch))
            json_str = json.dumps(actual_data, indent=2, ensure_ascii=False)
            # Dividir em linhas para melhor formatação
            for line in json_str.split('\n')[:50]:  # Limitar a 50 linhas
                elements.append(Paragraph(line, self.styles['Code']))
        
        return elements
    
    def _format_component_analysis(self, component: dict, number: int):
        """Formata a análise de um componente"""
        elements = []
        
        # Nome do componente
        comp_name = component.get('nome', f'Componente {number}')
        elements.append(Paragraph(
            f"{number}. {comp_name}",
            self.styles['CustomSection']
        ))
        
        # Tipo
        if 'tipo' in component:
            elements.append(Paragraph(
                f"<b>Tipo:</b> {component['tipo']}",
                self.styles['CustomBody']
            ))
        
        # Descrição
        if 'descricao' in component:
            elements.append(Paragraph(
                f"<b>Descrição:</b> {component['descricao']}",
                self.styles['CustomBody']
            ))
        
        elements.append(Spacer(1, 0.1*inch))
        
        # Ameaças identificadas
        if 'ameacas' in component:
            elements.append(Paragraph("<b>Ameaças Identificadas:</b>", self.styles['Highlight']))
            
            for ameaca in component['ameacas']:
                categoria = ameaca.get('categoria', 'N/A')
                descricao = ameaca.get('descricao', 'N/A')
                severidade = ameaca.get('severidade', 'Média')
                nome_ameaca = ameaca.get('nome_ameaca', '')
                impacto = ameaca.get('impacto', '')
                
                # Definir cor por severidade
                if severidade == 'Alta':
                    cor_severidade = '#cc0000'  # Vermelho
                    tag_sev = 'ALTA'
                elif severidade == 'Média':
                    cor_severidade = '#ff9900'  # Laranja
                    tag_sev = 'MÉDIA'
                else:
                    cor_severidade = '#009900'  # Verde
                    tag_sev = 'BAIXA'
                
                # Construir texto da ameaça
                if nome_ameaca:
                    texto = f"• <b>[{categoria}] {nome_ameaca}</b> <font color='{cor_severidade}'>[{tag_sev}]</font><br/>"
                else:
                    texto = f"• <b>[{categoria}]</b> <font color='{cor_severidade}'>[{tag_sev}]</font><br/>"
                
                texto += f"  {descricao}"
                
                if impacto:
                    texto += f"<br/>  <b>Impacto:</b> {impacto}"
                
                elements.append(Paragraph(texto, self.styles['CustomBody']))
                elements.append(Spacer(1, 0.05*inch))
        
        # Contramedidas
        if 'contramedidas' in component:
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph("<b>Contramedidas Recomendadas:</b>", self.styles['Highlight']))
            
            for contramedida in component['contramedidas']:
                # Verificar se é dicionário (novo formato) ou string (formato antigo)
                if isinstance(contramedida, dict):
                    # Novo formato estruturado
                    texto_contramedida = contramedida.get('contramedida', 'N/A')
                    prioridade = contramedida.get('prioridade', 'Média')
                    ameaca_rel = contramedida.get('ameaca_relacionada', '')
                    
                    # Definir cor por prioridade
                    if prioridade == 'Alta':
                        cor_prioridade = '#cc0000'  # Vermelho
                    elif prioridade == 'Média':
                        cor_prioridade = '#ff9900'  # Laranja
                    else:
                        cor_prioridade = '#009900'  # Verde
                    
                    # Formatar com prioridade
                    if ameaca_rel:
                        elements.append(Paragraph(
                            f"<font face='ZapfDingbats'>4</font> <b>[{ameaca_rel}]</b> {texto_contramedida} <font color='{cor_prioridade}'><b>[{prioridade.upper()}]</b></font>",
                            self.styles['CustomBody']
                        ))
                    else:
                        elements.append(Paragraph(
                            f"<font face='ZapfDingbats'>4</font> {texto_contramedida} <font color='{cor_prioridade}'><b>[{prioridade.upper()}]</b></font>",
                            self.styles['CustomBody']
                        ))
                else:
                    # Formato antigo (string simples)
                    elements.append(Paragraph(
                        f"<font face='ZapfDingbats'>4</font> {contramedida}",
                        self.styles['CustomBody']
                    ))
        
        elements.append(Spacer(1, 0.2*inch))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _format_json_analysis(self, data: dict):
        """Formata análise que está em formato JSON"""
        elements = []
        
        # Iterar pelas chaves principais
        for key, value in data.items():
            if key in ['componentes', 'components']:
                if isinstance(value, list):
                    for idx, comp in enumerate(value, 1):
                        elements.extend(self._format_component_analysis(comp, idx))
            else:
                # Adicionar outras seções
                elements.append(Paragraph(
                    key.replace('_', ' ').title(),
                    self.styles['CustomSection']
                ))
                
                if isinstance(value, (list, dict)):
                    elements.append(Paragraph(
                        "<pre>" + json.dumps(value, indent=2, ensure_ascii=False) + "</pre>",
                        self.styles['Code']
                    ))
                else:
                    elements.append(Paragraph(str(value), self.styles['CustomBody']))
                
                elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_stride_matrix(self, data: dict):
        """Cria a matriz STRIDE visual mostrando quais categorias se aplicam a cada componente"""
        elements = []
        
        elements.append(Paragraph("Matriz STRIDE - Visão Panorâmica", self.styles['CustomTitle']))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0066cc')))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph(
            """Esta matriz apresenta uma visão panorâmica de quais categorias STRIDE se aplicam a cada 
            componente da arquitetura. Uma célula marcada (X) indica que aquela categoria de ameaça 
            foi identificada para o componente.""",
            self.styles['CustomBody']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        matriz = data.get('matriz_stride', {})
        
        if not matriz:
            elements.append(Paragraph(
                "<i>Matriz STRIDE não disponível nesta análise.</i>",
                self.styles['Normal']
            ))
            return elements
        
        # Construir tabela da matriz
        # Headers: Componente, S, T, R, I, D, E
        matriz_data = [['Componente', 'S', 'T', 'R', 'I', 'D', 'E']]
        
        for componente, categorias in matriz.items():
            row = [componente[:30]]  # Limitar nome do componente
            for cat in ['S', 'T', 'R', 'I', 'D', 'E']:
                if categorias.get(cat, False):
                    row.append('X')
                else:
                    row.append('')
            matriz_data.append(row)
        
        # Criar tabela
        col_widths = [2.5*inch] + [0.5*inch] * 6
        matriz_table = Table(matriz_data, colWidths=col_widths)
        matriz_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            # Rows alternadas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            # Padding
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            # Cor dos checks
            ('TEXTCOLOR', (1, 1), (-1, -1), colors.HexColor('#cc0000')),
            ('FONTNAME', (1, 1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 1), (-1, -1), 12),
        ]))
        
        elements.append(matriz_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Legenda
        legenda_text = """
        <b>Legenda:</b><br/>
        <b>S</b> - Spoofing (Falsificação) | 
        <b>T</b> - Tampering (Adulteração) | 
        <b>R</b> - Repudiation (Repúdio) | 
        <b>I</b> - Information Disclosure (Vazamento) | 
        <b>D</b> - Denial of Service (Negação de Serviço) | 
        <b>E</b> - Elevation of Privilege (Elevação de Privilégio)
        """
        elements.append(Paragraph(legenda_text, self.styles['CustomBody']))
        
        return elements
    
    def _create_trust_boundaries_section(self, data: dict):
        """Cria a seção de Trust Boundaries (Fronteiras de Confiança)"""
        elements = []
        
        elements.append(Paragraph("Trust Boundaries - Fronteiras de Confiança", self.styles['CustomTitle']))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0066cc')))
        elements.append(Spacer(1, 0.2*inch))
        
        intro_text = """
        Trust Boundaries (Fronteiras de Confiança) são pontos críticos onde o nível de confiança muda 
        na arquitetura. A identificação e análise dessas fronteiras é fundamental na metodologia STRIDE, 
        pois são locais onde ataques frequentemente ocorrem. Qualquer dado que atravessa uma trust boundary 
        deve ser validado, autenticado e autorizado apropriadamente.
        """
        elements.append(Paragraph(intro_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        trust_boundaries = data.get('trust_boundaries', [])
        
        if not trust_boundaries:
            elements.append(Paragraph(
                "<i>Nenhuma trust boundary identificada ou informação não disponível.</i>",
                self.styles['Normal']
            ))
            return elements
        
        # Para cada trust boundary
        for idx, boundary in enumerate(trust_boundaries, 1):
            elements.append(Paragraph(
                f"{idx}. {boundary.get('nome', 'Trust Boundary')}",
                self.styles['CustomSection']
            ))
            
            # Descrição
            if 'descricao' in boundary:
                elements.append(Paragraph(
                    f"<b>Descrição:</b> {boundary['descricao']}",
                    self.styles['CustomBody']
                ))
            
            # Origem e Destino
            if 'componente_origem' in boundary and 'componente_destino' in boundary:
                elements.append(Paragraph(
                    f"<b>Travessia:</b> {boundary['componente_origem']} → {boundary['componente_destino']}",
                    self.styles['CustomBody']
                ))
            
            # Controles existentes
            if 'controles_existentes' in boundary and boundary['controles_existentes']:
                elements.append(Paragraph(
                    "<b>Controles de Segurança Existentes:</b>",
                    self.styles['Highlight']
                ))
                for controle in boundary['controles_existentes']:
                    elements.append(Paragraph(f"<font face='ZapfDingbats'>4</font> {controle}", self.styles['CustomBody']))
            
            # Ameaças
            if 'ameacas' in boundary and boundary['ameacas']:
                elements.append(Paragraph(
                    "<b>Ameaças Potenciais:</b>",
                    self.styles['Highlight']
                ))
                for ameaca in boundary['ameacas']:
                    elements.append(Paragraph(f"<font color='#cc0000'><b>!</b></font> {ameaca}", self.styles['CustomBody']))
            
            # Contramedidas recomendadas
            if 'contramedidas_recomendadas' in boundary and boundary['contramedidas_recomendadas']:
                elements.append(Paragraph(
                    "<b>Contramedidas Recomendadas:</b>",
                    self.styles['Highlight']
                ))
                for contramedida in boundary['contramedidas_recomendadas']:
                    elements.append(Paragraph(f"<font face='ZapfDingbats'>4</font> {contramedida}", self.styles['CustomBody']))
            
            elements.append(Spacer(1, 0.2*inch))
            elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_stride_methodology(self):
        """Cria a seção sobre metodologia STRIDE"""
        elements = []
        
        from stride_knowledge import STRIDE, STRIDE_DETAILS
        
        elements.append(Paragraph("Sobre a Metodologia STRIDE", self.styles['CustomTitle']))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0066cc')))
        elements.append(Spacer(1, 0.2*inch))
        
        intro_text = """
        STRIDE é uma metodologia de modelagem de ameaças desenvolvida pela Microsoft que fornece 
        um framework sistemático para identificar ameaças à segurança em sistemas de software. 
        O acrônimo representa seis categorias de ameaças:
        """
        
        elements.append(Paragraph(intro_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Tabela com categorias STRIDE
        stride_data = [['Categoria', 'Descrição', 'Foco']]
        
        stride_info = {
            'S - Spoofing': ('Falsificação de identidade', 'Autenticação'),
            'T - Tampering': ('Adulteração de dados', 'Integridade'),
            'R - Repudiation': ('Negação de ações', 'Não-repúdio'),
            'I - Information Disclosure': ('Vazamento de dados', 'Confidencialidade'),
            'D - Denial of Service': ('Negação de serviço', 'Disponibilidade'),
            'E - Elevation of Privilege': ('Elevação de privilégios', 'Autorização')
        }
        
        for cat, (desc, foco) in stride_info.items():
            stride_data.append([cat, desc, foco])
        
        stride_table = Table(stride_data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
        stride_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(stride_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Nota final
        footer_text = """
        <b>Nota:</b> Este relatório foi gerado automaticamente usando Inteligência Artificial 
        (GPT-4o com Vision) para análise de diagramas de arquitetura. As ameaças e recomendações 
        identificadas devem ser revisadas por especialistas em segurança para validação e 
        adaptação ao contexto específico do projeto.
        """
        
        elements.append(Paragraph(footer_text, self.styles['CustomBody']))
        
        return elements


def generate_stride_pdf_report(analysis_data, output_path: str, image_path: str = None):
    """
    Função helper para gerar relatório PDF
    
    Args:
        analysis_data: Dados da análise STRIDE
        output_path: Caminho do arquivo PDF a ser gerado
        image_path: Caminho da imagem do diagrama (opcional)
    
    Returns:
        str: Caminho do arquivo PDF gerado
    """
    generator = STRIDEReportGenerator()
    return generator.generate_report(analysis_data, output_path, image_path)
