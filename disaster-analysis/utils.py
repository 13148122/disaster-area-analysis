import google.generativeai as genai
from PIL import Image
import numpy as np
import cv2
import io

def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    print("Gemini configured successfully")

def analyze_images(before_image_file, after_image_file):
    try:
        # Read and convert images
        before_image = Image.open(before_image_file)
        after_image = Image.open(after_image_file)
        
        # Initialize Gemini Flash model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        Provide a comprehensive disaster impact analysis by comparing the before and after satellite images. 
        Structure your analysis with these sections:

        1. STRUCTURAL DAMAGE ASSESSMENT
        - Number of buildings completely destroyed
        - Number of buildings partially damaged
        - Types of structures affected
        - Severity level of structural damage

        2. ROAD NETWORK & ACCESSIBILITY
        - Main roads status
        - Alternative routes availability
        - Emergency vehicle access points
        - Critical bottlenecks or blockages
        - Percentage of road network affected

        3. FIRE IMPACT ANALYSIS
        - Total area affected by fire
        - Burn severity patterns
        - Direction of fire spread
        - Natural barriers affected
        - Potential secondary hazards

        4. INFRASTRUCTURE IMPACT
        - Power lines and utilities status
        - Communication infrastructure
        - Water supply systems
        - Critical facilities affected
        - Public service facilities status

        5. EMERGENCY RESPONSE RECOMMENDATIONS
        - Priority areas for immediate response
        - Suggested access routes for emergency vehicles
        - Resource deployment recommendations
        - Evacuation route suggestions
        - Safety considerations for responders

        6. RECOVERY PLANNING INSIGHTS
        - Short-term critical needs
        - Long-term reconstruction considerations
        - Infrastructure restoration priorities
        - Community impact mitigation strategies

        Provide specific numbers and percentages where possible. End with a brief disclaimer about the analysis limitations.
        Do not use asterisks or stars in your response. Use clear, direct statements.
        """

        # Generate content with both images
        response = model.generate_content([prompt, before_image, after_image])
        
        # Clean up the response text
        cleaned_text = response.text.replace('*', '')
        
        return {
            'success': True,
            'analysis': cleaned_text
        }
        
    except Exception as e:
        print(f"Error in analysis: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        } 