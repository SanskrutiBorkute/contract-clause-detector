# ClauseGuard AI — PDF Report Generator Service
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.graphics.shapes import Drawing, Rect, String

# Curated harmonious color palette
VOID = HexColor("#080C14")
BG = HexColor("#0F1520")
BG2 = HexColor("#141C2E")
VIOLET = HexColor("#7C3AED")
VIO_BG = HexColor("#F5F3FF") # light background for callout
VIO_BORDER = HexColor("#DDD6FE")
RED = HexColor("#EF4444")
RED_BG = HexColor("#FEF2F2")
RED_BORDER = HexColor("#FEE2E2")
ORANGE = HexColor("#F97316")
AMBER = HexColor("#F59E0B")
AMB_BG = HexColor("#FEF3C7")
AMB_BORDER = HexColor("#FDE68A")
GREEN = HexColor("#10B981")
GRN_BG = HexColor("#ECFDF5")
GRN_BORDER = HexColor("#A7F3D0")
TEXT_DARK = HexColor("#1E293B")
TEXT_MUTED = HexColor("#64748B")
WHITE = HexColor("#FFFFFF")

def create_risk_distribution_chart(counts):
    """
    Renders a beautiful horizontal bar chart representing risk distribution.
    """
    d = Drawing(520, 90)
    categories = [
        ("Critical", counts.get("critical", 0), RED),
        ("High", counts.get("high", 0) or counts.get("warning", 0) or 0, ORANGE),
        ("Warning", counts.get("warning", 0) or counts.get("medium", 0) or 0, AMBER),
        ("Safe", counts.get("safe", 0) or counts.get("low", 0) or 0, GREEN)
    ]
    
    total = sum(c[1] for c in categories)
    if total == 0:
        total = 1
        
    y_offset = 70
    for name, count, color in categories:
        # Label
        d.add(String(10, y_offset + 2, f"{name} ({count})", fontName="Helvetica-Bold", fontSize=9, fillColor=TEXT_DARK))
        # Background bar track
        d.add(Rect(120, y_offset, 320, 10, fillColor=HexColor("#F1F5F9"), strokeColor=None))
        # Filled progress bar
        bar_width = (count / float(total)) * 320
        if bar_width > 0:
            d.add(Rect(120, y_offset, bar_width, 10, fillColor=color, strokeColor=None))
        y_offset -= 20
        
    return d

