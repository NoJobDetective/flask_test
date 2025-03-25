# models.py
import json
import os
import uuid
from datetime import datetime

class ProjectManager:
    def __init__(self, data_file='projects.json'):
        self.data_file = data_file
        self.projects = self._load_data()
    
    def _load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {"projects": []}
        else:
            return {"projects": []}
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.projects, f, ensure_ascii=False, indent=2)
    
    def get_all_projects(self):
        return self.projects["projects"]
    
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
        return project_id
    
    def get_project(self, project_id):
        for project in self.projects["projects"]:
            if project["id"] == project_id:
                return project
        return None
    
    def update_project_name(self, project_id, new_name):
        for project in self.projects["projects"]:
            if project["id"] == project_id:
                project["name"] = new_name
                self.save_data()
                return True
        return False
    
    def delete_project(self, project_id):
        for i, project in enumerate(self.projects["projects"]):
            if project["id"] == project_id:
                del self.projects["projects"][i]
                self.save_data()
                return True
        return False
    
    def add_item(self, project_id, point_type, item_text):
        for project in self.projects["projects"]:
            if project["id"] == project_id:
                project["points"][point_type]["items"].append(item_text)
                self.save_data()
                return True
        return False
    
    def update_item(self, project_id, point_type, item_index, new_text):
        project = self.get_project(project_id)
        if project and 0 <= item_index < len(project["points"][point_type]["items"]):
            project["points"][point_type]["items"][item_index] = new_text
            self.save_data()
            return True
        return False
    
    def delete_item(self, project_id, point_type, item_index):
        project = self.get_project(project_id)
        if project and 0 <= item_index < len(project["points"][point_type]["items"]):
            del project["points"][point_type]["items"][item_index]
            self.save_data()
            return True
        return False
