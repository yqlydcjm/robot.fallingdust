import openai
import script
# Set your API key
openai.api_key = "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"
# Use the GPT-3 model
def chat(uid, content):
    completion = openai.Completion.create(
        model='text-davinci-003',
        prompt=content,
        temperature=0.8,
        max_tokens=120,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )

    s=completion.choices[0].text
    ls=[0]
    ls[0]=s[0]
    for i in range(1,len(s)):
        if s[i]!=ls[-1]:
            ls.append(s[i])
    completion.choices[0].text=''.join(ls)
    script.bl(uid, completion.choices[0].text)

def chats(uid, content):
    completion = openai.Completion.create(
        model='text-davinci-003',
        prompt=content,
        temperature=0.8,
        max_tokens=120,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )

    # script.bl(uid, completion.choices[0].text)
    s=completion.choices[0].text
    ls=[0]
    ls[0]=s[0]
    for i in range(1,len(s)):
        if s[i]!=ls[-1]:
            ls.append(s[i])
    completion.choices[0].text=''.join(ls)
    script.handle_privates(uid, completion.choices[0].text, completion.choices[0].text)