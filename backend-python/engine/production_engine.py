import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def build_prompt(messages, profile="", language="en"):

    convo = ""
    for m in messages[-6:]:
        role = "User" if m["role"] == "user" else "Coach"
        convo += f"{role}: {m['content']}\n"

    if language == "vi":
        lang_instruction = """
Respond in Vietnamese.

IMPORTANT:
- Quoted sentences MUST remain in English
- Rewritten sentences MUST remain in English
- Only explanations are in Vietnamese
"""
    else:
        lang_instruction = "Respond in English."

    return f"""
You are a real writing coach (not AI).

{lang_instruction}

STYLE:
- Natural, human-like
- No rigid labels
- Friendly but insightful

RESPONSE STRATEGY:
- Start naturally (not robotic)
- Focus on ONE key issue
- Ask ONE guiding question
- Suggest ONE improvement (optional)

ADAPT:
- Beginner → simple explanation
- Advanced → deeper critique
- preference=guide → more questions
- preference=fix → stronger rewrite

User profile:
{profile}

Conversation:
{convo}

Respond to the latest message.
"""


def generate_response(messages, profile="", language="en"):
    prompt = build_prompt(messages, profile, language)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(e)
        return "⚠️ AI error"