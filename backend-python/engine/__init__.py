from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY") #👈 dán KEY của gemini 

print("API KEY:", api_key)  # 👈 debug

if not api_key:
    print("⚠️ NO API KEY 01")
    client = None
else:
    from google import genai
    client = genai.Client(api_key=api_key)