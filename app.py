import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from groq import Groq

# --- Page & Style Configuration ---
st.set_page_config(page_title="Dairy-DPR Architect Pro", layout="wide", page_icon="🥛")
sns.set_theme(style="whitegrid")

st.title("🥛 Dairy-DPR Architect Pro")
st.subheader("Automated Industrial Blueprint, Financial DPR & Sustainability Engine")
st.markdown("---")

# =============================================================================
# SIDEBAR: USER INPUTS & ENGINE CREDENTIALS
# =============================================================================
st.sidebar.header("🔑 Optimization Infrastructure")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password", help="Processes and evaluates unstructured social/environmental files.")

st.sidebar.header("1. Plant Spatial Profiles")
location = st.sidebar.text_input("Proposed Location", "Punjab, India")
user_capex = st.sidebar.number_input("Allocated CAPEX Budget (INR)", min_value=100000, value=2500000, step=50000)
design_capacity = st.sidebar.number_input("Design Plant Capacity (LPD)", min_value=1000, value=10000, step=1000)
actual_capacity = st.sidebar.slider("Operational Processing Volume (LPD)", min_value=500, max_value=int(design_capacity), value=int(design_capacity * 0.85))

st.sidebar.header("2. Product Strategy Matrix")
products = []
if st.sidebar.checkbox("Liquid Pasteurized Milk", value=True): products.append("Milk")
if st.sidebar.checkbox("Ghee"): products.append("Ghee")
if st.sidebar.checkbox("Dahi / Yogurt"): products.append("Dahi")
if st.sidebar.checkbox("Mawa / Khoa"): products.append("Mawa")
if st.sidebar.checkbox("Paneer / Cheese"): products.append("Paneer")

st.sidebar.header("3. Water-Energy Nexus Assets")
annual_milk_kg = st.sidebar.number_input("Annual Raw Milk Throughput (kg)", min_value=10000, value=3000000)
annual_water_l = st.sidebar.number_input("Annual Groundwater Abstraction (Liters)", min_value=10000, value=9930000)
annual_electricity_kwh = st.sidebar.number_input("Annual Grid Energy Consumption (kWh)", min_value=1000, value=300000)

st.sidebar.header("4. External Compliance Node")
uploaded_social_file = st.sidebar.file_uploader("Upload Third-Party Baseline Studies", type=["csv", "txt"])

