#!/usr/bin/env python3
"""
🧪 Tests para el vulnerability scanner
"""

import pytest
import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from predict_vulnerabilities import extract_features
from ci_security_scanner import CISecurityScanner

def test_extract_features_vulnerable_c():
    """Test de extracción de features de código C vulnerable"""
    code = """
    #include <string.h>
    void vulnerable() {
        char buffer[64];
        strcpy(buffer, user_input);  // Vulnerable
    }
    """
    
    features = extract_features(code)
    
    assert features['usa_strcpy'] == True
    assert features['func_peligrosas_c'] > 0
    assert features['total_peligrosas'] > 0
    assert features['sanitizacion'] == False

def test_extract_features_safe_c():
    """Test de extracción de features de código C seguro"""
    code = """
    #include <string.h>
    #define MAX_SIZE 64
    
    void safe_function(const char* input) {
        char buffer[MAX_SIZE];
        if (input == NULL) return;
        
        strncpy(buffer, input, MAX_SIZE - 1);
        buffer[MAX_SIZE - 1] = '\\0';
    }
    """
    
    features = extract_features(code)
    
    assert features['usa_strcpy'] == False
    assert features['sanitizacion'] == True
    assert features['tiene_validacion_null'] == True

def test_extract_features_python_vulnerable():
    """Test de código Python con eval"""
    code = """
    def execute_code(user_input):
        result = eval(user_input)  # Vulnerable
        return result
    """
    
    features = extract_features(code)
    
    assert features['usa_eval'] == True
    assert features['func_peligrosas_python'] > 0
    assert features['es_python'] == 1

def test_scanner_initialization():
    """Test de inicialización del scanner"""
    # Este test requiere que existan los archivos del modelo
    if os.path.exists('xgboost_vulnerabilidades.pkl'):
        scanner = CISecurityScanner()
        assert scanner.model is not None
        assert scanner.vectorizer is not None

def test_complexity_calculation():
    """Test de cálculo de complejidad ciclomática"""
    code = """
    if (condition1) {
        for (int i = 0; i < 10; i++) {
            while (condition2) {
                if (condition3) {
                    // code
                }
            }
        }
    }
    """
    
    features = extract_features(code)
    # Debe detectar: if, for, while, if = 4
    assert features['complejidad_ciclomatica'] >= 4

def test_language_detection():
    """Test de detección de lenguaje"""
    
    # Python
    py_code = "def function():\n    print('hello')"
    py_features = extract_features(py_code)
    assert py_features['es_python'] == 1
    
    # JavaScript
    js_code = "const func = () => { console.log('test'); }"
    js_features = extract_features(js_code)
    assert js_features['es_javascript'] == 1
    
    # Java
    java_code = "public class Test { private void method() {} }"
    java_features = extract_features(java_code)
    assert java_features['es_java'] == 1

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
