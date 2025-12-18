// ARCHIVO SEGURO - Sistema de logging
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_LOG_LENGTH 1024
#define MAX_FILENAME_LENGTH 256

// Función segura: Uso correcto de snprintf
void log_message(const char *level, const char *message) {
    char log_entry[MAX_LOG_LENGTH];
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    
    // SEGURO: snprintf previene buffer overflow
    snprintf(log_entry, sizeof(log_entry), 
             "[%04d-%02d-%02d %02d:%02d:%02d] [%s] %s\n",
             t->tm_year + 1900, t->tm_mon + 1, t->tm_mday,
             t->tm_hour, t->tm_min, t->tm_sec,
             level, message);
    
    // Escribir a archivo de forma segura
    FILE *fp = fopen("application.log", "a");
    if (fp != NULL) {
        fputs(log_entry, fp);
        fclose(fp);
    }
}

// Función segura: Validación de nivel de log
int is_valid_log_level(const char *level) {
    const char *valid_levels[] = {"DEBUG", "INFO", "WARN", "ERROR", NULL};
    
    for (int i = 0; valid_levels[i] != NULL; i++) {
        if (strcmp(level, valid_levels[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

// Función segura: Lectura segura de input
void read_log_query(char *buffer, size_t buffer_size) {
    printf("Enter search term: ");
    
    // SEGURO: fgets con límite de tamaño
    if (fgets(buffer, buffer_size, stdin) != NULL) {
        // Remover newline si existe
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len - 1] == '\n') {
            buffer[len - 1] = '\0';
        }
    }
}

// Función segura: Sanitización de nombres de archivo
int sanitize_filename(const char *input, char *output, size_t output_size) {
    if (input == NULL || output == NULL || output_size == 0) {
        return 0;
    }
    
    size_t j = 0;
    for (size_t i = 0; input[i] != '\0' && j < output_size - 1; i++) {
        char c = input[i];
        
        // Solo permitir caracteres seguros
        if ((c >= 'a' && c <= 'z') || 
            (c >= 'A' && c <= 'Z') || 
            (c >= '0' && c <= '9') || 
            c == '_' || c == '-' || c == '.') {
            output[j++] = c;
        }
    }
    output[j] = '\0';
    
    return 1;
}

// Función segura: Rotación de logs con validación
void rotate_logs(const char *log_filename) {
    char safe_filename[MAX_FILENAME_LENGTH];
    char new_filename[MAX_FILENAME_LENGTH];
    
    // SEGURO: Sanitizar nombre de archivo
    if (!sanitize_filename(log_filename, safe_filename, sizeof(safe_filename))) {
        log_message("ERROR", "Invalid log filename");
        return;
    }
    
    // SEGURO: snprintf para construir path
    time_t now = time(NULL);
    snprintf(new_filename, sizeof(new_filename), 
             "%s.%ld.bak", safe_filename, (long)now);
    
    // Renombrar archivo
    if (rename(safe_filename, new_filename) == 0) {
        log_message("INFO", "Log rotated successfully");
    }
}
