import httpx
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def brave_search(query, count=5):
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": os.getenv("BRAVE_API_KEY")  
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

def summarize(prompt='', text=""):
    if prompt == '':
        prompt = f"Summarize this in bullet points:\n{text}"
    
    from openai import OpenAI
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Replace with your OpenAI API key
    response = client.chat.completions.create(model="gpt-4.1",
    messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content