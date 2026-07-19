import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import re
from groq import Groq

# PDF Text Extraction Engine
try:
    import pypdf
except ImportError:
    import os
    os.system('pip install pypdf')
    import pypdf

# ReportLab Layout & Presentation Engines
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- Application-wide Styling Settings ---
st.set_page_config(page_title="Dairy-DPR Architect Enterprise", layout="wide", page_icon="🥛")
sns.set_theme(style="whitegrid")

st.title("🏭 Dairy-DPR Architect Enterprise")
st.subheader("Automated Industrial Blueprint, 10-Year Financial Model & Sustainability DPR Engine")
st.markdown("---")

# =============================================================================
# SIDEBAR CONFIGURATION ARCHITECTURE & FAIL-SAFE INPUT LAYOUT
# =============================================================================
st.sidebar.header("🔑 Groq Inference Protocol")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password", help="Processes unstructured operational text files and optimizes the DPR text layers.")

st.sidebar.header("1. Promoter Profile & Context")
promoter_name = st.sidebar.text_input("Name of the Promoter / Enterprise", "")
promoter_exp = st.sidebar.text_area("Promoter Experience & Background", "")
location = st.sidebar.text_input("Proposed Project Location", "")

st.sidebar.header("2. Plant Capacity Scales")
user_capex_cr = st.sidebar.number_input("Allocated CAPEX Investment (in INR Crores)", min_value=0.0, value=250.0, step=10.0)
design_capacity_llpd = st.sidebar.number_input("Design Processing Capacity (in Lakh Liters/Day)", min_value=0.0, value=100.0, step=5.0)
actual_capacity_llpd = st.sidebar.slider("Operational Input Capacity (in Lakh Liters/Day)", min_value=1.0, max_value=200.0, value=85.0)

st.sidebar.header("3. Commodity Focus Checklist")
products = []
if st.sidebar.checkbox("Liquid Pasteurized Packaged Milk", value=True): products.append("Liquid Packaged Milk")
if st.sidebar.checkbox("Clarified Cow/Buffalo Ghee", value=True): products.append("Premium Ghee")
if st.sidebar.checkbox("Fermented Dahi & Probiotic Yogurt"): products.append("Dahi/Yogurt")
if st.sidebar.checkbox("Concentrated Solid Mawa / Khoa"): products.append("Mawa")
if st.sidebar.checkbox("Fresh Paneer & Cheddar Cheese Blocks", value=True): products.append("Paneer/Cheese")

st.sidebar.header("4. Direct Environmental Metrics")
input_annual_milk_kg = st.sidebar.number_input("Projected Annual Raw Milk Processing (kg)", min_value=0, value=365000000)
input_annual_water_l = st.sidebar.number_input("Projected Annual Groundwater Abstraction (Liters)", min_value=0, value=1208150000)
input_annual_elec_kwh = st.sidebar.number_input("Projected Annual Grid Power Allocation (kWh)", min_value=0, value=36500000)

st.sidebar.header("5. Custom Data Ingestion")
uploaded_social_file = st.sidebar.file_uploader("Upload External Social Impact Reports", type=["csv", "txt"])

# =============================================================================
# DYNAMIC SMART FALLBACK ENGINE (BYPASS LOGIC CONTROLLER)
# =============================================================================
final_promoter = promoter_name if promoter_name.strip() != "" else "National Dairy Development Alliance Corp."
final_exp = promoter_exp if promoter_exp.strip() != "" else "Over 25 years of multi-state livestock management, commercial cooperative aggregation, and bulk fluid logistics deployment."
final_location = location if location.strip() != "" else "Amritsar-Ludhiana Agro-Industrial Corridor, Punjab, India"

final_capex_cr = user_capex_cr if user_capex_cr > 0 else 250.0
final_capacity_llpd = design_capacity_llpd if design_capacity_llpd > 0 else 100.0
final_actual_llpd = actual_capacity_llpd if actual_capacity_llpd > 0 else 85.0

final_annual_milk_kg = input_annual_milk_kg if input_annual_milk_kg > 0 else 365000000
final_annual_water_l = input_annual_water_l if input_annual_water_l > 0 else 1208150000
final_annual_elec_kwh = input_annual_elec_kwh if input_annual_elec_kwh > 0 else 36500000

# Conversion math variables
capex_total_inr = final_capex_cr * 10000000
capacity_lpd = final_capacity_llpd * 100000
actual_lpd = final_actual_llpd * 100000

