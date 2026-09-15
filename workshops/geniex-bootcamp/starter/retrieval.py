"""Lab 201 baseline: replace the first-document policy with your own selection."""

def select_context(question, documents, max_chars=360):
    # Deliberately weak, executable baseline. Lab 201 supplies the requirements.
    # Do not solve this by hard-coding sample answers or document IDs.
    return documents[:1]
