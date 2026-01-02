import json
from quiz_engine import run_quiz

json_file = r"C:\Users\USER\Desktop\VS Codes\Code_Folder\PROJECT!\quiz_cli\questions.json"
with open(json_file, 'r', encoding='utf-8') as f:
  questions = json.load(f)

# print(questions)
if __name__ == "__main__":
  run_quiz(questions)
