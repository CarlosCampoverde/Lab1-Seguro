/**
 * EJEMPLO DE CÓDIGO VULNERABLE
 * Este archivo contiene múltiples vulnerabilidades de seguridad
 * para probar el sistema de detección
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Función vulnerable a buffer overflow
void copy_user_input() {
    char buffer[50];
    char user_data[200];
    
    printf("Ingrese su nombre: ");
    gets(user_data);  // VULNERABLE: gets() no verifica límites
    
    strcpy(buffer, user_data);  // VULNERABLE: strcpy() sin validación de tamaño
    printf("Hola, %s\n", buffer);
}

// Función vulnerable a command injection
void execute_command(char *filename) {
    char cmd[256];
    
    sprintf(cmd, "cat %s", filename);  // VULNERABLE: sprintf() puede causar overflow
    system(cmd);  // VULNERABLE: ejecución de comandos sin sanitización
}

// Función con múltiples problemas de memoria
void process_data(char *input) {
    char temp[100];
    char result[50];
    
    // Sin validación de longitud
    strcpy(temp, input);  // VULNERABLE
    strcat(temp, "_processed");  // VULNERABLE
    
    // Uso peligroso de scanf
    scanf("%s", result);  // VULNERABLE: sin límite de tamaño
    
    memcpy(result, temp, 100);  // VULNERABLE: puede copiar más allá del límite
}

// Función con problemas de formato de cadena
void log_message(char *user_msg) {
    printf(user_msg);  // VULNERABLE: format string vulnerability
}

int main() {
    char *dangerous_input = "A" * 300;  // Entrada muy grande
    
    copy_user_input();
    execute_command("/etc/passwd");
    process_data(dangerous_input);
    log_message("%s%s%s%s");
    
    return 0;
}
