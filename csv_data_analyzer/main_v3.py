import pandas as pd

df = pd.read_csv('Book1.csv')

mean_score = df["score"].mean()
scores_above_mean = df[df['score'] > mean_score]['score'].count()
mean_age = df['age'].mean()
participants = df['name'].count()

print("-"*50)
print(f'|\t Total Participants: {participants}')
print(f'|\t Average Score: {round(mean_score, 3)}')
print(f'|\t Average Age of Participants: {round(mean_age, 2)}')
print(f'|\t Number of Participants With Scores Above Average: {scores_above_mean}')
print("-"*50)