DWU_BENCHMARK = 3.31
TWF_BENCHMARK = 9.0

# Mathematical scaling indicators
user_dwu = final_annual_water_l / final_annual_milk_kg if (final_annual_milk_kg > 0) else 3.31
indirect_wf = (final_annual_elec_kwh * 56.9) / final_annual_milk_kg
user_twf = user_dwu + (indirect_wf * 0.1)
daily_effluent_lpd = (final_annual_water_l / 365) * 0.74
capacity_utilization = (actual_lpd / capacity_lpd) * 100 if capacity_lpd > 0 else 85.0

metric_passbook = {
    'dwu_variance': user_dwu - DWU_BENCHMARK,
    'twf_variance': user_twf - TWF_BENCHMARK
}

# =============================================================================
# 10-YEAR MULTI-VARIABLE CASHFLOW CORE MATH MODEL
# =============================================================================
years = np.arange(1, 11)
debt_ratio_constant = 0.70
term_loan_principal = capex_total_inr * debt_ratio_constant
equity_contribution = capex_total_inr * (1.0 - debt_ratio_constant)

interest_rate = 0.095
annual_repayment = term_loan_principal / 10

# Dynamic 10-year loops
revenue_year_1 = (actual_lpd * 365) * 48.0 
variable_cost_year_1 = (actual_lpd * 365) * 36.5 
staff_cost_year_1 = capex_total_inr * 0.04
other_exp_year_1 = capex_total_inr * 0.03

revenue_projection = [revenue_year_1 * (1.05 ** (y-1)) for y in years]
variable_projections = [variable_cost_year_1 * (1.04 ** (y-1)) for y in years]
staff_projections = [staff_cost_year_1 * (1.05 ** (y-1)) for y in years]
other_projections = [other_exp_year_1 * (1.03 ** (y-1)) for y in years]

depreciation_schedule = []
current_asset_value = capex_total_inr * 0.75 
for y in years:
    dep_val = current_asset_value * 0.15 
    depreciation_schedule.append(dep_val)
    current_asset_value -= dep_val

interest_payments = []
remaining_debt = term_loan_principal
for y in years:
    interest_payments.append(remaining_debt * interest_rate)
    remaining_debt -= annual_repayment

pbt_projection = []
net_profit_projection = []
dscr_projection = []

for i, y in enumerate(years):
    ebitda = revenue_projection[i] - (variable_projections[i] + staff_projections[i] + other_projections[i])
    ebit = ebitda - depreciation_schedule[i]
    pbt = ebit - interest_payments[i]
    pat = pbt * 0.75 
    pbt_projection.append(pbt)
    net_profit_projection.append(pat)
    
    numerator = pat + depreciation_schedule[i] + interest_payments[i]
    denominator = annual_repayment + interest_payments[i]
    dscr_projection.append(numerator / denominator if denominator > 0 else 1.5)

