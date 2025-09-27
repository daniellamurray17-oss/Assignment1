from App.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Resident(db.Model):
    __tablename__ = "residents"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    contact = db.Column(db.String(50), nullable=True)
    street_id = db.Column(db.Integer, db.ForeignKey("streets.id"), nullable=True)

    # Relationships
    stop_requests = db.relationship("StopRequest", backref="resident", lazy=True)
    notifications = db.relationship("Notification", backref="resident", lazy=True)

    def __init__(self, username, password, contact=None, street_id=None):
        self.username = username
        self.set_password(password)
        self.contact = contact
        self.street_id = street_id

    def set_password(self, password):
        """Hashes the password for storage."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifies the password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<Resident id={self.id} username={self.username} street_id={self.street_id}>"
