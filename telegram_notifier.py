#!/usr/bin/env python3
"""
📱 Telegram Notifier para CI/CD Pipeline
Envía notificaciones de todas las fases del pipeline
"""

import argparse
import os
import sys
import requests
import json
from datetime import datetime

class TelegramNotifier:
    def __init__(self, bot_token=None, chat_id=None):
        """Inicializar notificador"""
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or os.getenv('TELEGRAM_CHAT_ID')
        
        if not self.bot_token or not self.chat_id:
            raise ValueError("❌ TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID deben estar configurados")
        
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_message(self, message, status='info', url=None):
        """
        Envía mensaje a Telegram
        
        Args:
            message: Texto del mensaje
            status: 'success', 'error', 'warning', 'info'
            url: URL opcional para incluir
        """
        # Emojis según estado
        emoji_map = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        }
        
        emoji = emoji_map.get(status, 'ℹ️')
        
        # Formatear mensaje
        formatted_message = f"{emoji} **CI/CD Pipeline**\n\n"
        formatted_message += f"{message}\n\n"
        formatted_message += f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        if url:
            formatted_message += f"\n\n🔗 [Ver más]({url})"
        
        # Enviar
        try:
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    'chat_id': self.chat_id,
                    'text': formatted_message,
                    'parse_mode': 'Markdown'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ Notificación enviada a Telegram")
                return True
            else:
                print(f"⚠️ Error al enviar notificación: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error de conexión con Telegram: {e}")
            return False
    
    def send_file(self, file_path, caption=''):
        """Envía un archivo (JSON de resultados, por ejemplo)"""
        try:
            with open(file_path, 'rb') as f:
                response = requests.post(
                    f"{self.api_url}/sendDocument",
                    data={
                        'chat_id': self.chat_id,
                        'caption': caption
                    },
                    files={'document': f},
                    timeout=30
                )
            
            if response.status_code == 200:
                print(f"✅ Archivo enviado a Telegram")
                return True
            else:
                print(f"⚠️ Error al enviar archivo: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error al enviar archivo: {e}")
            return False
    
    def send_vulnerability_alert(self, scan_results_path):
        """Envía alerta detallada de vulnerabilidades"""
        try:
            with open(scan_results_path, 'r') as f:
                results = json.load(f)
            
            if not results.get('has_vulnerabilities'):
                return self.send_message("✅ No se detectaron vulnerabilidades", status='success')
            
            # Mensaje detallado
            message = "🚨 **VULNERABILIDADES DETECTADAS**\n\n"
            message += f"📊 **Resumen:**\n"
            message += f"   • Total archivos: {results['total_files']}\n"
            message += f"   • Vulnerables: {results['vulnerable']}\n"
            message += f"   • Seguros: {results['safe']}\n\n"
            
            message += "⚠️ **Archivos afectados:**\n"
            for vuln in results['vulnerabilities'][:5]:  # Máximo 5 para no saturar
                message += f"\n📄 `{vuln['file']}`\n"
                message += f"   Tipo: {vuln['type']}\n"
                message += f"   Probabilidad: {vuln['probability']:.1f}%\n"
                message += f"   Razón: {vuln['reason'][:100]}...\n"
            
            if len(results['vulnerabilities']) > 5:
                message += f"\n... y {len(results['vulnerabilities']) - 5} más\n"
            
            message += f"\n🔒 **Acción requerida:** Corregir vulnerabilidades antes de merge"
            
            # Enviar mensaje
            self.send_message(message, status='error')
            
            # Enviar archivo JSON completo
            self.send_file(scan_results_path, caption='Resultados completos del análisis')
            
            return True
            
        except Exception as e:
            print(f"❌ Error al procesar resultados: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='📱 Telegram Notifier para CI/CD')
    parser.add_argument('--message', required=True, help='Mensaje a enviar')
    parser.add_argument('--status', default='info', 
                       choices=['success', 'error', 'warning', 'info'],
                       help='Estado del mensaje')
    parser.add_argument('--url', help='URL opcional')
    parser.add_argument('--file', help='Archivo JSON de resultados (para alertas de vulnerabilidad)')
    
    args = parser.parse_args()
    
    try:
        notifier = TelegramNotifier()
        
        if args.file:
            # Es una alerta de vulnerabilidad con archivo
            success = notifier.send_vulnerability_alert(args.file)
        else:
            # Mensaje simple
            success = notifier.send_message(args.message, status=args.status, url=args.url)
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
