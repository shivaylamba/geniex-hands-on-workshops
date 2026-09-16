"""Reference implementation. Attempt starter.py before opening this file."""


def check_plan(task_ids, tasks, budget):
    """Return a deterministic plan, or reject invalid/over-budget task selections."""
    if type(budget) is not int or not 1 <= budget <= 240:
        raise ValueError('Budget must be an integer from 1 to 240 minutes')
    if not isinstance(task_ids, list) or not task_ids or len(task_ids) > len(tasks):
        raise ValueError('Select one or more tasks')
    if any(not isinstance(item, str) for item in task_ids):
        raise ValueError('Task IDs must be strings')
    if len(set(task_ids)) != len(task_ids):
        raise ValueError('Duplicate task IDs')
    index = {task['id']: task for task in tasks}
    if any(item not in index for item in task_ids):
        raise ValueError('Unknown task ID')
    selected = [index[item] for item in task_ids]
    total = sum(task['minutes'] for task in selected)
    if total > budget:
        raise ValueError(f'Plan needs {total} minutes but budget is {budget}')
    return {'task_ids': task_ids, 'tasks': selected, 'total_minutes': total,
            'budget_minutes': budget, 'remaining_minutes': budget - total}