class ReportGenerator:
    @staticmethod
    def generate_pdf(analysis_data, output_path):
        """
        Generates a professional PDF risk report from the contract analysis JSON.
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        
        styles = getSampleStyleSheet()
        
        # Define custom typography
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=HexColor("#1E1B4B") # Indigo dark
        )
        
        h1_style = ParagraphStyle(
            'H1',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=HexColor("#1E1B4B"),
            spaceBefore=14,
            spaceAfter=6
        )
        
        h2_style = ParagraphStyle(
            'H2',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=15,
            textColor=HexColor("#312E81"),
            spaceBefore=8,
            spaceAfter=4
        )
        
        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=TEXT_DARK,
            spaceAfter=6
        )
        
        ai_summary_style = ParagraphStyle(
            'AISummary',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=10,
            leading=14.5,
            textColor=HexColor("#1E293B"),
            backColor=HexColor("#F8FAFC"),
            borderColor=HexColor("#E2E8F0"),
            borderWidth=1,
            borderPadding=10,
            spaceAfter=10,
            borderRadius=4
        )
        
        body_bold = ParagraphStyle(
            'BodyBold',
            parent=body_style,
            fontName='Helvetica-Bold'
        )

        meta_label_style = ParagraphStyle(
            'MetaLabel',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8.5,
            leading=11,
            textColor=TEXT_MUTED
        )

        meta_val_style = ParagraphStyle(
            'MetaVal',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=12.5,
            textColor=TEXT_DARK
        )
        
        code_style = ParagraphStyle(
            'CodeText',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=8.5,
            leading=11,
            textColor=HexColor("#0F172A")
        )

        sugg_style = ParagraphStyle(
            'SuggText',
            parent=body_style,
            fontName='Helvetica-Oblique',
            fontSize=9.5,
            leading=13,
            textColor=HexColor("#4338CA")
        )
        
        story = []
        
        # --- HEADER BANNER ---
        banner_data = [
            [Paragraph("⚖ ClauseGuard AI", ParagraphStyle('BLogo', fontName='Helvetica-Bold', fontSize=17, textColor=WHITE, leading=21)),
             Paragraph("CONTRACT RISK REPORT", ParagraphStyle('BSub', fontName='Helvetica-Bold', fontSize=9.5, textColor=HexColor("#C7D2FE"), alignment=2, leading=13))]
        ]
        banner_table = Table(banner_data, colWidths=[270, 270])
        banner_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), HexColor("#1E1B4B")),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 13),
            ('TOPPADDING', (0,0), (-1,-1), 13),
        ]))
        story.append(banner_table)
        story.append(Spacer(1, 15))
        
        # --- CONTRACT METADATA ---
        summary_info = analysis_data["summary"]
        score = summary_info["risk_score"]
        
        # Map overall risk text color
        if score >= 81:
            risk_color = RED
        elif score >= 61:
            risk_color = ORANGE
        elif score >= 26:
            risk_color = AMBER
        else:
            risk_color = GREEN
            
        meta_table_data = [
            [Paragraph("Contract Type:", meta_label_style), Paragraph(summary_info["contract_type"], meta_val_style),
             Paragraph("Overall Risk:", meta_label_style), Paragraph(f"<b>{summary_info['overall_risk']} ({score}/100)</b>", ParagraphStyle('RiskCol', parent=meta_val_style, textColor=risk_color))],
            [Paragraph("Total Clauses:", meta_label_style), Paragraph(str(summary_info["clause_count"]), meta_val_style),
             Paragraph("Issues Flagged:", meta_label_style), Paragraph(str(summary_info["issues_count"]), meta_val_style)],
            [Paragraph("Page Count:", meta_label_style), Paragraph(f"{summary_info.get('page_count', 1)} pages", meta_val_style),
             Paragraph("Processing Time:", meta_label_style), Paragraph(f"{summary_info.get('processing_time_ms', 0):.0f} ms", meta_val_style)],
            [Paragraph("Reading Time:", meta_label_style), Paragraph(f"{summary_info['reading_time_mins']} mins", meta_val_style),
             Paragraph("AI Confidence:", meta_label_style), Paragraph(f"{summary_info.get('confidence', 95)}%", meta_val_style)]
        ]
        meta_table = Table(meta_table_data, colWidths=[100, 170, 100, 170])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), HexColor("#F8FAFC")),
            ('GRID', (0,0), (-1,-1), 0.5, HexColor("#E2E8F0")),
            ('PADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 15))
        
        # --- EXECUTIVE SUMMARY ---
        story.append(Paragraph("AI Executive Summary", h1_style))
        ai_summary_text = summary_info.get("ai_executive_summary", "")
        story.append(Paragraph(f'"{ai_summary_text}"', ai_summary_style))
        story.append(Spacer(1, 10))
        
        # --- FINAL RECOMMENDATION ---
        recommendation = summary_info.get("overall_recommendation", "")
        final_rec_label = summary_info.get("final_recommendation", "Legal Review Recommended")
        story.append(Paragraph("Final Recommendation", h1_style))
        
        rec_color_hex = "#10B981"  # green
        if final_rec_label == "Do Not Sign":
            rec_color_hex = "#EF4444"  # red
        elif final_rec_label == "Legal Review Recommended":
            rec_color_hex = "#F97316"  # orange
        elif final_rec_label == "Sign After Negotiation":
            rec_color_hex = "#F59E0B"  # amber

        story.append(Paragraph(f"<b><font color='{rec_color_hex}'>{final_rec_label.upper()}</font></b>: {recommendation}", body_style))
        story.append(Spacer(1, 10))
        
        # --- RISK DISTRIBUTION CHART ---
        story.append(Paragraph("Risk Distribution", h1_style))
        chart = create_risk_distribution_chart(analysis_data.get("counts", {}))
        story.append(chart)
        story.append(Spacer(1, 10))
        
        # --- TOP 5 KEY RISKS ---
        top_risks = summary_info.get("top_risks", [])
        if top_risks:
            story.append(Paragraph("Top Identified Risks", h1_style))
            for i, r in enumerate(top_risks[:5]):
                r_col = RED if r["risk_level"] == "CRITICAL" else (ORANGE if r["risk_level"] == "HIGH" else AMBER)
                story.append(Paragraph(f"<b>{i+1}. {r['category']}</b> (<font color='{r_col}'><b>{r['risk_level']}</b></font>): {r['reason']}", body_style))
            story.append(Spacer(1, 15))
            
        # --- KEY ISSUES FOUND (TABLE) ---
        issues_list = analysis_data.get("issues", [])
        if issues_list:
            story.append(Paragraph("Summary of Flagged Issues", h1_style))
            issues_table_data = [[
                Paragraph("<b>Clause ID</b>", ParagraphStyle('TH1', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
                Paragraph("<b>Category</b>", ParagraphStyle('TH2', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
                Paragraph("<b>Risk Level</b>", ParagraphStyle('TH3', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
                Paragraph("<b>Identified Vulnerability</b>", ParagraphStyle('TH4', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE))
            ]]
            
            for issue in issues_list:
                r_level = issue["risk_level"]
                r_col = RED if r_level == "CRITICAL" else (ORANGE if r_level == "HIGH" else AMBER)
                issues_table_data.append([
                    Paragraph(issue["clause_id"].upper(), body_bold),
                    Paragraph(issue["title"].split("—")[0].strip(), body_style),
                    Paragraph(f"<b>{r_level}</b>", ParagraphStyle('RColor', parent=body_bold, textColor=r_col)),
                    Paragraph(issue["why"], body_style)
                ])
            
            issues_table = Table(issues_table_data, colWidths=[65, 125, 80, 270])
            issues_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), HexColor("#312E81")),
                ('GRID', (0,0), (-1,-1), 0.5, HexColor("#CBD5E1")),
                ('PADDING', (0,0), (-1,-1), 6),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, HexColor("#F8FAFC")]),
            ]))
            story.append(issues_table)
            story.append(Spacer(1, 15))
            
        # --- MISSING PROTECTIONS ---
        missing_list = analysis_data.get("missing_protections", [])
        if missing_list:
            story.append(Paragraph("Missing Protections", h1_style))
            missing_table_data = [[
                Paragraph("<b>Missing Protection</b>", ParagraphStyle('MTH1', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
                Paragraph("<b>Risk & Importance</b>", ParagraphStyle('MTH2', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
                Paragraph("<b>Suggested Wording / Remedy</b>", ParagraphStyle('MTH3', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE))
            ]]
            
            for missing in missing_list:
                missing_table_data.append([
                    Paragraph(missing["name"], body_bold),
                    Paragraph(missing["why_missing"], body_style),
                    Paragraph(missing.get("remedy", "Add standard wording."), body_style)
                ])
                
            missing_table = Table(missing_table_data, colWidths=[130, 210, 200])
            missing_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), HexColor("#475569")),
                ('GRID', (0,0), (-1,-1), 0.5, HexColor("#CBD5E1")),
                ('PADDING', (0,0), (-1,-1), 6),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, HexColor("#F8FAFC")]),
            ]))
            story.append(missing_table)
            story.append(Spacer(1, 20))
            
        # --- PAGE BREAK FOR CLAUSE-BY-CLAUSE BREAKDOWN ---
        story.append(PageBreak())
        
        story.append(Paragraph("Detailed Clause-by-Clause Risk Analysis", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph("The following is an explainable granular analysis of key clauses in the contract, detailing matched evidence, specific offending sentences, potential legal consequences, and suggested dynamic rewrites.", ParagraphStyle('Intro', parent=body_style, fontSize=10, leading=14, textColor=TEXT_MUTED)))
        story.append(Spacer(1, 15))
        
        for clause in analysis_data.get("clauses", []):
            if clause["risk_level"] == "SAFE" and clause["category"] not in ["Parties", "Dispute Resolution"]:
                continue
                
            clause_elements = []
            
            # Heading
            header_text = f"<b>{clause['number']} — {clause['title']}</b>"
            r_level = clause["risk_level"]
            risk_color = RED if r_level == "CRITICAL" else (ORANGE if r_level == "HIGH" else (AMBER if r_level == "WARNING" else GREEN))
            risk_badge = f" [RISK: {r_level}]"
            
            clause_elements.append(Paragraph(header_text + f" <font color='{risk_color}'><b>{risk_badge}</b></font>", h2_style))
            clause_elements.append(Spacer(1, 4))
            
            # Original text box (Monospace styled block with dynamic sentence highlight)
            clause_text = clause["text"]
            det_sent = clause.get("detected_sentence")
            if det_sent and det_sent != "N/A" and det_sent.strip() != "":
                escaped_text = clause_text.replace("<", "&lt;").replace(">", "&gt;")
                escaped_det_sent = det_sent.replace("<", "&lt;").replace(">", "&gt;")
                highlighted_sent = f"<b><font color='#B91C1C'>{escaped_det_sent}</font></b>"
                if escaped_det_sent in escaped_text:
                    clause_text = escaped_text.replace(escaped_det_sent, highlighted_sent)
                else:
                    clause_text = escaped_text
            else:
                clause_text = clause_text.replace("<", "&lt;").replace(">", "&gt;")

            orig_data = [[Paragraph("<b>Original Clause Text:</b>", ParagraphStyle('Lbl', fontName='Helvetica-Bold', fontSize=8, textColor=TEXT_MUTED)), ""],
                         [Paragraph(clause_text, code_style), ""]]
            orig_table = Table(orig_data, colWidths=[520, 20])
            orig_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), HexColor("#F1F5F9")),
                ('SPAN', (0,0), (1,0)),
                ('SPAN', (0,1), (1,1)),
                ('BOX', (0,0), (-1,-1), 1, HexColor("#E2E8F0")),
                ('PADDING', (0,0), (-1,-1), 8),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ]))
            clause_elements.append(orig_table)
            clause_elements.append(Spacer(1, 6))
            
            # Risk details and Explainability
            if clause["risk_level"] != "SAFE":
                clause_elements.append(Paragraph(f"<b>Vulnerability:</b> {clause['reason']}", body_style))
                
                # Explainability fields
                ev_str = ", ".join(clause.get("matched_evidence", [])) or "Contextual similarity"
                clause_elements.append(Paragraph(f"<b>Matched Evidence:</b> <font color='#EF4444'>'{ev_str}'</font> (Risk Weight: +{clause.get('risk_weight', 0)}) | <b>Confidence:</b> {clause.get('confidence', 95)}%", body_style))
                
                det_sent = clause.get("detected_sentence", "N/A")
                if det_sent and det_sent != "N/A":
                    clause_elements.append(Paragraph(f"<b>Flagged Sentence:</b> <font color='#475569'><i>\"{det_sent}\"</i></font>", body_style))
                
                clause_elements.append(Paragraph(f"<b>What this means:</b> {clause['explanation']}", body_style))
                clause_elements.append(Paragraph(f"<b>Consequences:</b> {clause['consequences']}", body_style))
                
                # Rewrite box (Violet callout block)
                rewrite_data = [[Paragraph("<b>AI Dynamic Rewrite (Safer Wording):</b>", ParagraphStyle('LblR', fontName='Helvetica-Bold', fontSize=8.5, textColor=HexColor("#4338CA"))), ""],
                                [Paragraph(clause["rewrite"], sugg_style), ""]]
                rewrite_table = Table(rewrite_data, colWidths=[520, 20])
                rewrite_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), VIO_BG),
                    ('SPAN', (0,0), (1,0)),
                    ('SPAN', (0,1), (1,1)),
                    ('BOX', (0,0), (-1,-1), 1, VIO_BORDER),
                    ('LINELEFT', (0,0), (0,-1), 3, VIOLET),
                    ('PADDING', (0,0), (-1,-1), 8),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ]))
                clause_elements.append(rewrite_table)
                clause_elements.append(Spacer(1, 6))
                
                # Negotiation Advice & Indian Laws
                laws_str = ", ".join(clause["indian_law"]) if clause["indian_law"] else "General Indian Contract Principles"
                clause_elements.append(Paragraph(f"<b>Relevant Indian Law:</b> <font color='#4338CA'>{laws_str}</font>", body_style))
                clause_elements.append(Paragraph(f"<b>How to Negotiate:</b> {clause['negotiation_advice']}", body_style))
                
                if clause["financial_impact"] != "None":
                    clause_elements.append(Paragraph(f"<b>Financial Exposure:</b> <font color='red'><b>{clause['financial_impact']}</b></font>", body_style))
            else:
                clause_elements.append(Paragraph("<b>Analysis:</b> Standard balanced clause. No immediate adjustments needed.", body_style))
                
            clause_elements.append(Spacer(1, 12))
            story.append(KeepTogether(clause_elements))
            
        # --- NEGOTIATION CHECKLIST ---
        checklist_elements = []
        checklist_elements.append(PageBreak())
        checklist_elements.append(Paragraph("ClauseGuard AI — Negotiation Checklist", title_style))
        checklist_elements.append(Spacer(1, 10))
        
        checklist_intro = "Before signing this contract, ensure you have addressed the following items with the counterpart. Use the AI Suggested Rewrites from the previous pages as your template guide:"
        checklist_elements.append(Paragraph(checklist_intro, body_style))
        checklist_elements.append(Spacer(1, 10))
        
        checklist_items = [
            "<b>Security Deposit Capping:</b> Request reduction of security deposit to 2-3 months rent.",
            "<b>Disclaim Wear and Tear:</b> Ensure a clause explicitly declares that security deposit is returned in full, excluding normal wear & tear.",
            "<b>Mutual notice periods:</b> Standardize notice periods so both parties have equal notice periods (minimum 30 days) to terminate.",
            "<b>Cure periods:</b> Add a cure period (minimum 15 days) to rectify defaults before termination can be initiated.",
            "<b>Limit entry rights:</b> Require at least 24 hours advance written notice for any inspection or entry visits.",
            "<b>Rent escalation limits:</b> Cap annual rent increases at a maximum of 5% to 8% per annum.",
            "<b>Incorporate Force Majeure:</b> Ensure a modern act of god/lockdown clause is added to suspend rent obligations.",
            "<b>Document conditions:</b> Record property inventory and physical conditions with dated photos prior to taking possession."
        ]
        
        for item in checklist_items:
            checklist_elements.append(Paragraph(f"• [ ] {item}", ParagraphStyle('Chkl', parent=body_style, leftIndent=15, spaceAfter=8)))
            
        checklist_elements.append(Spacer(1, 30))
        checklist_elements.append(Paragraph("<b>Disclaimer:</b> This report is generated by an Artificial Intelligence system. It is designed to assist you in understanding commercial contracts and does not constitute formal legal advice. Please consult with a registered legal practitioner (lawyer) before signing any legally binding agreements.", ParagraphStyle('Discl', parent=body_style, fontName='Helvetica-Oblique', fontSize=8, textColor=TEXT_MUTED)))
        
        story.append(KeepTogether(checklist_elements))
        
        # Build PDF document
        doc.build(story)
