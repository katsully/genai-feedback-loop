import openai

openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"

with open("keys.txt") as f:
	lines = f.read().split('\n')
	openai.api_key = lines[0]
	openai.api_base = lines[1]
f.close()

# chat completion
# response = openai.ChatCompletion.create(engine="GPT-4", messages=[{"role": "system", "content": "You create prompts for the Dall-E system."},
#     {"role": "user", "content": "Describe the perfect image"},
# ])
# img_prompt = response.choices[0].message.content
# print(img_prompt)

img_response = openai.Image.create(
    prompt="a cat wearing a hat",
    n=1,
    size="256x256"
)
print(img_response)