import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from analyzer import analyze_item
from pricer import get_comparables, generate_price_estimate

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")

# ================== DUMMY SERVER FOR RENDER ==================
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running OK")

def run_dummy_server():
    port = int(os.getenv("PORT", 8080))
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"✅ Dummy health server running on port {port}")
        httpd.serve_forever()

# ================== BOT LOGIC ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛍️ **AI Resale Pricer Bot**\n\nSend a photo of any item to get a price estimate!")

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
🔍 **Analysis**
{analysis[:700]}...

💰 **Price Estimate**
**${est['median']}** (${est['low']}-${est['high']})
Confidence: {est['confidence']}

📝 **Tips**: {est['reasoning'][:700]}
"""
        await message.reply_text(reply, parse_mode='Markdown')
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def main():
    # Start dummy server for Render
    threading.Thread(target=run_dummy_server, daemon=True).start()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 Telegram Bot Started")
    app.run_polling()

if __name__ == "__main__":
    main()
