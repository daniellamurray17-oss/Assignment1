from App.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Driver(db.Model):
    __tablename__ = "drivers"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    contact = db.Column(db.String(50), nullable=True)

    # Relationships
    routes = db.relationship("Route", backref="driver", lazy=True)
    notifications = db.relationship("Notification", backref="driver", lazy=True)

    def __init__(self, username, password, contact=None):
        self.username = username
        self.set_password(password)
        self.contact = contact

    def set_password(self, password):
        """Hashes the password before saving."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifies the password against the hash."""
        return check_password_hash(self.password, password)

    def get_json(self):
        """Return a JSON-friendly dict of driver details."""
        return {
            "id": self.id,
            "username": self.username,
            "contact": self.contact,
            "routes": [r.id for r in self.routes],
            "notifications": [n.id for n in self.notifications]
        }

    def __repr__(self):
        return f"<Driver id={self.id} username={self.username}>"
