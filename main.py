import streamlit as st
import pandas as pd
from rapidfuzz import fuzz
from urllib.parse import urlparse
from io import BytesIO


# Function to extract the path from the URL (everything after the domain)
def extract_path(url):
    return urlparse(url).path

# Function to calculate similarity using RapidFuzz, ignoring case
def similarity(a, b):
    return fuzz.ratio(str(a).lower(), str(b).lower())

# Function to perform matching and return results
def match_urls(old_data, new_data):
    # Apply path extraction
    old_data['Old_Path'] = old_data['URL'].apply(extract_path)
    new_data['New_Path'] = new_data['URL'].apply(extract_path)

    # Perform matching based on path similarity and H1 similarity
    matched_urls = []

    for _, old_row in old_data.iterrows():
        old_path = old_row['Old_Path']
        full_old_url = old_row['URL']  # Keep the full old URL

        best_match = None
        best_similarity = 0

        for _, new_row in new_data.iterrows():
            new_path = new_row['New_Path']
            new_h1 = new_row['H1']

            # Compare paths ignoring case
            path_similarity = similarity(old_path, new_path)

            # Compare H1 from New.xlsx with Old URL path
            h1_similarity = similarity(old_path, new_h1) if pd.notnull(new_h1) else 0

            # Calculate the total similarity, giving weights to path and H1
            total_similarity = (path_similarity * 0.7) + (h1_similarity * 0.3)

            if total_similarity > best_similarity:
                best_similarity = total_similarity
                best_match = new_row['URL']

        matched_urls.append({
            'Old_URL': full_old_url,  # Output full old URL
            'Best_Match_New_URL': best_match,
            'Similarity_Score': best_similarity
        })

    return pd.DataFrame(matched_urls)

# Sidebar for additional information
st.sidebar.image("https://coalitiontechnologies.com/headless/assets/images/logo.svg", use_column_width=True)  # Add logo image

# Streamlit UI setup
st.title("4xx Redirects V2")

# Sidebar for additional information
st.sidebar.title("4xx Redirects V2 (BigC-URL path)")
st.sidebar.info("""

This script is designed to automate the process of suggesting redirects by matching old URLs (resulting in 4xx errors) with live URLs from an XML sitemap crawl based on the similarity of the URL paths and H1 tags.

**Files Used:**
- **Old.xlsx**: This Excel file represents the list of old URLs that result in 4xx errors. It contains one column: URL.
- **New.xlsx**: This Excel file represents the live URLs crawled from the XML sitemap, including the H1 tags for each URL. It contains two columns: URL and H1.

**Purpose:**
The script compares the URL paths from Old.xlsx with the paths from New.xlsx, and takes into account the similarity between the old path and the H1 tag from New.xlsx. It suggests the best matching live URL with a similarity score.

**Steps:**
1. Loading the Data (Old.xlsx, New.xlsx)
2. Extracting URL paths
3. Similarity Matching (Paths and H1)
4. Generating Redirect Suggestions
5. Exporting Results to Excel (output.xlsx)

""")

# Upload files
old_file = st.file_uploader("Upload Old.xlsx", type=["xlsx"])
new_file = st.file_uploader("Upload New.xlsx", type=["xlsx"])

if old_file and new_file:
    # Read uploaded Excel files
    old_data = pd.read_excel(old_file)
    new_data = pd.read_excel(new_file)

    # Rename columns to match the script
    old_data.columns = ['URL']
    new_data.columns = ['URL', 'H1']

    # Perform matching
    matched_df = match_urls(old_data, new_data)

    # Display the matched results
    st.write("Matched Results:")
    st.dataframe(matched_df)

    # Provide download link for the output file
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        matched_df.to_excel(writer, index=False)

    output.seek(0)
    st.download_button(
        label="Download Matched Results as Excel",
        data=output,
        file_name="matched_urls.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
