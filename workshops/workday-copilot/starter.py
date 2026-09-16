"""Learner file: implement one function in 201; harden it with tests in 301."""


def check_plan(task_ids, tasks, budget):
    """Contract:

    task_ids: nonempty list of unique known string IDs.
    tasks: trusted bundled records containing id, title, minutes.
    budget: integer (not bool), 1..240, supplied by the user, not the model.

    Reject bad IDs, duplicates, invalid budgets and over-budget plans with ValueError.
    Return a dict with task_ids, tasks (selected records in requested order),
    total_minutes, budget_minutes, remaining_minutes. See the lab for examples.
    Never ask the language model to do the sum or to authorize its own budget.
    """
    raise NotImplementedError('201: implement check_plan in starter.py')
