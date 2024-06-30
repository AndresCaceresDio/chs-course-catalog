# Program to fine tune gpt-3.5-turbo on a jsonl dataset
# Requires the user to have an API Key, as well as be on the paid plan of ChatGPT

from openai import OpenAI
client = OpenAI(api_key='MY_API_KEY')

response = client.files.create(
  file=open("my_file.jsonl", "rb"),
  purpose="fine-tune"
)

print(response) # the id that is printed is your training file id that replaces "file-abc123" below

# client.fine_tuning.jobs.create(
#   training_file="file-abc123",
#   model="gpt-3.5-turbo"
# )
