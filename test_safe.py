"""
Archivo de prueba - código SEGURO
Este archivo activa el pipeline por primera vez
"""

def greet(name):
    """Función segura de saludo"""
    return f"Hello, {name}!"

def add_numbers(a, b):
    """Suma dos números de forma segura"""
    return a + b

if __name__ == "__main__":
    print(greet("Pipeline CI/CD"))
    print(f"2 + 2 = {add_numbers(2, 2)}")
