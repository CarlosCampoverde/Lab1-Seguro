// TEST: Archivo para verificar el workflow del pipeline
// Este archivo contiene código VULNERABLE para probar la detección

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// VULNERABILIDAD: Buffer overflow con strcpy
void test_vulnerable_function(char *input) {
    char buffer[64];
    strcpy(buffer, input);  // PELIGRO: No verifica tamaño
    printf("Buffer: %s\n", buffer);
}

// VULNERABILIDAD: Uso de gets() (prohibido)
void test_gets_vulnerability() {
    char user_input[100];
    printf("Enter text: ");
    gets(user_input);  // PELIGRO: Buffer overflow garantizado
    printf("You entered: %s\n", user_input);
}

// VULNERABILIDAD: Command injection
void test_command_injection(char *filename) {
    char cmd[200];
    sprintf(cmd, "cat %s", filename);  // PELIGRO: No sanitiza input
    system(cmd);  // PELIGRO: Ejecuta comando del usuario
}

int main() {
    printf("=== TESTING SECURITY PIPELINE ===\n");
    printf("Este archivo debe ser detectado como VULNERABLE\n");
    printf("Probabilidad esperada: >85%%\n");
    
    // Este código nunca debe ejecutarse en producción
    // Solo es para demostración del scanner
    
    return 0;
}
