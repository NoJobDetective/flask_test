import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
PROJECT_DB = 'projects.json'

# JSONファイルからプロジェクト情報を読み込む
def load_projects():
    if not os.path.exists(PROJECT_DB):
        with open(PROJECT_DB, 'w') as f:
            json.dump([], f)
    with open(PROJECT_DB, 'r') as f:
        return json.load(f)

# プロジェクト情報をJSONファイルに保存する
def save_projects(projects):
    with open(PROJECT_DB, 'w') as f:
        json.dump(projects, f, indent=4, ensure_ascii=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    projects = load_projects()
    if request.method == 'POST':
        problem = request.form.get('problem')
        # テキストエリア内の各行をリスト化
        mvp_items = request.form.get('mvp').splitlines()
        later_items = request.form.get('later').splitlines()
        new_project = {
            "problem": problem,
            "mvp": [item.strip() for item in mvp_items if item.strip() != ""],
            "later": [item.strip() for item in later_items if item.strip() != ""]
        }
        projects.append(new_project)
        save_projects(projects)
        return redirect(url_for('index'))
    return render_template('index.html', projects=projects)

if __name__ == '__main__':
    app.run(debug=True)
