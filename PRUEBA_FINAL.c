// PRUEBA FINAL: Código VULNERABLE para demostrar el pipeline
// Este archivo debe ser detectado y BLOQUEAR el PR

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// VULNERABILIDAD 1: Buffer overflow con gets()
void prueba_gets() {
    char password[20];
    printf("Ingrese password: ");
    gets(password);  // CRÍTICO: Buffer overflow garantizado
    printf("Password: %s\n", password);
}

// VULNERABILIDAD 2: SQL Injection
void prueba_sql_injection(char *username) {
    char query[200];
    sprintf(query, "DELETE FROM users WHERE name='%s'", username);
    printf("Ejecutando: %s\n", query);
}

// VULNERABILIDAD 3: Command Injection
void prueba_command_injection(char *filename) {
    char cmd[150];
    sprintf(cmd, "rm -rf %s", filename);
    system(cmd);  // PELIGRO: Ejecuta comando del usuario
}

// VULNERABILIDAD 4: Buffer overflow con strcpy
void prueba_strcpy(char *input) {
    char buffer[32];
    strcpy(buffer, input);  // Sin verificar tamaño
}

int main() {
    printf("=== PRUEBA FINAL DEL PIPELINE ===\n");
    printf("Este código contiene 4 vulnerabilidades críticas:\n");
    printf("1. gets() - Buffer overflow\n");
    printf("2. SQL injection - sprintf sin sanitización\n");
    printf("3. Command injection - system() con input usuario\n");
    printf("4. strcpy() - Buffer overflow\n");
    printf("\n");
    printf("RESULTADO ESPERADO:\n");
    printf("- Scanner debe detectar como VULNERABLE (>90%%)\n");
    printf("- Workflow debe FALLAR\n");
    printf("- PR debe ser BLOQUEADO\n");
    printf("- Notificación Telegram debe enviarse\n");
    
    return 0;
}
