# Project Architecture

This application is structured to allow easy data upload, web search integration, and AI-powered data extraction.

- **Streamlit Frontend**: Handles user interactions like file uploads and input prompts.
- **Data Extraction**:
  - `web_search`: Performs a search on Google using SerpAPI based on a custom prompt.
  - `parse_results_with_llm`: Extracts data from search results using OpenAI's API.

Refer to `app/extraction.py` for the detailed implementation of these functions.
