from googlesearch import search 
from bs4 import BeautifulSoup
import requests
import re

## LISTA DE TOOLS QUE PUEDE USAR EL AGENTE
# Obtener URLs de noticias de Google
# Extraer contenido de una URL dada
# Preguntar al usuario para aclarar la búsqueda

def normalize_text(text):
    """
    Elimina tildes y caracteres especiales, dejando solo letras básicas.
    """
    if not isinstance(text, str):
        return text
    # Normaliza a forma NFD y elimina los caracteres diacríticos (tildes)
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    # Opcional: elimina otros caracteres no alfanuméricos
    text = ''.join(c for c in text if c.isalnum() or c.isspace())
    return text


def get_urls_from_googlesearch(query: str) -> list:
    news_sites = [
        # Diarios generalistas con secciones deportivas fuertes
        "site:elpais.com", "site:elmundo.es", "site:abc.es", "site:larazon.es",
        "site:elconfidencial.com", "site:publico.es", "site:eldiario.es", "site:20minutos.es",
        
        # Diarios deportivos principales
        "site:marca.com", "site:as.com", "site:mundodeportivo.com", "site:sport.es",
        "site:estadiodeportivo.com", "site:superdeporte.es", "site:todofichajes.com",
        
        # Medios especializados en fútbol
        "site:relevo.com", "site:besoccer.com", "site:futbolprimera.es",
        "site:defensacentral.com", "site:fichajes.net", "site:fichajes.com",
        "site:elgoldigital.com", "site:diariogol.com", "site:okdiario.com",
        
        # Cadenas de radio deportiva
        "site:cadenaser.com", "site:ondacero.es", "site:cope.es", "site:esradio.fm",
        "site:radioestadio.es", "site:cadenacopeeuskadi.es",
        
        # Televisiones deportivas
        "site:espn.com.ar", "site:tycsports.com", "site:ole.com.ar", "site:clarin.com",
        "site:lanacion.com.ar", "site:infobae.com", "site:perfil.com",
        
        # Medios internacionales en español
        "site:cnn.com", "site:bbcmundo.com", "site:dw.com", "site:france24.com",
        
        # Sitios especializados en Real Madrid
        "site:realmadrid.com", "site:managingmadrid.com", "site:defensa-central.com",
        "site:madridismo.com", "site:rmtv.es", "site:halamadrid.com",
        
        # Sitios especializados en Barcelona
        "site:fcbarcelona.es", "site:fcbarcelonanoticias.com", "site:mundoculer.com",
        "site:barcelonista.com", "site:somhiseaules.cat", "site:tot.cat",
        
        # Sitios especializados en Atlético Madrid
        "site:atleticodemadrid.com", "site:todoatletico.com", "site:unionatletica.com",
        
        # Medios regionales con cobertura deportiva
        "site:lavanguardia.com", "site:elperiodico.com", "site:naciodigital.cat",
        "site:vilaweb.cat", "site:ara.cat", "site:elpuntavui.cat",
        
        # Medios del País Vasco
        "site:deia.eus", "site:elcorreo.com", "site:noticiasdegipuzkoa.eus",
        "site:naiz.eus", "site:berria.eus", "site:eitb.eus",
        
        # Medios de Andalucía
        "site:diariodesevilla.es", "site:diariosur.es", "site:ideal.es",
        "site:granadahoy.com", "site:diariocordoba.com", "site:huelvainformacion.es",
        
        # Medios de Valencia
        "site:levante-emv.com", "site:lasprovincias.es", "site:informacion.es",
        "site:diarioinformacion.com", "site:elperiodico.com",
        
        # Medios de Galicia
        "site:lavozdegalicia.es", "site:farodevigo.es", "site:elcorreogallego.es",
        "site:atlantico.net", "site:galiciae.com",
        
        # Medios especializados en Primera División
        "site:laliga.com", "site:ligaconfidencial.com", "site:primerafederacion.es",
        
        # Medios especializados en Segunda División
        "site:segundadivision.es", "site:laligasmartbank.es",
        
        # Sitios de mercado de fichajes
        "site:transfermarkt.es", "site:fichajes.net", "site:mercadofichajes.com",
        "site:eldesmarque.com", "site:golsmedia.com", "site:futbolmercado.es",
        
        # Medios digitales deportivos
        "site:diarioas.com", "site:espndeportes.com", "site:goal.com",
        "site:90min.com", "site:footmercato.net", "site:calciomercato.com",
        
        # Blogs y medios independientes
        "site:elchiringuitotv.com", "site:jugones.com", "site:elgolazo24.com",
        "site:diariodelasamericas.com", "site:futbolred.com", "site:antena3.com",
        
        # Medios de Canarias
        "site:canarias7.es", "site:laprovincia.es", "site:eldia.es",
        
        # Medios de otras comunidades
        "site:heraldo.es", "site:diariodeavila.es", "site:elnortedecastilla.es",
        "site:diariodemallorca.es", "site:ultimahora.es", "site:diariodeleon.es",
        
        # Sitios especializados en fútbol femenino
        "site:futfem.com", "site:deportesfemeninos.es", "site:mujeresdeportistas.com",
        
        # Medios especializados en fútbol base y cantera
        "site:futbolbase.es", "site:cantera.es", "site:juvenilfutbol.com",
        
        # Sitios de estadísticas y datos
        "site:soccerstats.com", "site:resultados-futbol.com", "site:livescore.com",
        "site:espnfc.com", "site:skysports.com", "site:eurosport.com",
        
        # Medios internacionales con versión en español
        "site:marca.com", "site:mundodeportivo.com", "site:ole.com.ar",
        "site:depor.com", "site:elcomercio.pe", "site:publimetro.com",
        
        # Sitios especializados en Champions League
        "site:uefa.com", "site:championsleague.com", "site:europaleague.com",
        
        # Medios especializados en selecciones
        "site:sefutbol.com", "site:rfef.es", "site:seleccionespanola.es"
    ]
    news_query = f"{query} {' OR '.join(news_sites)}"
    return list(search(news_query, lang="es", unique=True))

