# api/index.py
import os
import requests
from flask import Flask, request, jsonify

TOKEN   = os.getenv("TOKEN")            # Bot token
GROUP_A = int(os.getenv("GROUP_A", 0))  # ID nhóm nguồn
GROUP_B = int(os.getenv("GROUP_B", 0))  # ID nhóm đích

app = Flask(__name__)  # Vercel sẽ nhận biết biến 'app' này

@app.route("/", methods=["GET"])
def home():
    return "Bot is alive!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    msg  = data.get("message") or {}
    chat = msg.get("chat", {}).get("id")

    # Nếu message từ đúng nhóm A
    if chat == GROUP_A:
        msg_id = msg.get("message_id")
        # Forward tin sang nhóm B
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/forwardMessage",
            json={
                "chat_id":       GROUP_B,
                "from_chat_id":  GROUP_A,
                "message_id":    msg_id
            }
        )
    return jsonify(ok=True)
