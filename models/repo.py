from database.database_interface import DatabaseInterface

db = DatabaseInterface.DB
ma = DatabaseInterface.MA


class Repo(db.Model):
    """Describes the database structure for a Repo"""

    # Table Names:
    __tablename__ = 'repos'
    __singular__ = 'repo'

    # create/modify infos:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    github_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    link = db.Column(db.String(256))
    description = db.Column(db.Text, nullable=False)
    num_stars = db.Column(db.Integer, nullable=False)
    pushed_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class RepoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Repo
        load_instance = True
