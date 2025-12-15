from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Association table for followers
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# Association table for subscriptions
subscriptions = db.Table('subscriptions',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('plan_id', db.Integer, db.ForeignKey('plan.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False) # 'trainer' or 'user'
    
    # Relationships
    plans_created = db.relationship('Plan', backref='trainer', lazy=True)
    followed = db.relationship('User', 
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    
    subscribed_plans = db.relationship('Plan', secondary=subscriptions, backref=db.backref('subscribers', lazy='dynamic'))

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False) # e.g., 30 days
    trainer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)