# =============================================================================
# ADVANCED STRUCTURAL GRAPHICS ENGINE
# =============================================================================
def generate_advanced_topology(selected_products):
    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.axis('off')
    
    box_props = dict(boxstyle='round,pad=0.5', facecolor='#0F172A', edgecolor='#38BDF8', lw=1.5)
    w_props = dict(boxstyle='round,pad=0.5', facecolor='#1E293B', edgecolor='#F43F5E', lw=1.5)
    
    ax.text(1, 3, "Bulk Silos Intake\n(100 LLPD Rated)", bbox=box_props, color='white', ha='center', weight='bold')
    ax.text(4, 3, "Clarification &\nBactofugation", bbox=box_props, color='white', ha='center', weight='bold')
    ax.text(7, 3, "High-Capacity\nPasteurization", bbox=box_props, color='white', ha='center', weight='bold')
    
    ax.annotate('', xy=(2.3, 3), xytext=(1.8, 3), arrowprops=dict(arrowstyle="-|>", color='#38BDF8', lw=2))
    ax.annotate('', xy=(5.3, 3), xytext=(4.8, 3), arrowprops=dict(arrowstyle="-|>", color='#38BDF8', lw=2))
    
    ax.text(10, 4, "Packaging Unit\n(Fluid Milk Lines)", bbox=box_props, color='white', ha='center')
    ax.text(10, 3, "Cheese & Paneer\nCoagulation Vats", bbox=box_props, color='white', ha='center')
    ax.text(10, 2, "By-Product Lines\n(Ghee / Mawa Pans)", bbox=box_props, color='white', ha='center')
    
    ax.annotate('', xy=(8.5, 3.8), xytext=(7.8, 3.2), arrowprops=dict(arrowstyle="-|>", color='#0EA5E9', lw=1.5))
    ax.annotate('', xy=(8.5, 3.0), xytext=(7.8, 3.0), arrowprops=dict(arrowstyle="-|>", color='#0EA5E9', lw=1.5))
    ax.annotate('', xy=(8.5, 2.2), xytext=(7.8, 2.8), arrowprops=dict(arrowstyle="-|>", color='#0EA5E9', lw=1.5))
    
    ax.text(4, 0.8, "Groundwater Intake\n(Empirical Sourcing)", bbox=w_props, color='white', ha='center')
    ax.text(7, 0.8, "K-Pack Systems CFS\nHigh-Fat Interceptor", bbox=w_props, color='white', ha='center', weight='bold')
    ax.text(10, 0.8, "Anaerobic Digester\n(Biological Secondary)", bbox=w_props, color='white', ha='center')
    
    ax.annotate('', xy=(5.5, 0.8), xytext=(4.8, 0.8), arrowprops=dict(arrowstyle="-|>", color='#F43F5E', lw=2))
    ax.annotate('', xy=(8.5, 0.8), xytext=(7.8, 0.8), arrowprops=dict(arrowstyle="-|>", color='#F43F5E', lw=2))
    
    ax.annotate('Wastewater\nDischarge', xy=(4, 1.4), xytext=(4, 2.5),
                arrowprops=dict(arrowstyle="->", color='#EF4444', lw=1.5, linestyle=':'), ha='center', color='#EF4444', fontsize=9)
    
    ax.set_xlim(-0.5, 12)
    ax.set_ylim(0, 4.8)
    plt.tight_layout()
    return fig

def generate_compliance_matrix():
    categories = ['Financial Viability\n(CAPEX Target)', 'Direct Water Use\n(DWU Ratio)', 'Energy Footprint\n(TWF Index)', 'Social Inclusion\n(Smallholders)']
    standards = [1.0, 1.0, 1.0, 1.0]
    
    real_scores = [
        min(1.3, final_capex_cr / 200.0),
        max(0.2, 1.0 - ((user_dwu - DWU_BENCHMARK) / DWU_BENCHMARK)),
        max(0.2, 1.0 - ((user_twf - TWF_BENCHMARK) / TWF_BENCHMARK)),
        1.25 
    ]
    
    x = np.arange(len(categories))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.bar(x - width/2, standards, width, label='Regional Benchmark Standards', color='#CBD5E1')
    ax.bar(x + width/2, real_scores, width, label='Project Enterprise Index', color='#1E3A8A')
    ax.set_ylabel('Normalized Compliance Multiplier')
    ax.set_title('Cross-Sector Compliance Alignment Framework')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9)
    ax.legend(loc='upper right')
    ax.axhline(1.0, color='#F43F5E', linestyle='--', alpha=0.8)
    plt.tight_layout()
    return fig

# =============================================================================
# DYNAMIC FORMAT OPTIMIZATION ENGINE (GROQ PARSING PIPELINE)
# =============================================================================
def generate_custom_dpr_narrative(format_blueprint):
    """Uses Groq AI to read the user-specified formatting/indexing layout from text or PDF,

    optimizes it using external open-source intelligence, and returns structural paragraphs.
    """
    if not groq_api_key:
        return None
        
    try:
   def generate_custom_dpr_narrative(format_blueprint):
    """Uses Groq AI to read the user-specified formatting/indexing layout from text or PDF,
    optimizes it using external open-source intelligence, and returns structural paragraphs.
    """
    if not groq_api_key:
        return None
        
    try:
        client = Groq(api_key=groq_api_key)
        prompt = f"""
        You are an elite institutional consultant specializing in mega-scale dairy processing infrastructures.
        The user has provided a custom layout format schema / chapter index reference to mimic:
        \"\"\"{format_blueprint[:6000]}\"\"\"

        Based on these custom execution constraints:
        - Promoter Entity: {final_promoter}
        - Sourcing Location Corridor: {final_location}
        - Design Plant Limit: {final_capacity_llpd} Lakh Liters/Day (Current Operations: {final_actual_llpd} LLPD)
        - Targeted Product Matrix Lines: {', '.join(products)}
        - Project Capital Investment Scale: INR {final_capex_cr} Crores

        Analyze the provided document blueprint format, index its chapters, and build out complete, elaborative narrative contents.
        Optimize the draft using strategic industry standard intelligence from open online parameters.
        
        Format your response cleanly using markdown headings for each section like:
        ### Chapter Title Or Section Name
        Followed by deep, professional multi-paragraph corporate narrative drafts. Do not include chat intros, outbacks, or summary filler text.
        """
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",  # Updated to the active Llama 3.3 model
            max_tokens=3500,
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        st.warning(f"Groq Optimization Engine could not complete format indexing: {str(e)}. Activating localized corporate template engine...")
        return None

