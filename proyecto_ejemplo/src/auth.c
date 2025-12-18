// ARCHIVO VULNERABLE - Sistema de autenticación
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "../include/auth.h"

// VULNERABILIDAD 1: Password hardcoded
#define ADMIN_PASSWORD "admin123"  // PELIGRO: Contraseña en código

// VULNERABILIDAD 2: Almacenamiento inseguro
char stored_passwords[100][50];  // PELIGRO: Passwords en plain text

// VULNERABILIDAD 3: Comparación insegura de passwords
int authenticate(char *username, char *password) {
    // PELIGRO: strcmp revela información por timing attack
    if (strcmp(username, "admin") == 0) {
        if (strcmp(password, ADMIN_PASSWORD) == 0) {
            return 1;
        }
    }
    
    // VULNERABILIDAD 4: SQL injection en verificación
    char query[200];
    sprintf(query, "SELECT * FROM users WHERE username='%s' AND password='%s'", 
            username, password);  // PELIGRO: SQL injection
    
    printf("Query: %s\n", query);
    
    return 0;
}

// VULNERABILIDAD 5: Función de reset password insegura
void reset_password(char *username, char *email) {
    char command[300];
    
    // PELIGRO: Command injection
    sprintf(command, "sendmail %s -s 'Password Reset'", email);
    system(command);
    
    // PELIGRO: Nueva password hardcoded
    char new_password[20] = "temp123";
    strcpy(stored_passwords[0], new_password);
}

// VULNERABILIDAD 6: Generación débil de tokens
char* generate_session_token(char *username) {
    static char token[50];
    
    // PELIGRO: Token predecible (solo timestamp)
    sprintf(token, "%s_%d", username, (int)time(NULL));
    
    return token;
}

// VULNERABILIDAD 7: Validación de permisos débil
int check_admin_access(char *username) {
    // PELIGRO: Usa strcmp sin validación previa
    if (strcmp(username, "admin") == 0 || strcmp(username, "root") == 0) {
        return 1;
    }
    return 0;
}
