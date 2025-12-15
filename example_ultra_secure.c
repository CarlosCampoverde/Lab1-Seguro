/**
 * EJEMPLO DE CÓDIGO ULTRA SEGURO
 * Implementa las mejores prácticas de seguridad para minimizar
 * la probabilidad de vulnerabilidades detectadas por el modelo
 * 
 * Características de seguridad:
 * - Sin funciones peligrosas (strcpy, gets, system, etc.)
 * - Validación exhaustiva de entrada
 * - Manejo seguro de buffers
 * - Límites estrictos en todas las operaciones
 * - Sanitización de datos
 * - Manejo de errores robusto
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdbool.h>

// Constantes para límites seguros
#define MAX_INPUT_LENGTH 256
#define MAX_BUFFER_SIZE 512
#define MAX_USERNAME_LENGTH 64
#define MAX_PASSWORD_LENGTH 128

/**
 * Función para validar entrada de usuario
 * Verifica que solo contenga caracteres alfanuméricos seguros
 */
bool validate_input(const char *input) {
    if (input == NULL) {
        return false;
    }
    
    size_t len = strlen(input);
    if (len == 0 || len > MAX_INPUT_LENGTH) {
        return false;
    }
    
    // Verificar caracteres permitidos
    for (size_t i = 0; i < len; i++) {
        if (!isalnum(input[i]) && input[i] != ' ' && 
            input[i] != '_' && input[i] != '-') {
            return false;
        }
    }
    
    return true;
}

/**
 * Función para sanitizar cadenas de texto
 * Elimina caracteres potencialmente peligrosos
 */
void sanitize_string(char *dest, const char *src, size_t dest_size) {
    if (dest == NULL || src == NULL || dest_size == 0) {
        return;
    }
    
    size_t j = 0;
    size_t src_len = strlen(src);
    
    for (size_t i = 0; i < src_len && j < dest_size - 1; i++) {
        // Solo copiar caracteres seguros
        if (isalnum(src[i]) || src[i] == ' ' || 
            src[i] == '.' || src[i] == '-' || src[i] == '_') {
            dest[j++] = src[i];
        }
    }
    
    dest[j] = '\0';  // Asegurar terminación null
}

/**
 * Función para leer entrada de usuario de forma segura
 */
bool safe_read_input(char *buffer, size_t buffer_size, const char *prompt) {
    if (buffer == NULL || buffer_size == 0) {
        return false;
    }
    
    printf("%s", prompt);
    
    if (fgets(buffer, buffer_size, stdin) == NULL) {
        return false;
    }
    
    // Eliminar salto de línea
    size_t len = strlen(buffer);
    if (len > 0 && buffer[len - 1] == '\n') {
        buffer[len - 1] = '\0';
    }
    
    // Validar la entrada
    if (!validate_input(buffer)) {
        fprintf(stderr, "Error: Entrada contiene caracteres no válidos\n");
        return false;
    }
    
    return true;
}

/**
 * Función para copiar cadenas de forma segura
 */
bool safe_string_copy(char *dest, const char *src, size_t dest_size) {
    if (dest == NULL || src == NULL || dest_size == 0) {
        return false;
    }
    
    size_t src_len = strlen(src);
    if (src_len >= dest_size) {
        fprintf(stderr, "Error: Cadena de origen demasiado grande\n");
        return false;
    }
    
    // Copiar de forma segura
    for (size_t i = 0; i < src_len && i < dest_size - 1; i++) {
        dest[i] = src[i];
    }
    dest[src_len] = '\0';
    
    return true;
}

/**
 * Función para concatenar cadenas de forma segura
 */
bool safe_string_concat(char *dest, const char *src, size_t dest_size) {
    if (dest == NULL || src == NULL || dest_size == 0) {
        return false;
    }
    
    size_t dest_len = strlen(dest);
    size_t src_len = strlen(src);
    
    if (dest_len + src_len >= dest_size) {
        fprintf(stderr, "Error: No hay espacio suficiente para concatenar\n");
        return false;
    }
    
    // Concatenar de forma segura
    for (size_t i = 0; i < src_len && dest_len + i < dest_size - 1; i++) {
        dest[dest_len + i] = src[i];
    }
    dest[dest_len + src_len] = '\0';
    
    return true;
}

