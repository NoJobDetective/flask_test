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

# 編集画面の表示および更新処理
@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_project(index):
    projects = load_projects()
    if index < 0 or index >= len(projects):
        return redirect(url_for('index'))
    if request.method == 'POST':
        # 編集後の内容を取得
        problem = request.form.get('problem')
        mvp_items = request.form.get('mvp', '').splitlines()
        later_items = request.form.get('later', '').splitlines()
        updated_project = {
            "problem": problem,
            "mvp": [item.strip() for item in mvp_items if item.strip() != ""],
            "later": [item.strip() for item in later_items if item.strip() != ""]
        }
        projects[index] = updated_project
        save_projects(projects)
        return redirect(url_for('index'))
    # GET時は既存のデータを編集フォームに渡す
    project = projects[index]
    return render_template('edit.html', project=project, index=index)

# 削除処理
@app.route('/delete/<int:index>', methods=['POST'])
def delete_project(index):
    projects = load_projects()
    if 0 <= index < len(projects):
        projects.pop(index)
        save_projects(projects)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
