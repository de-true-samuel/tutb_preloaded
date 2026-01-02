
# Situations:
- How can I curb an error when there is a row no values at all or no value at a specific column (DONE)
- How to remove excess data from a csv file (DONE in v4)

# Quick Tips Discovered
$ When importing or reading a file, be sure to be careful of the cwd - change cwd to dir of the file you want to run and then make all file paths in the code relative to it
$ When reading the values of in a csv row, take note that all the characters after the ',' is accounted for, including the spaces
$ When I wanted to get number of those with scores above mean in version 3, I noticed that using conditions of df such as: `df[df['score'] > mean].count()` would count all the columns as long as the score of such individual is above the mean_age, so after lots of experiments I got it I just put specified it is score I wanted by using: `df[df['score] > mean_age]['score'].count()`, just by appending ['score'] I was able to specify and count that particular one.
$ Putting a fucntion that just prints and returns nothing inside a `print()` will cause the function to print first, then the normal text will be printed out, but in the place where you put the function `None` will be displayed
$ When using `try..except` make sure you invlove all variables and data connected to the one initially in `try` section, so as to be able to handle all error
$ `NameError` is an error that usually occurs when a function receives an argument that is not defined
$ There is a difference between `op_mapping.get(op)` and `op_mapping[op]`, the first return the function object the later makes one a function
$ A fuuntion that was made a function by equation to a lamba, should have the required arguments of the lamda when executing

# Sites where I made research - samnick account
- https://gemini.google.com/share/72cf94183847
- https://share.google/aimode/lBOwmhKqGWUNJDJ6Y