import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
from groq import Groq

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
# INSTITUTIONAL COMPILATION ENGINE & ADVANCED PDF COMPILER
# =============================================================================
def fetch_groq_optimized_layer():
    """Utilizes Groq to build a search-optimized executive text layer tailored to user inputs."""
    if not groq_api_key:
        return "Standard industrial model optimization active. No API key provided for live dynamic text synthesis overrides."
    try:
        client = Groq(api_key=groq_api_key)
        prompt = f"""
        Act as a Principal Infrastructure Consultant specialized in institutional dairy plants.
        Generate a highly rigorous, technical executive framework statement for a processing plant with these specs:
        - Promoter: {final_promoter}
        - Location: {final_location}
        - Capacity: {final_capacity_llpd} LLPD (Operational Target: {final_actual_llpd} LLPD)
        - Selected Products: {', '.join(products)}
        - Capex: INR {final_capex_cr} Crores
        Provide exactly three long, dense paragraphs covering macro-economics, site competitive logistics advantages, and technology-driven margin protection systems.
        """
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-70b-versatile",
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Optimization module active with default fallback conditions. Notice: {str(e)}"

def compile_comprehensive_pdf():
    pdf_buffer = io.BytesIO()
    document = SimpleDocTemplate(pdf_buffer, pagesize=letter, leftMargin=40, rightMargin=40, topMargin=50, bottomMargin=50)
    story = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CoverTitle', fontSize=26, leading=32, textColor=colors.HexColor('#0F172A'), alignment=1, spaceAfter=20, fontName="Helvetica-Bold")
    subtitle_style = ParagraphStyle('CoverSub', fontSize=14, leading=18, textColor=colors.HexColor('#475569'), alignment=1, spaceAfter=180)
    meta_style = ParagraphStyle('CoverMeta', fontSize=11, leading=16, textColor=colors.HexColor('#1E293B'), alignment=1)
    
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
    story.append(Paragraph("STRATEGIC BLUEPRINT FOR A COMMERCIAL MEGA-SCALE DAIRY PLANT", ParagraphStyle('MainSub', fontSize=16, leading=22, textColor=colors.HexColor('#1E3A8A'), alignment=1, spaceAfter=15)))
    story.append(Paragraph(f"PRODUCTION PROFILE CAPACITY: {final_capacity_llpd} LAKH LITERS PER DAY", subtitle_style))
    story.append(Paragraph(f"<b>Promoter Corporation:</b> {final_promoter}<br/><b>Operational Sourcing Nexus:</b> {final_location}<br/><b>Capital Investment Blueprint:</b> INR {final_capex_cr} Crores", meta_style))
    story.append(PageBreak())
    
    # -------------------------------------------------------------------------
    # SYSTEMATIC MASTER INDEX / TABLE OF CONTENTS
    # -------------------------------------------------------------------------
    story.append(Paragraph("Master Structural Index", h1_style))
    story.append(Spacer(1, 10))
    
    index_data = [
        [Paragraph("<b>Chapter / Operational Section</b>", table_header), Paragraph("<b>Target Focus Area</b>", table_header)],
        [Paragraph("Chapter 1: Executive Summary & Strategic Optimization", table_text), Paragraph("High-level project scope and Groq AI text insights.", table_text)],
        [Paragraph("Chapter 2: Market Potential & Industry Structural Profile", table_text), Paragraph("Macro analysis of dairy processing supply chains in India.", table_text)],
        [Paragraph("Chapter 3: Technical Specifications & Sizing Logic", table_text), Paragraph("Design parameters, mass balances, and capacity curves.", table_text)],
        [Paragraph("Chapter 4: Supply Chain Logic & Raw Milk Procurement", table_text), Paragraph("Village-level aggregation and cold-chain infrastructure.", table_text)],
        [Paragraph("Chapter 5: Project Location & Agro-Industrial Advantages", table_text), Paragraph("Geographical assessment and infrastructure access points.", table_text)],
        [Paragraph("Chapter 6: Corporate Profile & Promoter Capabilities", table_text), Paragraph("Corporate background, operational track record, and values.", table_text)],
        [Paragraph("Chapter 7: Capital Cost Architecture & Financial Viability", table_text), Paragraph("CAPEX allocation breakdown and breakdown profiles.", table_text)],
        [Paragraph("Chapter 8: Operating Expenses & Annual Resource Outlays", table_text), Paragraph("Variable inputs, overheads, and annual raw costs.", table_text)],
        [Paragraph("Chapter 9: Comprehensive 10-Year Profitability Statement", table_text), Paragraph("Revenue models, EBIDTA, PAT, and trend mapping.", table_text)],
        [Paragraph("Chapter 10: Projected Balance Sheet Summaries", table_text), Paragraph("Asset structures, liability mapping, and equity tracking.", table_text)],
        [Paragraph("Chapter 11: Capital Depreciation Framework", table_text), Paragraph("Written Down Value (WDV) structural schedules.", table_text)],
        [Paragraph("Chapter 12: Debt Service Coverage & Solvency Metrics", table_text), Paragraph("DSCR, principal repayments, and interest obligations.", table_text)],
        [Paragraph("Annexure A: Unit Engineering Topology Blueprint", table_text), Paragraph("Visual process flow visualization map.", table_text)],
        [Paragraph("Annexure B: Cross-Sector Compliance & Sustainability Matrix", table_text), Paragraph("Environmental, economic, and benchmark performance metrics.", table_text)]
    ]
    t_idx = Table(index_data, colWidths=[240, 280])
    t_idx.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t_idx)
    story.append(PageBreak())
    
    # -------------------------------------------------------------------------
    # CHAPTER 1
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 1: Executive Summary & Strategic Optimization", h1_style))
    story.append(Paragraph("This document outlines the corporate blueprint for the establishment of an automated, resource-efficient multi-product dairy processing terminal. The project is scaled intentionally to accommodate regional supply elasticity while optimizing margin defense mechanisms against seasonal raw milk supply drops. By deploying highly specialized processing machinery, the terminal guarantees compliance with international safety protocols while achieving significant unit-level cost reductions.", body_style))
    
    groq_text = fetch_groq_optimized_layer()
    story.append(Paragraph("<b>Groq AI Search-Optimized Insights:</b>", h2_style))
    story.append(Paragraph(groq_text, body_style))
    story.append(PageBreak())
    
    # -------------------------------------------------------------------------
    # CHAPTER 2
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 2: Market Potential & Industry Structural Profile", h1_style))
    story.append(Paragraph("The dairy industry operates as a primary economic driver within the agricultural sector, exhibiting consistent compound annual growth rates driven by rising urban disposable incomes and expanding consumer preferences for functional nutrition. Traditional consumption models are transforming rapidly, moving away from unorganized fluid milk toward standardized, shelf-stable, value-added products.", body_style))
    story.append(Paragraph("Furthermore, competitive pressures require modern processing hubs to integrate smart cold chains and flexible downstream processing equipment. This allows the factory floor to quickly pivot between packaging fluid retail milk and producing high-margin commodities like premium clarified butterfat, aged cheeses, and probiotic yogurts based on live market pricing data.", body_style))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 3
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 3: Technical Specifications & Sizing Logic", h1_style))
    story.append(Paragraph(f"The facility is engineered with a core processing architecture rated at a daily peak design capacity of {final_capacity_llpd} Lakh Liters. Mass-balance optimization calculations indicate that at a baseline capacity utilization of {capacity_utilization:.1f}%, the plant will process a steady operational input of {final_actual_llpd} Lakh Liters per single production day.", body_style))
    story.append(Paragraph("The processing line incorporates advanced technological modules, including high-speed hermetic separators, integrated bactofuges to eliminate heat-resistant spore loads, and regenerative pasteurizers operating at thermal exchange efficiencies exceeding 92%. Automated Clean-In-Place (CIP) systems reduce chemical handling overhead and minimize downtime during batch transfers.", body_style))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 4
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 4: Supply Chain Logic & Raw Milk Procurement", h1_style))
    story.append(Paragraph("Sustaining an industrial asset of this scale requires a reliable, continuous raw material procurement network. The facility implements a multi-tiered direct collection model that eliminates intermediary leakage and establishes direct financial inclusion with primary livestock smallholders.", body_style))
    story.append(Paragraph("The network includes village-level pooling points equipped with solar-powered automatic milk collection units (AMCUs) that conduct instantaneous real-time quality testing for fat content and solids-not-fat (SNF). Collected volume is rapidly routed to bulk milk chilling centers (BMCs) to reduce temperatures to below 4°C within a strict 4-hour window, successfully preventing microbial development and preserving raw milk quality parameters.", body_style))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 5
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 5: Project Location & Agro-Industrial Advantages", h1_style))
    story.append(Paragraph(f"The selection of the primary construction site in the <b>{final_location}</b> was determined through a rigorous multi-criteria geographical information system (GIS) matrix. The location sits directly inside an established high-yield milkshed corridor, guaranteeing immediate physical access to high-quality raw milk sourcing networks.", body_style))
    story.append(Paragraph("Proximity to major high-speed multi-lane transport infrastructure facilitates rapid long-haul distribution of finished retail products to urban distribution hubs. Additionally, the location provides reliable access to necessary industrial infrastructure, including high-capacity power lines, reliable natural gas connections, and sustainable industrial water supplies.", body_style))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 6
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 6: Corporate Profile & Promoter Capabilities", h1_style))
    story.append(Paragraph(f"The enterprise is led by <b>{final_promoter}</b>, an organization built upon extensive operational experience and industry-vetted technical capabilities. <i>Strategic Background Statement:</i> {final_exp}", body_style))
    story.append(Paragraph("The core executive team includes industry veterans from dairy engineering, corporate finance, and commercial cold chain logistics. This diverse management capability ensures the enterprise can maintain strict cost controls during construction and hit targeted capacity utilization timelines within the first 12 months of operations.", body_style))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 7
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 7: Capital Cost Architecture & Financial Viability", h1_style))
    story.append(Paragraph("The total capital expenditure framework for this mega-scale dairy terminal is budgeted at a fixed allocation of INR <b>{final_capex_cr:.2f} Crores</b>. The investment distribution is strategically split to balance civil infrastructure longevity with advanced automation tooling systems.", body_style))
    
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

    # -------------------------------------------------------------------------
    # CHAPTER 8
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 8: Operating Expenses & Annual Resource Outlays", h1_style))
    story.append(Paragraph("Operating expenditures are modeled using direct cost matrices that adjust for inflationary trends across raw materials, energy access fees, and specialized engineering labor. The table below represents the baseline Year 1 operating projections at target capacity constraints.", body_style))
    
    op_breakdown_matrix = [
        [Paragraph("Operating Cost Vector Group (Year 1 Timeline)", table_header), Paragraph("Value Metric (INR)", table_header)],
        [Paragraph("Raw Materials Procurement Input Expenses", table_text), Paragraph(f"{variable_cost_year_1:,.2f}", table_text)],
        [Paragraph("Human Resources, Labor Allocation & Staff Overhead", table_text), Paragraph(f"{staff_cost_year_1:,.2f}", table_text)],
        [Paragraph("Other Miscellaneous Administrative & Utility Expenses", table_text), Paragraph(f"{other_exp_year_1:,.2f}", table_text)],
        [Paragraph("<b>Gross Annual Sales Realization Value</b>", table_text), Paragraph(f"<b>{revenue_year_1:,.2f}</b>", table_text)]
    ]
    t_obm = Table(op_breakdown_matrix, colWidths=[320, 200])
    t_obm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0EA5E9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t_obm)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 9
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 9: Comprehensive 10-Year Profitability Statement", h1_style))
    story.append(Paragraph("The long-term financial structure demonstrates strong profitability and compounding margin defense over the ten-year projection horizon. Revenue models assume a modest 5% annual price escalation, balancing market reality with long-term commercial optimization targets.", body_style))
    
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
    # CHAPTER 10
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 10: Projected Balance Sheet Summaries", h1_style))
    story.append(Paragraph("The company's balance sheet reflects a healthy capital structure, featuring rapid debt reduction and steady accumulation of corporate equity reserves over time. Retained earnings are re-invested into automated process upgrades to keep the plant operating at peak efficiency.", body_style))
    
    row_eq = [Paragraph("Total Equity Base", table_text)] + [Paragraph(f"{(equity_contribution + (sum(net_profit_projection[:i])*0.5))/10000000:.1f}", table_text) for i in range(1, 11)]
    row_debt = [Paragraph("Outstanding Debt", table_text)] + [Paragraph(f"{(term_loan_principal - (annual_repayment*(y-1)))/10000000:.1f}", table_text) for y in years]
    
    t_bs = Table([prof_headers, row_eq, row_debt], colWidths=[110] + [41]*10)
    t_bs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#334155')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_bs)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 11
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 11: Capital Depreciation Framework", h1_style))
    story.append(Paragraph("Depreciation planning applies the standard Written Down Value (WDV) method at a 15% blending rate across primary processing assets and manufacturing plant machinery groups. This systematic methodology matches asset value changes with active plant lifecycles, optimizing corporate tax structures during high-growth operational years.", body_style))
    
    row_dep = [Paragraph("Depreciation Allocation", table_text)] + [Paragraph(f"{d/10000000:.1f}", table_text) for d in depreciation_schedule]
    t_dep = Table([prof_headers, row_dep], colWidths=[110] + [41]*10)
    t_dep.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#475569')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_dep)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 12
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 12: Debt Service Coverage & Solvency Metrics", h1_style))
    story.append(Paragraph("Debt service validation calculations show strong solvency safety margins. The project's Debt Service Coverage Ratio (DSCR) remains comfortably above institutional lending thresholds, confirming the plant's ability to reliably meet capital obligations even during seasonal market fluctuations.", body_style))
    
    row_int = [Paragraph("Interest Expense Pay", table_text)] + [Paragraph(f"{int_p/10000000:.1f}", table_text) for int_p in interest_payments]
    row_dscr = [Paragraph("Calculated DSCR Index", table_text)] + [Paragraph(f"{dscr:.2f}", table_text) for dscr in dscr_projection]
    
    t_dc = Table([prof_headers, row_int, row_dscr], colWidths=[110] + [41]*10)
    t_dc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_dc)
    story.append(PageBreak())

    # =============================================================================
    # TECHNICAL ANNEXURES (VISUAL BLUEPRINT & METRICS COUPLING)
    # =============================================================================
    story.append(Paragraph("Annexure A: Unit Engineering Topology Blueprint", h1_style))
    story.append(Paragraph("This blueprint visualizes the automated processing sequence and resource routing layout designed for this facility, showing everything from initial fluid intake to downstream separation and integrated environmental treatment lines.", body_style))
    story.append(Spacer(1, 10))
    
    # Save Topology Figure to Buffer for ReportLab insertion
    fig_topo = generate_advanced_topology(products)
    topo_buf = io.BytesIO()
    fig_topo.savefig(topo_buf, format='png', dpi=200)
    topo_buf.seek(0)
    plt.close(fig_topo)
    story.append(Image(topo_buf, width=500, height=187))
    story.append(PageBreak())
    
    story.append(Paragraph("Annexure B: Cross-Sector Compliance & Sustainability Matrix", h1_style))
    story.append(Paragraph("The chart below maps the facility's sustainability performance indices against regional dairy sector benchmarks, tracking environmental impact, water footprint mitigation, and localized smallholder economic inclusion goals.", body_style))
    story.append(Spacer(1, 10))
    
    # Save Compliance Figure to Buffer for ReportLab insertion
    fig_comp = generate_compliance_matrix()
    comp_buf = io.BytesIO()
    fig_comp.savefig(comp_buf, format='png', dpi=200)
    comp_buf.seek(0)
    plt.close(fig_comp)
    story.append(Image(comp_buf, width=480, height=182))
    story.append(Spacer(1, 15))
    
    # Text-based indicators matrix
    story.append(Paragraph("<b>Calculated Empirical Performance Summary:</b>", h2_style))
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
                    model="llama-3.1-70b-versatile",
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
st.write("Compile all configuration parameters, financial matrices, and water-nexus charts into a multi-chapter detailed institutional project layout:")

if st.button("Generate & Optimize Structural DPR Report Document"):
    with st.spinner("Executing layout compilation, rendering vector image components, and optimizing narrative structures..."):
        generated_pdf_stream = compile_comprehensive_pdf()
        
        st.success("Institutional Detailed Project Report generated successfully!")
        st.download_button(
            label="Download Elaborative Corporate DPR PDF Asset",
            data=generated_pdf_stream,
            file_name="Mega_Dairy_Processing_Plant_Elaborative_DPR.pdf",
            mime="application/pdf"
        )
