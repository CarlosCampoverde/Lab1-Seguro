#include <string.h>
void bad() {
    char dest[10];
    strcpy(dest, "esto es mucho más largo de 10"); // ¡Vulnerabilidad clara!
}