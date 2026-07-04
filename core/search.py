from duckduckgo_search import DDGS

def web_search(query):

    try:

        with DDGS() as ddgs:

            results = list(ddgs.text(query, max_results=5))

        if not results:
            return None

        text = ""

        for r in results:

            text += f"Title: {r['title']}\n"
            text += f"Body: {r['body']}\n\n"

        return text

    except Exception as e:

        return None