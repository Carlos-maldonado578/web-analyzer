import requests
from bs4 import BeautifulSoup
import logging

def extract_facebook_data(fb_url):
    logging.info(f"Iniciando extracción de datos desde: {fb_url}")
    try:
        response = requests.get(fb_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscar posibles datos como email o teléfono en el HTML visible
        page_text = soup.get_text()
        email = None
        phone = None

        if '@' in page_text:
            email_candidates = page_text.split()
            email = next((word for word in email_candidates if '@' in word and '.' in word), None)

        phone_candidates = [
            word for word in page_text.split() if word.isdigit() and len(word) >= 8
        ]
        phone = phone_candidates[0] if phone_candidates else None

        logging.debug(f"Datos extraídos: Email: {email}, Teléfono: {phone}")
        return {
            "facebook_url": fb_url,
            "email": email,
            "phone": phone,
        }
    except Exception as e:
        logging.error(f"Error al extraer datos de Facebook desde {fb_url}: {str(e)}")
        return {"facebook_url": fb_url, "error": str(e)}
