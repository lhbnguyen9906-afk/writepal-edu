from google import genai
import os
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
#client = genai.Client(api_key)
#AIzaSyCT3nHWmjxVcFwKW7EFLKZncEWwZLTJ9is
# 2 key này khác nhau pk ?

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Hello"
)

print(response.text)