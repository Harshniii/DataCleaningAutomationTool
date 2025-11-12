import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Data Cleaning Automation Tool", page_icon="🧹", layout="wide")

st.title("🧹 Data Cleaning Automation Tool")
st.write("Upload a CSV file to automatically handle **missing values**, **remove outliers**, and **fix inconsistencies**.")

# File uploader
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

def clean_data(df):
    st.subheader("🔍 Cleaning in Progress...")
    st.write("1️⃣ Handling missing values...")
    df.fillna(df.median(numeric_only=True), inplace=True)
    df.fillna(df.mode().iloc[0], inplace=True)

    st.write("2️⃣ Removing outliers using IQR method...")
    for col in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    st.write("3️⃣ Fixing inconsistencies in categorical data...")
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip().str.lower().replace({
            'm': 'male', 'f': 'female', 'malee': 'male', 'fem': 'female'
        })
    return df

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Original Data Preview")
    st.dataframe(df.head())

    if st.button("🚀 Clean Data"):
        cleaned_df = clean_data(df.copy())
        st.success("✅ Data Cleaning Completed!")
        st.subheader("🧾 Cleaned Data Preview")
        st.dataframe(cleaned_df.head())

        # Download cleaned data
        csv = cleaned_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Download Cleaned CSV",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv",
        )

else:
    st.info("Please upload a CSV file to start cleaning.")