/**
 * Función para procesar datos de usuario de forma segura
 */
bool safe_process_user_data(const char *username, const char *email) {
    char sanitized_user[MAX_USERNAME_LENGTH];
    char sanitized_email[MAX_INPUT_LENGTH];
    char output_buffer[MAX_BUFFER_SIZE];
    
    // Validar entradas
    if (!validate_input(username) || !validate_input(email)) {
        fprintf(stderr, "Error: Datos de entrada no válidos\n");
        return false;
    }
    
    // Sanitizar datos
    sanitize_string(sanitized_user, username, sizeof(sanitized_user));
    sanitize_string(sanitized_email, email, sizeof(sanitized_email));
    
    // Construir mensaje de forma segura
    if (!safe_string_copy(output_buffer, "Usuario: ", sizeof(output_buffer))) {
        return false;
    }
    
    if (!safe_string_concat(output_buffer, sanitized_user, sizeof(output_buffer))) {
        return false;
    }
    
    if (!safe_string_concat(output_buffer, " | Email: ", sizeof(output_buffer))) {
        return false;
    }
    
    if (!safe_string_concat(output_buffer, sanitized_email, sizeof(output_buffer))) {
        return false;
    }
    
    // Usar formato fijo para evitar format string vulnerabilities
    printf("%s\n", output_buffer);
    
    return true;
}

/**
 * Función para validar y procesar archivos de forma segura
 */
bool safe_file_operation(const char *filename) {
    // Validar nombre de archivo
    if (!validate_input(filename)) {
        fprintf(stderr, "Error: Nombre de archivo no válido\n");
        return false;
    }
    
    // Verificar extensión permitida
    const char *extension = strrchr(filename, '.');
    if (extension == NULL || 
        (strcmp(extension, ".txt") != 0 && strcmp(extension, ".log") != 0)) {
        fprintf(stderr, "Error: Extensión de archivo no permitida\n");
        return false;
    }
    
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error al abrir archivo");
        return false;
    }
    
    char line[MAX_BUFFER_SIZE];
    int line_count = 0;
    
    while (fgets(line, sizeof(line), file) != NULL && line_count < 100) {
        // Procesar línea de forma segura
        line[strcspn(line, "\n")] = '\0';
        
        if (validate_input(line)) {
            printf("Línea %d: %s\n", ++line_count, line);
        }
    }
    
    fclose(file);
    return true;
}

/**
 * Función principal con validación exhaustiva
 */
int main(int argc, char *argv[]) {
    char username[MAX_USERNAME_LENGTH];
    char email[MAX_INPUT_LENGTH];
    
    printf("=== Sistema Ultra Seguro ===\n");
    printf("Implementación con validación exhaustiva\n\n");
    
    // Leer entrada de usuario de forma segura
    if (!safe_read_input(username, sizeof(username), "Ingrese nombre de usuario: ")) {
        fprintf(stderr, "Error al leer nombre de usuario\n");
        return 1;
    }
    
    if (!safe_read_input(email, sizeof(email), "Ingrese email: ")) {
        fprintf(stderr, "Error al leer email\n");
        return 1;
    }
    
    // Procesar datos de forma segura
    if (!safe_process_user_data(username, email)) {
        fprintf(stderr, "Error al procesar datos de usuario\n");
        return 1;
    }
    
    printf("\n=== Procesamiento completado exitosamente ===\n");
    printf("Características de seguridad implementadas:\n");
    printf("  ✓ Validación de entrada\n");
    printf("  ✓ Sanitización de datos\n");
    printf("  ✓ Límites de buffer estrictos\n");
    printf("  ✓ Manejo de errores robusto\n");
    printf("  ✓ Sin funciones peligrosas\n");
    printf("  ✓ Formato de salida seguro\n");
    
    return 0;
}
