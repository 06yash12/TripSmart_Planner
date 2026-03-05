import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_ai_response(user_question):
    """
    Get AI response for travel-related questions using Gemini API
    """
    try:
        # Configure Gemini API
        api_key = os.getenv("GEMINI_API_KEY", "")
        
        if not api_key:
            return {
                "error": True,
                "message": "⚠️ Gemini API key not configured. Please set GEMINI_API_KEY environment variable."
            }
        
        genai.configure(api_key=api_key)
        
        # List available models and use the first one that supports generateContent
        available_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
        except:
            pass
        
        # Try to use the first available model, or fallback to gemini-pro
        model_name = available_models[0] if available_models else 'gemini-pro'
        
        model = genai.GenerativeModel(model_name)
        
        # Create travel-focused prompt
        prompt = f"""You are an expert travel assistant. Answer the following travel-related question in a helpful, friendly, and informative way. 
        Provide practical advice, tips, and recommendations when relevant.
        
        Question: {user_question}
        
        Answer:"""
        
        # Generate response
        response = model.generate_content(prompt)
        
        return {
            "error": False,
            "answer": response.text
        }
        
    except Exception as e:
        error_msg = str(e)
        return {
            "error": True,
            "message": f"❌ Error: {error_msg}\n\n💡 Tip: Make sure you're using a valid Gemini API key from https://aistudio.google.com/app/apikey"
        }
