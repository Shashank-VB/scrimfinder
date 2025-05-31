import streamlit as st
import pandas as pd

st.title("SCRIM Difference Filter App")

# Upload input file with Link section numbers
input_file = st.file_uploader("Upload Excel file with Link Section Numbers", type=["xlsx", "xls"])

# Upload dataset file
dataset_file = st.file_uploader("Upload Dataset Excel File", type=["xlsx", "xls"])

# Add an Analyze button
if st.button("Analyze"):
    if input_file and dataset_file:
        try:
            # Read both files
            input_df = pd.read_excel(input_file)
            dataset_df = pd.read_excel(dataset_file)

            # Check for required columns
            if 'Link section' not in input_df.columns:
                st.error("Input file must contain a 'Link section' column.")
            elif not all(col in dataset_df.columns for col in ['Link section', 'Lane', 'Start Chainage', 'End Chainage', 'SCRIM Difference']):
                st.error("Dataset file must contain 'Link section', 'Lane', 'Start Chainage', 'End Chainage', and 'SCRIM Difference' columns.")
            else:
                # Filter dataset
                link_sections = input_df['Link section'].unique()
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
            st.error(f"Error processing files: {e}")
    else:
        st.warning("Please upload both input and dataset files before clicking Analyze.")
