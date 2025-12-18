#ifndef DATABASE_H
#define DATABASE_H

// Funciones de base de datos
void get_user_data(char *username);
void update_user_email(char *username, char *new_email);
void delete_user(char *username);
void create_user(char *username, char *email, char *role);
void backup_database(char *backup_path);
void export_user_data(char *username, char *output_file);
void search_users(char *search_term);

#endif
