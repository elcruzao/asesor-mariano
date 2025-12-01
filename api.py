from http.server import BaseHTTPRequestHandler
import asyncio
import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- AQUÍ PEGA TU TOKEN ---
TOKEN = "TOKEN = "7893181294:AAFV5mZpvEnMGob_Lq_pilhFTIboAZHQAvk" 
# ---------------------------

# La función que responde a los comandos (Igual que antes)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    user_first_name = update.effective_user.first_name

    if not args:
        await update.message.reply_text(f"¡Hola {user_first_name}! 👋 Soy el Asesor de Mariano. Usa la web para consultarme.")
        return

    payload = args[0].lower()

    if payload == "consulta":
        await update.message.reply_text(f"¡Hola {user_first_name}! 👋 Vienes por una **Consulta**. ¿En qué puedo ayudarte?")
    elif payload == "servicios":
        await update.message.reply_text(f"¡Bienvenido {user_first_name}! 👋 Aquí nuestros **Servicios**:\n1. 💅 Manicura\n2. 🚗 Taller\n3. 🍞 Panadería")
    elif payload == "soporte":
        await update.message.reply_text(f"🚨 **Soporte Técnico**\n\nDime {user_first_name}, ¿qué problema tienes?")
    else:
        await update.message.reply_text("¡Hola! Gracias por contactarnos.")

# La Clase que maneja la conexión con Vercel
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Recibir el mensaje de Telegram
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        json_data = json.loads(post_data.decode('utf-8'))

        async def main():
            # 2. Configurar el bot (se crea y se destruye en cada mensaje para ahorrar memoria)
            app = ApplicationBuilder().token(TOKEN).build()
            app.add_handler(CommandHandler('start', start))
            
            # 3. Procesar la actualización
            await app.initialize()
            update = Update.de_json(json_data, app.bot)
            await app.process_update(update)
            await app.shutdown()

        # 4. Ejecutar todo
        try:
            asyncio.run(main())
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            print(f"Error: {e}")

    def do_GET(self):
        # Por si entras al link desde el navegador para probar
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"El bot esta activo esperando a Telegram.")