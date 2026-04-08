from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("AIzaSyCT3nHWmjxVcFwKW7EFLKZncEWwZLTJ9is")
)

models = client.models.list()

for m in client.models.list():
    print(m.name)