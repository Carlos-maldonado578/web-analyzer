from flask import Flask, request, jsonify
from utils.email_extractor import extract_emails
from utils.text_analyzer import analyze_text
from utils.blog_detector import detect_blog
from utils.facebook_extractor import extract_facebook_data
from urllib.parse import urljoin
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import logging
import nltk
import os

# Establecer un directorio específico para nltk_data
nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

# Configurar la variable de entorno para NLTK
nltk.data.path.append(nltk_data_path)

# Verificar y descargar recursos necesarios
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    logging.info("Recurso 'punkt' no encontrado. Descargando...")
    nltk.download('punkt', download_dir=nltk_data_path)
    logging.info("Recurso 'punkt' descargado correctamente.")

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    logging.info("Recurso 'stopwords' no encontrado. Descargando...")
    nltk.download('stopwords', download_dir=nltk_data_path)
    logging.info("Recurso 'stopwords' descargado correctamente.")


# Configuración de logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend.log"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
CORS(app)

def analyze_website(url):
    logging.info(f"Iniciando análisis de la URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.debug(f"Página obtenida exitosamente: {url}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        
        # Extraer correos y temas
        emails = extract_emails(text_content)
        try:
            topics = analyze_text(text_content)
        except Exception as e:
            logging.error(f"Error al analizar el texto: {str(e)}")
            topics = []

        logging.info(f"Correos encontrados: {emails}")
        logging.info(f"Temas principales detectados: {topics}")
        
        # Extraer links y detectar blogs
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
        blog_link = detect_blog(links)
        logging.info(f"Link a blog detectado: {blog_link}")
        
        # Buscar enlaces de Facebook
        facebook_links = [link for link in links if 'facebook.com' in link.lower()]
        facebook_data = [
            extract_facebook_data(fb_link) for fb_link in facebook_links
        ]
        logging.info(f"Enlaces de Facebook detectados: {facebook_links}")
        
        return {
            "emails": emails,
            "topics": topics,
            "blog": blog_link or "No se detectó un blog en esta página.",
            "facebook_links": facebook_links,
            "facebook_data": facebook_data
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Error de red al analizar la URL {url}: {str(e)}")
        return {"error": "No se pudo acceder a la URL proporcionada."}
    except Exception as e:
        logging.error(f"Error inesperado al analizar la URL {url}: {str(e)}")
        return {"error": str(e)}


# Endpoint para analizar la página principal
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    logging.info("Solicitud recibida en /analyze")
    logging.debug(f"Datos de entrada: {data}")
    
    url = data.get('url')
    if not url:
        logging.warning("URL no proporcionada en la solicitud")
        return jsonify({"error": "URL no proporcionada."}), 400

    results = analyze_website(url)
    logging.debug(f"Resultados del análisis: {results}")
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
