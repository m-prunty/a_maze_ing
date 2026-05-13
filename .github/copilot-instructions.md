

# COPILOT INSTRUCTIONS:
## Docstrings
- MUST be less than 79 characters long, including the triple double quotes.
- If a docstring deserrves a singleline only yet chars exceed79 chars drop superlatives and unnecessary words to fit within the limit. For example, instead of "This function is responsible for parsing the configuration file and returning a dictionary of settings", you could write "Parse config file and return settings as dict".
- if necessary use abbreviations to fit within the line length constraint, but only if they are commonly understood and do not sacrifice clarity. For example, instead of "This function takes a list of numbers and returns the sum", you could write "Sum a list of nums",  integer->int, string->str, list->lst, dictionary->dict, etc.
- Also avoid using words like "This function", "This method", "This class", etc. in the docstring, as it is redundant and does not add any meaningful information. Instead, focus on describing what the function, method, or class does in a clear and concise manner. For example, instead of "This function takes a list of numbers and returns the sum", you could write "Return the sum of a list of numbers".
- Use docstrings to describe the purpose and behavior of functions, classes, and modules.
- First line must be imperative mood (e.g. "Parse the config" not "Parses the config")
- No trailing period on summary line
- If the docstring is more than one line, the second line should be blank, and the rest of the description should be indented to the same level as the first line.
- All lines of code MUST be less than 79 characters long, including docstrings. If a docstring exceeds this limit, it should be wrapped appropriately to fit within the line length constraint.
- keep the language in docstrings terse and to the point, avoiding unnecessary words or phrases. Focus on conveying the essential information clearly and concisely.
- Use triple double quotes for docstrings, even for one-liners.
- single purpose functions that are less than 5 lines can have a one-line docstring, but it must still follow the triple double quotes convention. For example:
