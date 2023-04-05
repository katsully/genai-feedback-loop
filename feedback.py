import requests
import time
import os

with open("keys.txt") as f:
    # converting our text file to a list of lines
    lines = f.read().split('\n')
    # openai api key
    api_key = lines[0]
    api_base = lines[1]
# close the file
f.close()

# response = openai.ChatCompletion.create(
# 			engine="GPT-4",
# 			messages=[
# 			{"role": "system", "content": "you write prompts for openai Dall-E"},
# 			{"role": "user", "content": "Describe the perfect image, be brief"}
# 			]
# 		)
# print(response.choices[0].message.content)

api_version = '2022-08-03-preview'
url = "{}dalle/text-to-image?api-version={}".format(api_base, api_version)
headers= { "api-key": api_key, "Content-Type": "application/json" }
body = {
    "caption": "A dog in a hat",
    "resolution": "1024x1024"
}
submission = requests.post(url, headers=headers, json=body)
operation_location = submission.headers['Operation-Location']
retry_after = submission.headers['Retry-after']
status = ""
while (status != "Succeeded"):
    time.sleep(int(retry_after))
    response = requests.get(operation_location, headers=headers)
    status = response.json()['status']
image_url = response.json()['result']['contentUrl']
print(image_url)

# chat completion
# response = openai.ChatCompletion.create(engine="GPT-4", messages=[{"role": "system", "content": "You create prompts for the Dall-E system."},
#     {"role": "user", "content": "Describe the perfect image, please be brief"},
# ])
# img_prompt = response.choices[0].message.content
# print(img_prompt)



