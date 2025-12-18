// ARCHIVO VULNERABLE - Punto de entrada del sistema
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../include/auth.h"
#include "../include/database.h"

// VULNERABILIDAD 1: Buffer overflow con gets()
void get_username(char *username) {
    printf("Enter username: ");
    gets(username);  // PELIGRO: Buffer overflow
}

// VULNERABILIDAD 2: Buffer overflow con strcpy()
void copy_data(char *source) {
    char destination[50];
    strcpy(destination, source);  // PELIGRO: No verifica tamaño
    printf("Data copied: %s\n", destination);
}

// VULNERABILIDAD 3: Command injection con system()
void execute_backup(char *filename) {
    char command[200];
    sprintf(command, "backup.sh %s", filename);  // PELIGRO: No sanitiza
    system(command);  // PELIGRO: Ejecuta comando del usuario
}

// VULNERABILIDAD 4: Format string vulnerability
void log_user_activity(char *activity) {
    printf(activity);  // PELIGRO: Format string attack
}

int main(int argc, char *argv[]) {
    char username[100];
    char password[100];
    
    printf("=== Sistema de Gestión de Usuarios ===\n\n");
    
    // Login vulnerable
    get_username(username);
    
    printf("Enter password: ");
    gets(password);  // PELIGRO: Otro gets()
    
    // Autenticar (función vulnerable en auth.c)
    if (authenticate(username, password)) {
        printf("Login successful!\n");
        
        // Operaciones de base de datos (vulnerable en database.c)
        get_user_data(username);
        
        // Ejecutar backup (vulnerable)
        execute_backup(username);
        
        // Log activity (vulnerable)
        log_user_activity(username);
    } else {
        printf("Login failed!\n");
    }
    
    return 0;
}
