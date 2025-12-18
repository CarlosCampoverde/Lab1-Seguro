# Ejemplo de código Python SEGURO
# Implementa validaciones y prácticas seguras

import json
import subprocess
import re

def procesar_datos_usuario(datos_json):
    # Uso seguro: JSON en lugar de pickle
    try:
        objeto = json.loads(datos_json)
        return objeto
    except json.JSONDecodeError:
        return None

def ejecutar_comando_seguro(comando):
    # Validación y lista blanca de comandos
    comandos_permitidos = ['ls', 'pwd', 'date']
    
    if comando not in comandos_permitidos:
        raise ValueError("Comando no permitido")
    
    # Uso de subprocess con lista (más seguro que shell=True)
    resultado = subprocess.run([comando], capture_output=True, text=True)
    return resultado.stdout

def validar_entrada(entrada):
    # Sanitización de entrada
    patron = r'^[a-zA-Z0-9\s]+$'
    if re.match(patron, entrada):
        return True
    return False

if __name__ == "__main__":
    datos_usuario = input("Ingrese datos: ")
    
    # Validar antes de procesar
    if validar_entrada(datos_usuario):
        print(f"Datos válidos: {datos_usuario}")
    else:
        print("Datos inválidos rechazados")
