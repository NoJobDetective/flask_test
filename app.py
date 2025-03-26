from flask import Flask, render_template, request, redirect, url_for
from models import db, Project, MVPItem, LaterItem

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db.init_app(app)

@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)

@app.route('/add_project', methods=['POST'])
def add_project():
    title = request.form['title']
    project = Project(title=title)
    db.session.add(project)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_item/<int:project_id>/<string:list_type>', methods=['POST'])
def add_item(project_id, list_type):
    content = request.form['content']
    if list_type == 'mvp':
        item = MVPItem(content=content, project_id=project_id)
    else:
        item = LaterItem(content=content, project_id=project_id)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('project_detail', project_id=project_id))
