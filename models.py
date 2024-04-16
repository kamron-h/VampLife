from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:vcbMOixkmIcpljbwqeKnKctjcCuQSgdh@monorail.proxy.rlwy.net:40444/railway'


migrate = Migrate(app, db)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    has_shadow = db.Column(db.Boolean, default=False)
    complexion = db.Column(db.String(20))
    dislike_garlic = db.Column(db.Boolean, default=False)
    accent = db.Column(db.Boolean, default=False)  # Changed to Boolean as it makes more sense
    vampire_likelihood = db.Column(db.String(20))

    def __init__(self, has_shadow, complexion, dislike_garlic, accent, vampire_likelihood):
        self.has_shadow = has_shadow
        self.complexion = complexion
        self.dislike_garlic = dislike_garlic
        self.accent = accent
        self.vampire_likelihood = vampire_likelihood