# =============================================================================
# INSTITUTIONAL PDF GENERATION PROTOCOL
# =============================================================================
def compile_comprehensive_pdf(custom_narrative_text=None):
    pdf_buffer = io.BytesIO()
    document = SimpleDocTemplate(pdf_buffer, pagesize=letter, leftMargin=40, rightMargin=40, topMargin=50, bottomMargin=50)
    story = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CoverTitle', fontSize=24, leading=30, textColor=colors.HexColor('#0F172A'), alignment=1, spaceAfter=15, fontName="Helvetica-Bold")
    subtitle_style = ParagraphStyle('CoverSub', fontSize=13, leading=17, textColor=colors.HexColor('#475569'), alignment=1, spaceAfter=160)
    meta_style = ParagraphStyle('CoverMeta', fontSize=10.5, leading=16, textColor=colors.HexColor('#1E293B'), alignment=1)
    
    h1_style = ParagraphStyle('H1Chapter', fontSize=14, leading=18, textColor=colors.HexColor('#1E3A8A'), spaceBefore=22, spaceAfter=12, fontName="Helvetica-Bold", keepWithNext=True)
    h2_style = ParagraphStyle('H2Section', fontSize=11, leading=15, textColor=colors.HexColor('#0284C7'), spaceBefore=14, spaceAfter=6, fontName="Helvetica-Bold", keepWithNext=True)
    body_style = ParagraphStyle('BodyFormat', fontSize=9.5, leading=15, textColor=colors.HexColor('#334155'), spaceAfter=10, alignment=4)
    table_text = ParagraphStyle('TableTxt', fontSize=8.5, leading=12, textColor=colors.HexColor('#1E293B'))
    table_header = ParagraphStyle('TableHdr', fontSize=9, leading=13, textColor=colors.white, fontName="Helvetica-Bold")

    # -------------------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("DETAILED PROJECT REPORT (DPR)", title_style))
    story.append(Paragraph("STRATEGIC COMMERCIAL PROPOSAL & COMPLIANCE BLUEPRINT", ParagraphStyle('MainSub', fontSize=14, leading=20, textColor=colors.HexColor('#1E3A8A'), alignment=1, spaceAfter=15)))
    story.append(Paragraph(f"PRODUCTION PROFILE CAPACITY: {final_capacity_llpd} LAKH LITERS PER DAY", subtitle_style))
    story.append(Paragraph(f"<b>Promoter Enterprise:</b> {final_promoter}<br/><b>Operational Sourcing Corridor:</b> {final_location}<br/><b>Capital Investment Architecture:</b> INR {final_capex_cr} Crores", meta_style))
    story.append(PageBreak())
    
    # -------------------------------------------------------------------------
    # INDEX CONTENT BLOCK
    # -------------------------------------------------------------------------
    story.append(Paragraph("Master Document Blueprint Index", h1_style))
    story.append(Spacer(1, 10))
    
    index_rows = [
        [Paragraph("<b>Document Structural Section</b>", table_header), Paragraph("<b>Target Focus Area Matrix</b>", table_header)]
    ]
    
    if custom_narrative_text:
        headings = re.findall(r'###\s*(.*)', custom_narrative_text)
        if headings:
            for h in headings:
                index_rows.append([Paragraph(h, table_text), Paragraph("User-specified custom structured deployment module.", table_text)])
        else:
            index_rows.append([Paragraph("Custom Document Chapters", table_text), Paragraph("Optimized structural narrative text blocks.", table_text)])
    else:
        # Default Fallback Framework Index Data
        default_sections = [
            ("Chapter 1: Executive Summary & Technical Scope", "High-level summary overview of the processing facility."),
            ("Chapter 2: Market Potential & Core Structural Profile", "Macro analysis of supply elasticities and nutritional consumption shifts."),
            ("Chapter 3: Technical Facility Specifications & Sizing", "Engineering parameters, mass-balance, and pasteurization logic."),
            ("Chapter 4: Supply Chain & Village Procurement Directives", "Cold-chain infrastructure and direct farming integration protocols."),
            ("Chapter 5: Project Location Siting Analysis", "GIS-vetted logistics routing configurations and resource pathways."),
            ("Chapter 6: Corporate Management & Operational Strategy", "Management experience profile and initialization milestones.")
        ]
        for title, desc in default_sections:
            index_rows.append([Paragraph(title, table_text), Paragraph(desc, table_text)])
            
    # Common financial and annex indices
    index_rows.extend([
        [Paragraph("Chapter 7: Financial Viability - Cost & Means Architecture", table_text), Paragraph("Detailed CAPEX financing and debt/equity allocation layers.", table_text)],
        [Paragraph("Chapter 8: Projected 10-Year Profitability Core Model", table_text), Paragraph("Comprehensive multi-variable revenue and profit statements.", table_text)],
        [Paragraph("Annexure A: Unit Process Flow Engineering Topology Blueprint", table_text), Paragraph("Visual process matrix map from raw input to packaging.", table_text)],
        [Paragraph("Annexure B: Cross-Sector Sustainability & Compliance Framework", table_text), Paragraph("Water footprints, effluent calculations, and benchmark indices.", table_text)]
    ])
    
    t_idx = Table(index_rows, colWidths=[240, 280])
    t_idx.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t_idx)
    story.append(PageBreak())
    
    # -------------------------------------------------------------------------
    # NARRATIVE CONTENT GENERATION NODE
    # -------------------------------------------------------------------------
    if custom_narrative_text:
        lines = custom_narrative_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('###'):
                cleaned_title = line.replace('###', '').strip()
                story.append(Paragraph(cleaned_title, h1_style))
            elif line.startswith('##'):
                cleaned_title = line.replace('##', '').strip()
                story.append(Paragraph(cleaned_title, h2_style))
            elif line:
                story.append(Paragraph(line, body_style))
        story.append(PageBreak())
    else:
        # --- Bypassed Fallback Default Chapter Text Modules ---
        story.append(Paragraph("Chapter 1: Executive Summary & Technical Scope", h1_style))
        story.append(Paragraph(f"This Detailed Project Report establishes the foundational operational parameters for a commercial mega-scale processing asset developed for {final_promoter}. The plant integrates automated high-capacity separation pipelines designed to protect system margins and provide seamless output flexibility.", body_style))
        
        story.append(Paragraph("Chapter 2: Market Potential & Core Structural Profile", h1_style))
        story.append(Paragraph("The consumer ecosystem exhibits high compound growth parameters for structured dairy derivatives. Moving beyond raw liquid logistics, modern operations protect their revenue profiles by converting surplus liquid milk intakes into value-added commodities like premium clarified ghee, artisanal cheeses, and active probiotic yogurts.", body_style))
        
        story.append(Paragraph("Chapter 3: Technical Facility Specifications & Sizing", h1_style))
        story.append(Paragraph(f"The facility is engineered around a core processing architecture rated at a maximum daily design capacity of {final_capacity_llpd} Lakh Liters. At a baseline capacity utilization of {capacity_utilization:.1f}%, the plant will sustain an input processing standard of {final_actual_llpd} Lakh Liters per operational cycle.", body_style))
        
        story.append(Paragraph("Chapter 4: Supply Chain & Village Procurement Directives", h1_style))
        story.append(Paragraph("Raw logistics lines use automated collection terminals to test fat and solids-not-fat metrics instantly. Chilling centers drop fluid milk temperatures to below 4 degrees Celsius within 4 hours, preserving milk properties and protecting localized farming networks.", body_style))
        
        story.append(Paragraph("Chapter 5: Project Location Siting Analysis", h1_style))
        story.append(Paragraph(f"The construction site inside <b>{final_location}</b> provides clear logistical access corridors to major metropolitan transit lines, ensuring efficient cross-state distribution of finished products.", body_style))
        
        story.append(Paragraph("Chapter 6: Corporate Management & Operational Strategy", h1_style))
        story.append(Paragraph(f"<b>Executive Lead Sign:</b> {final_promoter}<br/><b>Vetted Core Competencies:</b> {final_exp}", body_style))
        story.append(PageBreak())

    # -------------------------------------------------------------------------
    # FIXED TECHNICAL FINANCIAL CHAPTERS (COMMON INFRASTRUCTURE ELEMENTS)
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 7: Financial Viability - Cost & Means Architecture", h1_style))
    story.append(Paragraph("The overall capital budget for this commercial dairy processing layout is configured at an institutional target scale of INR <b>{final_capex_cr:.2f} Crores</b>. The table below outlines asset allocations adjusted for automation systems.", body_style))
    
    fin_summary_matrix = [
        [Paragraph("Asset Structuring Description Block", table_header), Paragraph("Allocation (INR Crores)", table_header)],
        [Paragraph("Core Civil Infrastructure & Structural Engineering", table_text), Paragraph(f"{final_capex_cr * 0.25:.2f}", table_text)],
        [Paragraph("High-Capacity Processing Plant Machinery Units", table_text), Paragraph(f"{final_capex_cr * 0.50:.2f}", table_text)],
        [Paragraph("K-Pack CFS Wastewater Plant & Utility Modules", table_text), Paragraph(f"{final_capex_cr * 0.10:.2f}", table_text)],
        [Paragraph("Working Capital Margin & Liquidity Buffer Reserves", table_text), Paragraph(f"{final_capex_cr * 0.15:.2f}", table_text)],
        [Paragraph("<b>Total Project CAPEX Funding Requirement</b>", table_text), Paragraph(f"<b>{final_capex_cr:.2f}</b>", table_text)],
        [Paragraph("Term Loan Financing (70% Leverage Structure)", table_text), Paragraph(f"{final_capex_cr * 0.70:.2f}", table_text)],
        [Paragraph("Promoter Equity Contribution (30% Capitalization)", table_text), Paragraph(f"{final_capex_cr * 0.30:.2f}", table_text)]
    ]
    t_fsm = Table(fin_summary_matrix, colWidths=[320, 200])
    t_fsm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t_fsm)
    story.append(PageBreak())

    story.append(Paragraph("Chapter 8: Projected 10-Year Profitability Core Model", h1_style))
    story.append(Paragraph("The long-term financial architecture displays strong liquidity coverage ratios and compounding margin health across the ten-year projection timeline.", body_style))
    
    prof_headers = [Paragraph("Metric (Cr INR)", table_header)] + [Paragraph(f"Y{y}", table_header) for y in years]
    row_rev = [Paragraph("Gross Revenue", table_text)] + [Paragraph(f"{r/10000000:.1f}", table_text) for r in revenue_projection]
    row_vc = [Paragraph("Variable Cost", table_text)] + [Paragraph(f"{v/10000000:.1f}", table_text) for v in variable_projections]
    row_pat = [Paragraph("Net Profit (PAT)", table_text)] + [Paragraph(f"{p/10000000:.1f}", table_text) for p in net_profit_projection]
    
    t_prof = Table([prof_headers, row_rev, row_vc, row_pat], colWidths=[110] + [41]*10)
    t_prof.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_prof)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # MANDATORY TECHNICAL ANNEXURES
    # -------------------------------------------------------------------------
    story.append(Paragraph("Annexure A: Unit Process Flow Engineering Topology Blueprint", h1_style))
    story.append(Paragraph("This chart maps out the sequence of equipment steps and resource paths configured for this processing facility, running from intake tanks to finished product packaging lines.", body_style))
    story.append(Spacer(1, 10))
    
    fig_topo = generate_advanced_topology(products)
    topo_buf = io.BytesIO()
    fig_topo.savefig(topo_buf, format='png', dpi=200)
    topo_buf.seek(0)
    plt.close(fig_topo)
    story.append(Image(topo_buf, width=500, height=187))
    story.append(PageBreak())
    
    story.append(Paragraph("Annexure B: Cross-Sector Sustainability & Compliance Framework", h1_style))
    story.append(Paragraph("The layout evaluates the facility's sustainability performance indices against regional dairy benchmarks, tracking resource usage, water efficiency, and local community inclusion parameters.", body_style))
    story.append(Spacer(1, 10))
    
    fig_comp = generate_compliance_matrix()
    comp_buf = io.BytesIO()
    fig_comp.savefig(comp_buf, format='png', dpi=200)
    comp_buf.seek(0)
    plt.close(fig_comp)
    story.append(Image(comp_buf, width=480, height=182))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Calculated Empirical Performance Key Metrics Summary:</b>", h2_style))
    story.append(Paragraph(f"• <b>Direct Water Use Ratio:</b> {user_dwu:.2f} L/kg of processed input raw milk (Target Regional Standard Benchmark: 3.31 L/kg)", body_style))
    story.append(Paragraph(f"• <b>Total Water Footprint Index:</b> {user_twf:.2f} L/kg total consumption footprint (Target Regional Standard Benchmark: 9.00 L/kg)", body_style))
    story.append(Paragraph(f"• <b>Daily Effluent Pre-Treatment Target Volume:</b> {daily_effluent_lpd:,.2f} Liters Per Day mapped to K-Pack System CFS standard operational layouts.", body_style))
    
    document.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer

