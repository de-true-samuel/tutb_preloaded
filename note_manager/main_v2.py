import json
import os
import sys
from datetime import datetime

def load_config(config_path):
  if not os.path.exists(config_path):
    print(f"The Config File Doesn't Exist: {config_path}")
    sys.exit(1)

  try:
    with open(config_path, 'r', encoding='utf-8') as f:
      config = json.load(f)
  except (json.JSONDecodeError, IOError):
    config = []

  return config

def display_actions(actions):
  print('\n---Note Manager---\n')
  for i, action in enumerate(actions, start=1):
    print(f"{i}. {action}")
  print('\n')

def add_note(notes, config_path):
  title = input("What is the Title of the note: ")
  content = input("THE NOTE:\n")
  tags = input("Tags (comma-separated): ").split(",")
  timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
  max_id = max([note['id'] for note in notes], default=0)
  new_id = max_id + 1
  note = {"id": new_id, "title": title, "content": content, 'tags': [tag.strip() for tag in tags], "created_at": timestamp}
  notes.append(note)
  with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(notes, f, indent=4)
  print("Note added successfully!")

def view_notes(notes):
  if not notes:
    print('No notes available.')
  else:
    for note in notes:
        print("-" * 40)
        print(f"ID: {note['id']}")
        print(f"Title: {note['title']}")
        print(f"Tags: {', '.join(note['tags'])}")
        print(f"Created: {note['created_at']}")
        print(note['content'])
    print('-'*40,)

def delete_notes(notes, config_path):
  if not notes:
    print("No note to delete")
    return
  
  view_notes(notes)
  while True:
    try:
      index = int(input("Pick the index of the note you want to delete: "))
      if 1 <= index <= len(notes):
        removed = notes.pop(index - 1)
        with open(config_path, 'w', encoding='utf-8') as f:
          json.dump(notes, f, indent=4)
        print(f"Note {removed['id']}, has been deleted")
        break
      else:
        print("Select a number from the indexed notes")
    except ValueError:
      print("Select a number from the notes\n")

def search_notes(notes):
  if not notes:
    print("No Notes available.")
    return
  
  keyword = input("Search keyword: ").lower()
  found = False
  for note in notes:
    if keyword in note['title'].lower() or keyword in note['content'].lower() or keyword in [tag.lower() for tag in note['tags']]:
      print('-'*40)
      print(f"[{note['id']}] {note['title']}")
      print(f"\t{note["content"]}")
      found = True
  print('')

  if not found:
    print("No note with the keyword(s) was found")

def filter_notes(notes):
  if not notes:
    print("No note available.")
    return
  keyword = input("Enter the tag name: ")

  found = False
  for note in notes:
    if keyword in note['tags']:
      print('-'*40)
      print(f'[{note['id']}] {note['title']}')
      print(f'Tags: {', '.join(note["tags"])}')
      print(note['content'])
      found = True
  
  if not found:
    print(f"No Note was tagged: {keyword}")
  
def sort_by_title(notes):
  if not notes:
    print("No note available.")
    return
  
  sorted_notes = sorted(notes, key=lambda n: n['title'].lower())
  for note in sorted_notes:
    print('-'*40)
    print(f'Title: {note["title"]}')
    print(note['content'])

def sort_by_date(notes):
  if not notes:
    print("No note available.")
    return
  
  sorted_notes = sorted(notes, key=lambda n: n['created_at'], reverse=True)
  for note in sorted_notes:
    print('-'*40)
    print(f'[{note['id']}] {note['title']}')
    print(f'Title: {note["created_at"]}')
    print(note['content'])

def exit():
  print('\n👋(^ _ ^)\tGoodbye!\n ')
  sys.exit(1)

def main():
  actions = ['Add Note', 'View All Notes', 'Delete Note', 'Search Notes', 'Filter Notes by Tags', 'Sort by Title', 'Sort by Date', 'Exit']
  config_path = 'notes.json'
  notes = load_config(config_path)
  total_actions = len(actions)
  actions_mapping = {
                1: lambda: add_note(notes, config_path),
                2: lambda: view_notes(notes),
                3: lambda: delete_notes(notes, config_path),
                4: lambda: search_notes(notes),
                5: lambda: filter_notes(notes),
                6: lambda: sort_by_title(notes),
                7: lambda: sort_by_date(notes),
                8: lambda: exit(),
  }

  display_actions(actions)

  while True:
    try:
      action_selected = int(input(f"Select any of the options 1-{total_actions}: "))
      if 1 <= action_selected <= len(actions):
        break
      else:
        display_actions(actions)
    except ValueError:
      print(f"Select an integer from 1 to {total_actions}.")

  action = actions_mapping[action_selected]
  action()

if __name__ == "__main__":
  while True:
    main()