import json
from typing import Any, Dict, List, Optional
from googlesearch import search 
from bs4 import BeautifulSoup
import requests
import re
from dotenv import load_dotenv
import os
from openai import OpenAI
import cloudscraper
import unicodedata 


load_dotenv()

## LISTA DE TOOLS QUE PUEDE USAR EL AGENTE
# Obtener URLs de noticias de Google
# Extraer contenido de una URL dada
# Preguntar al usuario para aclarar la búsqueda


class FantasyAssistantAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        self.conversation_history = []

    @staticmethod
    def get_news_sites() -> list:
        """Returns a list of news sites to search for football-related content."""
        return [
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

    def get_urls_from_googlesearch(self, query_string: str, lang: str = "es") -> Optional[list]:
        """Get the URLs related to the query from Google Search."""
        news_sites = self.get_news_sites()
        try: 
            news_query = f"{query_string} {' OR '.join(news_sites)}"
            urls = list(search(news_query, lang=lang, unique=True))
            return urls
        except Exception as e:
            print(f"Search to get URLs failed: {str(e)}")
            return None

    def extract_url_content(self, url: str, keywords: list) -> Optional[dict]:
        """Get the content of a URL using BeautifulSoup. The content is filtered by keywords."""
        try:
            session = cloudscraper.create_scraper()
            response = session.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()

            # Si la URL final es diferente, úsala
            final_url = response.url
              
            if final_url != url:
                return self.extract_url_content(final_url, keywords)

            soup = BeautifulSoup(response.content, 'html.parser')
  
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
                    temp_text_normalized = self.normalize_text(temp_text_lower)
                    if not any(self.normalize_text(k) in temp_text_normalized for k in keywords):
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

    def get_output_format(self, query_type: str) -> str:
        output = ""
        with open("outputs/" + query_type + ".txt",'r') as f:
            output = f.read()
        return output

    ## Utility functions (not tools used by the agent directly)
    def normalize_text(self, text):
        """Remove accents and special characters from the text."""
        if not isinstance(text, str):
            return text
        # Normaliza a forma NFD y elimina los caracteres diacríticos (tildes)
        text = unicodedata.normalize('NFD', text)
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        # Opcional: elimina otros caracteres no alfanuméricos
        text = ''.join(c for c in text if c.isalnum() or c.isspace())
        return text

    def ask_user_for_clarification(self, question_to_user: str) -> str:
        """Poses the question_to_user to the actual user and returns their typed response."""
        print(f"\nAgent needs clarification: {question_to_user}")
        response = input("Your response: ")
        return response

    def create_tool_definitions(self) -> List[Dict[str, Any]]:
        """Creates OpenAI function calling definitions for the tools."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_urls_from_googlesearch",
                    "description": "Get the URLs related to the query string from Google Search.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query_string": {
                                "type": "string",
                                "description": "The query string to search for in Google."
                            },
                            "lang": {
                                "type": "string",
                                "description": "Language of the search."
                            }
                        },
                        "required": ["query_string", "lang"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "extract_url_content",
                    "description": "Get the content of a URL using BeautifulSoup. The content is filtered by keywords.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL to extract content from."
                            },
                            "keywords": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "List of keywords that must exist in the extracted text."
                            }
                        },
                        "required": ["url", "keywords"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_output_format",
                    "description": "Get the output format depending on the query type.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query_type": {
                                "type": "string",
                                "description": "The name of the performed query type. It can have one of the following values: 'prob_fichaje' (signing a player for your Fantasy team) o 'prob_titularidad' (probability of being a starter in the next match)."
                            },
                        },
                        "required": ["query_name"]
                    }
                }
            }
        ]

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Executes the specified tool with given arguments."""
        if tool_name == "get_urls_from_googlesearch":
            return self.get_urls_from_googlesearch(arguments["query_string"], arguments["lang"])
        elif tool_name == "extract_url_content":
            return self.extract_url_content(arguments["url"], arguments["keywords"])
        elif tool_name == "get_output_format":
            return self.get_output_format(arguments["query_type"])
        else:
            return None

    def process_user_query(self, user_query: str) -> str:
        """Processes a user query using the OpenAI API with function calling."""
        self.conversation_history.append({"role": "user", "content": user_query})
        
        system_prompt = """
            Eres un analista asistente experto en fútbol español para juegos Fantasy como Futmondo, Biwenger o Fantasy Marca.
                        
            A tu disposición tienes las siguientes herramientas (tools):
            1. Obtener URLs de enlaces a través de la búsqueda de Google.
            2. Extraer contenido de una URL dada, filtrando por palabras clave.
            3. Preguntar a los usuarios para aclarar la búsqueda si la información es ambigua.
            4. Obtener un formato de salida específico para la respuesta.
            
            Tu tarea es ayudar a los usuarios a obtener información relevante sobre fichajes, rumores y noticias de jugadores y equipos.
            Si la información no es suficiente, pregunta al usuario para aclarar la búsqueda.

            A la hora de dar la respuesta (excepto si es para pedir aclaraciones), utiliza uno de los formatos de salida predefinidos que puedes obtener con la herramienta "get_output_format".
        """
        
        while True:
            messages = [
                {"role": "system", "content": system_prompt},
                *self.conversation_history
            ]
            
            # Call OpenAI API with function calling
            response = self.client.chat.completions.create(
                model="o4-mini",
                messages=messages,
                tools=self.create_tool_definitions(),
                tool_choice="auto"  # Let the model decide which tool to use
            )
            
            response_message = response.choices[0].message
            
            # If no tool calls, we're done
            if not response_message.tool_calls:
                self.conversation_history.append({"role": "assistant", "content": response_message.content})
                return response_message.content
            
            # Execute the tool the agent chose
            tool_call = response_message.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"\nExecuting tool: {function_name} with args: {function_args}")
            
            # Execute the tool
            result = self.execute_tool(function_name, function_args)
            
            # Add everything to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": function_name,
                        "arguments": json.dumps(function_args)
                    }
                }]
            })
            
            self.conversation_history.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": str(result) if result is not None else "No result found"
            })
    
    def chat(self):
        """Interactive chat loop."""
        print("Asistente de juegos Fantasy")
        print("Pregúntame sobre posibles fichajes en el juego, probabilidades de titularidad o cualquier cuestión relacionada")
        print("Escribe 'salir' para terminar la ejecución.\n")
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'salir']:
                print("¡Adiós!")
                break
            
            try:
                response = self.process_user_query(user_input)
                print(f"\nAsistente: {response}\n")
            except Exception as e:
                print(f"\nError: {e}\n")

if __name__ == "__main__":
    agent = FantasyAssistantAgent()
    agent.chat()