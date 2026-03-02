import streamlit as st
import pandas as pd
from docx import Document
import base64
from pathlib import Path

# Page configuration
st.set_page_config(page_title="GRCS Simulator", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for modern UI with top navbar
st.markdown("""
<style>
    /* Hide Streamlit header and toolbar */
    header {display: none !important;}
    #MainMenu {display: none !important;}
    .stDeployButton {display: none !important;}
    footer {display: none !important;}
    
    /* Hide default sidebar */
    [data-testid="collapsedControl"] {display: none;}
    
    /* Light Blue Background */
    .stApp {
        background: linear-gradient(180deg, #e3f2fd 0%, #bbdefb 100%);
    }
    
    /* Main container styling */
    .main {
        padding-top: 0rem !important;
        background: transparent;
    }
    .block-container {
        padding-top: 2rem !important;
        background: transparent;
    }
    
    /* Typography - Improved Visibility */
    h1 {font-size: 32px !important; font-weight: 700 !important; color: #0d47a1; margin-bottom: 1rem;}
    h2 {font-size: 22px !important; font-weight: 600 !important; color: #1565c0; margin-top: 1.5rem; margin-bottom: 1rem;}
    h3 {font-size: 16px !important; font-weight: 600 !important; color: #1976d2; margin-top: 1rem; margin-bottom: 0.5rem;}
    p, label, div {font-size: 15px !important; color: #263238; font-weight: 500;}
    
    /* Centered Page Header */
    .page-header {
        text-align: center;
        padding: 1.5rem 1.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(13, 71, 161, 0.12);
        margin: 1rem auto 1.5rem auto;
        max-width: 900px;
        border: 2px solid #2196f3;
    }
    .page-header h1 {
        font-size: 28px !important;
        color: #0d47a1 !important;
        margin-bottom: 0.5rem !important;
        font-weight: 800 !important;
    }
    .page-header p {
        font-size: 13px !important;
        color: #37474f !important;
        margin: 0 !important;
        font-weight: 400 !important;
    }
    
    /* Streamlit components - Better Visibility */
    .stSlider, .stSelectbox, .stCheckbox {
        font-size: 14px !important;
        color: #263238 !important;
        font-weight: 600 !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1976d2 0%, #0d47a1 100%);
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 14px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(25, 118, 210, 0.5);
        background: linear-gradient(135deg, #2196f3 0%, #1565c0 100%);
    }
    
    /* Expander Header Text - SIMPLE AND DIRECT */
    .streamlit-expanderHeader {
        background-color: #1565c0 !important;
        color: #ffffff !important;
    }
    
    .streamlit-expanderHeader p,
    .streamlit-expanderHeader span,
    .streamlit-expanderHeader div,
    .streamlit-expanderHeader * {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }
    
    /* Make text inside expandable headers white */
    [data-testid="stExpanderHeader"],
    button.st-emotion-cache-q16mip {
        color: white !important;
    }
    
    [data-testid="stExpanderHeader"] span,
    button.st-emotion-cache-q16mip span {
        color: white !important;
        font-weight: 700 !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        border: 2px solid #2196f3 !important;
        border-radius: 8px;
        background: white !important;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 26px !important;
        color: #0d47a1 !important;
        font-weight: 800 !important;
    }
    
    /* Custom cards - Blue Theme */
    .info-card {
        background: linear-gradient(135deg, #2196f3 0%, #1565c0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4);
    }
    
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #2196f3;
        box-shadow: 0 4px 16px rgba(13, 71, 161, 0.15);
        margin: 1rem 0;
    }
    
    /* Input labels with better visibility */
    label {
        color: #0d47a1 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }

</style>
""", unsafe_allow_html=True)

# Top Navbar with Logos and Navigation
st.markdown("""
<style>
    .top-navbar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: -6rem -6rem 2rem -6rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .navbar-logos {
        display: flex;
        align-items: center;
        gap: 2rem;
    }
    
    .navbar-logo {
        height: 50px;
        width: auto;
        background: white;
        padding: 8px;
        border-radius: 8px;
    }
    
    .navbar-title {
        color: white;
        font-size: 24px;
        font-weight: 700;
        margin: 0 2rem;
        flex-grow: 1;
    }
    
    .nav-tabs {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        background: rgba(255,255,255,0.1);
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .nav-tab {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        font-size: 13px;
        transition: all 0.3s;
        cursor: pointer;
        border: 2px solid transparent;
        white-space: nowrap;
    }
    
    .nav-tab:hover {
        background: white;
        color: #667eea;
        transform: translateY(-2px);
    }
    
    .nav-tab.active {
        background: white;
        color: #667eea;
        border-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Navigation tabs
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    simulator_btn = st.button("🎯 Simulator", use_container_width=True, type="secondary" if st.session_state.get("page", "Simulator") != "Simulator" else "primary")
with col2:
    ref_btn = st.button("📊 GRCS Reference", use_container_width=True, type="secondary" if st.session_state.get("page", "Simulator") != "Reference" else "primary")
with col3:
    doc_btn = st.button("📖 Documentation", use_container_width=True, type="secondary" if st.session_state.get("page", "Simulator") != "Documentation" else "primary")
with col4:
    weight_btn = st.button("⚖️ Weight Calc", use_container_width=True, type="secondary" if st.session_state.get("page", "Simulator") != "Weight" else "primary")
with col5:
    lusr_btn = st.button("📈 LUSR Calc", use_container_width=True, type="secondary" if st.session_state.get("page", "Simulator") != "LUSR" else "primary")

# Handle navigation
if simulator_btn:
    st.session_state.page = "Simulator"
elif ref_btn:
    st.session_state.page = "Reference"
elif doc_btn:
    st.session_state.page = "Documentation"
elif weight_btn:
    st.session_state.page = "Weight"
elif lusr_btn:
    st.session_state.page = "LUSR"

# Initialize default page
if "page" not in st.session_state:
    st.session_state.page = "Simulator"

page = st.session_state.page

st.markdown("---")

if page == "Simulator":
    st.markdown('''
    <div class="page-header">
        <h1>🎯 Golden Record Confidence Score (GRCS) Simulator</h1>
        <p>Calculate confidence scores for data matching and golden record creation</p>
    </div>
    ''', unsafe_allow_html=True)

    attributes = {
        "Aadhaar": 18,
        "Name": 9,
        "DOB": 9,
        "Mobile": 7,
        "Gender": 3,
        "Father Name": 6,
        "Mother Name": 4,
        "Permanent Address": 8,
        "PAN": 5
    }
    source_authority = {
        "UIDAI": 85,
        "Civil Registry": 80,
        "RTPS Certified": 82,
        "Income Tax": 78,
        "Bank CBS": 78,
        "Self Declared": 20
    }
    st.header("📋 Attribute Matching Section")
    total_score = 0
    for attr, weight in attributes.items():
        with st.expander(f"**{attr}** (Weight: {weight})", expanded=True):
            col1, col2 = st.columns(2)

            with col1:
                mi = st.slider(f"Match Strength (Mi) for {attr}", 0.0, 1.0, 1.0, key=f"mi_{attr}")

            with col2:
                source = st.selectbox(f"Source for {attr}", list(source_authority.keys()), key=f"src_{attr}")

            si = source_authority[source] / 100

            contribution = weight * mi * si
            total_score += contribution

            st.write(f"Contribution: {round(contribution,2)}")

    # Reinforcement
    st.header("⚡ Reinforcement")

    reinforcement = 0
    if st.checkbox("Aadhaar + Name + DOB Exact Match"):
        reinforcement = 5
        st.write("Reinforcement Applied: +5")

    # Risk Adjustment
    st.header("⚠️ Risk Adjustment")

    risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"])

    risk_factor = 0
    if risk_level == "Medium":
        risk_factor = 0.02
    elif risk_level == "High":
        risk_factor = 0.05

    # Final GRCS
    grcs = total_score + reinforcement
    grcs = grcs * (1 - risk_factor)

    st.header("📊 Final Result")

    st.subheader(f"GRCS Score: {round(grcs,2)}%")

    # Decision Logic
    if grcs >= 92:
        decision = "Auto Merge"
    elif grcs >= 80:
        decision = "Conditional Auto Merge"
    elif grcs >= 70:
        decision = "Steward Assisted Merge"
    elif grcs >= 60:
        decision = "Manual Validation"
    else:
        decision = "Create New Golden Record"

    st.subheader(f"Decision: {decision}")

elif page == "Reference":
    st.markdown('<div class="info-card"><h1 style="color: white; margin: 0;">📊 GRCS Reference Table</h1><p style="color: rgba(255,255,255,0.9); margin-top: 0.5rem;">Complete attribute reference with weights and matching rules</p></div>', unsafe_allow_html=True)
    
    st.markdown("### Complete GRCS Attribute Reference")
    
    # Read the Excel file
    excel_file = "data/GRCS.xlsx"
    df = pd.read_excel(excel_file)
    
    # Display the table
    st.dataframe(df, width='stretch', hide_index=True)
    
    # Show some statistics
    st.markdown("### Key Insights")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Attributes", len(df))
    with col2:
        st.metric("Total Weight", f"{df['Weight (%)'].sum():.2f}")
    with col3:
        st.metric("Max Weight Attribute", df.loc[df['Weight (%)'].idxmax(), 'Attribute'])
    with col4:
        st.metric("Avg Weight per Attribute", f"{df['Weight (%)'].mean():.2%}")
    
    # Download option
    st.markdown("### Download Data")
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="GRCS_Reference.csv",
        mime="text/csv"
    )

elif page == "Documentation":
    st.markdown('<div class="info-card"><h1 style="color: white; margin: 0;">📖 Technical Documentation</h1><p style="color: rgba(255,255,255,0.9); margin-top: 0.5rem;">Comprehensive GRCS methodology and matching algorithms</p></div>', unsafe_allow_html=True)
    
    # Read the DOCX file
    doc_file = "data/GRCS_Technical_Documentation.docx"
    doc = Document(doc_file)
    
    # Extract and display document content
    st.markdown("### Complete Technical Documentation")
    
    # Display all paragraphs
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            # Style headings
            if text.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
                st.markdown(f"#### {text}")
                
                # Add Match Strength table after section 5
                if text.startswith("5. Match Strength"):
                    st.markdown("**Match Strength Reference Table:**")
                    match_strength_data = {
                        "Match Scenario": ["Exact Match", "92% Similarity", "Year of Birth Only Matches", "Unverified Mobile"],
                        "Mi Value": [1.0, 0.92, 0.6, 0.5]
                    }
                    df_mi = pd.DataFrame(match_strength_data)
                    st.dataframe(df_mi, width='stretch', hide_index=True)
            else:
                st.markdown(text)
    
    # Display tables from document
    if doc.tables:
        st.markdown("### Reference Tables from Documentation")
        for i, table in enumerate(doc.tables):
            st.markdown(f"#### Reference Table {i+1}")
            
            # Convert table to dataframe
            data = []
            for row in table.rows:
                data.append([cell.text for cell in row.cells])
            
            if data:
                headers = data[0] if len(data) > 0 else []
                rows = data[1:] if len(data) > 1 else []
                df_table = pd.DataFrame(rows, columns=headers)
                st.dataframe(df_table, width='stretch', hide_index=True)
    
    # Download documentation
    st.markdown("### Download Documentation")
    with open(doc_file, 'rb') as f:
        doc_bytes = f.read()
    st.download_button(
        label="📥 Download DOCX",
        data=doc_bytes,
        file_name="GRCS_Technical_Documentation.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

elif page == "Weight":
    st.markdown('<div class="info-card"><h1 style="color: white; margin: 0;">⚖️ Weight Calculation</h1><p style="color: rgba(255,255,255,0.9); margin-top: 0.5rem;">Calculate attribute weights using ACS model (L, U, S, R parameters)</p></div>', unsafe_allow_html=True)
    
    # ========== WEIGHT CALCULATION CALCULATOR ==========
    st.header("🧮 Weight Calculation Calculator (Based on ACS Model)")
    
    st.markdown("""
    ### Formula:
    **ACS_i = (0.35 × L_i + 0.30 × U_i + 0.20 × S_i + 0.15 × R_i)**
    
    **Then:** Wi = (ACS_i / Total ACS) × 100
    
    **Parameters (each 0-10 scale):**
    - **L = Legal Strength** (35%)
    - **U = Uniqueness Power** (30%)
    - **S = Stability Over Time** (20%)
    - **R = Service Impact Risk** (15%)
    """)
    
    st.markdown("---")
    st.markdown("### Enter L, U, S, R Values (0-10) for Each Attribute:")
    
    attributes_list = ["Aadhaar", "Name", "DOB", "Mobile", "Gender", "Father Name", "Mother Name", "Permanent Address", "PAN"]
    
    # Store ACS calculations
    acs_data = []
    
    for attr in attributes_list:
        with st.expander(f"**{attr}**", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                L = st.slider("L", 0, 10, 5, key=f"{attr}_L")
            with col2:
                U = st.slider("U", 0, 10, 5, key=f"{attr}_U")
            with col3:
                S = st.slider("S", 0, 10, 5, key=f"{attr}_S")
            with col4:
                R = st.slider("R", 0, 10, 5, key=f"{attr}_R")
            
            # Calculate ACS for this attribute using the formula
            acs_score = (0.35 * L + 0.30 * U + 0.20 * S + 0.15 * R)
            
            st.caption(f"**ACS = (0.35×{L} + 0.30×{U} + 0.20×{S} + 0.15×{R}) = {acs_score:.2f}**")
            
            acs_data.append({"Attribute": attr, "ACS": acs_score})
    
    # Calculate Total ACS and Weights
    st.markdown("---")
    st.header("📊 Calculated Weights")
    
    total_acs = sum([item["ACS"] for item in acs_data])
    
    weight_results = []
    for item in acs_data:
        weight = (item["ACS"] / total_acs * 100) if total_acs > 0 else 0
        weight_results.append({
            "Attribute": item["Attribute"],
            "ACS Score": round(item["ACS"], 2),
            "Weight (%)": round(weight, 2)
        })
    
    df_weights = pd.DataFrame(weight_results)
    st.dataframe(df_weights, width='stretch', hide_index=True)
    
    st.markdown(f"**Total ACS: {total_acs:.2f}** | **Total Weight: 100.00%**")
    
    # Documentation below calculator
    st.markdown("---")
    st.header("📖 Weight Calculation Documentation")
    
    with st.expander("Complete Weight Calculation Documentation", expanded=False):
        # Read the DOCX file
        doc_file = "data/Weight Calculation.docx"
        doc = Document(doc_file)
        
        # Display all paragraphs
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                # Style headings
                if text.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
                    st.markdown(f"#### {text}")
                else:
                    st.markdown(text)
        
        # Display tables from document
        if doc.tables:
            st.markdown("### Reference Tables")
            for i, table in enumerate(doc.tables):
                st.markdown(f"#### Table {i+1}")
                
                # Convert table to dataframe
                data = []
                for row in table.rows:
                    data.append([cell.text for cell in row.cells])
                
                if data:
                    headers = data[0] if len(data) > 0 else []
                    rows = data[1:] if len(data) > 1 else []
                    df_table = pd.DataFrame(rows, columns=headers)
                    st.dataframe(df_table, width='stretch', hide_index=True)
    
    # Download documentation
    st.markdown("### Download Documentation")
    with open(doc_file, 'rb') as f:
        doc_bytes = f.read()
    st.download_button(
        label="📥 Download DOCX",
        data=doc_bytes,
        file_name="Weight_Calculation.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

elif page == "LUSR":
    st.markdown('<div class="info-card"><h1 style="color: white; margin: 0;">📈 LUSR Calculation</h1><p style="color: rgba(255,255,255,0.9); margin-top: 0.5rem;">LUSR methodology and calculation framework</p></div>', unsafe_allow_html=True)
    
    # Read the DOCX file
    doc_file = "data/LUSR Calculation.docx"
    doc = Document(doc_file)
    
    # Extract and display document content
    st.markdown("### Complete LUSR Calculation Documentation")
    
    # Display all paragraphs
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            # Style headings
            if text.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
                st.markdown(f"#### {text}")
            else:
                st.markdown(text)
    
    # Display tables from document
    if doc.tables:
        st.markdown("### Reference Tables")
        for i, table in enumerate(doc.tables):
            st.markdown(f"#### Table {i+1}")
            
            # Convert table to dataframe
            data = []
            for row in table.rows:
                data.append([cell.text for cell in row.cells])
            
            if data:
                headers = data[0] if len(data) > 0 else []
                rows = data[1:] if len(data) > 1 else []
                df_table = pd.DataFrame(rows, columns=headers)
                st.dataframe(df_table, width='stretch', hide_index=True)
    
    # Download documentation
    st.markdown("### Download Documentation")
    with open(doc_file, 'rb') as f:
        doc_bytes = f.read()
    st.download_button(
        label="📥 Download DOCX",
        data=doc_bytes,
        file_name="LUSR_Calculation.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )