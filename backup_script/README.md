# QUESTIONS
- Can `shutil.copytree()` also be used to copy files instead of folders: -> No it is the `.copy()` and `.copy2()` methods that can be used to copy files

# QUICK TIPS
$ The differnce between `os.makedirs` and `os.makedir` is that the first can create mulitiply parent folder to create the final one, while the later only creates one folder (the child folder), therefore errors can come up if a parent folder for the child folder in os.makedir doesn't exist
$ When using `shutil.copytree()`, note that the destination must not already exist
$ Single quotes aren't allowed in a JSON file
$ When working with absolute file paths, it is better to use `/` instead of `\` or `\\`
$ Error Handling for json files can involve handling `json.JSONDecoderError`
$ There is a type of error that's the parent or container of other errors involving the os, such includes: FileExistsError, FileNotFoundError, PermissionError and even TimeoutError.

RESEARCH SITES:
- https://gemini.google.com/share/2c1dbf50e294
- https://share.google/aimode/UdKqEmDWRFNj9DuDU