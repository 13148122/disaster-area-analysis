from flask import Blueprint, render_template, request, jsonify
from app.utils.image_analysis import analyze_disaster_images
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/analyze', methods=['POST'])
def analyze():
    try:
        print("Received analysis request")
        
        if 'before_image' not in request.files or 'after_image' not in request.files:
            print("Missing image files")
            return jsonify({'error': 'Both before and after images are required'}), 400

        before_image = request.files['before_image']
        after_image = request.files['after_image']

        if before_image.filename == '' or after_image.filename == '':
            print("Empty filenames")
            return jsonify({'error': 'No selected files'}), 400

        if not (allowed_file(before_image.filename) and allowed_file(after_image.filename)):
            print("Invalid file types")
            return jsonify({'error': 'Invalid file type. Please use PNG, JPG, or JPEG files'}), 400

        print("Processing images...")
        analysis_results = analyze_disaster_images(before_image, after_image)
        print("Analysis complete")
        
        return jsonify(analysis_results)
    
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500