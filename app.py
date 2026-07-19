import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
from groq import Groq

# ReportLab Libraries for PDF Generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- Page & Style Configuration ---
st.set_page_config(page_title="Dairy-DPR Architect Pro", layout="wide", page_icon="🥛")
sns.set_theme(style="whitegrid")

st.title("🥛 Dairy-DPR Architect Pro")
st.subheader("Automated Industrial Blueprint, Financial DPR & Sustainability Engine")
st.markdown("---")

# =============================================================================
# SIDEBAR: USER INPUTS / SYSTEM DEFAULTS
# =============================================================================
st.sidebar.header("🔑 Optimization Infrastructure")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password", help="Processes unstructured environmental/social studies.")

st.sidebar.header("1. Plant Spatial Profiles")
location = st.sidebar.text_input("Proposed Location (Defaults if blank)", "Punjab, India")
user_capex = st.sidebar.number_input("Allocated CAPEX Budget (INR)", min_value=0, value=2500000, step=50000)
design_capacity = st.sidebar.number_input("Design Plant Capacity (LPD)", min_value=1000, value=10000, step=1000)
actual_capacity = st.sidebar.slider("Operational Processing Volume (LPD)", min_value=500, max_value=int(design_capacity if design_capacity > 500 else 10000), value=int(design_capacity * 0.85 if design_capacity > 0 else 8500))

st.sidebar.header("2. Product Strategy Matrix")
products = []
if st.sidebar.checkbox("Liquid Pasteurized Milk", value=True): products.append("Milk")
if st.sidebar.checkbox("Ghee", value=True): products.append("Ghee")
if st.sidebar.checkbox("Dahi / Yogurt"): products.append("Dahi")
if st.sidebar.checkbox("Mawa / Khoa", value=True): products.append("Mawa")
if st.sidebar.checkbox("Paneer / Cheese"): products.append("Paneer")

st.sidebar.header("3. Water-Energy Nexus Assets")
annual_milk_kg = st.sidebar.number_input("Annual Raw Milk Throughput (kg)", min_value=0, value=3000000)
annual_water_l = st.sidebar.number_input("Annual Groundwater Abstraction (Liters)", min_value=0, value=9930000)
annual_electricity_kwh = st.sidebar.number_input("Annual Grid Energy Consumption (kWh)", min_value=0, value=300000)

st.sidebar.header("4. External Compliance Node")
uploaded_social_file = st.sidebar.file_uploader("Upload Third-Party Baseline Studies", type=["csv", "txt"])

# =============================================================================
# AUTOMATED BYPASS & FAIL-SAFE LOGIC ENGINE
# =============================================================================
# Fallback constraints if user resets inputs to 0
final_milk_kg = annual_milk_kg if annual_milk_kg > 0 else 3000000
final_water_l = annual_water_l if annual_water_l > 0 else 9930000
final_elec_kwh = annual_electricity_kwh if annual_electricity_kwh > 0 else 300000
final_capex = user_capex if user_capex > 0 else 2500000

DWU_BENCHMARK = 3.31
TWF_BENCHMARK = 9.0

# Base scaling logic from MANAGE templates
baseline_capacity = 20000
base_fixed_assets = 2000000
scaling_factor = design_capacity / baseline_capacity if design_capacity > 0 else 0.5
calculated_required_capex = base_fixed_assets * scaling_factor

# Hydrology metrics processing
capacity_utilization = (actual_capacity / design_capacity) * 100 if design_capacity > 0 else 85.0
user_dwu = final_water_l / final_milk_kg
indirect_wf = (final_elec_kwh * (5.69 / 0.1)) / final_milk_kg 
user_twf = user_dwu + (indirect_wf * 0.1) 
daily_effluent_lpd = (final_water_l / 365) * 0.74

metric_passbook = {
    'capex_ratio': final_capex / calculated_required_capex if calculated_required_capex > 0 else 1.0,
    'dwu_variance': user_dwu - DWU_BENCHMARK,
    'twf_variance': user_twf - TWF_BENCHMARK
}

