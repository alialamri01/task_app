#add imports 
from email import header
from typing import Collection
import typer
from rich.console import Console
from rich.table import Table 



console = Console() 

app = typer.Typer() 


#adds a task to the given category
@app.command(short_help='adds an task') 
def add(task: str, category: str):
    typer.echo(f"adding {task}, {category}")
    show()

#removes a task
@app.command(short_help='deletes a task')
def delete(position: int):
    typer.echo(f"deleting {position}")
    show()

#updates a task 
@app.command(short_help='updates a task') 
def update(position: int, task: str = None, category: str = None):
    typer.echo(f"updating {position}") 
    show()

#marks the task completed
app.command(short_help='marks a task complete') 
def complete(position: int):
    typer.echo(f"completed {position}")
    show()

#this command shows our tasks
@app.command(short_help='show the table of tasks') 
def show(): 
    tasks = [("Laundry", "Chores"), ("Back Day","Excercise")]
    console.print("[bold magenta]Todos[/bold magenta]!","💻")

    table = Table(show_header=True, header_style="bold blue")

    table.add_column("#", style='dim', width=6); 
    table.add_column("Task", min_width=20); 
    table.add_column("Category",min_width=12, justify='right')
    table.add_column("Status", min_width=12, justify='right')

    #create the colors for each category
    def get_category_color(category):
        COLORS = {'Work': 'cyan', 'Chores': 'green', 'Hobbies': 'white', 'Excercise': 'blue'}
        if category in COLORS:
            return COLORS[category]
        return 'white'

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task[1])
        is_done_str = '✅' if True == 2 else '❌'
        table.add_row(str(idx), task[0], f'[{c}]{task[1]}[/{c}]', is_done_str)
    console.print(table)


if __name__ == "__main__":
    app() 