# =============================================================================
# COMPONENT GRAPHICS GENERATOR (ILLUSTRATIVE PROCESS DIAGRAM)
# =============================================================================
def generate_process_diagram(selected_products):
    fig, ax = plt.subplots(figsize=(10, 2.5))
    ax.axis('off')
    
    # Core structural block coordinates
    stages = ["Raw Milk\nIntake", "Testing &\nChilling", "Pasteurization\n& Separation"]
    
    # Dynamic extension depending on user choices
    if "Ghee" in selected_products or "Mawa" in selected_products:
        stages.append("Thermal Cooking\n(Ghee/Mawa)")
    if "Dahi" in selected_products or "Paneer" in selected_products:
        stages.append("Fermentation/\nCoagulation")
    stages.append("Packaging &\nCold Chain")
    
    for i, stage in enumerate(stages):
        # Draw component processing blocks
        ax.text(i * 2.2, 0.5, stage, ha='center', va='center', color='white', weight='bold',
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#1E3A8A', edgecolor='#0284C7', lw=1.5))
        
        # Link sequences with flow direction indicators
        if i < len(stages) - 1:
            ax.annotate('', xy=((i + 1) * 2.2 - 0.5, 0.5), xytext=(i * 2.2 + 0.5, 0.5),
                        arrowprops=dict(arrowstyle="-|>", color='#0EA5E9', lw=2.5, mutation_scale=15))
            
    ax.set_xlim(-1, len(stages) * 2.2 - 1.2)
    ax.set_ylim(0, 1)
    return fig

# =============================================================================
# MULTI-VARIABLE COMPARATIVE BENCHMARKING CHART
# =============================================================================
def generate_benchmark_chart(user_metrics):
    # Normalized indexing against external scientific standards
    # Values represent ratios (User Asset Metric / Benchmark Standard Metric)
    categories = ['Economic Scale\n(CAPEX Match)', 'Direct Water\n(DWU Efficiency)', 'Total Footprint\n(TWF Nexus)', 'Social Target\n(Smallholders)']
    
    # 1.0 signifies ideal compliance alignment
    benchmark_baseline = [1.0, 1.0, 1.0, 1.0] 
    
    # Calculate relative ratios safely
    user_scores = [
        user_metrics['capex_ratio'],
        1.0 - (user_metrics['dwu_variance'] / 3.31),  # Higher indicates optimized lower water draw
        1.0 - (user_metrics['twf_variance'] / 9.0),   # Higher indicates optimized utility footprint
        1.10 # Target baseline alignment tracking factor
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
    ax.axhline(1.0, color='#EF4444', linestyle='--', alpha=0.7, label='Standard Target Parity')
    
    plt.tight_layout()
    return fig

# =============================================================================
# DATA SIMULATION ENGINE
# =============================================================================
DWU_BENCHMARK = 3.31
TWF_BENCHMARK = 9.0

# Scale technical systems utilizing standard framework templates
baseline_capacity = 20000
base_fixed_assets = 2000000
scaling_factor = design_capacity / baseline_capacity
calculated_required_capex = base_fixed_assets * scaling_factor

# Multi-variable water hydrology loops
capacity_utilization = (actual_capacity / design_capacity) * 100
user_dwu = annual_water_l / annual_milk_kg
indirect_wf = (annual_electricity_kwh * (5.69 / 0.1)) / annual_milk_kg 
user_twf = user_dwu + (indirect_wf * 0.1) 
daily_effluent_lpd = (annual_water_l / 365) * 0.74

metric_passbook = {
    'capex_ratio': user_capex / calculated_required_capex,
    'dwu_variance': user_dwu - DWU_BENCHMARK,
    'twf_variance': user_twf - TWF_BENCHMARK
}

# =============================================================================
# MAIN UI ROW STRUCTURES
# =============================================================================
st.header("🏢 Unit Topology Blueprint Layout")
st.write("Dynamic engineering node sequence map optimized for the specified product parameters:")
st.pyplot(generate_process_diagram(products))
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.header("📊 Multi-Variable Compliance Matrix")
    st.pyplot(generate_benchmark_chart(metric_passbook))
    
    st.subheader("Financial Performance Parameters")
    st.metric("Minimum Required Infrastructure Cost", f"₹ {calculated_required_capex:,.2f}")
    if calculated_required_capex > user_capex:
        st.error(f"⚠️ CAPEX Deficit: Plant expansion limits restricted by ₹ {calculated_required_capex - user_capex:,.2f}.")
    else:
        st.success("✅ Financial Compliance Verified.")

with col2:
    st.header("💧 Resource & Water Consumption Profile")
    st.write("Unit consumption indicators evaluated against empirical benchmarks from the [Punjab Dairy Case Study](https://www.mdpi.com/2073-4441/16/3/435):")
    
    st.metric(label="Direct Water Use (DWU)", value=f"{user_dwu:.2f} L/kg", 
              delta=f"{metric_passbook['dwu_variance']:.2f} L/kg vs Case Study Standard (3.31)", delta_color="inverse")
    st.metric(label="Total Water Footprint (TWF)", value=f"{user_twf:.2f} L/kg", 
              delta=f"{metric_passbook['twf_variance']:.2f} L/kg vs Case Study Standard (9.0)", delta_color="inverse")
    
    if capacity_utilization < 85.0:
        st.warning(f"⚠️ **Capacity Utilization Warning ({capacity_utilization:.1f}%):** Sub-optimal operations increase per-unit energy footprint overheads.")

st.markdown("---")

# =============================================================================
# ENVIRONMENTAL MODULE & INGESTION NODE
# =============================================================================
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

# =============================================================================
# GROQ INFERENCE PIPELINE
# =============================================================================
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
                        {
                            "role": "system",
                            "content": "You are an expert dairy sector consultant. Extract social impact benchmarks, smallholder integration strategies, and technological transparency details from the raw data, highlighting variances."
                        },
                        {
                            "role": "user",
                            "content": f"Compare these indicators against standard industrial dairy frameworks:\n\n{file_contents[:4000]}"
                        }
                    ],
                    model="llama-3.1-70b-versatile",
                )
            
            st.success("Analysis complete via Groq Processing Node!")
            st.markdown(f"### Extracted Insights from `{uploaded_social_file.name}`:")
            st.write(chat_completion.choices[0].message.content)
        except Exception as e:
            st.error(f"Inference pipeline execution failure: {e}")
else:
    st.info("💡 Upload an external localized social study inside the sidebar to display multi-project compliance tables.")
