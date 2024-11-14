import google.generativeai as genai
import os
# I will remove this key in the next few days
# I have provided this key solely for demonstration purposes
GEMINI_API_KEY = "AIzaSyD6OXS89hHRqzGCY1klK9A8qNlG0sJEvAU"

genai.configure(api_key=GEMINI_API_KEY)

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

model = genai.GenerativeModel(model_name="gemini-1.5-flash")