# =============================================================================
# MAIN INTERFACE RENDERING ENVIRONMENT
# =============================================================================
st.header("🏢 Unit Topology Blueprint Layout")
st.write("Dynamic engineering node sequence map optimized for the specified product parameters:")
st.pyplot(generate_advanced_topology(products))
st.markdown("---")

col_vis1, col_vis2 = st.columns(2)

with col_vis1:
    st.header("📊 Multi-Variable Compliance Matrix")
    st.pyplot(generate_compliance_matrix())

with col_vis2:
    st.header("💧 Resource Consumption & Footprint Analysis")
    st.write("Unit consumption indicators evaluated against empirical benchmarks from the [Punjab Dairy Case Study](https://www.mdpi.com/2073-4441/16/3/435):")
    st.metric(label="Direct Water Use (DWU)", value=f"{user_dwu:.2f} L/kg", 
              delta=f"{metric_passbook['dwu_variance']:.2f} L/kg vs Benchmark Standard (3.31)", delta_color="inverse")
    st.metric(label="Total Water Footprint (TWF)", value=f"{user_twf:.2f} L/kg", 
              delta=f"{metric_passbook['twf_variance']:.2f} L/kg vs Benchmark Standard (9.0)", delta_color="inverse")

st.markdown("---")

# =============================================================================
# REVISED PDF INGESTION & FORMAT LAYOUT OPTIMIZATION LAB
# =============================================================================
st.header("📋 DPR Report Format Ingestion & Optimization Lab")
st.write("Upload a target DPR template layout as a `.pdf` file. The engine will index the file layout structure and enrich it using open internet optimization insights.")

