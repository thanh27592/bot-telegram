import os
import requests
from flask import Flask, request

TOKEN = os.environ.get("TOKEN")         # Token Bot Telegram (đọc từ biến môi trường)
GROUP_A = int(os.environ.get("GROUP_A", "0"))   # ID nhóm nguồn A
GROUP_B = int(os.environ.get("GROUP_B", "0"))   # ID nhóm đích B

app = Flask(__name__)  # Ứng dụng Flask (Vercel sẽ nhận biết biến app này):contentReference[oaicite:4]{index=4}

@app.route("/", methods=["GET"])
def home():
    # Endpoint index để kiểm tra bot còn hoạt động
    return "Bot đang chạy (Flask webhook active)!"

@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    """Xử lý dữ liệu Webhook gửi từ Telegram"""
    data = request.get_json()  # Lấy nội dung JSON của update từ Telegram
    if not data:
        return "OK"  # Trả về OK ngay nếu không có dữ liệu

    # Kiểm tra nếu có tin nhắn mới và đến từ nhóm A
    message = data.get("message")
    if message:
        chat_id = message.get("chat", {}).get("id")
        # Chỉ forward nếu tin được gửi từ nhóm A (đúng ID nhóm nguồn)
        if chat_id == GROUP_A:
            msg_id = message.get("message_id")
            try:
                # Gửi yêu cầu forwardMessage tới Telegram Bot API
                res = requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/forwardMessage",
                    json={"chat_id": GROUP_B, "from_chat_id": GROUP_A, "message_id": msg_id}
                )
                # Kiểm tra kết quả gửi để debug (tùy chọn):
                # print(res.status_code, res.text)
            except Exception as e:
                print(f"Error forwarding message: {e}")
    return "OK"  # Trả về "OK" để Telegram biết server đã nhận (HTTP 200)
