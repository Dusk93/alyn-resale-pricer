import logging, os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from analyzer import analyze_item
from pricer import get_comparables, generate_price_estimate

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")   # Will come from Render env vars

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛍️ Send me a photo of any item for AI resale pricing!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    await message.reply_text("🔍 Analyzing with AI...")

    photo_file = await message.photo[-1].get_file()
    file_path = f"temp_{message.message_id}.jpg"
    await photo_file.download_to_drive(file_path)

    user_text = message.caption or ""

    try:
        analysis = analyze_item(file_path, user_text)
        df = get_comparables(analysis)
        est = generate_price_estimate(analysis, df)

        reply = f"""
🔍 **Analysis**: {analysis[:600]}...

💰 **Price**: **${est['median']}** (${est['low']}-${est['high']})
Confidence: {est['confidence']}

{est['reasoning'][:700]}
"""
        await message.reply_text(reply, parse_mode='Markdown')
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()

if __name__ == "__main__":
    main()