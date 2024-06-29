from openai import OpenAI
client = OpenAI(api_key='sk-proj-OhhalHV4AzxpDSaDOha9T3BlbkFJ6ppBjN1Z2hgoPQDHj2yz')

# response = client.files.create(
#   file=open("gpt.jsonl", "rb"),
#   purpose="fine-tune"
# )

# print(response)

client.fine_tuning.jobs.create(
  training_file="file-qsMgQJVneo6VUeG28FRFkxzm",
  model="gpt-3.5-turbo"
)
