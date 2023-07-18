import click
import json_manager

# To see more information about click: https://click.palletsprojects.com/en/8.1.x/
@click.group()
def cli():
    pass

# To create a new task
@cli.command()
@click.option('--title', required=True, help='Name of the task')
@click.option('--subject', required=True, help='Subject to which the task belongs')
@click.option('--description', required=True, help='A very short description of the task')
@click.option('--deadline', required=True, help='Task deadline (Format: mm/dd/yyyy)')
# To be able to use ctx
@click.pass_context 
# How do we receive those parameters? (ctx = context(the cli itself))
def new(ctx, title, subject, description, deadline):
    # Checking that the data exists
    if not title or not subject or not description or not deadline:
        ctx.fail('All data is required')
    else:
        existing_tasks = json_manager.read_json()
        new_id = len(existing_tasks) + 1
        new_task = {
            'id': new_id,
            'title': title,
            'subject': subject,
            'description': description,
            'deadline': deadline
        }
        existing_tasks.append(new_task)
        json_manager.write_json(existing_tasks)
        # print(f"{tasks} (id: {id}) was registered successfully")
        print(f"> {title} (id: {new_id}) was registered successfully")

# To read data from database
@cli.command()
def tasks():
    tasks = json_manager.read_json()
    for task in tasks:
        print(f"{task['id']} -> {task['title']} - {task['subject']} - {task['description']} - {task['deadline']}")

# To search for a single task
@cli.command()
@click.argument('id', type=int)
def task(id):
    existing_tasks = json_manager.read_json()
    # How to use next(): https://www.w3schools.com/python/python_ref_functions.asp
    # We can do this: task = next((task for task in existing_tasks if task['id'] == id), None) or
    task = next(iter([task for task in existing_tasks if task['id'] == id]), None)

    if task is None:
        print(f"> Task with id = {id} was not found")
    else:
        print(f"{task['id']} -> {task['title']} - {task['subject']} - {task['description']} - {task['deadline']}")

# To update any task
@cli.command()
@click.argument('id', type=int)
@click.option('--title', help='New name for the task')
@click.option('--subject', help='New subject to which the task belongs')
@click.option('--description', help='A very short new description for the task')
@click.option('--deadline', help='New task deadline (Format: mm/dd/yyyy)')
def update(id, title, subject, description, deadline):
    existing_tasks = json_manager.read_json()
    for task in existing_tasks:
        if task['id'] == id:
            if title is not None:
                task['title'] = title
            if subject is not None:
                task['subject'] = subject
            if description is not None:
                task['description'] = description
            if deadline is not None:
                task['deadline'] = deadline
            break
    json_manager.write_json(existing_tasks)
    print(f"> Task with id = {id} was updated successfully")

# To delete any task
@cli.command()
@click.argument('id', type=int)
def delete(id):
    existing_tasks = json_manager.read_json()
    task = next(iter([task for task in existing_tasks if task['id'] == id]), None)

    if task is None:
        print(f"> Task with id = {id} was not found")
    else:
        existing_tasks.remove(task)
        json_manager.write_json(existing_tasks)
        print(f"> Task with id = {id} was deleted successfully")

if __name__ == '__main__':
    cli()
