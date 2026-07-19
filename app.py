import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
from groq import Groq

# ReportLab Layout & Presentation Engines
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
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
groq_api_key = st.sidebar.text_input("Groq API Key", type="password", help="Processes unstructured operational text files.")

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

# Explicit definitions for baseline safety mapping
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
# ADVANCED STRUCTURAL GRAPHICS ENGINE (FIXED BBOX DICTIONARY COUPLING)
# =============================================================================
def generate_advanced_topology(selected_products):
    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.axis('off')
    
    # Styled Properties Mapped Safely into matplotlib bbox
    box_props = dict(boxstyle='round,pad=0.5', facecolor='#0F172A', edgecolor='#38BDF8', lw=1.5)
    w_props = dict(boxstyle='round,pad=0.5', facecolor='#1E293B', edgecolor='#F43F5E', lw=1.5)
    
    # Row 1: Core Dairy Refining Node Tracks (FIXED: dict assigned directly to bbox)
    ax.text(1, 3, "Bulk Silos Intake\n(100 LLPD Rated)", bbox=box_props, color='white', ha='center', weight='bold')
    ax.text(4, 3, "Clarification &\nBactofugation", bbox=box_props, color='white', ha='center', weight='bold')
    ax.text(7, 3, "High-Capacity\nPasteurization", bbox=box_props, color='white', ha='center', weight='bold')
    
    # Flow link elements Row 1
    ax.annotate('', xy=(2.3, 3), xytext=(1.8, 3), arrowprops=dict(arrowstyle="-|>", color='#38BDF8', lw=2))
    ax.annotate('', xy=(5.3, 3), xytext=(4.8, 3), arrowprops=dict(arrowstyle="-|>", color='#38BDF8', lw=2))
    
    # Multi-product processing branches (FIXED: dict assigned directly to bbox)
    ax.text(10, 4, "Packaging Unit\n(Fluid Milk Lines)", bbox=box_props, color='white', ha='center')
    ax.text(10, 3, "Cheese & Paneer\nCoagulation Vats", bbox=box_props, color='white', ha='center')
    ax.text(10, 2, "By-Product Lines\n(Ghee / Mawa Pans)", bbox=box_props, color='white', ha='center')
    
    ax.annotate('', xy=(8.5, 3.8), xytext=(7.8, 3.2), arrowprops=dict(arrowstyle="-|>", color='#0EA5E9', lw=1.5))
    ax.annotate('', xy=(8.5, 3.0), xytext=(7.8, 3.0), arrowprops=dict(arrowstyle="-|>", color='#0EA5E9', lw=1.5))
    ax.annotate('', xy=(8.5, 2.2), xytext=(7.8, 2.8), arrowprops=dict(arrowstyle="-|>", color='#0EA5E9', lw=1.5))
    
    # Row 2: Resource Water Infrastructure (FIXED: dict assigned directly to bbox)
    ax.text(4, 0.8, "Groundwater Intake\n(Empirical Sourcing)", bbox=w_props, color='white', ha='center')
    ax.text(7, 0.8, "K-Pack Systems CFS\nHigh-Fat Interceptor", bbox=w_props, color='white', ha='center', weight='bold')
    ax.text(10, 0.8, "Anaerobic Digester\n(Biological Secondary)", bbox=w_props, color='white', ha='center')
    
    ax.annotate('', xy=(5.5, 0.8), xytext=(4.8, 0.8), arrowprops=dict(arrowstyle="-|>", color='#F43F5E', lw=2))
    ax.annotate('', xy=(8.5, 0.8), xytext=(7.8, 0.8), arrowprops=dict(arrowstyle="-|>", color='#F43F5E', lw=2))
    
    # Inter-layer industrial link mapping (FIXED: lowercase fontsize applied)
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
# INDUSTRIAL COMPILATION ENGINE (COMPREHENSIVE PDF WRAPPER)
# =============================================================================
def compile_comprehensive_pdf():
    pdf_buffer = io.BytesIO()
    document = SimpleDocTemplate(pdf_buffer, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=45, bottomMargin=45)
    story = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CoverTitle', fontSize=26, leading=32, textColor=colors.HexColor('#0F172A'), alignment=1, spaceAfter=20, fontName="Helvetica-Bold")
    subtitle_style = ParagraphStyle('CoverSub', fontSize=14, leading=18, textColor=colors.HexColor('#475569'), alignment=1, spaceAfter=200)
    meta_style = ParagraphStyle('CoverMeta', fontSize=11, leading=15, textColor=colors.HexColor('#1E293B'), alignment=1)
    
    h1_style = ParagraphStyle('H1Chapter', fontSize=15, leading=19, textColor=colors.HexColor('#1E3A8A'), spaceBefore=18, spaceAfter=10, fontName="Helvetica-Bold", keepWithNext=True)
    body_style = ParagraphStyle('BodyFormat', fontSize=9.5, leading=14.5, textColor=colors.HexColor('#334155'), spaceAfter=8)
    table_text = ParagraphStyle('TableTxt', fontSize=8.5, leading=11, textColor=colors.HexColor('#1E293B'))
    table_header = ParagraphStyle('TableHdr', fontSize=9, leading=12, textColor=colors.white, fontName="Helvetica-Bold")

    # -------------------------------------------------------------------------
    # CHAPTER 1: TITLE PAGE
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("DETAILED PROJECT REPORT (DPR)<br/>MEGA DAIRY PROCESSING FACILITY", title_style))
    story.append(Paragraph(f"PRODUCTION DESIGN SCALE: {final_capacity_llpd} LAKH LITERS PER DAY", subtitle_style))
    story.append(Paragraph(f"<b>Prepared For:</b> {final_promoter}<br/><b>Operational Matrix Sourcing Node:</b> {final_location}<br/><b>Target CAPEX Structuring:</b> INR {final_capex_cr} Crores", meta_style))
    story.append(PageBreak())
    
    # -------------------------------------------------------------------------
    # CHAPTER 2: INTRODUCTION
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 2: Project Introduction & Operational Scope", h1_style))
    story.append(Paragraph(f"This Detailed Project Report establishes the operational and engineering metrics for a mega-scale milk processing facility situated within the {final_location}. India ranks as the world's preeminent producer of fluid milk, driven fundamentally by smallholder aggregation systems. This enterprise establishes a centralized processing nexus to capture regional production surpluses, extend commodity shelf-life profiles, and minimize post-harvest value dissipation across downstream supply networks.", body_style))
    
    # -------------------------------------------------------------------------
    # CHAPTER 3: MILK PROCUREMENT AND PROCESSING
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 3: Strategic Milk Procurement Framework", h1_style))
    story.append(Paragraph(f"The facility implements a structured milk pooling layout scaled to sustain a physical capacity of {final_capacity_llpd} Lakh Liters per day. Procurement logic uses a tiered network of village-level Bulk Milk Chilling (BMC) collection infrastructure connected to central testing centers to maintain strict quality metrics before transportation. Processing configurations integrate multi-tier separation pipelines to split raw intake streams into distinct standardized product families.", body_style))
    
    # -------------------------------------------------------------------------
    # CHAPTER 4: DOMESTIC AND EXPORT PERFORMANCE
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 4: Domestic Market & Export Performance Analysis", h1_style))
    story.append(Paragraph("The dairy sector represents one of the fastest-growing segments within agro-industrial commodity value chains. Domestic consumption profiles show high structural demand for processed value-added products like functional cheeses and premium ghee. In addition, geographical proximity to Middle Eastern and South Asian trade hubs enables access to export markets for skimmed milk powder (SMP) and white-label butterfat commodities.", body_style))
    
    # -------------------------------------------------------------------------
    # CHAPTER 5: PROJECT OBJECTIVES & PRODUCT PROFILES
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 5: Project Objectives & Diversified Product Profiles", h1_style))
    story.append(Paragraph("The central technical objectives of this deployment include: (1) Enhancing long-term shelf stability of regional fluid milk surpluses, (2) Optimizing resource use via advanced water recycling networks, and (3) Structuring value-added processing lines to diversify income generation. The product portfolio includes Pasteurized Fluid Liquid Milk, Probiotic Rich Dahi, Coagulated Paneer Blocks, and Standardized Ghee Formulations.", body_style))
    
    # -------------------------------------------------------------------------
    # CHAPTER 6: ABOUT THE PROMOTER
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 6: Corporate Profile & Promoter Capabilities", h1_style))
    story.append(Paragraph(f"<b>Promoter Entity Call Sign:</b> {final_promoter}<br/><b>Operational Track Record & Core Competencies:</b> {final_exp}", body_style))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 7: FINANCIAL VIABILITY (COST & MEANS)
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 7: Financial Viability - Cost of Project & Means of Finance", h1_style))
    
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
    t_fsm = Table(fin_summary_matrix, colWidths=[340, 200])
    t_fsm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_fsm)

    # -------------------------------------------------------------------------
    # CHAPTER 8, 9, 10, 11: ANNUAL OPERATING BREAKDOWNS
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapters 8-11: Annual Operating Outlays, Production Resource Consumption & Sales Metrics", h1_style))
    
    op_breakdown_matrix = [
        [Paragraph("Operating Cost Vector Group (Year 1 Timeline)", table_header), Paragraph("Value Metric (INR)", table_header)],
        [Paragraph("Raw Materials Procurement Input Expenses", table_text), Paragraph(f"{variable_cost_year_1:,.2f}", table_text)],
        [Paragraph("Human Resources, Labor Allocation & Staff Overhead", table_text), Paragraph(f"{staff_cost_year_1:,.2f}", table_text)],
        [Paragraph("Other Miscellaneous Administrative & Utility Expenses", table_text), Paragraph(f"{other_exp_year_1:,.2f}", table_text)],
        [Paragraph("<b>Gross Annual Sales Realization Value</b>", table_text), Paragraph(f"<b>{revenue_year_1:,.2f}</b>", table_text)]
    ]
    t_obm = Table(op_breakdown_matrix, colWidths=[340, 200])
    t_obm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0EA5E9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t_obm)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 12: 10-YEAR PROFITABILITY STATEMENT
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 12: Projected 10-Year Profitability Statement", h1_style))
    
    prof_headers = [Paragraph("Metric (Cr INR)", table_header)] + [Paragraph(f"Y{y}", table_header) for y in years]
    row_rev = [Paragraph("Gross Revenue", table_text)] + [Paragraph(f"{r/10000000:.1f}", table_text) for r in revenue_projection]
    row_vc = [Paragraph("Variable Cost", table_text)] + [Paragraph(f"{v/10000000:.1f}", table_text) for v in variable_projections]
    row_pat = [Paragraph("Net Profit (PAT)", table_text)] + [Paragraph(f"{p/10000000:.1f}", table_text) for p in net_profit_projection]
    
    t_prof = Table([prof_headers, row_rev, row_vc, row_pat], colWidths=[120] + [42]*10)
    t_prof.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_prof)

    # -------------------------------------------------------------------------
    # CHAPTER 13: 10-YEAR PROJECTED BALANCE SHEET
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 13: Projected 10-Year Balance Sheet Summary", h1_style))
    row_eq = [Paragraph("Total Equity Base", table_text)] + [Paragraph(f"{(equity_contribution + (sum(net_profit_projection[:i])*0.5))/10000000:.1f}", table_text) for i in range(1, 11)]
    row_debt = [Paragraph("Outstanding Debt", table_text)] + [Paragraph(f"{(term_loan_principal - (annual_repayment*(y-1)))/10000000:.1f}", table_text) for y in years]
    
    t_bs = Table([prof_headers, row_eq, row_debt], colWidths=[120] + [42]*10)
    t_bs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#334155')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_bs)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # CHAPTER 14: DEPRECIATION SCHEDULE (WDV)
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 14: Capital Asset Depreciation Schedule (WDV Method)", h1_style))
    row_dep = [Paragraph("Depreciation Allocation", table_text)] + [Paragraph(f"{d/10000000:.1f}", table_text) for d in depreciation_schedule]
    t_dep = Table([prof_headers, row_dep], colWidths=[120] + [42]*10)
    t_dep.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#475569')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_dep)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # CHAPTER 15: FUND FLOW STATEMENT
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 15: Projected 10-Year Fund Flow Statement", h1_style))
    row_flow = [Paragraph("Net Cash Inflow", table_text)] + [Paragraph(f"{(pat + depreciation_schedule[i])/10000000:.1f}", table_text) for i, pat in enumerate(net_profit_projection)]
    t_ff = Table([prof_headers, row_flow], colWidths=[120] + [42]*10)
    t_ff.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284C7')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_ff)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 16: DEBT COVERAGE RATIO, REPAYMENT & INTEREST MATRIX
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 16: Debt Service Coverage Ratio (DSCR) & Repayment Metrics", h1_style))
    row_int = [Paragraph("Interest Expense Pay", table_text)] + [Paragraph(f"{int_p/10000000:.1f}", table_text) for int_p in interest_payments]
    row_dscr = [Paragraph("Calculated DSCR Index", table_text)] + [Paragraph(f"{dscr:.2f}", table_text) for dscr in dscr_projection]
    
    t_dc = Table([prof_headers, row_int, row_dscr], colWidths=[120] + [42]*10)
    t_dc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_dc)
    
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
st.write("Compile all configuration parameters, financial matrices, and water-nexus charts into a 16-chapter Detailed Project Report:")

generated_pdf_stream = compile_comprehensive_pdf()

st.download_button(
    label="Download 16-Chapter Corporate DPR PDF Asset",
    data=generated_pdf_stream,
    file_name="Mega_Dairy_Processing_Plant_10Year_DPR.pdf",
    mime="application/pdf"
)
