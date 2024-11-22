// Obtener el formulario y la sección de resultados
const form = document.getElementById('analyzeForm');
const resultsDiv = document.getElementById('results');

// Escuchar el evento de envío del formulario
form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevenir el envío del formulario

    // Limpiar resultados previos
    resultsDiv.innerHTML = '<p>Analizando... Por favor, espera.</p>';

    // Obtener el valor de la URL ingresada
    const url = document.getElementById('url').value;

    try {
        // Hacer una solicitud POST al backend
        const response = await fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        });

        // Verificar si la solicitud fue exitosa
        if (!response.ok) {
            throw new Error(`Error en el servidor: ${response.statusText}`);
        }

        // Parsear la respuesta JSON
        const data = await response.json();

        // Mostrar los resultados
        displayResults(data);
    } catch (error) {
        // Mostrar el error en caso de que falle la solicitud
        resultsDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});

// Función para mostrar los resultados en la interfaz
function displayResults(data) {
    if (data.error) {
        resultsDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        return;
    }

    // Construir HTML dinámico para los resultados
    let html = '<h3>Resultados del Análisis</h3>';

    // Correos electrónicos encontrados
    if (data.emails && data.emails.length > 0) {
        html += '<h4>Correos Electrónicos:</h4><ul>';
        data.emails.forEach(email => {
            html += `<li>${email}</li>`;
        });
        html += '</ul>';
    } else {
        html += '<p>No se encontraron correos electrónicos.</p>';
    }

    // Temas principales
    if (data.topics && data.topics.length > 0) {
        html += '<h4>Temas Principales:</h4><ul>';
        data.topics.forEach(([topic, count]) => {
            html += `<li>${topic}: ${count}</li>`;
        });
        html += '</ul>';
    } else {
        html += '<p>No se detectaron temas principales.</p>';
    }

    // Blog
    html += `<h4>Blog:</h4><p>${data.blog}</p>`;

    // Enlaces de Facebook
    if (data.facebook_links && data.facebook_links.length > 0) {
        html += '<h4>Enlaces a Facebook:</h4><ul>';
        data.facebook_links.forEach(link => {
            html += `<li><a href="${link}" target="_blank">${link}</a></li>`;
        });
        html += '</ul>';
    } else {
        html += '<p>No se encontraron enlaces a Facebook.</p>';
    }

    // Datos extraídos de Facebook
    if (data.facebook_data && data.facebook_data.length > 0) {
        html += '<h4>Datos de Facebook:</h4>';
        data.facebook_data.forEach(fb => {
            html += `
                <div>
                    <p><strong>URL:</strong> <a href="${fb.facebook_url}" target="_blank">${fb.facebook_url}</a></p>
                    <p><strong>Email:</strong> ${fb.email || 'No encontrado'}</p>
                    <p><strong>Teléfono:</strong> ${fb.phone || 'No encontrado'}</p>
                </div>
            `;
        });
    }

    // Actualizar la sección de resultados
    resultsDiv.innerHTML = html;
}
