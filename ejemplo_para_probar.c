// EJEMPLO DE CÓDIGO VULNERABLE PARA PROBAR EL PIPELINE
// Este archivo contiene VARIAS vulnerabilidades intencionales

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Vulnerabilidad 1: Buffer Overflow con strcpy
void vulnerable_strcpy(char *user_input) {
    char buffer[10];
    strcpy(buffer, user_input);  // PELIGRO: No verifica tamaño
    printf("Buffer: %s\n", buffer);
}

// Vulnerabilidad 2: SQL Injection
void vulnerable_sql(char *username) {
    char query[200];
    sprintf(query, "SELECT * FROM users WHERE name='%s'", username);  // PELIGRO: Concatenación directa
    printf("Query: %s\n", query);
}

// Vulnerabilidad 3: Command Injection con system()
void vulnerable_system(char *filename) {
    char command[100];
    sprintf(command, "cat %s", filename);  // PELIGRO: No sanitiza input
    system(command);  // PELIGRO: Ejecuta comando del usuario
}

// Vulnerabilidad 4: Gets (función prohibida)
void vulnerable_gets() {
    char password[20];
    printf("Enter password: ");
    gets(password);  // PELIGRO: Buffer overflow garantizado
    printf("Password: %s\n", password);
}

// Vulnerabilidad 5: Format String
void vulnerable_format(char *user_string) {
    printf(user_string);  // PELIGRO: Format string vulnerability
}

int main() {
    char input[100];
    
    printf("Testing vulnerable code...\n");
    
    // Llamadas inseguras
    vulnerable_strcpy("Este texto es demasiado largo y causará overflow");
    vulnerable_sql("admin' OR '1'='1");
    vulnerable_system("../../etc/passwd");
    vulnerable_gets();
    vulnerable_format("%s%s%s%s%s");
    
    return 0;
}