# =============================================================================
# VISUALIZATION ENGINE FUNCTIONS
# =============================================================================
def generate_process_diagram(selected_products):
    fig, ax = plt.subplots(figsize=(10, 2.5))
    ax.axis('off')
    stages = ["Raw Milk\nIntake", "Testing &\nChilling", "Pasteurization\n& Separation"]
    if "Ghee" in selected_products or "Mawa" in selected_products:
        stages.append("Thermal Cooking\n(Ghee/Mawa)")
    if "Dahi" in selected_products or "Paneer" in selected_products:
        stages.append("Fermentation/\nCoagulation")
    stages.append("Packaging &\nCold Chain")
    
    for i, stage in enumerate(stages):
        ax.text(i * 2.2, 0.5, stage, ha='center', va='center', color='white', weight='bold',
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#1E3A8A', edgecolor='#0284C7', lw=1.5))
        if i < len(stages) - 1:
            ax.annotate('', xy=((i + 1) * 2.2 - 0.5, 0.5), xytext=(i * 2.2 + 0.5, 0.5),
                        arrowprops=dict(arrowstyle="-|>", color='#0EA5E9', lw=2.5, mutation_scale=15))
    ax.set_xlim(-1, len(stages) * 2.2 - 1.2)
    ax.set_ylim(0, 1)
    return fig

def generate_benchmark_chart(user_metrics):
    categories = ['Economic Scale\n(CAPEX Match)', 'Direct Water\n(DWU Efficiency)', 'Total Footprint\n(TWF Nexus)', 'Social Target\n(Smallholders)']
    benchmark_baseline = [1.0, 1.0, 1.0, 1.0] 
    user_scores = [
        user_metrics['capex_ratio'],
        max(0.1, 1.0 - (user_metrics['dwu_variance'] / 3.31)),
        max(0.1, 1.0 - (user_metrics['twf_variance'] / 9.0)),
        1.10 
    ]
    x = np.arange(len(categories))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(x - width/2, benchmark_baseline, width, label='Case Study Standards', color='#94A3B8')
    ax.bar(x + width/2, user_scores, width, label='Your Proposed Enterprise', color='#0284C7')
    ax.set_ylabel('Performance Vector Ratio')
    ax.set_title('Strategic Alignment Matrix (Economic, Social, & Environmental Check)')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(loc='upper right')
    ax.axhline(1.0, color='#EF4444', linestyle='--', alpha=0.7)
    plt.tight_layout()
    return fig

# =============================================================================
# PDF GENERATION ENGINE
# =============================================================================
def build_pdf_report():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#1E3A8A'), spaceAfter=15)
    section_style = ParagraphStyle('SecTitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#0284C7'), spaceBefore=12, spaceAfter=8)
    body_style = ParagraphStyle('BodyText', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=6)
    
    # Document Header
    story.append(Paragraph("DETAILED PROJECT REPORT (DPR): DAIRY PROCESSING PLANT", title_style))
    story.append(Paragraph(f"<b>Location of Enterprise:</b> {location}", body_style))
    story.append(Paragraph(f"<b>Target Processing Capability:</b> {design_capacity:,} Liters Per Day (LPD)", body_style))
    story.append(Spacer(1, 10))
    
    # Section 1: Financial Assessment
    story.append(Paragraph("1. Technical & Financial Feasibility Footprint", section_style))
    story.append(Paragraph(f"Analysis scaled using national infrastructure allocation constants. Minimum required installation cost for a processing plant with a capacity of {design_capacity:,} LPD is estimated at <b>INR {calculated_required_capex:,.2f}</b>.", body_style))
    
    fin_data = [
        ['Financial Parameter Description', 'Value Matrix'],
        ['Target Allocated CAPEX Investment', f"INR {final_capex:,.2f}"],
        ['Estimated Project Machinery Footprint', f"INR {calculated_required_capex:,.2f}"],
        ['Capacity Utilization Index', f"{capacity_utilization:.2f}%"]
    ]
    t_fin = Table(fin_data, colWidths=[300, 200])
    t_fin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey)
    ]))
    story.append(t_fin)
    story.append(Spacer(1, 15))
    
    # Section 2: Water Footprint Engine
    story.append(Paragraph("2. Environmental Water Intensity & Hydrology Profile", section_style))
    story.append(Paragraph("Evaluated against data from the empirical <i>Water Footprints of Dairy Milk Processing Industry Case Study</i>.", body_style))
    
    water_data = [
        ['Water Footprint Metric Identifier', 'Plant Footprint Intensity', 'Empirical Target Benchmark'],
        ['Direct Water Use (DWU)', f"{user_dwu:.2f} L/kg", f"{DWU_BENCHMARK} L/kg"],
        ['Total Water Footprint (TWF)', f"{user_twf:.2f} L/kg", f"{TWF_BENCHMARK} L/kg"],
        ['Emitted Hydrology Volumetric Output', f"{daily_effluent_lpd:,.2f} LPD", '74% of Direct Draw Input']
    ]
    t_wtr = Table(water_data, colWidths=[220, 140, 140])
    t_wtr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (2,0), colors.HexColor('#0EA5E9')),
        ('TEXTCOLOR', (0,0), (2,0), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F1F5F9')]),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_wtr)
    story.append(Spacer(1, 15))

    # Section 3: K-Pack Wastewater Integration
    story.append(Paragraph("3. Effluent Pre-Treatment Plan (K-Pack Systems Realization)", section_style))
    story.append(Paragraph("High-fat wastewater streams are pre-treated using a custom <b>K-Pack Systems Cross Flow Separator (CFS)</b> system prior to downstream anaerobic digestion to maximize operational uptime.", body_style))
    
    kpack_data = [
        ['Parameter Objective Group', 'Guaranteed Engineering Output Performance'],
        ['Total Suspended Solids (TSS) Eradication', 'Drop Reduction Matrix > 90%'],
        ['Oil & Grease Interception Efficiency', 'Separation Threshold > 90%'],
        ['Fat Extraction Efficiency', 'Removal Performance > 90%'],
        ['Sludge Thickening Concentration', '1% to 3% Extracted Dry Cake Output Solids']
    ]
    t_kp = Table(kpack_data, colWidths=[250, 250])
    t_kp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor('#0284C7')),
        ('TEXTCOLOR', (0,0), (1,0), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_kp)
    story.append(Spacer(1, 15))
    
    # Section 4: Social Benchmarks
    story.append(Paragraph("4. Socioeconomic Alignment & Smallholder Integration", section_style))
    story.append(Paragraph("Evaluated against the core baseline goals of the <i>Nutreco Trust Dairy Project Case Study</i> in India.", body_style))
    
    soc_data = [
        ['Socioeconomic Metric Area', 'Nutreco Reference Target Profile', 'Your Plant Implementation Model'],
        ['Smallholder Integration Pool', 'Prioritizes marginal holdings (~25% pool)', 'Sourced via structured localized collection centers'],
        ['Animal Yield Acceleration', 'Boosts production past 3-4 L/animal/day', 'Targeted yield scaling using advanced feed strategies'],
        ['Traceability Verification', 'Deploys digital Solitrace Systems', 'End-to-end QR code tracking integrated']
    ]
    t_soc = Table(soc_data, colWidths=[150, 175, 175])
    t_soc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (2,0), colors.HexColor('#475569')),
        ('TEXTCOLOR', (0,0), (2,0), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_soc)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# =============================================================================
