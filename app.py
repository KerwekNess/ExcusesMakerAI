from flask import Flask, jsonify, render_template, request
from config import Settings
from services.ai_service import AIService

app = Flask(__name__)

# Initialization
try:
    settings = Settings()
    settings.validate()
    ai_service = AIService(settings)
except Exception as e:
    print(f'Initialization Error: {e}')
    settings = None
    ai_service = None

@app.route('/')
def index():
    return render_template('index.html')

@app.post('/api/excuses')
def create_excuses():
    if ai_service is None:
        return jsonify({'error': 'Service initialization error. Check .env and logs.'}), 500

    payload = request.get_json(silent=True) or {}
    situation = (payload.get('situation') or request.form.get('situation') or '').strip()

    if not situation:
        return jsonify({'error': 'Please enter a situation.'}), 400

    try:
        text, items = ai_service.generate_excuses(situation)
        return jsonify({
            'text': text,
            'items': items
        })
    except Exception as e:
        print(f'Error generating excuses: {e}')
        return jsonify({'error': f'API Error: {str(e)}'}), 502

if __name__ == '__main__':
    debug_mode = True
    if settings:
        debug_mode = settings.DEBUG
    app.run(debug=debug_mode)
