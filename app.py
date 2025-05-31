import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="SCRIM Difference Filter", layout="wide")

# --- Sidebar Styling ---
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Content ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Logo_placeholder.svg/600px-Logo_placeholder.svg.png", width=150)
    st.markdown("## 🔧 Input Options")
    st.markdown("Choose how you'd like to provide Link section data.")
    input_method = st.radio("📥 Select Input Method", ["📝 Manual Entry", "📂 Excel Entry"])

    with st.expander("ℹ️ Instructions"):
        st.write("""
        1. Select input method (Manual or Excel).
        2. Upload the dataset file.
        3. Enter or upload Link section values.
        4. Click **Analyze** to filter rows with negative SCRIM Difference.
        """)

# --- Main App ---
st.title("📊 SCRIM Difference Filter App")

# Upload dataset file (common to both modes)
dataset_file = st.file_uploader("📄 Upload Dataset Excel File", type=["xlsx", "xls"])

# Initialize link_sections
link_sections = []

# Manual Entry Mode
if "Manual" in input_method:
    manual_input = st.text_area("✍️ Enter Link section values (one per line):")
    if manual_input:
        link_sections = [line.strip() for line in manual_input.splitlines() if line.strip()]

# Excel Entry Mode
elif "Excel" in input_method:
    input_file = st.file_uploader("📂 Upload Excel file with Link Section Numbers", type=["xlsx", "xls"])
    if input_file:
        try:
            input_df = pd.read_excel(input_file)
            if 'Link section' not in input_df.columns:
                st.error("❌ Input file must contain a 'Link section' column.")
            else:
                link_sections = input_df['Link section'].dropna().unique()
        except Exception as e:
            st.error(f"❌ Error reading input file: {e}")

# Analyze button
if st.button("🚀 Analyze"):
    if dataset_file and link_sections:
        try:
            dataset_df = pd.read_excel(dataset_file)

            required_cols = ['Link section', 'Lane', 'Start Chainage', 'End Chainage', 'SCRIM Difference']
            if not all(col in dataset_df.columns for col in required_cols):
                st.error(f"❌ Dataset file must contain the following columns: {', '.join(required_cols)}")
            else:
                # Filter dataset
                filtered_df = dataset_df[
                    (dataset_df['Link section'].isin(link_sections)) &
                    (dataset_df['SCRIM Difference'] < 0)
                ]

                st.success(f"✅ Found {len(filtered_df)} rows with negative SCRIM Difference.")

                # Display grouped results
                for link, group in filtered_df.groupby('Link section'):
                    with st.expander(f"🔗 Link Section: {link} ({len(group)} rows)"):
                        st.dataframe(group)

                # Download button
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Filtered Data as CSV", csv, "filtered_data.csv", "text/csv")

        except Exception as e:
            st.error(f"❌ Error processing dataset file: {e}")
    else:
        st.warning("⚠️ Please provide both dataset file and Link section values before analyzing.")
