from flask import Flask, render_template, request, jsonify # type: ignore
import requests # type: ignore

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"  # URL API Ollama
MODEL_NAME = "nature"  # Модель Ollama

@app.route("/")
def chat_bot():
    """Отображает главную страницу с интерфейсом чата."""
    return render_template("ChatBot.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """Обрабатывает сообщения от пользователя и отправляет их в Ollama."""
    try:
        if request.is_json:  # Если запрос содержит JSON (обычное текстовое сообщение)
            data = request.get_json()
            user_message = data["message"]
        elif "file" in request.files:  # Если запрос содержит файл
            file = request.files["file"]
            if file.filename.endswith(".txt"):  # Проверяем, что файл текстовый
                user_message = file.read().decode("utf-8")  # Читаем содержимое файла
            else:
                return jsonify({"response": "Error: Only .txt files are allowed."}), 400
        else:
            return jsonify({"response": "Error: Invalid request format."}), 400

        # Отправляем запрос в Ollama
        payload = {
            "prompt": user_message,
            "model": MODEL_NAME,
            "stream": False  # Отключаем стриминг для простоты
        }
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()  # Проверяем статус ответа

        json_data = response.json()
        ollama_response = json_data.get("response", "No response from Ollama.")
        return jsonify({"response": ollama_response})

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama: {e}")
        return jsonify({"response": f"Error: Could not connect to Ollama."}), 500

if __name__ == "__main__":
    app.run(debug=True)  # debug=True только для разработки