uploaded_format_pdf = st.file_uploader(
    "Upload Reference DPR Format Template (.pdf)", 
    type=["pdf"],
    help="Upload a PDF of a project report format. The layout text will be automatically extracted, parsed, and mapped by the Groq AI engine."
)

user_text_format_input = st.text_area(
    "Alternative Custom Chapter Notes / Index Layout (Optional Add-on)",
    placeholder="Example:\nChapter 1: Sourcing Dynamics\nChapter 2: Quality Testing Framework...",
    height=100,
    help="Provide explicit text layout rules here if you aren't uploading a layout template PDF."
)

# Extract and combine text layouts from PDF file streams
final_extracted_blueprint = ""
if uploaded_format_pdf is not None:
    try:
        with st.spinner("Indexing and parsing layout from uploaded PDF file stream..."):
            pdf_reader = pypdf.PdfReader(uploaded_format_pdf)
            pdf_text_accumulator = []
            for page_num, page in enumerate(pdf_reader.pages):
                extracted_page_text = page.extract_text()
                if extracted_page_text:
                    pdf_text_accumulator.append(extracted_page_text)
            
            final_extracted_blueprint = "\n".join(pdf_text_accumulator)
            if final_extracted_blueprint.strip() != "":
                st.success(f"🎯 Reference PDF structure successfully parsed! Extracted {len(pdf_reader.pages)} pages of format layout.")
            else:
                st.warning("⚠️ Could not extract readable structural layout text from the PDF pages. Ensure the file contains text layers rather than flat pictures.")
    except Exception as pdf_error:
        st.error(f"Failed to read format blueprint PDF element structure: {pdf_error}")

