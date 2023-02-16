import openai
import script
# Set your API key
openai.api_key = "your key"
def chat(uid, content):  #定义一个函数，以便后面反复调用
    try:
        response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt= content,
                    temperature=0.9,
                    max_tokens=2500,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.6,
                    stop=[" Human:", " AI:"]
                )
        script.bl(uid, response.choices[0].text)
    except Exception as exc:
        #print(exc)  #如果需要打印出故障原因可以使用本行代码，如果想增强美感，就屏蔽它。
        return "broken"
def chats(uid, content):  #定义一个函数，以便后面反复调用

    try:
        response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt= content,
                    temperature=0.9,
                    max_tokens=2500,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.6,
                    stop=[" Human:", " AI:"]
                )
        script.handle_privates(uid, response.choices[0].text)
    except Exception as exc:
        #print(exc)  #如果需要打印出故障原因可以使用本行代码，如果想增强美感，就屏蔽它。
        return "broken"
