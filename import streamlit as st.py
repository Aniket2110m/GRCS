import streamlit as st
import pandas as pd
from docx import Document

# Page configuration
st.set_page_config(page_title="GRCS Simulator", layout="wide")

# Custom CSS to reduce font sizes and improve styling
st.markdown("""
<style>
    h1 {font-size: 28px !important; margin-bottom: 5px;}
    h2 {font-size: 18px !important; margin-top: 10px; margin-bottom: 8px;}
    h3 {font-size: 14px !important; margin-top: 8px; margin-bottom: 5px;}
    p, label, div {font-size: 12px !important;}
    .stSlider, .stSelectbox, .stCheckbox {font-size: 11px !important;}
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("## 📌 Navigation")
page = st.sidebar.radio("Select Page:", ["🎯 Simulator", "📊 GRCS Reference Table", "📖 Technical Documentation", "⚖️ Weight Calculation", "📈 LUSR Calculation"], label_visibility="collapsed")

if page == "🎯 Simulator":
    st.title("🎯 Golden Record Confidence Score (GRCS) Simulator")

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

elif page == "📊 GRCS Reference Table":
    st.title("📊 GRCS Reference Table")
    
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

elif page == "📖 Technical Documentation":
    st.title("📖 GRCS Technical Documentation")
    
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

elif page == "⚖️ Weight Calculation":
    st.title("⚖️ Weight Calculation")
    
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

elif page == "📈 LUSR Calculation":
    st.title("📈 LUSR Calculation")
    
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