<?php
// Ejemplo de código PHP SEGURO
// Implementa prácticas seguras de desarrollo

// Consulta SQL segura con prepared statements
function consultarUsuarioSeguro($nombreUsuario) {
    $conexion = new mysqli("localhost", "user", "pass", "db");
    
    // Prepared statement previene SQL injection
    $stmt = $conexion->prepare("SELECT * FROM usuarios WHERE nombre = ?");
    $stmt->bind_param("s", $nombreUsuario);
    $stmt->execute();
    $resultado = $stmt->get_result();
    
    return $resultado;
}

// Procesamiento seguro sin eval
function procesarDatosSeguro($datosJSON) {
    $datos = json_decode($datosJSON, true);
    
    if (json_last_error() === JSON_ERROR_NONE) {
        return $datos;
    }
    return null;
}

// Ejecución segura de comandos con validación
function ejecutarComandoSeguro($comando) {
    $comandosPermitidos = ['ls', 'pwd', 'date'];
    
    if (!in_array($comando, $comandosPermitidos)) {
        throw new Exception("Comando no permitido");
    }
    
    // escapeshellcmd para sanitizar
    $comandoSeguro = escapeshellcmd($comando);
    $resultado = shell_exec($comandoSeguro);
    
    return $resultado;
}

// Validación de entrada
function validarEntrada($entrada) {
    // Filtrar y validar
    $filtrada = filter_var($entrada, FILTER_SANITIZE_STRING);
    
    if (preg_match('/^[a-zA-Z0-9\s]+$/', $filtrada)) {
        return $filtrada;
    }
    return false;
}

// Prevención de XSS
function mostrarMensajeSeguro($mensaje) {
    echo htmlspecialchars($mensaje, ENT_QUOTES, 'UTF-8');
}

// Protección CSRF con token
session_start();

function generarTokenCSRF() {
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

function verificarTokenCSRF($token) {
    return isset($_SESSION['csrf_token']) && 
           hash_equals($_SESSION['csrf_token'], $token);
}

// Carga segura de archivos
function subirArchivoSeguro($archivo) {
    $extensionesPermitidas = ['jpg', 'png', 'pdf'];
    $tamanoMaximo = 5 * 1024 * 1024; // 5MB
    
    $extension = pathinfo($archivo['name'], PATHINFO_EXTENSION);
    
    if (!in_array(strtolower($extension), $extensionesPermitidas)) {
        throw new Exception("Tipo de archivo no permitido");
    }
    
    if ($archivo['size'] > $tamanoMaximo) {
        throw new Exception("Archivo demasiado grande");
    }
    
    // Generar nombre aleatorio
    $nombreSeguro = bin2hex(random_bytes(16)) . '.' . $extension;
    $destino = "uploads/" . $nombreSeguro;
    
    move_uploaded_file($archivo['tmp_name'], $destino);
    return $nombreSeguro;
}

// Uso del código seguro
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (verificarTokenCSRF($_POST['csrf_token'])) {
        $entrada = validarEntrada($_POST['entrada']);
        
        if ($entrada !== false) {
            mostrarMensajeSeguro($entrada);
        } else {
            echo "Entrada rechazada por validación";
        }
    } else {
        echo "Token CSRF inválido";
    }
}
?>