# MAIN STREAMLIT INTERFACE RENDERING
# =============================================================================
st.header("🏢 Unit Topology Blueprint Layout")
st.write("Dynamic engineering node sequence map optimized for the specified product parameters:")
st.pyplot(generate_process_diagram(products))
st.markdown("---")

u_col1, u_col2 = st.columns(2)

with u_col1:
    st.header("📊 Multi-Variable Compliance Matrix")
    st.pyplot(generate_benchmark_chart(metric_passbook))
    
    st.subheader("Financial Performance Parameters")
    st.metric("Minimum Required Infrastructure Cost", f"₹ {calculated_required_capex:,.2f}")
    if calculated_required_capex > final_capex:
        st.error(f"⚠️ CAPEX Deficit: Plant expansion limits restricted by ₹ {calculated_required_capex - final_capex:,.2f}.")
    else:
        st.success("✅ Financial Compliance Verified.")

with u_col2:
    st.header("💧 Resource & Water Consumption Profile")
    st.write("Unit consumption indicators evaluated against empirical benchmarks from the [Punjab Dairy Case Study](https://www.mdpi.com/2073-4441/16/3/435):")
    
    st.metric(label="Direct Water Use (DWU)", value=f"{user_dwu:.2f} L/kg", 
              delta=f"{metric_passbook['dwu_variance']:.2f} L/kg vs Case Study Standard (3.31)", delta_color="inverse")
    st.metric(label="Total Water Footprint (TWF)", value=f"{user_twf:.2f} L/kg", 
              delta=f"{metric_passbook['twf_variance']:.2f} L/kg vs Case Study Standard (9.0)", delta_color="inverse")
    
    if capacity_utilization < 85.0:
        st.warning(f"⚠️ **Capacity Utilization Warning ({capacity_utilization:.1f}%):** Sub-optimal operations increase per-unit energy footprint overheads.")

