def print_options(options: list):  # if I put "-> dict" at the end of the function heading, what, will it do in the code
  for i, option in enumerate(options):
    print(f"\t{chr(65 + i)}. {option}")   #Refactor: stopped using the cap_alphabets variable and used a built in chr() method that makes use of the ASCII system

def option_indexing(option: str) -> int | None:
  mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
  option_index = mapping.get(option)
  return option_index   

def run_quiz(QUESTIONS):
  all_user_ans = []
  score = 0
  for i in range(len(QUESTIONS)):
    print(f"{i + 1}. {QUESTIONS[i]['question']}\n")
    print_options(QUESTIONS[i]['options'])
    print("\n")
    while True:
      user_ans = input("ANS ===> ").lower().strip()
      if option_indexing(user_ans) == None:
        print("Invlid option. Select options A-D")
      else: break
    all_user_ans.append(user_ans)
    if QUESTIONS[i]['options'][option_indexing(user_ans)] == QUESTIONS[i]['ans']:
      print("**CORRECT**")
      score += 1
    else:
      print("**WRONG**")
  print(f"Your score is: {score}")