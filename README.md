# 4xx-v2
4xx Redirect Automation (Version 2 - for BigCommerce to use the URL path)

# Automating 4xx Redirect Suggestions using Python

This script is designed to automate the process of suggesting redirects by matching old URLs (resulting in 4xx errors) with live URLs from an XML sitemap crawl based on the similarity of the URL paths and H1 tags.

## Files Used
1. **Old.xlsx**: This Excel file represents the list of old URLs that result in 4xx errors. It contains one column: `URL`.
2. **New.xlsx**: This Excel file represents the live URLs crawled from the XML sitemap, including the H1 tags for each URL. It contains two columns: `URL` and `H1`.

## Purpose
The script compares the URL paths (the part of the URL after the last `/`) from `Old.xlsx` with the paths from `New.xlsx` and also takes into account the similarity between the old path and the `H1` tag from `New.xlsx`. It then suggests the best matching live URL from the XML sitemap for each old 4xx URL, with a similarity score to aid in decision-making.

## Steps
1. **Loading the Data**: The script reads `Old.xlsx` and `New.xlsx` into two separate dataframes.
   - `Old.xlsx`: Contains a single column `URL`, representing the 4xx URLs.
   - `New.xlsx`: Contains two columns, `URL` (live URLs) and `H1` (the main heading of the live pages).

2. **Extracting the URL paths**: For both datasets, the path (the last part of the URL after the `/`) is extracted. This will be the primary element used for comparing old and new URLs.

3. **Similarity Matching**:
   - The script compares the paths of the old and new URLs using the `rapidfuzz` library's `fuzz.ratio` function.
   - In addition to path comparison, the script also compares the `Old_path` with the `H1` tag from the live URLs in `New.xlsx`. This helps improve accuracy when suggesting redirect matches.
   - The script calculates the overall similarity score by weighting the path similarity (70%) and the H1 similarity (30%).

4. **Generating Redirect Suggestions**:
   - For each 4xx URL in `Old.xlsx`, the script identifies the best matching live URL from `New.xlsx` based on the total similarity score.
   - The resulting matches, along with their similarity scores, are stored in a dataframe.

5. **Exporting the Results**: The final matched results are saved to an Excel file (`output.xlsx`), which contains:
   - `Old_URL`: The original 4xx URL.
   - `Best_Match_New_URL`: The live URL from `New.xlsx` that is the best match.
   - `Similarity_Score`: A numerical score representing the similarity between the old and new URLs.

## Requirements
Ensure you have the following dependencies installed:
```bash
!pip install rapidfuzz
