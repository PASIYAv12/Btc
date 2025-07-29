import os
from binance.client import Client
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# API Keys & Settings
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))

# Binance Client
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# --- Telegram Bot Commands ---

def restricted(func):
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != OWNER_ID:
            update.message.reply_text("❌ Access Denied.")
            return
        return func(update, context, *args, **kwargs)
    return wrapped

@restricted
def start(update, context):
    update.message.reply_text("👋 Welcome to your Binance Trading Bot.\nUse /help to see commands.")

@restricted
def help_command(update, context):
    update.message.reply_text(
        "/buy SYMBOL QTY TP SL\n"
        "/sell SYMBOL QTY TP SL\n"
        "/price SYMBOL\n"
        "/balance"
    )

@restricted
def price(update, context):
    if len(context.args) != 1:
        update.message.reply_text("Usage: /price BTCUSDT")
        return
    symbol = context.args[0].upper()
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        update.message.reply_text(f"{symbol} Price: {ticker['price']}")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

@restricted
def balance(update, context):
    try:
        account = client.get_account()
        msg = "💰 Balances:\n"
        for asset in account['balances']:
            if float(asset['free']) > 0:
                msg += f"{asset['asset']}: {asset['free']}\n"
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

@restricted
def buy(update, context):
    if len(context.args) != 4:
        update.message.reply_text("Usage: /buy BTCUSDT 0.001 60000 55000")
        return
    symbol, qty, tp, sl = context.args
    try:
        order = client.create_order(
            symbol=symbol.upper(),
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=float(qty)
        )
        update.message.reply_text(f"✅ BUY Order placed for {qty} {symbol}\n🎯 TP: {tp} | 🛑 SL: {sl}")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

@restricted
def sell(update, context):
    if len(context.args) != 4:
        update.message.reply_text("Usage: /sell BTCUSDT 0.001 60000 55000")
        return
    symbol, qty, tp, sl = context.args
    try:
        order = client.create_order(
            symbol=symbol.upper(),
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,
            quantity=float(qty)
        )
        update.message.reply_text(f"✅ SELL Order placed for {qty} {symbol}\n🎯 TP: {tp} | 🛑 SL: {sl}")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("price", price))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("buy", buy))
    dp.add_handler(CommandHandler("sell", sell))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
