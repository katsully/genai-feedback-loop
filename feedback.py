import requests
import time
import os
import openai

openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"

with open("keys.txt") as f:
	# converting our text file to a list of lines
	lines = f.read().split('\n')
	# openai api key
	openai.api_key = lines[0]
	openai.api_base = lines[1]
# close the file
f.close()

response = openai.ChatCompletion.create(
	engine="GPT-4",
	messages=[
	{"role": "system", "content": "You make prompts for Dall-E"},
	{"role": "user", "content": "Describe the most beautiful image, please be brief"}
	]
)

img_prompt = response.choices[0].message.content
print(img_prompt)

api_base = openai.api_base
api_key = openai.api_key

url = "{}dalle/text-to-image?api-version=2022-08-03-preview".format(api_base)
headers= { "api-key": api_key, "Content-Type": "application/json" }
body = {
    "caption": img_prompt,
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



