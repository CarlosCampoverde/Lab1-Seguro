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
    
    # Verificar features básicas que existen
    assert 'usa_strcpy' in features
    assert features['usa_strcpy'] == True
    assert 'func_peligrosas' in features
    assert features['func_peligrosas'] > 0

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
    
    # Verificar que no usa strcpy
    assert 'usa_strcpy' in features
    assert features['usa_strcpy'] == False

def test_extract_features_basic():
    """Test básico de extracción de features"""
    code = """
    def execute_code(user_input):
        result = eval(user_input)  # Vulnerable
        return result
    """
    
    features = extract_features(code)
    
    # Verificar que retorna un pandas Series con features básicas
    assert features is not None
    assert 'longitud' in features
    assert 'lineas' in features
    assert features['longitud'] > 0

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
    # Debe detectar estructuras de control
    assert 'complejidad_ciclomatica' in features
    assert features['complejidad_ciclomatica'] >= 1

def test_extract_features_returns_series():
    """Test que extract_features retorna una Serie de pandas"""
    code = "print('hello')"
    features = extract_features(code)
    
    # Verificar que es un objeto tipo Series
    assert hasattr(features, '__getitem__')
    assert len(features) > 0
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
