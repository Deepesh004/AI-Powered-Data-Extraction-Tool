import openai
import time
from serpapi import GoogleSearch

def web_search(entity_name, prompt, api_key):
    query = prompt.replace("{company}", entity_name)
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("organic_results", [])

def parse_results_with_llm(entity, search_results, custom_prompt, openai_api_key):
    openai.api_key = openai_api_key
    llm_prompt = f"Extract the {custom_prompt} for {entity} using these search results: {search_results}"
    for attempt in range(3):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": llm_prompt}]
            )
            return response['choices'][0]['message']['content'].strip()
        except openai.error.RateLimitError:
            time.sleep(5 * (2 ** attempt))  # exponential backoff
        except Exception as e:
            return str(e)
    return "Error: Unable to retrieve information"
