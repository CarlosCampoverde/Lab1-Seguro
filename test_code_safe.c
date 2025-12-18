// Código SEGURO para probar el pipeline
// Este archivo debería pasar el análisis de seguridad

#include <stdio.h>
#include <string.h>

#define MAX_SIZE 100

int main() {
    char buffer[MAX_SIZE];
    char name[MAX_SIZE];
    
    // Uso seguro de fgets en lugar de gets
    printf("Ingrese su nombre: ");
    if (fgets(name, MAX_SIZE, stdin) != NULL) {
        // Eliminar el newline
        name[strcspn(name, "\n")] = 0;
    }
    
    // Uso seguro de snprintf en lugar de sprintf
    snprintf(buffer, MAX_SIZE, "Hola, %s!", name);
    printf("%s\n", buffer);
    
    // Copia segura con strncpy
    char dest[MAX_SIZE];
    strncpy(dest, buffer, MAX_SIZE - 1);
    dest[MAX_SIZE - 1] = '\0';
    
    printf("Mensaje copiado: %s\n", dest);
    
    return 0;
}
