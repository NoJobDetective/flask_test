from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
TODO_FILE = 'data.txt'

# TODOリストをファイルから読み込む関数
def load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    
    with open(TODO_FILE, 'r', encoding='utf-8') as f:
        todos = [line.strip() for line in f.readlines() if line.strip()]
    return todos

# TODOリストをファイルに保存する関数
def save_todos(todos):
    with open(TODO_FILE, 'w', encoding='utf-8') as f:
        for todo in todos:
            f.write(f"{todo}\n")

@app.route('/')
def index():
    todos = load_todos()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    todo = request.form.get('todo')
    if todo and todo.strip():
        todos = load_todos()
        todos.append(todo)
        save_todos(todos)
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todos = load_todos()
    if 0 <= todo_id < len(todos):
        todos.pop(todo_id)
        save_todos(todos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
