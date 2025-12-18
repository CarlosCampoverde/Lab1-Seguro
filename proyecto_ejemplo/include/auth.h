#ifndef AUTH_H
#define AUTH_H

// Funciones de autenticación
int authenticate(char *username, char *password);
void reset_password(char *username, char *email);
char* generate_session_token(char *username);
int check_admin_access(char *username);

#endif
