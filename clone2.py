"""
Citizen Golden Record Simulator - Script 2
A Streamlit application for simulating identity confidence scoring.
"""

import streamlit as st
import pandas as pd
import base64
from pathlib import Path
from docx import Document

# Page configuration
st.set_page_config(
    page_title="GRCS Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
<style>
    html, body {
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }
    [data-testid="stToolbar"] {
        display: block !important;
        visibility: visible !important;
    }
    [data-testid="stDecoration"] {display: none !important;}
    #MainMenu {display: none !important;}
    .stDeployButton {display: none !important;}
    footer {display: none !important;}

    [data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    .stApp {
        background: linear-gradient(180deg, #e3f2fd 0%, #bbdefb 100%);
    }

    .main {
        padding-top: 0rem !important;
        background: transparent;
    }

    .block-container {
        padding-top: 5.2rem !important;
        background: transparent;
    }

    h1 {font-size: 32px !important; font-weight: 700 !important; color: #0d47a1; margin-bottom: 1rem;}
    h2 {font-size: 22px !important; font-weight: 600 !important; color: #1565c0; margin-top: 1.2rem; margin-bottom: 0.8rem;}
    h3 {font-size: 16px !important; font-weight: 600 !important; color: #1976d2; margin-top: 1rem; margin-bottom: 0.5rem;}
    p, label {font-size: 15px !important; color: #263238; font-weight: 500;}

    [data-testid="stDataFrame"] [role="columnheader"],
    [data-testid="stDataFrame"] [role="gridcell"],
    [data-testid="stTable"] th,
    [data-testid="stTable"] td {
        text-align: center !important;
    }

    [data-testid="stDataFrame"] [role="columnheader"],
    [data-testid="stTable"] th {
        font-weight: 700 !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="popover"] * {
        color: #10243a !important;
        opacity: 1 !important;
    }

    div[data-baseweb="popover"] [role="menu"],
    div[data-baseweb="popover"] [role="menuitem"],
    div[data-baseweb="popover"] [role="option"],
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li {
        background: #ffffff !important;
        color: #10243a !important;
    }

    div[data-baseweb="popover"] [role="menuitem"]:hover,
    div[data-baseweb="popover"] [role="option"]:hover,
    div[data-baseweb="popover"] li:hover {
        background: #e3f2fd !important;
        color: #0d47a1 !important;
    }

    .top-navbar {
        background: linear-gradient(135deg, #bbdefb 0%, #90caf9 100%);
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100vw;
        margin: 0;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border-radius: 0;
    }

    .navbar-logo {
        height: 50px;
        width: auto;
        background: white;
        padding: 8px;
        border-radius: 8px;
    }

    .navbar-title {
        color: #0d47a1;
        font-size: 24px;
        font-weight: 700;
        margin: 0 2rem;
        flex-grow: 1;
        text-align: center;
    }

    .page-header {
        text-align: center;
        padding: 1.5rem 1.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(13, 71, 161, 0.12);
        margin: 0.2rem auto 1.5rem auto;
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
        text-align: center !important;
    }

    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.78);
        border-right: 1px solid #90caf9;
    }

    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
        position: fixed !important;
        top: 5.6rem !important;
        left: 0.5rem !important;
        z-index: 1200 !important;
    }

    [data-testid="collapsedControl"] button,
    [data-testid="stSidebarCollapsedControl"] button,
    button[aria-label="Open sidebar"],
    button[aria-label="Close sidebar"] {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 42px !important;
        height: 42px !important;
        background: #0d47a1 !important;
        border: 2px solid #bbdefb !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(13, 71, 161, 0.45) !important;
        visibility: visible !important;
        opacity: 1 !important;
        color: #ffffff !important;
        transition: all 0.2s ease-in-out !important;
    }

    [data-testid="collapsedControl"] button:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover,
    button[aria-label="Open sidebar"]:hover,
    button[aria-label="Close sidebar"]:hover {
        background: #1565c0 !important;
        border-color: #e3f2fd !important;
        box-shadow: 0 6px 16px rgba(13, 71, 161, 0.55) !important;
        transform: translateY(-1px) !important;
    }

    [data-testid="collapsedControl"] button:focus-visible,
    [data-testid="stSidebarCollapsedControl"] button:focus-visible,
    button[aria-label="Open sidebar"]:focus-visible,
    button[aria-label="Close sidebar"]:focus-visible {
        outline: 2px solid #ffffff !important;
        outline-offset: 2px !important;
    }

    [data-testid="collapsedControl"] button svg,
    [data-testid="stSidebarCollapsedControl"] button svg,
    button[aria-label="Open sidebar"] svg,
    button[aria-label="Close sidebar"] svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #0d47a1 !important;
    }

    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] span {
        color: #1b2a3a !important;
        opacity: 1 !important;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: #0d47a1 !important;
        opacity: 1 !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #12304c !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="slider"] * {
        color: #12304c !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] {
        background: #1565c0 !important;
        border-color: #0d47a1 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #10243a !important;
        border: 1px solid #90caf9 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] input,
    [data-testid="stSidebar"] [data-baseweb="select"] span,
    [data-testid="stSidebar"] [data-baseweb="select"] div {
        color: #10243a !important;
        opacity: 1 !important;
    }

    [data-testid="stVegaLiteChart"] text,
    [data-testid="stVegaLiteChart"] span,
    [data-testid="stVegaLiteChart"] div {
        color: #12304c !important;
        fill: #12304c !important;
        opacity: 1 !important;
    }

    [data-testid="stVegaLiteChart"],
    [data-testid="stVegaLiteChart"] canvas,
    [data-testid="stVegaLiteChart"] svg,
    [data-testid="stVegaLiteChart"] > div,
    [data-testid="stVegaLiteChart"] .vega-embed,
    [data-testid="stVegaLiteChart"] .chart-wrapper,
    [data-testid="stArrowVegaLiteChart"],
    [data-testid="stArrowVegaLiteChart"] > div,
    .stVegaLiteChart,
    div[data-testid="stVegaLiteChart"] * {
        background: #ffffff !important;
        background-color: #ffffff !important;
    }

    [data-testid="stVegaLiteChart"] text {
        fill: #0d47a1 !important;
        color: #0d47a1 !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }

    [data-testid="stArrowVegaLiteChart"] {
        padding: 1rem !important;
        border-radius: 8px !important;
        background: #ffffff !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Load logos with error handling for deployment
def load_logo_base64(logo_path):
    """Load and encode logo file to base64 string."""
    try:
        if logo_path.exists():
            return base64.b64encode(logo_path.read_bytes()).decode()
    except Exception:
        st.warning(
            f"Logo not found: {logo_path.name}. "
            "App will work without logos."
        )
    return None


try:
    script_dir = Path(__file__).parent
    logo_bihar_path = script_dir / "assets" / "bihargovt-logo.png"
    logo_cipl_path = script_dir / "assets" / "cipl-logo.png"

    logo_bihar_b64 = load_logo_base64(logo_bihar_path)
    logo_cipl_b64 = load_logo_base64(logo_cipl_path)

    if logo_bihar_b64 and logo_cipl_b64:
        st.markdown(
            f"""
        <div class="top-navbar">
            <img src="data:image/png;base64,{logo_cipl_b64}"
                 class="navbar-logo" alt="CIPL Logo">
            <h2 class="navbar-title">
                Golden Record Confidence Score (GRCS)
            </h2>
            <img src="data:image/png;base64,{logo_bihar_b64}"
                 class="navbar-logo" alt="Bihar Government Logo">
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
        <div class="top-navbar">
            <h2 class="navbar-title" style="text-align: center; width: 100%;">
                Golden Record Confidence Score (GRCS)
            </h2>
        </div>
        """,
            unsafe_allow_html=True,
        )
except Exception as e:
    st.error(f"Error loading navbar: {e}")
    st.title("Golden Record Confidence Score (GRCS)")

st.markdown(
    """
<div class="page-header">
    <h1>Citizen Golden Record Simulator</h1>
    <p>Adjust identity attributes to see how the system classifies a citizen record.</p>
</div>
""",
    unsafe_allow_html=True,
)

# Navigation tabs
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    simulator_btn = st.button(
        "Simulator",
        use_container_width=True,
        type="secondary"
        if st.session_state.get("page", "Simulator") != "Simulator"
        else "primary",
    )
with col2:
    ref_btn = st.button(
        "GRCS Reference",
        use_container_width=True,
        type="secondary"
        if st.session_state.get("page", "Simulator") != "Reference"
        else "primary",
    )
with col3:
    doc_btn = st.button(
        "Documentation",
        use_container_width=True,
        type="secondary"
        if st.session_state.get("page", "Simulator") != "Documentation"
        else "primary",
    )
with col4:
    weight_btn = st.button(
        "Weight Calc",
        use_container_width=True,
        type="secondary"
        if st.session_state.get("page", "Simulator") != "Weight"
        else "primary",
    )
with col5:
    lusr_btn = st.button(
        "LUSR Calc",
        use_container_width=True,
        type="secondary"
        if st.session_state.get("page", "Simulator") != "LUSR"
        else "primary",
    )

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

if "page" not in st.session_state:
    st.session_state.page = "Simulator"

# ==========================================
# Application Configuration
# ==========================================

REFERENCE_DATA = [
    {"S.No": 1,  "Attribute": "Aadhaar",               "Weight (%)": 7.111274871, "Match Type": "Deterministic",       "Enterprise Rule": "UIDAI biometric verified"},
    {"S.No": 2,  "Attribute": "Name",                   "Weight (%)": 4.605747973, "Match Type": "Fuzzy + Phonetic",    "Enterprise Rule": "UIDAI > Civil Registry precedence"},
    {"S.No": 3,  "Attribute": "Date of Birth",          "Weight (%)": 5.600589536, "Match Type": "Exact > Year",        "Enterprise Rule": "Civil Registry override"},
    {"S.No": 4,  "Attribute": "Mobile Number",          "Weight (%)": 4.532056006, "Match Type": "OTP Verified",        "Enterprise Rule": "Aadhaar seeded + CBS timestamp"},
    {"S.No": 5,  "Attribute": "Gender",                 "Weight (%)": 4.679439941, "Match Type": "Exact",               "Enterprise Rule": "Legal identity anchor"},
    {"S.No": 6,  "Attribute": "Father's Name",          "Weight (%)": 5.011053795, "Match Type": "Fuzzy",               "Enterprise Rule": "Civil Registry priority"},
    {"S.No": 7,  "Attribute": "Mother's Name",          "Weight (%)": 5.011053795, "Match Type": "Fuzzy",               "Enterprise Rule": "Civil Registry validated"},
    {"S.No": 8,  "Attribute": "Permanent Address",      "Weight (%)": 4.56890199,  "Match Type": "Geo-normalized",      "Enterprise Rule": "UIDAI > Land Registry"},
    {"S.No": 9,  "Attribute": "Correspondence Address", "Weight (%)": 3.463522476, "Match Type": "Latest Timestamp",    "Enterprise Rule": "CBS latest update"},
    {"S.No": 10, "Attribute": "Caste",                  "Weight (%)": 5.342667649, "Match Type": "Certificate Verified","Enterprise Rule": "RTPS validated"},
    {"S.No": 11, "Attribute": "Marital Status",         "Weight (%)": 4.237288136, "Match Type": "Registry Preferred",  "Enterprise Rule": "Marriage Registry > Self"},
    {"S.No": 12, "Attribute": "Education Status",       "Weight (%)": 4.016212233, "Match Type": "Dept Certified",      "Enterprise Rule": "Education DB"},
    {"S.No": 13, "Attribute": "Employment Status",      "Weight (%)": 3.831982314, "Match Type": "Statutory",           "Enterprise Rule": "Labour Dept verified"},
    {"S.No": 14, "Attribute": "Ration Card Number",     "Weight (%)": 5.490051584, "Match Type": "Deterministic",       "Enterprise Rule": "PDS Household anchor"},
    {"S.No": 15, "Attribute": "Ration Card Type",       "Weight (%)": 4.089042,    "Match Type": "Exact",               "Enterprise Rule": "Welfare classification"},
    {"S.No": 16, "Attribute": "PAN ID",                 "Weight (%)": 6.632277082, "Match Type": "Deterministic",       "Enterprise Rule": "Income Tax authority"},
    {"S.No": 17, "Attribute": "Bank Account",           "Weight (%)": 5.711127487, "Match Type": "Masked Deterministic","Enterprise Rule": "CBS source-of-origin"},
    {"S.No": 18, "Attribute": "Land Ownership",         "Weight (%)": 6.042741341, "Match Type": "Legal Title",         "Enterprise Rule": "Land Registry override"},
    {"S.No": 19, "Attribute": "Motor Ownership",        "Weight (%)": 5.416359617, "Match Type": "Registration Match",  "Enterprise Rule": "VAHAN verified"},
    {"S.No": 20, "Attribute": "Nationality",            "Weight (%)": 4.605747973, "Match Type": "Legal",               "Enterprise Rule": "Civil Registry"},
]

SOURCE_AUTHORITY = {
    "UIDAI": 85,
    "Civil Registry": 80,
    "RTPS Certified": 82,
    "Income Tax": 78,
    "Bank CBS": 78,
    "Land Registry": 75,
    "Transport Registry": 75,
    "PDS": 70,
    "Survey DB": 45,
    "Self Declared": 20,
}

LUSR_TABLE_6 = [
    {"S.No": 1, "Attribute": "Aadhaar",       "L": 10, "U": 10, "S": 9, "R": 9, "ACL": 9.65},
    {"S.No": 2, "Attribute": "Name",          "L": 7,  "U": 5,  "S": 7, "R": 6, "ACL": 6.25},
    {"S.No": 3, "Attribute": "Date of Birth", "L": 8,  "U": 6,  "S": 9, "R": 8, "ACL": 7.6},
    {"S.No": 4, "Attribute": "Mobile Number", "L": 6,  "U": 6,  "S": 6, "R": 7, "ACL": 6.15},
    {"S.No": 5, "Attribute": "Gender",        "L": 7,  "U": 4,  "S": 9, "R": 6, "ACL": 6.35},
    {"S.No": 6, "Attribute": "PAN ID",        "L": 9,  "U": 9,  "S": 9, "R": 9, "ACL": 9.0},
]

# Weights derived from REFERENCE_DATA (first 10 attributes)
weights = {item["Attribute"]: item["Weight (%)"] / 100 for item in REFERENCE_DATA[:10]}

authority_scores = {
    "Aadhaar":                  85,
    "Name":                     80,
    "Date of Birth":            80,
    "Mobile Number":            78,
    "Gender":                   80,
    "Father's Name":            70,
    "Mother's Name":            70,
    "Permanent Address":        75,
    "Correspondence Address":   70,
    "Caste":                    82,
    "Marital Status":           75,
    "Education Status":         70,
    "Employment Status":        70,
    "Ration Card Number":       70,
    "Ration Card Type":         70,
    "PAN ID":                   78,
    "Bank Account":             78,
    "Land Ownership":           75,
    "Motor Ownership":          75,
    "Nationality":              80,
}

# ==========================================
# Module Render Functions
# ==========================================

def render_simulator():
    """Simulator with sidebar inputs."""
    st.sidebar.header("Scenario Inputs")

    results = []

    for attribute, weight in weights.items():
        mi = st.sidebar.slider(
            f"{attribute} Match Strength (Mi)",
            0.0, 1.0, 1.0
        )

        si = authority_scores.get(attribute, 70) / 100
        contribution = weight * mi * si

        results.append({
            "Attribute": attribute,
            "Weight": weight,
            "Mi": mi,
            "Si": si,
            "Contribution": contribution
        })

    df = pd.DataFrame(results)
    ics_score = df["Contribution"].sum()

    st.subheader("Attribute Contribution")
    st.dataframe(df, use_container_width=True)

    st.subheader("Identity Confidence Score")
    st.metric("ICS", f"{round(ics_score * 100, 2)}%")

    if ics_score >= 0.92:
        status = "Golden"
        color = "green"
    elif ics_score >= 0.75:
        status = "Silver"
        color = "orange"
    else:
        status = "Grey"
        color = "red"

    st.markdown(f"## Record Classification: :{color}[{status}]")

    st.subheader("Contribution by Attribute")
    st.bar_chart(df.set_index("Attribute")["Contribution"])


def render_reference_table():
    """GRCS Reference Table."""
    st.header("📊 GRCS Reference Table")

    df = pd.DataFrame(REFERENCE_DATA)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Attributes", len(df))
    with col2:
        st.metric("Total Weight %", f"{df['Weight (%)'].sum():.2f}%")
    with col3:
        max_attr = df.loc[df['Weight (%)'].idxmax()]
        st.metric("Max Weight Attribute", max_attr['Attribute'])
    with col4:
        st.metric("Avg Weight %", f"{df['Weight (%)'].mean():.2f}%")

    st.divider()

    st.subheader("Complete Attribute Reference")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "S.No":            st.column_config.NumberColumn("S.No", width="small"),
            "Attribute":       st.column_config.TextColumn("Attribute", width="medium"),
            "Weight (%)":      st.column_config.NumberColumn("Weight (%)", format="%.2f", width="small"),
            "Match Type":      st.column_config.TextColumn("Match Type", width="medium"),
            "Enterprise Rule": st.column_config.TextColumn("Enterprise Rule", width="large"),
        }
    )

    csv_data = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name="GRCS_Reference_Table.csv",
        mime="text/csv"
    )

    st.subheader("Filter by Weight Range")
    min_weight, max_weight = st.slider(
        "Select weight range (%)",
        min_value=float(df['Weight (%)'].min()),
        max_value=float(df['Weight (%)'].max()),
        value=(float(df['Weight (%)'].min()), float(df['Weight (%)'].max())),
        step=0.5
    )

    filtered_df = df[(df['Weight (%)'] >= min_weight) & (df['Weight (%)'] <= max_weight)]
    st.info(f"Showing {len(filtered_df)} attributes in selected range")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)


def render_technical_docs():
    """Technical Documentation."""
    st.header("📚 Technical Documentation")

    tabs = st.tabs(["Overview", "Authority Index", "Decision Engine", "Match Strength"])

    with tabs[0]:
        try:
            doc_file = "data/GRCS_Technical_Documentation.docx"
            if Path(doc_file).exists():
                doc = Document(doc_file)
                for para in doc.paragraphs:
                    if para.text.strip():
                        st.markdown(para.text)
            else:
                raise FileNotFoundError("DOCX not available")
        except Exception:
            st.markdown("""
### GRCS Scoring Methodology

**Formula:**
```
GRCS = Σ(Wi × Mi × Si) + Reinforcement - RiskAdjustment
```

Where:
- **Wi** = Attribute Weight (%)
- **Mi** = Match Strength (0-1)
- **Si** = Source Trust (AuthorityScore/100)

**Decision Thresholds:**
- ≥ 92%: Auto Merge
- 80–91%: Conditional Merge
- 70–79%: Steward Assisted
- 60–69%: Manual Review
- < 60%: Create New Record

### GRCS - Global Record Consolidation System

**Objective:** Establish a unified master identity record by consolidating records from multiple heterogeneous data sources while maintaining data integrity and traceability.

**Calculation Scope:**
1. Compute pairwise GRCS for each record pair
2. Normalize to 0–100 scale
3. Apply decision thresholds
4. Log all matches with rationale
""")

    with tabs[1]:
        st.markdown("### Authority Index - Source Credibility Scores")
        auth_df = pd.DataFrame(list(SOURCE_AUTHORITY.items()), columns=["Data Source", "Authority Score"])
        st.dataframe(auth_df, use_container_width=True, hide_index=True)
        st.markdown("""
**Authority Categories:**
- **85+**: Biometrically verified or legally issued IDs (UIDAI, Civil Registry)
- **78–82**: Statutory records with regular audit trails (Income Tax, Bank CBS)
- **70–75**: Registered entities with government backing (Land Registry, Transport)
- **45–70**: Administrative registries (PDS, Survey Data)
- **20**: Self-declared information with no verification
""")

    with tabs[2]:
        st.markdown("### Decision Engine - Match Thresholds")
        thresholds_df = pd.DataFrame([
            {"GRCS Score Range": "≥ 92%",  "Decision": "✅ Auto Merge",          "Confidence": "Very High"},
            {"GRCS Score Range": "80–91%", "Decision": "⚠️ Conditional Merge",   "Confidence": "High"},
            {"GRCS Score Range": "70–79%", "Decision": "👤 Steward Assisted",     "Confidence": "Medium"},
            {"GRCS Score Range": "60–69%", "Decision": "🔍 Manual Review",        "Confidence": "Low"},
            {"GRCS Score Range": "< 60%",  "Decision": "❌ Create New Record",    "Confidence": "Very Low"},
        ])
        st.dataframe(thresholds_df, use_container_width=True, hide_index=True)

    with tabs[3]:
        st.markdown("### Match Strength Model (M-Values)")
        match_strength_df = pd.DataFrame([
            {"Match Type": "Deterministic (Aadhaar)", "M-Value": "1.0",  "Example": "Aadhaar number exact match"},
            {"Match Type": "Legal Match",             "M-Value": "0.95", "Example": "PAN, Land Registry"},
            {"Match Type": "Fuzzy + Phonetic",        "M-Value": "0.85", "Example": "Name with tolerance → 85%"},
            {"Match Type": "Geo-normalized",          "M-Value": "0.80", "Example": "Address match after normalizing"},
            {"Match Type": "Year Match (DOB)",        "M-Value": "0.70", "Example": "Birth year only, day/month differ"},
            {"Match Type": "OTP Verified",            "M-Value": "0.90", "Example": "Mobile OTP authenticated"},
            {"Match Type": "Partial Match",           "M-Value": "0.60", "Example": "First name + initials"},
            {"Match Type": "No Match",                "M-Value": "0.0",  "Example": "Completely different values"},
        ])
        st.dataframe(match_strength_df, use_container_width=True, hide_index=True)


def render_weight_calculation():
    """Weight Calculation (ACS Model)."""
    st.header("⚖️ Weight Calculation (ACS Model)")

    st.markdown("### Attribute-Level ACS Calculation")
    st.caption("**Formula:** ACS = (0.35×L + 0.30×U + 0.20×S + 0.15×R)")

    st.subheader("LUSR Table 6 - Attribute Scoring Reference")
    lusr6_df = pd.DataFrame(LUSR_TABLE_6)
    st.dataframe(lusr6_df, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("Interactive ACS Calculator")

    selected_attribute = st.selectbox(
        "Select Attribute",
        [item["Attribute"] for item in LUSR_TABLE_6]
    )

    attr_data = next(item for item in LUSR_TABLE_6 if item["Attribute"] == selected_attribute)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        l_value = st.slider(
            "L (Legal) ▶ Deterministic Power",
            0, 10, attr_data["L"],
            help="How deterministic/legally binding is this attribute?"
        )

    with col2:
        u_value = st.slider(
            "U (Uniqueness) ▶ Distinguishing",
            0, 10, attr_data["U"],
            help="How unique is this attribute across population?"
        )

    with col3:
        s_value = st.slider(
            "S (Stability) ▶ Temporal Invariance",
            0, 10, attr_data["S"],
            help="Does this attribute remain stable over years?"
        )

    with col4:
        r_value = st.slider(
            "R (Risk) ▶ Fraud Susceptibility",
            0, 10, attr_data["R"],
            help="How easily can this be forged/manipulated?"
        )

    acs_score = (0.35 * l_value + 0.30 * u_value + 0.20 * s_value + 0.15 * r_value)

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Calculated ACS", f"{acs_score:.2f}/10.0")
    with metric_col2:
        st.metric("Reference ACL", f"{attr_data['ACL']}/10.0")
    with metric_col3:
        variance = abs(acs_score - attr_data['ACL'])
        st.metric("Variance", f"{variance:.2f}")

    st.progress(min(acs_score / 10, 1.0))

    if acs_score >= 9.0:
        st.success("⭐ Excellent discriminating power - Highest weight in GRCS")
    elif acs_score >= 7.0:
        st.info("✅ Good discriminating power - Highly reliable")
    elif acs_score >= 5.0:
        st.warning("⚠️ Moderate discriminating power - Use with other attributes")
    else:
        st.error("❌ Low discriminating power - Limited value in matching")


def render_lusr_calculation():
    """LUSR Calculation."""
    st.header("📊 LUSR Index Calculation")

    tabs = st.tabs(["Calculator", "Table 6 Reference", "Table 7 Scoring"])

    with tabs[0]:
        st.markdown("### LUSR Index Interactive Calculator")
        st.caption("Compute composite LUSR index for attribute assessment")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            lusr_l = st.slider(
                "L (Legal Strength)",
                0.0, 10.0, 8.5, 0.1,
                help="Deterministic and legal power of attribute"
            )

        with col2:
            lusr_u = st.slider(
                "U (Uniqueness)",
                0.0, 10.0, 8.0, 0.1,
                help="Distinguishing capability in population"
            )

        with col3:
            lusr_s = st.slider(
                "S (Stability)",
                0.0, 10.0, 8.5, 0.1,
                help="Temporal stability over lifetime"
            )

        with col4:
            lusr_r = st.slider(
                "R (Risk Impact)",
                0.0, 10.0, 8.0, 0.1,
                help="Fraud/manipulation susceptibility"
            )

        lusr_index = (lusr_l + lusr_u + lusr_s + lusr_r) / 4

        col1, col2 = st.columns(2)
        with col1:
            st.metric("LUSR Index (Average)", f"{lusr_index:.2f}/10.0")
        with col2:
            st.metric("Normalized Score", f"{(lusr_index / 10) * 100:.1f}%")

        st.progress(min(lusr_index / 10, 1.0))

        st.subheader("Component Breakdown")
        breakdown_df = pd.DataFrame([
            {"Component": "Legal",      "Score": lusr_l},
            {"Component": "Uniqueness", "Score": lusr_u},
            {"Component": "Stability",  "Score": lusr_s},
            {"Component": "Risk",       "Score": lusr_r},
        ])
        st.bar_chart(breakdown_df.set_index("Component")["Score"])

    with tabs[1]:
        st.markdown("### LUSR Table 6 - Attribute Scoring Reference")
        st.markdown("""
This table provides the L, U, S, R scores for each attribute and their
composite ACL (Attribute Credibility Level), used as reference values
in the weight calculation system.
""")
        lusr6_df = pd.DataFrame(LUSR_TABLE_6)
        st.dataframe(lusr6_df, use_container_width=True, hide_index=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg L Score", f"{lusr6_df['L'].mean():.2f}")
        with col2:
            st.metric("Avg U Score", f"{lusr6_df['U'].mean():.2f}")
        with col3:
            st.metric("Avg S Score", f"{lusr6_df['S'].mean():.2f}")
        with col4:
            st.metric("Avg R Score", f"{lusr6_df['R'].mean():.2f}")

    with tabs[2]:
        st.markdown("### LUSR Table 7 - Scoring Dimension Reference")
        st.markdown("""
Comprehensive scoring dimensions explaining the L-U-S-R model
and interpretation thresholds for attribute quality assessment.
""")
        lusr7_df = pd.DataFrame([
            {
                "Dimension":       "Legal (L)",
                "Description":     "Deterministic power & legal binding nature",
                "Scoring Range":   "0-10",
                "Characteristics": "Statutory ID > Certificate > Self-declared"
            },
            {
                "Dimension":       "Uniqueness (U)",
                "Description":     "Distinguishing capability in population",
                "Scoring Range":   "0-10",
                "Characteristics": "Aadhaar: 10 (1.3B unique) → Father Name: 5"
            },
            {
                "Dimension":       "Stability (S)",
                "Description":     "Temporal invariance over lifespan",
                "Scoring Range":   "0-10",
                "Characteristics": "Aadhaar/PAN: 9 → Address: 4 (volatile)"
            },
            {
                "Dimension":       "Risk (R)",
                "Description":     "Susceptibility to fraud/manipulation",
                "Scoring Range":   "0-10",
                "Characteristics": "Aadhaar: 9 (biometric) → Address: 3 (easily forged)"
            },
        ])
        st.dataframe(lusr7_df, use_container_width=True, hide_index=True)

        st.divider()

        st.markdown("### Quality Thresholds")
        thresholds_df = pd.DataFrame([
            {"LUSR Index": "8.5–10.0", "Quality": "🟢 Excellent", "Weight Assignment": "May increase from base"},
            {"LUSR Index": "7.0–8.4",  "Quality": "🟢 Good",      "Weight Assignment": "Standard (use base weight)"},
            {"LUSR Index": "5.0–6.9",  "Quality": "🟡 Moderate",  "Weight Assignment": "May decrease by 10–20%"},
            {"LUSR Index": "0.0–4.9",  "Quality": "🔴 Poor",      "Weight Assignment": "May decrease by 30–50%"},
        ])
        st.dataframe(thresholds_df, use_container_width=True, hide_index=True)


# ==========================================
# Page Routing
# ==========================================

page = st.session_state.get("page", "Simulator")

if page == "Simulator":
    st.markdown(
        """
    <div class="page-header">
        <h1>Citizen Golden Record Simulator</h1>
        <p>Adjust identity attributes to see how the system classifies a citizen record.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    render_simulator()
elif page == "Reference":
    render_reference_table()
elif page == "Documentation":
    render_technical_docs()
elif page == "Weight":
    render_weight_calculation()
elif page == "LUSR":
    render_lusr_calculation()

# Footer
st.markdown("---")
st.caption(
    "Golden Record Confidence Score (GRCS) Simulator | "
    "Citizen Golden Record System"
)