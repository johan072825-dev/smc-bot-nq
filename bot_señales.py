from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# =========================
# 🔐 CONFIGURACIÓN TELEGRAM
# =========================
TELEGRAM_TOKEN = TELEGRAM_TOKEN
TELEGRAM_CHAT_ID = TELEGRAM_CHAT_ID

# =========================
# 📲 FUNCIÓN ENVIAR MENSAJE
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
# 📊 SCORE SIMPLE DE CALIDAD
# (lo puedes mejorar después)
# =========================
def calculate_score(data):
    score = 5  # base

    if data.get("signal") == "BUY":
        score += 1
    if data.get("signal") == "SELL":
        score += 1

    if data.get("session") == "NY":
        score += 2

    if data.get("volatility", 0) > 1:
        score += 1

    return min(score, 10)

# =========================
# 🌐 WEBHOOK PRINCIPAL
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json

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
        return jsonify({"error": str(e)}), 500


# =========================
# 🚀 RUN LOCAL / RENDER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