# def get_urls_from_googlenews(query: str):
#     googlenews = GoogleNews(lang='es')
#     googlenews.search(query)
#     result = googlenews.result()
#     data = pd.DataFrame.from_dict(result)
#     data.head()

def extract_content_beautifulsoup(url: str, keywords) -> dict:
    """Fallback method using BeautifulSoup for basic content extraction, following redirects."""
    try:
        # Cambia requests por cloudscraper
        session = cloudscraper.create_scraper()
        response = session.get(url, timeout=10, allow_redirects=True)
        response.raise_for_status()

        # Si la URL final es diferente, úsala
        final_url = response.url

        soup = BeautifulSoup(response.content, 'html.parser')
            
        if final_url != url:
            return extract_content_beautifulsoup(final_url, keywords)

        # Remove script and style elements
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # Try to find title
        title = None
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        elif soup.find('h1'):
            title = soup.find('h1').get_text().strip()

        # Extract main content - try common article containers first
        content_selectors = [
            'article', '.article-content', '.post-content', '.entry-content',
            '.content', '#content', 'main', '.main-content', '.story-body', '.c-article-content'
        ]

        text = ""
        selector_found = None
        for selector in content_selectors:
            content_div = soup.select_one(selector)
            if content_div:
                temp_text = content_div.get_text(separator=' ', strip=True)
                temp_text_lower = temp_text.lower()
                temp_text_normalized = normalize_text(temp_text_lower)
                if not any(normalize_text(k) in temp_text_normalized for k in keywords):
                    continue
                else:
                    selector_found = selector
                    if temp_text not in text:  # Avoid duplicates
                        text = temp_text
                        break

        # If no specific content found, get body text
        if text == "":
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text(strip=True) for p in paragraphs])

        text = re.sub(r'\s+', ' ', text).strip()
        
        return {
            'title': title,
            'text': text,
            'url': final_url,
            'selector': selector_found if selector_found else 'body',
        }
        
    except Exception as e:
        print(f"BeautifulSoup failed: {str(e)}")
        return None
    
player_name = sys.argv[1]
team_name = sys.argv[2]

urls = get_urls_from_googlesearch(player_name + " " + team_name)
contents = []
for url in urls:
    res = extract_content_beautifulsoup(url, [player_name, team_name])
    if res is not None:
        contents.append(res)
    if len(contents) == 8:
        break

#print(contents)
#print(len(contents))

news = ""
for content in contents:
    news = news + "--- Noticia: " + content["title"] + " ---" + "\n"
    news = news + content["text"] + "\n\n"

# Extraemos el prompt a enviar 
with open('prompts/calcular_prob_fichaje_mercado.txt','r') as f:
    prompt = f.read()

prompt = prompt.replace("{player_name}", player_name)
prompt = prompt.replace("{team_name}", team_name)
prompt = prompt.replace("{scraped_data}", news)

#print(prompt)

# Hacemos la llamada a OpenAI para obtener la respuesta
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

response = client.responses.create(
    model="o4-mini",
    input=prompt
)

print(response.output_text)

