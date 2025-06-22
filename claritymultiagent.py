
import clarityagent as ca

def research_assistant(query):
    links = ca.brave_search(query, count=5)
    combined_text = ""
    for link in links:
        try:
            combined_text += ca.extract_text_from_url(link) + "\n\n"
        except Exception as e:
            print(f"Error with {link}: {e}")

    return ca.summarize(prompt='', text=combined_text)

if __name__ == "__main__":
    query = "What are the latest advancements in Agentic AI?"
    summary = research_assistant(query)
    print("Summary of Research:")
    print(summary)
# This code provides a simple research assistant that uses Brave Search to find relevant links,
# extracts text from those links, and summarizes the information using OpenAI's GPT-4o model.