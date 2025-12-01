import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Configuración básica para ver errores si algo falla
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Aquí capturamos los argumentos (lo que viene después del /start)
    # args es una lista. Si el link es ...?start=consulta, args[0] será "consulta"
    args = context.args
    
    # Usuario que nos habla
    user_first_name = update.effective_user.first_name

    # Si NO hay argumentos (el usuario entró al bot directamente, sin la web)
    if not args:
        await update.message.reply_text(
            f"¡Hola {user_first_name}! 👋 Soy el Asesor de Mariano.\n"
            "Escribe /ayuda para ver qué puedo hacer."
        )
        return

    # Si SÍ hay argumentos, miramos cuál es
    payload = args[0].lower() # Lo convertimos a minúsculas por seguridad

    if payload == "consulta":
        await update.message.reply_text(
            f"¡Hola {user_first_name}! 👋 Veo que vienes desde la web para hacer una **Consulta**.\n\n"
            "Cuéntame, ¿cuál es tu duda hoy?"
        )
        
    elif payload == "servicios":
        await update.message.reply_text(
            f"¡Bienvenido {user_first_name}! 👋 Aquí tienes nuestros **Servicios**:\n\n"
            "1. 💅 Gestión para Manicuras\n"
            "2. 🚗 Turnos para Talleres\n"
            "3. 🍞 Pedidos para Panaderías\n\n"
            "¿Cuál te interesa?"
        )
        
    elif payload == "soporte":
        await update.message.reply_text(
            f"🚨 **Soporte Técnico**\n\n"
            "Dime {user_first_name}, ¿qué problema estás teniendo? Estoy aquí para ayudarte."
        )
        
    else:
        # Por si ponen un link raro que no conocemos
        await update.message.reply_text("¡Hola! Gracias por contactarnos.")

if __name__ == '__main__':
    # AQUÍ PEGARÁS TU TOKEN DE BOTFATHER
    TOKEN = "TU_TOKEN_AQUI"
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Le decimos al bot: "Cuando recibas el comando /start, ejecuta la función 'start'"
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    # Arrancar el bot
    print("El bot se está iniciando...")
    application.run_polling()