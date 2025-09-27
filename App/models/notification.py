from App.database import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    route_id = db.Column(db.Integer, db.ForeignKey("routes.id"), nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    route = db.relationship("Route", back_populates="notifications")
    resident = db.relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification id={self.id} resident_id={self.resident_id} route_id={self.route_id} message='{self.message}'>"
