# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import ProjectManager

app = Flask(__name__)
project_manager = ProjectManager()

@app.route('/')
def index():
    projects = project_manager.get_all_projects()
    return render_template('index.html', projects=projects)

def create_project(self, name):
    project_id = str(uuid.uuid4())
    new_project = {
        "id": project_id,
        "name": name,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "points": {
            "definition": {
                "title": "1. 解決したい問題の定義",
                "items": []
            },
            "mvp": {
                "title": "2. MVP（最低限の機能）",
                "items": []
            },
            "backlog": {
                "title": "3. 追加機能（後回しリスト）",
                "items": []
            }
        }
    }
    self.projects["projects"].append(new_project)
    self.save_data()
    return project_id  # 文字列のproject_idを返す

@app.route('/project/<project_id>')
def view_project(project_id):
    project = project_manager.get_project(project_id)
    if project:
        return render_template('project.html', project=project)
    return redirect(url_for('index'))

@app.route('/project/<project_id>/update', methods=['POST'])
def update_project(project_id):
    name = request.form.get('project_name')
    if name and name.strip():
        project_manager.update_project_name(project_id, name)
    return redirect(url_for('view_project', project_id=project_id))

@app.route('/project/<project_id>/delete', methods=['POST'])
def delete_project(project_id):
    project_manager.delete_project(project_id)
    return redirect(url_for('index'))

@app.route('/project/<project_id>/item/add', methods=['POST'])
def add_item(project_id):
    point_type = request.form.get('point_type')
    item_text = request.form.get('item_text')
    if point_type and item_text and item_text.strip():
        project_manager.add_item(project_id, point_type, item_text)
    return redirect(url_for('view_project', project_id=project_id))

@app.route('/project/<project_id>/item/update', methods=['POST'])
def update_item(project_id):
    point_type = request.form.get('point_type')
    item_index = int(request.form.get('item_index'))
    new_text = request.form.get('new_text')
    
    if point_type and new_text and new_text.strip():
        success = project_manager.update_item(project_id, point_type, item_index, new_text)
        return jsonify({"success": success})
    return jsonify({"success": False}), 400

@app.route('/project/<project_id>/item/delete', methods=['POST'])
def delete_item(project_id):
    point_type = request.form.get('point_type')
    item_index = int(request.form.get('item_index'))
    
    success = project_manager.delete_item(project_id, point_type, item_index)
    return jsonify({"success": success})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
