import os
from flask import Flask, render_template
from github import Github
from models.repo import Repo, RepoSchema
from database.database_interface import DatabaseInterface

project_id = os.environ.get('CLOUD_PROJECT_ID')
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_ip = os.environ.get('CLOUD_SQL_DATABASE_IP')
instance_name = os.environ.get('CLOUD_SQL_INSTANCE_NAME')
env = os.environ.get('ENV', 'dev')

# Initialize Flask
app = Flask(__name__)

if env == 'dev':
    # Set sqlite database path
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'database/db.sqlite3')}"
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_ip}/{db_name}?charset=utf8mb4"

# Initialize Interfaces
DatabaseInterface(app)

# Initialize github library
PER_PAGE = 10

# Initialize github library
git = Github(per_page=PER_PAGE)


@app.route('/')
def top():
    # Display all repos in the database
    return render_template('index.html', repos=Repo.query.order_by(Repo.num_stars.desc()).all(), num=PER_PAGE)


@app.route('/repo_info/<github_id>')
def repo_info(github_id):
    # Display info for the specific repo requested
    return render_template('repo.html', repo=Repo.query.filter_by(github_id=github_id).one())


@app.route('/refresh')
def refresh():
    # Refresh the list of top github repos stored in the database

    # Find the top github repos, limited to the per_page configured in the lib initialization
    top_repos = git.search_repositories(query='stars:>1', sort='stars').get_page(0)

    # Create list of Repo dicts containing only the fields we want to store
    repos = [{'github_id': r.id, 'name': r.name, 'link': r.html_url, 'description': r.description, 'pushed_at': r.pushed_at.isoformat(), 'created_at': r.created_at.isoformat(), 'num_stars': r.stargazers_count} for r in top_repos]

    # Truncate the existing data
    meta = DatabaseInterface.DB.metadata
    for table in reversed(meta.sorted_tables):
        DatabaseInterface.DB.session.execute(table.delete())
    DatabaseInterface.DB.session.commit()

    # Validate and create new Repo entries
    repos = RepoSchema(exclude=['id']).load(repos, many=True)
    DatabaseInterface.DB.session.add_all(repos)
    DatabaseInterface.DB.session.commit()
    return render_template('index.html', repos=repos, num=PER_PAGE)


if __name__ == '__main__':
    # Create the database if it does not already exist
    with app.app_context():
        DatabaseInterface.DB.create_all()

    # Run the application
    app.run()
