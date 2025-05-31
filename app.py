import streamlit as st
import pandas as pd

st.title("SCRIM Difference Filter App")

# Sidebar option for input method
input_method = st.sidebar.radio("Select Input Method", ["Manual Entry", "Excel Entry"])

# Upload dataset file (common to both modes)
dataset_file = st.file_uploader("Upload Dataset Excel File", type=["xlsx", "xls"])

# Initialize link_sections
link_sections = []

# Manual Entry Mode
if input_method == "Manual Entry":
    manual_input = st.text_area("Enter Link section values (one per line):")
    if manual_input:
        link_sections = [line.strip() for line in manual_input.splitlines() if line.strip()]

# Excel Entry Mode
elif input_method == "Excel Entry":
    input_file = st.file_uploader("Upload Excel file with Link Section Numbers", type=["xlsx", "xls"])
    if input_file:
        try:
            input_df = pd.read_excel(input_file)
            if 'Link section' not in input_df.columns:
                st.error("Input file must contain a 'Link section' column.")
            else:
                link_sections = input_df['Link section'].dropna().unique()
        except Exception as e:
            st.error(f"Error reading input file: {e}")

# Analyze button
if st.button("Analyze"):
    if dataset_file and link_sections:
        try:
            dataset_df = pd.read_excel(dataset_file)

            required_cols = ['Link section', 'Lane', 'Start Chainage', 'End Chainage', 'SCRIM Difference']
            if not all(col in dataset_df.columns for col in required_cols):
                st.error(f"Dataset file must contain the following columns: {', '.join(required_cols)}")
            else:
                # Filter dataset
                filtered_df = dataset_df[
                    (dataset_df['Link section'].isin(link_sections)) &
                    (dataset_df['SCRIM Difference'] < 0)
                ]

                st.subheader("Filtered Results (Negative SCRIM Difference)")
                st.dataframe(filtered_df)

                # Option to download the filtered data
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Filtered Data as CSV", csv, "filtered_data.csv", "text/csv")

        except Exception as e:
            st.error(f"Error processing dataset file: {e}")
    else:
        st.warning("Please provide both dataset file and Link section values before analyzing.")

