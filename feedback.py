import requests
import time
import os
import openai
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO

def wrap_text_pixel_width(text, font, max_width):
	words = text.split()
	wrapped_lines = []
	current_line = []

	for word in words:
		current_line.append(word)
		line_width, _ = font.getsize(' '.join(current_line))
		if line_width > max_width:
			current_line.pop()
			wrapped_lines.append(' '.join(current_line))
			current_line = [word]

	wrapped_lines.append(' '.join(current_line))
	return '\n'.join(wrapped_lines)

openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"

prev_chat_prompt = ""
new_chat_prompt = "Describe the most beautiful image, please be brief"

loop_count = 5
font_size = 32
font = ImageFont.truetype("arial.ttf", font_size)

with open("keys.txt") as f:
	# converting our text file to a list of lines
	lines = f.read().split('\n')
	# openai api key
	openai.api_key = lines[0]
	openai.api_base = lines[1]
# close the file
f.close()

for x in range(loop_count):
	print("Loop #{}".format(x+1))
	response = openai.ChatCompletion.create(
		engine="GPT-4",
		messages=[
		{"role": "system", "content": "You make prompts for Dall-E"},
		{"role": "user", "content": "Using this text: {}, come up with a Dall-E prompt.".format(new_chat_prompt)}
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
	data = requests.get(image_url).content
	img = Image.open(BytesIO(data))
	
	wrapped_text = wrap_text_pixel_width(img_prompt, font, img.width)
	
	# create a new image with extra space at the bottom for the caption
	new_image = Image.new('RGB', (img.width, img.height + 200), (255, 255, 255))
	new_image.paste(img, (0,0))

	draw = ImageDraw.Draw(new_image)
	draw.text((10, img.height + 10), wrapped_text, font=font, fill=(0,0,0))

	new_image.save('img{}.jpg'.format(x))

	prev_chat_prompt = new_chat_prompt
	new_chat_prompt = image_url			



