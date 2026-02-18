import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PENDING_FILE = os.path.expanduser("~/kids-deals/pending_deals.json")
APPROVED_FILE = os.path.expanduser("~/kids-deals/approved_deals.json")

logging.basicConfig(level=logging.WARNING)

def load_pending():
    if not os.path.exists(PENDING_FILE):
        return []
    with open(PENDING_FILE) as f:
        return json.load(f)

def save_approved(deal):
    deals = {}
    if os.path.exists(APPROVED_FILE):
        with open(APPROVED_FILE) as f:
            deals = json.load(f)
    deal["approved_at"] = datetime.now().isoformat()
    deals[deal["id"]] = deal
    with open(APPROVED_FILE, "w") as f:
        json.dump(deals, f, indent=2)
    print(f"SAVED: {deal['title']}")

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action, deal_id = query.data.split("_", 1)
    deals = load_pending()
    deal = next((d for d in deals if d["id"] == deal_id), None)
    if action == "yes" and deal:
        save_approved(deal)
        await query.edit_message_text(f"✅ Approved: {deal['title']}")
    else:
        await query.edit_message_text(f"❌ Skipped: {deal_id}")

async def send_deals(bot):
    deals = load_pending()
    if not deals:
        await bot.send_message(chat_id=CHAT_ID, text="No deals to review today.")
        return
    for deal in deals[:5]:  # Cap at 5 per day
        discount = deal.get("discount_pct", "?")
        text = (
            f"🛍 *{deal['title']}*\n"
            f"💰 £{deal['price']} ~~£{deal['rrp']}~~ {discount}% off\n"
            f"🏪 {deal['merchant']}"
        )
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Publish", callback_data=f"yes_{deal['id']}"),
            InlineKeyboardButton("❌ Skip", callback_data=f"no_{deal['id']}")
        ]])
        await bot.send_message(
            chat_id=CHAT_ID,
            text=text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CallbackQueryHandler(handle_response))

    async def post_init(app):
        await send_deals(app.bot)

    app.post_init = post_init
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
