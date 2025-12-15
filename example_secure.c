/**
 * EJEMPLO DE CÓDIGO SEGURO
 * Este archivo implementa buenas prácticas de seguridad
 * para contrastar con el código vulnerable
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#define MAX_INPUT_SIZE 100
#define MAX_BUFFER_SIZE 256

// Función segura para copiar entrada del usuario
void safe_copy_user_input() {
    char buffer[MAX_BUFFER_SIZE];
    char user_data[MAX_INPUT_SIZE];
    
    printf("Ingrese su nombre: ");
    
    // Uso seguro: fgets con límite de tamaño
    if (fgets(user_data, sizeof(user_data), stdin) != NULL) {
        // Eliminar el salto de línea
        user_data[strcspn(user_data, "\n")] = 0;
        
        // Validar longitud antes de copiar
        if (strlen(user_data) < sizeof(buffer)) {
            // Uso seguro: strncpy con límite
            strncpy(buffer, user_data, sizeof(buffer) - 1);
            buffer[sizeof(buffer) - 1] = '\0';  // Asegurar terminación null
            printf("Hola, %s\n", buffer);
        } else {
            printf("Error: Entrada demasiado larga\n");
        }
    }
}

// Función para sanitizar nombres de archivo
int validate_filename(const char *filename) {
    if (filename == NULL || strlen(filename) == 0) {
        return 0;
    }
    
    // Verificar caracteres peligrosos
    const char *dangerous_chars = ";|&$`<>(){}[]!";
    for (int i = 0; filename[i] != '\0'; i++) {
        if (strchr(dangerous_chars, filename[i]) != NULL) {
            return 0;  // Carácter peligroso encontrado
        }
    }
    
    return 1;  // Filename seguro
}

// Función segura para procesar archivos
void safe_read_file(const char *filename) {
    if (!validate_filename(filename)) {
        printf("Error: Nombre de archivo no válido\n");
        return;
    }
    
    // Abrir archivo de forma segura
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error al abrir archivo");
        return;
    }
    
    char line[MAX_BUFFER_SIZE];
    while (fgets(line, sizeof(line), file) != NULL) {
        // Procesar línea de forma segura
        printf("%s", line);
    }
    
    fclose(file);
}

// Función segura para procesar datos
void safe_process_data(const char *input) {
    if (input == NULL) {
        printf("Error: Entrada nula\n");
        return;
    }
    
    size_t input_len = strlen(input);
    if (input_len >= MAX_BUFFER_SIZE) {
        printf("Error: Entrada excede el tamaño máximo\n");
        return;
    }
    
    char temp[MAX_BUFFER_SIZE];
    char result[MAX_BUFFER_SIZE];
    
    // Copia segura con validación
    strncpy(temp, input, sizeof(temp) - 1);
    temp[sizeof(temp) - 1] = '\0';
    
    // Concatenación segura
    const char *suffix = "_processed";
    if (strlen(temp) + strlen(suffix) < sizeof(temp)) {
        strncat(temp, suffix, sizeof(temp) - strlen(temp) - 1);
    }
    
    // Lectura segura con límite
    if (scanf("%99s", result) == 1) {
        printf("Resultado procesado: %s\n", temp);
    }
}

// Función segura para logging con formato fijo
void safe_log_message(const char *user_msg) {
    if (user_msg == NULL) {
        return;
    }
    
    // Usar formato fijo para evitar format string vulnerability
    printf("%s\n", user_msg);
}

// Función auxiliar para limpiar buffer de entrada
void clear_input_buffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

int main() {
    printf("=== Ejemplo de Código Seguro ===\n\n");
    
    safe_copy_user_input();
    
    const char *safe_filename = "data.txt";
    safe_read_file(safe_filename);
    
    const char *test_input = "Test data for processing";
    safe_process_data(test_input);
    
    safe_log_message("Sistema funcionando correctamente");
    
    printf("\n=== Ejecución completada sin vulnerabilidades ===\n");
    
    return 0;
}
