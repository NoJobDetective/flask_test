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

# テンプレートフォルダがない場合に備えて、HTMLを文字列として定義
@app.route('/templates/index.html')
def get_template():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>TODOリスト</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin: 10px 0;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
        }
        form {
            margin: 20px 0;
            display: flex;
        }
        input[type="text"] {
            flex-grow: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px 0 0 5px;
        }
        button {
            padding: 10px 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 0 5px 5px 0;
            cursor: pointer;
        }
        .delete {
            color: #f44336;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <h1>TODOリスト</h1>
    
    <form action="/add" method="post">
        <input type="text" name="todo" placeholder="新しいTODOを入力" required>
        <button type="submit">追加</button>
    </form>
    
    <ul>
        {% for todo in todos %}
        <li>
            {{ todo }}
            <a href="/delete/{{ loop.index0 }}" class="delete">削除</a>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
"""

if __name__ == '__main__':
    # templatesディレクトリを作成
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # index.htmlを作成
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(app.view_functions['get_template'].__doc__ or 
                app.view_functions['get_template']())
    
    app.run(host='0.0.0.0', port=5000, debug=True)
