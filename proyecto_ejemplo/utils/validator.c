// ARCHIVO SEGURO - Validación y sanitización
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX_USERNAME_LENGTH 50
#define MAX_EMAIL_LENGTH 100

// Función segura: Validación de username
int validate_username(const char *username) {
    if (username == NULL) {
        return 0;
    }
    
    size_t len = strlen(username);
    
    // Verificar longitud
    if (len < 3 || len > MAX_USERNAME_LENGTH) {
        return 0;
    }
    
    // Verificar caracteres permitidos (solo alphanumeric y underscore)
    for (size_t i = 0; i < len; i++) {
        if (!isalnum(username[i]) && username[i] != '_') {
            return 0;
        }
    }
    
    return 1;
}

// Función segura: Validación de email
int validate_email(const char *email) {
    if (email == NULL) {
        return 0;
    }
    
    size_t len = strlen(email);
    
    // Verificar longitud
    if (len < 5 || len > MAX_EMAIL_LENGTH) {
        return 0;
    }
    
    // Verificar que tiene @
    const char *at = strchr(email, '@');
    if (at == NULL) {
        return 0;
    }
    
    // Verificar que tiene punto después del @
    const char *dot = strchr(at, '.');
    if (dot == NULL || dot == at + 1) {
        return 0;
    }
    
    // Verificar caracteres válidos
    for (size_t i = 0; i < len; i++) {
        char c = email[i];
        if (!isalnum(c) && c != '@' && c != '.' && c != '_' && c != '-') {
            return 0;
        }
    }
    
    return 1;
}

// Función segura: Sanitización de input SQL
void sanitize_sql_input(const char *input, char *output, size_t output_size) {
    if (input == NULL || output == NULL || output_size == 0) {
        return;
    }
    
    size_t j = 0;
    for (size_t i = 0; input[i] != '\0' && j < output_size - 1; i++) {
        char c = input[i];
        
        // Escapar caracteres peligrosos
        if (c == '\'' || c == '"' || c == '\\') {
            if (j < output_size - 2) {
                output[j++] = '\\';
                output[j++] = c;
            }
        } else if (isprint(c)) {
            output[j++] = c;
        }
    }
    output[j] = '\0';
}

// Función segura: Validación de path
int is_safe_path(const char *path) {
    if (path == NULL) {
        return 0;
    }
    
    // Rechazar paths con ../
    if (strstr(path, "../") != NULL || strstr(path, "..\\") != NULL) {
        return 0;
    }
    
    // Rechazar paths absolutos
    if (path[0] == '/' || (strlen(path) > 2 && path[1] == ':')) {
        return 0;
    }
    
    return 1;
}

// Función segura: Limitar longitud de string
void safe_string_copy(const char *src, char *dest, size_t dest_size) {
    if (src == NULL || dest == NULL || dest_size == 0) {
        return;
    }
    
    // SEGURO: strncpy con null termination garantizada
    strncpy(dest, src, dest_size - 1);
    dest[dest_size - 1] = '\0';
}

// Función segura: Validación de número de teléfono
int validate_phone(const char *phone) {
    if (phone == NULL) {
        return 0;
    }
    
    size_t len = strlen(phone);
    
    // Verificar longitud (10-15 dígitos)
    if (len < 10 || len > 15) {
        return 0;
    }
    
    // Verificar que solo contiene dígitos y caracteres permitidos
    for (size_t i = 0; i < len; i++) {
        if (!isdigit(phone[i]) && phone[i] != '+' && 
            phone[i] != '-' && phone[i] != ' ' && phone[i] != '(' && phone[i] != ')') {
            return 0;
        }
    }
    
    return 1;
}

// Función segura: Validación de rango numérico
int validate_range(int value, int min, int max) {
    return (value >= min && value <= max);
}
