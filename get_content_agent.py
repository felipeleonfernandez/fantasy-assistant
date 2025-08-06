from googlesearch import search 
from bs4 import BeautifulSoup
import requests
import re

## LISTA DE TOOLS QUE PUEDE USAR EL AGENTE
# Obtener URLs de noticias de Google
# Extraer contenido de una URL


def get_urls_from_google(query: str, num_results: int = 1) -> list:
    urls = []

    for result in search(query, num_results):
        urls.append(result)

    return urls


def extract_content_beautifulsoup(url: str) -> dict:
        """Fallback method using BeautifulSoup for basic content extraction."""
        try:
            session = requests.Session()
            response = session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
                script.decompose()
            
            # Try to find title
            title = None
            if soup.title:
                title = soup.title.string.strip()
            elif soup.find('h1'):
                title = soup.find('h1').get_text().strip()
            
            # Extract main content - try common article containers first
            content_selectors = [
                'article', '.article-content', '.post-content', '.entry-content',
                '.content', '#content', 'main', '.main-content'
            ]
            
            text = ""
            for selector in content_selectors:
                content_div = soup.select_one(selector)
                if content_div:
                    text = content_div.get_text(separator=' ', strip=True)
                    break
            
            # If no specific content found, get body text
            if not text and soup.body:
                text = soup.body.get_text(separator=' ', strip=True)
            
            # Clean up text
            text = re.sub(r'\s+', ' ', text).strip()
            
            return {
                'title': title,
                'text': text,
                'publish_date': None,
                'url': url,
            }
        except Exception as e:
            print(f"BeautifulSoup failed: {str(e)}")
            return None

urls = get_urls_from_google("mariano alaves", 3)
contents = []

for url in urls:
    #print(url)
    contents.append(extract_content_beautifulsoup(url))

#for content in contents:
#    print(content)

news = ""
for content in contents:
    news = news + "--- Noticia: " + content["title"] + " ---" + "\n"
    news = news + content["text"] + "\n\n"

print(news)
