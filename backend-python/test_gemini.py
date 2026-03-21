from google import genai

client = genai.Client(api_key="AIzaSyD_JCjrhvj6Y7HigICKTeMYv3t9vgPel6w")

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Hello"
)

print(response.text)