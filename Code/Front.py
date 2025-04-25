import streamlit as st
import pandas as pd
import re
import io

# Streamlit App Title
st.title("📄 Name and Phone Number Extractor App")

# Step 1: File uploader
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Step 2: Read the uploaded file
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)

    # Step 3: Extract Particulars (Name) and Address
    particulars = data.get('Particulars')  # Use .get() to avoid KeyError
    addresses = data.get('Address')

    if particulars is not None and addresses is not None:
        
        # Step 4: Clean the Particulars
        def clean_particulars(name):
            if pd.isna(name):
                return None
            name = name.strip()
            name = re.sub(r'^(BFL|IDFC)\s+', '', name, flags=re.I)
            name = re.sub(r'\s+(BFL|IDFC)$', '', name, flags=re.I)
            return name.strip()

        cleaned_particulars = particulars.apply(clean_particulars)

        # Step 5: Extract Phone Number
        def extract_phone(address):
            if pd.isna(address):
                return None
            match = re.search(r'\b\d{10}\b', address)
            return match.group(0) if match else None

        phone_numbers = addresses.apply(extract_phone)

        # Step 6: Create final cleaned DataFrame
        final_data = pd.DataFrame({
            'Particulars': cleaned_particulars,
            'Phone Number': phone_numbers
        })

        final_data = final_data.dropna(subset=['Phone Number'])
        final_data = final_data.sort_values(by='Particulars')

        # Step 7: Show cleaned data
        st.success("✅ Processed Successfully!")
        st.dataframe(final_data)

        # Step 8: Prepare for download
        csv_buffer = io.StringIO()
        final_data.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        # Step 9: Download button
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv_data,
            file_name='Cleaned_Customer_Phone_Numbers.csv',
            mime='text/csv'
        )

    else:
        st.error("❌ Your file must have 'Particulars' and 'Address' columns.")

else:
    st.info("⬆️ Please upload a CSV or Excel file to begin.")
