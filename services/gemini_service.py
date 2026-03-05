import os
import logging

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.error("google-generativeai package not installed")

if GENAI_AVAILABLE:
    load_dotenv()

class GeminiService:
    def __init__(self):
        if not GENAI_AVAILABLE:
            logger.error("Gemini AI package not available")
            self.model = None
            self.model_name = None
            return
            
        api_key = os.getenv('GEMINI_API_KEY')
        logger.info(f"API Key loaded: {bool(api_key)}")
        
        if not api_key or api_key == 'your_gemini_api_key_here':
            logger.warning("GEMINI_API_KEY not found or not configured in environment variables")
            self.model = None
            self.model_name = None
        else:
            try:
                logger.info("Configuring Gemini API...")
                genai.configure(api_key=api_key)
                
                # List available models
                try:
                    available_models = []
                    for model in genai.list_models():
                        if 'generateContent' in model.supported_generation_methods:
                            available_models.append(model.name.replace('models/', ''))
                    logger.info(f"Available models: {available_models}")
                except Exception as list_error:
                    logger.warning(f"Could not list models: {list_error}")
                    available_models = []
                
                # Try models in order from lowest to highest (updated list for 2026)
                models_to_try = ['gemini-1.5-flash', 'gemini-1.5-flash-8b', 'gemini-1.5-pro']
                
                # If we got available models, use those instead
                if available_models:
                    models_to_try = available_models
                
                for model_name in models_to_try:
                    try:
                        logger.info(f"Trying model: {model_name}")
                        self.model = genai.GenerativeModel(model_name)
                        self.model_name = model_name
                        logger.info(f"✅ Gemini model created: {self.model_name}")
                        break
                    except Exception as model_error:
                        logger.warning(f"Model {model_name} failed: {str(model_error)}")
                        continue
                
                if not hasattr(self, 'model') or self.model is None:
                    raise Exception("No available Gemini models found")
                    
            except Exception as e:
                logger.error(f"Failed to configure Gemini: {str(e)}", exc_info=True)
                self.model = None
                self.model_name = None
    
    def get_travel_response(self, user_query: str, conversation_history: list = None) -> str:
        """
        Get AI response for travel-related queries
        
        Args:
            user_query: The user's question
            conversation_history: List of previous messages for context
            
        Returns:
            AI-generated response
        """
        if not GENAI_AVAILABLE:
            return ("Google Generative AI package is not installed. "
                   "Please run: pip install google-generativeai")
        
        if not self.model:
            return ("I'm currently unable to connect to the AI service. "
                   "Please make sure the GEMINI_API_KEY is configured in your .env file. "
                   "You can get a free API key from: https://aistudio.google.com/app/apikey")
        
        try:
            # Simple, direct prompt
            prompt = f"""You are a helpful travel assistant for Indian destinations. 
Answer this travel question clearly and concisely:

{user_query}

Provide practical, helpful information."""
            
            logger.info(f"Sending query to Gemini ({self.model_name}): {user_query[:50]}...")
            
            # Generate response - try without safety settings first
            try:
                response = self.model.generate_content(prompt)
            except Exception as e:
                # If that fails, try with relaxed safety settings
                logger.warning(f"First attempt failed, trying with safety settings: {str(e)}")
                response = self.model.generate_content(
                    prompt,
                    safety_settings=[
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                    ]
                )
            
            # Try to get text from response
            if hasattr(response, 'text') and response.text:
                logger.info("Successfully received response from Gemini")
                return response.text
            
            # Check candidates
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text:
                                return part.text
            
            # Check for blocked response
            if hasattr(response, 'prompt_feedback'):
                logger.warning(f"Response blocked: {response.prompt_feedback}")
                return ("I couldn't generate a response for that query. Please try rephrasing your question.")
            
            logger.warning("Received empty response from Gemini")
            return ("I received an empty response. Please try again or use the quick question buttons above.")
            
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}", exc_info=True)
            error_msg = str(e).lower()
            
            # Provide more specific error messages
            if "404" in error_msg or "not found" in error_msg or "model" in error_msg:
                return ("❌ Model not found. The Gemini API models may have been updated. Please check the latest model names.")
            elif "api" in error_msg and ("key" in error_msg or "invalid" in error_msg):
                return ("❌ API key error. Please verify your GEMINI_API_KEY in the .env file is correct.")
            elif "quota" in error_msg or "limit" in error_msg or "429" in error_msg:
                return ("⚠️ API quota exceeded. Please try again in a few moments.")
            elif "safety" in error_msg or "blocked" in error_msg:
                return ("🛡️ Response was blocked by safety filters. Please rephrase your question.")
            elif "network" in error_msg or "connection" in error_msg:
                return ("🌐 Network error. Please check your internet connection and try again.")
            else:
                return (f"⚠️ An error occurred: {str(e)}\n\nPlease try again or use the quick question buttons above.")
    
    def is_available(self) -> bool:
        """Check if the Gemini service is available"""
        return self.model is not None
