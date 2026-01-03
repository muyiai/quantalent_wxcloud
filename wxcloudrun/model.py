from datetime import datetime

from wxcloudrun import db


# 面试题库
class Questions(db.Model):
    __tablename__ = 'Questions'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    hint = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(255), nullable=False)
    firms = db.Column(db.String(255), nullable=False)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


class Companies(db.Model):
    __tablename__ = 'Companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
