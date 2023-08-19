import os
import json

def load_json(sub_path: str, cog: str) -> dict[str, str]:
  data = {}
  filePath = f"data/{cog}/{sub_path}.json"
  
  if not os.path.isfile(filePath):
    with open(filePath, "w") as file:
      json.dump(data, file)
      file.close()
          
  with open(filePath, "r") as file:
    try:
      data = json.load(file)
    except json.decoder.JSONDecodeError:
      data = {}

  return data
  
def save_json(data: dict[str, str], sub_path: str, cog: str) -> None:
  filePath = f"data/{cog}/{sub_path}.json"

  with open(filePath, "w") as file:
    json.dump(data, file)