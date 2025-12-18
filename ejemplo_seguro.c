// EJEMPLO DE CÓDIGO SEGURO PARA COMPARACIÓN
// Este archivo usa prácticas seguras

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Versión segura: strncpy con límite
void secure_strcpy(const char *user_input, size_t max_len) {
    char buffer[100];
    strncpy(buffer, user_input, max_len - 1);
    buffer[max_len - 1] = '\0';  // Asegurar null termination
    printf("Buffer seguro: %s\n", buffer);
}

// Versión segura: Prepared statements (simulado)
void secure_sql(const char *username) {
    // En producción: usar prepared statements
    // Aquí solo validamos input
    if (strlen(username) > 50) {
        printf("Error: Username too long\n");
        return;
    }
    
    // Validar caracteres permitidos
    for (size_t i = 0; i < strlen(username); i++) {
        if (!isalnum(username[i]) && username[i] != '_') {
            printf("Error: Invalid characters\n");
            return;
        }
    }
    
    printf("Executing safe query for user: %s\n", username);
}

// Versión segura: Lista blanca de archivos permitidos
void secure_file_access(const char *filename) {
    const char *allowed_files[] = {"file1.txt", "file2.txt", NULL};
    
    for (int i = 0; allowed_files[i] != NULL; i++) {
        if (strcmp(filename, allowed_files[i]) == 0) {
            printf("Access granted to: %s\n", filename);
            return;
        }
    }
    
    printf("Access denied: File not in whitelist\n");
}

// Versión segura: fgets en lugar de gets
void secure_input() {
    char password[20];
    printf("Enter password: ");
    
    if (fgets(password, sizeof(password), stdin) != NULL) {
        // Remover newline
        password[strcspn(password, "\n")] = '\0';
        printf("Password received securely\n");
    }
}

int main() {
    printf("Testing secure code...\n");
    
    secure_strcpy("Input seguro", 100);
    secure_sql("usuario_valido");
    secure_file_access("file1.txt");
    secure_input();
    
    return 0;
}
