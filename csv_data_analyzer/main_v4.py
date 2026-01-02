import pandas as pd
from pathlib import Path
# expected_cols = ['name', 'age', 'score']
def display_categories(header: list):
  for i, category in enumerate(header):
    print(f"\t{i+1}. {category}")

try:
  file_path = input("Specify the file-path for the CSV File: ")
  file = Path(file_path)
  header_row = pd.read_csv(file_path, nrows=1)
  no_of_cols = len(header_row.columns)
  df = pd.read_csv(file_path, usecols=range(no_of_cols))
  categories = list(df.columns)
  print(f"\nThe categories of data in the CSV are:")
  display_categories(categories)
  while True:
      selected_category = input("What category are you dealing with: ")
      if selected_category in categories:
        break
      else:
        print("Invalid Input. Select one of categories displayed before\n")
  op_list = ['mean', 'sum', 'count']
  op_mapping = {
            'mean': lambda selected_category: df[selected_category].mean() if (df.dtypes[selected_category] == int or df.dtypes[selected_category] == float) else None,
            'sum': lambda selected_category: df[selected_category].sum() if (df.dtypes[selected_category] == int or df.dtypes[selected_category] == float) else None,
            'count': lambda selected_category: df[selected_category].count(),
  }
  while True:
    op = input("What operation Do You Want To Perform (mean, count, sum): ").strip().lower()
    if op in op_list:
      break
    else:
      print("Invalid Input.\n")

  op_func = op_mapping[op]
  result = op_func(selected_category)
  if result == None:
    print("Wrong Operation for Value")
  else:
    print(f"Result: {result}")
except FileNotFoundError:
  print(f"File Not Found: {file.name}")
except PermissionError:
  print(f"Permission to Access File was Denied: {file.name}")
except Exception as err:
  print(f"Error occured: {err}")


#Just found_out how to remove excess data in excess columns