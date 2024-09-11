from openai import OpenAI

openai = OpenAI(
    api_key="HTj80cPBu4Qaiw80oIUZAs6J9Nzg73XK",
    base_url="https://api.deepinfra.com/v1/openai",
)

input = "The food was delicious and the waiter...", # or an array ["hello", "world"]

embeddings = openai.embeddings.create(
  model="BAAI/bge-large-en-v1.5",
  input=input,
  encoding_format="float"
)
if isinstance(input, str):
    print(embeddings.data[0].embedding)
else:
    for i in range(len(input)):
        print(embeddings.data[i].embedding)


print(embeddings.usage.prompt_tokens)