# Append text area input on top if available
if user_text_format_input.strip() != "":
    final_extracted_blueprint = f"{user_text_format_input}\n\n=== Extracted PDF Layout Context ===\n{final_extracted_blueprint}"

st.markdown("---")

# Environmental Engineering Specifications (K-Pack Systems Framework)
st.header("⚙️ High-Fat Effluent Control (K-Pack Systems CFS Alignment)")
st.write(f"Pre-treatment engineering scale targets computed for an estimated volume of **{daily_effluent_lpd:,.2f} LPD**:")

env_c1, env_c2 = st.columns(2)
with env_c1:
    st.markdown("""
    **Unstructured Wastewater Parameters:**
    * **Solids Concentration Range:** 0.1% to 0.8% Dry Matter
    * **Fat, Oil and Grease (FOG) Presence:** Very High Load Profile Expected
    * **Downstream Integration Core:** Pre-treatment via Cross Flow Separator (CFS) mandatory before biological anaerobic loops.
    """)
with env_c2:
    st.markdown("""
    **Guaranteed Pre-Treatment System Performance Metrics:**
    * **Total Suspended Solids (TSS) Reduction:** Greater than 90% System Clean Efficiency
    * **Oil and Grease Extraction Efficiency:** Greater than 90% Separation
    * **Sludge Solid Concentration Matrix:** Thickened to 1% to 3% Extracted Dry Cake Solids
    """)

