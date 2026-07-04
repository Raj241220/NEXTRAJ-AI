import os
from dotenv import load_dotenv
from groq import Groq

from core.memory import add_message, get_history
from core.controller import execute_command
from core.search import web_search
from core.utils import get_current_date, get_current_time

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_ai(prompt):

    # ==========================
    # Save User Message
    # ==========================

    add_message("user", prompt)

    user_prompt = prompt.lower()

    # ==========================
    # Date
    # ==========================

    if (
        "today's date" in user_prompt
        or "what is today's date" in user_prompt
        or "current date" in user_prompt
        or "date today" in user_prompt
    ):

        reply = f"📅 Today is {get_current_date()}."

        add_message("assistant", reply)

        return reply

    # ==========================
    # Time
    # ==========================

    if (
        "current time" in user_prompt
        or "time now" in user_prompt
        or "what time is it" in user_prompt
    ):

        reply = f"🕒 Current time is {get_current_time()}."

        add_message("assistant", reply)

        return reply

    # ==========================
    # Computer Control
    # ==========================

    result = execute_command(prompt)

    if result:

        add_message("assistant", result)

        return result

    # ==========================
    # Internet Search
    # ==========================

    search_result = web_search(prompt)

    system_prompt = """
You are NEXTRAJ.AI.

You are a smart, friendly and intelligent AI assistant.

Rules:

- Remember previous conversation.
- Give short and clear answers.
- If Internet Search Results are available,
  use them.
- Otherwise answer using your own knowledge.
"""

    messages = [

        {
            "role": "system",
            "content": system_prompt
        }

    ]

    # Memory

    messages.extend(get_history())

    # Internet Results

    if search_result:

        messages.append(

            {

                "role": "system",

                "content":
                f"Latest Internet Search Results:\n\n{search_result}"

            }

        )

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=messages,

            temperature=0.7,

            max_tokens=2048

        )

        reply = response.choices[0].message.content

        add_message("assistant", reply)

        return reply

    except Exception as e:

        return f"AI Error: {str(e)}"