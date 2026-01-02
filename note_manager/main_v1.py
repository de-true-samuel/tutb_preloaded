import json
import os
import sys

def display_actions(actions):
  print('\n---Note Manager---\n')
  for i, action in enumerate(actions, start=1):
    print(f"{i}. {action}")
  print('\n')

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

def add_note(notes, config_path):
  title = input("What is the Title of the note: ")
  content = input("THE NOTE:\n")
  num_of_notes = len(notes)
  index = num_of_notes + 1
  note = {"index": index, "title": title, "content": content}
  notes.append(note)
  with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(notes, f, indent=4)
  print("Note added successfully!")

def view_notes(notes):
  total_notes = len(notes)
  if not notes:
    print('No notes available.')
  else:
    for i in range(total_notes):
      print('-'*50)
      print(f"\tIndex: {notes[i]['index']}, Title: {notes[i]['title']}")
      print(f"\tNote: {notes[i]['content']}")
    print('-'*50,)

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
        print(f"Note {removed['index']}, has been deleted")
        break
      else:
        print("Select a number from the indexed notes")
    except ValueError:
      print("Select a number from the notes\n")

def main():
  actions = ['Add Note', 'View All Notes', 'Delete Note']
  config_path = 'notes.json'
  notes = load_config(config_path)
  total_actions = len(actions)
  actions_mapping = {
                1: lambda: add_note(notes, config_path),
                2: lambda: view_notes(notes),
                3: lambda: delete_notes(notes, config_path),
  }

  # Display options and ask for inputs
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
    to_continue = input("Do you wish to use the **Note Manager** again (y/n): ").lower()
    if to_continue != 'y':
      print('\nGoodbye!\n')
      break