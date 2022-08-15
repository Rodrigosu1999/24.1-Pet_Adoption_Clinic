from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """Pets Model."""

    __tablename__ = "pets"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(30),
                     nullable=False,)
    species = db.Column(db.String(30),
                        nullable=False,)
    photo_url = db.Column(db.String,
                          server_default='https://www.tibs.org.tw/images/default.jpg')
    age = db.Column(db.Integer,
                    nullable=True)
    notes = db.Column(db.String)
    available = db.Column(db.Boolean,
                          nullable=False,
                          default=True)