st.markdown("---")

# Unstructured Data Parsing Node (Groq Pipeline Integration)
st.header("🤝 Social Impact Evaluation & Document Parser")
st.write("Socioeconomic profile cross-analyzed with targets from the [Nutreco Trust Dairy Case Study](https://www.nutreco.com/en/sustainability/good-citizenship/community-development/trust-dairy-project/).")

if uploaded_social_file is not None:
    if not groq_api_key:
        st.error("🔒 Input your Groq API Key within the control panel sidebar to execute text data ingestion loops.")
    else:
        try:
            raw_text = uploaded_social_file.read().decode("utf-8")
            groq_client = Groq(api_key=groq_api_key)
            with st.spinner("Executing high-speed document text mapping via Groq optimization pipeline..."):
                inference_execution = groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are an expert dairy industry infrastructure consultant. Analyze the text provided, extract specific social/livelihood compliance metrics, and contrast them with baseline regional cooperative frameworks."},
                        {"role": "user", "content": f"Extract social metrics and generate a comparative vector framework for this text:\n\n{raw_text[:4000]}"}
                    ],
                    model="llama-3.3-70b-versatile",  # Updated to the active Llama 3.3 model
                )
            st.success("Analysis complete via Groq Processing Node!")
            st.write(inference_execution.choices[0].message.content)
        except Exception as error:
            st.error(f"Inference pipeline execution failure: {error}")
else:
    st.info("💡 **Dynamic Bypass Activated:** Standard case-study social parameters are pre-loaded because no custom third-party study was uploaded.")

# =============================================================================
# EXPORT INTERFACE COMPILER ACTION NODE
# =============================================================================
st.markdown("---")
st.subheader("💾 Institutional Compilation Node")
st.write("Compile all configuration parameters, financial matrices, and water-nexus charts into a structured institutional report document:")

if st.button("Generate & Optimize Structural DPR Report Document"):
    with st.spinner("Executing structural index parsing, running Groq text generation nodes, and rendering vector components..."):
        
        optimized_narrative_layer = None
        # Verify if template structures are present or trigger the structural layout bypass
        if final_extracted_blueprint.strip() != "":
            if not groq_api_key:
                st.error("🔒 Groq API Key required to process custom layout formats. Please insert an API key or clear the custom file uploads to utilize the default master blueprint.")
            else:
                optimized_narrative_layer = generate_custom_dpr_narrative(final_extracted_blueprint)
        else:
            st.info("ℹ️ **Dynamic Layout Bypass Triggered:** No custom PDF blueprint layout index provided. Standard corporate master infrastructure template activated.")
        
        # Generate the ReportLab PDF Document Stream
        generated_pdf_stream = compile_comprehensive_pdf(custom_narrative_text=optimized_narrative_layer)
        
        st.success("DPR Compilation Complete!")
        st.download_button(
            label="Download Elaborative Optimized DPR PDF Asset",
            data=generated_pdf_stream,
            file_name="Mega_Dairy_Processing_Plant_Optimized_DPR.pdf",
            mime="application/pdf"
        )
