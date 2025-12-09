#include <string.h>
void good() {
    char dest[50];
    strncpy(dest, "texto seguro", 49);
    dest[49] = '\0';
}