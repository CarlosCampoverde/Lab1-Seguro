# Ejemplo de código Python VULNERABLE
# Contiene múltiples vulnerabilidades de seguridad

import pickle
import os

def procesar_datos_usuario(datos_serializados):
    # VULNERABILIDAD 1: Deserialización insegura
    objeto = pickle.loads(datos_serializados)
    return objeto

def ejecutar_comando(comando):
    # VULNERABILIDAD 2: Ejecución de comandos sin sanitización
    resultado = os.system(comando)
    return resultado

def evaluar_expresion(expresion):
    # VULNERABILIDAD 3: Uso de eval sin validación
    resultado = eval(expresion)
    return resultado

if __name__ == "__main__":
    # Uso inseguro de las funciones
    datos_usuario = input("Ingrese datos: ")
    ejecutar_comando(datos_usuario)
    resultado = evaluar_expresion(datos_usuario)
    print(f"Resultado: {resultado}")
