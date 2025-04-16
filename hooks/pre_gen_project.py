import re
import sys

MODULE_REGEX = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

project_slug = "{{ cookiecutter.project_slug }}"
author_email = "{{ cookiecutter.author_email }}"

if not re.match(MODULE_REGEX, project_slug):
    print(
        f"ERROR: The project slug ({project_slug}) is not a valid Python module name."
    )
    print(
        "Please use only letters, numbers, and underscores, starting with a letter or underscore."
    )
    # Exit to cancel project generation
    sys.exit(1)

if not re.match(EMAIL_REGEX, author_email):
    print(f"ERROR: The author email ({author_email}) does not appear to be valid.")
    # Exit to cancel project generation
    sys.exit(1)

print("Pre-generation validation checks passed.")
