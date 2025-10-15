from flask import Flask, render_template, request, redirect, url_for
from db import (
    get_all_tasks,
    add_task,
    delete_task,
    toggle_task,
    edit_task,
    init_db,
    close_connection,
)
from flask import g

app = Flask(__name__)

# Register teardown function
app.teardown_appcontext(close_connection)


@app.route("/")
def index():
    all_tasks = get_all_tasks()
    due_tasks = [task for task in all_tasks if not task['completed']]
    completed_tasks = [task for task in all_tasks if task['completed']]
    return render_template('index.html', due_tasks=due_tasks, completed_tasks=completed_tasks)

@app.route("/add", methods=["POST"])
def add_task_route():
    title = request.form.get("title")
    if title:
        add_task(title)
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task_route(task_id):
    delete_task(task_id)
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>")
def toggle_task_route(task_id):
    toggle_task(task_id)
    return redirect(url_for("index"))


@app.route("/edit/<int:task_id>", methods=["POST"])
def edit_task_route(task_id):
    new_title = request.form.get("title")
    if new_title:
        edit_task(task_id, new_title)
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db(app)
    app.run(debug=True)
