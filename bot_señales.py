from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# =========================
# 🔐 CONFIGURACIÓN TELEGRAM
# =========================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# =========================
# 📲 FUNCIÓN ENVIAR MENSAJE
# =========================
def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Missing Telegram credentials")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, data=payload)
    print("Telegram response:", response.status_code, response.text)


# =========================
# 📊 SCORE SIMPLE DE CALIDAD
# =========================
def calculate_score(data):
    score = 5  # base

    if data.get("signal") == "BUY":
        score += 1
    elif data.get("signal") == "SELL":
        score += 1

    if data.get("session") == "NY":
        score += 2

    if float(data.get("volatility", 0)) > 1:
        score += 1

    return min(score, 10)


# =========================
# 🌐 WEBHOOK PRINCIPAL
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json or {}

        symbol = data.get("symbol", "N/A")
        signal = data.get("signal", "N/A")
        price = data.get("price", "N/A")

        score = calculate_score(data)

        message = f"""
🚨 <b>SMC BOT SIGNAL</b>

📊 Symbol: {symbol}
📈 Signal: {signal}
💰 Price: {price}

⭐ Quality Score: {score}/10
        """

        send_telegram_message(message)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# =========================
# 🚀 RUN LOCAL / RENDER
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
