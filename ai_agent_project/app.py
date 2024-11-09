import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
import openai
import time

# Initialize API Keys
SERP_API_KEY = 'baa28dddb1ba7f11263f298d0eeefdee821215e59778efe67bf45a73773cedbc'  
OPENAI_API_KEY = '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'  
openai.api_key = OPENAI_API_KEY

# Streamlit App Header
st.title("AI-Powered Data Extraction Tool")
st.write("Begin by uploading a CSV file.")

# Section: Upload File
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
df = None

try:
    # Load and Display Data if Uploaded
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Here's a preview of your data:")
            st.write(df.head())
        except Exception as e:
            st.error(f"Error loading CSV: {e}")
        
        # Select the column for data extraction
        if df is not None:
            column_names = df.columns.tolist()
            selected_column = st.selectbox("Select the primary column to extract data from:", column_names)
except Exception as e:
    st.error(f"An error occurred while processing the file: {e}")

# Prompt Setup
custom_prompt = st.text_input("Enter a search prompt using '{company}' as a placeholder (e.g., 'Find the contact email for {company}').")
if "{company}" not in custom_prompt:
    st.warning("Your prompt should contain '{company}' as a placeholder.")

# Function to Perform Web Search with SerpAPI
def web_search(entity_name, prompt):
    query = prompt.replace("{company}", entity_name)
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY,
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        return results.get("organic_results", [])
    except Exception as e:
        st.error(f"Error with SerpAPI request: {e}")
        return []

def call_openai_api_with_retry(entity, search_results, custom_prompt, retries=3, delay=5):
    for i in range(retries):
        try:
            # API call
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": custom_prompt}]
            )
            return response
        except openai.error.RateLimitError:
            if i < retries - 1:
                st.warning(f"Rate limit reached. Retrying in {delay * (2 ** i)} seconds...")
                time.sleep(delay * (2 ** i))  # Exponential backoff
            else:
                st.error("Rate limit reached. Please try again later or check your quota.")
                return None
        except Exception as e:
            st.error(f"Error with OpenAI API request: {e}")
            return None

# Function to Extract Data with OpenAI's Model
def parse_results_with_llm(entity, search_results, custom_prompt):
    llm_prompt = f"Please extract the {custom_prompt} for {entity} using these search results: {search_results}"
    response = call_openai_api_with_retry(entity, search_results, custom_prompt)
    if response:
        return response['choices'][0]['message']['content'].strip()
    return "No data extracted."

# Run Data Extraction when Button is Clicked
if st.button("Run Data Extraction"):
    if df is not None and custom_prompt:
        results = {}
        extracted_data = {}

        try:
            # Process each entry in the selected column
            for entity in df[selected_column]:
                search_results = web_search(entity, custom_prompt)
                results[entity] = search_results
                extracted_data[entity] = parse_results_with_llm(entity, search_results, custom_prompt)

            # Display Extraction Results
            st.write("Raw Search Results:", results)
            st.write("Extracted Data:", extracted_data)

            # Convert extracted data to DataFrame and display
            extracted_df = pd.DataFrame(list(extracted_data.items()), columns=['Entity', 'Extracted Data'])
            st.write("Final Extracted Information:")
            st.write(extracted_df)

            # Download Option for Extracted Data
            csv = extracted_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Extracted Data as CSV", data=csv, file_name="extracted_data.csv", mime="text/csv")
        except Exception as e:
            st.error(f"An error occurred during data extraction: {e}")
    else:
        st.warning("Please upload a file and make sure your prompt is valid.")
