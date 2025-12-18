<?php
// Ejemplo de código PHP VULNERABLE
// Contiene múltiples vulnerabilidades de seguridad

// VULNERABILIDAD 1: SQL Injection
function consultarUsuario($nombreUsuario) {
    $conexion = mysqli_connect("localhost", "user", "pass", "db");
    $query = "SELECT * FROM usuarios WHERE nombre = '$nombreUsuario'";
    $resultado = mysqli_query($conexion, $query);  // Vulnerable
    return $resultado;
}

// VULNERABILIDAD 2: Uso de eval
function procesarCodigo($codigo) {
    eval($codigo);  // Extremadamente peligroso
}

// VULNERABILIDAD 3: Ejecución de comandos sin sanitización
function ejecutarComando($comando) {
    $resultado = exec($comando);  // Sin validación
    return $resultado;
}

// VULNERABILIDAD 4: Deserialización insegura
function deserializar($datos) {
    $objeto = unserialize($datos);  // Peligroso
    return $objeto;
}

// VULNERABILIDAD 5: Include/Require con datos de usuario
function cargarArchivo($nombreArchivo) {
    include($_GET['archivo']);  // Path traversal
}

// VULNERABILIDAD 6: XSS sin escapar
function mostrarMensaje($mensaje) {
    echo $mensaje;  // Sin htmlspecialchars
}

// Uso inseguro
$entrada = $_POST['entrada'];
procesarCodigo($entrada);
ejecutarComando($entrada);

// VULNERABILIDAD 7: CSRF - Sin token
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nuevoEmail = $_POST['email'];
    // Cambiar email sin validar origen
}

// VULNERABILIDAD 8: Carga de archivos sin validación
if (isset($_FILES['archivo'])) {
    $destino = "uploads/" . $_FILES['archivo']['name'];
    move_uploaded_file($_FILES['archivo']['tmp_name'], $destino);
}
?>
