# 📱 PASO 2: Configurar Bot de Telegram

## Instrucciones Paso a Paso

### 1️⃣ Crear el Bot

1. Abre Telegram en tu teléfono o computadora
2. Busca el contacto: **@BotFather**
3. Envía el comando: `/newbot`
4. Bot Father te preguntará:
   - **Nombre del bot**: (ej: "Vulnerability Scanner Bot")
   - **Username del bot**: (debe terminar en 'bot', ej: "carlos_vulnscanner_bot")
5. **¡IMPORTANTE!** Copia el **TOKEN** que te da (parecido a):
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789
   ```

### 2️⃣ Obtener tu Chat ID

1. Busca el bot: **@userinfobot** en Telegram
2. Envía: `/start`
3. El bot te responderá con tu información
4. **Copia tu ID** (es un número, ej: `123456789`)

### 3️⃣ Probar Localmente

Abre PowerShell y ejecuta:

```powershell
# Configura las variables (REEMPLAZA con tus valores)
$env:TELEGRAM_BOT_TOKEN="1234567890:ABCdefGHI..."  # TU TOKEN
$env:TELEGRAM_CHAT_ID="123456789"                  # TU CHAT ID

# Probar notificación
python telegram_notifier.py --message "✅ Bot configurado correctamente!" --status "success"
```

Si recibes el mensaje en Telegram, **¡funciona!** ✅

### 4️⃣ Valores para Configurar

**Guarda estos valores (los necesitarás en el Paso 3):**

```
TELEGRAM_BOT_TOKEN=___________________________________________
TELEGRAM_CHAT_ID=______________
```

---

## ✅ Verificación

- [ ] Bot creado en @BotFather
- [ ] TOKEN copiado
- [ ] Chat ID obtenido de @userinfobot
- [ ] Prueba local exitosa (mensaje recibido)

**Cuando hayas completado esto, continúa con el Paso 3** ➡️

---

## 🆘 Problemas Comunes

**No recibo el mensaje de prueba:**
- Verifica que copiaste bien el TOKEN (completo, sin espacios)
- Verifica el CHAT_ID (es solo números)
- Asegúrate de haber iniciado conversación con tu bot (envíale /start primero)

**Error al ejecutar telegram_notifier.py:**
- Verifica que las variables de entorno están configuradas
- Verifica que estás usando el Python del .venv
