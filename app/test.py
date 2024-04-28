from g4f.client import Client

client = Client()

kata = "hello"
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role":"user", "content":f"{kata}"}]
)


print(response.choices[0].message.content)