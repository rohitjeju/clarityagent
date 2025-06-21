import httpx
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

def brave_search(query, api_key, count=5):
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key
    }
    params = {
        "q": query,
        "count": count
    }

    response = httpx.get(url, headers=headers, params=params)
    results = response.json()

    links = []
    if "web" in results:
        for item in results["web"]["results"]:
            links.append(item["url"])

    return links

def extract_text_from_url(url):
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.text, 'html.parser')
    paragraphs = [p.text for p in soup.find_all('p')]
    return "\n".join(paragraphs[:20])  # limit to avoid overload

def summarize(prompt="", text=""):
    if prompt != "":
        prompt = f"Summarize this in bullet points:\n{text}"
    
    from openai import OpenAI
    
    client = OpenAI(api_key="your key")  # Replace with your OpenAI API key
    response = client.chat.completions.create(model="gpt-4o",
    messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

def research_assistant(query, API_KEY="your key"):
    links = brave_search(query, API_KEY)
    combined_text = ""
    for link in links:
        try:
            combined_text += extract_text_from_url(link) + "\n\n"
        except Exception as e:
            print(f"Error with {link}: {e}")

    return summarize(combined_text)

if __name__ == "__main__":
    query = "What are the latest advancements in AI?"
    summary = research_assistant(query)
    print("Summary of Research:")
    print(summary)
# This code provides a simple research assistant that uses Brave Search to find relevant links,
# extracts text from those links, and summarizes the information using OpenAI's GPT-4o model.