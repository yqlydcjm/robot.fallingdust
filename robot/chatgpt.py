import openai
import script
# Set your API key
openai.api_key = "your key"
# Use the GPT-3 model
def chat(uid, content):
    completion = openai.Completion.create(
        engine="text-davinci-002",
        prompt=content,
        max_tokens=1024,
        temperature=0.5
    )
    script.bl(uid, completion.choices[0].text)

def chats(uid, content):
    completion = openai.Completion.create(
        engine="text-davinci-002",
        prompt=content,
        max_tokens=1024,
        temperature=0.5
    )
    script.handle_privates(uid, completion.choices[0].text)
