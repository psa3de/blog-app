import uuid
from extensions import db, bcrypt
from datetime import datetime, timezone
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, SerializerMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, index=True)
    public_id = db.Column(db.String(50), unique=True, default=lambda:str(uuid.uuid4()), index=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    admin = db.Column(db.Boolean)
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password: str):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    
    serialize_rules = ('-_password_hash', )
