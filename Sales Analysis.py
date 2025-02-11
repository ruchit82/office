import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load and analyze Excel data
def analyze_excel_data(file_path):
    try:
        # Load data
        data = pd.read_excel(file_path)
        st.write("### Preview of the Data")
        st.write(data.head(10))

        # Display unique categories before deletion
        unique_categories_before = data['CATEGORY'].unique()
        st.write("### Unique Categories Before Deletion")
        st.write(unique_categories_before)

        # Filter data
        df = data[~data['CATEGORY'].isin(['ST', 'LOOSE PCS', 'PARA BIDS', 'Langadi', 'PROCESS LOSS', 'SCRAP PCC', 'BALL CHAIN', 'SIGNING TAR', 'Fine'])]

        # Display filtered data
        st.write("### Data After Deleting Specific Categories")
        st.write(df)

        # Display unique categories after deletion
        unique_categories_after = df['CATEGORY'].unique()
        st.write("### Unique Categories After Deletion")
        st.write(unique_categories_after)

        # Check for required columns
        required_columns = ['DocDate', 'type', 'parName', 'CATEGORY', 'weight', 'noPcs']
        if not all(col in data.columns for col in required_columns):
            st.error(f"The dataset must contain these columns: {required_columns}")
        else:
            # Party weight summary
            party_weight_summary = df.groupby('parName')['weight'].sum().reset_index()
            top_10_parties = party_weight_summary.sort_values(by='weight', ascending=False).head(10)
            bottom_5_parties = party_weight_summary.sort_values(by='weight', ascending=True).head(5)

            st.write("### Bottom 5 Parties by Weight")
            st.write(bottom_5_parties)

            st.write("### Top 10 Parties by Weight")
            st.write(top_10_parties)

            # Category-wise summary
            category_summary = df.groupby('CATEGORY').agg({
                'weight': 'sum',
                'noPcs': 'sum'
            }).reset_index()

            # Top 10 categories by weight
            top_10_categories = category_summary.sort_values(by='weight', ascending=False).head(10)
            st.write("### Top 10 Categories by Weight")
            st.write(top_10_categories)

            # Bottom 5 categories by weight
            bottom_5_categories = category_summary.sort_values(by='weight', ascending=True).head(5)
            st.write("### Bottom 5 Categories by Weight")
            st.write(bottom_5_categories)

            # Category-wise summary output
            st.write("### Category-wise Summary")
            st.write(category_summary)

            # Bar Plot: Top 10 Parties by Weight
            st.write("### Bar Plot: Top 10 Parties by Weight")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='weight', y='parName', data=top_10_parties, palette='Blues_r', ax=ax)
            ax.set_title('Top 10 Parties by Weight')
            st.pyplot(fig)

            # Bar Plot: Bottom 5 Parties by Weight
            st.write("### Bar Plot: Bottom 5 Parties by Weight")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='weight', y='parName', data=bottom_5_parties, palette='Reds_r', ax=ax)
            ax.set_title('Bottom 5 Parties by Weight')
            st.pyplot(fig)

            # Bar Plot: Top 10 Categories by Weight
            st.write("### Bar Plot: Top 10 Categories by Weight")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='weight', y='CATEGORY', data=top_10_categories, palette='Greens_r', ax=ax)
            ax.set_title('Top 10 Categories by Weight')
            st.pyplot(fig)

            # Bar Plot: Bottom 5 Categories by Weight
            st.write("### Bar Plot: Bottom 5 Categories by Weight")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='weight', y='CATEGORY', data=bottom_5_categories, palette='Oranges_r', ax=ax)
            ax.set_title('Bottom 5 Categories by Weight')
            st.pyplot(fig)

          
                  

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")

# Streamlit app
st.title("Excel Data Analysis App")
file_path = st.text_input("Please enter the file path to your Excel file:")
if file_path:
    analyze_excel_data(file_path)
