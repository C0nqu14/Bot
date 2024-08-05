from flask import Flask, request, jsonify
import nltk
from nltk.chat.util import Chat, reflections
import google.generativeai as genai

app = Flask(__name__)

# Inicialize o NLTK Chatbot
pares = [
    [
        r"(oi|olá|hey|tudo bem\?)",
        ["oi amigo", "Eai?", "Sim"]
    ],
    [
        r"(como te chamas\?|qual é o teu nome\?|tens um nome\?)",
        ["Sou a MarviniBOT", "Sim, tenho um nome, MarviniBOT", "Pode me chamar de MarviniBOT"]
    ],
    [
        r"(o que é a Marvini\?|o que vocês fazem\?|quais são os vossos serviços\?|quem são vocês\?)",
        ["A Marvini é uma empresa focada em contabilidade"]
    ],
    [
        r"(interessante|legal|maneiro)",
        ["E muito...", "Esperas para veres o nosso local", "Isso ainda é pouco"]
    ]
]

chatbot = Chat(pares, reflections)

# Configure o modelo do Google Generative AI
chave = "AIzaSyDt73YD_Cov48NIfDXXSUhAUIsfd_Fg-RA"
genai.configure(api_key=chave)
model = genai.GenerativeModel("gemini-1.0-pro")
chat = model.start_chat(history=[])

@app.route('/message', methods=['POST'])
def message():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    response = chatbot.respond(user_message)
    if response is None:
        response = chat.send_message(user_message)
        response_text = response.text
    else:
        response_text = response

    return jsonify({'message': response_text})

if __name__ == '__main__':
    app.run(debug=True)