st.markdown("---")

# Environmental Pre-treatment (K-Pack Systems CFS Alignment)
st.header("⚙️ High-Fat Effluent Control (K-Pack Systems CFS Parameters)")
st.write(f"Pre-treatment engineering scale targets computed for an estimated volume of **{daily_effluent_lpd:,.2f} LPD**:")
high_fat_products = [p for p in products if p in ["Ghee", "Mawa", "Paneer"]]
fog_status = "Very High (FOG Interception Architecture Mandatory)" if len(high_fat_products) > 0 else "Moderate"

env_col1, env_col2 = st.columns(2)
with env_col1:
    st.markdown(f"""
    **Computed Wastewater Parameters:**
    * **Solids Load Interval:** 0.1% - 0.8% Dry Matter
    * **Fat, Oil & Grease (FOG) Presence:** {fog_status}
    * **Engineering Optimization Core:** Cross Flow Separator (CFS) Configuration Required before anaerobic digestion.
    """)
with env_col2:
    st.markdown("""
    **Guaranteed Treatment System Efficiency:**
    * **Total Suspended Solids (TSS) Reduction:** $>90\%$ Removal
    * **Oil & Grease Extraction Rate:** $>90\%$ Separation
    * **Sludge Solid Concentration:** Thickened to $1\% - 3\%$ Outlet Dry Cake
    """)

st.markdown("---")

# Social Impact Evaluation & Groq Parsing Node
st.header("🤝 Social Impact Evaluation & Document Parser")
st.write("Socioeconomic profile cross-analyzed with targets from the [Nutreco Trust Dairy Case Study](https://www.nutreco.com/en/sustainability/good-citizenship/community-development/trust-dairy-project/).")

if uploaded_social_file is not None:
    if not groq_api_key:
        st.error("🔒 Please supply a valid Groq API Key to execute text ingestion pipelines.")
    else:
        try:
            file_contents = uploaded_social_file.read().decode("utf-8")
            client = Groq(api_key=groq_api_key)
            with st.spinner("Analyzing document text structure via Groq Llama-3 optimization..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are an expert dairy sector consultant. Extract social impact benchmarks from the raw data, highlighting variances."},
                        {"role": "user", "content": f"Compare these indicators against standard industrial dairy frameworks:\n\n{file_contents[:4000]}"}
                    ],
                    model="llama-3.1-70b-versatile",
                )
            st.success("Analysis complete via Groq Processing Node!")
            st.write(chat_completion.choices[0].message.content)
        except Exception as e:
            st.error(f"Inference pipeline execution failure: {e}")
else:
    st.info("💡 Dynamic Bypass Engaged: Standard case-study social parameters are activated because no custom third-party study was uploaded.")

# =============================================================================
# FILE EXPORT MODULE
# =============================================================================
st.markdown("---")
st.subheader("💾 Export & Document Generation Compile")

pdf_data = build_pdf_report()

st.download_button(
    label="Download Complete Finance-Ready DPR PDF",
    data=pdf_data,
    file_name="Detailed_Project_Report_Dairy.pdf",
    mime="application/pdf"
)
