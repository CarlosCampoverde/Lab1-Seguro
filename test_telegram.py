import requests

TOKEN = "8350995822:AAGqGedj7xH6mE_2zjBPoNVcfCRVTvcjekk"
CHAT_ID = "8043865676"

url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
response = requests.post(url, json={
    'chat_id': CHAT_ID,
    'text': '✅ Bot de Telegram configurado correctamente!\n\n🤖 Pipeline CI/CD Lab1\n📊 Sistema de detección de vulnerabilidades\n\nEl bot está listo para enviar notificaciones.'
})

if response.status_code == 200:
    print('✅ Mensaje enviado exitosamente a Telegram!')
    print(f'📱 Verifica tu Telegram (Chat ID: {CHAT_ID})')
else:
    print(f'❌ Error: {response.text}')
