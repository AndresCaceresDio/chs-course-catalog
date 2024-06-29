from openai import OpenAI
client = OpenAI(api_key='MY_API_KEY')

# response = client.files.create(
#   file=open("my_file.jsonl", "rb"),
#   purpose="fine-tune"
# )

# print(response)

client.fine_tuning.jobs.create(
  training_file="file-abc123",
  model="gpt-3.5-turbo"
)
