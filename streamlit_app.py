import os
import streamlit as st
import pandas as pd
import plotly.express as px
import base64


# ... (keep your st.set_page_config, st.markdown CSS, SECTIONS, and helper functions unchanged) ...

# -----------------------------------------------------------------------------
# Page Header with Crop Trust Logo on the Left (Crop Trust Website Style)
# -----------------------------------------------------------------------------
LOGO_FILE = "images/ctLOGO.svg"  # logo is in the images folder 

header_logo_col, header_title_col = st.columns([1.15, 4.85], vertical_alignment="center")
with header_logo_col:
    # <-- 3. REPLACE st.image(...) WITH THIS BLOCK
    if os.path.exists(LOGO_FILE):
        with open(LOGO_FILE, "rb") as f:
            b64_logo = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(
            f'<img src="data:image/svg+xml;base64,{b64_logo}" style="width: 185px; height: auto; display: block;" alt="Crop Trust Logo">',
            unsafe_allow_html=True
        )
    else:
        st.warning(f"Logo file '{LOGO_FILE}' not found in app directory.")

with header_title_col:
    st.markdown(
        """
        <div class="ct-header-title-wrap">
            <h1 class="ct-header-title">PGRFA Conservation and Use Metrics Dashboard</h1>
            <p class="ct-header-subtitle">Overview of the global status of ex situ conservation and use of genetic resources of 30 crops</p>
            <p class="ct-header-subtitle">Data retrieved from multiple sources in 2025</p>
            <p class="ct-header-sublink">Full reports on the 30 crops available on <a href="https://www.croptrust.org/knowledge-hub/crop-conservation-strategies/" target="_blank" rel="noopener noreferrer">Crop Trust Website</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )


# -----------------------------------------------------------------------------
# Configuration & Layout
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PGRFA conservation and use metrics",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS to increase font size of the left sidebar navigation menu and style the header
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] [data-testid="stRadio"] label p {
        font-size: 1.12rem !important;
        font-weight: 500 !important;
        line-height: 1.45 !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label {
        padding-top: 4px;
        padding-bottom: 4px;
    }
    .ct-header-title-wrap {
        border-left: 2px solid #cbd5e1;
        padding-left: 1.25rem;
        margin-left: 0.25rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .ct-header-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
        line-height: 1.2;
    }
    .ct-header-subtitle {
        font-size: 0.95rem;
        color: #475569;
        margin: 0.25rem 0 0 0;
        font-weight: 400;
    }
    .ct-header-sublink {
        font-size: 0.9rem;
        color: #475569;
        margin: 0.2rem 0 0 0;
        font-weight: 400;
    }
    .ct-header-sublink a {
        color: #2a9d8f;
        text-decoration: underline;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# Sections Definition & Synchronized Navigation State
# -----------------------------------------------------------------------------
SECTIONS = [
    "📊 Production and Trade",
    "🌾 Genebank Holdings",
    "🌿 Taxa Conserved in Genebanks",
    "🧬 Accession Diversity",
    "🏛️ Policy & MLS Governance",
    "🛡️ Conservation Status & Safety",
    "📚 Documentation, Info Systems & Research",
    "📋 Raw Data Explorer",
    "📖 Methods and data sources"
]

if "selected_section" not in st.session_state:
    st.session_state.selected_section = SECTIONS[0]

def on_top_topic_change():
    st.session_state.selected_section = st.session_state.top_topic_select

def on_sidebar_topic_change():
    st.session_state.selected_section = st.session_state.sidebar_topic_radio

def get_crop_chart_height(n_items, min_height=520, px_per_bar=26, margin_px=140):
    """Scale chart height dynamically so 30 crops never overlap on the y-axis."""
    return max(min_height, int(n_items) * px_per_bar + margin_px)



# Topics dropdown directly below the main header
topic_col, _ = st.columns([2, 3])
with topic_col:
    st.selectbox(
        "Topics:",
        options=SECTIONS,
        index=SECTIONS.index(st.session_state.selected_section),
        key="top_topic_select",
        on_change=on_top_topic_change
    )

st.divider()

# -----------------------------------------------------------------------------
# Crop Type Mapping & Metric Domains (30 Crops)
# -----------------------------------------------------------------------------
CROP_TYPE_MAP = {
    # Original 15 crops
    "Allium": "Vegetables & Others",
    "Amaranth": "Grains & Pseudo-cereals",
    "Baobab": "Vegetables & Others",
    "Beet": "Roots & Tubers",
    "Carrot": "Roots & Tubers",
    "Cotton": "Oilseeds & Industrial",
    "Jute mallow": "Vegetables & Others",
    "Lettuce": "Vegetables & Others",
    "Okra": "Vegetables & Others",
    "Pigeonpea": "Legumes",
    "Sesame": "Oilseeds & Industrial",
    "Soybean": "Legumes",
    "Sugarcane": "Oilseeds & Industrial",
    "Tomato": "Vegetables & Others",
    "Turkey berry": "Vegetables & Others",
    # Additional 15 crops (30-crop dataset)
    "Alfalfa": "Forages",
    "Apple": "Fruits & Nuts",
    "Bambara groundnut": "Legumes",
    "Banana": "Fruits & Nuts",
    "Barley": "Grains & Pseudo-cereals",
    "Bean": "Legumes",
    "Breadfruit": "Fruits & Nuts",
    "Cacao": "Oilseeds & Industrial",
    "Cassava": "Roots & Tubers",
    "Chickpea": "Legumes",
    "Coconut": "Oilseeds & Industrial",
    "Coffee": "Oilseeds & Industrial",
    "Common bean": "Legumes",
    "Cowpea": "Legumes",
    "Eggplant": "Vegetables & Others",
    "Faba bean": "Legumes",
    "Finger millet": "Grains & Pseudo-cereals",
    "Grasspea": "Legumes",
    "Groundnut": "Legumes",
    "Lentil": "Legumes",
    "Maize": "Grains & Pseudo-cereals",
    "Oat": "Grains & Pseudo-cereals",
    "Pea": "Legumes",
    "Pearl millet": "Grains & Pseudo-cereals",
    "Pepper": "Vegetables & Others",
    "Potato": "Roots & Tubers",
    "Rice": "Grains & Pseudo-cereals",
    "Rye": "Grains & Pseudo-cereals",
    "Sorghum": "Grains & Pseudo-cereals",
    "Sunflower": "Oilseeds & Industrial",
    "Sweetpotato": "Roots & Tubers",
    "Taro": "Roots & Tubers",
    "Wheat": "Grains & Pseudo-cereals",
    "Yam": "Roots & Tubers"
}

TYPE_COLOR_MAP = {
    "Legumes": "#2a9d8f",
    "Grains & Pseudo-cereals": "#e9c46a",
    "Roots & Tubers": "#f4a261",
    "Oilseeds & Industrial": "#e76f51",
    "Vegetables & Others": "#457b9d",
    "Fruits & Nuts": "#8ab17d",
    "Forages": "#6d597a"
}

MATERIAL_COLOR_MAP = {
    "Landraces": "#2a9d8f",
    "Crop wild relatives (cwr)": "#1d3557",
    "Improved varieties": "#457b9d",
    "Breeding materials": "#e9c46a",
    "Weedy materials": "#e76f51"
}

STORAGE_MODE_COLOR_MAP = {
    "Seed storage": "#1d3557",
    "Field storage": "#64b5f6",
    "In-vitro storage": "#e63946",
    "Cryo storage": "#2a9d8f",
    "Dna": "#e9c46a",
    "Other storage": "#f4a261",
    "Not marked with a storage type": "#94a3b8"
}

METRIC_DOMAINS = {
    "Production & Trade": [
        "Harvested area worldwide (ha)",
        "Total production worldwide (tonnes)",
        "Gross production value worldwide (current thousand USD)",
        "Export quantity worldwide (tonnes)",
        "Export value worldwide (current thousand USD)",
        "Import quantity worldwide (tonnes)",
        "Import value worldwide (current thousand USD)"
    ],
    "Food & Nutrition": [
        "Contribution to calories in global food supplies (kcal/capita/day)",
        "Contribution to protein in global food supplies (g/capita/day)",
        "Contribution to fat in global food supplies (g/capita/day)",
        "Contribution to food weight in global food supplies (g/capita/day)"
    ],
    "Public Engagement": [
        "Number of public pageviews on Wikipedia over one year"
    ]
}

# -----------------------------------------------------------------------------
# Data Loaders (30-Sheet Merged Files)
# -----------------------------------------------------------------------------
FILE_TABLE1 = "Data/merged_30_sheets_Table1_all_crops.xlsx"
FILE_TABLE2 = "Data/merged_30_sheets_SI_Table1_all_crops.xlsx"
FILE_SI_TABLE2 = "Data/merged_30_sheets_SI_Table2_all_crops.xlsx"
FILE_TABLE3 = "Data/merged_30_sheets_Table3_all_crops.xlsx"
FILE_TABLE4 = "Data/merged_30_sheets_Table4_all_crops.xlsx"
FILE_TABLE5 = "Data/merged_30_sheets_Table5_all_crops.xlsx"
FILE_TABLE6 = "Data/merged_30_sheets_Table6_all_crops.xlsx"

def clean_numeric(series):
    """Safely convert strings with commas, %, or em-dashes to float."""
    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.replace("—", "", regex=False)
        .str.strip(),
        errors="coerce"
    ).fillna(0)

def clean_percentage(series):
    """Convert percentage strings (e.g. '67.7%') or decimal proportions (e.g. 0.473) to 0-100 scale."""
    raw_str = series.astype(str).str.strip()
    has_pct = raw_str.str.contains("%", regex=False)
    num = pd.to_numeric(
        raw_str.str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.replace("—", "", regex=False)
        .str.strip(),
        errors="coerce"
    ).fillna(0)
    return num.where(has_pct | (num > 1), num * 100)

@st.cache_data
def load_table1(file_path):
    xls = pd.ExcelFile(file_path)
    records = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        df["Crop"] = sheet
        df["Crop Type"] = CROP_TYPE_MAP.get(sheet, "Vegetables & Others")
        df["Global Value Cleaned"] = clean_numeric(df["Global Value"])
        
        num_cols = [
            "Number of countries where significant contributor",
            "Evenness of contribution across world regions",
            "Estimated international interdependence"
        ]
        for col in num_cols:
            if col in df.columns:
                df[col] = clean_numeric(df[col])
        records.append(df)
    return pd.concat(records, ignore_index=True)

@st.cache_data
def load_table2(file_path):
    xls = pd.ExcelFile(file_path)
    records = []
    t2_num_cols = [
        "Number of accessions",
        "Percent of total",
        "Cumulative percent",
        "Number of accessions in long term storage (-18-20 C)",
        "Number of accessions conserved in vitro or in cryo storage",
        "Number of accessions included in MLS (from GLIS)",
        "Number of accessions included in MLS (from genebank collections databases)"
    ]
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        df["Crop"] = sheet
        df["Crop Type"] = CROP_TYPE_MAP.get(sheet, "Vegetables & Others")
        
        for col in t2_num_cols:
            if col in df.columns:
                df[col] = clean_numeric(df[col])
            else:
                df[col] = 0.0
        records.append(df)
    return pd.concat(records, ignore_index=True)

@st.cache_data
def load_si_table2(file_path):
    xls = pd.ExcelFile(file_path)
    records = []
    acc_col = "Number of accessions (from genebank collections databases)"
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        df["Crop"] = sheet
        df["Crop Type"] = CROP_TYPE_MAP.get(sheet, "Vegetables & Others")
        df["Accessions Cleaned"] = clean_numeric(df[acc_col])
        total_crop_acc = df["Accessions Cleaned"].sum()
        df["Percent of Crop Accessions"] = (
            (df["Accessions Cleaned"] / total_crop_acc * 100) if total_crop_acc > 0 else 0.0
        )
        records.append(df)
    return pd.concat(records, ignore_index=True)

@st.cache_data
def load_table3(file_path):
    xls = pd.ExcelFile(file_path)
    records = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        df["Crop"] = sheet
        df["Crop Type"] = CROP_TYPE_MAP.get(sheet, "Vegetables & Others")
        df["Number Cleaned"] = clean_numeric(df["Number"])
        df["Percentage Cleaned"] = clean_numeric(df["Percentage"])
        records.append(df)
    return pd.concat(records, ignore_index=True)

@st.cache_data
def load_table4(file_path):
    xls = pd.ExcelFile(file_path)
    records = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        df["Crop"] = sheet
        df["Crop Type"] = CROP_TYPE_MAP.get(sheet, "Vegetables & Others")
        df["Number Cleaned"] = clean_numeric(df["Number"])
        df["Percentage Cleaned"] = clean_numeric(df["Percentage"])
        records.append(df)
    return pd.concat(records, ignore_index=True)

@st.cache_data
def load_table5(file_path):
    xls = pd.ExcelFile(file_path)
    records = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        df["Crop"] = sheet
        df["Crop Type"] = CROP_TYPE_MAP.get(sheet, "Vegetables & Others")
        df["Number Cleaned"] = clean_numeric(df["Number"])
        df["Percentage Cleaned"] = clean_percentage(df["Percentage"])
        records.append(df)
    return pd.concat(records, ignore_index=True)

@st.cache_data
def load_table6(file_path):
    xls = pd.ExcelFile(file_path)
    records = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        df["Crop"] = sheet
        df["Crop Type"] = CROP_TYPE_MAP.get(sheet, "Vegetables & Others")
        df["Number Cleaned"] = clean_numeric(df["Number"])
        records.append(df)
    return pd.concat(records, ignore_index=True)

try:
    df_t1 = load_table1(FILE_TABLE1)
    df_t2 = load_table2(FILE_TABLE2)
    df_si_t2 = load_si_table2(FILE_SI_TABLE2)
    df_t3 = load_table3(FILE_TABLE3)
    df_t4 = load_table4(FILE_TABLE4)
    df_t5 = load_table5(FILE_TABLE5)
    df_t6 = load_table6(FILE_TABLE6)
except Exception as e:
    st.error(f"Error loading Excel data files: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# Sidebar Navigation & Controls
# -----------------------------------------------------------------------------
st.sidebar.header("Navigation")
st.sidebar.radio(
    "Go to Section:",
    options=SECTIONS,
    index=SECTIONS.index(st.session_state.selected_section),
    key="sidebar_topic_radio",
    on_change=on_sidebar_topic_change
)

selected_section = st.session_state.selected_section

st.sidebar.divider()
st.sidebar.header("Filter & Group Controls")

# 1. Filter by Crop Type
all_crop_types = sorted(df_t1["Crop Type"].unique().tolist())
selected_crop_types = st.sidebar.multiselect(
    "Select Crop Category/Type:",
    options=all_crop_types,
    default=all_crop_types
)

# Filter datasets by Crop Type
t1_type_filtered = df_t1[df_t1["Crop Type"].isin(selected_crop_types)]
t2_type_filtered = df_t2[df_t2["Crop Type"].isin(selected_crop_types)]
si_t2_type_filtered = df_si_t2[df_si_t2["Crop Type"].isin(selected_crop_types)]
t3_type_filtered = df_t3[df_t3["Crop Type"].isin(selected_crop_types)]
t4_type_filtered = df_t4[df_t4["Crop Type"].isin(selected_crop_types)]
t5_type_filtered = df_t5[df_t5["Crop Type"].isin(selected_crop_types)]
t6_type_filtered = df_t6[df_t6["Crop Type"].isin(selected_crop_types)]

# 2. Filter by Specific Crops
available_crops = sorted(t1_type_filtered["Crop"].unique().tolist())
selected_crops = st.sidebar.multiselect(
    "Select Specific Crop(s):",
    options=available_crops,
    default=available_crops
)

# 3. Filter Domain & Specific Metric for Production and Trade
if selected_section == "📊 Production and Trade":
    selected_domain = st.sidebar.selectbox(
        "Select Metric Domain:",
        options=list(METRIC_DOMAINS.keys())
    )
    domain_metrics = METRIC_DOMAINS[selected_domain]
    selected_metric = st.sidebar.selectbox(
        "Select Metric to Visualize:",
        options=domain_metrics
    )
else:
    selected_domain = list(METRIC_DOMAINS.keys())[0]
    selected_metric = METRIC_DOMAINS[selected_domain][0]

# Final filtered dataframes
t1_crops_filtered = t1_type_filtered[t1_type_filtered["Crop"].isin(selected_crops)]
t1_final = t1_crops_filtered[t1_crops_filtered["Metric"] == selected_metric]

t2_final = t2_type_filtered[t2_type_filtered["Crop"].isin(selected_crops)]
si_t2_final = si_t2_type_filtered[si_t2_type_filtered["Crop"].isin(selected_crops)]
t3_final = t3_type_filtered[t3_type_filtered["Crop"].isin(selected_crops)]
t4_final = t4_type_filtered[t4_type_filtered["Crop"].isin(selected_crops)]
t5_final = t5_type_filtered[t5_type_filtered["Crop"].isin(selected_crops)]
t6_final = t6_type_filtered[t6_type_filtered["Crop"].isin(selected_crops)]

crop_chart_h = get_crop_chart_height(len(selected_crops), min_height=650, px_per_bar=26, margin_px=140)

# =============================================================================
# SECTION 1: Production and Trade
# =============================================================================
if selected_section == "📊 Production and Trade":
    if selected_domain in ("Production & Trade", "Food & Nutrition"):
        st.header(selected_domain)
    else:
        st.header(f"{selected_domain}: '{selected_metric}'")
    
    t1_subtab1, t1_subtab2, t1_subtab3, t1_subtab4 = st.tabs([
        "📈 Crop Level Comparison",
        "📊 Metrics by Crop Type",
        "🌐 Interdependence Matrix", 
        "📋 Raw Data Table"
    ])

    nutrition_metrics = [
        ("Contribution to calories in global food supplies (kcal/capita/day)", "Calories (kcal/capita/day)"),
        ("Contribution to protein in global food supplies (g/capita/day)", "Protein (g/capita/day)"),
        ("Contribution to fat in global food supplies (g/capita/day)", "Fat (g/capita/day)")
    ]

    prod_trade_metrics = [
        ("Total production worldwide (tonnes)", "Total Production (tonnes)"),
        ("Gross production value worldwide (current thousand USD)", "Gross Production Value (1,000 USD)"),
        ("Export value worldwide (current thousand USD)", "Export Value (1,000 USD)"),
        ("Import value worldwide (current thousand USD)", "Import Value (1,000 USD)")
    ]

    # Subtab 1: Crop Level Comparison
    with t1_subtab1:
        st.subheader("Crop Level Comparison")
        if selected_domain == "Food & Nutrition":
            nut_cols = st.columns(3)
            for idx, (metric_name, axis_label) in enumerate(nutrition_metrics):
                with nut_cols[idx]:
                    nut_df = t1_crops_filtered[t1_crops_filtered["Metric"] == metric_name].sort_values(
                        by="Global Value Cleaned", ascending=True
                    )
                    fig_nut = px.bar(
                        nut_df,
                        x="Global Value Cleaned",
                        y="Crop",
                        color="Crop Type",
                        color_discrete_map=TYPE_COLOR_MAP,
                        text_auto=".2s",
                        title=axis_label,
                        orientation="h",
                        height=crop_chart_h,
                        hover_data=["Number of countries where significant contributor"]
                    )
                    fig_nut.update_layout(
                        xaxis_title=axis_label,
                        yaxis_title="Crop Name" if idx == 0 else "",
                        yaxis={"categoryorder": "total ascending"},
                        showlegend=(idx == 2)
                    )
                    st.plotly_chart(fig_nut, use_container_width=True)

        elif selected_domain == "Production & Trade":
            for row_start in range(0, len(prod_trade_metrics), 2):
                row_cols = st.columns(2)
                for col_idx in range(2):
                    metric_idx = row_start + col_idx
                    if metric_idx < len(prod_trade_metrics):
                        metric_name, axis_label = prod_trade_metrics[metric_idx]
                        with row_cols[col_idx]:
                            pt_df = t1_crops_filtered[t1_crops_filtered["Metric"] == metric_name].sort_values(
                                by="Global Value Cleaned", ascending=True
                            )
                            fig_pt = px.bar(
                                pt_df,
                                x="Global Value Cleaned",
                                y="Crop",
                                color="Crop Type",
                                color_discrete_map=TYPE_COLOR_MAP,
                                text_auto=".2s",
                                title=axis_label,
                                orientation="h",
                                height=crop_chart_h,
                                hover_data=["Number of countries where significant contributor"]
                            )
                            fig_pt.update_layout(
                                xaxis_title=axis_label,
                                yaxis_title="Crop Name" if col_idx == 0 else "",
                                yaxis={"categoryorder": "total ascending"},
                                showlegend=(metric_idx == 1)
                            )
                            st.plotly_chart(fig_pt, use_container_width=True)

        else:
            t1_crop_sorted = t1_final.sort_values(by="Global Value Cleaned", ascending=True)
            fig_crop_bar = px.bar(
                t1_crop_sorted,
                x="Global Value Cleaned",
                y="Crop",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text_auto=".2s",
                title=f"Breakdown per Crop ({selected_metric})",
                orientation="h",
                height=crop_chart_h,
                hover_data=["Number of countries where significant contributor"]
            )
            fig_crop_bar.update_layout(
                xaxis_title=selected_metric,
                yaxis_title="Crop Name",
                yaxis={"categoryorder": "total ascending"}
            )
            st.plotly_chart(fig_crop_bar, use_container_width=True)

    # Subtab 2: Metrics by Crop Type
    with t1_subtab2:
        st.subheader("Metrics by Crop Type")
        if selected_domain == "Food & Nutrition":
            type_nut_cols = st.columns(3)
            for idx, (metric_name, axis_label) in enumerate(nutrition_metrics):
                with type_nut_cols[idx]:
                    group_by_type = (
                        t1_crops_filtered[t1_crops_filtered["Metric"] == metric_name]
                        .groupby("Crop Type", as_index=False)["Global Value Cleaned"]
                        .sum()
                        .sort_values(by="Global Value Cleaned", ascending=True)
                    )
                    fig_type_bar = px.bar(
                        group_by_type,
                        x="Global Value Cleaned",
                        y="Crop Type",
                        color="Crop Type",
                        color_discrete_map=TYPE_COLOR_MAP,
                        text_auto=".2s",
                        title=axis_label,
                        orientation="h"
                    )
                    fig_type_bar.update_layout(
                        xaxis_title=axis_label,
                        yaxis_title="Crop Category" if idx == 0 else "",
                        yaxis={"categoryorder": "total ascending"},
                        showlegend=False
                    )
                    st.plotly_chart(fig_type_bar, use_container_width=True)

        elif selected_domain == "Production & Trade":
            for row_start in range(0, len(prod_trade_metrics), 2):
                row_cols = st.columns(2)
                for col_idx in range(2):
                    metric_idx = row_start + col_idx
                    if metric_idx < len(prod_trade_metrics):
                        metric_name, axis_label = prod_trade_metrics[metric_idx]
                        with row_cols[col_idx]:
                            group_by_type = (
                                t1_crops_filtered[t1_crops_filtered["Metric"] == metric_name]
                                .groupby("Crop Type", as_index=False)["Global Value Cleaned"]
                                .sum()
                                .sort_values(by="Global Value Cleaned", ascending=True)
                            )
                            fig_type_bar = px.bar(
                                group_by_type,
                                x="Global Value Cleaned",
                                y="Crop Type",
                                color="Crop Type",
                                color_discrete_map=TYPE_COLOR_MAP,
                                text_auto=".2s",
                                title=axis_label,
                                orientation="h"
                            )
                            fig_type_bar.update_layout(
                                xaxis_title=axis_label,
                                yaxis_title="Crop Category" if col_idx == 0 else "",
                                yaxis={"categoryorder": "total ascending"},
                                showlegend=False
                            )
                            st.plotly_chart(fig_type_bar, use_container_width=True)

        else:
            group_by_type = (
                t1_final.groupby("Crop Type", as_index=False)["Global Value Cleaned"]
                .sum()
                .sort_values(by="Global Value Cleaned", ascending=True)
            )
            fig_type_bar = px.bar(
                group_by_type,
                x="Global Value Cleaned",
                y="Crop Type",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text_auto=".2s",
                title=f"Total Value Grouped by Category ({selected_metric})",
                orientation="h"
            )
            fig_type_bar.update_layout(
                xaxis_title=selected_metric,
                yaxis_title="Crop Category",
                yaxis={"categoryorder": "total ascending"},
                showlegend=False
            )
            st.plotly_chart(fig_type_bar, use_container_width=True)

    # Subtab 3: Regional Evenness vs. International Interdependence
    with t1_subtab3:
        st.subheader("Regional Evenness vs. International Interdependence")
        st.markdown("*Bubble size corresponds to the global value of the selected metric.*")
        fig_scatter = px.scatter(
            t1_final,
            x="Evenness of contribution across world regions",
            y="Estimated international interdependence",
            size="Global Value Cleaned",
            color="Crop Type",
            color_discrete_map=TYPE_COLOR_MAP,
            hover_name="Crop",
            text="Crop",
            title="Interdependence Matrix across Crop Types",
            labels={
                "Evenness of contribution across world regions": "Regional Evenness (0 to 1)",
                "Estimated international interdependence": "Interdependence Score (0 to 1)"
            }
        )
        fig_scatter.update_traces(textposition="top center")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Subtab 4: Filtered Raw Data & Download
    with t1_subtab4:
        st.subheader("Filtered Production and Trade Data")
        display_cols = [
            "Crop", "Crop Type", "Metric", "Global Value Cleaned",
            "Number of countries where significant contributor",
            "Evenness of contribution across world regions",
            "Estimated international interdependence"
        ]
        st.dataframe(t1_final[display_cols], use_container_width=True)
        csv_t1 = t1_final[display_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Production and Trade CSV",
            data=csv_t1,
            file_name="pgrfa_production_and_trade.csv",
            mime="text/csv",
            key="dl_t1_subtab"
        )

# =============================================================================
# SECTION 2: Genebank Holdings
# =============================================================================
elif selected_section == "🌾 Genebank Holdings":
    st.header("Genebank Holding Institutions & MLS Status")
    
    t2_subtab1, t2_subtab2 = st.tabs([
        "🌾 Single Crop Deep-Dive (Dropdown)",
        "📂 Category Breakdown (Crop Types)"
    ])

    with t2_subtab1:
        selected_crop_t2 = st.selectbox(
            "👇 Choose a Crop to Visualize Genebank Holdings:",
            options=available_crops,
            index=0
        )
        crop_t2_df = t2_final[t2_final["Crop"] == selected_crop_t2].sort_values(by="Number of accessions", ascending=False)
        crop_type_label = CROP_TYPE_MAP.get(selected_crop_t2, "Other")
        
        st.markdown(f"### 📌 Selected Crop: **{selected_crop_t2}** *(Category: {crop_type_label})*")
        
        total_crop_acc = crop_t2_df['Number of accessions'].sum()
        
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric("Total Accessions", f"{total_crop_acc:,.0f}")
        with kpi2:
            st.metric("Holding Institutions", len(crop_t2_df))
        with kpi3:
            lt_sum = crop_t2_df['Number of accessions in long term storage (-18-20 C)'].sum()
            st.metric("Long-Term Storage (-18°C)", f"{lt_sum:,.0f}")
        with kpi4:
            mls_sum = crop_t2_df['Number of accessions included in MLS (from GLIS)'].sum()
            st.metric("Included in MLS (GLIS)", f"{mls_sum:,.0f}")

        st.divider()
        top_n_inst = st.slider(f"Select Top N Institutions to Display for {selected_crop_t2}:", min_value=3, max_value=max(3, len(crop_t2_df)), value=min(15, len(crop_t2_df)))
        
        top_inst_df = crop_t2_df.head(top_n_inst).copy()
        top_inst_df["MLS Included (Max)"] = top_inst_df[[
            "Number of accessions included in MLS (from GLIS)",
            "Number of accessions included in MLS (from genebank collections databases)"
        ]].max(axis=1)
        top_inst_df["MLS Included (Max)"] = top_inst_df[["MLS Included (Max)", "Number of accessions"]].min(axis=1)
        top_inst_df["Not in MLS / Unspecified"] = (top_inst_df["Number of accessions"] - top_inst_df["MLS Included (Max)"]).clip(lower=0)
        
        top_inst_melted = top_inst_df.melt(
            id_vars=["Institution Code", "Institution Name", "Number of accessions"],
            value_vars=["MLS Included (Max)", "Not in MLS / Unspecified"],
            var_name="MLS Status",
            value_name="Accession Count"
        )
        
        fig_single_crop = px.bar(
            top_inst_melted,
            x="Institution Code",
            y="Accession Count",
            color="MLS Status",
            barmode="stack",
            hover_name="Institution Name",
            hover_data={"Number of accessions": ":,.0f", "Accession Count": ":,.0f"},
            text_auto=".2s",
            color_discrete_map={
                "MLS Included (Max)": "#2a9d8f",
                "Not in MLS / Unspecified": "#cbd5e1"
            },
            title=f"Top {top_n_inst} Genebank Institutions Holding {selected_crop_t2} Accessions (MLS Inclusion)"
        )
        fig_single_crop.update_layout(
            xaxis_title="Institution Code (WIEWS)",
            yaxis_title="Accessions Conserved",
            xaxis={"categoryorder": "array", "categoryarray": top_inst_df["Institution Code"].tolist()},
            legend_title="Status"
        )
        st.plotly_chart(fig_single_crop, use_container_width=True)

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            lt_val = crop_t2_df["Number of accessions in long term storage (-18-20 C)"].sum()
            vitro_val = crop_t2_df["Number of accessions conserved in vitro or in cryo storage"].sum()
            other_val = max(0, total_crop_acc - (lt_val + vitro_val))
            
            storage_pie_df = pd.DataFrame({
                "Storage Type": ["Long-Term Seed (-18°C)", "In-Vitro / Cryo", "Other / Unspecified"],
                "Accessions": [lt_val, vitro_val, other_val]
            })
            fig_storage_pie = px.pie(
                storage_pie_df,
                names="Storage Type",
                values="Accessions",
                hole=0.4,
                title=f"Storage Condition Distribution for {selected_crop_t2}",
                color_discrete_sequence=["#1b4332", "#52b788", "#b7e4c7"]
            )
            st.plotly_chart(fig_storage_pie, use_container_width=True)

        with col_s2:
            mls_glis = crop_t2_df["Number of accessions included in MLS (from GLIS)"].sum()
            mls_db = crop_t2_df["Number of accessions included in MLS (from genebank collections databases)"].sum()
            
            mls_glis_pct = (mls_glis / total_crop_acc * 100) if total_crop_acc > 0 else 0
            mls_db_pct = (mls_db / total_crop_acc * 100) if total_crop_acc > 0 else 0
            
            mls_comp_df = pd.DataFrame({
                "Reporting System": ["MLS (GLIS)", "MLS (Genebank DBs)"],
                "Percentage": [mls_glis_pct, mls_db_pct],
                "Accessions": [mls_glis, mls_db]
            })
            fig_mls_bar = px.bar(
                mls_comp_df,
                x="Reporting System",
                y="Percentage",
                color="Reporting System",
                text=mls_comp_df["Percentage"].apply(lambda v: f"{v:.1f}%"),
                hover_data={"Accessions": ":,.0f", "Percentage": ":.2f%"},
                title=f"MLS Accession Reporting (% of Total) for {selected_crop_t2}",
                color_discrete_sequence=["#2a9d8f", "#e9c46a"]
            )
            fig_mls_bar.update_traces(textposition="outside")
            fig_mls_bar.update_layout(
                yaxis_title="Percentage of Total Accessions (%)",
                yaxis_range=[0, max(100, mls_glis_pct * 1.15, mls_db_pct * 1.15)],
                showlegend=False
            )
            st.plotly_chart(fig_mls_bar, use_container_width=True)

    with t2_subtab2:
        st.subheader("Holdings Aggregated by Crop Category")
        t2_type_summary = t2_final.groupby("Crop Type", as_index=False)[[
            "Number of accessions",
            "Number of accessions in long term storage (-18-20 C)",
            "Number of accessions included in MLS (from GLIS)"
        ]].sum()
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            fig_type_acc = px.bar(
                t2_type_summary,
                x="Crop Type",
                y="Number of accessions",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text_auto=".2s",
                title="Total Accessions per Crop Category"
            )
            fig_type_acc.update_layout(showlegend=False)
            st.plotly_chart(fig_type_acc, use_container_width=True)

        with col_t2:
            t2_type_melted = t2_type_summary.melt(
                id_vars=["Crop Type"],
                value_vars=[
                    "Number of accessions in long term storage (-18-20 C)",
                    "Number of accessions included in MLS (from GLIS)"
                ],
                var_name="Category",
                value_name="Accession Count"
            )
            t2_type_melted["Category"] = t2_type_melted["Category"].replace({
                "Number of accessions in long term storage (-18-20 C)": "Long-Term Storage (-18°C)",
                "Number of accessions included in MLS (from GLIS)": "MLS Included (GLIS)"
            })
            fig_type_comp = px.bar(
                t2_type_melted,
                x="Crop Type",
                y="Accession Count",
                color="Category",
                barmode="group",
                text_auto=".2s",
                title="Storage & MLS Inclusion by Category",
                color_discrete_sequence=["#1b4332", "#52b788"]
            )
            st.plotly_chart(fig_type_comp, use_container_width=True)

# =============================================================================
# SECTION 3: Taxa Conserved in Genebanks
# =============================================================================
elif selected_section == "🌿 Taxa Conserved in Genebanks":
    st.header("Taxa Conserved in Genebanks")
    
    si2_subtab1, si2_subtab2, si2_subtab3 = st.tabs([
        "🌿 Single Crop Taxa Deep-Dive",
        "📊 Taxonomic Richness Across Crops & Categories",
        "📋 Filtered Conserved Taxa Data"
    ])

    # Subtab 1: Single Crop Taxa Breakdown
    with si2_subtab1:
        selected_crop_si2 = st.selectbox(
            "👇 Choose a Crop to Explore Conserved Taxa:",
            options=available_crops,
            index=0
        )
        crop_si2_df = (
            si_t2_final[si_t2_final["Crop"] == selected_crop_si2]
            .sort_values(by="Accessions Cleaned", ascending=False)
            .reset_index(drop=True)
        )
        crop_type_si2 = CROP_TYPE_MAP.get(selected_crop_si2, "Other")
        
        st.markdown(f"### 📌 Selected Crop: **{selected_crop_si2}** *(Category: {crop_type_si2})*")
        
        total_si2_acc = crop_si2_df["Accessions Cleaned"].sum()
        num_taxa_crop = len(crop_si2_df)
        top_taxon_name = crop_si2_df.loc[0, "Taxon"] if not crop_si2_df.empty else "N/A"
        top_taxon_share = crop_si2_df.loc[0, "Percent of Crop Accessions"] if not crop_si2_df.empty else 0.0
        
        tkpi1, tkpi2, tkpi3 = st.columns(3)
        with tkpi1:
            st.metric("Total Accessions (Genebank DBs)", f"{total_si2_acc:,.0f}")
        with tkpi2:
            st.metric("Distinct Conserved Taxa", f"{num_taxa_crop:,.0f}")
        with tkpi3:
            st.metric(
                label=f"Dominant Taxon ({top_taxon_name})",
                value=f"{top_taxon_share:.1f}%"
            )

        st.divider()
        max_taxa_slider = max(1, len(crop_si2_df))
        if max_taxa_slider > 1:
            top_n_taxa = st.slider(
                f"Select Top N Taxa to Display for {selected_crop_si2}:",
                min_value=1,
                max_value=max_taxa_slider,
                value=min(15, max_taxa_slider)
            )
        else:
            top_n_taxa = 1
            st.info(f"Only 1 taxon is recorded for {selected_crop_si2}.")
        
        top_taxa_df = crop_si2_df.head(top_n_taxa).sort_values(by="Accessions Cleaned", ascending=True)
        
        # Dynamically scale chart height with the number of displayed taxa (28px per bar + margins)
        dynamic_taxa_bar_height = max(420, len(top_taxa_df) * 28 + 140)
        
        col_tx1, col_tx2 = st.columns([3, 2])
        with col_tx1:
            fig_taxa_bar = px.bar(
                top_taxa_df,
                x="Accessions Cleaned",
                y="Taxon",
                text_auto=".2s",
                hover_data={"Accessions Cleaned": ":,.0f", "Percent of Crop Accessions": ":.2f%"},
                title=f"Top {top_n_taxa} Conserved Taxa for {selected_crop_si2}",
                orientation="h",
                height=dynamic_taxa_bar_height,
                color_discrete_sequence=[TYPE_COLOR_MAP.get(crop_type_si2, "#2a9d8f")]
            )
            fig_taxa_bar.update_layout(
                xaxis_title="Number of Accessions",
                yaxis_title="Taxon",
                yaxis={"categoryorder": "total ascending", "automargin": True},
                bargap=0.25
            )
            st.plotly_chart(fig_taxa_bar, use_container_width=True)
            
        with col_tx2:
            pie_top_df = crop_si2_df.head(min(4, len(crop_si2_df)))[["Taxon", "Accessions Cleaned"]].copy()
            if len(crop_si2_df) > 4:
                other_acc = crop_si2_df.iloc[4:]["Accessions Cleaned"].sum()
                pie_top_df = pd.concat([
                    pie_top_df,
                    pd.DataFrame({"Taxon": ["Others"], "Accessions Cleaned": [other_acc]})
                ], ignore_index=True)
            
            fig_taxa_pie = px.pie(
                pie_top_df,
                names="Taxon",
                values="Accessions Cleaned",
                hole=0.4,
                title=f"Taxonomic Composition of {selected_crop_si2} Holdings",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(fig_taxa_pie, use_container_width=True)

    # Subtab 2: Cross-Crop & Category Taxonomic Richness
    with si2_subtab2:
        st.subheader("Taxonomic Richness & Accession Concentration Across Crops")
        
        taxa_richness_df = (
            si_t2_final.groupby(["Crop", "Crop Type"], as_index=False)
            .agg(
                Distinct_Taxa=("Taxon", "nunique"),
                Total_Accessions=("Accessions Cleaned", "sum")
            )
            .sort_values(by="Distinct_Taxa", ascending=True)
        )
        
        taxa_cat_df = (
            si_t2_final.groupby("Crop Type", as_index=False)
            .agg(
                Distinct_Taxa=("Taxon", "nunique"),
                Total_Accessions=("Accessions Cleaned", "sum")
            )
            .sort_values(by="Distinct_Taxa", ascending=True)
        )
        
        dynamic_rich_crop_height = max(520, len(taxa_richness_df) * 26 + 140)
        dynamic_rich_cat_height = max(520, len(taxa_cat_df) * 45 + 140)
        
        col_tr1, col_tr2 = st.columns(2)
        with col_tr1:
            fig_rich_crop = px.bar(
                taxa_richness_df,
                x="Distinct_Taxa",
                y="Crop",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text_auto=True,
                hover_data={"Total_Accessions": ":,.0f"},
                title="Number of Conserved Taxa per Crop",
                orientation="h",
                height=dynamic_rich_crop_height
            )
            fig_rich_crop.update_layout(
                xaxis_title="Distinct Taxa Count",
                yaxis_title="Crop",
                yaxis={"categoryorder": "total ascending", "automargin": True}
            )
            st.plotly_chart(fig_rich_crop, use_container_width=True)
            
        with col_tr2:
            fig_rich_cat = px.bar(
                taxa_cat_df,
                x="Distinct_Taxa",
                y="Crop Type",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text_auto=True,
                hover_data={"Total_Accessions": ":,.0f"},
                title="Total Conserved Taxa by Crop Category",
                orientation="h",
                height=dynamic_rich_cat_height
            )
            fig_rich_cat.update_layout(
                xaxis_title="Distinct Taxa Count",
                yaxis_title="Crop Category",
                yaxis={"categoryorder": "total ascending", "automargin": True},
                showlegend=False
            )
            st.plotly_chart(fig_rich_cat, use_container_width=True)

    # Subtab 3: Filtered Conserved Taxa Dataset
    with si2_subtab3:
        st.subheader("Filtered Taxa Conserved in Genebanks Dataset")
        si2_display_cols = [
            "Crop",
            "Crop Type",
            "Taxon",
            "Accessions Cleaned",
            "Percent of Crop Accessions"
        ]
        st.dataframe(si_t2_final[si2_display_cols], use_container_width=True)
        csv_si2 = si_t2_final[si2_display_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Conserved Taxa CSV",
            data=csv_si2,
            file_name="pgrfa_conserved_taxa.csv",
            mime="text/csv",
            key="dl_si2_subtab"
        )

# =============================================================================
# SECTION 4: Accession Diversity & Taxonomy
# =============================================================================
elif selected_section == "🧬 Accession Diversity":
    st.header("Accession Biological Types & Taxonomic Diversity")
    
    t3_subtab1, t3_subtab2, t3_subtab3 = st.tabs([
        "🧬 Accession Types Breakdown",
        "🏛️ Taxonomic & Institutional Scope",
        "📋 Filtered Accession Diversity Data"
    ])

    bio_metrics = [
        "Number of accessions of landraces in genebank collections",
        "Number of accessions of crop wild relatives (CWR) in genebank collections",
        "Number of accessions of improved varieties in genebank collections",
        "Number of accessions of breeding materials in genebank collections",
        "Number of accessions of weedy materials in genebank collections"
    ]

    material_order = list(MATERIAL_COLOR_MAP.keys())

    with t3_subtab1:
        st.subheader("Biological & Diversity Material Types per Crop")
        t3_bio = t3_final[t3_final["Metric"].isin(bio_metrics)].copy()
        t3_bio["Material Type"] = t3_bio["Metric"].str.replace("Number of accessions of ", "", regex=False).str.replace(" in genebank collections", "", regex=False).str.capitalize()
        
        fig_bio_crop = px.bar(
            t3_bio,
            x="Number Cleaned",
            y="Crop",
            color="Material Type",
            color_discrete_map=MATERIAL_COLOR_MAP,
            category_orders={"Material Type": material_order},
            title="Biological Material Types breakdown by Crop",
            text_auto=".2s",
            barmode="stack",
            orientation="h",
            height=crop_chart_h
        )
        fig_bio_crop.update_layout(xaxis_title="Number of Accessions", yaxis_title="Crop", yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_bio_crop, use_container_width=True)

        t3_bio_cat = t3_bio.groupby(["Crop Type", "Material Type"], as_index=False)["Number Cleaned"].sum()
        fig_bio_cat = px.bar(
            t3_bio_cat,
            x="Number Cleaned",
            y="Crop Type",
            color="Material Type",
            color_discrete_map=MATERIAL_COLOR_MAP,
            category_orders={"Material Type": material_order},
            title="Biological Material Types breakdown by Category",
            text_auto=".2s",
            barmode="group",
            orientation="h",
            height=520
        )
        fig_bio_cat.update_layout(xaxis_title="Accession Count", yaxis_title="Crop Category", yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_bio_cat, use_container_width=True)

    with t3_subtab2:
        st.subheader("Taxonomic Scope & Global Institutional Reach")
        t3_tax_metrics = [
            "Number of distinct taxonomic names in genebank collections",
            "Number of institutions holding genebank collections",
            "Number of countries where germplasm has been collected for genebank collections"
        ]
        selected_tax_metric = st.selectbox("Select Diversity / Scope Indicator:", options=t3_tax_metrics, index=0)
        t3_tax_df = t3_final[t3_final["Metric"] == selected_tax_metric].sort_values(by="Number Cleaned", ascending=True)
        
        fig_tax_bar = px.bar(
            t3_tax_df,
            x="Number Cleaned",
            y="Crop",
            color="Crop Type",
            color_discrete_map=TYPE_COLOR_MAP,
            text_auto=".2s",
            title=f"Comparison across Crops: {selected_tax_metric}",
            orientation="h",
            height=crop_chart_h
        )
        fig_tax_bar.update_layout(xaxis_title="Count", yaxis_title="Crop Name", yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_tax_bar, use_container_width=True)

    with t3_subtab3:
        st.subheader("Filtered Accession Diversity Dataset")
        t3_display_cols = ["Crop", "Crop Type", "Metric", "Number Cleaned", "Percentage Cleaned"]
        st.dataframe(t3_final[t3_display_cols], use_container_width=True)
        csv_t3 = t3_final[t3_display_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Accession Diversity CSV",
            data=csv_t3,
            file_name="pgrfa_accession_diversity.csv",
            mime="text/csv",
            key="dl_t3_subtab"
        )

# =============================================================================
# SECTION 5: Policy, Governance & MLS Status
# =============================================================================
elif selected_section == "🏛️ Policy & MLS Governance":
    st.header("Policy, Governance, DOIs & MLS Status")
    
    t4_subtab1, t4_subtab2, t4_subtab3 = st.tabs([
        "🏛️ Institutional Governance & Annex I",
        "🌐 MLS Inclusion & DOI Identifiers",
        "📋 Filtered Policy & Governance Data"
    ])

    with t4_subtab1:
        st.subheader("International vs. National Genebank Holdings & Annex I Inclusion")
        
        inst_metrics = [
            "Number of accessions in genebank collections in international institutions",
            "Number of accessions in genebank collections in national or other institutions"
        ]
        
        t4_inst = t4_final[t4_final["Metric"].isin(inst_metrics)].copy()
        t4_inst["Institution Type"] = t4_inst["Metric"].str.replace("Number of accessions in genebank collections in ", "", regex=False).str.capitalize()
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            fig_inst_crop = px.bar(
                t4_inst,
                x="Number Cleaned",
                y="Crop",
                color="Institution Type",
                title="International vs. National Accessions per Crop",
                text_auto=".2s",
                barmode="stack",
                orientation="h",
                height=crop_chart_h,
                color_discrete_sequence=["#2a9d8f", "#e76f51"]
            )
            fig_inst_crop.update_layout(xaxis_title="Accession Count", yaxis_title="Crop", yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_inst_crop, use_container_width=True)

        with col_p2:
            t4_annex = t4_final[t4_final["Metric"] == "Number of accessions in genebank collections in Annex I"]
            fig_annex_bar = px.bar(
                t4_annex,
                x="Number Cleaned",
                y="Crop",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                title="Annex I Accession Holdings per Crop",
                text_auto=".2s",
                orientation="h",
                height=crop_chart_h
            )
            fig_annex_bar.update_layout(xaxis_title="Accessions in Annex I", yaxis_title="Crop", yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_annex_bar, use_container_width=True)

    with t4_subtab2:
        st.subheader("Multilateral System (MLS) Status & Digital Object Identifiers (DOI)")
        
        mls_doi_metrics = [
            "Number of accessions with DOI (Plant Treaty GLIS 2025)",
            "Number of accessions included in the Multilateral System (MLS) (Plant Treaty GLIS 2025)",
            "Number of accessions included in the Multilateral System (MLS) (genebank collections databases)",
            "Number of accessions not included in the Multilateral System (MLS) (genebank collections databases)",
            "Number of accessions without information regarding inclusion in the Multilateral System (MLS) (genebank collections databases)"
        ]
        
        selected_t4_metric = st.selectbox(
            "Select Governance / Policy Indicator:",
            options=mls_doi_metrics,
            index=0
        )
        
        t4_sel_df = t4_final[t4_final["Metric"] == selected_t4_metric].copy()
        
        tot_acc_t3 = (
            t3_final[t3_final["Metric"] == "Total number of accessions in genebank collections"]
            [["Crop", "Number Cleaned"]]
            .rename(columns={"Number Cleaned": "Total Accessions"})
        )
        
        mls_stacked_config = {
            "Number of accessions included in the Multilateral System (MLS) (Plant Treaty GLIS 2025)": {
                "selected_label": "Included in MLS (GLIS)",
                "remaining_label": "Remaining Accessions",
                "color": "#2a9d8f"
            },
            "Number of accessions included in the Multilateral System (MLS) (genebank collections databases)": {
                "selected_label": "Included in MLS (Genebank DBs)",
                "remaining_label": "Remaining Accessions",
                "color": "#2a9d8f"
            },
            "Number of accessions not included in the Multilateral System (MLS) (genebank collections databases)": {
                "selected_label": "Not Included in MLS (Genebank DBs)",
                "remaining_label": "Remaining Accessions",
                "color": "#e76f51"
            },
            "Number of accessions without information regarding inclusion in the Multilateral System (MLS) (genebank collections databases)": {
                "selected_label": "No MLS Information (Genebank DBs)",
                "remaining_label": "Remaining Accessions",
                "color": "#e9c46a"
            }
        }
        
        if selected_t4_metric == "Number of accessions with DOI (Plant Treaty GLIS 2025)":
            doi_pct_df = t4_sel_df.merge(tot_acc_t3, on="Crop", how="left")
            doi_pct_df["DOI Percentage"] = (
                (doi_pct_df["Number Cleaned"] / doi_pct_df["Total Accessions"] * 100)
                .fillna(0)
            )
            doi_pct_df = doi_pct_df.sort_values(by="DOI Percentage", ascending=True)
            
            fig_t4_crop = px.bar(
                doi_pct_df,
                x="DOI Percentage",
                y="Crop",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text=doi_pct_df["DOI Percentage"].apply(lambda v: f"{v:.1f}%"),
                hover_data={"Number Cleaned": ":,.0f", "Total Accessions": ":,.0f", "DOI Percentage": ":.2f%"},
                title="Crop Breakdown: Percentage of Accessions with DOI (%)",
                orientation="h",
                height=crop_chart_h
            )
            fig_t4_crop.update_traces(textposition="outside")
            fig_t4_crop.update_layout(
                xaxis_title="Percentage of Accessions with DOI (%)",
                xaxis_range=[0, max(100, doi_pct_df["DOI Percentage"].max() * 1.15 if not doi_pct_df.empty else 100)],
                yaxis_title="Crop",
                yaxis={"categoryorder": "total ascending"}
            )

            doi_total_df = t4_sel_df.sort_values(by="Number Cleaned", ascending=True)
            fig_t4_right = px.bar(
                doi_total_df,
                x="Number Cleaned",
                y="Crop",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text_auto=".2s",
                hover_data={"Number Cleaned": ":,.0f"},
                title="Crop Breakdown: Total Number of Accessions with DOI",
                orientation="h",
                height=crop_chart_h
            )
            fig_t4_right.update_layout(
                xaxis_title="Number of Accessions with DOI",
                yaxis_title="Crop",
                yaxis={"categoryorder": "total ascending"}
            )
        elif selected_t4_metric in mls_stacked_config:
            cfg = mls_stacked_config[selected_t4_metric]
            sel_label = cfg["selected_label"]
            rem_label = cfg["remaining_label"]
            
            mls_stack_df = t4_sel_df.merge(tot_acc_t3, on="Crop", how="left")
            mls_stack_df["Total Accessions"] = mls_stack_df["Total Accessions"].fillna(0)
            mls_stack_df[sel_label] = mls_stack_df[["Number Cleaned", "Total Accessions"]].min(axis=1)
            mls_stack_df[rem_label] = (mls_stack_df["Total Accessions"] - mls_stack_df[sel_label]).clip(lower=0)
            mls_stack_df = mls_stack_df.sort_values(by="Total Accessions", ascending=True)
            
            mls_melted = mls_stack_df.melt(
                id_vars=["Crop", "Crop Type", "Total Accessions"],
                value_vars=[sel_label, rem_label],
                var_name="MLS Status",
                value_name="Accessions"
            )
            
            fig_t4_crop = px.bar(
                mls_melted,
                x="Accessions",
                y="Crop",
                color="MLS Status",
                barmode="stack",
                color_discrete_map={
                    sel_label: cfg["color"],
                    rem_label: "#cbd5e1"
                },
                hover_data={"Total Accessions": ":,.0f", "Accessions": ":,.0f"},
                text_auto=".2s",
                title=f"Crop Breakdown: Total Accessions vs. {selected_t4_metric}",
                orientation="h",
                height=crop_chart_h
            )
            fig_t4_crop.update_layout(
                xaxis_title="Number of Accessions",
                yaxis_title="Crop",
                yaxis={"categoryorder": "total ascending"},
                legend_title="Status"
            )

            t4_cat_grp = t4_sel_df.groupby("Crop Type", as_index=False)["Number Cleaned"].sum()
            fig_t4_right = px.bar(
                t4_cat_grp,
                x="Number Cleaned",
                y="Crop Type",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text_auto=".2s",
                title=f"Category Aggregation: {selected_t4_metric}",
                orientation="h"
            )
            fig_t4_right.update_layout(
                xaxis_title="Aggregated Count",
                yaxis_title="Crop Category",
                yaxis={"categoryorder": "total ascending"},
                showlegend=False
            )
        else:
            t4_sel_df_sorted = t4_sel_df.sort_values(by="Number Cleaned", ascending=True)
            fig_t4_crop = px.bar(
                t4_sel_df_sorted,
                x="Number Cleaned",
                y="Crop",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text_auto=".2s",
                title=f"Crop Breakdown: {selected_t4_metric}",
                orientation="h",
                height=crop_chart_h
            )
            fig_t4_crop.update_layout(xaxis_title="Count", yaxis_title="Crop", yaxis={"categoryorder": "total ascending"})

            t4_cat_grp = t4_sel_df.groupby("Crop Type", as_index=False)["Number Cleaned"].sum()
            fig_t4_right = px.bar(
                t4_cat_grp,
                x="Number Cleaned",
                y="Crop Type",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text_auto=".2s",
                title=f"Category Aggregation: {selected_t4_metric}",
                orientation="h"
            )
            fig_t4_right.update_layout(
                xaxis_title="Aggregated Count",
                yaxis_title="Crop Category",
                yaxis={"categoryorder": "total ascending"},
                showlegend=False
            )

        if selected_t4_metric in mls_stacked_config:
            st.plotly_chart(fig_t4_crop, use_container_width=True)
            st.plotly_chart(fig_t4_right, use_container_width=True)
        else:
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.plotly_chart(fig_t4_crop, use_container_width=True)
            with col_m2:
                st.plotly_chart(fig_t4_right, use_container_width=True)

    with t4_subtab3:
        st.subheader("Filtered Policy & Governance Dataset")
        t4_display_cols = ["Crop", "Crop Type", "Metric", "Number Cleaned", "Percentage Cleaned"]
        st.dataframe(t4_final[t4_display_cols], use_container_width=True)
        csv_t4 = t4_final[t4_display_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Policy & Governance CSV",
            data=csv_t4,
            file_name="pgrfa_policy_governance.csv",
            mime="text/csv",
            key="dl_t4_subtab"
        )

# =============================================================================
# SECTION 6: Conservation Status & Safety
# =============================================================================
elif selected_section == "🛡️ Conservation Status & Safety":
    st.header("Conservation Status & Safety")
    
    t5_subtab1, t5_subtab2, t5_subtab3, t5_subtab4 = st.tabs([
        "🧬 Storage Conditions",
        "🌱 Regeneration Status (2014–2019)",
        "❄️ Safety Duplication",
        "📋 Filtered Conservation Status Data"
    ])
    
    tot_acc_t3_t5 = (
        t3_final[t3_final["Metric"] == "Total number of accessions in genebank collections"]
        [["Crop", "Number Cleaned"]]
        .rename(columns={"Number Cleaned": "Total Accessions"})
    )

    storage_mode_order = list(STORAGE_MODE_COLOR_MAP.keys())

    with t5_subtab1:
        st.subheader("Genebank Storage Modes & Seed Storage Conditions")
        
        general_storage_metrics = [
            "Number of accessions held in seed storage in genebank collections",
            "Number of accessions held in field storage in genebank collections",
            "Number of accessions held in in-vitro storage in genebank collections",
            "Number of accessions held in cryo storage in genebank collections",
            "Number of accessions held as DNA in genebank collections",
            "Number of accessions held in other storage in genebank collections",
            "Number of accessions not marked with a storage type in genebank collections"
        ]
        
        seed_duration_metrics = [
            "Number of accessions held in short-term seed storage in genebank collections",
            "Number of accessions held in medium-term seed storage in genebank collections",
            "Number of accessions held in long-term seed storage in genebank collections",
            "Number of accessions held in seed storage of undefined type in genebank collections"
        ]
        
        t5_gen_storage = t5_final[t5_final["Metric"].isin(general_storage_metrics)].copy()
        t5_gen_storage["Storage Mode"] = (
            t5_gen_storage["Metric"]
            .str.replace("Number of accessions held in ", "", regex=False)
            .str.replace("Number of accessions held as ", "", regex=False)
            .str.replace("Number of accessions ", "", regex=False)
            .str.replace(" in genebank collections", "", regex=False)
            .str.capitalize()
        )
        
        col_st1, col_st2 = st.columns(2)
        with col_st1:
            fig_gen_crop = px.bar(
                t5_gen_storage,
                x="Number Cleaned",
                y="Crop",
                color="Storage Mode",
                color_discrete_map=STORAGE_MODE_COLOR_MAP,
                category_orders={"Storage Mode": storage_mode_order},
                title="Storage Modes Breakdown per Crop",
                text_auto=".2s",
                barmode="stack",
                orientation="h",
                height=crop_chart_h
            )
            fig_gen_crop.update_layout(
                xaxis_title="Number of Accessions",
                yaxis_title="Crop",
                yaxis={"categoryorder": "total ascending"}
            )
            st.plotly_chart(fig_gen_crop, use_container_width=True)
            
        with col_st2:
            t5_gen_cat = t5_gen_storage.groupby(["Crop Type", "Storage Mode"], as_index=False)["Number Cleaned"].sum()
            fig_gen_cat = px.bar(
                t5_gen_cat,
                x="Number Cleaned",
                y="Crop Type",
                color="Storage Mode",
                color_discrete_map=STORAGE_MODE_COLOR_MAP,
                category_orders={"Storage Mode": storage_mode_order},
                title="Storage Modes Breakdown by Crop Category",
                text_auto=".2s",
                barmode="stack",
                orientation="h",
                height=crop_chart_h
            )
            fig_gen_cat.update_layout(
                xaxis_title="Accession Count",
                yaxis_title="Crop Category",
                yaxis={"categoryorder": "total ascending"}
            )
            st.plotly_chart(fig_gen_cat, use_container_width=True)
            
        st.divider()
        st.subheader("Seed Storage Sub-Types (Short-, Medium-, Long-Term & Undefined)")
        
        t5_seed_dur = t5_final[t5_final["Metric"].isin(seed_duration_metrics)].copy()
        t5_seed_dur["Seed Storage Type"] = (
            t5_seed_dur["Metric"]
            .str.replace("Number of accessions held in ", "", regex=False)
            .str.replace(" in genebank collections", "", regex=False)
            .str.capitalize()
        )
        
        col_sd1, col_sd2 = st.columns(2)
        with col_sd1:
            fig_seed_crop = px.bar(
                t5_seed_dur,
                x="Number Cleaned",
                y="Crop",
                color="Seed Storage Type",
                title="Seed Storage Conditions per Crop",
                text_auto=".2s",
                barmode="stack",
                orientation="h",
                height=crop_chart_h,
                color_discrete_sequence=["#e9c46a", "#52b788", "#1b4332", "#94a3b8"]
            )
            fig_seed_crop.update_layout(
                xaxis_title="Seed Accessions",
                yaxis_title="Crop",
                yaxis={"categoryorder": "total ascending"}
            )
            st.plotly_chart(fig_seed_crop, use_container_width=True)
            
        with col_sd2:
            t5_seed_cat = t5_seed_dur.groupby(["Crop Type", "Seed Storage Type"], as_index=False)["Number Cleaned"].sum()
            fig_seed_cat = px.bar(
                t5_seed_cat,
                x="Number Cleaned",
                y="Crop Type",
                color="Seed Storage Type",
                title="Seed Storage Conditions by Crop Category",
                text_auto=".2s",
                barmode="stack",
                orientation="h",
                height=crop_chart_h,
                color_discrete_sequence=["#e9c46a", "#52b788", "#1b4332", "#94a3b8"]
            )
            fig_seed_cat.update_layout(
                xaxis_title="Seed Accessions",
                yaxis_title="Crop Category",
                yaxis={"categoryorder": "total ascending"}
            )
            st.plotly_chart(fig_seed_cat, use_container_width=True)

    with t5_subtab2:
        st.subheader("Regeneration Activity, Backlog & Budget Gaps (2014–2019)")
        
        regen_metrics = [
            "Number of accessions in genebank collections regenerated 2014-2019",
            "Number of accessions in genebank collections in need of regeneration 2014-2019",
            "Number of accessions in genebank collections in need of regeneration without budget for regeneration 2014-2019"
        ]
        
        regen_label_map = {
            "Number of accessions in genebank collections regenerated 2014-2019": "Regenerated (2014–2019)",
            "Number of accessions in genebank collections in need of regeneration 2014-2019": "In Need of Regeneration",
            "Number of accessions in genebank collections in need of regeneration without budget for regeneration 2014-2019": "In Need (Without Budget)"
        }
        
        t5_regen = t5_final[t5_final["Metric"].isin(regen_metrics)].copy()
        t5_regen["Regeneration Status"] = t5_regen["Metric"].map(regen_label_map)
        
        col_rg1, col_rg2 = st.columns(2)
        with col_rg1:
            fig_regen_crop = px.bar(
                t5_regen,
                x="Number Cleaned",
                y="Crop",
                color="Regeneration Status",
                barmode="group",
                text_auto=".2s",
                title="Regeneration Progress & Budget Shortfalls per Crop",
                orientation="h",
                height=crop_chart_h,
                color_discrete_map={
                    "Regenerated (2014–2019)": "#2a9d8f",
                    "In Need of Regeneration": "#e9c46a",
                    "In Need (Without Budget)": "#e76f51"
                }
            )
            fig_regen_crop.update_layout(
                xaxis_title="Number of Accessions",
                yaxis_title="Crop",
                yaxis={"categoryorder": "total ascending"}
            )
            st.plotly_chart(fig_regen_crop, use_container_width=True)
            
        with col_rg2:
            t5_regen_cat = t5_regen.groupby(["Crop Type", "Regeneration Status"], as_index=False)["Number Cleaned"].sum()
            fig_regen_cat = px.bar(
                t5_regen_cat,
                x="Number Cleaned",
                y="Crop Type",
                color="Regeneration Status",
                barmode="group",
                text_auto=".2s",
                title="Regeneration Progress & Budget Shortfalls by Category",
                orientation="h",
                height=crop_chart_h,
                color_discrete_map={
                    "Regenerated (2014–2019)": "#2a9d8f",
                    "In Need of Regeneration": "#e9c46a",
                    "In Need (Without Budget)": "#e76f51"
                }
            )
            fig_regen_cat.update_layout(
                xaxis_title="Aggregated Accessions",
                yaxis_title="Crop Category",
                yaxis={"categoryorder": "total ascending"}
            )
            st.plotly_chart(fig_regen_cat, use_container_width=True)

    with t5_subtab3:
        st.subheader("Ex-Situ Safety Duplication (Out of Country & Svalbard Global Seed Vault)")
        
        safety_metrics = [
            "Number of accessions safety duplicated out of the country in genebank collections",
            "Number of accessions in genebank collections safety duplicated in Svalbard"
        ]
        
        selected_safety_metric = st.selectbox(
            "Select Safety Duplication Indicator:",
            options=safety_metrics,
            index=0
        )
        
        t5_safety_df = t5_final[t5_final["Metric"] == selected_safety_metric].copy()
        
        safety_label = (
            "Safety Duplicated Out of Country"
            if "out of the country" in selected_safety_metric
            else "Safety Duplicated in Svalbard"
        )
        safety_color = "#2a9d8f" if "out of the country" in selected_safety_metric else "#457b9d"
        
        safety_stack_df = t5_safety_df.merge(tot_acc_t3_t5, on="Crop", how="left")
        safety_stack_df["Total Accessions"] = safety_stack_df["Total Accessions"].fillna(0)
        safety_stack_df[safety_label] = safety_stack_df[["Number Cleaned", "Total Accessions"]].min(axis=1)
        safety_stack_df["Not Safety Duplicated / Unreported"] = (
            safety_stack_df["Total Accessions"] - safety_stack_df[safety_label]
        ).clip(lower=0)
        safety_stack_df = safety_stack_df.sort_values(by="Total Accessions", ascending=True)
        
        safety_melted = safety_stack_df.melt(
            id_vars=["Crop", "Crop Type", "Total Accessions"],
            value_vars=[safety_label, "Not Safety Duplicated / Unreported"],
            var_name="Duplication Status",
            value_name="Accessions"
        )
        
        fig_safety_crop = px.bar(
            safety_melted,
            x="Accessions",
            y="Crop",
            color="Duplication Status",
            barmode="stack",
            color_discrete_map={
                safety_label: safety_color,
                "Not Safety Duplicated / Unreported": "#cbd5e1"
            },
            hover_data={"Total Accessions": ":,.0f", "Accessions": ":,.0f"},
            text_auto=".2s",
            title=f"Crop Breakdown: Total Accessions vs. {selected_safety_metric}",
            orientation="h",
            height=crop_chart_h
        )
        fig_safety_crop.update_layout(
            xaxis_title="Number of Accessions",
            yaxis_title="Crop",
            yaxis={"categoryorder": "total ascending"},
            legend_title="Status"
        )
        st.plotly_chart(fig_safety_crop, use_container_width=True)
        
        t5_safety_cat = t5_safety_df.groupby("Crop Type", as_index=False)["Number Cleaned"].sum()
        fig_safety_cat = px.bar(
            t5_safety_cat,
            x="Number Cleaned",
            y="Crop Type",
            color="Crop Type",
            color_discrete_map=TYPE_COLOR_MAP,
            text_auto=".2s",
            title=f"Category Aggregation: {selected_safety_metric}",
            orientation="h"
        )
        fig_safety_cat.update_layout(
            xaxis_title="Aggregated Accessions",
            yaxis_title="Crop Category",
            yaxis={"categoryorder": "total ascending"},
            showlegend=False
        )
        st.plotly_chart(fig_safety_cat, use_container_width=True)

    with t5_subtab4:
        st.subheader("Filtered Conservation Status Dataset")
        t5_display_cols = ["Crop", "Crop Type", "Metric", "Number Cleaned", "Percentage Cleaned"]
        st.dataframe(t5_final[t5_display_cols], use_container_width=True)
        csv_t5 = t5_final[t5_display_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Conservation Status CSV",
            data=csv_t5,
            file_name="pgrfa_conservation_safety.csv",
            mime="text/csv",
            key="dl_t5_subtab"
        )

# =============================================================================
# SECTION 7: Documentation, Information Systems & Research Resources
# =============================================================================
elif selected_section == "📚 Documentation, Info Systems & Research":
    st.header("Documentation, Information Systems, and Research Resources")
    
    t6_subtab1, t6_subtab2, t6_subtab3, t6_subtab4 = st.tabs([
        "🗂️ Passport Data & GBIF Records",
        "🧬 Genomic Resources (NCBI Entrez)",
        "📖 Scientific Publications",
        "📋 Filtered Documentation & Research Data"
    ])

    with t6_subtab1:
        st.subheader("Passport Data Completeness Index & GBIF Occurrence Records")
        
        passport_metric = "Passport data completeness index (range 0-10) as a median value across accessions in genebank collections"
        gbif_metric = "Number of research materials as recorded in GBIF (2025)"
        
        col_doc1, col_doc2 = st.columns(2)
        with col_doc1:
            t6_passport = t6_final[t6_final["Metric"] == passport_metric].sort_values(by="Number Cleaned", ascending=True)
            fig_passport_crop = px.bar(
                t6_passport,
                x="Number Cleaned",
                y="Crop",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text=t6_passport["Number Cleaned"].apply(lambda v: f"{v:.1f}"),
                title="Median Passport Data Completeness Index (0–10) per Crop",
                orientation="h",
                height=crop_chart_h
            )
            fig_passport_crop.update_traces(textposition="outside")
            fig_passport_crop.update_layout(
                xaxis_title="Completeness Index (0 to 10)",
                xaxis_range=[0, 10.8],
                yaxis_title="Crop",
                yaxis={"categoryorder": "total ascending"}
            )
            st.plotly_chart(fig_passport_crop, use_container_width=True)
            
        with col_doc2:
            t6_passport_cat = t6_passport.groupby("Crop Type", as_index=False)["Number Cleaned"].mean().sort_values(by="Number Cleaned", ascending=True)
            fig_passport_cat = px.bar(
                t6_passport_cat,
                x="Number Cleaned",
                y="Crop Type",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text=t6_passport_cat["Number Cleaned"].apply(lambda v: f"{v:.2f}"),
                title="Average Passport Data Completeness Index by Category",
                orientation="h",
                height=crop_chart_h
            )
            fig_passport_cat.update_traces(textposition="outside")
            fig_passport_cat.update_layout(
                xaxis_title="Mean Completeness Index (0 to 10)",
                xaxis_range=[0, 10.8],
                yaxis_title="Crop Category",
                yaxis={"categoryorder": "total ascending"},
                showlegend=False
            )
            st.plotly_chart(fig_passport_cat, use_container_width=True)
            
        st.divider()
        st.subheader("Research Materials Recorded in GBIF (2025)")
        
        col_gb1, col_gb2 = st.columns(2)
        with col_gb1:
            t6_gbif = t6_final[t6_final["Metric"] == gbif_metric].sort_values(by="Number Cleaned", ascending=True)
            fig_gbif_crop = px.bar(
                t6_gbif,
                x="Number Cleaned",
                y="Crop",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text_auto=".2s",
                title="GBIF Research Materials per Crop (2025)",
                orientation="h",
                height=crop_chart_h
            )
            fig_gbif_crop.update_layout(
                xaxis_title="Number of Research Materials",
                yaxis_title="Crop",
                yaxis={"categoryorder": "total ascending"}
            )
            st.plotly_chart(fig_gbif_crop, use_container_width=True)
            
        with col_gb2:
            t6_gbif_cat = t6_gbif.groupby("Crop Type", as_index=False)["Number Cleaned"].sum().sort_values(by="Number Cleaned", ascending=True)
            fig_gbif_cat = px.bar(
                t6_gbif_cat,
                x="Number Cleaned",
                y="Crop Type",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text_auto=".2s",
                title="Aggregated GBIF Research Materials by Category (2025)",
                orientation="h",
                height=crop_chart_h
            )
            fig_gbif_cat.update_layout(
                xaxis_title="Aggregated Research Materials",
                yaxis_title="Crop Category",
                yaxis={"categoryorder": "total ascending"},
                showlegend=False
            )
            st.plotly_chart(fig_gbif_cat, use_container_width=True)

    with t6_subtab2:
        st.subheader("Genomic & Molecular Sequence Resources (NCBI Entrez, 2022)")
        
        ncbi_metrics = [
            "Number of genes as recorded in NCBI's Entrez database as of 2022",
            "Number of genomes as recorded in NCBI's Entrez database as of 2022",
            "Number of nucleotides as recorded in NCBI's Entrez database as of 2022",
            "Number of proteins as recorded in NCBI's Entrez database as of 2022"
        ]
        
        selected_ncbi_metric = st.selectbox(
            "Select NCBI Entrez Sequence Indicator:",
            options=ncbi_metrics,
            index=0
        )
        
        t6_ncbi_df = t6_final[t6_final["Metric"] == selected_ncbi_metric].sort_values(by="Number Cleaned", ascending=True)
        
        col_nc1, col_nc2 = st.columns(2)
        with col_nc1:
            fig_ncbi_crop = px.bar(
                t6_ncbi_df,
                x="Number Cleaned",
                y="Crop",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text_auto=".2s",
                title=f"Crop Breakdown: {selected_ncbi_metric}",
                orientation="h",
                height=crop_chart_h
            )
            fig_ncbi_crop.update_layout(
                xaxis_title="Count",
                yaxis_title="Crop",
                yaxis={"categoryorder": "total ascending"}
            )
            st.plotly_chart(fig_ncbi_crop, use_container_width=True)
            
        with col_nc2:
            t6_ncbi_cat = t6_ncbi_df.groupby("Crop Type", as_index=False)["Number Cleaned"].sum().sort_values(by="Number Cleaned", ascending=True)
            fig_ncbi_cat = px.bar(
                t6_ncbi_cat,
                x="Number Cleaned",
                y="Crop Type",
                color="Crop Type",
                color_discrete_map=TYPE_COLOR_MAP,
                text_auto=".2s",
                title=f"Category Aggregation: {selected_ncbi_metric}",
                orientation="h",
                height=crop_chart_h
            )
            fig_ncbi_cat.update_layout(
                xaxis_title="Aggregated Count",
                yaxis_title="Crop Category",
                yaxis={"categoryorder": "total ascending"},
                showlegend=False
            )
            st.plotly_chart(fig_ncbi_cat, use_container_width=True)

    with t6_subtab3:
        st.subheader("Scientific Literature Coverage (Google Scholar & PubMed Central)")
        
        pub_metrics = [
            "Number of publications listed in Google Scholar with taxon name in title published between 2009 and 2019",
            "Number of publications listed in PubMed Central with taxon name in text as of 2022"
        ]
        
        pub_label_map = {
            "Number of publications listed in Google Scholar with taxon name in title published between 2009 and 2019": "Google Scholar (2009–2019, Title)",
            "Number of publications listed in PubMed Central with taxon name in text as of 2022": "PubMed Central (as of 2022, Text)"
        }
        
        t6_pub = t6_final[t6_final["Metric"].isin(pub_metrics)].copy()
        t6_pub["Publication Source"] = t6_pub["Metric"].map(pub_label_map)
        
        col_pb1, col_pb2 = st.columns(2)
        with col_pb1:
            fig_pub_crop = px.bar(
                t6_pub,
                x="Number Cleaned",
                y="Crop",
                color="Publication Source",
                barmode="group",
                text_auto=".2s",
                title="Scientific Publications per Crop",
                orientation="h",
                height=crop_chart_h,
                color_discrete_map={
                    "Google Scholar (2009–2019, Title)": "#e9c46a",
                    "PubMed Central (as of 2022, Text)": "#2a9d8f"
                }
            )
            fig_pub_crop.update_layout(
                xaxis_title="Number of Publications",
                yaxis_title="Crop",
                yaxis={"categoryorder": "total ascending"}
            )
            st.plotly_chart(fig_pub_crop, use_container_width=True)
            
        with col_pb2:
            t6_pub_cat = t6_pub.groupby(["Crop Type", "Publication Source"], as_index=False)["Number Cleaned"].sum()
            fig_pub_cat = px.bar(
                t6_pub_cat,
                x="Number Cleaned",
                y="Crop Type",
                color="Publication Source",
                barmode="group",
                text_auto=".2s",
                title="Scientific Publications by Crop Category",
                orientation="h",
                height=crop_chart_h,
                color_discrete_map={
                    "Google Scholar (2009–2019, Title)": "#e9c46a",
                    "PubMed Central (as of 2022, Text)": "#2a9d8f"
                }
            )
            fig_pub_cat.update_layout(
                xaxis_title="Aggregated Publications",
                yaxis_title="Crop Category",
                yaxis={"categoryorder": "total ascending"}
            )
            st.plotly_chart(fig_pub_cat, use_container_width=True)

    with t6_subtab4:
        st.subheader("Filtered Documentation & Research Dataset")
        t6_display_cols = ["Crop", "Crop Type", "Metric", "Number Cleaned"]
        st.dataframe(t6_final[t6_display_cols], use_container_width=True)
        csv_t6 = t6_final[t6_display_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Documentation & Research CSV",
            data=csv_t6,
            file_name="pgrfa_documentation_research.csv",
            mime="text/csv",
            key="dl_t6_subtab"
        )

# =============================================================================
# SECTION 8: Data Explorer
# =============================================================================
elif selected_section == "📋 Raw Data Explorer":
    st.header("Raw Dataset Directory")
    
    st.subheader("Production and Trade Data")
    st.dataframe(t1_final, use_container_width=True)
    
    st.divider()
    
    st.subheader("Genebank Holdings Data")
    st.dataframe(t2_final, use_container_width=True)
    
    st.divider()
    
    st.subheader("Taxa Conserved in Genebanks Data")
    st.dataframe(si_t2_final, use_container_width=True)
    
    st.divider()
    
    st.subheader("Accession Diversity Data")
    st.dataframe(t3_final, use_container_width=True)
    
    st.divider()
    
    st.subheader("Policy & Governance Data")
    st.dataframe(t4_final, use_container_width=True)
    
    st.divider()
    
    st.subheader("Conservation Status & Safety Data")
    st.dataframe(t5_final, use_container_width=True)
    
    st.divider()
    
    st.subheader("Documentation, Info Systems & Research Data")
    st.dataframe(t6_final, use_container_width=True)
    
    col_d1, col_d2, col_d3, col_d4, col_d5, col_d6 = st.columns(6)
    with col_d1:
        csv_t2 = t2_final.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Genebank Holdings CSV",
            data=csv_t2,
            file_name="pgrfa_genebank_holdings.csv",
            mime="text/csv",
            key="dl_t2_explorer"
        )
    with col_d2:
        csv_si2_exp = si_t2_final.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Conserved Taxa CSV",
            data=csv_si2_exp,
            file_name="pgrfa_conserved_taxa.csv",
            mime="text/csv",
            key="dl_si2_explorer"
        )
    with col_d3:
        csv_t3 = t3_final.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Accession Diversity CSV",
            data=csv_t3,
            file_name="pgrfa_accession_diversity.csv",
            mime="text/csv",
            key="dl_t3_explorer"
        )
    with col_d4:
        csv_t4 = t4_final.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Policy & Governance CSV",
            data=csv_t4,
            file_name="pgrfa_policy_governance.csv",
            mime="text/csv",
            key="dl_t4_explorer"
        )
    with col_d5:
        csv_t5_exp = t5_final.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Conservation Status CSV",
            data=csv_t5_exp,
            file_name="pgrfa_conservation_safety.csv",
            mime="text/csv",
            key="dl_t5_explorer"
        )
    with col_d6:
        csv_t6_exp = t6_final.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Documentation & Research CSV",
            data=csv_t6_exp,
            file_name="pgrfa_documentation_research.csv",
            mime="text/csv",
            key="dl_t6_explorer"
        )

# =============================================================================
# SECTION 9: Methods and Data Sources
# =============================================================================
elif selected_section == "📖 Methods and data sources":
    st.header("Methods and data sources")
    st.markdown(
        """
        **Primary Data Sources**
        * [Genesys](https://www.genesys-pgr.org/)
        * World Information and Early Warning System on Plant Genetic Resources for Food and Agriculture of the Food and Agriculture Organization of the United Nations ([FAO WIEWS](https://www.fao.org/wiews/))
        * Botanic Gardens Conservation International PlantSearch database ([BGCI PlantSearch](https://plantsearch.bgci.org/))
        * Global Information System of the International Treaty on Plant Genetic Resources for Food and Agriculture ([Plant Treaty GLIS](https://ssl.fao.org/glis/))
        * Data Store of the International Treaty on Plant Genetic Resources for Food and Agriculture ([Plant Treaty Data Store](https://mls.planttreaty.org/itt/))
        * Svalbard Global Seed Vault portal ([SGSV portal](https://seedvault.nordgen.org/))
        * International Union for the Protection of New Varieties of Plants ([UPOV](https://www.upov.int/)) PLUTO database
        * [FAOSTAT](https://www.fao.org/faostat/en/#data)
        * National Center for Biotechnology Information’s Entrez database ([NCBI Entrez](https://www.ncbi.nlm.nih.gov/Web/Search/entrezfs.html))
        * [Google Scholar](https://scholar.google.com/)
        * [PubMed Central](https://pmc.ncbi.nlm.nih.gov/)
        * [Wikipedia](https://www.wikipedia.org/)
        * Global Biodiversity Information Facility ([GBIF](https://www.gbif.org/))

        **Literature & Supplementary Databases**
        * Some of these data were acquired from literature/databases including [Khoury et al. (2023)](https://www.fao.org/documents/card/en/c/cc6876en) and [Khoury et al. (2025)](https://doi.org/10.4060/cd4850en).

        **Data Processing & Code**
        * Data processing, metric calculation, and table generation were conducted in R, with code available on this [GitLab repository](https://gitlab.com/GlobalCropDiversityTrust/pgrfa-metrics).
        * Extended methods are available [here](https://www.croptrust.org/fileadmin/uploads/croptrust/Documents/GCCS_Summaries/GCCS_metrics_methods.pdf/).
        """
    )
# -----------------------------------------------------------------------------
# Footer Disclaimer (at the very bottom of the script)
# -----------------------------------------------------------------------------

st.divider()
st.markdown(
    """
    <div class="ct-footer-box">
        <p><span class="ct-footer-heading">Crop Trust</span><br>
        Platz der Vereinten Nationen 7, 53113 Bonn, Germany<br>
        General Contact: +49 (0) 228 85427 118 | <a href="mailto:info@croptrust.org">info@croptrust.org</a></p>
        <p><span class="ct-footer-heading">Copyright:</span> © 2025 Global Crop Diversity Trust.</p>
        <p><span class="ct-footer-heading">Disclaimer:</span> Data presented in this dashboard reflect information retrieved and analyzed in 2025. For current figures, please refer directly to the primary sources listed in <em>Methods and data sources</em>.</p>
        <p><span class="ct-footer-heading">Permission to Use:</span> This publication may be reproduced in whole or in part, and in any form, for educational or non-profit purposes without special permission from the copyright holder, provided that the source is acknowledged. No use of this publication may be made for resale or for any other commercial purpose without prior written permission from the Global Crop Diversity Trust.
        Except as otherwise expressly indicated, all text, charts, and tabular content contained in this document are licensed under the Creative Commons Attribution–NonCommercial–ShareAlike (CC BY-NC-SA) license.</p>
        <p><span class="ct-footer-heading">Suggested Citation:</span> Giovannini, P (2026) <em>PGRFA Conservation and Use Metrics Dashboard</em>. Bonn, Germany: Global Crop Diversity Trust. URL: to be added here</p>
        <p><span class="ct-footer-heading">Acknowledgements:</span> The metrics shown in this dashboard were developed as part of the project <em>Mainstreaming Global Crop Conservation Strategies in Plant Treaty Processes</em>, led by the Crop Trust and funded by the German Federal Ministry of Agriculture, Food and Regional Identity (BMLEH).</p>
    </div>
    """,
    unsafe_allow_html=True
)
