from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")

print("API KEY:", api_key)  # 👈 debug

if not api_key:
    print("⚠️ NO API KEY")
    client = None
else:
    from google import genai
    client = genai.Client(api_key=api_key)