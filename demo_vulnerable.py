"""
CÓDIGO VULNERABLE - Demostración de detección por IA
Este archivo contiene múltiples vulnerabilidades intencionales
"""

import pickle
import os

def load_data_unsafe(filename):
    """VULNERABLE: Deserialización insegura con pickle"""
    with open(filename, 'rb') as f:
        data = pickle.loads(f.read())  # ⚠️ VULNERABILIDAD
    return data

def execute_command(user_input):
    """VULNERABLE: Ejecución de comandos sin validación"""
    os.system(user_input)  # ⚠️ VULNERABILIDAD

def eval_expression(expression):
    """VULNERABLE: Evaluación dinámica de código"""
    result = eval(expression)  # ⚠️ VULNERABILIDAD
    return result

class DatabaseConnector:
    def query(self, user_query):
        """VULNERABLE: SQL Injection potencial"""
        sql = f"SELECT * FROM users WHERE name = '{user_query}'"  # ⚠️ VULNERABILIDAD
        return sql

if __name__ == "__main__":
    # Este código debería ser bloqueado por el pipeline
    print("⚠️ Este archivo contiene código vulnerable")
