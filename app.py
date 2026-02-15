import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Нет текста"}), 400

    prompt = f"""
Ты редактор деловых сообщений.
Очисти текст от слов-паразитов, исправь грамматику и сделай его деловым.

Текст:
{text}
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt
    )

    cleaned = response.output_text

    return jsonify({"result": cleaned})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
