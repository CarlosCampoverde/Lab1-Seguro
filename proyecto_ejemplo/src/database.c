// ARCHIVO VULNERABLE - Operaciones de base de datos
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../include/database.h"

// VULNERABILIDAD 1: SQL injection en SELECT
void get_user_data(char *username) {
    char query[500];
    
    // PELIGRO: Concatenación directa de input del usuario
    sprintf(query, "SELECT * FROM users WHERE username='%s'", username);
    
    printf("Executing query: %s\n", query);
    // En producción esto ejecutaría: sql_execute(query);
}

// VULNERABILIDAD 2: SQL injection en UPDATE
void update_user_email(char *username, char *new_email) {
    char query[500];
    
    // PELIGRO: Sin prepared statements
    sprintf(query, "UPDATE users SET email='%s' WHERE username='%s'", 
            new_email, username);
    
    printf("Executing: %s\n", query);
}

// VULNERABILIDAD 3: SQL injection en DELETE
void delete_user(char *username) {
    char query[300];
    
    // PELIGRO: Vulnerable a: ' OR '1'='1
    sprintf(query, "DELETE FROM users WHERE username='%s'", username);
    
    printf("Deleting user: %s\n", query);
}

// VULNERABILIDAD 4: SQL injection en INSERT
void create_user(char *username, char *email, char *role) {
    char query[600];
    
    // PELIGRO: Tres parámetros sin sanitizar
    sprintf(query, "INSERT INTO users (username, email, role) VALUES ('%s', '%s', '%s')",
            username, email, role);
    
    printf("Creating user: %s\n", query);
}

// VULNERABILIDAD 5: Command injection en backup
void backup_database(char *backup_path) {
    char command[400];
    
    // PELIGRO: Path controlado por usuario
    sprintf(command, "mysqldump -u root database > %s", backup_path);
    system(command);
}

// VULNERABILIDAD 6: Path traversal
void export_user_data(char *username, char *output_file) {
    char filepath[200];
    
    // PELIGRO: No valida ../ en output_file
    sprintf(filepath, "/data/exports/%s", output_file);
    
    FILE *fp = fopen(filepath, "w");
    if (fp) {
        fprintf(fp, "User data for: %s\n", username);
        fclose(fp);
    }
}

// VULNERABILIDAD 7: Buffer overflow en búsqueda
void search_users(char *search_term) {
    char buffer[50];
    char query[200];
    
    // PELIGRO: strcpy sin verificar tamaño
    strcpy(buffer, search_term);
    
    // PELIGRO: SQL injection también
    sprintf(query, "SELECT * FROM users WHERE name LIKE '%%%s%%'", buffer);
    
    printf("Search query: %s\n", query);
}
