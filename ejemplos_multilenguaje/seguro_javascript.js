// Ejemplo de código JavaScript SEGURO
// Implementa prácticas seguras de desarrollo

// Función segura para procesar datos (sin eval)
function procesarDatosSeguro(datosJSON) {
    try {
        return JSON.parse(datosJSON);  // Más seguro que eval
    } catch (error) {
        console.error("Error al parsear JSON:", error);
        return null;
    }
}

// Sanitización de HTML para prevenir XSS
function escaparHTML(texto) {
    const div = document.createElement('div');
    div.textContent = texto;
    return div.innerHTML;
}

function mostrarMensajeSeguro(mensaje) {
    // Usar textContent en lugar de innerHTML
    const elemento = document.getElementById('output');
    elemento.textContent = escaparHTML(mensaje);
}

// Validación de entrada
function validarEntrada(entrada) {
    const patron = /^[a-zA-Z0-9\s]+$/;
    return patron.test(entrada);
}

// Redirección segura con validación de URL
function redirigirSeguro(url) {
    const urlsPermitidas = [
        'https://example.com',
        'https://trusted-site.com'
    ];
    
    const urlObj = new URL(url);
    const esSeguro = urlsPermitidas.some(permitida => 
        url.startsWith(permitida)
    );
    
    if (esSeguro) {
        window.location.href = url;
    } else {
        console.error("URL no permitida");
    }
}

// Manipulación segura de DOM
function agregarContenidoSeguro(contenido) {
    const elemento = document.createElement('div');
    elemento.textContent = contenido;  // textContent en lugar de innerHTML
    document.body.appendChild(elemento);
}

// Uso del código seguro
const entradaUsuario = prompt("Ingrese datos:");

if (validarEntrada(entradaUsuario)) {
    mostrarMensajeSeguro(entradaUsuario);
    console.log("Datos procesados de forma segura");
} else {
    console.error("Entrada rechazada por validación");
}

// Content Security Policy helper
const cspConfig = {
    'default-src': "'self'",
    'script-src': "'self' 'unsafe-inline'",
    'style-src': "'self' 'unsafe-inline'"
};
