from flask import Flask, request
import requests
import os

app = Flask(__name__)

# =========================
# 🔐 VARIABLES
# =========================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# =========================
# 📲 ENVIAR MENSAJE
# =========================
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

# =========================
# 📡 WEBHOOK TRADINGVIEW
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if not data:
        return {"error": "no data"}, 400

    action = data.get("action", "SIN ACCION")
    symbol = data.get("symbol", "N/A")
    price = data.get("price", "N/A")
    timeframe = data.get("timeframe", "N/A")

    message = f"""
📊 <b>NUEVA SEÑAL SMC</b>

🟡 Acción: {action}
📈 Símbolo: {symbol}
💰 Precio: {price}
⏱ Timeframe: {timeframe}

🔥 Enviado desde TradingView
"""

    send_telegram_message(message)

    return {"status": "ok"}, 200

# =========================
# 🧪 TEST MANUAL (NO AUTOMÁTICO)
# =========================
@app.route("/test")
def test():
    send_telegram_message("🔥 BOT OK - conexión activa")
    return "OK"

# =========================
# 🌐 HOME
# =========================
@app.route("/")
def home():
    return "🔥 Bot de señales activo"

# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
