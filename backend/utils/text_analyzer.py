import logging
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

def analyze_text(content):
    if not content:
        logging.warning("El contenido proporcionado está vacío.")
        return []

    logging.debug("Iniciando tokenización y análisis de texto...")
    words = word_tokenize(content)
    stop_words = set(stopwords.words('english') + stopwords.words('spanish'))
    keywords = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    logging.debug(f"Palabras clave detectadas: {keywords[:10]}")  # Solo muestra las primeras 10 para evitar saturación de logs
    return Counter(keywords).most_common(10)

