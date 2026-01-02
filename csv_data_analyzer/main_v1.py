# Some features of Version 2 was added here cause version 1 was just to print out the list of each row using csv.reader()
import csv
import sys
from pathlib import Path


def analyze_csv(file_path: str) -> tuple:
  participants = 0
  average_score = 0
  total_score = 0
  scores = []
  total_age = 0
  average_age = 0
  no_above_average_scores = 0
  with open(file_path, 'r') as f:
    csv_reader = csv.reader(f)
    header = next(csv_reader)   #this skips and save the header of the lists
    age_index = header.index("age")
    score_index = header.index("score")
    for row in csv_reader:
      score = int(row[score_index])
      age = int(row[age_index])
      participants += 1
      scores.append(score)
      total_age += age
    
    total_score = sum(score for score in scores)
    average_age = total_age / participants if participants > 0 else 0
    average_score = total_score / participants if participants > 0 else 0
    no_above_average_scores = sum(1 for score in scores if score > average_score)
  return participants, average_age, average_score, no_above_average_scores

if __name__ == "__main__":
  try:
    file_path = sys.argv[1] if len(sys.argv) > 1 else "data.csv"
    file = Path(file_path)
    participants, average_age, average_score, no_above_average_scores = analyze_csv(file_path)
  except FileNotFoundError:
    print(f"File not Found: {file.name}")
  except PermissionError:
    print(f"Permission Denied: {file.name}")
  except Exception as err:
    print(f"Error Found: {err}")

  print("-"*50)
  print(f'|\t Total Participants: {participants}')
  print(f'|\t Average Score: {round(average_score, 3)}')
  print(f'|\t Average Age of Participants: {round(average_age, 2)}')
  print(f'|\t Number of Participants With Scores Above Average: {no_above_average_scores}')
  print("-"*50)
