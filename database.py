from re import S
import sqlite3
from turtle import pos
from typing import List
import datetime
from model import Todo

conn = sqlite3.connect('tasks_to_do.db')

c = conn.cursor() 

def build_table(): 
    c.execute("""CREATE TABLE IF NOT EXISTS tasks_to_do (
                                               task text, 
                                               category text, 
                                               date_added text, 
                                               date_completed text, 
                                               status text,
                                               position integer )""")


#call the function we made to build the table 
build_table() 

#function tot insert tasks 
def insert_task(task: Todo):
    c.execute('select count(*) FROM tasks_to_do')
    count = c.fetchone()[0]
    task.position = count if count else 0
    with conn: 
        c.execute('INSERT INTO tasks_to_do VALUES ( :task, :category, :date_added, :date_completed, :status, :position)',
        {'task': task.task, 'category': task.category, 'date_added': task.date_added, 'date_completed': task.date_completed,
         'status': task.status, 'position': task.position})

#create function to retrieve all of the tasks 
def get_all_tasks() -> List[Todo]:
    c.execute('select * from tasks_to_do')
    results = c.fetchall()
    tasks = [] 
    for result in results: 
        tasks.append(Todo(*result))
    return tasks 

#create function to delete a task 
def delete_task(position): 
    c.execute('select count(*) from tasks_to_do')
    count = c.fetchone()[0]

    with conn: 
        c.execute("DELETE from task_to_do WHERE position= :position",{"position": position})
        for pos in range(position+1, count): 
            change_position(pos, pos-1, False)

#create a function which shifts all of the positions every time something is deleted from the middle 
def change_position(old_position: int, new_position: int, commit = True): 
    c.execute("UPDATE tasks_to_do SET position= :old_position WHERE new_position= :new_position", 
             {'old_position': old_position, 'new_position': new_position})
    if commit:
        conn.commit() 

#create a function for updating tasks 
def update_task(position: int, task: str, category: str): 
    with conn: 
        if task is not None and category is not None: 
            c.execute("UPDATE tasks_to_do SET task= :task, category=:category WHERE position= :position",
            {'task': task, 'category': category, 'position': position})
        elif task is not None: 
            c.execute("UPDATE tasks_to_do SET task= :task WHERE position= :position",
            {'task': task, 'category': category, 'position': position})
        elif category is not None: 
            c.execute("UPDATE tasks_to_do SET category= :category WHERE position= :position",
            {'task': task, 'category': category, 'position': position})

#create a function for a completed task 
def complete_task(position: int): 
    with conn: 
        c.execute("UPDATE tasks_to_do SET status= :status, date_completed= :date_completed WHERE position= :position",
                 {'status': 'complete', 'date_completed': datetime.datetime.now().isoformat()})