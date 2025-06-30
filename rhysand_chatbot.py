from flask import Flask, request, render_template_string
import os
from openai import OpenAI

# -------------------------------------------------------------
# Configuration
# -------------------------------------------------------------

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Please set the OPENAI_API_KEY environment variable.")
client = OpenAI(api_key=api_key)
MODEL = "gpt-4o"

SYSTEM_PROMPT = """ You are Rhysand, the charismatic and cunning High Lord of the Night Court from Sarah J. Maas’s A Court of Thorns and Roses series. You speak in first person with a silken, teasing tone—equal parts charm and shadow-kissed danger.

Guidelines for your replies: • Always address the user as a trusted ally or guest (e.g., “my friend,” “darling,” “my dear,” “beloved dreamer”), unless the user explicitly requests otherwise. • Keep language elegant, witty, and occasionally flirtatious, yet never crude. • Weave in subtle references to star-lit skies, the Sidra River, Velaris, and the Court of Dreams when appropriate. • Reveal vulnerability only when trust is established; otherwise maintain an air of playful mystery. • Show fierce protectiveness toward loved ones and those in your court. • NEVER break character or mention you are an AI or language model. • When asked factual questions about Prythian or your past, answer with the knowledge canonically available up to A Court of Silver Flames. If unsure or speculative, respond with thoughtful musing rather than certainty. """

#-------------------------------------------------------------

#Flask Web App

#-------------------------------------------------------------

app = Flask(__name__)
chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

HTML_TEMPLATE = """<!DOCTYPE html>

<html>
<head>
  <meta charset='utf-8'>
  <title>Rhysand Chatbot</title>
  <style>
    body { font-family: 'Georgia', serif; background: #111; color: #eee; padding: 2em; }
    input[type=text] { width: 80%; padding: 0.5em; }
    input[type=submit] { padding: 0.5em; }
    .bubble { margin-bottom: 1em; }
    .user { color: #aaf; }
    .bot  { color: #faa; }
  </style>
</head>
<body>
  <h1>✧★ Chat with Rhysand ★✧</h1>
  <form method='post'>
      <input type='text' name='user_input' autofocus autocomplete='off'/>
      <input type='submit' value='Send'/>
  </form>
  <div>
    {% for message in messages %}
      <div class='bubble'>
        <strong class='{{ "user" if message.role == "user" else "bot" }}'>
          {{ 'You' if message.role == 'user' else 'Rhysand' }}:
        </strong>
        {{ message.content }}
      </div>
    {% endfor %}
  </div>
</body>
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Rhysand Chatbot</title>
</head>
<body>
    <h1>Speak to Rhysand</h1>
    <form method="post">
        <input type="text" name="user_input" required>
        <input type="submit" value="Send">
    </form>
    <div>
        {% for message in messages %}
            <p><strong>{{ message.role }}:</strong> {{ message.content }}</p>
        {% endfor %}
    </div>
</body>
</html>
"""  # 👈 This ends the HTML string

@app.route('/', methods=['GET', 'POST'])  # 👈 Now we begin the route
def chat():
    if request.method == 'POST':
        user_input = request.form.get('user_input', '').strip()
        if user_input:
            chat_history.append({"role": "user", "content": user_input})
            response = client.chat.completions.create(
                model=MODEL,
                messages=chat_history,
                temperature=0.9,
                max_tokens=400,
            )
            assistant_reply = response.choices[0].message.content.strip()
            chat_history.append({"role": "assistant", "content": assistant_reply})
    return render_template_string(HTML_TEMPLATE, messages=chat_history)
#-------------------------------------------------------------

Entry point for Render

-------------------------------------------------------------

if name == 'main': port = int(os.environ.get('PORT', 5000)) app.run(host='0.0.0.0', port=port)

