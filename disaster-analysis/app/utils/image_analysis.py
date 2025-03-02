import google.generativeai as genai
from PIL import Image
import numpy as np
import cv2
import io

def configure_palm(api_key):
    try:
        genai.configure(api_key=api_key)
        print("\nConfiguring Gemini Vision model...")
    except Exception as e:
        print(f"\nError in configuration: {str(e)}")
        raise

def split_image_into_blocks(image, block_size=512):
    """Split image into blocks for analysis"""
    height, width = image.shape[:2]
    blocks = []
    positions = []
    
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            block = image[y:min(y + block_size, height), 
                        x:min(x + block_size, width)]
            blocks.append(block)
            positions.append((x, y))
    
    return blocks, positions

def analyze_block(before_block, after_block):
    """Analyze before/after blocks using Gemini Vision"""
    try:
        # Convert numpy arrays to PIL Images
        before_pil = Image.fromarray(before_block)
        after_pil = Image.fromarray(after_block)
        
        # Convert PIL images to bytes
        before_buffer = io.BytesIO()
        after_buffer = io.BytesIO()
        before_pil.save(before_buffer, format='PNG')
        after_pil.save(after_buffer, format='PNG')
        before_bytes = before_buffer.getvalue()
        after_bytes = after_buffer.getvalue()

        # Initialize Gemini Vision model
        model = genai.GenerativeModel('gemini-pro-vision')
        
        prompt = """
        Compare these before and after satellite images of an area affected by fire.
        The first image is the before image, and the second is the after image.
        Please analyze and provide:
        1. Number of buildings/structures that appear damaged or destroyed
        2. Road accessibility status
        3. Percentage of area affected by fire
        4. Any visible infrastructure damage
        5. Recommendations for emergency response
        Be specific and detailed in your analysis.
        """

        # Generate content with both images
        response = model.generate_content(
            contents=[
                prompt,
                {"mime_type": "image/png", "data": before_bytes},
                {"mime_type": "image/png", "data": after_bytes}
            ]
        )
        
        return response.text
    except Exception as e:
        print(f"\nError in analyze_block: {str(e)}")
        raise

def analyze_disaster_images(before_image_file, after_image_file):
    """Main function to analyze before/after disaster images"""
    try:
        # Read images
        before_image = cv2.imdecode(
            np.frombuffer(before_image_file.read(), np.uint8),
            cv2.IMREAD_COLOR
        )
        after_image = cv2.imdecode(
            np.frombuffer(after_image_file.read(), np.uint8),
            cv2.IMREAD_COLOR
        )
        
        # Convert BGR to RGB
        before_image = cv2.cvtColor(before_image, cv2.COLOR_BGR2RGB)
        after_image = cv2.cvtColor(after_image, cv2.COLOR_BGR2RGB)
        
        # Split images into blocks
        before_blocks, positions = split_image_into_blocks(before_image)
        after_blocks, _ = split_image_into_blocks(after_image)
        
        # Analyze each block
        analysis_results = []
        for i, (before_block, after_block, pos) in enumerate(zip(before_blocks, after_blocks, positions)):
            print(f"\nAnalyzing block {i+1}...")
            analysis = analyze_block(before_block, after_block)
            analysis_results.append({
                'block_id': i,
                'position': pos,
                'analysis': analysis
            })
        
        return {
            'total_blocks': len(analysis_results),
            'results': analysis_results
        }
    except Exception as e:
        print(f"\nError in analyze_disaster_images: {str(e)}")
        raise