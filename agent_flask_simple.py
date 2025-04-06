from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# Konfiguracja API Gemini - **UWAGA: WPROWADŹ SWÓJ KLUCZ API TUTAJ**
GOOGLE_API_KEY = "AIzaSyBMEnnqCZzHPx8qlVVbbB6eT_PKPoWHetk"  # ZASTĄP "YOUR_API_KEY" SWOIM PRAWDZIWYM KLUCZEM API
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash') # TU MOŻE BYĆ INNA NAZWA MODELU!
else:
    print("Nie podano klucza API Google.")
    model = None

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explain', methods=['POST'])
def explain_concept():
    if not model:
        return jsonify({'error': 'API Gemini nie jest skonfigurowane.'}), 500

    data = request.get_json()
    text_to_explain = data.get('text')

    if not text_to_explain:
        return jsonify({'error': 'Nie podano tekstu do wyjaśnienia.'}), 400

    prompt = f"""Jesteś elokwętnym szlachciem i mówisz w jezyku taki, jak Polacy mówili 300 lat temu .

    Tekst do wyjaśnienia: {text_to_explain}"""

    try:
        response = model.generate_content(prompt)
        explanation = response.text
        return jsonify({'explanation': explanation})
    except Exception as e:
        return jsonify({'error': f'Wystąpił błąd podczas generowania wyjaśnienia: {str(e)}'}), 500
@app.route('/generate_title', methods=['POST'])
def generate_title():
    if not model:
        return jsonify({'title': 'Nowa rozmowa'})

    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'title': 'Nowa rozmowa'})

    prompt = f"""Na podstawie poniższej wypowiedzi użytkownika, zaproponuj krótki, zwięzły i chwytliwy tytuł rozmowy. Nie dodawaj cudzysłowów, nie pisz 'Tytuł:', tylko samą nazwę.

Wypowiedź: {text}"""

    try:
        response = model.generate_content(prompt)
        title = response.text.strip()
        return jsonify({'title': title})
    except Exception as e:
        return jsonify({'title': 'Rozmowa'}), 200

if __name__ == '__main__':
    app.run(debug=True)