from flask import Flask, render_template, request, jsonify
from utils import configure_gemini, analyze_images
import os

app = Flask(__name__)

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)

# Configure Gemini with your API key
GEMINI_API_KEY = 'AIzaSyCOpwPl8r7SdxaKSzFr_z0stJjqOCKH-YQ'  # Replace with your actual API key
configure_gemini(GEMINI_API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'before_image' not in request.files or 'after_image' not in request.files:
            return jsonify({'success': False, 'error': 'Both images required'}), 400
            
        before_image = request.files['before_image']
        after_image = request.files['after_image']
        
        if before_image.filename == '' or after_image.filename == '':
            return jsonify({'success': False, 'error': 'No files selected'}), 400
            
        # Analyze images using Gemini
        result = analyze_images(before_image, after_image)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting server on port 8080...")
    # Using 0.0.0.0 to allow all incoming connections
    app.run(host='0.0.0.0', port=8080, debug=True) 