// Ejemplo de código JavaScript VULNERABLE
// Contiene múltiples vulnerabilidades de seguridad

// VULNERABILIDAD 1: Uso de eval
function procesarDatos(codigoUsuario) {
    return eval(codigoUsuario);  // Extremadamente peligroso
}

// VULNERABILIDAD 2: innerHTML con datos no sanitizados
function mostrarMensaje(mensaje) {
    document.getElementById('output').innerHTML = mensaje;  // XSS
}

// VULNERABILIDAD 3: Uso de Function constructor
function ejecutarFuncion(codigo) {
    const fn = new Function(codigo);
    return fn();
}

// VULNERABILIDAD 4: document.write sin validación
function escribirContenido(contenido) {
    document.write(contenido);  // Vulnerable a inyección
}

// Código inseguro
const entradaUsuario = prompt("Ingrese código:");
const resultado = procesarDatos(entradaUsuario);
mostrarMensaje(resultado);

// VULNERABILIDAD 5: Acceso directo a window.location
function redirigir(url) {
    window.location = url;  // Sin validación de URL
}

// VULNERABILIDAD 6: Manipulación de DOM peligrosa
function agregarScript(scriptUrl) {
    const script = document.createElement('script');
    script.src = scriptUrl;  // Sin validación
    document.head.appendChild(script);
}
