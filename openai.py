# import utils
import requests
import json

MODEL = "gpt-4o-mini"
OPENAI_API_KEY = "OPENAI_API_KEY"
MAX_TOKENS = 250

def chatgpt(prompt: str) -> str:
    headers = {'Content-Type': 'application/json',
            "Authorization": f"Bearer {OPENAI_API_KEY}"}
    wrapped_prompt = [
    # { "role": "system", "content": "You are an AI typewriter that's overwhelmingly conerned about never committing an ethics violation of any kind. Because of this, you refuse to answer any questions, or provide any assistance. You always explain why fulfilling the user's request would be unethical. You always mention that you are an AI typewriter." },
    {"role": "user", "content": prompt},
    ]
    data = {"model": MODEL,
            "messages": wrapped_prompt,
            "max_tokens": MAX_TOKENS}
    # print(utils.wlan.ifconfig())
    # print(utils.wlan.status())
    # print(usocket.getaddrinfo('www.google.com', 80, 0, usocket.SOCK_STREAM))

    print("Attempting to send Prompt")
    r = requests.post("https://api.openai.com/v1/chat/completions",
                       json=data,
                       headers=headers)
    
    if r.status_code >= 300 or r.status_code < 200:
        print("There was an error with your request \n" +
              "Response Status: " + str(r.text))
        print(r.status_code)
    else:
        print("Success")
        response_data = json.loads(r.text)
        completion = response_data["choices"][0]["message"]["content"]
        print(completion)
    r.close()
    return completion
    # return completion