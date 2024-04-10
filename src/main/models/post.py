from datetime import datetime, timezone
from extensions import db

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(50), nullable=False)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    author = db.relationship(
        'User',
        backref=db.backref('user', uselist=False)
    )

    content = db.Column(db.Text)
    status = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
