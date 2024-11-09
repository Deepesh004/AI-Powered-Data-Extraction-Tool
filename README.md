AI-Powered Data Extraction Tool
This project is a Streamlit application that uses OpenAI's language models and SerpAPI's Google Search API to extract targeted information from the web for each entry in a CSV file. Users can upload a CSV file, define a prompt, and obtain specific information for each entity listed in the file. The extracted data can be downloaded in CSV format for further analysis or record-keeping.

Table of Contents
Features
Installation
Usage
Project Structure
API Key Configuration
Sample Data
Troubleshooting
Contributing
License
Features
CSV Upload: Easily upload a CSV file for data extraction.
Custom Prompts: Define search prompts using placeholders (e.g., {company}).
Automated Web Search: Search for each entity in the selected column using SerpAPI's Google Search API.
AI-Powered Extraction: Use OpenAI's GPT model to extract information from the search results.
CSV Download: Download extracted data in CSV format for easy access and analysis.
Installation
Clone the Repository:
git clone https://github.com/your-username/ai-powered-data-extraction-tool.git
cd ai-powered-data-extraction-tool

Set API Keys:
Add your API keys for SerpAPI and OpenAI in the app/app.py file or load them from environment variables.
Run the Application:
streamlit run app/app.py
Use the Tool:
Upload a CSV file.
Select the column containing the entity names (e.g., company names).
Enter a prompt, using {company} as a placeholder (e.g., Find the contact email for {company}).
Click "Run Data Extraction" to start the process.
View or download the extracted data as a CSV file.
Project Structure
.
├── app/
│   ├── app.py                # Main Streamlit application
│   ├── extraction.py         # Contains data extraction functions
├── data/
│   └── sample.csv            # Sample CSV data file for testing
├── docs/
│   └── architecture.md       # Documentation on project architecture
├── README.md
├── requirements.txt          # Required dependencies
API Key Configuration
To use the application, you'll need API keys for:
SerpAPI: Get your API key by signing up at SerpAPI.
OpenAI: Get your API key by signing up at OpenAI.
Add these keys in app/app.py:
python
Copy code
# Initialize API Keys
SERP_API_KEY = 'your_serpapi_key_here'
OPENAI_API_KEY = 'your_openai_key_here'
openai.api_key = OPENAI_API_KEY
Troubleshooting
RateLimitError: If the OpenAI API rate limit is reached, the tool will retry automatically with exponential backoff. For frequent issues, consider upgrading your OpenAI plan or using a less intensive prompt.
Invalid API Key: Ensure that the API keys for both OpenAI and SerpAPI are valid and correctly added in app/app.py.
Contributing
Contributions are welcome! Please feel free to open issues, fork the repository, and submit pull requests.
