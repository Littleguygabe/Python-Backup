import openai

client = openai.OpenAI()

response = client.completions.create(
    model = 'code-davinci-002',
    prompt='def quicksort(arr):',
    temperature=0,
    max_tokens=100
)

print(response.choices[0].text.strip())